"""AI - Compute orbital demand — exogenous per Sprint 11f Option A."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class DemandInputs:
    """Exogenous orbital-DC deployment demand in cash and kg."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


@dataclass(frozen=True, slots=True)
class DemandResult:
    """Masked exogenous demand (pass-through)."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


def compute_demand(inputs: DemandInputs) -> DemandResult:
    """Wanted deployment = exogenous cash and kg demand (Option A).

    Excel cell:        AI - Compute!— (Orbital DC)
    Excel label:       "ODC cash demand ($mm)"
    Architecture ref:  §9.2 / demand⊥output decoupling
    Principle:         12 (demand purely exogenous)

    Formula: Wanted deployment = exogenous cash and kg demand (Option A).

    """
    return DemandResult(
        cash_demand_mm=inputs.cash_demand_mm, kg_demand_kg=inputs.kg_demand_kg
    )
