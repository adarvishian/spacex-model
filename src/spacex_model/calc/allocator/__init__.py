"""Allocator package — V4.113 CAE cash pool + unified two-resource fill (U2)."""

from spacex_model.calc.allocator.brain import AllocatorInputs, compute_allocator
from spacex_model.calc.allocator.carve_out import compute_carve_out
from spacex_model.calc.allocator.cash_pool import compute_cash_boy
from spacex_model.calc.allocator.conservation import (
    AllocatorConservationInputs,
    AllocatorConservationResult,
    compute_allocator_conservation,
    compute_r14_cash_flow_identity,
)
from spacex_model.calc.allocator.demand_builders import compute_exogenous_demands
from spacex_model.calc.allocator.deployment import apply_first_year_override
from spacex_model.calc.allocator.irr_display import (
    compute_four_program_prior_irrs,
    compute_module_spot_irrs,
    roll_up_module_irrs,
)
from spacex_model.calc.allocator.priority import FourProgramIrrs, compute_softmax_shares
from spacex_model.calc.allocator.strategic_seed import compute_strategic_seed
from spacex_model.calc.allocator.two_resource_fill import compute_two_resource_fill
from spacex_model.calc.allocator.mars_carveout import compute_mars_carveout
from spacex_model.calc.allocator.physical_gates import (
    apply_f9_supply_gate,
    apply_v2_phase_out_gate,
    apply_v3_startup_gate,
)
from spacex_model.calc.allocator.queue_gate import (
    QueueGateResult,
    available_cash_for_irr_queue,
    compute_non_module_claims,
    compute_queue_gate,
)
from spacex_model.calc.allocator.types import (
    AllocatorResult,
    CashAllocations,
    KgAllocations,
    QueueSubBlockDemands,
    QueueSubBlockIrrs,
)
from spacex_model.calc.allocator.vehicle_build import compute_vehicle_build_claim

__all__ = [
    "AllocatorConservationInputs",
    "AllocatorConservationResult",
    "AllocatorInputs",
    "AllocatorResult",
    "CashAllocations",
    "FourProgramIrrs",
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
    "compute_allocator_conservation",
    "compute_carve_out",
    "compute_cash_boy",
    "compute_exogenous_demands",
    "compute_four_program_prior_irrs",
    "compute_mars_carveout",
    "compute_module_spot_irrs",
    "compute_non_module_claims",
    "compute_queue_gate",
    "compute_r14_cash_flow_identity",
    "compute_softmax_shares",
    "compute_strategic_seed",
    "compute_two_resource_fill",
    "compute_vehicle_build_claim",
    "roll_up_module_irrs",
]
