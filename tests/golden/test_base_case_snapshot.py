"""Golden snapshot regression — PRD §10.8 / §11.5 byte-stable reproducibility."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from spacex_model.engine.pipeline import ModelResult

GOLDEN = Path(__file__).resolve().parent / "base_case_snapshot.json"


def _current_snapshot(result: ModelResult) -> dict:
    return {
        "group_revenue_2025": result.group_pnl.group_revenue_net.at(2025),
        "group_ebitda_2025": result.group_pnl.group_ebitda.at(2025),
        "group_fcf_2025": result.group_pnl.group_fcf.at(2025),
        "implied_ev_2025_b": result.valuation.implied_ev_2025_billions,
        "module_fcf_2025": {
            k: result.module_outputs[k].module_fcf.at(2025) for k in sorted(result.module_outputs)
        },
        "outputs_hash": result.audit["outputs_hash"],
    }


def test_base_case_golden_snapshot(model_result: ModelResult) -> None:
    expected = json.loads(GOLDEN.read_text(encoding="utf-8"))
    actual = _current_snapshot(model_result)
    assert actual["outputs_hash"] == expected["outputs_hash"]
    for key in ("group_revenue_2025", "group_ebitda_2025", "group_fcf_2025", "implied_ev_2025_b"):
        assert actual[key] == pytest.approx(expected[key], rel=1e-9, abs=1e-6)
    for mod, fcf in expected["module_fcf_2025"].items():
        assert actual["module_fcf_2025"][mod] == pytest.approx(fcf, rel=1e-9, abs=1e-6)
