"""Block C Q1 2026 sanity anchors — audit §7.3 P1-9."""

from __future__ import annotations

import pytest

from spacex_model.inputs.s1_profiles import (
    S1_Q1_2026_CAPEX_MM,
    S1_Q1_2026_OCF_MM,
    S1_Q1_2026_REVENUE_MM,
)


def test_q1_2026_anchor_constants() -> None:
    """S-1 disclosed Q1 2026 anchors from FIN_STMTS_NOTES_2."""
    assert S1_Q1_2026_REVENUE_MM == pytest.approx(4_694.0)
    assert S1_Q1_2026_OCF_MM == pytest.approx(1_047.0)
    assert S1_Q1_2026_CAPEX_MM == pytest.approx(10_107.0)


def test_q1_2026_annualized_sanity_vs_s1() -> None:
    """Annualized Q1 run-rate vs FY25 anchors — wide tolerance sense check."""
    fy25_revenue = 18_674.0
    fy25_capex = 20_737.0
    q1_rev_annualized = S1_Q1_2026_REVENUE_MM * 4
    q1_capex_annualized = S1_Q1_2026_CAPEX_MM * 4
    assert q1_rev_annualized / fy25_revenue == pytest.approx(1.005, rel=0.15)
    assert q1_capex_annualized / fy25_capex == pytest.approx(1.95, rel=0.25)
