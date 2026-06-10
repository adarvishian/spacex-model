"""Unified allocator conservation identities — U4 / F6 guardrails."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc.allocator.debt_facilities import (
    DebtFacilitiesResult,
    compute_chip_transfer_revenue_mm,
)
from spacex_model.calc.allocator.types import AllocatorResult
from spacex_model.config.constants import (
    CONSERVATION_RESIDUAL_TOLERANCE_MM,
    FIRST_YEAR,
    HORIZON_YEARS,
    LAST_YEAR,
)
from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class AllocatorConservationInputs:
    """Inputs for unified-spine allocator guardrails."""

    allocator: AllocatorResult
    group_fcf: YearVector
    debt: DebtFacilitiesResult | None = None
    gigabay_throughput: YearVector | None = None
    chips_demanded: YearVector | None = None
    bridge_drawdown: YearVector | None = None
    ipo_drawdown: YearVector | None = None


@dataclass(frozen=True, slots=True)
class AllocatorConservationResult:
    """Per-check OK flags and residuals for allocator + CAE cash-flow identity."""

    ok_by_check: dict[str, bool]
    residuals_by_check: dict[str, dict[int, float]]

    @property
    def all_ok(self) -> bool:
        return all(self.ok_by_check.values())


def compute_r14_cash_flow_identity(
    *,
    cash_eoy: YearVector,
    cash_available: YearVector,
    group_fcf: YearVector,
    terafab_interest: YearVector,
    terafab_repayment: YearVector,
    odc_draw: YearVector,
    odc_interest: YearVector,
    odc_repayment: YearVector,
    bridge_drawdown: YearVector | None = None,
    ipo_drawdown: YearVector | None = None,
) -> dict[int, float]:
    """Conservation tab R14 — CAE cash spine includes all facility flows (F6).

    Excel cell:        Conservation!D14:S14
    Excel label:       "Cash-flow identity"
    Architecture ref:  PRD U4 / MASTER CONTEXT §4.7
    Principle:         19 (R14 repaired: … − R134 + R135 + R136)

    Formula: Conservation tab R14 — CAE cash spine includes all facility flows (F6).

    residual = R56 − R11 − R55 + R106 + R107 − R134 + R135 + R136

    """
    bridge = (
        bridge_drawdown.values
        if bridge_drawdown is not None
        else np.zeros(HORIZON_YEARS)
    )
    ipo = ipo_drawdown.values if ipo_drawdown is not None else np.zeros(HORIZON_YEARS)
    years = range(FIRST_YEAR, LAST_YEAR + 1)
    residuals: dict[int, float] = {}
    for year in years:
        idx = year - FIRST_YEAR
        # R11 = R8 + R9 + R10 (+ draw); cash_eoy uses R8-chained BoY — add R9/R10 back (F6).
        residuals[year] = float(
            cash_eoy.values[idx]
            - cash_available.values[idx]
            - group_fcf.values[idx]
            + terafab_interest.values[idx]
            + terafab_repayment.values[idx]
            - odc_draw.values[idx]
            + odc_interest.values[idx]
            + odc_repayment.values[idx]
            + bridge[idx]
            + ipo[idx]
        )
    return residuals


def _sum_cash_alloc(cash) -> np.ndarray:
    total = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for vec in cash.as_tuple():
        total += vec.values
    return total


def compute_allocator_conservation(
    inputs: AllocatorConservationInputs,
) -> AllocatorConservationResult:
    """Unified allocator guardrails: bounds, deploy identity, leftovers, R14.

    Excel cell:        Conservation tab + CAE unified spine
    Excel label:       "ALL OK (R108-equivalent)" … "Cash-flow identity"
    Architecture ref:  PRD U4 gate
    Principle:         19 (F6 repaired; superseded paths retired)

    Formula: Unified allocator guardrails: bounds, deploy identity, leftovers, R14.

    """
    alloc = inputs.allocator
    years = range(FIRST_YEAR, LAST_YEAR + 1)
    tol = CONSERVATION_RESIDUAL_TOLERANCE_MM
    ok: dict[str, bool] = {}
    residuals: dict[str, dict[int, float]] = {}

    pool = alloc.remaining_pool or YearVector.zeros()
    total_cash = _sum_cash_alloc(alloc.cash)
    alloc_residuals: dict[int, float] = {}
    for year in years:
        idx = year - FIRST_YEAR
        alloc_residuals[year] = float(total_cash[idx] - pool.values[idx])
    residuals["alloc_bounds"] = alloc_residuals
    ok["alloc_bounds"] = all(v <= tol for v in alloc_residuals.values())

    throughput = inputs.gigabay_throughput or YearVector.zeros()
    slots_used = alloc.ship_slots_used or YearVector.zeros()
    slot_residuals: dict[int, float] = {}
    for year in years:
        idx = year - FIRST_YEAR
        slot_residuals[year] = float(slots_used.values[idx] - throughput.values[idx])
    residuals["slot_bounds"] = slot_residuals
    ok["slot_bounds"] = all(v <= tol for v in slot_residuals.values())

    seed = alloc.strategic_seed_cash or YearVector.zeros()
    odc_total = alloc.odc_total_cash or alloc.cash.odc
    pool_odc = alloc.odc_pool_cash or YearVector.zeros()
    deploy_residuals: dict[int, float] = {}
    for year in years:
        idx = year - FIRST_YEAR
        deploy_residuals[year] = float(
            odc_total.values[idx] - seed.values[idx] - pool_odc.values[idx]
        )
    residuals["odc_deploy_identity"] = deploy_residuals
    ok["odc_deploy_identity"] = all(abs(v) <= tol for v in deploy_residuals.values())

    cash_left = alloc.water_fill_residual or YearVector.zeros()
    slots_idle = alloc.ship_slots_idle or YearVector.zeros()
    leftover_residuals: dict[int, float] = {}
    for year in years:
        idx = year - FIRST_YEAR
        leftover_residuals[year] = float(
            min(cash_left.values[idx], slots_idle.values[idx])
        )
    residuals["leftovers_parked"] = leftover_residuals
    ok["leftovers_parked"] = all(
        cash_left.values[idx] >= -tol and slots_idle.values[idx] >= -tol
        for idx in range(HORIZON_YEARS)
    )

    if inputs.chips_demanded is not None and alloc.chip_at_cost_per_sat is not None:
        expected = compute_chip_transfer_revenue_mm(
            inputs.chips_demanded, alloc.chip_at_cost_per_sat
        )
        chip_residuals: dict[int, float] = {}
        for year in years:
            idx = year - FIRST_YEAR
            chips = inputs.chips_demanded.values[idx]
            if chips > 0.0:
                chip_residuals[year] = float(
                    expected.values[idx]
                    - chips * alloc.chip_at_cost_per_sat.values[idx] / 1e6
                )
            else:
                chip_residuals[year] = 0.0
        residuals["chip_transfer_absorption"] = chip_residuals
        ok["chip_transfer_absorption"] = all(
            abs(v) <= tol for v in chip_residuals.values()
        )

    cash_eoy = alloc.cash_eoy or YearVector.zeros()
    cash_avail = alloc.cash_available_for_year or alloc.available_cash
    gcf = inputs.group_fcf
    if inputs.debt is not None:
        tf = inputs.debt.terafab
        odc = inputs.debt.odc
        r14 = compute_r14_cash_flow_identity(
            cash_eoy=cash_eoy,
            cash_available=cash_avail,
            group_fcf=gcf,
            terafab_interest=tf.interest,
            terafab_repayment=tf.repayment,
            odc_draw=odc.draw,
            odc_interest=odc.interest,
            odc_repayment=odc.repayment,
            bridge_drawdown=inputs.bridge_drawdown,
            ipo_drawdown=inputs.ipo_drawdown,
        )
    else:
        z = YearVector.zeros()
        r14 = compute_r14_cash_flow_identity(
            cash_eoy=cash_eoy,
            cash_available=cash_avail,
            group_fcf=gcf,
            terafab_interest=z,
            terafab_repayment=z,
            odc_draw=z,
            odc_interest=z,
            odc_repayment=z,
            bridge_drawdown=inputs.bridge_drawdown,
            ipo_drawdown=inputs.ipo_drawdown,
        )
    residuals["R14"] = r14
    ok["R14"] = all(abs(v) <= tol for v in r14.values())

    return AllocatorConservationResult(ok_by_check=ok, residuals_by_check=residuals)
