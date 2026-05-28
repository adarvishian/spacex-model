"""ODC demand — exogenous per Sprint 11f Option A (Phase B stub)."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class DemandInputs:
    """Exogenous ODC deployment demand in cash and kg."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


@dataclass(frozen=True, slots=True)
class DemandResult:
    """Masked exogenous demand (zeros under V2.16 verdict per D6)."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


def compute_demand(inputs: DemandInputs) -> DemandResult:
    """Wanted deployment = wanted_sat_count × cost_per_sat (exogenous; Phase B pass-through).

    Excel cell:        ODC!— (Phase C)
    Excel label:       "ODC cash demand ($mm)"
    Architecture ref:  §20.8 / §6.5 (Sprint 11f Option A)
    Principle:         12 (demand purely exogenous)

    """
    return DemandResult(
        cash_demand_mm=inputs.cash_demand_mm,
        kg_demand_kg=inputs.kg_demand_kg,
    )
