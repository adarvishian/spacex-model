"""Allocator brain — orchestrates cash pool, queue gate, sigmoid queues (Architecture §6)."""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.cash_pool import compute_cash_boy
from spacex_model.calc.allocator.demand_builders import compute_exogenous_demands
from spacex_model.calc.allocator.deployment import apply_first_year_override, cap_cash_allocations_to_available
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
    QueueSubBlockDemands,
    QueueSubBlockIrrs,
)
from spacex_model.calc.allocator.vehicle_build import compute_vehicle_build_claim
from spacex_model.calc.launch_capacity import LaunchCapacityResult
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class AllocatorInputs:
    """Upstream inputs for a single allocator pass."""

    assumptions: Assumptions
    module_outputs: dict[str, AllocatorOut]
    opex: YearVector
    corp_capex: YearVector
    spectrum_capex: YearVector
    taxes: YearVector
    launch_capacity: LaunchCapacityResult
    prior_year_group_fcf: YearVector | None = None
    lunar_mars_kg_reserved: YearVector | None = None
    f9_launches: YearVector | None = None
    f9_customer_launches: YearVector | None = None
    forward_kg_demands: dict[str, YearVector] | None = None
    starlink_vehicle_irrs: QueueSubBlockIrrs | None = None
    historical_2025: dict[str, float] | None = None
    sigmoid_k: float = 2.0
    solver_cash_boy: YearVector | None = None


def _scale_by_ratio(original: YearVector, scaled_launches: YearVector, base_launches: np.ndarray) -> YearVector:
    """Scale cash demand proportionally when F9 gate caps launch equivalents."""
    out = original.values.copy()
    for t in range(HORIZON_YEARS):
        base = base_launches[t]
        if base > 0:
            out[t] *= scaled_launches.values[t] / base
    return YearVector(out)


def _v2_launch_anchors(assumptions: Assumptions) -> tuple[np.ndarray, np.ndarray]:
    lr = assumption_scalar(assumptions, "Satellite cost per kg — learning rate", default=0.0)
    offsets = np.arange(HORIZON_YEARS, dtype=np.float64)
    learn = np.power(1.0 + lr, offsets)
    bb_anchor = assumption_scalar(assumptions, "V2 Mini BB Sats Launched 2025", default=2987.0)
    dtc_anchor = assumption_scalar(assumptions, "V2 Mini DTC Sats Launched 2025", default=182.0)
    return bb_anchor * learn, dtc_anchor * learn


def _apply_physical_gates(
    demands: QueueSubBlockDemands,
    assumptions: Assumptions,
    *,
    f9_launches: YearVector | None,
    f9_customer_launches: YearVector | None,
) -> QueueSubBlockDemands:
    phase_out = int(
        assumption_scalar(
            assumptions,
            "V2 phase-out year (no V2 BB / V2 DTC launches from this year)",
            default=2028.0,
        )
    )
    v3_startup = int(
        assumption_scalar(assumptions, "V3 Starlink launch trigger year", default=2027.0)
    )

    v2_bb_cash = apply_v2_phase_out_gate(demands.starlink_v2_bb_cash, phase_out_year=phase_out)
    v2_dtc_cash = apply_v2_phase_out_gate(demands.starlink_v2_dtc_cash, phase_out_year=phase_out)
    v3_bb_cash = apply_v3_startup_gate(demands.starlink_v3_bb_cash, startup_year=v3_startup)
    v3_dtc_cash = apply_v3_startup_gate(demands.starlink_v3_dtc_cash, startup_year=v3_startup)
    v3_bb_kg = apply_v3_startup_gate(demands.starlink_v3_bb_kg, startup_year=v3_startup)
    v3_dtc_kg = apply_v3_startup_gate(demands.starlink_v3_dtc_kg, startup_year=v3_startup)

    bb_launches, dtc_launches = _v2_launch_anchors(assumptions)
    if f9_launches is not None and f9_customer_launches is not None:
        f9_internal = YearVector(
            np.maximum(0.0, f9_launches.values - f9_customer_launches.values)
        )
        sats_bb = assumption_scalar(assumptions, "Sats per F9 launch — V2 BB", default=29.0)
        sats_dtc = assumption_scalar(assumptions, "Sats per F9 launch — V2 DTC", default=7.0)
        gated_bb = apply_f9_supply_gate(
            YearVector(bb_launches), f9_internal, sats_per_f9_launch=sats_bb
        )
        gated_dtc = apply_f9_supply_gate(
            YearVector(dtc_launches), f9_internal, sats_per_f9_launch=sats_dtc
        )
        v2_bb_cash = _scale_by_ratio(v2_bb_cash, gated_bb, bb_launches)
        v2_dtc_cash = _scale_by_ratio(v2_dtc_cash, gated_dtc, dtc_launches)

    return replace(
        demands,
        starlink_v2_bb_cash=v2_bb_cash,
        starlink_v2_dtc_cash=v2_dtc_cash,
        starlink_v3_bb_cash=v3_bb_cash,
        starlink_v3_dtc_cash=v3_dtc_cash,
        starlink_v3_bb_kg=v3_bb_kg,
        starlink_v3_dtc_kg=v3_dtc_kg,
    )


def _forward_kg_from_modules(
    module_outputs: dict[str, AllocatorOut],
    lunar_mars_kg: YearVector | None,
) -> dict[str, YearVector]:
    z = YearVector.zeros()
    return {
        "starlink": module_outputs.get("starlink", AllocatorOut.zeros()).capacity_demand_kg,
        "odc": module_outputs.get("odc", AllocatorOut.zeros()).capacity_demand_kg,
        "customer_launch": module_outputs.get(
            "customer_launch", AllocatorOut.zeros()
        ).capacity_demand_kg,
        "lunar_mars": lunar_mars_kg or z,
    }


def compute_allocator(inputs: AllocatorInputs) -> AllocatorResult:
    """Run full Allocator brain: pool → gate → sigmoid cash/kg → first-year override.

    Excel cell:        Allocator!— (Phase D orchestrator)
    Excel label:       "ALLOCATOR BRAIN"
    Architecture ref:  §6 + §20.2 (Sprint 11f Option A)
    Principle:         4 (queue gate before IRR sigmoid allocation)

    """
    a = inputs.assumptions
    cash_boy = inputs.solver_cash_boy if inputs.solver_cash_boy is not None else compute_cash_boy(a, inputs.prior_year_group_fcf)
    mars_carveout = compute_mars_carveout(a, inputs.prior_year_group_fcf)

    raw_demands = compute_exogenous_demands(a)
    demands = _apply_physical_gates(
        raw_demands,
        a,
        f9_launches=inputs.f9_launches,
        f9_customer_launches=inputs.f9_customer_launches,
    )

    forward_kg = inputs.forward_kg_demands or _forward_kg_from_modules(
        inputs.module_outputs,
        inputs.lunar_mars_kg_reserved,
    )
    vehicle_build_claim = compute_vehicle_build_claim(
        a,
        forward_kg,
        inputs.launch_capacity,
    )

    non_module_claims = compute_non_module_claims(
        inputs.opex,
        inputs.corp_capex,
        inputs.spectrum_capex,
        inputs.taxes,
        mars_carveout,
        vehicle_build_claim,
    )
    available_cash = available_cash_for_irr_queue(cash_boy, non_module_claims)

    irrs = roll_up_module_irrs(
        inputs.module_outputs,
        starlink_vehicle_irrs=inputs.starlink_vehicle_irrs,
    )
    sigmoid_k = inputs.sigmoid_k
    if a.lookup("Sigmoid IRR-blend exponent k") is not None:
        sigmoid_k = assumption_scalar(a, "Sigmoid IRR-blend exponent k", default=sigmoid_k)

    cash_alloc = compute_sigmoid_cash_allocations(
        available_cash,
        demands,
        irrs,
        sigmoid_k=sigmoid_k,
    )

    lm_kg = inputs.lunar_mars_kg_reserved or YearVector.zeros()
    capacity_available_kg = YearVector(
        np.maximum(
            0.0,
            inputs.launch_capacity.total_annual_capacity_kg.values - lm_kg.values,
        )
    )
    kg_alloc = compute_sigmoid_kg_allocations(
        capacity_available_kg,
        demands,
        irrs,
        sigmoid_k=sigmoid_k,
    )

    if inputs.historical_2025:
        cash_alloc, kg_alloc = apply_first_year_override(
            cash_alloc,
            kg_alloc,
            inputs.historical_2025,
        )

    cash_alloc = cap_cash_allocations_to_available(cash_alloc, available_cash)

    return AllocatorResult(
        cash=cash_alloc,
        kg=kg_alloc,
        cash_boy=cash_boy,
        available_cash=available_cash,
        mars_carveout=mars_carveout,
        vehicle_build_claim=vehicle_build_claim,
        non_module_claims=non_module_claims,
        capacity_available_kg=capacity_available_kg,
    )
