"""Starlink module orchestrator — vending-machine P&L (Phase C).

Architecture §8 / PRD §4.3.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc._vending_machine import build_allocator_out
from spacex_model.calc.launch_capacity import LaunchCapacityResult
from spacex_model.calc.starlink.revenue_curve import compute_bb_revenue, compute_dtc_revenue
from spacex_model.calc.starlink.vehicle_pools import VehiclePoolsResult, compute_vehicle_pools
from spacex_model.calc.starlink_capacity import (
    OdcBandwidthClaim,
    StarlinkCapacityInputs,
    StarlinkCapacityResult,
    compute_starlink_capacity,
)
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions
from spacex_model.inputs.demand_curves import DemandCurves


@dataclass(frozen=True, slots=True)
class StarlinkInputs:
    """Upstream inputs for Starlink module + Starlink Capacity."""

    assumptions: Assumptions
    demand_curves: DemandCurves
    launch_capacity: LaunchCapacityResult | None = None
    odc_bandwidth_claim: OdcBandwidthClaim | None = None
    spectrum_amort_mm: YearVector | None = None
    vehicle_pools: VehiclePoolsResult | None = None


def _pools(inputs: StarlinkInputs) -> VehiclePoolsResult:
    if inputs.vehicle_pools is not None:
        return inputs.vehicle_pools
    return compute_vehicle_pools(inputs.assumptions)


def _dep_per_kg_year_for_life(assumptions: Assumptions, useful_life_years: float) -> np.ndarray:
    """$/kg/yr depreciation scaled from BB 5yr anchor — P1-2 DTC 3yr / BB 5yr split."""
    bb_life = assumption_scalar(
        assumptions, "Satellite useful life — V2 Mini (years)", default=5.0
    )
    base = assumption_scalar(assumptions, "Satellite Dep per kg — base year ($/kg/yr)", default=128.8)
    decay = assumption_scalar(assumptions, "Satellite Dep per kg — annual decay rate", default=0.01)
    scale = bb_life / max(useful_life_years, 1.0)
    offsets = np.arange(HORIZON_YEARS, dtype=np.float64)
    return base * scale * np.power(1.0 - decay, offsets)


def _pool_fleet_mass_kg(
    active_fleet: np.ndarray,
    mass_kg: float,
) -> np.ndarray:
    return active_fleet * mass_kg


def _active_mass_kg(pools: VehiclePoolsResult, assumptions: Assumptions) -> np.ndarray:
    v2_mass = assumption_scalar(assumptions, "V2 Mini Mass (kg)", default=575.0)
    v3_mass = assumption_scalar(assumptions, "V3 Mass (kg)", default=2000.0)
    fleet_mass = (
        pools.v2_bb.active_fleet.values * v2_mass
        + pools.v2_dtc.active_fleet.values * v2_mass
        + pools.v3_bb.active_fleet.values * v3_mass
        + pools.v3_dtc.active_fleet.values * v3_mass
    )
    legacy_life = assumption_scalar(assumptions, "Legacy V1/V1.5 D&A useful life (yrs)", default=4.0)
    legacy_bw_2025 = assumption_scalar(
        assumptions, "Legacy V1/V1.5 Bandwidth — end-2025 (Gbps)", default=71888.0
    )
    legacy_mass_equiv = legacy_bw_2025 / 96.0 * v2_mass if legacy_bw_2025 > 0 else 0.0
    legacy_mass = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        if t < legacy_life:
            legacy_mass[t] = legacy_mass_equiv * max(0.0, 1.0 - t / legacy_life)
    return fleet_mass + legacy_mass


def compute_constellation_da(inputs: StarlinkInputs) -> YearVector:
    """Constellation D&A = active mass × $/kg/yr + legacy V1/V1.5 D&A runoff.

    Excel cell:        Starlink!D153
    Excel label:       "Constellation D&A ($mm)"
    Architecture ref:  §8 Starlink COGS
    Principle:         8 (vending-machine module)

    """
    pools = _pools(inputs)
    a = inputs.assumptions
    v2_mass = assumption_scalar(a, "V2 Mini Mass (kg)", default=575.0)
    v3_mass = assumption_scalar(a, "V3 Mass (kg)", default=2000.0)
    bb_life_v2 = assumption_scalar(a, "Satellite useful life — V2 Mini (years)", default=5.0)
    bb_life_v3 = assumption_scalar(a, "Satellite useful life — V3 (years)", default=5.0)
    dtc_life_v2 = assumption_scalar(
        a, "Satellite useful life — V2 Mini DTC (years)", default=3.0
    )
    dtc_life_v3 = assumption_scalar(a, "Satellite useful life — V3 DTC (years)", default=3.0)

    dep_v2_bb = _dep_per_kg_year_for_life(a, bb_life_v2)
    dep_v2_dtc = _dep_per_kg_year_for_life(a, dtc_life_v2)
    dep_v3_bb = _dep_per_kg_year_for_life(a, bb_life_v3)
    dep_v3_dtc = _dep_per_kg_year_for_life(a, dtc_life_v3)

    v2_v3_da = (
        _pool_fleet_mass_kg(pools.v2_bb.active_fleet.values, v2_mass) * dep_v2_bb
        + _pool_fleet_mass_kg(pools.v2_dtc.active_fleet.values, v2_mass) * dep_v2_dtc
        + _pool_fleet_mass_kg(pools.v3_bb.active_fleet.values, v3_mass) * dep_v3_bb
        + _pool_fleet_mass_kg(pools.v3_dtc.active_fleet.values, v3_mass) * dep_v3_dtc
    ) / 1e6

    legacy_da_anchor = assumption_scalar(
        inputs.assumptions, "Legacy V1/V1.5 D&A baseline ($mm, 2025 anchor)", default=130.0
    )
    legacy_life = int(
        assumption_scalar(inputs.assumptions, "Legacy V1/V1.5 D&A useful life (yrs)", default=4.0)
    )
    legacy_da = np.zeros(HORIZON_YEARS, dtype=np.float64)
    annual_legacy = legacy_da_anchor / legacy_life if legacy_life > 0 else 0.0
    for t in range(min(legacy_life, HORIZON_YEARS)):
        legacy_da[t] = annual_legacy

    return YearVector(v2_v3_da + legacy_da)


def compute_starlink_capacity_result(inputs: StarlinkInputs) -> StarlinkCapacityResult:
    """Run Starlink Capacity sub-tab from module intermediates.

    Excel cell:        Starlink Capacity!— 
    Excel label:       "BB Gbps available for external Starlink revenue"
    Architecture ref:  §8.5
    Principle:         3 (supply-side bandwidth aggregation)

    """
    pools = _pools(inputs)
    capacity_pre = _capacity_from_pools(pools, inputs)
    bb_rev = compute_bb_revenue(
        capacity_pre.available_bb_gbps,
        assumptions=inputs.assumptions,
        demand_curves=inputs.demand_curves,
    )
    dtc_rev = compute_dtc_revenue(
        capacity_pre.available_dtc_gbps,
        assumptions=inputs.assumptions,
        demand_curves=inputs.demand_curves,
    )
    starshield = compute_starshield_revenue(inputs)
    subtotal = bb_rev.values + dtc_rev.values + starshield.values
    ground_ops_pct = assumption_scalar(inputs.assumptions, "Starlink ground ops % of revenue", default=0.04)
    ground_ops = YearVector(subtotal * ground_ops_pct)
    spectrum = inputs.spectrum_amort_mm or YearVector.zeros()
    return compute_starlink_capacity(
        StarlinkCapacityInputs(
            pools=pools,
            constellation_da_mm=compute_constellation_da(inputs),
            ground_ops_mm=ground_ops,
            spectrum_amort_mm=spectrum,
            odc_claim=inputs.odc_bandwidth_claim,
        )
    )


def _capacity_from_pools(
    pools: VehiclePoolsResult,
    inputs: StarlinkInputs,
) -> StarlinkCapacityResult:
    """Initial capacity pass before revenue-dependent ground ops."""
    odc_bb = (
        inputs.odc_bandwidth_claim.bb_gbps.values
        if inputs.odc_bandwidth_claim
        else np.zeros(HORIZON_YEARS)
    )
    odc_dtc = (
        inputs.odc_bandwidth_claim.dtc_gbps.values
        if inputs.odc_bandwidth_claim
        else np.zeros(HORIZON_YEARS)
    )
    total_bb = pools.total_bb_gbps.values
    total_dtc = pools.total_dtc_gbps.values
    return StarlinkCapacityResult(
        total_bb_gbps=pools.total_bb_gbps,
        total_dtc_gbps=pools.total_dtc_gbps,
        available_bb_gbps=YearVector(np.maximum(0.0, total_bb - odc_bb)),
        available_dtc_gbps=YearVector(np.maximum(0.0, total_dtc - odc_dtc)),
        bb_pool_cost_basis_mm=YearVector.zeros(),
        dtc_pool_cost_basis_mm=YearVector.zeros(),
        bb_at_cost_rate_per_gbps=YearVector.zeros(),
        dtc_at_cost_rate_per_gbps=YearVector.zeros(),
    )


def _starshield_reserved_pct(assumptions: Assumptions) -> np.ndarray:
    start = assumption_scalar(assumptions, "Starshield Reserved % — start", default=0.0257)
    floor = assumption_scalar(assumptions, "Starshield Reserved % — floor", default=0.0001)
    decay = assumption_scalar(assumptions, "Starshield Reserved % — decay rate", default=0.25)
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        values[t] = max(floor, start * np.power(1.0 - decay, t))
    return values


def _starshield_rev_per_gbps(assumptions: Assumptions) -> np.ndarray:
    base = assumption_scalar(assumptions, "Starshield Rev per Gbps — base year ($/Gbps)", default=164699.0)
    decay = assumption_scalar(assumptions, "Starshield Rev per Gbps — decay rate", default=0.05)
    offsets = np.arange(HORIZON_YEARS, dtype=np.float64)
    return base * np.power(1.0 - decay, offsets)


def compute_starshield_revenue(inputs: StarlinkInputs) -> YearVector:
    """Starshield revenue = reserved Gbps × $/Gbps/yr.

    Excel cell:        Starlink!D110
    Excel label:       "Starshield revenue ($mm)"
    Architecture ref:  §8 Starshield
    Principle:         8 (vending-machine module)

    """
    pools = _pools(inputs)
    reserved_pct = _starshield_reserved_pct(inputs.assumptions)
    rev_per_gbps = _starshield_rev_per_gbps(inputs.assumptions)
    reserved_gbps = pools.total_bb_gbps.values * reserved_pct
    revenue_mm = reserved_gbps * rev_per_gbps / 1e6
    scope = assumption_scalar(
        inputs.assumptions,
        cl.STARSHIELD_S1_GOV_CONNECTIVITY_SCOPE_FACTOR,
        default=1.0,
    )
    return YearVector(revenue_mm * scope)


def compute_hardware_revenue(inputs: StarlinkInputs) -> YearVector:
    """Terminal hardware revenue from net subscriber adds × blended retail price.

    Excel cell:        Starlink!D135
    Excel label:       "Terminal hardware revenue ($mm)"
    Architecture ref:  §8.4
    Principle:         8 (derived subs from revenue / ARPU)

    """
    capacity = compute_starlink_capacity_result(inputs)
    bb_rev = compute_bb_revenue(
        capacity.available_bb_gbps,
        assumptions=inputs.assumptions,
        demand_curves=inputs.demand_curves,
    )
    dtc_rev = compute_dtc_revenue(
        capacity.available_dtc_gbps,
        assumptions=inputs.assumptions,
        demand_curves=inputs.demand_curves,
    )
    from spacex_model.inputs.s1_profiles import broadband_arpu_sub_mo

    bb_arpu = assumption_year_vector(
        inputs.assumptions,
        "Broadband ARPU ($/sub/mo, year-row)",
        default=float(broadband_arpu_sub_mo()[0]),
    )
    if bb_arpu.at(FIRST_YEAR) >= 99.0:
        bb_arpu = YearVector(broadband_arpu_sub_mo())
    dtc_arpu = assumption_year_vector(inputs.assumptions, "DTC ARPU ($/sub/mo, year-row)", default=16.0)

    bb_subs = np.where(bb_arpu.values > 0, bb_rev.values / (bb_arpu.values * 12.0), 0.0)
    dtc_subs = np.where(dtc_arpu.values > 0, dtc_rev.values / (dtc_arpu.values * 12.0), 0.0)
    total_subs = bb_subs + dtc_subs

    boy_subs = assumption_scalar(
        inputs.assumptions, "Starting BoY 2025 subscribers (millions)", default=5.0
    )
    subsidy_mix = assumption_scalar(
        inputs.assumptions, "Subsidy mix (% of net adds subsidized)", default=0.5
    )
    price_sub = assumption_scalar(inputs.assumptions, "Terminal retail price ($, subsidized)", default=300.0)
    price_full = assumption_scalar(
        inputs.assumptions, "Terminal retail price ($, non-subsidized)", default=500.0
    )
    blended_price = subsidy_mix * price_sub + (1.0 - subsidy_mix) * price_full

    net_adds = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        if t == 0:
            net_adds[t] = max(0.0, total_subs[t] - boy_subs)
        else:
            net_adds[t] = max(0.0, total_subs[t] - total_subs[t - 1])
    return YearVector(net_adds * blended_price)


def compute_internal_bandwidth_revenue(inputs: StarlinkInputs) -> YearVector:
    """Internal bandwidth transfer revenue from ODC Gbps claim × pool rates.

    Excel cell:        Starlink!D143
    Excel label:       "Starlink internal bandwidth revenue ($mm)"
    Architecture ref:  §7.2
    Principle:         9 (at-cost internal transfer)

    """
    if inputs.odc_bandwidth_claim is None:
        return YearVector.zeros()
    capacity = compute_starlink_capacity_result(inputs)
    claim = inputs.odc_bandwidth_claim
    values = (
        claim.bb_gbps.values * capacity.bb_at_cost_rate_per_gbps.values / 1e6
        + claim.dtc_gbps.values * capacity.dtc_at_cost_rate_per_gbps.values / 1e6
    )
    return YearVector(values)


def compute_revenue(inputs: StarlinkInputs | None = None) -> YearVector:
    """BB + DTC + Starshield + hardware + internal bandwidth revenue.

    Excel cell:        Starlink!D178
    Excel label:       "Total Revenue ($mm)"
    Architecture ref:  §8 Starlink revenue
    Principle:         8 (vending-machine module)

    """
    if inputs is None:
        return YearVector.zeros()

    capacity = compute_starlink_capacity_result(inputs)
    bb = compute_bb_revenue(
        capacity.available_bb_gbps,
        assumptions=inputs.assumptions,
        demand_curves=inputs.demand_curves,
    )
    dtc = compute_dtc_revenue(
        capacity.available_dtc_gbps,
        assumptions=inputs.assumptions,
        demand_curves=inputs.demand_curves,
    )
    starshield = compute_starshield_revenue(inputs)
    hardware = compute_hardware_revenue(inputs)
    internal_bw = compute_internal_bandwidth_revenue(inputs)
    total = bb.values + dtc.values + starshield.values + hardware.values + internal_bw.values
    return YearVector(total)


def compute_launch_services_cost(inputs: StarlinkInputs) -> YearVector:
    """Internal launch services at fully-allocated F9/Starship rates.

    Excel cell:        Starlink!D156
    Excel label:       "Launch services cost ($mm)"
    Architecture ref:  §8 Starlink COGS / §7.1
    Principle:         9 (internal transfers at fully-allocated cost)

    """
    if inputs.launch_capacity is None:
        return YearVector.zeros()
    pools = _pools(inputs)
    lc = inputs.launch_capacity
    f9_launches = pools.f9_v2_bb_launches.values + pools.f9_v2_dtc_launches.values
    ship_launches = pools.starship_v3_bb_launches.values + pools.starship_v3_dtc_launches.values
    cost = f9_launches * lc.f9_at_cost_rate.values + ship_launches * lc.starship_at_cost_rate.values
    return YearVector(cost)


def compute_cogs(inputs: StarlinkInputs | None = None) -> YearVector:
    """Constellation D&A, launch services, ground ops, spectrum, terminals.

    Excel cell:        Starlink!D170
    Excel label:       "Total COGS ($mm)"
    Architecture ref:  §8 Starlink COGS
    Principle:         9 (internal launch at fully-allocated rate)

    """
    if inputs is None:
        return YearVector.zeros()

    revenue = compute_revenue(inputs)
    constellation_da = compute_constellation_da(inputs)
    launch_cost = compute_launch_services_cost(inputs)
    ground_ops_pct = assumption_scalar(inputs.assumptions, "Starlink ground ops % of revenue", default=0.04)
    insurance_pct = assumption_scalar(inputs.assumptions, "Starlink insurance % of revenue", default=0.01)
    other_pct = assumption_scalar(inputs.assumptions, "Starlink other COGS % of revenue", default=0.02)
    spectrum = inputs.spectrum_amort_mm or YearVector.zeros()

    hardware = compute_hardware_revenue(inputs)
    terminal_cogs_per = assumption_scalar(inputs.assumptions, "Terminal COGS per unit ($)", default=500.0)
    subsidy_mix = assumption_scalar(
        inputs.assumptions, "Subsidy mix (% of net adds subsidized)", default=0.5
    )
    price_sub = assumption_scalar(inputs.assumptions, "Terminal retail price ($, subsidized)", default=300.0)
    price_full = assumption_scalar(
        inputs.assumptions, "Terminal retail price ($, non-subsidized)", default=500.0
    )
    blended_retail = subsidy_mix * price_sub + (1.0 - subsidy_mix) * price_full
    terminal_cogs = YearVector(hardware.values * (terminal_cogs_per / max(blended_retail, 1.0)))

    total = (
        constellation_da.values
        + launch_cost.values
        + revenue.values * ground_ops_pct
        + spectrum.values
        + terminal_cogs.values
        + revenue.values * (insurance_pct + other_pct)
    )
    return YearVector(total)


def compute_gross_profit(inputs: StarlinkInputs | None = None) -> YearVector:
    """Gross profit = revenue − COGS.

    Excel cell:        Starlink!D181
    Excel label:       "Gross Profit ($mm)"
    Architecture ref:  §3 module framing
    Principle:         7 (Module EBITDA = Gross Profit)

    """
    if inputs is None:
        return YearVector.zeros()
    return YearVector(compute_revenue(inputs).values - compute_cogs(inputs).values)


def compute_capex(inputs: StarlinkInputs | None = None) -> YearVector:
    """Sat manufacturing CapEx from launches × unit cost (no facility lag in Phase C).

    Excel cell:        Starlink!D98
    Excel label:       "Module CapEx ($mm)"
    Architecture ref:  §8 Starlink CapEx
    Principle:         8 (vehicle build via queue gate for Starship kg)

    """
    if inputs is None:
        return YearVector.zeros()

    pools = _pools(inputs)
    a = inputs.assumptions
    v2_cost_kg = assumption_scalar(a, "V2 Mini cost per kg — base year ($/kg)", default=650.0)
    v2_mass = assumption_scalar(a, "V2 Mini Mass (kg)", default=575.0)
    v3_mass = assumption_scalar(a, "V3 Mass (kg)", default=2000.0)
    v2_unit = v2_cost_kg * v2_mass / 1e6
    v3_unit = v2_cost_kg * v3_mass / 1e6

    capex = (
        pools.v2_bb.launches.values * v2_unit
        + pools.v2_dtc.launches.values * v2_unit
        + pools.v3_bb.launches.values * v3_unit
        + pools.v3_dtc.launches.values * v3_unit
    )
    return YearVector(capex)


def compute_fcf(inputs: StarlinkInputs | None = None) -> YearVector:
    """Module FCF = EBITDA + constellation D&A add-back − CapEx.

    Excel cell:        Starlink!D188
    Excel label:       "Module FCF ($mm)"
    Architecture ref:  §3 module FCF
    Principle:         8 (pre-tax module FCF)

    """
    if inputs is None:
        return YearVector.zeros()
    ebitda = compute_gross_profit(inputs)
    capex = compute_capex(inputs)
    da = compute_constellation_da(inputs)
    return YearVector(ebitda.values + da.values - capex.values)


def compute_allocator_out(inputs: StarlinkInputs | None = None) -> AllocatorOut:
    """Assemble Allocator OUT from vending-machine sections.

    Excel cell:        Starlink!D201:AC210
    Excel label:       "CENTRAL ALLOCATOR OUTPUTS"
    Architecture ref:  §8 Allocator OUT contract
    Principle:         3 (canonical cross-tab labels via registry)

    """
    if inputs is None:
        z = YearVector.zeros()
        return build_allocator_out(revenue=z, cogs=z, capex=z)

    revenue = compute_revenue(inputs)
    cogs = compute_cogs(inputs)
    capex = compute_capex(inputs)
    da = compute_constellation_da(inputs)
    pools = _pools(inputs)
    kg_demand = YearVector(
        pools.v3_bb_kg_demand.values + pools.v3_dtc_kg_demand.values
    )
    return build_allocator_out(
        revenue=revenue,
        cogs=cogs,
        capex=capex,
        capacity_demand_kg=kg_demand,
        module_da_addback=da,
    )
