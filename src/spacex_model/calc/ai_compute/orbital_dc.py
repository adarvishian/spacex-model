"""Orbital DC (ODC) sub-module — dual-revenue slice within AI - Compute tab."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc.starlink_capacity import StarlinkCapacityResult
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import (
    assumption_scalar,
    assumption_year_vector,
    derived_sat_unit_cost_mm,
)
from spacex_model.domain.irr import compute_irr_engine
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class OrbitalDcInputs:
    """Inputs for Orbital DC within unified AI - Compute module."""

    assumptions: Assumptions
    starlink_capacity: StarlinkCapacityResult | None = None
    sats_deployed: YearVector | None = None
    chip_at_cost_per_sat: YearVector | None = None


def _per_sat_model_a_revenue_mm(assumptions: Assumptions, year_index: int) -> float:
    compute_kw = assumption_scalar(assumptions, cl.COMPUTE_POWER_PER_SAT_KW)
    coreweave = assumption_year_vector(
        assumptions, cl.COREWEAVE_BASELINE_ANCHOR_YEAR_ROW, default=12.0
    )
    pue_uplift = assumption_scalar(assumptions, cl.ORBITAL_PUE_UPLIFT_VS_TERRESTRIAL)
    util = assumption_scalar(assumptions, cl.ODC_UTILIZATION_FACTOR)
    gw = compute_kw / 1e6
    baseline = (
        coreweave.values[year_index]
        if year_index < HORIZON_YEARS
        else coreweave.at(FIRST_YEAR)
    )
    return gw * baseline * pue_uplift * util * 1000.0


def _per_sat_model_b_revenue_mm(assumptions: Assumptions, year_index: int) -> float:
    compute_kw = assumption_scalar(assumptions, cl.COMPUTE_POWER_PER_SAT_KW)
    chip_tdp = assumption_year_vector(
        assumptions, cl.CHIP_TDP_PER_CHIP_W_YEAR_ROW, default=700.0
    )
    chip_fp8 = assumption_year_vector(
        assumptions, cl.CHIP_FP8_PERFORMANCE_TFLOPS_YEAR_ROW, default=1979.0
    )
    util = assumption_scalar(assumptions, cl.ODC_UTILIZATION_FACTOR)
    ecr = assumption_scalar(assumptions, cl.EFFECTIVE_COMPUTE_RATIO_RATIO)
    mix = assumption_scalar(assumptions, cl.WORKLOAD_MIX_INFERENCE_SHARE)
    price_gpu_hr = assumption_year_vector(
        assumptions, cl.PRICE_PER_H100_GPU_HR_YEAR_ROW, default=2.0
    )

    tdp = chip_tdp.values[year_index]
    fp8 = chip_fp8.values[year_index]
    if tdp <= 0:
        return 0.0
    price = price_gpu_hr.values[year_index]
    billable = (
        (compute_kw * 1000.0 / tdp)
        * fp8
        / 1e6
        * 8760.0
        * util
        * ecr
        * mix
        * price
        / 1e6
    )
    return billable


def per_sat_combined_revenue_mm(assumptions: Assumptions, year_index: int) -> float:
    """Credence-weighted Model A/B per-sat revenue ($mm/yr).

    Excel cell:        AI - Compute!—
    Excel label:       "Per-sat combined revenue ($mm/yr)"
    Architecture ref:  §9.2 dual revenue
    Principle:         8 (vending-machine module)

    Formula: Credence-weighted Model A/B per-sat revenue ($mm/yr).

    """
    pr_a = 0.5  # V4.131 retired Model A credence Pr(A)
    a = _per_sat_model_a_revenue_mm(assumptions, year_index)
    b = _per_sat_model_b_revenue_mm(assumptions, year_index)
    return pr_a * a + (1.0 - pr_a) * b


def per_sat_bandwidth_cost_mm(
    assumptions: Assumptions,
    starlink_capacity: StarlinkCapacityResult | None,
    year_index: int,
) -> float:
    """Per-sat bandwidth services cost from Starlink Capacity pool rates.

    Excel cell:        AI - Compute!—
    Excel label:       "Bandwidth services cost ($mm)"
    Architecture ref:  §7.2 / §9.4
    Principle:         9 (at-cost internal bandwidth)

    Formula: Per-sat bandwidth services cost from Starlink Capacity pool rates.

    """
    if starlink_capacity is None:
        return 0.0
    bb_share = assumption_scalar(assumptions, cl.BB_SHARE_OF_ODC_BANDWIDTH_CLAIM)
    gbps_per_gwh = assumption_scalar(assumptions, cl.GBPS_PER_GWH_ODC_COMPUTE_ENERGY)
    compute_kw = assumption_scalar(assumptions, cl.COMPUTE_POWER_PER_SAT_KW)
    gbps_per_sat = gbps_per_gwh * compute_kw
    bb_rate = starlink_capacity.bb_at_cost_rate_per_gbps.values[year_index] / 1e6
    dtc_rate = starlink_capacity.dtc_at_cost_rate_per_gbps.values[year_index] / 1e6
    return (
        bb_share * gbps_per_sat * bb_rate + (1.0 - bb_share) * gbps_per_sat * dtc_rate
    )


def per_sat_net_marginal_revenue_mm(
    assumptions: Assumptions,
    starlink_capacity: StarlinkCapacityResult | None,
    year_index: int,
) -> float:
    """Combined revenue minus opex and bandwidth per sat ($mm/yr).

    Excel cell:        AI - Compute!—
    Excel label:       "Per-sat net marginal revenue ($mm/yr)"
    Architecture ref:  §9.4 IRR engine input
    Principle:         2 (per-unit marginal IRR)

    Formula: Combined revenue minus opex and bandwidth per sat ($mm/yr).

    """
    combined = per_sat_combined_revenue_mm(assumptions, year_index)
    ground = assumption_scalar(assumptions, cl.ODC_GROUND_OPS_PCT_REV)
    insurance = assumption_scalar(assumptions, cl.ODC_INSURANCE_PCT_REV)
    other = assumption_scalar(assumptions, cl.ODC_OTHER_COGS_PCT_REV)
    opex = combined * (ground + insurance + other)
    bandwidth = per_sat_bandwidth_cost_mm(assumptions, starlink_capacity, year_index)
    return combined - opex - bandwidth


def _fleet_from_deployment(deployed: YearVector | None) -> YearVector:
    if deployed is None:
        return YearVector.zeros()
    fleet = np.zeros(HORIZON_YEARS, dtype=np.float64)
    active = 0.0
    for t in range(HORIZON_YEARS):
        active += deployed.values[t]
        fleet[t] = active
    return YearVector(fleet)


def orbital_bandwidth_claim(inputs: OrbitalDcInputs) -> tuple[YearVector, YearVector]:
    """BB and DTC Gbps claim for Starlink Capacity.

    Excel cell:        AI - Compute!—
    Excel label:       "ODC BB Gbps demand"
    Architecture ref:  §7.2
    Principle:         3 (canonical cross-tab labels)

    Formula: BB and DTC Gbps claim for Starlink Capacity.

    """
    fleet = _fleet_from_deployment(inputs.sats_deployed)
    bb_share = assumption_scalar(inputs.assumptions, cl.BB_SHARE_OF_ODC_BANDWIDTH_CLAIM)
    gbps = assumption_scalar(inputs.assumptions, cl.GBPS_PER_GWH_ODC_COMPUTE_ENERGY)
    compute_kw = assumption_scalar(inputs.assumptions, cl.COMPUTE_POWER_PER_SAT_KW)
    per_sat = gbps * compute_kw
    bb = fleet.values * per_sat * bb_share
    dtc = fleet.values * per_sat * (1.0 - bb_share)
    return YearVector(bb), YearVector(dtc)


def compute_orbital_revenue(inputs: OrbitalDcInputs) -> YearVector:
    """External orbital DC revenue from deployed fleet.

    Excel cell:        AI - Compute!—
    Excel label:       "Revenue: Orbital DC"
    Architecture ref:  §9 unified AI - Compute
    Principle:         8 (vending-machine module)

    Formula: External orbital DC revenue from deployed fleet.

    """
    deployed = inputs.sats_deployed or YearVector.zeros()
    external_share = YearVector.constant(0.05)
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        if deployed.values[t] <= 0:
            continue
        ext_rev = (
            per_sat_combined_revenue_mm(inputs.assumptions, t)
            * external_share.values[t]
        )
        values[t] = ext_rev * deployed.values[t]
    return YearVector(values)


def compute_orbital_cogs(inputs: OrbitalDcInputs) -> YearVector:
    """Orbital DC COGS — bandwidth at-cost + Terafab chip transfer (bucket 2).

    Excel cell:        AI - Compute!—
    Excel label:       "COGS: Orbital DC"
    Architecture ref:  §9.4 + U1 at-cost chip transfer
    Principle:         9 (predetermined at-cost transfer; fab not in growth CapEx)

    Formula: Orbital DC COGS — bandwidth at-cost + Terafab chip transfer (bucket 2).

    """
    deployed = inputs.sats_deployed or YearVector.zeros()
    chip = inputs.chip_at_cost_per_sat or YearVector.zeros()
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        if deployed.values[t] <= 0:
            continue
        bw = per_sat_bandwidth_cost_mm(inputs.assumptions, inputs.starlink_capacity, t)
        chip_mm = chip.values[t] / 1e6
        values[t] = (bw + chip_mm) * deployed.values[t]
    return YearVector(values)


def per_sat_blended_irr(inputs: OrbitalDcInputs) -> float:
    """Per-sat blended IRR — growth CapEx slug only; Terafab lump excluded (U1).

    Excel cell:        AI - Compute!—
    Excel label:       "Spot IRR: ODC"
    Architecture ref:  §9.4 + U1 three-bucket split
    Principle:         2 (per-unit marginal IRR; bucket-2 fab out of −CapEx leg)

    Formula: Per-sat blended IRR — growth CapEx slug only; Terafab lump excluded (U1).

    """
    a = inputs.assumptions
    mass = a.lookup_scalar(cl.V3_MASS_KG)
    slug_mm = derived_sat_unit_cost_mm(a, mass)
    subsystem = slug_mm * 0.5
    chip = (
        inputs.chip_at_cost_per_sat.at(2025) / 1e6
        if inputs.chip_at_cost_per_sat is not None
        else 0.0
    )
    cost = subsystem + chip
    if cost <= 0.0:
        cost = slug_mm
    n = int(assumption_scalar(a, cl.ODC_FLEET_DESIGN_LIFE_YEARS))
    rev = np.array(
        [
            per_sat_net_marginal_revenue_mm(a, inputs.starlink_capacity, t)
            for t in range(n)
        ],
        dtype=np.float64,
    )
    result = compute_irr_engine(cost, rev, horizon_n=n)
    return result.blended
