"""AI - Compute orbital output — cash- and kg-bounded deployment."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_allocation import AllocatorAllocation
from spacex_model.calc.ai_compute.demand import DemandResult
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class OutputResult:
    """Orbital DC sats deployed after MIN(cash, kg, target)."""

    sats_deployed: YearVector


def compute_output(
    demand: DemandResult,
    allocation: AllocatorAllocation,
    assumptions: Assumptions | None = None,
    *,
    unit_cost_mm: float | None = None,
    mass_kg: float | None = None,
) -> OutputResult:
    """Actual deployment = MIN(cash/unit, kg/mass, exogenous demand cap).

    Excel cell:        AI - Compute!— (Orbital DC)
    Excel label:       "Orbital DC proposed allocation ($mm)"
    Architecture ref:  §9.2 (cash-driven deployment)
    Principle:         12 (output never feeds demand)

    """
    if assumptions is not None:
        if unit_cost_mm is None and assumptions.lookup(cl.V3_BB_SAT_UNIT_COST_MM_SAT) is not None:
            unit_cost_mm = assumption_scalar(assumptions, cl.V3_BB_SAT_UNIT_COST_MM_SAT, default=50.0)
        if mass_kg is None:
            mass_kg = assumption_scalar(assumptions, cl.V3_BB_SAT_MASS_KG, default=2000.0)
    cost = unit_cost_mm if unit_cost_mm is not None else 50.0
    mass = mass_kg if mass_kg is not None else 2000.0

    units = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        cash_units = allocation.cash_mm.values[t] / cost if cost > 0 else 0.0
        kg_units = allocation.kg_to_leo.values[t] / mass if mass > 0 else 0.0
        demand_units = demand.cash_demand_mm.values[t] / cost if cost > 0 else 0.0
        units[t] = max(0.0, min(cash_units, kg_units, demand_units))
    return OutputResult(sats_deployed=YearVector(units))
