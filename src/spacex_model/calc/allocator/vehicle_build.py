"""Vehicle build claim — forward-aggregate kg demand sized (Architecture §6.6)."""

from __future__ import annotations

import numpy as np

from spacex_model.calc.launch_capacity import LaunchCapacityResult
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


def _forward_at(values: np.ndarray, t: int, lead: int) -> float:
    idx = t + lead
    if idx >= HORIZON_YEARS:
        return 0.0
    return float(values[idx])


def compute_vehicle_build_claim(
    assumptions: Assumptions,
    forward_kg_demands: dict[str, YearVector],
    launch_capacity: LaunchCapacityResult,
    *,
    lead_time: int = 2,
) -> YearVector:
    """Non-module Starship build cash claim sized at T+lead aggregate kg gap.

    Excel cell:        Allocator!D150:AC150
    Excel label:       "Vehicle build claim ($mm)"
    Architecture ref:  §6.6 (forward-aggregate kg demand)
    Principle:         8 (vehicle build at queue gate, not module CapEx)

    """
    lead = int(
        assumption_scalar(
            assumptions,
            cl.VEHICLE_BUILD_LEAD_TIME_YEARS,
            default=float(lead_time),
        )
    )
    launches_per_vehicle = assumption_scalar(
        assumptions,
        cl.LAUNCHES_PER_STARSHIP_VEHICLE_PER_YEAR_CADENCE_VARIANT_BLEND_USED_FOR_SIZING,
        default=24.0,
    )

    capacity_kg = launch_capacity.total_annual_capacity_kg.values
    per_launch_upmass = launch_capacity.per_launch_upmass_kg.values
    blended_vehicle_cost = launch_capacity.blended_cost_per_starship_vehicle.values

    claim = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        forward_demand = sum(
            _forward_at(vec.values, t, lead) for vec in forward_kg_demands.values()
        )
        projected_capacity = _forward_at(capacity_kg, t, lead)
        gap = max(0.0, forward_demand - projected_capacity)
        payload = per_launch_upmass[t]
        if payload <= 0.0 or launches_per_vehicle <= 0.0:
            continue
        required_launches = gap / payload
        required_vehicles = required_launches / launches_per_vehicle
        claim[t] = required_vehicles * blended_vehicle_cost[t]
    return YearVector(claim)
