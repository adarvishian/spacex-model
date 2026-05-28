"""Mars carve-out — prior-year Group FCF × pct with floor (Architecture §11.1)."""

from __future__ import annotations

import numpy as np

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


def compute_mars_carveout(
    assumptions: Assumptions,
    prior_year_group_fcf: YearVector | None = None,
) -> YearVector:
    """Mars carve-out = MAX(floor, prior-year Group FCF × Mars pct).

    Excel cell:        Allocator!— (Phase C)
    Excel label:       "Mars carve-out ($mm)"
    Architecture ref:  §11.1 / §6.2
    Principle:         22 (Mars carve-out off-the-top)

    """
    pct = assumption_scalar(assumptions, "Mars carve-out % of prior-year Group FCF", default=0.15)
    floor = assumption_scalar(assumptions, "Mars carve-out floor ($mm/yr)", default=1000.0)
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        if year == FIRST_YEAR:
            values[t] = floor
        elif prior_year_group_fcf is not None:
            values[t] = max(floor, prior_year_group_fcf.values[t - 1] * pct)
        else:
            values[t] = floor
    return YearVector(values)
