"""Cash BoY tracker per Architecture §6.1 + §2.13 pre-IPO bridge."""

from __future__ import annotations

import numpy as np

from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions
from spacex_model.inputs.s1_profiles import BRIDGE_DRAWDOWN_YEAR

_BRIDGE_LOAN_2025_MM = 20_000.0
_STARTING_CASH_MM = 11_385.0  # S-1 BS Dec 31, 2024 (audit P0-1)
_IPO_AMOUNT_MM = 30_000.0
_IPO_YEAR = 2027


def starting_cash_mm(assumptions: Assumptions) -> float:
    """Starting cash position EoY 2024 ($mm) for R109 identity.

    Excel cell:        Assumptions!B (Starting cash position EoY 2024)
    Excel label:       "Starting cash position EoY 2024 ($mm)"
    Architecture ref:  §6.1 + §15.2 R109
    Principle:         4 (cash pool feeds queue gate)

    """
    return assumption_scalar(
        assumptions,
        cl.STARTING_CASH_POSITION_EOY_2024_MM,
        default=_STARTING_CASH_MM,
    )


def _bridge_drawdown_year(assumptions: Assumptions) -> int:
    """Year of $20B pre-IPO bridge receipt — S-1 MDA §6.5 (P1-1: March 2026)."""
    return int(
        assumption_scalar(
            assumptions,
            cl.PRE_IPO_BRIDGE_DRAWDOWN_YEAR,
            default=float(BRIDGE_DRAWDOWN_YEAR),
        )
    )


def compute_bridge_drawdown(assumptions: Assumptions) -> YearVector:
    """Pre-IPO bridge loan drawdown by year ($mm); $20B in bridge year per §2.13.

    Excel cell:        Assumptions!B (Pre-IPO debt facility)
    Excel label:       "Pre-IPO debt facility ($mm)"
    Architecture ref:  §2.13 + §15.2 R109
    Principle:         4 (bridge inflow in cash pool tracker)

    """
    bridge = assumption_scalar(
        assumptions,
        cl.PRE_IPO_DEBT_FACILITY_MM,
        default=_BRIDGE_LOAN_2025_MM,
    )
    bridge_year = _bridge_drawdown_year(assumptions)
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    idx = bridge_year - FIRST_YEAR
    if 0 <= idx < HORIZON_YEARS:
        values[idx] = bridge
    return YearVector(values)


def compute_ipo_drawdown(assumptions: Assumptions) -> YearVector:
    """IPO injection by year ($mm).

    Excel cell:        Assumptions!B (IPO injection amount)
    Excel label:       "IPO injection amount ($mm)"
    Architecture ref:  §6.1 + §15.2 R109
    Principle:         4 (IPO inflow in cash pool tracker)

    """
    ipo_year = int(
        assumption_scalar(assumptions, cl.IPO_INJECTION_YEAR, default=float(_IPO_YEAR))
    )
    ipo_amount = assumption_scalar(
        assumptions,
        cl.IPO_INJECTION_AMOUNT_MM,
        default=_IPO_AMOUNT_MM,
    )
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        if year == ipo_year:
            values[t] = ipo_amount
    return YearVector(values)


def compute_cash_boy(
    assumptions: Assumptions,
    prior_year_group_fcf: YearVector | None = None,
) -> YearVector:
    """Year-chained Cash BoY with IPO and pre-IPO bridge inflows.

    Excel cell:        Allocator!D8:AC8
    Excel label:       "Cash BoY ($mm)"
    Architecture ref:  §6.1 + §2.13 (pre-IPO debt facility)
    Principle:         4 (cash pool feeds queue gate)

    Formula: Cash_BoY(N) = Cash_BoY(N−1) + Group_FCF(N−1) + IPO(N) + Pre_IPO_debt(N).
        Starting cash $11,385M EoY 2024 (S-1); bridge $20B in 2026 (P1-1); IPO $30B in 2027.

    """
    starting = starting_cash_mm(assumptions)
    ipo_year = int(
        assumption_scalar(assumptions, cl.IPO_INJECTION_YEAR, default=float(_IPO_YEAR))
    )
    ipo_amount = assumption_scalar(
        assumptions,
        cl.IPO_INJECTION_AMOUNT_MM,
        default=_IPO_AMOUNT_MM,
    )
    bridge = assumption_scalar(
        assumptions,
        cl.PRE_IPO_DEBT_FACILITY_MM,
        default=_BRIDGE_LOAN_2025_MM,
    )
    bridge_year = _bridge_drawdown_year(assumptions)

    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        ipo = ipo_amount if year == ipo_year else 0.0
        pre_ipo = bridge if year == bridge_year else 0.0
        if t == 0:
            values[t] = starting + pre_ipo + ipo
        else:
            prior_fcf = (
                prior_year_group_fcf.values[t - 1]
                if prior_year_group_fcf is not None
                else 0.0
            )
            values[t] = values[t - 1] + prior_fcf + ipo + pre_ipo
    return YearVector(values)
