"""CAE kg-rationing gate — pro-rata allotment (R45–R52, defect F2 intact)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc.allocator.priority import ModuleSpotIrrs
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class KgRationingResult:
    """Pro-rata kg allotment independent of cash softmax (F2 defect)."""

    total_kg_demand: YearVector
    lm_kg_reserved: YearVector
    capacity_after_lm: YearVector
    kg_binding_flag: YearVector
    desired_kg: ModuleSpotIrrs
    allotment_kg: ModuleSpotIrrs


def compute_kg_rationing(
    desired_kg: ModuleSpotIrrs,
    total_capacity_kg: YearVector,
    lm_kg_reserved: YearVector,
) -> KgRationingResult:
    """Pro-rata kg gate: allotment_i = capacity × demand_i / Σdemand.

    Excel cell:        Cash Allocation Engine!D50:D52
    Excel label:       "Launch capacity allotment: Starlink (kg)" …
    Architecture ref:  §2.3 kg-rationing (superseded in U2)
    Principle:         12 (demand exogenous; ranks independently of cash)

    Note: CAE cached values show CL allotment often 0 while pro-rata ≠ 0 — defect F2/F4.

    """
    lm = lm_kg_reserved.values
    cap_after = np.maximum(0.0, total_capacity_kg.values - lm)

    dem_sl = desired_kg.starlink.values
    dem_cl = desired_kg.customer_launch.values
    dem_ai = desired_kg.ai_compute.values
    total_dem = dem_sl + dem_cl + dem_ai

    allot_sl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    allot_cl = np.zeros(HORIZON_YEARS, dtype=np.float64)
    allot_ai = np.zeros(HORIZON_YEARS, dtype=np.float64)
    binding = np.zeros(HORIZON_YEARS, dtype=np.float64)
    memo_total = np.zeros(HORIZON_YEARS, dtype=np.float64)

    for t in range(HORIZON_YEARS):
        td = total_dem[t]
        cap = cap_after[t]
        memo_total[t] = td
        if td > 0.0 and cap > 0.0:
            allot_sl[t] = cap * dem_sl[t] / td
            allot_cl[t] = cap * dem_cl[t] / td
            allot_ai[t] = cap * dem_ai[t] / td
        binding[t] = 1.0 if td > cap and cap > 0.0 else 0.0

    return KgRationingResult(
        total_kg_demand=YearVector(memo_total),
        lm_kg_reserved=lm_kg_reserved,
        capacity_after_lm=YearVector(cap_after),
        kg_binding_flag=YearVector(binding),
        desired_kg=desired_kg,
        allotment_kg=ModuleSpotIrrs(
            starlink=YearVector(allot_sl),
            customer_launch=YearVector(allot_cl),
            ai_compute=YearVector(allot_ai),
        ),
    )
