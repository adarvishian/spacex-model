"""CAE absorptive-capacity water-fill — single-pass cascade (R112–R129)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc.allocator.priority import ModuleSpotIrrs, compute_softmax_shares
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class WaterFillResult:
    """Desired → capped → spillover → allocated final."""

    desired_cash: ModuleSpotIrrs
    capped_cash: ModuleSpotIrrs
    headroom: ModuleSpotIrrs
    spillover_weights: ModuleSpotIrrs
    allocated_final: ModuleSpotIrrs
    residual: YearVector


def compute_water_fill(
    remaining_pool: YearVector,
    desired_cash: ModuleSpotIrrs,
    initial_allocation: ModuleSpotIrrs,
    spot_irr: ModuleSpotIrrs,
    assumptions: Assumptions,
) -> WaterFillResult:
    """Single-pass water-fill: cap at desired, redistribute residual by exp(β·IRR).

    Excel cell:        Cash Allocation Engine!D127:D129
    Excel label:       "Allocated final: Starlink ($mm)" … "Allocated final: AI-Compute ($mm)"
    Architecture ref:  §2.3 water-fill (A-refresh V4.102)
    Principle:         4 (growth allocation capped at absorptive demand)

    """
    _, _, shares = compute_softmax_shares(spot_irr, assumptions)
    exp_irr, _, _ = compute_softmax_shares(spot_irr, assumptions)

    desired = desired_cash
    capped_sl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    capped_cl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    capped_ai = np.zeros(HORIZON_YEARS, dtype=np.float64)
    head_sl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    head_cl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    head_ai = np.zeros(HORIZON_YEARS, dtype=np.float64)
    final_sl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    final_cl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    final_ai = np.zeros(HORIZON_YEARS, dtype=np.float64)
    residual = np.zeros(HORIZON_YEARS, dtype=np.float64)

    init = initial_allocation
    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        pool = remaining_pool.values[t]
        if year == FIRST_YEAR or pool <= 0.0:
            continue

        d = (
            desired.starlink.values[t],
            desired.customer_launch.values[t],
            desired.ai_compute.values[t],
        )
        init_vals = (
            init.starlink.values[t],
            init.customer_launch.values[t],
            init.ai_compute.values[t],
        )
        spill_w = (
            exp_irr.starlink.values[t],
            exp_irr.customer_launch.values[t],
            exp_irr.ai_compute.values[t],
        )

        capped = [min(init_vals[i], d[i]) for i in range(3)]
        capped_sum = sum(capped)
        res = max(0.0, pool - capped_sum)
        residual[t] = res

        headroom = [max(0.0, d[i] - capped[i]) for i in range(3)]
        spill_total = sum(spill_w[i] for i in range(3) if headroom[i] > 0.0)

        spill_alloc = [0.0, 0.0, 0.0]
        if spill_total > 0.0 and res > 0.0:
            for i in range(3):
                if headroom[i] > 0.0:
                    spill_alloc[i] = min(headroom[i], res * spill_w[i] / spill_total)

        final = [capped[i] + spill_alloc[i] for i in range(3)]
        final_sum = sum(final)
        if final_sum > pool and final_sum > 0.0:
            scale = pool / final_sum
            final = [v * scale for v in final]

        capped_sl[t], capped_cl[t], capped_ai[t] = capped
        head_sl[t], head_cl[t], head_ai[t] = headroom
        final_sl[t], final_cl[t], final_ai[t] = final

    return WaterFillResult(
        desired_cash=desired_cash,
        capped_cash=ModuleSpotIrrs(
            starlink=YearVector(capped_sl),
            customer_launch=YearVector(capped_cl),
            ai_compute=YearVector(capped_ai),
        ),
        headroom=ModuleSpotIrrs(
            starlink=YearVector(head_sl),
            customer_launch=YearVector(head_cl),
            ai_compute=YearVector(head_ai),
        ),
        spillover_weights=exp_irr,
        allocated_final=ModuleSpotIrrs(
            starlink=YearVector(final_sl),
            customer_launch=YearVector(final_cl),
            ai_compute=YearVector(final_ai),
        ),
        residual=YearVector(residual),
    )
