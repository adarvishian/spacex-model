"""V2 historical fleet retirement — linear over useful life (Architecture §8.3)."""

from __future__ import annotations

import numpy as np

from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector


def historical_opening_balance_deorbit(
    baseline_sats: float,
    useful_life_years: float,
) -> YearVector:
    """Linear retirement of SoY 2025 historical fleet over N years.

    Excel cell:        Starlink!D52:D53
    Excel label:       "V2 BB historical retirement"
    Architecture ref:  §8.3
    Principle:         23 (anchor-and-offset; not year-chained cumulative)

    """
    rate = baseline_sats / useful_life_years if useful_life_years > 0 else 0.0
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    n = int(useful_life_years)
    for t in range(min(n, HORIZON_YEARS)):
        values[t] = rate
    return YearVector(values)


def launch_cohort_deorbit(
    launches: YearVector,
    *,
    useful_life_years: int,
) -> YearVector:
    """Retire launch cohorts after useful life (Rule 23 year-chained exception).

    Excel cell:        Starlink!D54:D57
    Excel label:       "V2 BB launch-cohort retirement"
    Architecture ref:  §8.3
    Principle:         23 (year-chained cumulative deorbit)

    """
    deorbit = np.zeros(HORIZON_YEARS, dtype=np.float64)
    lag = max(1, useful_life_years)
    for t in range(HORIZON_YEARS):
        src = t - lag
        if src >= 0:
            deorbit[t] = launches.values[src]
    return YearVector(deorbit)
