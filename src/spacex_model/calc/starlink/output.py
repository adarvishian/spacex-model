"""Starlink output — cash-, kg-, and F9-gated launches (Phase C)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_allocation import AllocatorAllocation
from spacex_model.calc.starlink.demand import DemandResult
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class OutputResult:
    """Launches deployed after MIN(cash/unit, kg/mass, internal target)."""

    sats_launched: YearVector


def compute_output(
    demand: DemandResult,
    allocation: AllocatorAllocation,
    *,
    unit_cost_mm: float = 1.0,
    mass_kg: float = 575.0,
) -> OutputResult:
    """Output = MIN(cash_alloc / unit_cost, kg_alloc / mass, demand cap).

    Excel cell:        Starlink!— (Phase C)
    Excel label:       "Starlink proposed allocation ($mm)"
    Architecture ref:  §8.1 / §20.2
    Principle:         12 (output bounded by cash; never feeds demand)

    """
    units = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        cash_units = allocation.cash_mm.values[t] / unit_cost_mm if unit_cost_mm > 0 else 0.0
        kg_units = allocation.kg_to_leo.values[t] / mass_kg if mass_kg > 0 else 0.0
        demand_units = demand.cash_demand_mm.values[t] / unit_cost_mm if unit_cost_mm > 0 else 0.0
        units[t] = max(0.0, min(cash_units, kg_units, demand_units))
    return OutputResult(sats_launched=YearVector(units))
