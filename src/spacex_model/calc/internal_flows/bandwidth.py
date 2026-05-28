"""Bandwidth at-cost transfer pricing per Architecture §7.2."""

from __future__ import annotations

from spacex_model.calc.starlink_capacity import StarlinkCapacityResult
from spacex_model.domain.year_vector import YearVector


def rate_per_unit(
    starlink_capacity: StarlinkCapacityResult,
    *,
    pool: str = "bb",
) -> YearVector:
    """Fully-allocated at-cost bandwidth rate ($/Gbps/yr).

    Excel cell:        Starlink Capacity!D11 / D40
    Excel label:       "BB pool at-cost rate ($/Gbps/yr)"
    Architecture ref:  §7.2 (fully-allocated bandwidth transfer)
    Principle:         9 (internal transfers at fully-allocated cost)

    """
    if pool == "dtc":
        return starlink_capacity.dtc_at_cost_rate_per_gbps
    return starlink_capacity.bb_at_cost_rate_per_gbps


def internal_transfer_revenue(
    bb_gbps_claim: YearVector,
    dtc_gbps_claim: YearVector,
    starlink_capacity: StarlinkCapacityResult,
) -> YearVector:
    """Starlink internal bandwidth revenue = Σ ODC Gbps claim × pool at-cost rate.

    Excel cell:        Starlink!D143
    Excel label:       "Starlink internal bandwidth revenue ($mm)"
    Architecture ref:  §7.2
    Principle:         9 (source books internal transfer revenue)

    """
    values = (
        bb_gbps_claim.values * starlink_capacity.bb_at_cost_rate_per_gbps.values / 1e6
        + dtc_gbps_claim.values * starlink_capacity.dtc_at_cost_rate_per_gbps.values / 1e6
    )
    return YearVector(values)


def conservation_residual(
    internal_transfer_revenue_vec: YearVector,
    consumer_bandwidth_services_cost: YearVector,
) -> YearVector:
    """R106 conservation: source rev − ODC bandwidth services COGS.

    Excel cell:        Group P&L!R106
    Excel label:       "Bandwidth elimination check"
    Architecture ref:  §15 conservation block
    Principle:         9 (internal flow conservation)

    """
    return YearVector(
        internal_transfer_revenue_vec.values - consumer_bandwidth_services_cost.values
    )
