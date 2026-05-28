"""Allocator package — cash/kg IRR queues and queue gate (Architecture §6)."""

from spacex_model.calc.allocator.brain import AllocatorInputs, compute_allocator
from spacex_model.calc.allocator.cash_pool import compute_cash_boy
from spacex_model.calc.allocator.demand_builders import compute_exogenous_demands
from spacex_model.calc.allocator.deployment import apply_first_year_override
from spacex_model.calc.allocator.irr_display import roll_up_module_irrs
from spacex_model.calc.allocator.mars_carveout import compute_mars_carveout
from spacex_model.calc.allocator.physical_gates import (
    apply_f9_supply_gate,
    apply_v2_phase_out_gate,
    apply_v3_startup_gate,
)
from spacex_model.calc.allocator.queue_gate import (
    available_cash_for_irr_queue,
    compute_non_module_claims,
)
from spacex_model.calc.allocator.sigmoid_cash import compute_sigmoid_cash_allocations
from spacex_model.calc.allocator.sigmoid_kg import compute_sigmoid_kg_allocations
from spacex_model.calc.allocator.types import (
    AllocatorResult,
    CashAllocations,
    KgAllocations,
    QueueSubBlockDemands,
    QueueSubBlockIrrs,
)
from spacex_model.calc.allocator.vehicle_build import compute_vehicle_build_claim

__all__ = [
    "AllocatorInputs",
    "AllocatorResult",
    "CashAllocations",
    "KgAllocations",
    "QueueSubBlockDemands",
    "QueueSubBlockIrrs",
    "apply_first_year_override",
    "apply_f9_supply_gate",
    "apply_v2_phase_out_gate",
    "apply_v3_startup_gate",
    "available_cash_for_irr_queue",
    "compute_allocator",
    "compute_cash_boy",
    "compute_exogenous_demands",
    "compute_mars_carveout",
    "compute_non_module_claims",
    "compute_sigmoid_cash_allocations",
    "compute_sigmoid_kg_allocations",
    "compute_vehicle_build_claim",
    "roll_up_module_irrs",
]
