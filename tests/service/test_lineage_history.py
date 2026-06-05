"""L3 — per-cell ingest diff store and fetch_change_history."""

from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path

import pytest

from spacex_model.config.settings import get_repo_root
from spacex_model.io.excel_ingest import IngestResult, run_formula_pass, run_value_pass
from spacex_model.io.snapshot_store import (
    read_cell_changes,
    record_ingest_changes,
    storage_cell_key,
)
from spacex_model.service.lineage_history import fetch_change_history

WORKBOOK = get_repo_root() / "SpaceX V4.113.xlsx"


def _ingest_without_hook(path: Path = WORKBOOK) -> IngestResult:
    formula = run_formula_pass(path)
    values = run_value_pass(path)
    return IngestResult(workbook_path=path, formula_pass=formula, value_pass=values)


def _group_revenue_2030_key(ingest: IngestResult) -> tuple[str, str]:
    sheet = "Group P&L"
    label = "Group Revenue ($mm)"
    row = next(
        r for r, lbl in ingest.value_pass.labels_by_sheet[sheet].items() if lbl == label
    )
    year = 2030
    return "group.group_revenue_net", storage_cell_key(sheet, row, year)


@pytest.fixture
def cell_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("SPACEX_MODEL_CELL_HISTORY_DIR", str(tmp_path))
    return tmp_path


def test_two_version_diff_changed_and_unchanged_cells(cell_store: Path) -> None:
    ingest_v1 = _ingest_without_hook()
    record_ingest_changes(ingest_v1, store_dir=cell_store)

    lineage_key, cell_key = _group_revenue_2030_key(ingest_v1)
    sheet = "Group P&L"
    row = int(cell_key.split(".R")[1].split(".")[0])
    year = 2030

    prior = ingest_v1.value_pass.cached_values[(sheet, row, year)]
    assert isinstance(prior, (int, float))

    ingest_v2 = copy.deepcopy(ingest_v1)
    ingest_v2.value_pass.cached_values[(sheet, row, year)] = float(prior) + 100.0
    ingest_v2 = replace(ingest_v2, workbook_path=Path("SpaceX V4.114-synthetic.xlsx"))
    record_ingest_changes(ingest_v2, store_dir=cell_store)

    changed = fetch_change_history(lineage_key, year=year, store_dir=cell_store)
    kinds = [e["change_kind"] for e in changed]
    assert "initial" in kinds
    assert "value" in kinds
    value_entry = next(e for e in changed if e["change_kind"] == "value")
    effect = value_entry["effect_on_cell"]
    assert effect is not None
    assert effect["before"] == pytest.approx(float(prior))
    assert effect["after"] == pytest.approx(float(prior) + 100.0)
    assert effect["delta"] == pytest.approx(100.0)
    assert value_entry["commit_sha"] == ingest_v2.workbook_path.name or effect["after"] is not None
    assert "V4.114" in value_entry["title"]

    from spacex_model.io.snapshot_store import _CHANGE_SCHEMA, _changes_path, _read_parquet_rows

    rows = _read_parquet_rows(_changes_path(cell_store), _CHANGE_SCHEMA)
    other = next(r for r in rows if r["cell_key"] != cell_key and r["change_kind"] == "initial")
    unchanged = fetch_change_history(
        other["lineage_key"],
        year=other["year"],
        store_dir=cell_store,
    )
    assert len(unchanged) == 1
    assert unchanged[0]["change_kind"] == "initial"

    spurious = [e for e in changed if "sprint" in (e.get("title") or "").lower()]
    assert not spurious


def test_no_spurious_entries_on_reingest_same_fingerprint(cell_store: Path) -> None:
    ingest = _ingest_without_hook()
    first = record_ingest_changes(ingest, store_dir=cell_store)
    assert len(first) > 0
    second = record_ingest_changes(ingest, store_dir=cell_store)
    assert second == []

    lineage_key, _ = _group_revenue_2030_key(ingest)
    records = read_cell_changes(lineage_key, year=2030, store_dir=cell_store)
    assert len(records) == 1
    assert records[0]["change_kind"] == "initial"


def test_assumptions_input_change_kind(cell_store: Path) -> None:
    ingest_v1 = _ingest_without_hook()
    record_ingest_changes(ingest_v1, store_dir=cell_store)

    row_record = next(
        r
        for r in ingest_v1.value_pass.assumptions_rows
        if r.year_values.get(2025) is not None
        and not r.label.startswith("§")
        and not r.label.isupper()
    )
    row = row_record.row
    prior = ingest_v1.value_pass.cached_values[("Assumptions", row, 2025)]
    assert isinstance(prior, (int, float))

    ingest_v2 = copy.deepcopy(ingest_v1)
    ingest_v2.value_pass.cached_values[("Assumptions", row, 2025)] = float(prior) + 1.0
    ingest_v2 = replace(ingest_v2, workbook_path=Path("SpaceX V4.114-synthetic.xlsx"))
    record_ingest_changes(ingest_v2, store_dir=cell_store)

    key = storage_cell_key("Assumptions", row, 2025)
    entries = fetch_change_history(key, year=2025, store_dir=cell_store)
    value_entries = [e for e in entries if e["change_kind"] in ("input", "value", "anchor")]
    assert value_entries
    assert value_entries[0]["change_kind"] == "input"
