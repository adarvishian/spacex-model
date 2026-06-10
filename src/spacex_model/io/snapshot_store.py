"""Diagnostic snapshot store and per-cell xlsx version diff (L3)."""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.config.settings import (
    _default_cell_history_dir,
    _default_cell_history_read_dir,
    get_repo_root,
)
from spacex_model.engine.label_lookup import normalize_label
from spacex_model.inputs.s1_2025_anchors import S1_INGEST_ANCHORS_2025
from spacex_model.io.excel_ingest import IngestResult
from spacex_model.io.label_remaps import build_remap_index, load_remap_table

_logger = logging.getLogger(__name__)

FIELD_YEAR = "year"
FIELD_BASE_CASE = "base_case"
FIELD_MC_MIN = "mc_min"
FIELD_MC_MAX = "mc_max"
FIELD_MC_DISTRIBUTION = "mc_distribution"
_SCALAR_YEAR = 0

_CHANGE_KINDS = (
    "initial",
    "value",
    "formula",
    "input",
    "anchor",
    "added",
    "removed",
    "renamed",
)

_CHANGE_SCHEMA = pa.schema(
    [
        ("cell_key", pa.string()),
        ("identity_key", pa.string()),
        ("lineage_key", pa.string()),
        ("sheet", pa.string()),
        ("row", pa.int32()),
        ("year", pa.int32()),
        ("field", pa.string()),
        ("label", pa.string()),
        ("label_key", pa.string()),
        ("prior_label", pa.string()),
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
        ("identity_key", pa.string()),
        ("lineage_key", pa.string()),
        ("sheet", pa.string()),
        ("row", pa.int32()),
        ("year", pa.int32()),
        ("field", pa.string()),
        ("label", pa.string()),
        ("label_key", pa.string()),
        ("value", pa.float64()),
        ("formula", pa.string()),
        ("model_version", pa.string()),
    ]
)

_ANCHOR_LABELS: frozenset[str] = frozenset(
    spec.assumptions_label or spec.name for spec in S1_INGEST_ANCHORS_2025
)


def _sheet_slug(sheet: str) -> str:
    from spacex_model.service.sheets_meta import sheet_for_name

    meta = sheet_for_name(sheet)
    return meta.slug if meta else sheet.lower().replace(" ", "_")


def _is_section_header(label: str) -> bool:
    return label.startswith("§") or label.startswith("▸") or label.isupper()


def _label_lineage_map() -> dict[tuple[str, str], str]:
    from spacex_model.service.grid import _LABEL_LINEAGE

    return _LABEL_LINEAGE


def cell_history_read_dir() -> Path:
    """Bundled / committed store (readable on serverless)."""
    override = __import__("os").environ.get("SPACEX_MODEL_CELL_HISTORY_DIR")
    if override:
        return Path(override).resolve()
    return _default_cell_history_read_dir()


def cell_history_write_dir() -> Path:
    """Writable store — /tmp on serverless."""
    override = __import__("os").environ.get("SPACEX_MODEL_CELL_HISTORY_DIR")
    if override:
        return Path(override).resolve()
    return _default_cell_history_dir()


def cell_history_dir() -> Path:
    """Backward-compatible alias for read dir."""
    return cell_history_read_dir()


def _changes_path(store_dir: Path) -> Path:
    return store_dir / "changes.parquet"


def _snapshot_path(store_dir: Path) -> Path:
    return store_dir / "value_snapshot.parquet"


def _metadata_path(store_dir: Path) -> Path:
    return store_dir / "metadata.json"


def label_identity_key(sheet: str, label: str, year: int, field: str) -> str:
    """Primary diff identity — label-based, not row positional."""
    return f"{sheet}|{normalize_label(label)}|{year}|{field}"


def storage_cell_key(sheet: str, row: int, year: int, field: str = FIELD_YEAR) -> str:
    """Positional key for grid display / legacy lookups."""
    slug = _sheet_slug(sheet)
    if field == FIELD_YEAR:
        return f"grid.{slug}.R{row}.{year}"
    return f"grid.{slug}.R{row}.{field}"


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
        return str(a or "") == str(b or "")
    if fa is None or fb is None:
        return str(a) == str(b)
    return abs(fa - fb) < 1e-9


def _lineage_key_for_cell(sheet: str, label: str, row: int, year: int) -> str:
    mapped = _label_lineage_map().get((sheet, label))
    if mapped:
        return mapped
    slug = _sheet_slug(sheet)
    if year == _SCALAR_YEAR:
        return f"grid.{slug}.R{row}.scalar"
    return f"grid.{slug}.R{row}.{year}"


def _row_formula_index(ingest: IngestResult) -> dict[tuple[str, int], str | None]:
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
    field: str,
) -> str:
    if formula_changed:
        return "formula"
    if not value_changed:
        return "value"
    if field == FIELD_BASE_CASE or (
        sheet == "Assumptions" and field == FIELD_YEAR and value_changed
    ):
        if sheet == "Assumptions" and field in (FIELD_YEAR, FIELD_BASE_CASE):
            if normalize_label(label) in {normalize_label(a) for a in _ANCHOR_LABELS}:
                return "anchor"
            return "input"
    if sheet == "Assumptions" and value_changed:
        if normalize_label(label) in {normalize_label(a) for a in _ANCHOR_LABELS}:
            return "anchor"
        if field == FIELD_YEAR:
            return "input"
    return "value"


def _append_cell(
    cells: list[dict[str, Any]],
    *,
    sheet: str,
    row: int,
    label: str,
    year: int,
    field: str,
    value: Any,
    formula: str | None,
) -> None:
    cells.append(
        {
            "cell_key": storage_cell_key(
                sheet, row, year if field == FIELD_YEAR else _SCALAR_YEAR, field
            ),
            "identity_key": label_identity_key(
                sheet, label, year if field == FIELD_YEAR else _SCALAR_YEAR, field
            ),
            "lineage_key": _lineage_key_for_cell(
                sheet, label, row, year if field == FIELD_YEAR else _SCALAR_YEAR
            ),
            "sheet": sheet,
            "row": row,
            "year": year if field == FIELD_YEAR else _SCALAR_YEAR,
            "field": field,
            "label": label,
            "label_key": normalize_label(label),
            "value": value,
            "formula": formula,
        }
    )


def _iter_ingest_cells(ingest: IngestResult) -> list[dict[str, Any]]:
    """Yield records for year columns, Assumptions scalars, and MC metadata."""
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
                _append_cell(
                    cells,
                    sheet=sheet,
                    row=row,
                    label=label,
                    year=year,
                    field=FIELD_YEAR,
                    value=raw,
                    formula=formula,
                )

    for row_record in ingest.value_pass.assumptions_rows:
        if row_record.label.startswith("§") or row_record.label.isupper():
            continue
        sheet = "Assumptions"
        row = row_record.row
        formula = formulas.get((sheet, row))
        if row_record.base_case is not None:
            _append_cell(
                cells,
                sheet=sheet,
                row=row,
                label=row_record.label,
                year=_SCALAR_YEAR,
                field=FIELD_BASE_CASE,
                value=row_record.base_case,
                formula=formula,
            )
        if row_record.mc_min is not None:
            _append_cell(
                cells,
                sheet=sheet,
                row=row,
                label=row_record.label,
                year=_SCALAR_YEAR,
                field=FIELD_MC_MIN,
                value=row_record.mc_min,
                formula=formula,
            )
        if row_record.mc_max is not None:
            _append_cell(
                cells,
                sheet=sheet,
                row=row,
                label=row_record.label,
                year=_SCALAR_YEAR,
                field=FIELD_MC_MAX,
                value=row_record.mc_max,
                formula=formula,
            )
        if row_record.distribution:
            _append_cell(
                cells,
                sheet=sheet,
                row=row,
                label=row_record.label,
                year=_SCALAR_YEAR,
                field=FIELD_MC_DISTRIBUTION,
                value=row_record.distribution,
                formula=row_record.distribution,
            )

    return cells


def _ingest_fingerprint(ingest: IngestResult) -> str:
    parts: list[str] = [ingest.workbook_path.name]
    for cell in sorted(_iter_ingest_cells(ingest), key=lambda c: c["identity_key"]):
        val = _coerce_float(cell["value"])
        text = cell["value"] if val is None else val
        parts.append(f"{cell['identity_key']}={text}:{cell.get('formula') or ''}")
    digest = hashlib.sha256("\n".join(parts).encode()).hexdigest()
    return digest


def _read_parquet_rows(path: Path, schema: pa.Schema) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    table = pq.read_table(path)  # type: ignore[no-untyped-call]
    return table.to_pylist()


def _write_parquet_rows(
    path: Path, rows: list[dict[str, Any]], schema: pa.Schema
) -> None:
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


def _backfill_row(row: dict[str, Any], ingest: IngestResult | None) -> dict[str, Any]:
    """Migrate legacy positional rows to label-identity schema."""
    out = dict(row)
    if out.get("identity_key") and out.get("label_key"):
        out.setdefault("field", FIELD_YEAR)
        return out
    cell_key = str(out.get("cell_key", ""))
    sheet = str(out.get("sheet", ""))
    row_num = int(out.get("row", 0))
    year = int(out.get("year", 0))
    field = FIELD_YEAR
    if ".base_case" in cell_key:
        field = FIELD_BASE_CASE
    elif ".mc_min" in cell_key:
        field = FIELD_MC_MIN
    elif ".mc_max" in cell_key:
        field = FIELD_MC_MAX
    elif ".mc_distribution" in cell_key:
        field = FIELD_MC_DISTRIBUTION
    label = str(out.get("label") or "")
    if not label and ingest is not None:
        label = ingest.value_pass.labels_by_sheet.get(sheet, {}).get(row_num, "")
    out["field"] = field
    out["label"] = label
    out["label_key"] = normalize_label(label) if label else ""
    scalar_year = year if field == FIELD_YEAR else _SCALAR_YEAR
    out["identity_key"] = label_identity_key(sheet, label, scalar_year, field)
    out.setdefault("prior_label", None)
    return out


def migrate_cell_history_store(
    store_dir: Path, ingest: IngestResult | None = None
) -> bool:
    """One-time backfill of label columns on legacy parquet. Returns True if migrated."""
    snap_path = _snapshot_path(store_dir)
    if not snap_path.is_file():
        return False
    rows = _read_parquet_rows(snap_path, _SNAPSHOT_SCHEMA)
    if not rows:
        return False
    if rows[0].get("identity_key"):
        return False
    migrated = [_backfill_row(r, ingest) for r in rows]
    _write_parquet_rows(snap_path, migrated, _SNAPSHOT_SCHEMA)
    change_rows = _read_parquet_rows(_changes_path(store_dir), _CHANGE_SCHEMA)
    if change_rows:
        migrated_changes = [_backfill_row(r, ingest) for r in change_rows]
        _write_parquet_rows(_changes_path(store_dir), migrated_changes, _CHANGE_SCHEMA)
    return True


def _change_record(
    cell: dict[str, Any],
    *,
    change_kind: str,
    prior: dict[str, Any] | None,
    model_version: str,
    commit_sha: str,
    timestamp: str,
    prior_label: str | None = None,
) -> dict[str, Any]:
    prior_value = prior.get("value") if prior else None
    prior_formula = prior.get("formula") if prior else None
    new_value = cell["value"]
    new_formula = cell.get("formula")
    pv = _coerce_float(prior_value)
    nv = _coerce_float(new_value)
    if cell["field"] == FIELD_MC_DISTRIBUTION:
        prior_formula = str(prior_value) if prior_value is not None else prior_formula
        new_formula = str(new_value) if new_value is not None else new_formula
        pv, nv = None, None
    delta = (nv - pv) if pv is not None and nv is not None else None
    return {
        "cell_key": cell["cell_key"],
        "identity_key": cell["identity_key"],
        "lineage_key": cell["lineage_key"],
        "sheet": cell["sheet"],
        "row": cell["row"],
        "year": cell["year"],
        "field": cell["field"],
        "label": cell["label"],
        "label_key": cell["label_key"],
        "prior_label": prior_label,
        "prior_value": pv,
        "new_value": nv,
        "delta": delta,
        "formula_prior": prior_formula,
        "formula_new": new_formula,
        "model_version": model_version,
        "commit_sha": commit_sha,
        "timestamp": timestamp,
        "change_kind": change_kind,
    }


def record_ingest_changes(
    ingest: IngestResult,
    *,
    store_dir: Path | None = None,
) -> list[dict[str, Any]]:
    """Diff ingest against prior snapshot; append label-keyed change records."""
    root = store_dir or cell_history_write_dir()
    root.mkdir(parents=True, exist_ok=True)
    migrate_cell_history_store(root, ingest)

    fingerprint = _ingest_fingerprint(ingest)
    meta_path = _metadata_path(root)
    if meta_path.is_file():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("fingerprint") == fingerprint:
            return []

    prior_rows = [
        _backfill_row(r, ingest)
        for r in _read_parquet_rows(_snapshot_path(root), _SNAPSHOT_SCHEMA)
    ]
    prior_by_identity = {
        row["identity_key"]: row for row in prior_rows if row.get("identity_key")
    }

    remap_table = load_remap_table()
    remap_new_to_old = build_remap_index(remap_table)

    now = datetime.now(UTC).isoformat()
    model_version = ingest.workbook_path.name
    commit_sha = _git_sha() or ""
    is_first_ingest = not prior_rows

    current_cells = _iter_ingest_cells(ingest)
    current_by_identity = {c["identity_key"]: c for c in current_cells}

    new_changes: list[dict[str, Any]] = []
    handled_prior: set[str] = set()

    for identity_key, cell in current_by_identity.items():
        prior = prior_by_identity.get(identity_key)
        if prior is not None:
            handled_prior.add(identity_key)
            prior_value = prior.get("value")
            prior_formula = prior.get("formula")
            new_value = cell["value"]
            new_formula = cell.get("formula")
            if cell["field"] == FIELD_MC_DISTRIBUTION:
                value_changed = str(prior_value or "") != str(new_value or "")
                formula_changed = False
            else:
                value_changed = not _values_equal(prior_value, new_value)
                formula_changed = (prior_formula or "") != (new_formula or "")

            if is_first_ingest:
                new_changes.append(
                    _change_record(
                        cell,
                        change_kind="initial",
                        prior=None,
                        model_version=model_version,
                        commit_sha=commit_sha,
                        timestamp=now,
                    )
                )
            elif value_changed or formula_changed:
                kind = _classify_change_kind(
                    cell["sheet"],
                    cell["label"],
                    value_changed=value_changed,
                    formula_changed=formula_changed,
                    field=cell["field"],
                )
                new_changes.append(
                    _change_record(
                        cell,
                        change_kind=kind,
                        prior=prior,
                        model_version=model_version,
                        commit_sha=commit_sha,
                        timestamp=now,
                    )
                )
            continue

        old_label = remap_new_to_old.get(cell["label_key"])
        prior_via_rename: dict[str, Any] | None = None
        if old_label:
            old_identity = label_identity_key(
                cell["sheet"], old_label, cell["year"], cell["field"]
            )
            prior_via_rename = prior_by_identity.get(old_identity)
            if prior_via_rename is not None:
                handled_prior.add(old_identity)
                new_changes.append(
                    _change_record(
                        cell,
                        change_kind="renamed",
                        prior=prior_via_rename,
                        model_version=model_version,
                        commit_sha=commit_sha,
                        timestamp=now,
                        prior_label=old_label,
                    )
                )
                pv = prior_via_rename.get("value")
                nv = cell["value"]
                if not is_first_ingest and not _values_equal(pv, nv):
                    kind = _classify_change_kind(
                        cell["sheet"],
                        cell["label"],
                        value_changed=True,
                        formula_changed=False,
                        field=cell["field"],
                    )
                    new_changes.append(
                        _change_record(
                            cell,
                            change_kind=kind,
                            prior=prior_via_rename,
                            model_version=model_version,
                            commit_sha=commit_sha,
                            timestamp=now,
                            prior_label=old_label,
                        )
                    )
                continue

        kind = "initial" if is_first_ingest else "added"
        new_changes.append(
            _change_record(
                cell,
                change_kind=kind,
                prior=None,
                model_version=model_version,
                commit_sha=commit_sha,
                timestamp=now,
            )
        )

    for identity_key, prior in prior_by_identity.items():
        if identity_key in handled_prior:
            continue
        prior_cell = dict(prior)
        prior_cell["value"] = prior.get("value")
        new_changes.append(
            _change_record(
                prior_cell,
                change_kind="removed",
                prior=prior,
                model_version=model_version,
                commit_sha=commit_sha,
                timestamp=now,
            )
        )

    new_snapshot = [
        {
            "cell_key": c["cell_key"],
            "identity_key": c["identity_key"],
            "lineage_key": c["lineage_key"],
            "sheet": c["sheet"],
            "row": c["row"],
            "year": c["year"],
            "field": c["field"],
            "label": c["label"],
            "label_key": c["label_key"],
            "value": (
                _coerce_float(c["value"])
                if c["field"] != FIELD_MC_DISTRIBUTION
                else None
            ),
            "formula": (
                str(c["value"])
                if c["field"] == FIELD_MC_DISTRIBUTION
                else c.get("formula")
            ),
            "model_version": model_version,
        }
        for c in current_cells
    ]

    if new_changes:
        existing = [
            _backfill_row(r, ingest)
            for r in _read_parquet_rows(_changes_path(root), _CHANGE_SCHEMA)
        ]
        _write_parquet_rows(_changes_path(root), existing + new_changes, _CHANGE_SCHEMA)

    _write_parquet_rows(_snapshot_path(root), new_snapshot, _SNAPSHOT_SCHEMA)
    meta_path.write_text(
        json.dumps(
            {
                "fingerprint": fingerprint,
                "model_version": model_version,
                "timestamp": now,
                "commit_sha": commit_sha,
                "schema_version": 2,
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
    if re.fullmatch(r"grid\.\w+\.R\d+\.\w+", key):
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


def _merge_change_rows(read_dir: Path, write_dir: Path) -> list[dict[str, Any]]:
    rows = _read_parquet_rows(_changes_path(read_dir), _CHANGE_SCHEMA)
    if write_dir.resolve() == read_dir.resolve():
        return rows
    extra = _read_parquet_rows(_changes_path(write_dir), _CHANGE_SCHEMA)
    if not extra:
        return rows
    seen = {r.get("identity_key", r.get("cell_key")) for r in rows}
    for row in extra:
        key = row.get("identity_key", row.get("cell_key"))
        if key not in seen:
            rows.append(row)
            seen.add(key)
    return rows


def read_cell_changes(
    key: str,
    *,
    year: int | None = None,
    store_dir: Path | None = None,
    ingest: IngestResult | None = None,
) -> list[dict[str, Any]]:
    """Return change records for a lineage key (optionally scoped to one year)."""
    read_dir = store_dir or cell_history_read_dir()
    write_dir = cell_history_write_dir() if store_dir is None else store_dir
    rows = _merge_change_rows(read_dir, write_dir)
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

    if ingest is not None:
        for (sheet, label), mapped in _label_lineage_map().items():
            if mapped == key:
                label_key = normalize_label(label)
                return [
                    r
                    for r in rows
                    if r.get("label_key") == label_key
                    and r.get("sheet") == sheet
                    and (year is None or r.get("year") == year)
                ]

    return [
        r
        for r in rows
        if r["lineage_key"] == key and (year is None or r["year"] == year)
    ]


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
        if (
            isinstance(year, int)
            and FIRST_YEAR <= year <= LAST_YEAR
            and value is not None
        ):
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
        "year_value_coverage": {
            str(y): year_coverage.get(y, 0) for y in range(FIRST_YEAR, LAST_YEAR + 1)
        },
        "warnings": ingest.value_pass.warnings,
        "demand_curves": {
            "bb_breakpoints": (
                len(ingest.demand_curves.bb_breakpoints) if ingest.demand_curves else 0
            ),
            "dtc_breakpoints": (
                len(ingest.demand_curves.dtc_breakpoints) if ingest.demand_curves else 0
            ),
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
    path.write_text(
        json.dumps(ingest_to_snapshot_dict(ingest), indent=2), encoding="utf-8"
    )
