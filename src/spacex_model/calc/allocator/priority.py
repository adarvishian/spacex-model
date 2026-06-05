"""CAE top-level IRR-softmax — exp(β·IRR) + soft floor (R27–R44)."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class ModuleSpotIrrs:
    """Prior-year spot IRR for the three CAE first-class modules."""

    starlink: YearVector
    customer_launch: YearVector
    ai_compute: YearVector

    @classmethod
    def zeros(cls) -> ModuleSpotIrrs:
        z = YearVector.zeros()
        return cls(starlink=z, customer_launch=z, ai_compute=z)


@dataclass(frozen=True, slots=True)
class SoftmaxAllocationResult:
    """Top-level softmax shares and pool-weighted cash (pre water-fill)."""

    spot_irr: ModuleSpotIrrs
    exp_irr: ModuleSpotIrrs
    exp_irr_sum: YearVector
    shares: ModuleSpotIrrs
    allocated_cash: ModuleSpotIrrs
    leftover_cash: YearVector


def _beta(assumptions: Assumptions) -> float:
    return assumption_scalar(
        assumptions,
        cl.ALLOCATION_SHARPNESS_TOP_LEVEL_3_MODULE_BLEND,
        default=3.0,
    )


def _soft_floor(assumptions: Assumptions) -> float:
    return assumption_scalar(
        assumptions,
        cl.ALLOCATOR_MIN_SOFTMAX_SHARE_FLOOR_PER_MODULE_FRAC,
        default=0.05,
    )


def compute_softmax_shares(
    spot_irr: ModuleSpotIrrs,
    assumptions: Assumptions,
    *,
    n_modules: int = 3,
) -> tuple[ModuleSpotIrrs, YearVector, ModuleSpotIrrs]:
    """exp(β·IRR) weights → soft-floor shares (D1).

    Excel cell:        Cash Allocation Engine!D35:D37
    Excel label:       "Allocation share: Starlink" … "Allocation share: AI-Compute"
    Architecture ref:  §5.2 priority (order only)
    Principle:         2 (prior-yr IRR drives softmax weights)

    """
    beta = _beta(assumptions)
    floor = _soft_floor(assumptions)
    residual = max(0.0, 1.0 - n_modules * floor)

    exp_sl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    exp_cl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    exp_ai = np.zeros(HORIZON_YEARS, dtype=np.float64)
    share_sl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    share_cl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    share_ai = np.zeros(HORIZON_YEARS, dtype=np.float64)
    exp_sum = np.zeros(HORIZON_YEARS, dtype=np.float64)

    for t in range(HORIZON_YEARS):
        irrs = (
            spot_irr.starlink.values[t],
            spot_irr.customer_launch.values[t],
            spot_irr.ai_compute.values[t],
        )
        weights = [math.exp(beta * irr) for irr in irrs]
        total = sum(weights)
        exp_sl[t], exp_cl[t], exp_ai[t] = weights
        exp_sum[t] = total
        if total <= 0.0:
            share_sl[t] = share_cl[t] = share_ai[t] = 1.0 / n_modules
        else:
            share_sl[t] = floor + residual * weights[0] / total
            share_cl[t] = floor + residual * weights[1] / total
            share_ai[t] = floor + residual * weights[2] / total

    exp_irr = ModuleSpotIrrs(
        starlink=YearVector(exp_sl),
        customer_launch=YearVector(exp_cl),
        ai_compute=YearVector(exp_ai),
    )
    shares = ModuleSpotIrrs(
        starlink=YearVector(share_sl),
        customer_launch=YearVector(share_cl),
        ai_compute=YearVector(share_ai),
    )
    return exp_irr, YearVector(exp_sum), shares


def compute_softmax_allocation(
    remaining_pool: YearVector,
    spot_irr: ModuleSpotIrrs,
    assumptions: Assumptions,
) -> SoftmaxAllocationResult:
    """Allocate remaining pool by softmax shares; 2025 anchor = 0.

    Excel cell:        Cash Allocation Engine!D39:D41
    Excel label:       "Allocated cash to Starlink ($mm)" … "Allocated cash to AI-Compute ($mm)"
    Architecture ref:  §2.3 CAE top-level IRR-softmax
    Principle:         4 (queue gate + carve-out before IRR allocation)

    """
    exp_irr, exp_sum, shares = compute_softmax_shares(spot_irr, assumptions)

    alloc_sl = remaining_pool.values * shares.starlink.values
    alloc_cl = remaining_pool.values * shares.customer_launch.values
    alloc_ai = remaining_pool.values * shares.ai_compute.values

    for t in range(HORIZON_YEARS):
        if FIRST_YEAR + t == FIRST_YEAR:
            alloc_sl[t] = alloc_cl[t] = alloc_ai[t] = 0.0

    allocated = ModuleSpotIrrs(
        starlink=YearVector(alloc_sl),
        customer_launch=YearVector(alloc_cl),
        ai_compute=YearVector(alloc_ai),
    )
    total_alloc = alloc_sl + alloc_cl + alloc_ai
    leftover = np.maximum(0.0, remaining_pool.values - total_alloc)

    return SoftmaxAllocationResult(
        spot_irr=spot_irr,
        exp_irr=exp_irr,
        exp_irr_sum=exp_sum,
        shares=shares,
        allocated_cash=allocated,
        leftover_cash=YearVector(leftover),
    )
