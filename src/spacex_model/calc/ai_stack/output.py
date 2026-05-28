"""AI Stack output — zero in v1."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.calc._allocator_allocation import AllocatorAllocation
from spacex_model.calc.ai_stack.demand import DemandResult
from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class OutputResult:
    """Zero output in v1."""

    units_deployed: YearVector


def compute_output(demand: DemandResult, allocation: AllocatorAllocation) -> OutputResult:
    """Zero deployment in v1.

    Excel cell:        AI Stack!— (v1.x)
    Excel label:       "AI Stack proposed allocation ($mm)"
    Architecture ref:  §12 AI Stack stub
    Principle:         12 (output never feeds demand)

    """
    _ = (demand, allocation)
    return OutputResult(units_deployed=YearVector.zeros())
