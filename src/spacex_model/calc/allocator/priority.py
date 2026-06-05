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
class FourProgramIrrs:
    """Prior-year spot IRR for four first-class programs (U2)."""

    starlink: YearVector
    odc: YearVector
    terrestrial: YearVector
    customer_launch: YearVector

    @classmethod
    def zeros(cls) -> FourProgramIrrs:
        z = YearVector.zeros()
        return cls(starlink=z, odc=z, terrestrial=z, customer_launch=z)


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


def compute_two_year_avg_prior_irr(spot_irr: FourProgramIrrs) -> FourProgramIrrs:
    """2-yr rolling average of prior-year marginal IRR (D3).

    Excel cell:        Cash Allocation Engine (U2 unified weights)
    Excel label:       "▸ IRR-weighted allocation parameters"
    Architecture ref:  PRD §5.2 priority + D3
    Principle:         2 (prior-yr IRR only; no this-year returns)

    """
    def _avg(vec: np.ndarray) -> np.ndarray:
        out = np.zeros(HORIZON_YEARS, dtype=np.float64)
        for t in range(HORIZON_YEARS):
            if t == 0:
                out[t] = vec[t]
            else:
                out[t] = 0.5 * (vec[t] + vec[t - 1])
        return out

    return FourProgramIrrs(
        starlink=YearVector(_avg(spot_irr.starlink.values)),
        odc=YearVector(_avg(spot_irr.odc.values)),
        terrestrial=YearVector(_avg(spot_irr.terrestrial.values)),
        customer_launch=YearVector(_avg(spot_irr.customer_launch.values)),
    )


def compute_soft_floor_shares(
    prior_irr_avg: FourProgramIrrs,
    assumptions: Assumptions,
    *,
    n_programs: int = 4,
) -> FourProgramIrrs:
    """Soft-floor shares from 2-yr-avg prior IRR weights (D1).

    Excel cell:        Cash Allocation Engine!D35:D37 (four-program extension)
    Excel label:       "Allocation share: Starlink" … "Allocation share: terrestrial"
    Architecture ref:  PRD §5.2 share = floor + (1−N·floor)·w/Σw
    Principle:         2 (priority order only; floor kept per D1)

    """
    floor = _soft_floor(assumptions)
    residual = max(0.0, 1.0 - n_programs * floor)

    share_sl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    share_odc = np.zeros(HORIZON_YEARS, dtype=np.float64)
    share_ter = np.zeros(HORIZON_YEARS, dtype=np.float64)
    share_cl = np.zeros(HORIZON_YEARS, dtype=np.float64)

    arrays = (
        prior_irr_avg.starlink.values,
        prior_irr_avg.odc.values,
        prior_irr_avg.terrestrial.values,
        prior_irr_avg.customer_launch.values,
    )
    for t in range(HORIZON_YEARS):
        weights = [max(0.0, w) for w in (arrays[0][t], arrays[1][t], arrays[2][t], arrays[3][t])]
        total = sum(weights)
        if total <= 0.0:
            share_sl[t] = share_odc[t] = share_ter[t] = share_cl[t] = 1.0 / n_programs
        else:
            share_sl[t] = floor + residual * weights[0] / total
            share_odc[t] = floor + residual * weights[1] / total
            share_ter[t] = floor + residual * weights[2] / total
            share_cl[t] = floor + residual * weights[3] / total

    return FourProgramIrrs(
        starlink=YearVector(share_sl),
        odc=YearVector(share_odc),
        terrestrial=YearVector(share_ter),
        customer_launch=YearVector(share_cl),
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
