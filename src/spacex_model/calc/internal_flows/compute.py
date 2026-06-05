"""Compute at-cost transfer pricing per Architecture §7.3."""

from __future__ import annotations

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.ai_compute.module import AiComputeInputs
from spacex_model.calc.ai_compute.orbital_dc import (
    per_sat_bandwidth_cost_mm,
    per_sat_combined_revenue_mm,
)
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.year_vector import YearVector


def _module_out(outputs: dict[str, AllocatorOut], key: str) -> AllocatorOut:
    return outputs.get(key, AllocatorOut.zeros())


def _fleet_pflop_hrs(inputs: AiComputeInputs) -> YearVector:
    deployed = inputs.sats_deployed or YearVector.zeros()
    compute_kw = assumption_scalar(inputs.assumptions, cl.COMPUTE_POWER_PER_SAT_KW, default=140.0)
    chip_tdp = assumption_year_vector(inputs.assumptions, cl.CHIP_TDP_PER_CHIP_W_YEAR_ROW, default=700.0)
    chip_fp8 = assumption_year_vector(
        inputs.assumptions, cl.CHIP_FP8_PERFORMANCE_TFLOPS_YEAR_ROW, default=1979.0
    )
    util = assumption_scalar(inputs.assumptions, cl.ODC_UTILIZATION_FACTOR, default=0.85)
    ecr = assumption_scalar(inputs.assumptions, cl.EFFECTIVE_COMPUTE_RATIO_RATIO, default=0.6)

    fleet = np.zeros(HORIZON_YEARS, dtype=np.float64)
    active = 0.0
    for t in range(HORIZON_YEARS):
        active += deployed.values[t]
        fleet[t] = active

    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        if fleet[t] <= 0:
            continue
        tdp = chip_tdp.values[t]
        fp8 = chip_fp8.values[t]
        if tdp <= 0:
            continue
        pflops = (compute_kw * 1000.0 / tdp) * fp8 / 1e6 * fleet[t]
        values[t] = pflops * 8760.0 * util * ecr
    return YearVector(values)


def _fully_allocated_annual_cost_mm(inputs: AiComputeInputs) -> YearVector:
    deployed = inputs.sats_deployed or YearVector.zeros()
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        count = deployed.values[t]
        if count <= 0:
            continue
        combined_rev = per_sat_combined_revenue_mm(inputs.assumptions, t)
        ground = assumption_scalar(inputs.assumptions, cl.ODC_GROUND_OPS_PCT_REV, default=0.05)
        insurance = assumption_scalar(inputs.assumptions, cl.ODC_INSURANCE_PCT_REV, default=0.01)
        other = assumption_scalar(inputs.assumptions, cl.ODC_OTHER_COGS_PCT_REV, default=0.03)
        opex = combined_rev * (ground + insurance + other)
        bandwidth = per_sat_bandwidth_cost_mm(inputs.assumptions, inputs.starlink_capacity, t)
        values[t] = count * (opex + bandwidth)
    return YearVector(values)


def rate_per_unit(inputs: AiComputeInputs) -> YearVector:
    """Fully-allocated at-cost compute rate ($/PFLOP-hr).
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    cost = _fully_allocated_annual_cost_mm(inputs).values
    hours = _fleet_pflop_hrs(inputs).values
    rate = np.nan_to_num(np.where(hours > 0, cost * 1e6 / np.maximum(hours, 1e-12), 0.0))
    return YearVector(rate)


def internal_transfer_revenue(
    inputs: AiComputeInputs,
    *,
    internal_pflop_hrs: YearVector | None = None,
) -> YearVector:
    """ODC internal compute transfer revenue = internal PFLOP-hrs × at-cost rate.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    rate = rate_per_unit(inputs)
    if internal_pflop_hrs is None:
        fleet_hrs = _fleet_pflop_hrs(inputs)
        internal_share = assumption_year_vector(
            inputs.assumptions,
            cl.ODC_EXTERNAL_COMPUTE_SHARE_CUSTOMERS_YEAR_ROW,
            default=0.05,
        )
        internal_pflop_hrs = YearVector(fleet_hrs.values * (1.0 - internal_share.values))
    values = internal_pflop_hrs.values * rate.values / 1e6
    return YearVector(values)


def conservation_residual(
    internal_transfer_revenue_vec: YearVector,
    consumer_internal_compute_cost: YearVector,
) -> YearVector:
    """Compute elimination check — source rev − consumer COGS.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    return YearVector(
        internal_transfer_revenue_vec.values - consumer_internal_compute_cost.values
    )
