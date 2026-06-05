"""Orbital DC (ODC) sub-module — dual-revenue slice within AI - Compute tab."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc.starlink_capacity import StarlinkCapacityResult
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.irr import compute_irr_engine
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class OrbitalDcInputs:
    """Inputs for Orbital DC within unified AI - Compute module."""

    assumptions: Assumptions
    starlink_capacity: StarlinkCapacityResult | None = None
    sats_deployed: YearVector | None = None


def _per_sat_model_a_revenue_mm(assumptions: Assumptions, year_index: int) -> float:
    compute_kw = assumption_scalar(assumptions, cl.COMPUTE_POWER_PER_SAT_KW, default=140.0)
    coreweave = assumption_year_vector(assumptions, cl.COREWEAVE_BASELINE_ANCHOR_YEAR_ROW, default=12.0)
    pue_uplift = assumption_scalar(assumptions, cl.ORBITAL_PUE_UPLIFT_VS_TERRESTRIAL, default=1.12 / 1.4)
    util = assumption_scalar(assumptions, cl.ODC_UTILIZATION_FACTOR, default=0.85)
    gw = compute_kw / 1e6
    baseline = coreweave.values[year_index] if year_index < HORIZON_YEARS else coreweave.at(FIRST_YEAR)
    return gw * baseline * pue_uplift * util * 1000.0


def _per_sat_model_b_revenue_mm(assumptions: Assumptions, year_index: int) -> float:
    compute_kw = assumption_scalar(assumptions, cl.COMPUTE_POWER_PER_SAT_KW, default=140.0)
    chip_tdp = assumption_year_vector(assumptions, cl.CHIP_TDP_PER_CHIP_W_YEAR_ROW, default=700.0)
    chip_fp8 = assumption_year_vector(
        assumptions, cl.CHIP_FP8_PERFORMANCE_TFLOPS_YEAR_ROW, default=1979.0
    )
    util = assumption_scalar(assumptions, cl.ODC_UTILIZATION_FACTOR, default=0.85)
    ecr = assumption_scalar(assumptions, cl.EFFECTIVE_COMPUTE_RATIO_RATIO, default=0.6)
    mix = assumption_scalar(assumptions, cl.WORKLOAD_MIX_INFERENCE_SHARE, default=0.85)
    price_gpu_hr = assumption_year_vector(assumptions, cl.PRICE_PER_H100_GPU_HR_YEAR_ROW, default=2.0)

    tdp = chip_tdp.values[year_index]
    fp8 = chip_fp8.values[year_index]
    if tdp <= 0:
        return 0.0
    price = price_gpu_hr.values[year_index]
    billable = (compute_kw * 1000.0 / tdp) * fp8 / 1e6 * 8760.0 * util * ecr * mix * price / 1e6
    return billable


def per_sat_combined_revenue_mm(assumptions: Assumptions, year_index: int) -> float:
    """Credence-weighted Model A/B per-sat revenue ($mm/yr).

    Excel cell:        AI - Compute!—
    Excel label:       "Per-sat combined revenue ($mm/yr)"
    Architecture ref:  §9.2 dual revenue
    Principle:         8 (vending-machine module)

    """
    pr_a = assumption_scalar(assumptions, cl.CREDENCE_ON_MODEL_A_PR_A, default=0.6)
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

    """
    if starlink_capacity is None:
        return 0.0
    bb_share = assumption_scalar(assumptions, cl.BB_SHARE_OF_ODC_BANDWIDTH_CLAIM, default=0.5)
    gbps_per_gwh = assumption_scalar(assumptions, cl.GBPS_PER_GWH_ODC_COMPUTE_ENERGY, default=0.05)
    compute_kw = assumption_scalar(assumptions, cl.COMPUTE_POWER_PER_SAT_KW, default=140.0)
    gbps_per_sat = gbps_per_gwh * compute_kw
    bb_rate = starlink_capacity.bb_at_cost_rate_per_gbps.values[year_index] / 1e6
    dtc_rate = starlink_capacity.dtc_at_cost_rate_per_gbps.values[year_index] / 1e6
    return bb_share * gbps_per_sat * bb_rate + (1.0 - bb_share) * gbps_per_sat * dtc_rate


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

    """
    combined = per_sat_combined_revenue_mm(assumptions, year_index)
    ground = assumption_scalar(assumptions, cl.ODC_GROUND_OPS_PCT_REV, default=0.05)
    insurance = assumption_scalar(assumptions, cl.ODC_INSURANCE_PCT_REV, default=0.01)
    other = assumption_scalar(assumptions, cl.ODC_OTHER_COGS_PCT_REV, default=0.03)
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

    """
    fleet = _fleet_from_deployment(inputs.sats_deployed)
    bb_share = assumption_scalar(inputs.assumptions, cl.BB_SHARE_OF_ODC_BANDWIDTH_CLAIM, default=0.5)
    gbps = assumption_scalar(inputs.assumptions, cl.GBPS_PER_GWH_ODC_COMPUTE_ENERGY, default=0.05)
    compute_kw = assumption_scalar(inputs.assumptions, cl.COMPUTE_POWER_PER_SAT_KW, default=140.0)
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

    """
    deployed = inputs.sats_deployed or YearVector.zeros()
    external_share = assumption_year_vector(
        inputs.assumptions, cl.ODC_EXTERNAL_COMPUTE_SHARE_CUSTOMERS_YEAR_ROW, default=0.05
    )
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        if deployed.values[t] <= 0:
            continue
        ext_rev = per_sat_combined_revenue_mm(inputs.assumptions, t) * external_share.values[t]
        values[t] = ext_rev * deployed.values[t]
    return YearVector(values)


def compute_orbital_cogs(inputs: OrbitalDcInputs) -> YearVector:
    """Orbital DC bandwidth COGS from at-cost internal transfers.

    Excel cell:        AI - Compute!—
    Excel label:       "COGS: Orbital DC"
    Architecture ref:  §9.4
    Principle:         9 (at-cost internal bandwidth)

    """
    deployed = inputs.sats_deployed or YearVector.zeros()
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        if deployed.values[t] <= 0:
            continue
        bw = per_sat_bandwidth_cost_mm(inputs.assumptions, inputs.starlink_capacity, t)
        values[t] = bw * deployed.values[t]
    return YearVector(values)


def per_sat_blended_irr(inputs: OrbitalDcInputs) -> float:
    """Per-sat blended IRR for Orbital DC spot signal.

    Excel cell:        AI - Compute!—
    Excel label:       "Spot IRR: ODC"
    Architecture ref:  §9.4
    Principle:         2 (per-unit marginal IRR)

    """
    a = inputs.assumptions
    cost = assumption_scalar(a, cl.V3_BB_SAT_UNIT_COST_MM_SAT, default=50.0)
    n = int(assumption_scalar(a, cl.ODC_FLEET_DESIGN_LIFE_YEARS, default=5.0))
    rev = np.array(
        [per_sat_net_marginal_revenue_mm(a, inputs.starlink_capacity, t) for t in range(n)],
        dtype=np.float64,
    )
    result = compute_irr_engine(cost, rev, horizon_n=n)
    return result.blended
