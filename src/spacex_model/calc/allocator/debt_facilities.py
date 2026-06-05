"""CAE debt facilities — Terafab project-finance debt (U3); ODC bypass retired.

Terafab (R103–R111): genuine project debt, repaid from at-cost chip transfer.
ODC facility (R131–R140): folded into unified spine — draw always zero (F5 fixed).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import CONSERVATION_RESIDUAL_TOLERANCE_MM, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class TerafabFacilityInputs:
    """Terafab construction facility — CAE R103–R111."""

    assumptions: Assumptions
    terafab_capex_to_fund: YearVector
    cash_eoy: YearVector | None = None
    ipo_injection: YearVector | None = None
    group_fcf: YearVector | None = None
    chip_transfer_revenue: YearVector | None = None


@dataclass(frozen=True, slots=True)
class TerafabFacilityResult:
    capex_to_fund: YearVector
    draw: YearVector
    interest: YearVector
    repayment: YearVector
    balance_eoy: YearVector
    cum_draws: YearVector
    cum_repayments: YearVector
    conservation_draw_repay_balance: YearVector


@dataclass(frozen=True, slots=True)
class OdcFacilityInputs:
    """ODC construction facility — CAE R131–R140."""

    assumptions: Assumptions
    odc_capex_need: YearVector
    odc_pool_allocation: YearVector
    ai_compute_module_fcf: YearVector | None = None


@dataclass(frozen=True, slots=True)
class OdcFacilityResult:
    capex_need: YearVector
    pool_allocation: YearVector
    draw: YearVector
    interest: YearVector
    repayment: YearVector
    balance_eoy: YearVector
    cum_draws: YearVector
    cum_repayments: YearVector
    conservation_draw_repay_balance: YearVector


@dataclass(frozen=True, slots=True)
class DebtFacilitiesResult:
    terafab: TerafabFacilityResult
    odc: OdcFacilityResult


def _vec_or_zero(vec: YearVector | None) -> np.ndarray:
    return vec.values if vec is not None else np.zeros(HORIZON_YEARS, dtype=np.float64)


def compute_terafab_facility(inputs: TerafabFacilityInputs) -> TerafabFacilityResult:
    """Terafab construction facility debt layer — CAE R103–R111.

    Excel cell:        Cash Allocation Engine!D105:S111
    Excel label:       "Facility draw ($mm)" … "Conservation: Σdraw − Σrepay − balance"
    Architecture ref:  §5.4 D5 (project-finance debt, out of IRR)
    Principle:         4 (debt layer on enabling-infra CapEx)

    """
    a = inputs.assumptions
    facility_cap = assumption_scalar(a, cl.TERAFAB_FACILITY_CAP_MM, default=0.0)
    interest_rate = assumption_scalar(a, cl.TERAFAB_FACILITY_INTEREST_RATE_ANNUAL, default=0.0)
    min_cash_buffer = assumption_scalar(a, cl.MINIMUM_CASH_BUFFER_MM, default=0.0)
    fcf_sweep = assumption_scalar(a, cl.FCF_REPAYMENT_SWEEP_OF_EXCESS_FCF, default=0.5)
    repaid_by_year = int(assumption_scalar(a, cl.TERAFAB_FACILITY_REPAID_BY_YEAR, default=2035.0))
    draw_end_year = int(assumption_scalar(a, cl.TERAFAB_FACILITY_DRAW_WINDOW_END_YEAR, default=2030.0))

    cash_eoy = _vec_or_zero(inputs.cash_eoy)
    ipo = _vec_or_zero(inputs.ipo_injection)
    group_fcf = _vec_or_zero(inputs.group_fcf)
    chip_transfer = _vec_or_zero(inputs.chip_transfer_revenue)

    draw = np.zeros(HORIZON_YEARS, dtype=np.float64)
    interest = np.zeros(HORIZON_YEARS, dtype=np.float64)
    repayment = np.zeros(HORIZON_YEARS, dtype=np.float64)
    balance = np.zeros(HORIZON_YEARS, dtype=np.float64)
    cum_draws = np.zeros(HORIZON_YEARS, dtype=np.float64)
    cum_repayments = np.zeros(HORIZON_YEARS, dtype=np.float64)

    for t in range(HORIZON_YEARS):
        year = 2025 + t
        prior_bal = 0.0 if t == 0 else balance[t - 1]
        prior_cum_draw = 0.0 if t == 0 else cum_draws[t - 1]
        prior_cum_repay = 0.0 if t == 0 else cum_repayments[t - 1]
        prior_cash = 0.0 if t == 0 else cash_eoy[t - 1]
        prior_fcf = 0.0 if t == 0 else group_fcf[t - 1]

        capex_need = inputs.terafab_capex_to_fund.values[t]
        if year <= draw_end_year and t > 0 and capex_need > 0.0:
            headroom_cap = max(0.0, facility_cap - prior_bal)
            draw[t] = min(capex_need, headroom_cap)

        if t > 0:
            interest[t] = prior_bal * interest_rate
            amort = 0.0
            if year <= repaid_by_year:
                amort = prior_bal / max(1, repaid_by_year - year + 1)
            fcf_repay = fcf_sweep * max(0.0, prior_fcf - min_cash_buffer)
            chip_repay = max(0.0, chip_transfer[t])
            repayment[t] = min(prior_bal + draw[t], max(fcf_repay, amort, chip_repay))
            balance[t] = prior_bal + draw[t] - repayment[t]

        cum_draws[t] = prior_cum_draw + draw[t]
        cum_repayments[t] = prior_cum_repay + repayment[t]

    conservation = cum_draws - cum_repayments - balance

    return TerafabFacilityResult(
        capex_to_fund=inputs.terafab_capex_to_fund,
        draw=YearVector(draw),
        interest=YearVector(interest),
        repayment=YearVector(repayment),
        balance_eoy=YearVector(balance),
        cum_draws=YearVector(cum_draws),
        cum_repayments=YearVector(cum_repayments),
        conservation_draw_repay_balance=YearVector(conservation),
    )


def compute_odc_facility(inputs: OdcFacilityInputs) -> OdcFacilityResult:
    """ODC facility retired — funding via strategic seed + pool allocation (U3 / F5).

    Excel cell:        Cash Allocation Engine!D134:S140 (xlsx bypass preserved for diagnostic)
    Excel label:       "ODC facility draw ($mm)" … "Conservation: ODC Σdraw − Σrepay − balance"
    Architecture ref:  PRD U3 fold ODC bypass into spine
    Principle:         4 (no pool bypass; seed + allocation only)

    """
    z = YearVector.zeros()
    return OdcFacilityResult(
        capex_need=inputs.odc_capex_need,
        pool_allocation=inputs.odc_pool_allocation,
        draw=z,
        interest=z,
        repayment=z,
        balance_eoy=z,
        cum_draws=z,
        cum_repayments=z,
        conservation_draw_repay_balance=z,
    )


def compute_chip_transfer_revenue_mm(
    chips_demanded: YearVector,
    chip_at_cost_per_sat: YearVector,
) -> YearVector:
    """At-cost chip transfer revenue — Terafab debt repayment source (bucket 2).

    Excel cell:        AI - Compute / Facilities Build cross-tab
    Excel label:       "Chip purchases (internal transfer) ($mm)"
    Architecture ref:  §5.1 bucket-2 at-cost transfer + D5
    Principle:         9 (predetermined transfer price funds project debt)

    """
    values = chips_demanded.values * chip_at_cost_per_sat.values / 1e6
    return YearVector(values)


def compute_debt_facilities(
    terafab_inputs: TerafabFacilityInputs,
    odc_inputs: OdcFacilityInputs,
) -> DebtFacilitiesResult:
    """Both CAE debt layers.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    return DebtFacilitiesResult(
        terafab=compute_terafab_facility(terafab_inputs),
        odc=compute_odc_facility(odc_inputs),
    )


def terafab_debt_conservation_ok(result: TerafabFacilityResult) -> bool:
    """CAE R111: Σdraw − Σrepay − balance = 0.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    residual = np.abs(result.conservation_draw_repay_balance.values)
    return bool(np.all(residual <= CONSERVATION_RESIDUAL_TOLERANCE_MM))


def odc_debt_conservation_ok(result: OdcFacilityResult) -> bool:
    """CAE R140: ODC Σdraw − Σrepay − balance = 0.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    residual = np.abs(result.conservation_draw_repay_balance.values)
    return bool(np.all(residual <= CONSERVATION_RESIDUAL_TOLERANCE_MM))
