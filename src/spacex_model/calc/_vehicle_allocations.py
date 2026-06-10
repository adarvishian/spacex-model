"""Per-vehicle Allocator IN allocations for Starlink vehicle pools."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.calc._allocator_allocation import AllocatorAllocation
from spacex_model.calc.allocator.types import CashAllocations, KgAllocations
from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class VehicleAllocations:
    """Cash and kg allocations mapped to four Starlink vehicle pools."""

    v2_bb: AllocatorAllocation
    v2_dtc: AllocatorAllocation
    v3_bb: AllocatorAllocation
    v3_dtc: AllocatorAllocation

    @classmethod
    def from_allocator(
        cls,
        cash: CashAllocations,
        kg: KgAllocations,
    ) -> VehicleAllocations:
        z = YearVector.zeros()
        return cls(
            v2_bb=AllocatorAllocation(cash_mm=cash.starlink_v2_bb, kg_to_leo=z),
            v2_dtc=AllocatorAllocation(cash_mm=cash.starlink_v2_dtc, kg_to_leo=z),
            v3_bb=AllocatorAllocation(
                cash_mm=cash.starlink_v3_bb,
                kg_to_leo=kg.starlink_v3_bb,
            ),
            v3_dtc=AllocatorAllocation(
                cash_mm=cash.starlink_v3_dtc,
                kg_to_leo=kg.starlink_v3_dtc,
            ),
        )

    @classmethod
    def zeros(cls) -> VehicleAllocations:
        z = YearVector.zeros()
        alloc = AllocatorAllocation(cash_mm=z, kg_to_leo=z)
        return cls(v2_bb=alloc, v2_dtc=alloc, v3_bb=alloc, v3_dtc=alloc)
