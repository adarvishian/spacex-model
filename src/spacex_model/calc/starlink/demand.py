"""Starlink demand — four vehicle pools, exogenous Option A (Phase B stub)."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class DemandInputs:
    """Per-vehicle exogenous cash/kg demand (aggregated at module level in Phase C)."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


@dataclass(frozen=True, slots=True)
class DemandResult:
    """Masked demand after physical gates and IRR mask (Phase B: pass-through)."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


def compute_demand(inputs: DemandInputs) -> DemandResult:
    """Exogenous demand per vehicle pool; no output feedback (Sprint 11f Option A).

    Excel cell:        Starlink!— (Phase C)
    Excel label:       "Starlink cash demand ($mm)"
    Architecture ref:  §8.1 / §20.2 (vehicle-level queue)
    Principle:         12 (demand purely exogenous)

    """
    return DemandResult(
        cash_demand_mm=inputs.cash_demand_mm,
        kg_demand_kg=inputs.kg_demand_kg,
    )
