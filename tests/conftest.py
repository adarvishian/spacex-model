"""Shared pytest fixtures for reconciliation blocks."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.engine.pipeline import ModelResult, run_base_case

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"


@pytest.fixture(scope="module")
def model_result() -> ModelResult:
    if not WORKBOOK.exists():
        pytest.skip("V2.16 workbook not present")
    return run_base_case(write_outputs=False)
