"""Launch services at-cost transfer pricing per Architecture §7.1."""

from __future__ import annotations

from spacex_model.calc.launch_capacity import LaunchCapacityResult
from spacex_model.domain.year_vector import YearVector


def at_cost_launch_services_rate(
    launch_capacity: LaunchCapacityResult,
    *,
    vehicle: str = "f9",
) -> YearVector:
    """Fully-allocated at-cost launch services rate ($mm/launch).

    Excel cell:        Launch Capacity!D71 / D40
    Excel label:       "At-cost launch services rate ($mm/launch)"
    Architecture ref:  §7.1 (fully-allocated launch transfer)
    Principle:         9 (internal transfers at fully-allocated cost)

    """
    if vehicle == "starship":
        return launch_capacity.starship_at_cost_rate
    return launch_capacity.f9_at_cost_rate


def internal_transfer_revenue(
    f9_internal_launches: YearVector,
    starship_internal_launches: YearVector,
    launch_capacity: LaunchCapacityResult,
) -> YearVector:
    """Customer Launch internal transfer revenue = Σ internal launches × at-cost rate.

    Excel cell:        Customer Launch!D70
    Excel label:       "Customer Launch internal transfer revenue ($mm)"
    Architecture ref:  §7.1
    Principle:         9 (source books internal transfer revenue)

    """
    f9_rate = launch_capacity.f9_at_cost_rate.values
    ship_rate = launch_capacity.starship_at_cost_rate.values
    rev = (
        f9_internal_launches.values * f9_rate
        + starship_internal_launches.values * ship_rate
    )
    return YearVector(rev)


def conservation_residual(
    internal_transfer_revenue_vec: YearVector,
    consumer_launch_services_cost: YearVector,
) -> YearVector:
    """R105 conservation: source rev − Σ consumer COGS.

    Excel cell:        Group P&L!R105
    Excel label:       "Launch services elimination check"
    Architecture ref:  §15 conservation block
    Principle:         9 (internal flow conservation)

    """
    return YearVector(internal_transfer_revenue_vec.values - consumer_launch_services_cost.values)
