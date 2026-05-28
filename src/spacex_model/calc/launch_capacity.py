"""Launch Capacity — supply-side tab (Phase C).

Architecture §4 Launch Capacity / PRD §4.1. Not a P&L module.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import (
    assumption_scalar,
    assumption_year_vector,
    wrights_law_cost,
    year_chained_boy_from_eoy,
    year_chained_eoy,
    year_offset,
)
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class LaunchCapacityInputs:
    """Upstream inputs for Launch Capacity."""

    assumptions: Assumptions
    vehicle_build_claim_mm: YearVector | None = None
    f9_customer_launches: YearVector | None = None
    f9_starlink_v2_bb_launches: YearVector | None = None
    f9_starlink_v2_dtc_launches: YearVector | None = None


@dataclass(frozen=True, slots=True)
class LaunchCapacityResult:
    """Canonical Launch Capacity outputs consumed by downstream modules."""

    total_starship_launches: YearVector
    total_annual_capacity_kg: YearVector
    f9_launches: YearVector
    f9_fleet_eoy: YearVector
    f9_manufactured: YearVector
    f9_annual_capacity_kg: YearVector
    per_launch_upmass_kg: YearVector
    starship_at_cost_rate: YearVector
    f9_at_cost_rate: YearVector
    annual_vehicle_da: YearVector
    blended_cost_per_kg: YearVector
    launches_per_starship_cadence: YearVector
    blended_cost_per_starship_vehicle: YearVector


def _zeros() -> YearVector:
    return YearVector.zeros()


def compute_launch_capacity(inputs: LaunchCapacityInputs) -> LaunchCapacityResult:
    """Compute full Launch Capacity tab per V2.16 mechanics / Architecture §20.4.

    Excel cell:        Launch Capacity!D34:AC34
    Excel label:       "Total Annual Capacity (kg-to-LEO)"
    Architecture ref:  §20.4 capacity supply
    Principle:         3 (supply-side tab; no module P&L)

    """
    a = inputs.assumptions
    cap = a.capacity

    # --- Assumption scalars (§3 Capacity) ---
    sh_mfg_base = assumption_scalar(a, "Super Heavy manufacturing cost ($mm/unit, base year)")
    ship_mfg_base = assumption_scalar(a, "Starship 2nd-stage manufacturing cost ($mm/unit, base)")
    payload_booster_only = assumption_scalar(a, "Payload — booster-only mode (kg-to-LEO)")
    payload_fully_reusable = assumption_scalar(
        a, "Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)", default=100_000.0
    )
    if payload_fully_reusable == 100_000.0:
        alt = a.lookup("Payload — fully reusable mode (kg-to-LEO)")
        if alt and alt.scalar() is not None:
            payload_fully_reusable = float(alt.scalar())

    cadence_ceiling = assumption_scalar(a, "Cadence ceiling (flights/booster/year)")
    wl_turnaround = assumption_scalar(a, "WL learning rate — turnaround vs cum upmass doubling")
    base_turnaround = assumption_scalar(a, "Base turnaround time per booster (years/flight)", default=1.0)

    f9_booster_cost = assumption_scalar(a, "F9 booster (1st stage) mfg cost ($mm/unit)")
    f9_2nd_stage = assumption_scalar(a, "F9 2nd stage mfg cost ($mm/unit)")
    f9_fairing = assumption_scalar(a, "F9 fairing cost net of 75% recovery ($mm/flight)")
    f9_ops = assumption_scalar(a, "F9 per-launch ops cost ($mm)")
    f9_refurb_pct = assumption_scalar(a, "F9 booster refurb % of mfg")
    f9_payload = assumption_scalar(a, "F9 payload to LEO (kg)")
    f9_lifetime_reuses = assumption_scalar(a, "F9 lifetime reuses per booster")
    f9_cadence = assumption_scalar(a, "F9 cadence per booster (flights/year, flat)")
    f9_base_build_rate = assumption_scalar(a, "F9 base booster build rate (boosters/year, pre-V3-trigger)")
    v3_trigger_year = int(assumption_scalar(a, "V3 Starlink launch trigger year"))
    f9_decay_window = assumption_scalar(a, "F9 build-rate decay window (years)")
    f9_starting_fleet = assumption_scalar(a, "F9 starting fleet at 2025 SoY (boosters)")
    f9_retirement_rate = assumption_scalar(a, "F9 retirement rate (% of launches/year)", default=0.01)

    starship_mfg_anchor = assumption_scalar(
        a, "Starship manufacturing cost anchor ($mm/stack, 2024 baseline)", default=90.0
    )
    starship_mfg_wl = assumption_scalar(
        a, "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)", default=0.15
    )
    starship_ops_anchor = assumption_scalar(
        a, "Starship ops + fuel + refurb cost anchor ($mm/launch, 2024 baseline)", default=12.0
    )
    starship_ops_wl = assumption_scalar(
        a, "Starship ops + fuel + refurb WL learning rate (% reduction per doubling cum stacks)",
        default=0.1,
    )
    starship_wl_anchor_cum = assumption_scalar(
        a, "Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)", default=4.0
    )
    starship_booster_share = assumption_scalar(
        a, "Starship booster share of manufacturing cost (% of stack mfg)", default=0.6
    )
    lifetime_reuses_ship = assumption_scalar(a, "Lifetime reuses per ship (cap)", default=30.0)

    variant_mix = assumption_year_vector(a, "Variant mix (% fully reusable)").values
    lifetime_reuses_booster = assumption_year_vector(a, "Lifetime reuses per booster (year cap)").values

    vehicle_build = (
        inputs.vehicle_build_claim_mm.values
        if inputs.vehicle_build_claim_mm is not None
        else np.zeros(HORIZON_YEARS)
    )

    f9_customer = (
        inputs.f9_customer_launches.values
        if inputs.f9_customer_launches is not None
        else np.zeros(HORIZON_YEARS)
    )
    f9_sl_bb = (
        inputs.f9_starlink_v2_bb_launches.values
        if inputs.f9_starlink_v2_bb_launches is not None
        else np.zeros(HORIZON_YEARS)
    )
    f9_sl_dtc = (
        inputs.f9_starlink_v2_dtc_launches.values
        if inputs.f9_starlink_v2_dtc_launches is not None
        else np.zeros(HORIZON_YEARS)
    )

    years = np.arange(FIRST_YEAR, FIRST_YEAR + HORIZON_YEARS)

    # --- Starship fleet (Rule 23 year-chained) ---
    blended_vehicle_cost = sh_mfg_base + ship_mfg_base
    boosters_built = np.where(
        blended_vehicle_cost > 0,
        vehicle_build / blended_vehicle_cost,
        0.0,
    )
    boosters_retired = np.zeros(HORIZON_YEARS)
    starship_fleet_eoy = year_chained_eoy(
        np.zeros(HORIZON_YEARS), boosters_built, boosters_retired
    )

    cum_stacks = np.zeros(HORIZON_YEARS)
    cum_stacks[0] = starship_wl_anchor_cum + boosters_built[0]
    for t in range(1, HORIZON_YEARS):
        cum_stacks[t] = cum_stacks[t - 1] + boosters_built[t]

    # --- Starship cadence (Wright's Law on lagged cum upmass) ---
    per_launch_upmass = variant_mix * payload_fully_reusable + (1.0 - variant_mix) * payload_booster_only
    cum_upmass = np.zeros(HORIZON_YEARS)
    wl_alpha = -np.log2(1.0 - wl_turnaround) if wl_turnaround < 1.0 else 0.0

    cadence = np.ones(HORIZON_YEARS)
    total_starship_launches = np.zeros(HORIZON_YEARS)

    for t in range(HORIZON_YEARS):
        if t == 0:
            cadence[t] = 1.0
        else:
            prior_cum = cum_upmass[t - 1]
            if prior_cum > 0 and payload_fully_reusable > 0:
                mult = (prior_cum / payload_fully_reusable) ** wl_alpha
            else:
                mult = 1.0
            cadence[t] = max(1.0, min(cadence_ceiling, (1.0 / base_turnaround) * mult))

        booster_only = starship_fleet_eoy[t] * cadence[t] * (1.0 - variant_mix[t])
        fully_reusable = starship_fleet_eoy[t] * cadence[t] * variant_mix[t]
        total_starship_launches[t] = booster_only + fully_reusable

        if t == 0:
            cum_upmass[t] = 0.0
        else:
            cum_upmass[t] = cum_upmass[t - 1] + total_starship_launches[t - 1] * per_launch_upmass[t - 1]

    total_annual_capacity = total_starship_launches * per_launch_upmass

    # --- Starship at-cost rate (fully-allocated per Architecture §7.1) ---
    starship_mfg_cost = wrights_law_cost(
        starship_mfg_anchor, cum_stacks, starship_wl_anchor_cum, starship_mfg_wl
    )
    starship_ops_cost = wrights_law_cost(
        starship_ops_anchor, cum_stacks, starship_wl_anchor_cum, starship_ops_wl
    )
    with np.errstate(divide="ignore", invalid="ignore"):
        starship_da_share = np.where(
            lifetime_reuses_booster > 0,
            starship_mfg_cost
            * (
                starship_booster_share / np.maximum(lifetime_reuses_booster, 1.0)
                + (1.0 - starship_booster_share) / max(lifetime_reuses_ship, 1.0)
            ),
            0.0,
        )
    starship_at_cost = starship_ops_cost + starship_da_share

    # --- F9 fleet dynamics ---
    f9_manufactured = np.zeros(HORIZON_YEARS)
    f9_launches = np.zeros(HORIZON_YEARS)
    f9_retired = np.zeros(HORIZON_YEARS)

    for t in range(HORIZON_YEARS):
        year = years[t]
        if year == 2025:
            f9_manufactured[t] = 17.0
            f9_launches[t] = 171.0
            f9_retired[t] = 6.0
        elif year == 2026:
            f9_manufactured[t] = 17.0
            f9_launches[t] = 171.0
            demand = f9_customer[t] + f9_sl_bb[t] + f9_sl_dtc[t]
            f9_retired[t] = min(
                f9_starting_fleet + f9_manufactured[t] if t == 0 else 0,
                f9_launches[t] * f9_retirement_rate,
            )
            # Will recompute retired after fleet known
        else:
            decay = max(0.0, 1.0 - (year - v3_trigger_year) / f9_decay_window)
            f9_manufactured[t] = max(0.0, f9_base_build_rate * decay)
            demand = f9_customer[t] + f9_sl_bb[t] + f9_sl_dtc[t]
            f9_launches[t] = 0.0  # placeholder until fleet computed

    f9_fleet_eoy = np.zeros(HORIZON_YEARS)
    f9_boy = np.zeros(HORIZON_YEARS)
    f9_boy[0] = f9_starting_fleet
    for t in range(HORIZON_YEARS):
        year = years[t]
        if t > 0:
            f9_boy[t] = f9_fleet_eoy[t - 1]
        if year == 2025:
            f9_fleet_eoy[t] = 39.0
        elif year == 2026:
            f9_retired[t] = min(f9_boy[t] + f9_manufactured[t], f9_launches[t] * f9_retirement_rate)
            f9_fleet_eoy[t] = f9_boy[t] + f9_manufactured[t] - f9_retired[t]
        else:
            supply_cap = f9_boy[t] * f9_cadence
            demand = f9_customer[t] + f9_sl_bb[t] + f9_sl_dtc[t]
            f9_launches[t] = min(supply_cap, demand)
            f9_retired[t] = min(f9_boy[t] + f9_manufactured[t], f9_launches[t] * f9_retirement_rate)
            f9_fleet_eoy[t] = max(0.0, f9_boy[t] + f9_manufactured[t] - f9_retired[t])

    f9_annual_capacity = f9_boy * f9_cadence * f9_payload
    f9_variable = f9_2nd_stage + f9_fairing + f9_ops + f9_refurb_pct * f9_booster_cost
    f9_da_share = f9_booster_cost / f9_lifetime_reuses
    f9_at_cost_scalar = f9_variable + f9_da_share
    f9_at_cost = np.full(HORIZON_YEARS, f9_at_cost_scalar)

    total_launches = f9_launches + total_starship_launches
    total_upmass = f9_launches * f9_payload + total_annual_capacity
    total_launch_capex = f9_launches * f9_at_cost + total_starship_launches * starship_at_cost
    with np.errstate(divide="ignore", invalid="ignore"):
        blended_kg = np.where(total_upmass > 0, total_launch_capex * 1e6 / total_upmass, 0.0)

    annual_vehicle_da = total_starship_launches * starship_da_share + f9_launches * f9_da_share

    return LaunchCapacityResult(
        total_starship_launches=YearVector(total_starship_launches),
        total_annual_capacity_kg=YearVector(total_annual_capacity),
        f9_launches=YearVector(f9_launches),
        f9_fleet_eoy=YearVector(f9_fleet_eoy),
        f9_manufactured=YearVector(f9_manufactured),
        f9_annual_capacity_kg=YearVector(f9_annual_capacity),
        per_launch_upmass_kg=YearVector(per_launch_upmass),
        starship_at_cost_rate=YearVector(starship_at_cost),
        f9_at_cost_rate=YearVector(f9_at_cost),
        annual_vehicle_da=YearVector(annual_vehicle_da),
        blended_cost_per_kg=YearVector(blended_kg),
        launches_per_starship_cadence=YearVector(cadence),
        blended_cost_per_starship_vehicle=YearVector.constant(blended_vehicle_cost),
    )


def total_annual_capacity_kg(inputs: LaunchCapacityInputs | None = None) -> YearVector:
    """Total Annual Capacity (kg-to-LEO) — Starship-only canonical label.

    Excel cell:        Launch Capacity!D34:AC34
    Excel label:       "Total Annual Capacity (kg-to-LEO)"
    Architecture ref:  §20.4 capacity supply
    Principle:         3 (supply-side tab; no module P&L)

    """
    if inputs is None:
        return _zeros()
    return compute_launch_capacity(inputs).total_annual_capacity_kg
