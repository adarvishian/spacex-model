"""Facilities Build — 7-bucket enabling-infra CapEx engine (V4.113 FB tab).

Architecture §5.1 bucket-2 / PRD R2. Not a P&L module; books no FCF.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import CONSERVATION_RESIDUAL_TOLERANCE_MM, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


def _vec_or_zero(vec: YearVector | None) -> np.ndarray:
    return vec.values if vec is not None else np.zeros(HORIZON_YEARS, dtype=np.float64)


def _straight_line_da(
    capex_lines: list[np.ndarray],
    lives: list[float],
) -> np.ndarray:
    """MIN(cum CapEx, Σ line_cum/life) per Excel FB D&A rows."""
    da = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        total_cum = 0.0
        target = 0.0
        for capex, life in zip(capex_lines, lives, strict=True):
            if life <= 0:
                continue
            cum = float(np.sum(capex[: t + 1]))
            total_cum += cum
            target += cum / life
        da[t] = min(total_cum, target)
    return da


def _bucket_da_residual(capex: np.ndarray, da: np.ndarray) -> np.ndarray:
    """cum D&A − cum CapEx per bucket (≤ 0 when D&A lags CapEx)."""
    cum_capex = np.cumsum(capex)
    cum_da = np.cumsum(da)
    return cum_da - cum_capex


@dataclass(frozen=True, slots=True)
class FacilitiesBuildInputs:
    """Upstream drivers — exogenous to FB (cross-tab reads)."""

    assumptions: Assumptions
    sats_built_starlink: YearVector | None = None
    ships_built: YearVector | None = None
    boosters_built: YearVector | None = None
    chips_demanded: YearVector | None = None
    group_revenue_base: YearVector | None = None
    starship_launches: YearVector | None = None
    terminal_toggle: float | None = None


@dataclass(frozen=True, slots=True)
class FacilitiesBuildResult:
    """Canonical Facilities Build outputs."""

    sat_mfg_capex: YearVector
    sat_mfg_da: YearVector
    launch_vehicle_capex: YearVector
    launch_vehicle_da: YearVector
    terminal_capex: YearVector
    terminal_da: YearVector
    hq_capex: YearVector
    hq_da: YearVector
    chip_fab_capex: YearVector
    chip_fab_da: YearVector
    starfactory_capex: YearVector
    starfactory_da: YearVector
    gigabay_installed_capacity: YearVector
    total_facility_capex: YearVector
    conservation_max_bucket: YearVector


def compute_facilities_build(inputs: FacilitiesBuildInputs) -> FacilitiesBuildResult:
    """Capacity-step facility CapEx engine — V4.113 Facilities Build tab.

    Excel cell:        Facilities Build!D43:S43
    Excel label:       "Total facility CapEx ($mm) = sat-mfg + launch/vehicle + terminal + HQ"
    Architecture ref:  §5.1 bucket-2 enabling infrastructure
    Principle:         3 (supply-side tab; at-cost transfer out)

    """
    a = inputs.assumptions
    sats = _vec_or_zero(inputs.sats_built_starlink)
    ships = _vec_or_zero(inputs.ships_built)
    boosters = _vec_or_zero(inputs.boosters_built)
    chips = _vec_or_zero(inputs.chips_demanded)
    revenue = _vec_or_zero(inputs.group_revenue_base)
    starship_launches = _vec_or_zero(inputs.starship_launches)

    # --- Bucket 1: Satellite-mfg (Redmond) ---
    sat_base = assumption_scalar(a, cl.SAT_FACTORY_BASE_CAPACITY_2025_SATS_YR, default=0.0)
    sat_incr = assumption_scalar(a, cl.SAT_FACTORY_CAPACITY_SATS_YR_PER_INCREMENT, default=1.0)
    sat_cost = assumption_scalar(a, cl.SAT_FACTORY_COST_PER_CAPACITY_INCREMENT_MM, default=0.0)
    sat_exp = assumption_scalar(a, cl.SAT_FACILITY_CAPACITY_RATIO_CAPEX_EXPONENT, default=1.0)
    sat_life = assumption_scalar(a, cl.SAT_FACTORY_USEFUL_LIFE_YEARS, default=20.0)
    gs_per_yr = assumption_scalar(a, cl.GROUND_STATIONS_BUILT_PER_YEAR_PLACEHOLDER_FLAT, default=0.0)
    gs_cost = assumption_scalar(a, cl.GROUND_STATION_BUILD_CAPEX_PER_STATION_MM, default=0.0)
    gs_life = assumption_scalar(a, cl.GROUND_STATION_USEFUL_LIFE_YEARS, default=15.0)

    installed_sat_cap = np.zeros(HORIZON_YEARS, dtype=np.float64)
    new_sat_factory_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)
    ground_station_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)

    for t in range(HORIZON_YEARS):
        if t == 0:
            installed_sat_cap[t] = max(sat_base, sats[t])
        else:
            installed_sat_cap[t] = max(installed_sat_cap[t - 1], sats[t])
        prior_cap = sat_base if t == 0 else installed_sat_cap[t - 1]
        if sat_incr > 0:
            ratio = max(0.0, sats[t] - prior_cap) / sat_incr
        else:
            ratio = 0.0
        new_sat_factory_capex[t] = (ratio**sat_exp) * sat_cost if ratio > 0 else 0.0
        ground_station_capex[t] = gs_per_yr * gs_cost

    sat_mfg_capex = new_sat_factory_capex + ground_station_capex
    sat_mfg_da = _straight_line_da(
        [new_sat_factory_capex, ground_station_capex],
        [sat_life, gs_life],
    )

    # --- Bucket 2: Starship / Gigabay / engines / pads ---
    gigabay_base = assumption_scalar(a, cl.GIGABAY_BASE_CAPACITY_2025_SHIPS_YR, default=8.0)
    cap_ceiling = assumption_scalar(a, cl.STARSHIP_BUILD_CAPACITY_CEILING_SHIPS_YR, default=250.0)
    cap_ramp = assumption_scalar(a, cl.MAX_STARSHIP_BUILD_CAPACITY_ADDED_PER_YEAR_SHIPS_YR, default=15.0)
    op_year = int(assumption_scalar(a, cl.STARSHIP_OPERATIONAL_YEAR, default=2025.0))
    ships_per_gigabay = assumption_scalar(a, cl.STARSHIP_FACILITY_CAPACITY_SHIPS_YR_PER_GIGABAY, default=100.0)
    gigabay_cost = assumption_scalar(a, cl.STARSHIP_FACILITY_COST_PER_GIGABAY_INCREMENT_MM, default=500.0)
    ship_fac_life = assumption_scalar(a, cl.STARSHIP_FACILITY_USEFUL_LIFE_YEARS, default=30.0)
    raptor_booster = assumption_scalar(a, cl.RAPTOR_ENGINES_PER_BOOSTER_SUPER_HEAVY, default=33.0)
    raptor_ship = assumption_scalar(a, cl.RAPTOR_ENGINES_PER_SHIP_2ND_STAGE, default=3.0)
    eng_base = assumption_scalar(a, cl.ENGINE_FACILITY_BASE_CAPACITY_2025_ENGINES_YR, default=0.0)
    eng_incr = assumption_scalar(a, cl.ENGINE_FACILITY_CAPACITY_ENGINES_YR_PER_INCREMENT, default=1.0)
    eng_cost = assumption_scalar(a, cl.ENGINE_FACILITY_COST_PER_CAPACITY_INCREMENT_MM, default=0.0)
    eng_life = assumption_scalar(a, cl.ENGINE_FACILITY_USEFUL_LIFE_YEARS, default=25.0)
    launches_per_pad = assumption_scalar(a, cl.STARSHIP_LAUNCHES_PER_PAD_PER_YEAR, default=50.0)
    pads_base = assumption_scalar(a, cl.LAUNCH_PADS_BASE_IN_SERVICE_2025_STARSHIP_CAPABLE, default=0.0)
    pad_cost = assumption_scalar(a, cl.LAUNCH_PAD_BUILD_UPGRADE_COST_MM_PER_PAD, default=0.0)
    pad_life = assumption_scalar(a, cl.LAUNCH_PAD_USEFUL_LIFE_YEARS, default=30.0)

    gigabay_cap = np.zeros(HORIZON_YEARS, dtype=np.float64)
    new_gigabay_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)
    engine_demand = np.zeros(HORIZON_YEARS, dtype=np.float64)
    new_engine_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)
    installed_engine_cap = np.zeros(HORIZON_YEARS, dtype=np.float64)
    pads_needed = np.zeros(HORIZON_YEARS, dtype=np.float64)
    new_pad_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)
    installed_pads = np.zeros(HORIZON_YEARS, dtype=np.float64)
    starfactory_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)

    for t in range(HORIZON_YEARS):
        year = 2025 + t
        years_since_op = max(0, year - op_year)
        gigabay_cap[t] = min(cap_ceiling, gigabay_base + cap_ramp * years_since_op)
        if t > 0:
            added = max(0.0, gigabay_cap[t] - gigabay_cap[t - 1])
        else:
            added = 0.0
        if ships_per_gigabay > 0:
            new_gigabay_capex[t] = (added / ships_per_gigabay) * gigabay_cost

        engine_demand[t] = boosters[t] * raptor_booster + ships[t] * raptor_ship
        if t == 0:
            installed_engine_cap[t] = max(eng_base, engine_demand[t])
            prior_eng = eng_base
        else:
            installed_engine_cap[t] = max(installed_engine_cap[t - 1], engine_demand[t])
            prior_eng = installed_engine_cap[t - 1]
        if eng_incr > 0:
            new_engine_capex[t] = max(0.0, engine_demand[t] - prior_eng) / eng_incr * eng_cost

        if launches_per_pad > 0:
            pads_needed[t] = starship_launches[t] / launches_per_pad
        if t == 0:
            installed_pads[t] = max(pads_base, np.ceil(pads_needed[t]))
            prior_pads = pads_base
        else:
            installed_pads[t] = max(installed_pads[t - 1], np.ceil(pads_needed[t]))
            prior_pads = installed_pads[t - 1]
        new_pads = max(0.0, np.ceil(pads_needed[t]) - prior_pads)
        new_pad_capex[t] = new_pads * pad_cost

    launch_vehicle_capex = new_gigabay_capex + new_engine_capex + new_pad_capex + starfactory_capex
    launch_vehicle_da = _straight_line_da(
        [new_gigabay_capex, new_engine_capex, new_pad_capex, starfactory_capex],
        [ship_fac_life, eng_life, pad_life, ship_fac_life],
    )

    # --- Bucket 3: Terminals (toggle-gated, default OFF) ---
    term_toggle = (
        inputs.terminal_toggle
        if inputs.terminal_toggle is not None
        else assumption_scalar(a, cl.TERMINAL_FACTORY_CAPEX_TOGGLE_1_ON_0_OFF, default=0.0)
    )
    terminal_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)
    terminal_da = np.zeros(HORIZON_YEARS, dtype=np.float64)
    if term_toggle > 0:
        term_incr = assumption_scalar(a, cl.TERMINAL_FACTORY_CAPACITY_KITS_YR_PER_INCREMENT, default=1.0)
        term_cost = assumption_scalar(a, cl.TERMINAL_FACTORY_COST_PER_CAPACITY_INCREMENT_MM, default=0.0)
        term_life = assumption_scalar(a, cl.TERMINAL_FACTORY_USEFUL_LIFE_YEARS, default=20.0)
        # Placeholder demand — flat growth proxy when toggle on
        kits = np.ones(HORIZON_YEARS) * term_incr
        for t in range(HORIZON_YEARS):
            terminal_capex[t] = kits[t] / term_incr * term_cost * term_toggle
        terminal_da = _straight_line_da([terminal_capex], [term_life])

    # --- Bucket 4: HQ (Group revenue %) ---
    hq_pct = assumption_scalar(a, cl.HQ_FACILITY_CAPEX_OF_REVENUE, default=0.0)
    hq_life = assumption_scalar(a, cl.HQ_FACILITY_USEFUL_LIFE_YEARS, default=30.0)
    hq_capex = revenue * hq_pct
    hq_da = _straight_line_da([hq_capex], [hq_life])

    # --- Bucket 5: Chip-fab (Terafab) ---
    chips_per_wspm = assumption_scalar(a, cl.TERAFAB_GOOD_CHIPS_PER_WSPM_PER_YR, default=1.0)
    wspm_per_phase = assumption_scalar(a, cl.TERAFAB_CAPACITY_PER_FAB_PHASE_WSPM_PHASE, default=1.0)
    fab_all_in = assumption_scalar(a, cl.TERAFAB_FAB_CAPEX_BLENDED_ALL_IN_WSPM, default=0.0)
    constr_window = int(assumption_scalar(a, cl.TERAFAB_FAB_CONSTRUCTION_WINDOW_YEARS, default=3.0))
    fab_life = assumption_scalar(a, cl.TERAFAB_FAB_USEFUL_LIFE_DEPRECIATION_YEARS, default=20.0)
    spacex_share = assumption_scalar(a, cl.TERAFAB_SPACEX_COST_CAPACITY_SHARE_FRAC, default=1.0)

    required_wspm = np.zeros(HORIZON_YEARS, dtype=np.float64)
    installed_wspm = np.zeros(HORIZON_YEARS, dtype=np.float64)
    new_wspm = np.zeros(HORIZON_YEARS, dtype=np.float64)
    fab_slug_cost = np.zeros(HORIZON_YEARS, dtype=np.float64)
    new_fab_capex_spread = np.zeros(HORIZON_YEARS, dtype=np.float64)
    chip_fab_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)

    for t in range(HORIZON_YEARS):
        if chips_per_wspm > 0:
            required_wspm[t] = chips[t] / chips_per_wspm
        if wspm_per_phase > 0:
            target = np.ceil(required_wspm[t] / wspm_per_phase) * wspm_per_phase
        else:
            target = required_wspm[t]
        if t == 0:
            installed_wspm[t] = max(0.0, target)
        else:
            installed_wspm[t] = max(installed_wspm[t - 1], target)
        new_wspm[t] = installed_wspm[t] if t == 0 else max(0.0, installed_wspm[t] - installed_wspm[t - 1])
        fab_slug_cost[t] = new_wspm[t] * fab_all_in / 1_000_000.0

    for t in range(HORIZON_YEARS):
        window = fab_slug_cost[max(0, t - constr_window + 1) : t + 1]
        new_fab_capex_spread[t] = float(np.sum(window)) / max(constr_window, 1)
        chip_fab_capex[t] = new_fab_capex_spread[t] * spacex_share

    # Chip-fab D&A: depreciate only after useful-life offset (year offset row)
    chip_fab_da = np.zeros(HORIZON_YEARS, dtype=np.float64)
    if fab_life > 0:
        for t in range(HORIZON_YEARS):
            offset = t  # year offset from FB row 5
            depreciable = float(np.sum(chip_fab_capex[: t + 1]))
            if offset >= round(fab_life):
                start = max(0, t - int(round(fab_life)) + 1)
                depreciable -= float(np.sum(chip_fab_capex[:start]))
            chip_fab_da[t] = max(0.0, depreciable) / fab_life

    starfactory_da = _straight_line_da([starfactory_capex], [ship_fac_life])

    total = (
        sat_mfg_capex
        + launch_vehicle_capex
        + terminal_capex
        + hq_capex
        + chip_fab_capex
        + starfactory_capex
    )

    bucket_residuals = [
        _bucket_da_residual(sat_mfg_capex, sat_mfg_da),
        _bucket_da_residual(launch_vehicle_capex, launch_vehicle_da),
        _bucket_da_residual(terminal_capex, terminal_da),
        _bucket_da_residual(hq_capex, hq_da),
        _bucket_da_residual(chip_fab_capex, chip_fab_da),
        _bucket_da_residual(starfactory_capex, starfactory_da),
    ]
    conservation = np.max(np.stack(bucket_residuals, axis=0), axis=0)

    return FacilitiesBuildResult(
        sat_mfg_capex=YearVector(sat_mfg_capex),
        sat_mfg_da=YearVector(sat_mfg_da),
        launch_vehicle_capex=YearVector(launch_vehicle_capex),
        launch_vehicle_da=YearVector(launch_vehicle_da),
        terminal_capex=YearVector(terminal_capex),
        terminal_da=YearVector(terminal_da),
        hq_capex=YearVector(hq_capex),
        hq_da=YearVector(hq_da),
        chip_fab_capex=YearVector(chip_fab_capex),
        chip_fab_da=YearVector(chip_fab_da),
        starfactory_capex=YearVector(starfactory_capex),
        starfactory_da=YearVector(starfactory_da),
        gigabay_installed_capacity=YearVector(gigabay_cap),
        total_facility_capex=YearVector(total),
        conservation_max_bucket=YearVector(conservation),
    )


def facilities_conservation_ok(result: FacilitiesBuildResult) -> bool:
    """FB R44: max bucket (cum D&A − cum CapEx) must be ≤ 0 every year.

    Excel cell:        Facilities Build!D44:S44
    Excel label:       "Conservation: max bucket (cum D&A − cum CapEx): must be ≤ 0"
    Architecture ref:  §15 conservation
    Principle:         19 (enabling-infra D&A never exceeds cum CapEx)

    """
    return bool(
        np.all(result.conservation_max_bucket.values <= CONSERVATION_RESIDUAL_TOLERANCE_MM)
    )
