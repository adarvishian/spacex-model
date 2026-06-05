"""CAE carve-out — Lunar/Mars senior claim + remaining pool (R23–R25)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc.lunar_mars.carveout import compute_mars_carveout
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class CarveOutResult:
    """Senior LM carve-out and IRR-weighted remaining pool."""

    lunar_mars_carveout: YearVector
    remaining_pool: YearVector


def compute_carve_out(
    assumptions: Assumptions,
    pool_after_gate: YearVector,
    prior_year_group_fcf: YearVector | None = None,
) -> CarveOutResult:
    """LM carve-out off the top; remaining pool gated to 0 in 2025 anchor.

    Excel cell:        Cash Allocation Engine!D24:D25
    Excel label:       "Lunar/Mars carve-out cash ($mm)" … "Remaining pool for IRR-weighted allocation ($mm)"
    Architecture ref:  §2.3 carve-out + §5.2 senior claims
    Principle:         22 (Mars carve-out off-the-top on prior-yr FCF)
    
    Formula: LM carve-out off the top; remaining pool gated to 0 in 2025 anchor.

    ODC strategic seed is a separate senior claim after LM carve-out (U3); LM uses prior FCF × pct.

    """
    carveout = compute_mars_carveout(assumptions, prior_year_group_fcf)
    remaining = np.maximum(0.0, pool_after_gate.values - carveout.values)
    for t in range(HORIZON_YEARS):
        if FIRST_YEAR + t == FIRST_YEAR:
            remaining[t] = 0.0
    return CarveOutResult(
        lunar_mars_carveout=carveout,
        remaining_pool=YearVector(remaining),
    )
