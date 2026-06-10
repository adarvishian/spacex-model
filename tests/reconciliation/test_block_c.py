"""Block C sense / sanity checks — PRD §7.3 / V4.131 horizon."""

from __future__ import annotations

import numpy as np
import pytest

from spacex_model.calc.customer_launch.module import CustomerLaunchInputs, _starship_customer_launches
from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.engine.pipeline import ModelResult
from spacex_model.inputs.v4_131_2025_anchors import V4_131_INGEST_ANCHORS_2025


def test_no_nan_or_inf(model_result: ModelResult) -> None:
    for name, vec in model_result.all_year_vectors():
        assert not np.any(np.isnan(vec)), f"{name} contains NaN"
        assert not np.any(np.isinf(vec)), f"{name} contains inf"


def test_starship_launches_2025_near_zero(model_result: ModelResult) -> None:
    # Supply-side fleet may show fractional pre-commercial activity; customer = 0 (S-1)
    assert abs(model_result.starship_launches(FIRST_YEAR)) < 0.5


def test_starship_customer_launches_2026_positive(model_result: ModelResult) -> None:
    """P1-5: S-1 expects small positive customer Starship launches from 2H 2026."""
    cl = CustomerLaunchInputs(
        assumptions=model_result.assumptions,
        launch_capacity=model_result.launch_capacity,
    )
    assert _starship_customer_launches(cl).at(2026) >= 2.0


def test_f9_launches_2025(model_result: ModelResult) -> None:
    launches = model_result.f9_launches(FIRST_YEAR)
    assert 165 <= launches <= 177, f"F9 launches 2025: {launches}"


@pytest.mark.expected_disposition_D4
def test_f9_customer_launch_irr_disposition(model_result: ModelResult) -> None:
    """D4: F9 Blended IRR expected outside [8%, 25%] — recorded disposition, no halt."""
    irr = model_result.module_outputs["customer_launch"].blended_irr.at(FIRST_YEAR)
    assert irr > 0.0 or irr == -1.0


def test_ai_compute_s1_revenue_2025(model_result: ModelResult) -> None:
    """V4.131: AI - Compute carries S-1 AI segment revenue anchor in 2025."""
    anchor = next(a for a in V4_131_INGEST_ANCHORS_2025 if "AI segment" in a.name)
    actual = model_result.module_outputs["ai_compute"].total_revenue.at(FIRST_YEAR)
    assert actual == pytest.approx(anchor.target, rel=anchor.tolerance_pct)


def test_implied_dtc_subs_2025_sane(model_result: ModelResult) -> None:
    subs = model_result.starlink_dtc_subs_eoy(FIRST_YEAR)
    assert subs < 15_000_000, f"Implied DTC subs 2025: {subs:,.0f}"


def test_wrights_law_monotone(model_result: ModelResult) -> None:
    cost = model_result.starlink_sat_cost_per_kg()
    assert all(cost[i] >= cost[i + 1] for i in range(len(cost) - 1)), "Wright's Law violation"


@pytest.mark.parametrize("year", [2025, 2026])
def test_starlink_v3_pre_trigger_zero(model_result: ModelResult, year: int) -> None:
    assert model_result.starlink_v3_bb_launches(year) == 0.0
    assert model_result.starlink_v3_dtc_launches(year) == 0.0


def test_starlink_v2_post_phaseout_zero(model_result: ModelResult) -> None:
    for year in range(2028, LAST_YEAR + 1):
        assert model_result.starlink_v2_bb_launches(year) == 0.0
        assert model_result.starlink_v2_dtc_launches(year) == 0.0
