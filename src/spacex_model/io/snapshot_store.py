"""Diagnostic snapshot store and per-cell xlsx version diff (L3)."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.config.settings import _default_cell_history_dir, get_repo_root
from spacex_model.engine.label_lookup import normalize_label
from spacex_model.inputs.s1_2025_anchors import S1_INGEST_ANCHORS_2025
from spacex_model.io.excel_ingest import IngestResult


def _sheet_slug(sheet: str) -> str:
    from spacex_model.service.sheets_meta import sheet_for_name

    meta = sheet_for_name(sheet)
    return meta.slug if meta else sheet.lower().replace(" ", "_")


def _is_section_header(label: str) -> bool:
    return label.startswith("§") or label.startswith("▸") or label.isupper()


def _label_lineage_map() -> dict[tuple[str, str], str]:
    from spacex_model.service.grid import _LABEL_LINEAGE

    return _LABEL_LINEAGE

_CHANGE_KINDS = ("initial", "value", "formula", "input", "anchor")

_CHANGE_SCHEMA = pa.schema(
    [
        ("cell_key", pa.string()),
        ("lineage_key", pa.string()),
        ("sheet", pa.string()),
        ("row", pa.int32()),
        ("year", pa.int32()),
        ("prior_value", pa.float64()),
        ("new_value", pa.float64()),
        ("delta", pa.float64()),
        ("formula_prior", pa.string()),
        ("formula_new", pa.string()),
        ("model_version", pa.string()),
        ("commit_sha", pa.string()),
        ("timestamp", pa.string()),
        ("change_kind", pa.string()),
    ]
)

_SNAPSHOT_SCHEMA = pa.schema(
    [
        ("cell_key", pa.string()),
        ("lineage_key", pa.string()),
        ("sheet", pa.string()),
        ("row", pa.int32()),
        ("year", pa.int32()),
        ("value", pa.float64()),
        ("formula", pa.string()),
        ("model_version", pa.string()),
    ]
)

_ANCHOR_LABELS: frozenset[str] = frozenset(
    spec.assumptions_label or spec.name for spec in S1_INGEST_ANCHORS_2025
)


def cell_history_dir() -> Path:
    """Persistent store for per-cell ingest diffs."""
    override = __import__("os").environ.get("SPACEX_MODEL_CELL_HISTORY_DIR")
    if override:
        return Path(override).resolve()
    return _default_cell_history_dir()


def _changes_path(store_dir: Path) -> Path:
    return store_dir / "changes.parquet"


def _snapshot_path(store_dir: Path) -> Path:
    return store_dir / "value_snapshot.parquet"


def _metadata_path(store_dir: Path) -> Path:
    return store_dir / "metadata.json"


def _serialize_value(value: Any) -> Any:
    if isinstance(value, float):
        return value
    if isinstance(value, (int, str, bool)) or value is None:
        return value
    return str(value)


def _coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            return float(text)
        except ValueError:
            return None
    return None


def _values_equal(a: Any, b: Any) -> bool:
    fa, fb = _coerce_float(a), _coerce_float(b)
    if fa is None and fb is None:
        return True
    if fa is None or fb is None:
        return str(a) == str(b)
    return abs(fa - fb) < 1e-9


def _lineage_key_for_cell(sheet: str, label: str, row: int, year: int) -> str:
    mapped = _label_lineage_map().get((sheet, label))
    if mapped:
        return mapped
    slug = _sheet_slug(sheet)
    return f"grid.{slug}.R{row}.{year}"


def storage_cell_key(sheet: str, row: int, year: int) -> str:
    """Canonical per-cell key (sheet/row/year) for the change store."""
    return f"grid.{_sheet_slug(sheet)}.R{row}.{year}"


def _row_formula_index(ingest: IngestResult) -> dict[tuple[str, int], str | None]:
    """First formula string per (sheet, row) — sufficient for row-level formula diffs."""
    out: dict[tuple[str, int], str | None] = {}
    for cell in ingest.formula_pass.formulas:
        key = (cell.sheet, cell.row)
        if key not in out and cell.formula:
            out[key] = cell.formula
    return out


def _classify_change_kind(
    sheet: str,
    label: str,
    *,
    value_changed: bool,
    formula_changed: bool,
) -> str:
    if formula_changed:
        return "formula"
    if sheet == "Assumptions" and value_changed:
        return "input"
    if normalize_label(label) in {normalize_label(a) for a in _ANCHOR_LABELS} and value_changed:
        return "anchor"
    return "value"


def _iter_ingest_cells(ingest: IngestResult) -> list[dict[str, Any]]:
    """Yield one record per year-column grid cell with a label."""
    formulas = _row_formula_index(ingest)
    cells: list[dict[str, Any]] = []
    for sheet, labels in ingest.value_pass.labels_by_sheet.items():
        if sheet == "Claude Log":
            continue
        for row, label in labels.items():
            if _is_section_header(label):
                continue
            formula = formulas.get((sheet, row))
            for year in range(FIRST_YEAR, LAST_YEAR + 1):
                raw = ingest.value_pass.cached_values.get((sheet, row, year))
                if raw is None and formula is None:
                    continue
                cell_key = storage_cell_key(sheet, row, year)
                lineage_key = _lineage_key_for_cell(sheet, label, row, year)
                cells.append(
                    {
                        "cell_key": cell_key,
                        "lineage_key": lineage_key,
                        "sheet": sheet,
                        "row": row,
                        "year": year,
                        "label": label,
                        "value": raw,
                        "formula": formula,
                    }
                )
    return cells


def _ingest_fingerprint(ingest: IngestResult) -> str:
    parts: list[str] = [ingest.workbook_path.name]
    for cell in sorted(_iter_ingest_cells(ingest), key=lambda c: c["cell_key"]):
        val = _coerce_float(cell["value"])
        parts.append(f"{cell['cell_key']}={val}:{cell.get('formula') or ''}")
    digest = hashlib.sha256("\n".join(parts).encode()).hexdigest()
    return digest


def _read_parquet_rows(path: Path, schema: pa.Schema) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    table = pq.read_table(path)  # type: ignore[no-untyped-call]
    rows: list[dict[str, Any]] = table.to_pylist()
    return rows


def _write_parquet_rows(path: Path, rows: list[dict[str, Any]], schema: pa.Schema) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        pq.write_table(schema.empty_table(), path)  # type: ignore[no-untyped-call]
        return
    columns: dict[str, list[Any]] = {name: [] for name in schema.names}
    for row in rows:
        for name in schema.names:
            columns[name].append(row.get(name))
    pq.write_table(pa.table(columns, schema=schema), path)  # type: ignore[no-untyped-call]


def _git_sha() -> str | None:
    import subprocess

    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=get_repo_root(),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def record_ingest_changes(
    ingest: IngestResult,
    *,
    store_dir: Path | None = None,
) -> list[dict[str, Any]]:
    """Diff ingest against prior snapshot; append per-cell change records."""
    root = store_dir or cell_history_dir()
    root.mkdir(parents=True, exist_ok=True)

    fingerprint = _ingest_fingerprint(ingest)
    meta_path = _metadata_path(root)
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("fingerprint") == fingerprint:
            return []

    prior_rows = _read_parquet_rows(_snapshot_path(root), _SNAPSHOT_SCHEMA)
    prior_by_key = {row["cell_key"]: row for row in prior_rows}

    now = datetime.now(UTC).isoformat()
    model_version = ingest.workbook_path.name
    commit_sha = _git_sha() or ""

    new_changes: list[dict[str, Any]] = []
    new_snapshot: list[dict[str, Any]] = []

    for cell in _iter_ingest_cells(ingest):
        cell_key = cell["cell_key"]
        prior = prior_by_key.get(cell_key)
        prior_value = prior.get("value") if prior else None
        prior_formula = prior.get("formula") if prior else None
        new_value = cell["value"]
        new_formula = cell.get("formula")

        value_changed = prior is not None and not _values_equal(prior_value, new_value)
        formula_changed = prior is not None and (prior_formula or "") != (new_formula or "")

        if prior is None:
            change_kind = "initial"
            delta = None
            new_changes.append(
                {
                    "cell_key": cell_key,
                    "lineage_key": cell["lineage_key"],
                    "sheet": cell["sheet"],
                    "row": cell["row"],
                    "year": cell["year"],
                    "prior_value": None,
                    "new_value": _coerce_float(new_value),
                    "delta": delta,
                    "formula_prior": None,
                    "formula_new": new_formula,
                    "model_version": model_version,
                    "commit_sha": commit_sha,
                    "timestamp": now,
                    "change_kind": change_kind,
                }
            )
        elif value_changed or formula_changed:
            pv = _coerce_float(prior_value)
            nv = _coerce_float(new_value)
            delta = (nv - pv) if pv is not None and nv is not None else None
            change_kind = _classify_change_kind(
                cell["sheet"],
                cell["label"],
                value_changed=value_changed,
                formula_changed=formula_changed,
            )
            new_changes.append(
                {
                    "cell_key": cell_key,
                    "lineage_key": cell["lineage_key"],
                    "sheet": cell["sheet"],
                    "row": cell["row"],
                    "year": cell["year"],
                    "prior_value": pv,
                    "new_value": nv,
                    "delta": delta,
                    "formula_prior": prior_formula,
                    "formula_new": new_formula,
                    "model_version": model_version,
                    "commit_sha": commit_sha,
                    "timestamp": now,
                    "change_kind": change_kind,
                }
            )

        new_snapshot.append(
            {
                "cell_key": cell_key,
                "lineage_key": cell["lineage_key"],
                "sheet": cell["sheet"],
                "row": cell["row"],
                "year": cell["year"],
                "value": _coerce_float(new_value),
                "formula": new_formula,
                "model_version": model_version,
            }
        )

    if new_changes:
        existing = _read_parquet_rows(_changes_path(root), _CHANGE_SCHEMA)
        _write_parquet_rows(_changes_path(root), existing + new_changes, _CHANGE_SCHEMA)

    _write_parquet_rows(_snapshot_path(root), new_snapshot, _SNAPSHOT_SCHEMA)
    meta_path.write_text(
        json.dumps(
            {
                "fingerprint": fingerprint,
                "model_version": model_version,
                "timestamp": now,
                "commit_sha": commit_sha,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return new_changes


def resolve_storage_keys(
    key: str,
    *,
    year: int | None = None,
    ingest: IngestResult | None = None,
) -> list[str]:
    """Map a lineage/grid key to storage cell_key(s)."""
    import re

    if re.fullmatch(r"grid\.\w+\.R\d+\.\d{4}", key):
        return [key]

    if year is not None:
        for (sheet, label), mapped in _label_lineage_map().items():
            if mapped == key:
                labels = {}
                if ingest is not None:
                    labels = ingest.value_pass.labels_by_sheet.get(sheet, {})
                for row, lbl in labels.items():
                    if lbl == label:
                        return [storage_cell_key(sheet, row, year)]
        return []

    prefix: str | None = None
    for (sheet, label), mapped in _label_lineage_map().items():
        if mapped == key:
            labels = {}
            if ingest is not None:
                labels = ingest.value_pass.labels_by_sheet.get(sheet, {})
            for row, lbl in labels.items():
                if lbl == label:
                    prefix = f"grid.{_sheet_slug(sheet)}.R{row}."
                    break
    if prefix:
        return [prefix]

    return []


def read_cell_changes(
    key: str,
    *,
    year: int | None = None,
    store_dir: Path | None = None,
    ingest: IngestResult | None = None,
) -> list[dict[str, Any]]:
    """Return change records for a lineage key (optionally scoped to one year)."""
    root = store_dir or cell_history_dir()
    rows = _read_parquet_rows(_changes_path(root), _CHANGE_SCHEMA)
    if not rows:
        return []

    storage_keys = resolve_storage_keys(key, year=year, ingest=ingest)
    if storage_keys and year is not None and len(storage_keys) == 1:
        return [r for r in rows if r["cell_key"] == storage_keys[0]]

    if storage_keys and year is None and storage_keys[0].endswith("."):
        prefix = storage_keys[0]
        return [r for r in rows if r["cell_key"].startswith(prefix)]

    if re_fullmatch_grid_key(key):
        return [r for r in rows if r["cell_key"] == key]

    return [r for r in rows if r["lineage_key"] == key and (year is None or r["year"] == year)]


def re_fullmatch_grid_key(key: str) -> bool:
    import re

    return bool(re.fullmatch(r"grid\.\w+\.R\d+\.\d{4}", key))


def ingest_to_snapshot_dict(ingest: IngestResult) -> dict[str, Any]:
    """Full diagnostic snapshot metadata for divergence triage."""
    labels_by_sheet = ingest.value_pass.labels_by_sheet
    label_rows: dict[str, dict[str, int]] = {}
    duplicate_labels: list[str] = []
    for sheet, labels in labels_by_sheet.items():
        sheet_map: dict[str, int] = {}
        for row_idx, label in labels.items():
            if label in sheet_map and sheet_map[label] != row_idx:
                duplicate_labels.append(f"{sheet}: duplicate label {label!r}")
            sheet_map[label] = row_idx
        label_rows[sheet] = sheet_map

    year_coverage: dict[int, int] = {}
    for (_sheet, _row, year), value in ingest.value_pass.cached_values.items():
        if isinstance(year, int) and FIRST_YEAR <= year <= LAST_YEAR and value is not None:
            year_coverage[year] = year_coverage.get(year, 0) + 1

    return {
        "workbook": str(ingest.workbook_path),
        "workbook_version": ingest.workbook_path.name,
        "horizon": {
            "first_year": FIRST_YEAR,
            "last_year": LAST_YEAR,
            "years": list(range(FIRST_YEAR, LAST_YEAR + 1)),
        },
        "sheet_names": ingest.formula_pass.sheet_names,
        "label_count_by_sheet": {s: len(lbls) for s, lbls in labels_by_sheet.items()},
        "label_rows": label_rows,
        "duplicate_labels": duplicate_labels,
        "assumption_rows": len(ingest.value_pass.assumptions_rows),
        "formula_cells": len(ingest.formula_pass.formulas),
        "cached_value_count": len(ingest.value_pass.cached_values),
        "year_value_coverage": {str(y): year_coverage.get(y, 0) for y in range(FIRST_YEAR, LAST_YEAR + 1)},
        "warnings": ingest.value_pass.warnings,
        "demand_curves": {
            "bb_breakpoints": len(ingest.demand_curves.bb_breakpoints) if ingest.demand_curves else 0,
            "dtc_breakpoints": len(ingest.demand_curves.dtc_breakpoints) if ingest.demand_curves else 0,
        },
        "sample_assumptions": [
            {
                "label": r.label,
                "base_case": _serialize_value(r.base_case),
                "y2025": _serialize_value(r.year_values.get(2025)),
            }
            for r in ingest.value_pass.assumptions_rows[:8]
        ],
    }


def write_diagnostic_snapshot(ingest: IngestResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ingest_to_snapshot_dict(ingest), indent=2), encoding="utf-8")
