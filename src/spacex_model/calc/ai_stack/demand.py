"""AI Stack demand — stub; zero deployment in v1 per D3."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class DemandInputs:
    """Stub demand inputs (zeroed in v1)."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


@dataclass(frozen=True, slots=True)
class DemandResult:
    """Zero demand permanently per project_ai_stack_no_launch_demand lock."""

    cash_demand_mm: YearVector
    kg_demand_kg: YearVector


def compute_demand(inputs: DemandInputs) -> DemandResult:
    """Exogenous demand — zeros in v1 (Sprint 6 pre-wire).

    Excel cell:        AI Stack!— (Phase C / v1.x)
    Excel label:       "AI Stack cash demand ($mm)"
    Architecture ref:  §12 AI Stack (v1 stub)
    Principle:         12 (demand decoupled from output)

    """
    return DemandResult(
        cash_demand_mm=inputs.cash_demand_mm,
        kg_demand_kg=inputs.kg_demand_kg,
    )
