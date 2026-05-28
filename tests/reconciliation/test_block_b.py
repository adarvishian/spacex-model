"""Block B external calibration anchors — S-1 audited 2025 (audit §7.2 P0-11)."""

from __future__ import annotations

import pytest

from spacex_model.config.constants import FIRST_YEAR
from spacex_model.engine.pipeline import ModelResult
from spacex_model.testing.block_b_anchors import load_block_b_parametrize_args


@pytest.mark.parametrize(
    "name,target,tolerance,halt_low,halt_high",
    load_block_b_parametrize_args(),
)
def test_block_b_anchor(
    model_result: ModelResult,
    name: str,
    target: float,
    tolerance: float,
    halt_low: float,
    halt_high: float,
) -> None:
    actual = model_result.lookup_anchor(name, year=FIRST_YEAR)
    assert halt_low <= actual <= halt_high, (
        f"{name} 2025: actual={actual:,.0f} HALT range [{halt_low:,.0f}, {halt_high:,.0f}]"
    )
    if target == 0:
        assert abs(actual - target) <= 1.0, f"{name} 2025: expected exact {target}, got {actual}"
        return
    relative_err = abs(actual - target) / abs(target)
    assert relative_err <= tolerance, (
        f"{name} 2025: actual={actual:,.0f} target={target:,.0f} "
        f"err={relative_err:.2%} > tol={tolerance:.2%}"
    )
