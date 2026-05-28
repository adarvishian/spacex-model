"""Customer Launch demand — exogenous per Sprint 11f Option A (Phase B stub)."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class DemandInputs:
    """Exogenous demand drivers; no allocator output references."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


@dataclass(frozen=True, slots=True)
class DemandResult:
    """Masked exogenous demand after IRR gate (zeros until Phase D)."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


def compute_demand(inputs: DemandInputs) -> DemandResult:
    """Exogenous demand: anchor × learning × year-mask + facility CapEx (Phase B: pass-through).

    Excel cell:        Customer Launch!— (Phase C)
    Excel label:       "Customer Launch cash demand ($mm)"
    Architecture ref:  §6.5 / §20.3 (Sprint 11f Option A)
    Principle:         12 (demand purely exogenous; output never feeds back)

    """
    return DemandResult(
        cash_demand_mm=inputs.cash_demand_mm,
        kg_demand_kg=inputs.kg_demand_kg,
    )
