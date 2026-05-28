"""Lunar Mars output — ships deployed from carve-out cash (Phase B stub)."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.calc._allocator_allocation import AllocatorAllocation
from spacex_model.calc.lunar_mars.demand import DemandResult
from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class OutputResult:
    """Surface ships / payload deployed."""

    ships_deployed: YearVector


def compute_output(demand: DemandResult, allocation: AllocatorAllocation) -> OutputResult:
    """Bounded by carve-out allocation; Phase B returns zeros.

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "Lunar Mars proposed allocation ($mm)"
    Architecture ref:  §11 deployment
    Principle:         12 (output never feeds demand)

    """
    _ = (demand, allocation)
    return OutputResult(ships_deployed=YearVector.zeros())
