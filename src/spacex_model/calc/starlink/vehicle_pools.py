"""V2/V3 vehicle pool fleet tracking and launch outputs (Architecture §8.1)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_allocation import AllocatorAllocation
from spacex_model.calc._vehicle_allocations import VehicleAllocations
from spacex_model.calc.starlink.deorbit import historical_opening_balance_deorbit, launch_cohort_deorbit
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class VehiclePoolSpec:
    """Static per-vehicle physical and cost parameters."""

    name: str
    mass_kg: float
    bb_gbps_per_sat: float
    dtc_gbps_per_sat: float
    unit_cost_mm: float
    sats_per_f9_launch: float
    sats_per_starship_launch: float
    useful_life_years: int
    historical_baseline: float
    launch_anchor_2025: float | None = None


@dataclass(frozen=True, slots=True)
class VehiclePoolState:
    """Single vehicle pool year-vectors."""

    launches: YearVector
    active_fleet: YearVector
    bb_gbps: YearVector
    dtc_gbps: YearVector
    f9_launches: YearVector
    starship_launches: YearVector
    starship_kg_demand: YearVector


@dataclass(frozen=True, slots=True)
class VehiclePoolsResult:
    """Aggregated four-pool constellation state."""

    v2_bb: VehiclePoolState
    v2_dtc: VehiclePoolState
    v3_bb: VehiclePoolState
    v3_dtc: VehiclePoolState
    total_active_sats: YearVector
    total_bb_gbps: YearVector
    total_dtc_gbps: YearVector
    legacy_bb_gbps: YearVector
    f9_v2_bb_launches: YearVector
    f9_v2_dtc_launches: YearVector
    starship_v3_bb_launches: YearVector
    starship_v3_dtc_launches: YearVector
    v3_bb_kg_demand: YearVector
    v3_dtc_kg_demand: YearVector


def _pool_spec_v2_bb(assumptions: Assumptions) -> VehiclePoolSpec:
    a = assumptions
    cost_kg = assumption_scalar(a, "V2 Mini cost per kg — base year ($/kg)", default=650.0)
    mass = assumption_scalar(a, "V2 Mini Mass (kg)", default=575.0)
    return VehiclePoolSpec(
        name="V2 BB",
        mass_kg=mass,
        bb_gbps_per_sat=assumption_scalar(a, "V2 Mini Bandwidth per Sat — BB (Gbps)", default=96.0),
        dtc_gbps_per_sat=0.0,
        unit_cost_mm=cost_kg * mass / 1e6,
        sats_per_f9_launch=assumption_scalar(a, "Sats per F9 launch — V2 BB", default=29.0),
        sats_per_starship_launch=0.0,
        useful_life_years=int(assumption_scalar(a, "Satellite useful life — V2 Mini (years)", default=5.0)),
        historical_baseline=assumption_scalar(a, "V2 Mini BB historical baseline (SoY 2025)", default=5246.0),
        launch_anchor_2025=assumption_scalar(a, "V2 Mini BB Sats Launched 2025", default=2987.0),
    )


def _pool_spec_v2_dtc(assumptions: Assumptions) -> VehiclePoolSpec:
    a = assumptions
    cost_kg = assumption_scalar(a, "V2 Mini cost per kg — base year ($/kg)", default=650.0)
    mass = assumption_scalar(a, "V2 Mini Mass (kg)", default=575.0)
    return VehiclePoolSpec(
        name="V2 DTC",
        mass_kg=mass,
        bb_gbps_per_sat=0.0,
        dtc_gbps_per_sat=assumption_scalar(a, "V2 Mini Bandwidth per Sat — DTC (Gbps)", default=0.2),
        unit_cost_mm=cost_kg * mass / 1e6,
        sats_per_f9_launch=assumption_scalar(a, "Sats per F9 launch — V2 DTC", default=7.0),
        sats_per_starship_launch=0.0,
        useful_life_years=int(
            assumption_scalar(a, cl.SATELLITE_USEFUL_LIFE_V2_DTC_YEARS, default=3.0)
        ),
        historical_baseline=assumption_scalar(a, "V2 Mini DTC historical baseline (SoY 2025)", default=650.0),
        launch_anchor_2025=assumption_scalar(a, "V2 Mini DTC Sats Launched 2025", default=182.0),
    )


def _pool_spec_v3_bb(assumptions: Assumptions) -> VehiclePoolSpec:
    a = assumptions
    cost_kg = assumption_scalar(a, "V2 Mini cost per kg — base year ($/kg)", default=650.0)
    mass = assumption_scalar(a, "V3 Mass (kg)", default=2000.0)
    return VehiclePoolSpec(
        name="V3 BB",
        mass_kg=mass,
        bb_gbps_per_sat=assumption_scalar(a, "V3 BB Bandwidth per Sat — base year (Gbps)", default=1000.0),
        dtc_gbps_per_sat=0.0,
        unit_cost_mm=cost_kg * mass / 1e6,
        sats_per_f9_launch=0.0,
        sats_per_starship_launch=assumption_scalar(a, "Sats per Starship launch — V3 BB", default=60.0),
        useful_life_years=int(assumption_scalar(a, "Satellite useful life — V3 (years)", default=5.0)),
        historical_baseline=0.0,
        launch_anchor_2025=assumption_scalar(a, "V3 BB Sats Launched 2025", default=0.0),
    )


def _pool_spec_v3_dtc(assumptions: Assumptions) -> VehiclePoolSpec:
    a = assumptions
    cost_kg = assumption_scalar(a, "V2 Mini cost per kg — base year ($/kg)", default=650.0)
    mass = assumption_scalar(a, "V3 Mass (kg)", default=2000.0)
    return VehiclePoolSpec(
        name="V3 DTC",
        mass_kg=mass,
        bb_gbps_per_sat=0.0,
        dtc_gbps_per_sat=assumption_scalar(a, "V3 DTC Bandwidth per Sat (Gbps)", default=2.75),
        unit_cost_mm=cost_kg * mass / 1e6,
        sats_per_f9_launch=0.0,
        sats_per_starship_launch=assumption_scalar(a, "Sats per Starship launch — V3 DTC", default=15.0),
        useful_life_years=int(
            assumption_scalar(a, cl.SATELLITE_USEFUL_LIFE_V3_DTC_YEARS, default=3.0)
        ),
        historical_baseline=0.0,
        launch_anchor_2025=assumption_scalar(a, "V3 DTC Sats Launched 2025", default=0.0),
    )


def _launches_for_pool(
    spec: VehiclePoolSpec,
    assumptions: Assumptions,
    *,
    is_v2: bool,
    is_dtc: bool,
    ratchet_active: np.ndarray,
    v3_startup_year: int | None,
    allocation: AllocatorAllocation | None,
) -> np.ndarray:
    """Exogenous demand + bounded output; 2025 first-year anchors per §2.16."""
    launches = np.zeros(HORIZON_YEARS, dtype=np.float64)
    phase_out = int(
        assumption_scalar(
            assumptions,
            "V2 phase-out year (no V2 BB / V2 DTC launches from this year)",
            default=2028.0,
        )
        if is_v2
        else 9999
    )
    v2_dtc_cap = is_v2 and is_dtc

    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        if year == FIRST_YEAR and spec.launch_anchor_2025 is not None:
            launches[t] = spec.launch_anchor_2025
            continue
        if is_v2 and year >= phase_out:
            launches[t] = 0.0
            continue
        if v2_dtc_cap and year > FIRST_YEAR:
            launches[t] = 0.0
            continue
        if not is_v2 and v3_startup_year is not None and year < v3_startup_year:
            launches[t] = 0.0
            continue
        if is_v2 and ratchet_active[t] > 0:
            launches[t] = 0.0
            continue
        if allocation is not None and spec.unit_cost_mm > 0:
            cash_units = allocation.cash_mm.values[t] / spec.unit_cost_mm
            kg_units = (
                allocation.kg_to_leo.values[t] / spec.mass_kg if spec.mass_kg > 0 else 0.0
            )
            launches[t] = max(0.0, min(cash_units, kg_units))
    return launches


def _active_fleet(
    spec: VehiclePoolSpec,
    launches: np.ndarray,
    *,
    include_historical: bool,
    end_2025_anchor: float | None = None,
) -> np.ndarray:
    """Active fleet = historical baseline + cum launches − deorbit (Rule 23 exception)."""
    hist_deorbit = (
        historical_opening_balance_deorbit(spec.historical_baseline, spec.useful_life_years).values
        if include_historical
        else np.zeros(HORIZON_YEARS)
    )
    cohort_deorbit = launch_cohort_deorbit(
        YearVector(launches), useful_life_years=spec.useful_life_years
    ).values
    active = np.zeros(HORIZON_YEARS, dtype=np.float64)
    cum_launched = 0.0
    cum_hist_deorbit = 0.0
    cum_cohort_deorbit = 0.0
    baseline = spec.historical_baseline if include_historical else 0.0
    for t in range(HORIZON_YEARS):
        cum_launched += launches[t]
        cum_hist_deorbit += hist_deorbit[t]
        cum_cohort_deorbit += cohort_deorbit[t]
        active[t] = max(0.0, baseline + cum_launched - cum_hist_deorbit - cum_cohort_deorbit)
        if t == 0 and end_2025_anchor is not None:
            active[t] = end_2025_anchor
    return active


def _pool_state(spec: VehiclePoolSpec, launches: np.ndarray, active: np.ndarray) -> VehiclePoolState:
    f9 = np.zeros(HORIZON_YEARS)
    ship = np.zeros(HORIZON_YEARS)
    kg = np.zeros(HORIZON_YEARS)
    for t in range(HORIZON_YEARS):
        if spec.sats_per_f9_launch > 0:
            f9[t] = launches[t] / spec.sats_per_f9_launch
        if spec.sats_per_starship_launch > 0:
            ship[t] = launches[t] / spec.sats_per_starship_launch
            kg[t] = launches[t] * spec.mass_kg
    return VehiclePoolState(
        launches=YearVector(launches),
        active_fleet=YearVector(active),
        bb_gbps=YearVector(active * spec.bb_gbps_per_sat),
        dtc_gbps=YearVector(active * spec.dtc_gbps_per_sat),
        f9_launches=YearVector(f9),
        starship_launches=YearVector(ship),
        starship_kg_demand=YearVector(kg),
    )


def compute_vehicle_pools(
    assumptions: Assumptions,
    *,
    allocation: AllocatorAllocation | None = None,
    allocations: VehicleAllocations | None = None,
) -> VehiclePoolsResult:
    """Track four vehicle pools; 2025 launch anchors; V2 phase-out + V3 startup gates.

    Excel cell:        Starlink!D33:D63
    Excel label:       "V2 BB launches per year"
    Architecture ref:  §8.1 / §8.2 / §8.3
    Principle:         12 (demand/output decoupling at module boundary)

    """
    if allocations is not None:
        alloc_v2_bb = allocations.v2_bb
        alloc_v2_dtc = allocations.v2_dtc
        alloc_v3_bb = allocations.v3_bb
        alloc_v3_dtc = allocations.v3_dtc
    elif allocation is not None:
        alloc_v2_bb = alloc_v2_dtc = alloc_v3_bb = alloc_v3_dtc = allocation
    else:
        alloc_v2_bb = alloc_v2_dtc = alloc_v3_bb = alloc_v3_dtc = None

    v3_bb_start = int(assumption_scalar(assumptions, "V3 BB first launch year", default=2026.0))
    v3_dtc_start = int(assumption_scalar(assumptions, "V3 DTC first launch year", default=2028.0))

    ratchet = np.zeros(HORIZON_YEARS)
    v3_bb_launches = _launches_for_pool(
        _pool_spec_v3_bb(assumptions),
        assumptions,
        is_v2=False,
        is_dtc=False,
        ratchet_active=ratchet,
        v3_startup_year=v3_bb_start,
        allocation=alloc_v3_bb,
    )
    for t in range(HORIZON_YEARS):
        if v3_bb_launches[t] > 0 or (t > 0 and ratchet[t - 1] > 0):
            ratchet[t] = 1.0
        elif t > 0:
            ratchet[t] = ratchet[t - 1]

    v2_bb_spec = _pool_spec_v2_bb(assumptions)
    v2_dtc_spec = _pool_spec_v2_dtc(assumptions)
    v3_bb_spec = _pool_spec_v3_bb(assumptions)
    v3_dtc_spec = _pool_spec_v3_dtc(assumptions)

    v2_bb_launches = _launches_for_pool(
        v2_bb_spec, assumptions, is_v2=True, is_dtc=False,
        ratchet_active=ratchet, v3_startup_year=None, allocation=alloc_v2_bb,
    )
    v2_dtc_launches = _launches_for_pool(
        v2_dtc_spec, assumptions, is_v2=True, is_dtc=True,
        ratchet_active=ratchet, v3_startup_year=None, allocation=alloc_v2_dtc,
    )
    v3_bb_launches = _launches_for_pool(
        v3_bb_spec, assumptions, is_v2=False, is_dtc=False,
        ratchet_active=ratchet, v3_startup_year=v3_bb_start, allocation=alloc_v3_bb,
    )
    v3_dtc_launches = _launches_for_pool(
        v3_dtc_spec, assumptions, is_v2=False, is_dtc=True,
        ratchet_active=ratchet, v3_startup_year=v3_dtc_start, allocation=alloc_v3_dtc,
    )

    v2_bb_active = _active_fleet(
        v2_bb_spec,
        v2_bb_launches,
        include_historical=True,
        end_2025_anchor=assumption_scalar(
            assumptions, "V2 Mini BB Active Sats — end-2025", default=5246.0
        ),
    )
    v2_dtc_active = _active_fleet(
        v2_dtc_spec,
        v2_dtc_launches,
        include_historical=True,
        end_2025_anchor=assumption_scalar(
            assumptions, "V2 Mini DTC Active Sats — end-2025", default=650.0
        ),
    )
    v3_bb_active = _active_fleet(v3_bb_spec, v3_bb_launches, include_historical=False)
    v3_dtc_active = _active_fleet(v3_dtc_spec, v3_dtc_launches, include_historical=False)

    v2_bb = _pool_state(v2_bb_spec, v2_bb_launches, v2_bb_active)
    v2_dtc = _pool_state(v2_dtc_spec, v2_dtc_launches, v2_dtc_active)
    v3_bb = _pool_state(v3_bb_spec, v3_bb_launches, v3_bb_active)
    v3_dtc = _pool_state(v3_dtc_spec, v3_dtc_launches, v3_dtc_active)

    legacy_bb = assumption_year_vector(
        assumptions, "Legacy V1/V1.5 Active Bandwidth (Gbps, year-row runoff)", default=71888.0
    )

    total_bb = YearVector(
        v2_bb.bb_gbps.values + v3_bb.bb_gbps.values + legacy_bb.values
    )
    total_dtc = YearVector(v2_dtc.dtc_gbps.values + v3_dtc.dtc_gbps.values)
    total_sats = YearVector(
        v2_bb.active_fleet.values
        + v2_dtc.active_fleet.values
        + v3_bb.active_fleet.values
        + v3_dtc.active_fleet.values
    )

    return VehiclePoolsResult(
        v2_bb=v2_bb,
        v2_dtc=v2_dtc,
        v3_bb=v3_bb,
        v3_dtc=v3_dtc,
        total_active_sats=total_sats,
        total_bb_gbps=total_bb,
        total_dtc_gbps=total_dtc,
        legacy_bb_gbps=legacy_bb,
        f9_v2_bb_launches=v2_bb.f9_launches,
        f9_v2_dtc_launches=v2_dtc.f9_launches,
        starship_v3_bb_launches=v3_bb.starship_launches,
        starship_v3_dtc_launches=v3_dtc.starship_launches,
        v3_bb_kg_demand=v3_bb.starship_kg_demand,
        v3_dtc_kg_demand=v3_dtc.starship_kg_demand,
    )
