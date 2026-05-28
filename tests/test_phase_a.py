"""Phase A smoke tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.config.settings import get_settings
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.pipeline import run_base_case
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.inputs.assumptions import assumptions_from_ingest

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_ingest_assumptions() -> None:
    ingest = ingest_workbook(WORKBOOK)
    assumptions = assumptions_from_ingest(ingest)
    assert len(assumptions.by_label) > 200
    assert 0.20 <= assumptions.tax_rate <= 0.22
    assert assumptions.starting_cash_eoy_2024 == 5000


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_base_case_pipeline() -> None:
    result = run_base_case(WORKBOOK, write_outputs=False)
    assert result.solver_trace.converged
    assert len(result.module_outputs) == 5


def test_year_vector_shape() -> None:
    z = YearVector.zeros()
    assert len(z) == HORIZON_YEARS


def test_settings_default_workbook() -> None:
    settings = get_settings()
    assert "V2.16" in settings.workbook_path.name
