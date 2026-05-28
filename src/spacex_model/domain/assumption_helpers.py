"""Helpers for reading Assumptions year-vectors and scalars."""

from __future__ import annotations

import numpy as np

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


def assumption_scalar(assumptions: Assumptions, label: str, *, default: float | None = None) -> float:
    """Return scalar base-case value for an Assumptions label."""
    return assumptions.lookup_scalar(label, default=default)


def assumption_year_vector(
    assumptions: Assumptions,
    label: str,
    *,
    default: float = 0.0,
) -> YearVector:
    """Return length-26 YearVector from Assumptions year-row or scalar base."""
    row = assumptions.lookup(label)
    if row is None:
        return YearVector.constant(default)
    vec = row.as_year_vector()
    if row.base_case is not None and isinstance(row.base_case, (int, float)):
        for idx in range(HORIZON_YEARS):
            if vec[idx] == 0.0 and not row.year_values:
                vec[idx] = float(row.base_case)
    return YearVector(vec)


def wrights_law_cost(
    anchor_cost: float,
    cum_units: np.ndarray,
    anchor_cum_units: float,
    learning_rate: float,
) -> np.ndarray:
    """Wright's Law: cost = anchor × (cum / anchor_cum)^log₂(1 − lr)."""
    if anchor_cum_units <= 0:
        return np.full_like(cum_units, anchor_cost, dtype=np.float64)
    exponent = np.log2(1.0 - learning_rate) if learning_rate < 1.0 else 0.0
    ratio = np.maximum(cum_units / anchor_cum_units, 1e-12)
    return anchor_cost * np.power(ratio, exponent)


def year_chained_eoy(boy: np.ndarray, adds: np.ndarray, retires: np.ndarray) -> np.ndarray:
    """EoY stock = BoY + adds − retires with next-year BoY = prior EoY (Rule 23)."""
    eoy = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        boy_t = boy[t] if t == 0 else eoy[t - 1]
        eoy[t] = max(0.0, boy_t + adds[t] - retires[t])
    return eoy


def year_chained_boy_from_eoy(eoy: np.ndarray, *, initial_boy: float) -> np.ndarray:
    """BoY[t] = EoY[t-1]; BoY[0] = initial_boy."""
    boy = np.zeros(HORIZON_YEARS, dtype=np.float64)
    boy[0] = initial_boy
    for t in range(1, HORIZON_YEARS):
        boy[t] = eoy[t - 1]
    return boy


def year_offset(year: int) -> int:
    """Calendar year → horizon index."""
    return year - FIRST_YEAR


def bounded_cagr_pct_vector(
    start_pct: float,
    end_pct: float,
    cagr: float,
) -> np.ndarray:
    """Anchor-and-offset bounded CAGR year-row per Rule 23."""
    offsets = np.arange(HORIZON_YEARS, dtype=np.float64)
    anchor = start_pct
    raw = anchor * np.power(1.0 + cagr, offsets)
    if cagr >= 0:
        return np.minimum(end_pct, raw)
    return np.maximum(end_pct, raw)


def year_chained_cumulative(adds: np.ndarray, *, initial: float = 0.0) -> np.ndarray:
    """Cumulative running sum with optional BoY seed (Rule 23 exception)."""
    cumulative = np.zeros(HORIZON_YEARS, dtype=np.float64)
    running = initial
    for t in range(HORIZON_YEARS):
        running += adds[t]
        cumulative[t] = running
    return cumulative
