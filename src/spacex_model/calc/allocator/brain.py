"""CAE allocator brain — pool → gate → carve-out → two-resource fill (U2)."""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.cap_base import CapBaseInputs, compute_cap_base
from spacex_model.calc.allocator.cae_demands import (
    aggregate_cae_demands,
    four_cash_to_sub_blocks,
    four_kg_to_sub_blocks,
    four_program_demands,
)
from spacex_model.calc.allocator.carve_out import compute_carve_out
from spacex_model.calc.allocator.cash_pool import (
    compute_bridge_drawdown,
    compute_cash_boy,
    compute_ipo_drawdown,
)
from spacex_model.calc.allocator.debt_facilities import (
    DebtFacilitiesResult,
    OdcFacilityInputs,
    TerafabFacilityInputs,
    compute_chip_transfer_revenue_mm,
    compute_debt_facilities,
)
from spacex_model.calc.allocator.strategic_seed import (
    StrategicSeedInputs,
    compute_strategic_seed,
)
from spacex_model.calc.allocator.demand_builders import compute_exogenous_demands
from spacex_model.calc.allocator.deployment import apply_first_year_override, cap_cash_allocations_to_available
from spacex_model.calc.allocator.irr_display import compute_four_program_prior_irrs
from spacex_model.calc.allocator.physical_gates import (
    apply_f9_supply_gate,
    apply_v2_phase_out_gate,
    apply_v3_startup_gate,
)
from spacex_model.calc.allocator.queue_gate import compute_non_module_claims, compute_queue_gate
from spacex_model.calc.allocator.types import (
    AllocatorResult,
    CashAllocations,
    KgAllocations,
    QueueSubBlockDemands,
    QueueSubBlockIrrs,
)
from spacex_model.calc.allocator.two_resource_fill import (
    compute_two_resource_fill,
    kg_per_ship_year,
)
from spacex_model.calc.allocator.vehicle_build import compute_vehicle_build_claim
from spacex_model.calc.facilities_build import FacilitiesBuildResult
from spacex_model.calc.launch_capacity import LaunchCapacityResult
from spacex_model.config import canonical_labels as cl
from spacex_model.config.canonical_labels_supplement import (
    SATS_PER_F9_LAUNCH_V2_BB,
    SATS_PER_F9_LAUNCH_V2_DTC,
    V2_PHASE_OUT_YEAR,
)
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class AllocatorInputs:
    """Upstream inputs for a single CAE allocator pass."""

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
    solver_cash_boy: YearVector | None = None
    facilities_build: FacilitiesBuildResult | None = None
    group_fcf: YearVector | None = None
    corp_sga: YearVector | None = None
    shared_rd: YearVector | None = None


def _scale_by_ratio(original: YearVector, scaled_launches: YearVector, base_launches: np.ndarray) -> YearVector:
    out = original.values.copy()
    for t in range(HORIZON_YEARS):
        base = base_launches[t]
        if base > 0:
            out[t] *= scaled_launches.values[t] / base
    return YearVector(out)


def _v2_launch_anchors(assumptions: Assumptions) -> tuple[np.ndarray, np.ndarray]:
    lr = assumption_scalar(assumptions, cl.SATELLITE_COST_PER_KG_LEARNING_RATE, default=0.0)
    offsets = np.arange(HORIZON_YEARS, dtype=np.float64)
    learn = np.power(1.0 + lr, offsets)
    bb_anchor = assumption_scalar(assumptions, cl.V2_MINI_BB_SATS_LAUNCHED_2025, default=2987.0)
    dtc_anchor = assumption_scalar(assumptions, cl.V2_MINI_DTC_SATS_LAUNCHED_2025, default=182.0)
    return bb_anchor * learn, dtc_anchor * learn


def _apply_physical_gates(
    demands: QueueSubBlockDemands,
    assumptions: Assumptions,
    *,
    f9_launches: YearVector | None,
    f9_customer_launches: YearVector | None,
) -> QueueSubBlockDemands:
    phase_out = int(assumption_scalar(assumptions, V2_PHASE_OUT_YEAR, default=2028.0))
    v3_startup = int(assumption_scalar(assumptions, cl.V3_STARLINK_LAUNCH_TRIGGER_YEAR, default=2027.0))

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
        sats_bb = assumption_scalar(assumptions, SATS_PER_F9_LAUNCH_V2_BB, default=29.0)
        sats_dtc = assumption_scalar(assumptions, SATS_PER_F9_LAUNCH_V2_DTC, default=7.0)
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


def _resolve_facilities(
    inputs: AllocatorInputs,
    forward_kg: dict[str, YearVector],
) -> FacilitiesBuildResult | None:
    if inputs.facilities_build is not None:
        return inputs.facilities_build
    return None


def _gigabay_throughput(fb: FacilitiesBuildResult | None) -> YearVector:
    if fb is not None:
        return fb.gigabay_installed_capacity
    return YearVector.zeros()


def _chip_transfer_revenue_estimate(
    assumptions: Assumptions,
    odc_kg: YearVector,
    chip_at_cost_per_sat: YearVector,
) -> YearVector:
    """Estimate at-cost chip transfer from exogenous ODC kg demand (acyclic)."""
    mass = assumption_scalar(assumptions, cl.V3_MASS_KG, default=2000.0)
    chips_per_sat = assumption_scalar(assumptions, cl.CHIPS_PER_SAT, default=0.0)
    if mass <= 0.0 or chips_per_sat <= 0.0:
        return YearVector.zeros()
    sats = odc_kg.values / mass
    chips = sats * chips_per_sat
    return compute_chip_transfer_revenue_mm(YearVector(chips), chip_at_cost_per_sat)


def compute_allocator(inputs: AllocatorInputs) -> AllocatorResult:
    """Run full CAE spine: pool → gate → carve-out → two-resource fill → debt.

    Excel cell:        Cash Allocation Engine (orchestrator)
    Excel label:       "▸ Cash Allocation Engine inputs"
    Architecture ref:  §2.3 CAE map + PRD U2
    Principle:         4 (queue gate before IRR-weighted allocation)

    """
    a = inputs.assumptions
    cash_boy = (
        inputs.solver_cash_boy
        if inputs.solver_cash_boy is not None
        else compute_cash_boy(a, inputs.prior_year_group_fcf)
    )
    bridge = compute_bridge_drawdown(a)
    ipo = compute_ipo_drawdown(a)
    cash_available = YearVector(cash_boy.values + bridge.values + ipo.values)

    raw_demands = compute_exogenous_demands(a)
    demands = _apply_physical_gates(
        raw_demands,
        a,
        f9_launches=inputs.f9_launches,
        f9_customer_launches=inputs.f9_customer_launches,
    )
    cae_dem = aggregate_cae_demands(a, demands, inputs.module_outputs)
    fb_early = _resolve_facilities(inputs, {})
    cap_base = compute_cap_base(
        CapBaseInputs(
            assumptions=a,
            sub_demands=demands,
            module_outputs=inputs.module_outputs,
            facilities_build=fb_early,
        )
    )

    forward_kg = inputs.forward_kg_demands or cae_dem.unified_kg.forward_kg_by_program(
        inputs.lunar_mars_kg_reserved,
    )
    vehicle_build_claim = compute_vehicle_build_claim(
        a,
        forward_kg,
        inputs.launch_capacity,
    )

    corp_sga = inputs.corp_sga if inputs.corp_sga is not None else inputs.opex
    shared_rd = inputs.shared_rd if inputs.shared_rd is not None else YearVector.zeros()

    gate = compute_queue_gate(
        cash_available,
        corp_sga=corp_sga,
        shared_rd=shared_rd,
        corp_capex=inputs.corp_capex,
        spectrum_capex=inputs.spectrum_capex,
        taxes=inputs.taxes,
        vehicle_build_claim=vehicle_build_claim,
        maintenance_capex=cap_base.maintenance_claim,
        enabling_infra_equity=cap_base.enabling_infra_equity,
    )
    carve = compute_carve_out(a, gate.pool_after_gate, inputs.prior_year_group_fcf)

    fb = _resolve_facilities(inputs, forward_kg)
    prior_irr = compute_four_program_prior_irrs(
        inputs.module_outputs,
        a,
        facilities_build=fb,
        chip_at_cost_per_sat=cap_base.chip_at_cost_per_sat,
    )
    seed = compute_strategic_seed(
        StrategicSeedInputs(
            assumptions=a,
            odc_demand_buildable=cap_base.odc_demand_buildable,
            odc_kg_demand=demands.odc_kg,
            prior_odc_irr=prior_irr.odc,
            pool_after_carveout=carve.remaining_pool,
        )
    )
    four_dem = four_program_demands(
        cap_base.growth_caps,
        cap_base.odc_demand_buildable,
        cap_base.terr_demand_buildable,
        cae_dem.unified_kg,
        demands,
    )
    lm_kg = inputs.lunar_mars_kg_reserved or YearVector.zeros()
    kg_reserved = YearVector(lm_kg.values + seed.kg_reserved.values)
    fill = compute_two_resource_fill(
        seed.remaining_pool,
        four_dem,
        prior_irr,
        a,
        gigabay_throughput=_gigabay_throughput(fb),
        kg_per_ship_yr=kg_per_ship_year(a, inputs.launch_capacity.per_launch_upmass_kg),
        lm_kg_reserved=kg_reserved,
        total_desired_launch_kg=cae_dem.unified_kg.total,
    )

    (
        cl_cash,
        sl_v2_bb,
        sl_v2_dtc,
        sl_v3_bb,
        sl_v3_dtc,
        odc_cash,
        ai_stack_cash,
    ) = four_cash_to_sub_blocks(fill.allocated_cash, demands)
    odc_total_cash = YearVector(fill.allocated_cash.odc.values + seed.cash_claim.values)
    cash_alloc = CashAllocations(
        customer_launch=cl_cash,
        starlink_v2_bb=sl_v2_bb,
        starlink_v2_dtc=sl_v2_dtc,
        starlink_v3_bb=sl_v3_bb,
        starlink_v3_dtc=sl_v3_dtc,
        odc=odc_total_cash,
        ai_stack=ai_stack_cash,
    )

    cl_kg, sl_v3_bb_kg, sl_v3_dtc_kg, odc_kg, ai_stack_kg = four_kg_to_sub_blocks(
        fill.allocated_kg,
        demands,
    )
    odc_total_kg = YearVector(odc_kg.values + seed.kg_reserved.values)
    kg_alloc = KgAllocations(
        customer_launch=cl_kg,
        starlink_v3_bb=sl_v3_bb_kg,
        starlink_v3_dtc=sl_v3_dtc_kg,
        odc=odc_total_kg,
        ai_stack=ai_stack_kg,
    )

    if inputs.historical_2025:
        cash_alloc, kg_alloc = apply_first_year_override(
            cash_alloc,
            kg_alloc,
            inputs.historical_2025,
        )

    available_cash = seed.remaining_pool
    cash_alloc = cap_cash_allocations_to_available(cash_alloc, available_cash)

    non_module_claims = compute_non_module_claims(
        inputs.opex,
        inputs.corp_capex,
        inputs.spectrum_capex,
        inputs.taxes,
        carve.lunar_mars_carveout,
        vehicle_build_claim,
    )

    group_fcf_for_debt = inputs.group_fcf or inputs.prior_year_group_fcf or YearVector.zeros()
    cash_eoy = YearVector(cash_boy.values + group_fcf_for_debt.values)

    debt: DebtFacilitiesResult | None = None
    if fb is not None:
        group_fcf = group_fcf_for_debt
        chip_transfer = _chip_transfer_revenue_estimate(
            a, demands.odc_kg, cap_base.chip_at_cost_per_sat
        )
        debt = compute_debt_facilities(
            TerafabFacilityInputs(
                assumptions=a,
                terafab_capex_to_fund=fb.chip_fab_capex,
                cash_eoy=cash_eoy,
                ipo_injection=ipo,
                group_fcf=group_fcf,
                chip_transfer_revenue=chip_transfer,
            ),
            OdcFacilityInputs(
                assumptions=a,
                odc_capex_need=cap_base.odc_demand_buildable,
                odc_pool_allocation=odc_total_cash,
                ai_compute_module_fcf=inputs.module_outputs.get(
                    "ai_compute", AllocatorOut.zeros()
                ).module_fcf,
            ),
        )

    ai_compute_cash = YearVector(
        odc_total_cash.values + fill.allocated_cash.terrestrial.values
    )

    return AllocatorResult(
        cash=cash_alloc,
        kg=kg_alloc,
        cash_boy=cash_boy,
        available_cash=available_cash,
        mars_carveout=carve.lunar_mars_carveout,
        vehicle_build_claim=vehicle_build_claim,
        non_module_claims=non_module_claims,
        capacity_available_kg=YearVector(
            _gigabay_throughput(fb).values
            * kg_per_ship_year(a, inputs.launch_capacity.per_launch_upmass_kg).values
            - kg_reserved.values
        ),
        pool_after_gate=gate.pool_after_gate,
        remaining_pool=seed.remaining_pool,
        allocated_final_starlink=fill.allocated_cash.starlink,
        allocated_final_customer_launch=fill.allocated_cash.customer_launch,
        allocated_final_ai_compute=ai_compute_cash,
        allocated_final_odc=odc_total_cash,
        strategic_seed_cash=seed.cash_claim,
        strategic_seed_kg=seed.kg_reserved,
        odc_graduated=seed.graduated,
        odc_total_cash=odc_total_cash,
        allocated_final_terrestrial=fill.allocated_cash.terrestrial,
        kg_binding_flag=fill.kg_binding_flag,
        total_desired_launch_kg=cae_dem.unified_kg.total,
        memo_total_kg_demand=cae_dem.unified_kg.total,
        growth_cap_starlink=cap_base.growth_caps.starlink,
        growth_cap_customer_launch=cap_base.growth_caps.customer_launch,
        growth_cap_ai_compute=cap_base.growth_caps.ai_compute,
        maintenance_claim=cap_base.maintenance_claim,
        enabling_infra_equity=cap_base.enabling_infra_equity,
        chip_at_cost_per_sat=cap_base.chip_at_cost_per_sat,
        water_fill_residual=fill.cash_residual,
        capped_share_starlink=fill.capped_shares.starlink,
        capped_share_odc=fill.capped_shares.odc,
        capped_share_terrestrial=fill.capped_shares.terrestrial,
        capped_share_customer_launch=fill.capped_shares.customer_launch,
        ship_slots_used=fill.ship_slots_used,
        ship_slots_idle=fill.ship_slots_idle,
        debt_odc_draw=debt.odc.draw if debt else None,
        debt_terafab_draw=debt.terafab.draw if debt else None,
        odc_pool_cash=fill.allocated_cash.odc,
        cash_available_for_year=cash_available,
        cash_eoy=cash_eoy,
        debt=debt,
    )
