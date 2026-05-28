"""Bandwidth-driven BB/DTC revenue via Demand Curves + TAM shift."""

from __future__ import annotations

import numpy as np

from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions
from spacex_model.inputs.demand_curves import DemandCurves


def tam_shift_vector(assumptions: Assumptions) -> np.ndarray:
    """Annual TAM shift = (1 + inflation)^t × (1 + GNI)^t per Sprint 10.5.

    Excel cell:        Demand Curves!D141
    Excel label:       "Annual TAM shift multiplier"
    Architecture ref:  §8.4 / Sprint 10.5
    Principle:         12 (anchor-and-offset year exponent)

    """
    inflation = assumption_scalar(assumptions, "TAM inflation rate (annual)", default=0.025)
    gni = assumption_scalar(assumptions, "GNI per capita growth rate (annual)", default=0.03)
    offsets = np.arange(HORIZON_YEARS, dtype=np.float64)
    return np.power(1.0 + inflation, offsets) * np.power(1.0 + gni, offsets)


def compute_bb_revenue(
    available_bb_gbps: YearVector,
    *,
    assumptions: Assumptions,
    demand_curves: DemandCurves,
) -> YearVector:
    """BB revenue from piecewise-linear Demand Curves lookup × TAM shift.

    Excel cell:        Starlink!D120
    Excel label:       "BB Revenue ($mm)"
    Architecture ref:  §8.4
    Principle:         3 (bandwidth-driven revenue)

    """
    shifts = tam_shift_vector(assumptions)
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        values[t] = demand_curves.lookup_bb_revenue(
            available_bb_gbps.values[t], t, tam_shift=float(shifts[t])
        )
    return YearVector(values)


def compute_dtc_revenue(
    available_dtc_gbps: YearVector,
    *,
    assumptions: Assumptions,
    demand_curves: DemandCurves,
) -> YearVector:
    """DTC revenue from piecewise-linear Demand Curves lookup × TAM shift.

    Excel cell:        Starlink!D131
    Excel label:       "DTC Revenue ($mm)"
    Architecture ref:  §8.4
    Principle:         3 (bandwidth-driven revenue)

    """
    shifts = tam_shift_vector(assumptions)
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        values[t] = demand_curves.lookup_dtc_revenue(
            available_dtc_gbps.values[t], t, tam_shift=float(shifts[t])
        )
    return YearVector(values)
