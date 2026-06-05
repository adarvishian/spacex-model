"""CAE Level-2 within-AI split — ODC vs Terrestrial softmax (R76–R94)."""

from __future__ import annotations

from dataclasses import dataclass

import math

import numpy as np

from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class Level2SplitResult:
    """ODC / Terrestrial cash split inside AI-Compute roll-up."""

    spot_irr_odc: YearVector
    spot_irr_terrestrial: YearVector
    share_odc: YearVector
    share_terrestrial: YearVector
    allocated_odc: YearVector
    allocated_terrestrial: YearVector
    spillover_odc: YearVector
    spillover_terrestrial: YearVector


def compute_level2_split(
    ai_compute_cash: YearVector,
    spot_irr_odc: YearVector,
    spot_irr_terrestrial: YearVector,
    desired_odc: YearVector,
    desired_terrestrial: YearVector,
    assumptions: Assumptions,
) -> Level2SplitResult:
    """Level-2 softmax split of AI-Compute pool between ODC and Terrestrial.

    Excel cell:        Cash Allocation Engine!D88:D90
    Excel label:       "Orbital DC: allocated cash ($mm) ◄ CAE Level-2"
    Architecture ref:  §2.3 Level-2 within-AI (superseded in U2)
    Principle:         2 (IRR-priority sub-split inside AI roll-up)

    """
    beta = assumption_scalar(
        assumptions,
        cl.ALLOCATION_SHARPNESS_AI_ORBITAL_TERRESTRIAL_SUB_SPLIT,
        default=3.0,
    )
    floor = assumption_scalar(
        assumptions,
        cl.ALLOCATOR_MIN_SOFTMAX_SHARE_FLOOR_PER_MODULE_FRAC,
        default=0.05,
    )
    n = 2
    residual = max(0.0, 1.0 - n * floor)

    share_odc = np.zeros(HORIZON_YEARS, dtype=np.float64)
    share_ter = np.zeros(HORIZON_YEARS, dtype=np.float64)
    alloc_odc = np.zeros(HORIZON_YEARS, dtype=np.float64)
    alloc_ter = np.zeros(HORIZON_YEARS, dtype=np.float64)
    spill_odc = np.zeros(HORIZON_YEARS, dtype=np.float64)
    spill_ter = np.zeros(HORIZON_YEARS, dtype=np.float64)

    for t in range(HORIZON_YEARS):
        if FIRST_YEAR + t == FIRST_YEAR:
            continue
        pool = ai_compute_cash.values[t]
        if pool <= 0.0:
            continue
        irrs = (spot_irr_odc.values[t], spot_irr_terrestrial.values[t])
        weights = [math.exp(beta * irr) for irr in irrs]
        total = sum(weights)
        if total <= 0.0:
            share_odc[t] = share_ter[t] = 0.5
        else:
            share_odc[t] = floor + residual * weights[0] / total
            share_ter[t] = floor + residual * weights[1] / total

        init_odc = pool * share_odc[t]
        init_ter = pool * share_ter[t]
        d_odc = desired_odc.values[t]
        d_ter = desired_terrestrial.values[t]
        capped_odc = min(init_odc, d_odc) if d_odc > 0.0 else init_odc
        capped_ter = min(init_ter, d_ter) if d_ter > 0.0 else init_ter
        res = max(0.0, pool - capped_odc - capped_ter)
        head_odc = max(0.0, d_odc - capped_odc)
        head_ter = max(0.0, d_ter - capped_ter)
        spill_w_odc, spill_w_ter = weights
        spill_total = (spill_w_odc if head_odc > 0 else 0) + (spill_w_ter if head_ter > 0 else 0)
        extra_odc = extra_ter = 0.0
        if spill_total > 0.0 and res > 0.0:
            if head_odc > 0.0:
                extra_odc = min(head_odc, res * spill_w_odc / spill_total)
            if head_ter > 0.0:
                extra_ter = min(head_ter, res * spill_w_ter / spill_total)
        alloc_odc[t] = capped_odc + extra_odc
        alloc_ter[t] = capped_ter + extra_ter
        spill_odc[t] = extra_odc
        spill_ter[t] = extra_ter

    return Level2SplitResult(
        spot_irr_odc=spot_irr_odc,
        spot_irr_terrestrial=spot_irr_terrestrial,
        share_odc=YearVector(share_odc),
        share_terrestrial=YearVector(share_ter),
        allocated_odc=YearVector(alloc_odc),
        allocated_terrestrial=YearVector(alloc_ter),
        spillover_odc=YearVector(spill_odc),
        spillover_terrestrial=YearVector(spill_ter),
    )
