"""ODC output — cash- and kg-bounded deployment (Phase D)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_allocation import AllocatorAllocation
from spacex_model.calc.odc.demand import DemandResult
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class OutputResult:
    """Sats deployed after MIN(cash, kg, target) — zero under Base Case per D6."""

    sats_deployed: YearVector


def compute_output(
    demand: DemandResult,
    allocation: AllocatorAllocation,
    *,
    unit_cost_mm: float = 50.0,
    mass_kg: float = 2000.0,
) -> OutputResult:
    """Actual deployment = MIN(cash/unit, kg/mass, exogenous demand cap).

    Excel cell:        ODC!— (Phase D)
    Excel label:       "ODC proposed allocation ($mm)"
    Architecture ref:  §20.8 (cash-driven deployment)
    Principle:         12 (output never feeds demand)

    """
    units = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        cash_units = allocation.cash_mm.values[t] / unit_cost_mm if unit_cost_mm > 0 else 0.0
        kg_units = allocation.kg_to_leo.values[t] / mass_kg if mass_kg > 0 else 0.0
        demand_units = demand.cash_demand_mm.values[t] / unit_cost_mm if unit_cost_mm > 0 else 0.0
        units[t] = max(0.0, min(cash_units, kg_units, demand_units))
    return OutputResult(sats_deployed=YearVector(units))
