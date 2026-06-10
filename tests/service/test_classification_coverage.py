"""Milestone 4.4 — derivation panel classification coverage gate (≥95%)."""

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

_COVERAGE_FLOOR = 0.95


def _finite(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


@pytest.fixture(scope="module")
def base_result() -> Any:
    workbook = get_settings().workbook_path
    if not workbook.exists():
        pytest.skip(f"workbook not found: {workbook}")
    return run_base_case(workbook, write_outputs=False)


def test_grid_cell_classification_coverage(base_result: Any) -> None:
    """≥95% of finite grid cells receive a real input/derived/stub classification."""
    total = 0
    classified = 0
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

                total += 1
                enriched = enrich_lineage(
                    row["lineage_keys"][year_idx],
                    base_result,
                    year=year,
                    sheet=meta.source_sheet,
                    row=row["row_index"],
                    sheet_slug=meta.slug,
                )
                kind = enriched.get("cell_kind")
                if kind in {"input", "derived"}:
                    classified += 1
                elif kind == "stub" and meta.slug in PLACEHOLDER_SLUGS:
                    classified += 1
                elif kind == "stub":
                    false_stubs.append(f"{meta.slug}!R{row['row_index']} {year}")

    assert total > 0
    coverage = classified / total
    assert coverage >= _COVERAGE_FLOOR, (
        f"classification coverage {coverage:.1%} < {_COVERAGE_FLOOR:.0%}; "
        f"false stubs ({len(false_stubs)}): {false_stubs[:10]}"
    )
