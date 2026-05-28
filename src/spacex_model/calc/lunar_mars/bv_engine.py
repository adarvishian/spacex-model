"""Lunar Mars BV engine — accumulated book value memos (Architecture §11)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class BvEngineResult:
    """Accumulated book value and memo decay rows."""

    lunar_accumulated_bv_mm: YearVector
    mars_accumulated_bv_mm: YearVector
    lunar_bv_decay_mm: YearVector
    mars_bv_decay_mm: YearVector
    module_da_mm: YearVector


def compute_bv_engine(
    assumptions: Assumptions,
    *,
    lunar_surface_payload_kg: YearVector,
    mars_surface_payload_kg: YearVector,
    lunar_mission_capex_mm: YearVector,
    mars_mission_capex_mm: YearVector,
) -> BvEngineResult:
    """Accumulated BV from labour output + hardware value add; memo decay for Valuation.

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "Lunar Accumulated Book Value ($mm)"
    Architecture ref:  §11 BV engine
    Principle:         8 (BV decay memo-only, not Group D&A)

    """
    capital_life = assumption_scalar(
        assumptions, "Capital lifetime — book value straight-line depreciation (years)", default=10.0
    )
    labour_mass = assumption_scalar(assumptions, "Labour unit mass (kg)", default=60.0)
    labour_output = assumption_scalar(
        assumptions, "Labour unit base hourly output ($/hr; burdened $22/0.7)", default=31.43
    )
    daily_hours = assumption_scalar(assumptions, "Labour unit daily working hours", default=22.0)
    prod_factor = assumption_scalar(assumptions, "Labour unit productivity factor vs human baseline", default=1.0)
    prod_lr = assumption_scalar(assumptions, "Labour unit productivity learning rate (%/yr)", default=0.05)
    hardware_cost = assumption_year_vector(
        assumptions, "Hardware replacement cost factor ($/kg landed) — declining", default=1000.0
    )
    lunar_labour_share = assumption_year_vector(
        assumptions, "Lunar labour share of surface payload — year-row", default=0.3
    )
    mars_labour_share = assumption_year_vector(
        assumptions, "Mars labour share of surface payload — year-row", default=0.3
    )

    lunar_bv = np.zeros(HORIZON_YEARS, dtype=np.float64)
    mars_bv = np.zeros(HORIZON_YEARS, dtype=np.float64)
    lunar_decay = np.zeros(HORIZON_YEARS, dtype=np.float64)
    mars_decay = np.zeros(HORIZON_YEARS, dtype=np.float64)
    active_lunar_labour = 0.0
    active_mars_labour = 0.0

    for t in range(HORIZON_YEARS):
        prod_mult = prod_factor * np.power(1.0 + prod_lr, t)
        annual_labour_output = labour_output * daily_hours * 365.0 * prod_mult / 1000.0

        lunar_labour_kg = lunar_surface_payload_kg.values[t] * lunar_labour_share.values[t]
        mars_labour_kg = mars_surface_payload_kg.values[t] * mars_labour_share.values[t]
        active_lunar_labour += lunar_labour_kg / labour_mass if labour_mass > 0 else 0.0
        active_mars_labour += mars_labour_kg / labour_mass if labour_mass > 0 else 0.0

        lunar_hw_kg = lunar_surface_payload_kg.values[t] * (1.0 - lunar_labour_share.values[t])
        mars_hw_kg = mars_surface_payload_kg.values[t] * (1.0 - mars_labour_share.values[t])
        hw_cost = hardware_cost.values[t]

        lunar_contrib = active_lunar_labour * annual_labour_output + lunar_hw_kg * hw_cost / 1000.0
        mars_contrib = active_mars_labour * annual_labour_output + mars_hw_kg * hw_cost / 1000.0

        if t == 0:
            lunar_bv[t] = lunar_contrib
            mars_bv[t] = mars_contrib
        else:
            decay_factor = 1.0 - 1.0 / capital_life if capital_life > 0 else 0.0
            lunar_bv[t] = lunar_contrib + lunar_bv[t - 1] * decay_factor
            mars_bv[t] = mars_contrib + mars_bv[t - 1] * decay_factor

        lunar_decay[t] = lunar_bv[t] / capital_life if capital_life > 0 else 0.0
        mars_decay[t] = mars_bv[t] / capital_life if capital_life > 0 else 0.0

    cumulative_capex = lunar_mission_capex_mm.values + mars_mission_capex_mm.values
    running = np.zeros(HORIZON_YEARS, dtype=np.float64)
    total = 0.0
    for t in range(HORIZON_YEARS):
        total += cumulative_capex[t]
        running[t] = total
    module_da = running / capital_life if capital_life > 0 else np.zeros(HORIZON_YEARS)

    return BvEngineResult(
        lunar_accumulated_bv_mm=YearVector(lunar_bv),
        mars_accumulated_bv_mm=YearVector(mars_bv),
        lunar_bv_decay_mm=YearVector(lunar_decay),
        mars_bv_decay_mm=YearVector(mars_decay),
        module_da_mm=YearVector(module_da),
    )
