"""Lunar Mars deployment — ships from carve-out cash (Architecture §11)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import (
    assumption_scalar,
    assumption_year_vector,
)
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class DeploymentResult:
    """Surface ships, payload, and kg reserved off-the-top."""

    lunar_ships: YearVector
    mars_ships: YearVector
    lunar_surface_payload_kg: YearVector
    mars_surface_payload_kg: YearVector
    lunar_mission_capex_mm: YearVector
    mars_mission_capex_mm: YearVector
    capacity_demand_kg: YearVector


def compute_deployment(
    assumptions: Assumptions, carveout_cash_mm: YearVector
) -> DeploymentResult:
    """Deploy Lunar/Mars ships from carve-out cash shares; zero before first mission year.

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "Lunar ships deployed"
    Architecture ref:  §11 deployment
    Principle:         22 (carve-out cash deployment)

    Formula: Deploy Lunar/Mars ships from carve-out cash shares; zero before first mission year.

    """
    first_mission = int(
        assumption_scalar(assumptions, cl.FIRST_MISSION_YEAR_LUNAR_MARS)
    )
    lunar_share = assumption_year_vector(
        assumptions, cl.LUNAR_SHARE_OF_MARS_MOON_CARVE_OUT_CASH_YEAR_ROW, default=1.0
    )
    mars_share = assumption_year_vector(
        assumptions, cl.MARS_SHARE_OF_CARVE_OUT_CASH_YEAR_ROW, default=0.0
    )
    lunar_payload = assumption_scalar(
        assumptions, cl.LUNAR_PAYLOAD_PER_SURFACE_LANDED_STARSHIP_KG
    )
    mars_payload = assumption_scalar(
        assumptions, cl.MARS_PAYLOAD_PER_SURFACE_LANDED_STARSHIP_KG
    )
    lunar_depot = assumption_scalar(
        assumptions, cl.LUNAR_FUEL_DEPOT_MULTIPLIER_PER_OUTBOUND_STARSHIP
    )
    mars_depot = assumption_scalar(
        assumptions, cl.MARS_FUEL_DEPOT_MULTIPLIER_PER_OUTBOUND_STARSHIP
    )
    ship_cost = 100.0
    leo_payload = assumption_scalar(
        assumptions, cl.PAYLOAD_FULLY_REUSABLE_MODE_KG_TO_LEO
    )

    lunar_ships = np.zeros(HORIZON_YEARS, dtype=np.float64)
    mars_ships = np.zeros(HORIZON_YEARS, dtype=np.float64)
    lunar_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)
    mars_capex = np.zeros(HORIZON_YEARS, dtype=np.float64)

    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        if year < first_mission:
            continue
        lunar_cash = carveout_cash_mm.values[t] * lunar_share.values[t]
        mars_cash = carveout_cash_mm.values[t] * mars_share.values[t]
        if ship_cost > 0:
            lunar_ships[t] = lunar_cash / ship_cost
            mars_ships[t] = mars_cash / ship_cost
        lunar_capex[t] = lunar_cash
        mars_capex[t] = mars_cash

    lunar_surface = lunar_ships / (1.0 + lunar_depot)
    mars_surface = mars_ships / (1.0 + mars_depot)
    lunar_payload_kg = lunar_surface * lunar_payload
    mars_payload_kg = mars_surface * mars_payload
    kg_demand = (
        lunar_ships * (1.0 + lunar_depot) + mars_ships * (1.0 + mars_depot)
    ) * leo_payload

    return DeploymentResult(
        lunar_ships=YearVector(lunar_ships),
        mars_ships=YearVector(mars_ships),
        lunar_surface_payload_kg=YearVector(lunar_payload_kg),
        mars_surface_payload_kg=YearVector(mars_payload_kg),
        lunar_mission_capex_mm=YearVector(lunar_capex),
        mars_mission_capex_mm=YearVector(mars_capex),
        capacity_demand_kg=YearVector(kg_demand),
    )
