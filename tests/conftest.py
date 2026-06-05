"""Shared pytest fixtures for reconciliation blocks."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import ModelResult, run_base_case

REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def model_result() -> ModelResult:
    workbook = get_settings().workbook_path
    if not workbook.exists():
        pytest.skip(f"V4.113 workbook not present: {workbook}")
    return run_base_case(workbook, write_outputs=False)
