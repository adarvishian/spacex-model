"""L1 acceptance — no false stub classification on grid-renderable cells."""

from __future__ import annotations

import math
from typing import Any

import pytest

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_base_case
from spacex_model.service.grid import build_grid_payload
from spacex_model.service.lineage_enrich import enrich_lineage
from spacex_model.service.sheets_meta import SHEETS
from spacex_model.service.stub_registry import PLACEHOLDER_SLUGS


def _finite(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


@pytest.fixture(scope="module")
def base_result() -> Any:
    workbook = get_settings().workbook_path
    if not workbook.exists():
        pytest.skip(f"workbook not found: {workbook}")
    return run_base_case(workbook, write_outputs=False)


def test_no_false_stubs_on_finite_display_cells(base_result: Any) -> None:
    """Every non-placeholder cell with a grid number must not be classified stub."""
    false_stubs: list[str] = []

    for meta in SHEETS:
        if meta.slug == "run_audit":
            continue

        grid = build_grid_payload(meta, base_result)
        for row in grid["rows"]:
            if row.get("is_header"):
                continue
            for year_idx, year in enumerate(grid["years"]):
                display = row["year_values"][year_idx]
                if not _finite(display):
                    continue

                enriched = enrich_lineage(
                    row["lineage_keys"][year_idx],
                    base_result,
                    year=year,
                    sheet=meta.source_sheet,
                    row=row["row_index"],
                    sheet_slug=meta.slug,
                )
                if enriched.get("cell_kind") == "stub" and meta.slug not in PLACEHOLDER_SLUGS:
                    false_stubs.append(
                        f"{meta.slug}!R{row['row_index']} {year} ({row['label'][:40]})"
                    )

    assert false_stubs == [], f"false stubs ({len(false_stubs)}): {false_stubs[:20]}"


def test_derived_cell_value_matches_grid_per_sheet(base_result: Any) -> None:
    """At least one derived cell per non-placeholder sheet: value == grid (F6)."""
    checked_sheets: set[str] = set()

    for meta in SHEETS:
        if meta.slug in PLACEHOLDER_SLUGS or meta.slug == "run_audit":
            continue

        grid = build_grid_payload(meta, base_result)
        for row in grid["rows"]:
            if row.get("is_header"):
                continue
            for year_idx, year in enumerate(grid["years"]):
                if meta.slug in checked_sheets:
                    break
                display = row["year_values"][year_idx]
                kind = row["cell_kinds"][year_idx]
                if not _finite(display) or kind != "derived":
                    continue

                enriched = enrich_lineage(
                    row["lineage_keys"][year_idx],
                    base_result,
                    year=year,
                    sheet=meta.source_sheet,
                    row=row["row_index"],
                    sheet_slug=meta.slug,
                )
                assert enriched["cell_kind"] == "derived"
                assert enriched["computed_value"] == pytest.approx(float(display))
                checked_sheets.add(meta.slug)
                break
            if meta.slug in checked_sheets:
                break

    expected = {
        m.slug
        for m in SHEETS
        if m.slug not in PLACEHOLDER_SLUGS and m.slug not in {"run_audit", "assumptions"}
    }
    assert checked_sheets == expected, f"missing sheets: {expected - checked_sheets}"
