"""Compute at-cost transfer pricing per Architecture §7.3."""

from __future__ import annotations

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.odc.module import OdcInputs, per_sat_bandwidth_cost_mm, per_sat_combined_revenue_mm
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.year_vector import YearVector


def _module_out(outputs: dict[str, AllocatorOut], key: str) -> AllocatorOut:
    return outputs.get(key, AllocatorOut.zeros())


def _fleet_pflop_hrs(inputs: OdcInputs) -> YearVector:
    """Fleet annual PFLOP-hrs delivered (util-adjusted) from deployed sats."""
    deployed = inputs.sats_deployed or YearVector.zeros()
    compute_kw = assumption_scalar(inputs.assumptions, "Compute power per sat (kW)", default=140.0)
    chip_tdp = assumption_year_vector(inputs.assumptions, "Chip TDP per chip (W) — year-row", default=700.0)
    chip_fp8 = assumption_year_vector(
        inputs.assumptions, "Chip FP8 performance per chip (TFLOPS) — year-row", default=1979.0
    )
    util = assumption_scalar(inputs.assumptions, "ODC utilization factor", default=0.85)
    ecr = assumption_scalar(inputs.assumptions, "Effective Compute Ratio (ECR)", default=0.6)

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


def _fully_allocated_annual_cost_mm(inputs: OdcInputs) -> YearVector:
    """ODC fully-allocated annual cost = sat D&A + launch + bandwidth + insurance + other COGS."""
    deployed = inputs.sats_deployed or YearVector.zeros()
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        count = deployed.values[t]
        if count <= 0:
            continue
        combined_rev = per_sat_combined_revenue_mm(inputs.assumptions, t)
        ground = assumption_scalar(inputs.assumptions, "ODC ground ops % of revenue", default=0.05)
        insurance = assumption_scalar(inputs.assumptions, "ODC insurance % of revenue", default=0.01)
        other = assumption_scalar(inputs.assumptions, "ODC other COGS % of revenue", default=0.03)
        opex = combined_rev * (ground + insurance + other)
        bandwidth = per_sat_bandwidth_cost_mm(inputs.assumptions, inputs.starlink_capacity, t)
        values[t] = count * (opex + bandwidth)
    return YearVector(values)


def rate_per_unit(inputs: OdcInputs) -> YearVector:
    """Fully-allocated at-cost compute rate ($/PFLOP-hr).

    Excel cell:        ODC!— (Architecture §7.3)
    Excel label:       "ODC at-cost compute rate ($/PFLOP-hr)"
    Architecture ref:  §7.3 (fully-allocated compute transfer)
    Principle:         9 (internal transfers at fully-allocated cost)

    """
    cost = _fully_allocated_annual_cost_mm(inputs).values
    hours = _fleet_pflop_hrs(inputs).values
    rate = np.nan_to_num(np.where(hours > 0, cost * 1e6 / np.maximum(hours, 1e-12), 0.0))
    return YearVector(rate)


def internal_transfer_revenue(
    inputs: OdcInputs,
    *,
    internal_pflop_hrs: YearVector | None = None,
) -> YearVector:
    """ODC internal compute transfer revenue = internal PFLOP-hrs × at-cost rate.

    Excel cell:        ODC!— (internal transfer revenue)
    Excel label:       "Internal transfer revenue (at-cost compute) ($mm)"
    Architecture ref:  §7.3
    Principle:         9 (source books internal transfer revenue)

    """
    rate = rate_per_unit(inputs)
    if internal_pflop_hrs is None:
        fleet_hrs = _fleet_pflop_hrs(inputs)
        internal_share = assumption_year_vector(
            inputs.assumptions,
            "ODC external compute share to customers % — year-row",
            default=0.05,
        )
        internal_pflop_hrs = YearVector(fleet_hrs.values * (1.0 - internal_share.values))
    values = internal_pflop_hrs.values * rate.values / 1e6
    return YearVector(values)


def conservation_residual(
    internal_transfer_revenue_vec: YearVector,
    consumer_internal_compute_cost: YearVector,
) -> YearVector:
    """R107 conservation: source rev − AI Stack internal compute COGS.

    Excel cell:        Group P&L!R107
    Excel label:       "Compute elimination check"
    Architecture ref:  §15 conservation block
    Principle:         9 (internal flow conservation)

    """
    return YearVector(
        internal_transfer_revenue_vec.values - consumer_internal_compute_cost.values
    )
