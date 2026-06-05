"""Allocator package — V4.113 CAE cash pool, softmax, kg-rationing, water-fill."""

from spacex_model.calc.allocator.brain import AllocatorInputs, compute_allocator
from spacex_model.calc.allocator.carve_out import compute_carve_out
from spacex_model.calc.allocator.cash_pool import compute_cash_boy
from spacex_model.calc.allocator.demand_builders import compute_exogenous_demands
from spacex_model.calc.allocator.deployment import apply_first_year_override
from spacex_model.calc.allocator.irr_display import (
    compute_module_spot_irrs,
    roll_up_module_irrs,
)
from spacex_model.calc.allocator.kg_rationing import compute_kg_rationing
from spacex_model.calc.allocator.mars_carveout import compute_mars_carveout
from spacex_model.calc.allocator.physical_gates import (
    apply_f9_supply_gate,
    apply_v2_phase_out_gate,
    apply_v3_startup_gate,
)
from spacex_model.calc.allocator.priority import compute_softmax_allocation
from spacex_model.calc.allocator.queue_gate import (
    QueueGateResult,
    available_cash_for_irr_queue,
    compute_non_module_claims,
    compute_queue_gate,
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
from spacex_model.calc.allocator.water_fill import compute_water_fill

__all__ = [
    "AllocatorInputs",
    "AllocatorResult",
    "CashAllocations",
    "KgAllocations",
    "QueueGateResult",
    "QueueSubBlockDemands",
    "QueueSubBlockIrrs",
    "apply_first_year_override",
    "apply_f9_supply_gate",
    "apply_v2_phase_out_gate",
    "apply_v3_startup_gate",
    "available_cash_for_irr_queue",
    "compute_allocator",
    "compute_carve_out",
    "compute_cash_boy",
    "compute_exogenous_demands",
    "compute_kg_rationing",
    "compute_mars_carveout",
    "compute_module_spot_irrs",
    "compute_non_module_claims",
    "compute_queue_gate",
    "compute_sigmoid_cash_allocations",
    "compute_sigmoid_kg_allocations",
    "compute_softmax_allocation",
    "compute_vehicle_build_claim",
    "compute_water_fill",
    "roll_up_module_irrs",
]
