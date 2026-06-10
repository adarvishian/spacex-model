"""Allocator datatypes — cash/kg allocations, demands, IRRs, and result bundle."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from spacex_model.domain.year_vector import YearVector

if TYPE_CHECKING:
    from spacex_model.calc.allocator.debt_facilities import DebtFacilitiesResult


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
            customer_launch=z, starlink_v3_bb=z, starlink_v3_dtc=z, odc=z, ai_stack=z
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
    """Full CAE allocator outputs for downstream modules and Group P&L."""

    cash: CashAllocations
    kg: KgAllocations
    cash_boy: YearVector
    available_cash: YearVector
    mars_carveout: YearVector
    vehicle_build_claim: YearVector
    non_module_claims: YearVector
    capacity_available_kg: YearVector
    pool_after_gate: YearVector | None = None
    remaining_pool: YearVector | None = None
    allocated_final_starlink: YearVector | None = None
    allocated_final_customer_launch: YearVector | None = None
    allocated_final_ai_compute: YearVector | None = None
    kg_binding_flag: YearVector | None = None
    total_desired_launch_kg: YearVector | None = None
    memo_total_kg_demand: YearVector | None = None
    growth_cap_starlink: YearVector | None = None
    growth_cap_customer_launch: YearVector | None = None
    growth_cap_ai_compute: YearVector | None = None
    maintenance_claim: YearVector | None = None
    enabling_infra_equity: YearVector | None = None
    chip_at_cost_per_sat: YearVector | None = None
    water_fill_residual: YearVector | None = None
    allocated_final_odc: YearVector | None = None
    allocated_final_terrestrial: YearVector | None = None
    capped_share_starlink: YearVector | None = None
    capped_share_odc: YearVector | None = None
    capped_share_terrestrial: YearVector | None = None
    capped_share_customer_launch: YearVector | None = None
    ship_slots_used: YearVector | None = None
    ship_slots_idle: YearVector | None = None
    strategic_seed_cash: YearVector | None = None
    strategic_seed_kg: YearVector | None = None
    odc_graduated: YearVector | None = None
    odc_total_cash: YearVector | None = None
    debt_odc_draw: YearVector | None = None
    debt_terafab_draw: YearVector | None = None
    odc_pool_cash: YearVector | None = None
    cash_available_for_year: YearVector | None = None
    cash_eoy: YearVector | None = None
    debt: DebtFacilitiesResult | None = None

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
            pool_after_gate=z,
            remaining_pool=z,
            allocated_final_starlink=z,
            allocated_final_customer_launch=z,
            allocated_final_ai_compute=z,
            kg_binding_flag=z,
            total_desired_launch_kg=z,
            memo_total_kg_demand=z,
            growth_cap_starlink=z,
            growth_cap_customer_launch=z,
            growth_cap_ai_compute=z,
            maintenance_claim=z,
            enabling_infra_equity=z,
            chip_at_cost_per_sat=z,
            water_fill_residual=z,
            allocated_final_odc=z,
            allocated_final_terrestrial=z,
            capped_share_starlink=z,
            capped_share_odc=z,
            capped_share_terrestrial=z,
            capped_share_customer_launch=z,
            ship_slots_used=z,
            ship_slots_idle=z,
            strategic_seed_cash=z,
            strategic_seed_kg=z,
            odc_graduated=z,
            odc_total_cash=z,
            debt_odc_draw=z,
            debt_terafab_draw=z,
            odc_pool_cash=z,
            cash_available_for_year=z,
            cash_eoy=z,
            debt=None,
        )
