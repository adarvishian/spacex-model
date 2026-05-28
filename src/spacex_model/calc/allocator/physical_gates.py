"""Physical gates — V2 phase-out, V3 startup, F9 supply (Architecture §20.2)."""

from __future__ import annotations

import numpy as np

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector


def apply_v2_phase_out_gate(
    values: YearVector,
    *,
    phase_out_year: int,
) -> YearVector:
    """Zero demand/allocation for years at or after V2 phase-out.

    Excel cell:        Allocator!— (Phase D)
    Excel label:       "V2 phase-out gate"
    Architecture ref:  §20.2 (V2 phase-out gate)
    Principle:         12 (exogenous demand masked by year gates)

    """
    masked = values.values.copy()
    for t in range(HORIZON_YEARS):
        if FIRST_YEAR + t >= phase_out_year:
            masked[t] = 0.0
    return YearVector(masked)


def apply_v3_startup_gate(
    values: YearVector,
    *,
    startup_year: int,
) -> YearVector:
    """Zero demand/allocation for years before V3 Starlink launch trigger.

    Excel cell:        Allocator!— (Phase D)
    Excel label:       "V3 startup gate"
    Architecture ref:  §20.2 (V3 startup gate)
    Principle:         12 (exogenous demand masked by year gates)

    """
    masked = values.values.copy()
    for t in range(HORIZON_YEARS):
        if FIRST_YEAR + t < startup_year:
            masked[t] = 0.0
    return YearVector(masked)


def apply_f9_supply_gate(
    launch_demand_sats: YearVector,
    f9_launches_available: YearVector,
    *,
    sats_per_f9_launch: float,
) -> YearVector:
    """Cap V2 launch demand by F9 internal capacity (sats per year).

    Excel cell:        Starlink!— (Phase D)
    Excel label:       "F9 supply gate (V2 launches)"
    Architecture ref:  §20.2 (F9 supply gate)
    Principle:         12 (physical supply binds V2 deployment)

    """
    if sats_per_f9_launch <= 0:
        return YearVector.zeros()
    cap_sats = f9_launches_available.values * sats_per_f9_launch
    capped = np.minimum(launch_demand_sats.values, cap_sats)
    return YearVector(capped)
