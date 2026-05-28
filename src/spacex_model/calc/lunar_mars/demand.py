"""Lunar Mars demand — strategic carve-out; not in IRR queue."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class DemandInputs:
    """Carve-out cash demand (exogenous from Mars/Lunar share)."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


@dataclass(frozen=True, slots=True)
class DemandResult:
    """Deployment demand from carve-out cash."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


def compute_demand(inputs: DemandInputs) -> DemandResult:
    """Exogenous carve-out-driven demand (Phase B pass-through).

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "Lunar Mars cash demand ($mm)"
    Architecture ref:  §11 strategic carve-out
    Principle:         22 (Mars carve-off prior-year Group FCF)

    """
    return DemandResult(
        cash_demand_mm=inputs.cash_demand_mm,
        kg_demand_kg=inputs.kg_demand_kg,
    )
