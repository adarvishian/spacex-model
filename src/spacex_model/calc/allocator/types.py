"""Allocator datatypes — cash/kg allocations, demands, IRRs, and result bundle."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class CashAllocations:
    """Seven cash-queue sub-block allocations ($mm)."""

    customer_launch: YearVector
    starlink_v2_bb: YearVector
    starlink_v2_dtc: YearVector
    starlink_v3_bb: YearVector
    starlink_v3_dtc: YearVector
    odc: YearVector
    ai_stack: YearVector

    @classmethod
    def zeros(cls) -> CashAllocations:
        z = YearVector.zeros()
        return cls(
            customer_launch=z,
            starlink_v2_bb=z,
            starlink_v2_dtc=z,
            starlink_v3_bb=z,
            starlink_v3_dtc=z,
            odc=z,
            ai_stack=z,
        )

    def as_tuple(self) -> tuple[YearVector, ...]:
        return (
            self.customer_launch,
            self.starlink_v2_bb,
            self.starlink_v2_dtc,
            self.starlink_v3_bb,
            self.starlink_v3_dtc,
            self.odc,
            self.ai_stack,
        )


@dataclass(frozen=True, slots=True)
class KgAllocations:
    """Five kg-queue sub-block allocations (kg-to-LEO)."""

    customer_launch: YearVector
    starlink_v3_bb: YearVector
    starlink_v3_dtc: YearVector
    odc: YearVector
    ai_stack: YearVector

    @classmethod
    def zeros(cls) -> KgAllocations:
        z = YearVector.zeros()
        return cls(
            customer_launch=z,
            starlink_v3_bb=z,
            starlink_v3_dtc=z,
            odc=z,
            ai_stack=z,
        )

    def as_tuple(self) -> tuple[YearVector, ...]:
        return (
            self.customer_launch,
            self.starlink_v3_bb,
            self.starlink_v3_dtc,
            self.odc,
            self.ai_stack,
        )


@dataclass(frozen=True, slots=True)
class QueueSubBlockDemands:
    """Exogenous cash + kg demands for IRR sigmoid queues (Sprint 11f Option A)."""

    customer_launch_cash: YearVector
    starlink_v2_bb_cash: YearVector
    starlink_v2_dtc_cash: YearVector
    starlink_v3_bb_cash: YearVector
    starlink_v3_dtc_cash: YearVector
    odc_cash: YearVector
    ai_stack_cash: YearVector
    customer_launch_kg: YearVector
    starlink_v3_bb_kg: YearVector
    starlink_v3_dtc_kg: YearVector
    odc_kg: YearVector
    ai_stack_kg: YearVector

    @classmethod
    def zeros(cls) -> QueueSubBlockDemands:
        z = YearVector.zeros()
        return cls(
            customer_launch_cash=z,
            starlink_v2_bb_cash=z,
            starlink_v2_dtc_cash=z,
            starlink_v3_bb_cash=z,
            starlink_v3_dtc_cash=z,
            odc_cash=z,
            ai_stack_cash=z,
            customer_launch_kg=z,
            starlink_v3_bb_kg=z,
            starlink_v3_dtc_kg=z,
            odc_kg=z,
            ai_stack_kg=z,
        )

    def cash_tuple(self) -> tuple[YearVector, ...]:
        return (
            self.customer_launch_cash,
            self.starlink_v2_bb_cash,
            self.starlink_v2_dtc_cash,
            self.starlink_v3_bb_cash,
            self.starlink_v3_dtc_cash,
            self.odc_cash,
            self.ai_stack_cash,
        )

    def kg_tuple(self) -> tuple[YearVector, ...]:
        return (
            self.customer_launch_kg,
            self.starlink_v3_bb_kg,
            self.starlink_v3_dtc_kg,
            self.odc_kg,
            self.ai_stack_kg,
        )


@dataclass(frozen=True, slots=True)
class QueueSubBlockIrrs:
    """Blended IRR year-vectors for each cash-queue sub-block."""

    customer_launch: YearVector
    starlink_v2_bb: YearVector
    starlink_v2_dtc: YearVector
    starlink_v3_bb: YearVector
    starlink_v3_dtc: YearVector
    odc: YearVector
    ai_stack: YearVector

    @classmethod
    def zeros(cls) -> QueueSubBlockIrrs:
        z = YearVector.zeros()
        return cls(
            customer_launch=z,
            starlink_v2_bb=z,
            starlink_v2_dtc=z,
            starlink_v3_bb=z,
            starlink_v3_dtc=z,
            odc=z,
            ai_stack=z,
        )

    def as_tuple(self) -> tuple[YearVector, ...]:
        return (
            self.customer_launch,
            self.starlink_v2_bb,
            self.starlink_v2_dtc,
            self.starlink_v3_bb,
            self.starlink_v3_dtc,
            self.odc,
            self.ai_stack,
        )


@dataclass(frozen=True, slots=True)
class AllocatorResult:
    """Full Allocator brain outputs for downstream modules and Group P&L."""

    cash: CashAllocations
    kg: KgAllocations
    cash_boy: YearVector
    available_cash: YearVector
    mars_carveout: YearVector
    vehicle_build_claim: YearVector
    non_module_claims: YearVector
    capacity_available_kg: YearVector

    @classmethod
    def zeros(cls) -> AllocatorResult:
        z = YearVector.zeros()
        return cls(
            cash=CashAllocations.zeros(),
            kg=KgAllocations.zeros(),
            cash_boy=z,
            available_cash=z,
            mars_carveout=z,
            vehicle_build_claim=z,
            non_module_claims=z,
            capacity_available_kg=z,
        )
