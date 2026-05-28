"""Per-unit IRR engine unit tests — PRD §2.6 / §10.1."""

from __future__ import annotations

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from spacex_model.domain.irr import IRR_CUTOFF, _solve_irr, compute_irr_engine


def test_all_negative_cashflows_return_cutoff() -> None:
    cf = np.array([-10.0, -1.0, -2.0, -3.0], dtype=np.float64)
    assert _solve_irr(cf) == IRR_CUTOFF
    rev = np.array([-1.0, -2.0, -3.0], dtype=np.float64)
    result = compute_irr_engine(10.0, rev, horizon_n=3)
    assert result.spot == IRR_CUTOFF


def test_all_positive_cashflows_return_zero_convention() -> None:
    cf = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    assert _solve_irr(cf) == 0.0
    result = compute_irr_engine(0.0, np.array([1.0, 2.0, 3.0]), horizon_n=3)
    assert result.spot == 0.0


def test_mixed_sign_stream_returns_valid_irr() -> None:
    cf = np.array([-100.0, 40.0, 40.0, 40.0, 40.0, 40.0], dtype=np.float64)
    spot = _solve_irr(cf)
    assert spot > IRR_CUTOFF
    periods = np.arange(len(cf), dtype=np.float64)
    npv = np.sum(cf / np.power(1.0 + spot, periods))
    assert abs(npv) < 1e-2

    result = compute_irr_engine(100.0, cf[1:], horizon_n=5)
    assert result.spot > IRR_CUTOFF


@pytest.mark.slow
@given(
    cost=st.floats(min_value=10.0, max_value=200.0),
    r0=st.floats(min_value=5.0, max_value=80.0),
    r1=st.floats(min_value=5.0, max_value=80.0),
    r2=st.floats(min_value=5.0, max_value=80.0),
)
@settings(max_examples=50, deadline=10_000)
def test_random_mixed_sign_streams_npv_near_zero(
    cost: float,
    r0: float,
    r1: float,
    r2: float,
) -> None:
    """Excel IRR parity within 1e-2 NPV tolerance on generated streams."""
    rev = np.array([r0, r1, r2], dtype=np.float64)
    result = compute_irr_engine(cost, rev, horizon_n=3)
    if result.blended <= IRR_CUTOFF + 1e-9:
        return
    cf = np.concatenate(([-cost], rev))
    periods = np.arange(len(cf), dtype=np.float64)
    npv = np.sum(cf / np.power(1.0 + result.blended, periods))
    assert abs(npv) < 1e-2
