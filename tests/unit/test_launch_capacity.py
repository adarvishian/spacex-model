"""Launch capacity unit tests — migrated from test_phase_c per PRD §10.1."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.calc.launch_capacity import LaunchCapacityInputs, compute_launch_capacity
from spacex_model.config.constants import FIRST_YEAR
from spacex_model.inputs.assumptions import Assumptions, assumptions_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook

REPO = Path(__file__).resolve().parents[2]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"


@pytest.fixture(scope="module")
def assumptions() -> Assumptions:
    if not WORKBOOK.exists():
        return Assumptions()
    return assumptions_from_ingest(ingest_workbook(WORKBOOK))


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_launch_capacity_2025_calibration(assumptions: Assumptions) -> None:
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    y = FIRST_YEAR
    assert lc.f9_launches.at(y) == pytest.approx(171.0, abs=5.0)
    assert lc.f9_fleet_eoy.at(y) == pytest.approx(39.0, abs=5.0)
    assert lc.f9_manufactured.at(y) == pytest.approx(17.0, abs=2.0)
    assert lc.total_starship_launches.at(y) == 0.0
    assert 400 <= lc.blended_cost_per_kg.at(y) <= 800
