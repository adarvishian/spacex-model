"""Guardrail: lineage/API contract work must not change model outputs.

PRD Lineage Trust §10 Sprint 0 — golden snapshot of Group + per-module outputs.
Re-run after every lineage sprint; failure means model numbers moved.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.engine.pipeline import ModelResult

BASELINE = Path(__file__).resolve().parent / "no_model_drift_baseline.json"


def _years() -> range:
    return range(FIRST_YEAR, LAST_YEAR + 1)


def _snapshot(result: ModelResult) -> dict[str, Any]:
    """Group + per-module FCF series + outputs hash (pipeline _outputs_hash inputs)."""
    years = _years()
    return {
        "group_revenue_net": {
            str(y): result.group_pnl.group_revenue_net.at(y) for y in years
        },
        "group_ebitda": {
            str(y): result.group_pnl.group_ebitda.at(y) for y in years
        },
        "group_fcf": {
            str(y): result.group_pnl.group_fcf.at(y) for y in years
        },
        "module_fcf": {
            mod: {str(y): result.module_outputs[mod].module_fcf.at(y) for y in years}
            for mod in sorted(result.module_outputs)
        },
        "implied_ev_2025_b": result.valuation.implied_ev_2025_billions,
        "outputs_hash": result.audit["outputs_hash"],
    }


def test_no_model_drift_against_baseline(model_result: ModelResult) -> None:
    assert BASELINE.exists(), f"baseline missing — record with: {BASELINE}"
    expected = json.loads(BASELINE.read_text(encoding="utf-8"))
    actual = _snapshot(model_result)

    assert actual["outputs_hash"] == expected["outputs_hash"]

    ev = actual["implied_ev_2025_b"]
    assert ev == pytest.approx(expected["implied_ev_2025_b"], rel=1e-9, abs=1e-6)

    for series_name in ("group_revenue_net", "group_ebitda", "group_fcf"):
        for year, exp_val in expected[series_name].items():
            assert actual[series_name][year] == pytest.approx(exp_val, rel=1e-9, abs=1e-6)

    for mod, years in expected["module_fcf"].items():
        for year, exp_val in years.items():
            assert actual["module_fcf"][mod][year] == pytest.approx(exp_val, rel=1e-9, abs=1e-6)
