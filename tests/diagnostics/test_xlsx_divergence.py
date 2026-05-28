"""xlsx diagnostic divergence harness — per-cell parametrize per PRD §7.6."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.engine.label_lookup import lookup_by_label
from spacex_model.engine.pipeline import run_base_case
from spacex_model.io.divergence import (
    DivergenceEntry,
    DivergenceReport,
    build_divergence_report,
    finalize_triage,
)

REPO = Path(__file__).resolve().parents[2]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"

_MAPPED_CELLS: list[tuple[str, int, int]] = []
if WORKBOOK.exists():
    _bootstrap_result = run_base_case(write_outputs=False)
    _bootstrap_report = finalize_triage(
        build_divergence_report(_bootstrap_result), _bootstrap_result
    )
    _MAPPED_CELLS = sorted(
        {(e.sheet, e.row, e.year) for e in _bootstrap_report.entries if e.code_value is not None}
    )


@pytest.fixture(scope="module")
def base_case_result():
    if not WORKBOOK.exists():
        pytest.skip("V2.16 workbook not present")
    if _MAPPED_CELLS:
        return _bootstrap_result
    return run_base_case(write_outputs=False)


@pytest.fixture(scope="module")
def divergence_report(base_case_result) -> DivergenceReport:
    return finalize_triage(build_divergence_report(base_case_result), base_case_result)


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_divergence_report_generated(divergence_report: DivergenceReport) -> None:
    assert divergence_report.mapped_count > 0
    assert (
        divergence_report.matching_count + divergence_report.diverging_count
        <= divergence_report.mapped_count
    )


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_zero_open_triage_a_or_d_after_finalize(divergence_report: DivergenceReport) -> None:
    assert len(divergence_report.open_type_a) == 0
    assert len(divergence_report.open_type_d) == 0


@pytest.mark.skipif(not _MAPPED_CELLS, reason="No mapped xlsx cells")
@pytest.mark.parametrize("sheet,row,year", _MAPPED_CELLS)
def test_xlsx_divergence_cell(
    sheet: str,
    row: int,
    year: int,
    divergence_report: DivergenceReport,
    base_case_result,
) -> None:
    """Record-and-pass per-cell divergence artifact (PRD §7.6)."""
    ingest = base_case_result.ingest
    label = ingest.value_pass.labels_by_sheet.get(sheet, {}).get(row, "")
    xlsx_val = float(ingest.value_pass.cached_values[(sheet, row, year)])
    code_val = lookup_by_label(base_case_result, sheet, label, year)
    assert code_val is not None

    matched: list[DivergenceEntry] = [
        e for e in divergence_report.entries if e.sheet == sheet and e.row == row and e.year == year
    ]
    assert matched, f"Cell ({sheet}, {row}, {year}) missing from divergence report"
    entry = matched[0]
    assert entry.xlsx_value == pytest.approx(xlsx_val)
    assert entry.code_value == pytest.approx(code_val)
    recomputed_delta = code_val - xlsx_val
    assert (abs(recomputed_delta) <= entry.tolerance) == entry.within_tolerance
