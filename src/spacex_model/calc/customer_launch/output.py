"""Customer Launch output — bounded by allocator cash/kg (Phase B stub)."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.calc._allocator_allocation import AllocatorAllocation
from spacex_model.calc.customer_launch.demand import DemandResult
from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class OutputResult:
    """Deployed output after MIN(cash, kg, internal target) — zeros until Phase C."""

    units_deployed: YearVector


def compute_output(demand: DemandResult, allocation: AllocatorAllocation) -> OutputResult:
    """Output = MIN(cash_alloc / unit_cost, kg_alloc / mass, internal_target); Phase B returns zeros.

    Excel cell:        Customer Launch!— (Phase C)
    Excel label:       "Customer Launch proposed allocation ($mm)"
    Architecture ref:  §6.5 / §20.3 (Sprint 11f Option A)
    Principle:         12 (output bounded by cash; never feeds demand)

    """
    _ = (demand, allocation)
    return OutputResult(units_deployed=YearVector.zeros())
