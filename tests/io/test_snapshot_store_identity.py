"""Milestone 2.1/2.2 — label-identity change store tests."""

from __future__ import annotations

import copy
from dataclasses import replace
from pathlib import Path

import pytest

from spacex_model.config.settings import get_repo_root
from spacex_model.engine.label_lookup import normalize_label
from spacex_model.io.excel_ingest import IngestResult, run_formula_pass, run_value_pass
from spacex_model.io.label_remaps import RemapEntry, RemapTable, write_remap_table
from spacex_model.io.snapshot_store import (
    _CHANGE_SCHEMA,
    FIELD_MC_MIN,
    FIELD_YEAR,
    _changes_path,
    _read_parquet_rows,
    label_identity_key,
    read_cell_changes,
    record_ingest_changes,
    storage_cell_key,
)

WORKBOOK = get_repo_root() / "SpaceX V4.113.xlsx"


def _ingest_without_hook(path: Path = WORKBOOK) -> IngestResult:
    formula = run_formula_pass(path)
    values = run_value_pass(path)
    return IngestResult(workbook_path=path, formula_pass=formula, value_pass=values)


@pytest.fixture
def cell_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("SPACEX_MODEL_CELL_HISTORY_DIR", str(tmp_path))
    return tmp_path


@pytest.fixture
def remap_store(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    remap_dir = tmp_path / "data" / "label_remaps"
    remap_dir.mkdir(parents=True)
    table = RemapTable(
        from_workbook="SpaceX V4.113.xlsx",
        to_workbook="SpaceX V4.131.xlsx",
        entries=[
            RemapEntry(
                old_label="Legacy Label Alpha",
                new_label="Legacy Label Beta",
                status="faithful",
            )
        ],
    )
    write_remap_table(table, remap_dir / "test.json")
    monkeypatch.setenv("SPACEX_MODEL_CELL_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setattr(
        "spacex_model.io.snapshot_store.get_repo_root",
        lambda: tmp_path,
    )
    monkeypatch.setattr(
        "spacex_model.io.label_remaps.get_repo_root",
        lambda: tmp_path,
    )
    return tmp_path / "history"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V4.113 workbook not present")
def test_row_insertion_history_follows_label_not_row(cell_store: Path) -> None:
    ingest_v1 = _ingest_without_hook()
    sheet = "Assumptions"
    target_label = "Synthetic Row Insert Label"
    old_row = 777
    new_row = 778
    year = 2025
    ingest_v1.value_pass.labels_by_sheet.setdefault(sheet, {})[old_row] = target_label
    ingest_v1.value_pass.cached_values[(sheet, old_row, year)] = 3.14
    record_ingest_changes(ingest_v1, store_dir=cell_store)

    identity = label_identity_key(sheet, target_label, year, FIELD_YEAR)

    ingest_v2 = copy.deepcopy(ingest_v1)
    labels = dict(ingest_v2.value_pass.labels_by_sheet[sheet])
    del labels[old_row]
    labels[new_row] = target_label
    ingest_v2.value_pass.labels_by_sheet[sheet] = labels
    ingest_v2.value_pass.cached_values[(sheet, new_row, year)] = 3.14
    del ingest_v2.value_pass.cached_values[(sheet, old_row, year)]
    ingest_v2 = replace(ingest_v2, workbook_path=Path("synthetic-row-insert.xlsx"))
    record_ingest_changes(ingest_v2, store_dir=cell_store)

    rows = _read_parquet_rows(_changes_path(cell_store), _CHANGE_SCHEMA)
    identity_changes = [r for r in rows if r.get("identity_key") == identity]
    kinds = {r["change_kind"] for r in identity_changes}
    assert "initial" in kinds
    assert "removed" not in kinds
    assert "added" not in kinds


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V4.113 workbook not present")
def test_removal_emits_removed_kind(cell_store: Path) -> None:
    ingest_v1 = _ingest_without_hook()
    sheet = "Assumptions"
    removed_label = "Synthetic Variable To Remove"
    remove_row = 888
    ingest_v1.value_pass.labels_by_sheet.setdefault(sheet, {})[
        remove_row
    ] = removed_label
    ingest_v1.value_pass.cached_values[(sheet, remove_row, 2025)] = 42.0
    record_ingest_changes(ingest_v1, store_dir=cell_store)

    ingest_v2 = copy.deepcopy(ingest_v1)
    del ingest_v2.value_pass.labels_by_sheet[sheet][remove_row]
    del ingest_v2.value_pass.cached_values[(sheet, remove_row, 2025)]
    ingest_v2 = replace(ingest_v2, workbook_path=Path("synthetic-removal.xlsx"))
    record_ingest_changes(ingest_v2, store_dir=cell_store)

    rows = _read_parquet_rows(_changes_path(cell_store), _CHANGE_SCHEMA)
    removed = [r for r in rows if r["change_kind"] == "removed"]
    assert removed
    assert any(r.get("label") == removed_label for r in removed)


def test_rename_via_remap_table_emits_renamed(remap_store: Path) -> None:
    store = remap_store
    sheet = "Assumptions"
    old_label = "Legacy Label Alpha"
    new_label = "Legacy Label Beta"
    year = 2025

    ingest_v1 = _ingest_without_hook()
    ingest_v1.value_pass.labels_by_sheet.setdefault(sheet, {})[99] = old_label
    ingest_v1.value_pass.cached_values[(sheet, 99, year)] = 1.0
    record_ingest_changes(ingest_v1, store_dir=store)

    ingest_v2 = copy.deepcopy(ingest_v1)
    ingest_v2.value_pass.labels_by_sheet[sheet] = {100: new_label}
    ingest_v2.value_pass.cached_values = {(sheet, 100, year): 1.0}
    ingest_v2 = replace(ingest_v2, workbook_path=Path("SpaceX V4.131.xlsx"))
    record_ingest_changes(ingest_v2, store_dir=store)

    rows = _read_parquet_rows(_changes_path(store), _CHANGE_SCHEMA)
    renamed = [r for r in rows if r["change_kind"] == "renamed"]
    assert renamed
    assert renamed[0].get("prior_label") == old_label
    assert renamed[0].get("label") == new_label


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V4.113 workbook not present")
def test_mc_min_change_produces_change_record(cell_store: Path) -> None:
    ingest_v1 = _ingest_without_hook()
    row_record = next(
        r for r in ingest_v1.value_pass.assumptions_rows if r.mc_min is not None
    )
    record_ingest_changes(ingest_v1, store_dir=cell_store)

    ingest_v2 = copy.deepcopy(ingest_v1)
    idx = ingest_v2.value_pass.assumptions_rows.index(row_record)
    updated = replace(row_record, mc_min=float(row_record.mc_min) + 0.5)  # type: ignore[arg-type]
    ingest_v2.value_pass.assumptions_rows[idx] = updated
    ingest_v2 = replace(ingest_v2, workbook_path=Path("mc-change.xlsx"))
    record_ingest_changes(ingest_v2, store_dir=cell_store)

    identity = label_identity_key("Assumptions", row_record.label, 0, FIELD_MC_MIN)
    rows = _read_parquet_rows(_changes_path(cell_store), _CHANGE_SCHEMA)
    mc_changes = [
        r
        for r in rows
        if r.get("identity_key") == identity and r["change_kind"] != "initial"
    ]
    assert mc_changes
    assert mc_changes[0]["field"] == FIELD_MC_MIN


def test_read_by_label_key_with_ingest(cell_store: Path) -> None:
    ingest = _ingest_without_hook()
    sheet = "Group P&L"
    label = "Group Revenue ($mm)"
    row = next(
        r for r, lbl in ingest.value_pass.labels_by_sheet[sheet].items() if lbl == label
    )
    year = 2030
    record_ingest_changes(ingest, store_dir=cell_store)

    lineage = "group.group_revenue_net"
    rows = read_cell_changes(lineage, year=year, store_dir=cell_store, ingest=ingest)
    assert rows
    assert rows[0]["label_key"] == normalize_label(label)
    assert rows[0]["cell_key"] == storage_cell_key(sheet, row, year)
