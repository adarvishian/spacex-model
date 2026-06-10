"""Three-bucket CapEx split + growth-cap base (U1 / F1 cap-base reconciliation).

Bucket 1 — Growth: IRR-ranked allocation, capped at R64/R65/R66.
Bucket 2 — Enabling infrastructure: senior claim + project debt (Terafab).
Bucket 3 — Maintenance / refresh: predetermined senior claim in queue gate.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.priority import ModuleSpotIrrs
from spacex_model.calc.allocator.types import QueueSubBlockDemands
from spacex_model.calc.facilities_build import FacilitiesBuildResult
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import (
    assumption_scalar,
    assumption_year_vector,
    derived_sat_unit_cost_mm,
)
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class CapBaseInputs:
    """Predetermined inputs for three-bucket classification (acyclic)."""

    assumptions: Assumptions
    sub_demands: QueueSubBlockDemands
    module_outputs: dict[str, AllocatorOut]
    facilities_build: FacilitiesBuildResult | None = None
    starlink_headroom_sats: YearVector | None = None
    starlink_blended_slug_mm: YearVector | None = None
    odc_target_sats: YearVector | None = None
    terr_target_mw: YearVector | None = None
    odc_demand_buildable_override: YearVector | None = None
    terr_demand_buildable_override: YearVector | None = None


@dataclass(frozen=True, slots=True)
class CapBaseResult:
    """Growth caps + senior claims + at-cost chip transfer."""

    growth_caps: ModuleSpotIrrs
    maintenance_claim: YearVector
    enabling_infra_equity: YearVector
    chip_at_cost_per_sat: YearVector
    odc_demand_buildable: YearVector
    terr_demand_buildable: YearVector


def _module_capex(outputs: dict[str, AllocatorOut], key: str) -> np.ndarray:
    out = outputs.get(key)
    if out is None:
        return np.zeros(HORIZON_YEARS, dtype=np.float64)
    return out.module_capex.values


def _starlink_headroom_sats(inputs: CapBaseInputs) -> np.ndarray:
    if inputs.starlink_headroom_sats is not None:
        return inputs.starlink_headroom_sats.values
    vec = assumption_year_vector(
        inputs.assumptions, cl.DEMAND_SATURATION_DEPLOYMENT_HEADROOM_SATS, default=0.0
    ).values
    if np.any(vec > 0.0):
        return vec
    return np.maximum(0.0, inputs.sub_demands.starlink_v3_bb_kg.values / 2000.0)


def _starlink_blended_slug_mm(inputs: CapBaseInputs) -> np.ndarray:
    if inputs.starlink_blended_slug_mm is not None:
        return inputs.starlink_blended_slug_mm.values
    vec = assumption_year_vector(
        inputs.assumptions,
        cl.BLENDED_NEW_SAT_CAPEX_SLUG_MM_SAT_MEMO_ONLY_FEEDS_CAE_R88_CAP_NO_LONGER_DRIVES_DEPLOYMENT,
        default=0.0,
    ).values
    if np.any(vec > 0.0):
        return vec
    mass = inputs.assumptions.lookup_scalar(cl.V3_MASS_KG)
    fallback = derived_sat_unit_cost_mm(inputs.assumptions, mass)
    return np.full(HORIZON_YEARS, fallback, dtype=np.float64)


def compute_chip_at_cost_per_sat(
    assumptions: Assumptions, facilities_build: FacilitiesBuildResult | None
) -> YearVector:
    """Predetermined Terafab chip transfer — design-capacity absorption, never ÷ this-year volume.

    Excel cell:        AI - Compute!D39
    Excel label:       "Chip cost at-cost ($/sat)"
    Architecture ref:  §5.1 bucket-2 at-cost transfer
    Principle:         9 (predetermined absorption basis)

    Formula: Predetermined Terafab chip transfer — design-capacity absorption, never ÷ this-year volume.

    """
    a = assumptions
    chips_per_sat = a.lookup_scalar(cl.CHIPS_PER_SAT, default=0.0)
    if chips_per_sat <= 0.0:
        compute_kw = assumption_scalar(a, cl.COMPUTE_POWER_PER_SAT_KW)
        chip_tdp = 700.0
        if chip_tdp > 0:
            chips_per_sat = max(1.0, np.floor(compute_kw * 1000.0 / chip_tdp))

    asp_anchor = a.lookup_scalar(
        "Chip cost basis ($/TFLOPS, gen anchor @2025)", default=0.0
    )
    prod_frac = assumption_scalar(
        a, cl.TERAFAB_PRODUCTION_COST_FRAC_CHIP_AT_COST_DC_CAPEX
    )
    wl_decay = assumption_scalar(
        a, cl.CHIP_COST_PER_TFLOPS_DECLINE_RATE_G_PER_FLOP_A8_2
    )
    offsets = np.arange(HORIZON_YEARS, dtype=np.float64)
    asp = asp_anchor * np.power(1.0 - wl_decay, offsets)

    values = chips_per_sat * asp * prod_frac

    if facilities_build is not None:
        chips_per_wspm = assumption_scalar(a, cl.TERAFAB_GOOD_CHIPS_PER_WSPM_PER_YR)
        fab_life = assumption_scalar(a, cl.TERAFAB_FAB_USEFUL_LIFE_DEPRECIATION_YEARS)
        cum_capex = np.cumsum(facilities_build.chip_fab_capex.values)
        cum_wspm = np.cumsum(np.maximum(facilities_build.chip_fab_capex.values, 0.0))
        for t in range(HORIZON_YEARS):
            lifetime_output = (
                max(cum_wspm[t], 1.0) * chips_per_wspm * max(fab_life, 1.0)
            )
            if lifetime_output > 0 and cum_capex[t] > 0:
                absorption = (cum_capex[t] / lifetime_output) * chips_per_sat
                values[t] = max(values[t], absorption)

    return YearVector(values)


def _odc_target_sats(inputs: CapBaseInputs) -> np.ndarray:
    if inputs.odc_target_sats is not None:
        return inputs.odc_target_sats.values
    odc_cash = inputs.sub_demands.odc_cash.values
    mass = assumption_scalar(inputs.assumptions, cl.V3_MASS_KG)
    cost = derived_sat_unit_cost_mm(inputs.assumptions, mass)
    if cost > 0 and np.any(odc_cash > 0):
        return odc_cash / cost
    kg = inputs.sub_demands.odc_kg.values
    mass = assumption_scalar(inputs.assumptions, cl.V3_MASS_KG)
    if mass > 0:
        return kg / mass
    return np.zeros(HORIZON_YEARS, dtype=np.float64)


def _terr_target_mw(inputs: CapBaseInputs) -> np.ndarray:
    if inputs.terr_target_mw is not None:
        return inputs.terr_target_mw.values
    cash = inputs.sub_demands.ai_stack_cash.values
    slug = assumption_scalar(inputs.assumptions, cl.TERRESTRIAL_MW_BUILD) / 1e6
    if slug > 0 and np.any(cash > 0):
        return cash / slug
    return assumption_year_vector(
        inputs.assumptions, cl.TERR_DEMAND_BUILDABLE_CAPEX_MM, default=0.0
    ).values


def _subsystem_cost_per_sat(assumptions: Assumptions) -> np.ndarray:
    wl = assumption_year_vector(
        assumptions, cl.SUBSYSTEM_COST_W_WL_SAT, default=0.0
    ).values
    if np.any(wl > 0.0):
        return wl
    mass = assumptions.lookup_scalar(cl.V3_MASS_KG)
    slug_mm = derived_sat_unit_cost_mm(assumptions, mass)
    floor = assumptions.lookup_scalar(
        cl.WRIGHT_S_LAW_FLOOR_PCT_OF_BASE_SUBSYSTEM_COST, default=0.2
    )
    return np.full(HORIZON_YEARS, slug_mm * 1e6 * max(floor, 0.5), dtype=np.float64)


def compute_ai_demand_buildable(
    inputs: CapBaseInputs, chip_at_cost: YearVector
) -> tuple[YearVector, YearVector]:
    """ODC + Terr growth-slice demand-buildable CapEx (feeds CAE R66).

    Excel cell:        AI - Compute!D202:D203
    Excel label:       "ODC demand-buildable CapEx ($mm)" … "Terr demand-buildable CapEx ($mm)"
    Architecture ref:  §5.1 bucket-1 growth slice
    Principle:         12 (exogenous demand; fab excluded from growth base)

    Formula: ODC + Terr growth-slice demand-buildable CapEx (feeds CAE R66).

    """
    a = inputs.assumptions
    target_sats = _odc_target_sats(inputs)
    subsystem = _subsystem_cost_per_sat(a)
    odc = target_sats * (subsystem + chip_at_cost.values) / 1e6

    mw = _terr_target_mw(inputs)
    slug_mw = assumption_scalar(a, cl.TERRESTRIAL_MW_BUILD) / 1e6
    wl = assumption_scalar(a, cl.TERRESTRIAL_FACILITY_COST_CAGR)
    offsets = np.arange(HORIZON_YEARS, dtype=np.float64)
    slug_vec = slug_mw * np.power(1.0 + wl, offsets)
    terr = mw * slug_vec

    if inputs.odc_demand_buildable_override is not None:
        odc = inputs.odc_demand_buildable_override.values
    if inputs.terr_demand_buildable_override is not None:
        terr = inputs.terr_demand_buildable_override.values

    return YearVector(odc), YearVector(terr)


def compute_maintenance_claim(inputs: CapBaseInputs) -> YearVector:
    """Bucket-3 maintenance / refresh — predetermined senior queue-gate claim.

    Excel cell:        Cash Allocation Engine (U1 Python senior claim — not yet on xlsx gate)
    Excel label:       "Maintenance / refresh CapEx ($mm)"
    Architecture ref:  §5.1 bucket-3
    Principle:         4 (senior claim before IRR queue)

    Formula: Bucket-3 maintenance / refresh — predetermined senior queue-gate claim.

    """
    a = inputs.assumptions
    slug = _starlink_blended_slug_mm(inputs)
    headroom = _starlink_headroom_sats(inputs)
    repl_rate = assumption_scalar(a, cl.TERMINAL_REPLACEMENT_RATE_INSTALLED_YR)
    starlink_maint = headroom * slug * repl_rate

    cl_maint = np.zeros(HORIZON_YEARS, dtype=np.float64)

    return YearVector(starlink_maint + cl_maint)


def compute_enabling_infra_equity_claim(
    facilities_build: FacilitiesBuildResult | None,
) -> YearVector:
    """Bucket-2 enabling-infra equity portion — Terafab lump funded via project debt (U3).

    Excel cell:        Facilities Build (non-Terafab buckets)
    Excel label:       "Total facility CapEx ($mm)" ex chip-fab
    Architecture ref:  §5.1 bucket-2
    Principle:         3 (enabling infra out of IRR growth base)

    Formula: Bucket-2 enabling-infra equity portion — Terafab lump funded via project debt (U3).

    """
    if facilities_build is None:
        return YearVector.zeros()
    equity = (
        facilities_build.sat_mfg_capex.values
        + facilities_build.launch_vehicle_capex.values
        + facilities_build.terminal_capex.values
        + facilities_build.hq_capex.values
        + facilities_build.starfactory_capex.values
    )
    return YearVector(equity)


def compute_growth_caps(
    inputs: CapBaseInputs, chip_at_cost: YearVector
) -> ModuleSpotIrrs:
    """CAE R64/R65/R66 — growth-slice max deployable caps.

    Excel cell:        Cash Allocation Engine!D64:D66
    Excel label:       "Cap: Starlink max deployable ($mm)" … "Cap: AI-Compute max deployable ($mm)"
    Architecture ref:  PRD U1 / F1 cap-base reconciliation
    Principle:         4 (growth allocation capped at absorbable demand)

    Formula: CAE R64/R65/R66 — growth-slice max deployable caps.

    """
    headroom = _starlink_headroom_sats(inputs)
    slug = _starlink_blended_slug_mm(inputs)
    starlink_cap = headroom * slug

    cl_cap = _module_capex(inputs.module_outputs, "customer_launch")
    if not np.any(cl_cap > 0.0):
        cl_cap = inputs.sub_demands.customer_launch_cash.values

    odc_build, terr_build = compute_ai_demand_buildable(inputs, chip_at_cost)
    ai_cap = odc_build.values + terr_build.values

    return ModuleSpotIrrs(
        starlink=YearVector(starlink_cap),
        customer_launch=YearVector(cl_cap),
        ai_compute=YearVector(ai_cap),
    )


def compute_cap_base(inputs: CapBaseInputs) -> CapBaseResult:
    """Full three-bucket split for allocator spine (U1).

    Excel cell:        Cash Allocation Engine + AI - Compute roll-up
    Excel label:       "▸ CAPACITY-PRIORITY ALLOCATION"
    Architecture ref:  PRD §5.1 three-bucket taxonomy
    Principle:         4 (growth slice only in IRR queue)

    Formula: Full three-bucket split for allocator spine (U1).

    """
    chip = compute_chip_at_cost_per_sat(inputs.assumptions, inputs.facilities_build)
    odc_build, terr_build = compute_ai_demand_buildable(inputs, chip)
    return CapBaseResult(
        growth_caps=compute_growth_caps(inputs, chip),
        maintenance_claim=compute_maintenance_claim(inputs),
        enabling_infra_equity=compute_enabling_infra_equity_claim(
            inputs.facilities_build
        ),
        chip_at_cost_per_sat=chip,
        odc_demand_buildable=odc_build,
        terr_demand_buildable=terr_build,
    )
