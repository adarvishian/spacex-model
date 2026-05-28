"""Valuation — Phase C stub: implied EV 2025 = 10× group revenue per PRD §5.5."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.calc.group_pnl import GroupPnlResult
from spacex_model.config.constants import FIRST_YEAR
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class ValuationInputs:
    """Inputs for Valuation stub — Group P&L + Assumptions §11."""

    assumptions: Assumptions
    group_pnl: GroupPnlResult
    revenue_multiple: float = 10.0


@dataclass(frozen=True, slots=True)
class ValuationResult:
    """Valuation stub outputs (full DCF lands in Phase D)."""

    implied_ev_by_year: YearVector
    implied_ev_2025_billions: float
    group_wacc: float
    terminal_growth: float


def compute_implied_ev_multiple(
    group_revenue_net: YearVector,
    *,
    multiple: float = 10.0,
) -> YearVector:
    """Implied EV = revenue multiple × Group Revenue net of eliminations.

    Excel cell:        Valuation!— (Phase C stub)
    Excel label:       "Implied EV (10× rev cross-check)"
    Architecture ref:  §14.3 SoTP multiples / PRD §5.5 calibration
    Principle:         3 (canonical valuation cross-check)

    """
    return YearVector(multiple * group_revenue_net.values)


def compute_valuation(inputs: ValuationInputs) -> ValuationResult:
    """Valuation stub — implied EV 2025 = 10× Group Revenue ($146.5B target).

    Excel cell:        Valuation!— (Phase C stub)
    Excel label:       "VALUATION -- DCF off Group FCF + Sum-of-parts ..."
    Architecture ref:  §14 Valuation tab (stub)
    Principle:         3 (EV cross-check against group revenue)

    Full Group DCF, SoTP, comparables, and sensitivity land in Phase D after
    Allocator closes the iterative loop.
    """
    wacc = inputs.assumptions.lookup_scalar("Group WACC", default=0.10)
    terminal_g = inputs.assumptions.lookup_scalar(
        "Terminal growth rate g (group + most modules)",
        default=0.025,
    )
    implied = compute_implied_ev_multiple(
        inputs.group_pnl.group_revenue_net,
        multiple=inputs.revenue_multiple,
    )
    ev_2025_mm = float(implied.at(FIRST_YEAR))
    ev_2025_b = ev_2025_mm / 1000.0

    return ValuationResult(
        implied_ev_by_year=implied,
        implied_ev_2025_billions=ev_2025_b,
        group_wacc=wacc,
        terminal_growth=terminal_g,
    )
