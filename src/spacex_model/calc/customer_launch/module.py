"""Customer Launch module — vending-machine P&L (Phase C).

Architecture §4 Customer Launch / PRD §4.2.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc._vending_machine import build_allocator_out
from spacex_model.calc.internal_flows.launch_services import internal_transfer_revenue
from spacex_model.calc.launch_capacity import LaunchCapacityResult
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.inputs.s1_profiles import f9_customer_launches_per_year, starship_customer_launches_per_year
from spacex_model.domain.irr import compute_irr_engine
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class CustomerLaunchInputs:
    """Upstream inputs for Customer Launch."""

    assumptions: Assumptions
    launch_capacity: LaunchCapacityResult
    f9_internal_launches: YearVector | None = None
    starship_internal_launches: YearVector | None = None
    starship_customer_launches: YearVector | None = None


def f9_effective_dep_lifetime(assumptions: Assumptions) -> float:
    """F9 booster D&A denominator — min(engineering reuses, 25-flight accounting cap) P1-3.

    Excel cell:        Customer Launch!— (F9 D&A add-back)
    Excel label:       "F9 effective dep lifetime (flights)"
    Architecture ref:  §4 Customer Launch COGS / MDA §11.5
    Principle:         8 (accounting cap on booster depreciation)

    """
    engineering = assumption_scalar(assumptions, cl.F9_LIFETIME_REUSES_PER_BOOSTER)
    cap = assumption_scalar(
        assumptions,
        cl.F9_BOOSTER_ACCOUNTING_DEPRECIATION_CAP_FLIGHTS,
        default=25.0,
    )
    return min(engineering, cap)


def _f9_customer_launches(inputs: CustomerLaunchInputs) -> YearVector:
    """F9 customer launches — Assumptions year-row; S-1 default 43 in 2025 (P0-5)."""
    a = inputs.assumptions
    row = a.lookup(cl.F9_CUSTOMER_LAUNCHES_PER_YEAR)
    if row is not None and (row.year_values or row.base_case is not None):
        vec = row.as_year_vector()
        if row.base_case is not None and isinstance(row.base_case, (int, float)):
            for idx in range(HORIZON_YEARS):
                if vec[idx] == 0.0 and not row.year_values:
                    vec[idx] = float(row.base_case)
        return YearVector(vec)
    anchor = float(f9_customer_launches_per_year()[0])
    try:
        cagr = assumption_scalar(a, "Total customer launch market CAGR (% growth/yr)")
    except (KeyError, ValueError):
        cagr = 0.0
    if cagr <= 0.0:
        return YearVector(f9_customer_launches_per_year())
    years = np.arange(HORIZON_YEARS, dtype=np.float64)
    vec = anchor * np.power(1.0 + cagr, years)
    vec[0] = anchor
    return YearVector(vec)


def _f9_customer_price(inputs: CustomerLaunchInputs) -> YearVector:
    return assumption_year_vector(
        inputs.assumptions,
        "F9 customer launch price ($mm/launch) — 2025 anchor",
        default=111.0,
    )


def _starship_customer_launches(inputs: CustomerLaunchInputs) -> YearVector:
    """Starship external launches — Assumptions year-row; S-1 2H 2026 start (P1-5)."""
    if inputs.starship_customer_launches is not None:
        return inputs.starship_customer_launches
    row = inputs.assumptions.lookup(cl.STARSHIP_CUSTOMER_LAUNCHES_PER_YEAR)
    if row is not None and (row.year_values or row.base_case is not None):
        return YearVector(row.as_year_vector())
    return YearVector(starship_customer_launches_per_year())


def _starship_customer_price(inputs: CustomerLaunchInputs) -> YearVector:
    return assumption_year_vector(
        inputs.assumptions,
        "Starship customer launch price ($mm/launch) — year-row",
    )


def compute_revenue(inputs: CustomerLaunchInputs) -> YearVector:
    """External + internal launch revenue.

    Excel cell:        Customer Launch!D83
    Excel label:       "Total Revenue ($mm)"
    Architecture ref:  §4 Customer Launch revenue
    Principle:         8 (vending-machine; no OpEx on module tab)

    """
    f9_launches = _f9_customer_launches(inputs)
    f9_price = _f9_customer_price(inputs)
    f9_rev = YearVector(f9_launches.values * f9_price.values)

    if inputs.starship_customer_launches is not None:
        ship_launches = inputs.starship_customer_launches
    else:
        ship_launches = _starship_customer_launches(inputs)
    ship_price = _starship_customer_price(inputs)
    ship_rev = YearVector(ship_launches.values * ship_price.values)

    f9_int = inputs.f9_internal_launches or YearVector.zeros()
    ship_int = inputs.starship_internal_launches or YearVector.zeros()
    internal_rev = internal_transfer_revenue(f9_int, ship_int, inputs.launch_capacity)

    return YearVector(f9_rev.values + ship_rev.values + internal_rev.values)


def compute_cogs(inputs: CustomerLaunchInputs) -> YearVector:
    """Launch COGS at fully-allocated at-cost rate.

    Excel cell:        Customer Launch!D93
    Excel label:       "Total COGS ($mm)"
    Architecture ref:  §4 Customer Launch COGS
    Principle:         9 (internal transfers at fully-allocated cost)

    """
    a = inputs.assumptions
    lc = inputs.launch_capacity
    f9_cust = _f9_customer_launches(inputs)
    f9_int = inputs.f9_internal_launches or YearVector.zeros()

    if inputs.starship_customer_launches is not None:
        ship_cust = inputs.starship_customer_launches
    else:
        ship_cust = _starship_customer_launches(inputs)
    ship_int = inputs.starship_internal_launches or YearVector.zeros()

    f9_var_per_launch = lc.f9_at_cost_rate.values - (lc.f9_at_cost_rate.values * 0)  # full at-cost
    # Variable + D&A decomposition from Launch Capacity
    f9_booster_cost = assumption_scalar(a, "F9 booster (1st stage) mfg cost ($mm/unit)")
    f9_lifetime = f9_effective_dep_lifetime(a)
    f9_2nd = assumption_scalar(a, "F9 2nd stage mfg cost ($mm/unit)")
    f9_fairing = assumption_scalar(a, "F9 fairing cost net of 75% recovery ($mm/flight)")
    f9_ops = assumption_scalar(a, "F9 per-launch ops cost ($mm)")
    f9_refurb = assumption_scalar(a, "F9 booster refurb % of mfg")
    f9_var = f9_2nd + f9_fairing + f9_ops + f9_refurb * f9_booster_cost
    f9_da = f9_booster_cost / f9_lifetime

    total_f9_launches = f9_cust.values + f9_int.values
    f9_variable = total_f9_launches * f9_var
    f9_da_cogs = total_f9_launches * f9_da

    total_ship = ship_cust.values + ship_int.values
    ship_var = total_ship * lc.starship_at_cost_rate.values * 0  # Starship var embedded in at-cost
    ship_da = total_ship * (
        lc.starship_at_cost_rate.values - lc.starship_at_cost_rate.values * 0
    )

    revenue = compute_revenue(inputs)
    insurance_pct = assumption_scalar(a, "Launch insurance % of external revenue", default=0.05)
    other_pct = assumption_scalar(a, "Launch other COGS % of external revenue", default=0.02)
    ground_ops_pct = assumption_scalar(
        a, "Customer Launch ground ops % of revenue", default=0.01
    )

    external_rev = f9_cust.values * _f9_customer_price(inputs).values + ship_cust.values * _starship_customer_price(inputs).values
    insurance = external_rev * insurance_pct
    other = external_rev * other_pct
    ground_ops = revenue.values * ground_ops_pct

    # Simplified: F9 COGS = launches × at-cost; Starship COGS = ship launches × at-cost
    f9_cogs = total_f9_launches * lc.f9_at_cost_rate.values
    ship_cogs = total_ship * lc.starship_at_cost_rate.values
    total = f9_cogs + ship_cogs + ground_ops + insurance + other
    return YearVector(total)


def compute_gross_profit(inputs: CustomerLaunchInputs) -> YearVector:
    """Gross profit = revenue − COGS.

    Excel cell:        Customer Launch!D94
    Excel label:       "Gross Profit ($mm)"
    Architecture ref:  §3 module framing
    Principle:         7 (Module EBITDA = Gross Profit)

    """
    return YearVector(compute_revenue(inputs).values - compute_cogs(inputs).values)


def compute_capex(inputs: CustomerLaunchInputs) -> YearVector:
    """Ground equipment + integration CapEx; excludes vehicle build.

    Excel cell:        Customer Launch!D99
    Excel label:       "Module CapEx ($mm)"
    Architecture ref:  §4 Customer Launch CapEx
    Principle:         8 (vehicle build at queue gate, not module CapEx)

    """
    revenue = compute_revenue(inputs)
    capex_pct = assumption_scalar(
        inputs.assumptions,
        "Customer Launch ground equipment CapEx % of revenue",
        default=0.005,
    )
    return YearVector(revenue.values * capex_pct)


def compute_fcf(inputs: CustomerLaunchInputs) -> YearVector:
    """Module FCF = EBITDA + D&A add-back − CapEx.

    Excel cell:        Customer Launch!D101
    Excel label:       "Module FCF ($mm)"
    Architecture ref:  §3 module FCF definition
    Principle:         8 (pre-tax module FCF; no corp overhead)

    """
    ebitda = compute_gross_profit(inputs)
    capex = compute_capex(inputs)
    f9_launches = _f9_customer_launches(inputs)
    f9_int = inputs.f9_internal_launches or YearVector.zeros()
    f9_booster_cost = assumption_scalar(inputs.assumptions, "F9 booster (1st stage) mfg cost ($mm/unit)")
    f9_lifetime = f9_effective_dep_lifetime(inputs.assumptions)
    da_addback = YearVector((f9_launches.values + f9_int.values) * (f9_booster_cost / f9_lifetime))
    return YearVector(ebitda.values + da_addback.values - capex.values)


def compute_launch_services_revenue_memo(inputs: CustomerLaunchInputs) -> YearVector:
    """P1-11 memo: Launch Services vs L&D split of external CL revenue (S-1 Space sub-mix).

    Excel cell:        Customer Launch!— (memo)
    Excel label:       "Launch Services revenue ($mm) — S-1 memo"
    Architecture ref:  §4 Customer Launch + MDA §1.3
    Principle:         3 (reconciliation memo; total revenue unchanged)

    """
    f9_launches = _f9_customer_launches(inputs)
    f9_price = _f9_customer_price(inputs)
    ship_launches = _starship_customer_launches(inputs)
    ship_price = _starship_customer_price(inputs)
    external = f9_launches.values * f9_price.values + ship_launches.values * ship_price.values
    share = assumption_year_vector(
        inputs.assumptions,
        cl.LAUNCH_SERVICES_REVENUE_SHARE_YEAR_ROW,
        default=0.63,
    )
    return YearVector(external * share.values)


def compute_launch_development_revenue_memo(inputs: CustomerLaunchInputs) -> YearVector:
    """P1-11 memo: L&D portion of external CL revenue.

    Excel cell:        Customer Launch!— (memo)
    Excel label:       "Launch & Development revenue ($mm) — S-1 memo"
    Architecture ref:  §4 Customer Launch + MDA §1.3
    Principle:         3 (reconciliation memo)

    """
    f9_launches = _f9_customer_launches(inputs)
    f9_price = _f9_customer_price(inputs)
    ship_launches = _starship_customer_launches(inputs)
    ship_price = _starship_customer_price(inputs)
    external = f9_launches.values * f9_price.values + ship_launches.values * ship_price.values
    share = assumption_year_vector(
        inputs.assumptions,
        cl.LAUNCH_SERVICES_REVENUE_SHARE_YEAR_ROW,
        default=0.63,
    )
    return YearVector(external * (1.0 - share.values))


def _compute_f9_irr(inputs: CustomerLaunchInputs) -> YearVector:
    """Per-booster annual F9 IRR (D4 expected high disposition)."""
    a = inputs.assumptions
    lc = inputs.launch_capacity
    f9_booster_cost = assumption_scalar(a, "F9 booster (1st stage) mfg cost ($mm/unit)")
    cost_slug = f9_booster_cost
    f9_price = _f9_customer_price(inputs).at(FIRST_YEAR)
    at_cost = lc.f9_at_cost_rate.at(FIRST_YEAR)
    insurance_pct = assumption_scalar(a, "Launch insurance % of external revenue", default=0.05)
    other_pct = assumption_scalar(a, "Launch other COGS % of external revenue", default=0.02)
    f9_cadence = assumption_scalar(a, "F9 cadence per booster (flights/year, flat)")
    margin_per_launch = f9_price - at_cost - f9_price * (insurance_pct + other_pct)
    annual_margin = margin_per_launch * f9_cadence

    n = int(assumption_scalar(a, "Customer Launch depreciation useful life (years)", default=5.0))
    rev_vec = np.full(n, annual_margin)
    result = compute_irr_engine(cost_slug, rev_vec, forward_weight=0.7, horizon_n=n)
    blended = np.full(HORIZON_YEARS, result.blended)
    return YearVector(blended)


def compute_allocator_out(inputs: CustomerLaunchInputs | None = None) -> AllocatorOut:
    """Assemble Allocator OUT from vending-machine sections.

    Excel cell:        Customer Launch!D201:AC210
    Excel label:       "CENTRAL ALLOCATOR OUTPUTS"
    Architecture ref:  §4 Allocator OUT contract
    Principle:         3 (canonical cross-tab labels via registry)

    """
    if inputs is None:
        z = YearVector.zeros()
        return build_allocator_out(revenue=z, cogs=z, capex=z)

    revenue = compute_revenue(inputs)
    cogs = compute_cogs(inputs)
    capex = compute_capex(inputs)
    irr = _compute_f9_irr(inputs)

    ship_launches = inputs.starship_customer_launches or YearVector.zeros()
    upmass = inputs.launch_capacity.per_launch_upmass_kg
    capacity_demand = YearVector(ship_launches.values * upmass.values)

    return build_allocator_out(
        revenue=revenue,
        cogs=cogs,
        capex=capex,
        capacity_demand_kg=capacity_demand,
        spot_irr=irr,
        forward_irr=irr,
        blended_irr=irr,
    )
