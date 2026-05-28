"""Allocator IN allocation types — cash and kg per module (Phase B contract)."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class AllocatorAllocation:
    """Cash and kg-to-LEO allocations from the Allocator for one module or vehicle."""

    cash_mm: YearVector
    kg_to_leo: YearVector

    @classmethod
    def zeros(cls) -> AllocatorAllocation:
        z = YearVector.zeros()
        return cls(cash_mm=z, kg_to_leo=z)
