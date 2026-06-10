"""Unified two-resource allocator — cash + Gigabay throughput (U2 / F2).

One 2-yr-avg prior-IRR weight + 5% soft floor across {Starlink, ODC, Terr, CL}.
Cross-resource MIN + bounded finite cascade; supersedes pro-rata kg + Level-2 softmax.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc.allocator.priority import (
    FourProgramIrrs,
    compute_soft_floor_shares,
    compute_two_year_avg_prior_irr,
)
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions

# Program order: Starlink, ODC, Terrestrial, Customer Launch
_N_PROGRAMS = 4
_LAUNCH_MASK = np.array([True, True, False, True], dtype=bool)
_IDX_TERR = 2


@dataclass(frozen=True, slots=True)
class FourProgramDemands:
    """Growth-slice cash caps and exogenous kg per first-class program."""

    cash_caps: FourProgramIrrs
    kg: FourProgramIrrs


@dataclass(frozen=True, slots=True)
class TwoResourceFillResult:
    """Cash + Gigabay reconciled allocation across four programs."""

    prior_irr_avg: FourProgramIrrs
    shares: FourProgramIrrs
    capped_shares: FourProgramIrrs
    allocated_cash: FourProgramIrrs
    allocated_kg: FourProgramIrrs
    ship_slots_used: YearVector
    cash_residual: YearVector
    ship_slots_idle: YearVector
    kg_binding_flag: YearVector


def _as_array(four: FourProgramIrrs) -> np.ndarray:
    return np.stack(
        [
            four.starlink.values,
            four.odc.values,
            four.terrestrial.values,
            four.customer_launch.values,
        ],
        axis=0,
    )


def _from_array(values: np.ndarray) -> FourProgramIrrs:
    return FourProgramIrrs(
        starlink=YearVector(values[0]),
        odc=YearVector(values[1]),
        terrestrial=YearVector(values[2]),
        customer_launch=YearVector(values[3]),
    )


def _proportional_fill(pool: float, shares: np.ndarray, caps: np.ndarray) -> np.ndarray:
    """Two-pass proportional fill capped at per-program limits."""
    out = np.zeros(_N_PROGRAMS, dtype=np.float64)
    if pool <= 0.0 or shares.sum() <= 0.0:
        return out
    norm = shares / shares.sum()
    first = np.minimum(pool * norm, caps)
    out = first.copy()
    residual = pool - first.sum()
    if residual <= 1e-9:
        return out
    headroom = np.maximum(0.0, caps - first)
    spill_w = norm * (headroom > 0.0)
    spill_total = spill_w.sum()
    if spill_total <= 0.0:
        return out
    for i in range(_N_PROGRAMS):
        if headroom[i] > 0.0:
            out[i] += min(headroom[i], residual * spill_w[i] / spill_total)
    return out


def _reconcile_year(
    pool: float,
    gigabay_ships: float,
    shares: np.ndarray,
    cash_caps: np.ndarray,
    kg_demands: np.ndarray,
    kg_per_ship_yr: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, float, float]:
    """One cash fill + one slot fill + MIN + single re-cascade."""
    cash_funded = _proportional_fill(pool, shares, cash_caps)

    ship_demands = np.zeros(_N_PROGRAMS, dtype=np.float64)
    if kg_per_ship_yr > 0.0:
        for i in range(_N_PROGRAMS):
            if _LAUNCH_MASK[i] and kg_demands[i] > 0.0:
                ship_demands[i] = kg_demands[i] / kg_per_ship_yr

    launch_shares = shares.copy()
    launch_shares[~_LAUNCH_MASK] = 0.0
    ship_funded = _proportional_fill(gigabay_ships, launch_shares, ship_demands)

    slot_cash = cash_caps.copy()
    for i in range(_N_PROGRAMS):
        if not _LAUNCH_MASK[i]:
            continue
        if ship_demands[i] > 0.0 and ship_funded[i] < ship_demands[i]:
            slot_cash[i] = cash_funded[i] * (ship_funded[i] / ship_demands[i])
        elif ship_demands[i] <= 0.0:
            slot_cash[i] = cash_funded[i]

    final_cash = np.minimum(np.minimum(cash_funded, slot_cash), cash_caps)

    cash_slack = max(0.0, pool - final_cash.sum())
    if cash_slack > 1e-6:
        headroom = np.maximum(0.0, cash_caps - final_cash)
        spill_w = shares * (headroom > 0.0)
        spill_total = spill_w.sum()
        if spill_total > 0.0:
            for i in range(_N_PROGRAMS):
                if headroom[i] > 0.0:
                    extra = min(headroom[i], cash_slack * spill_w[i] / spill_total)
                    final_cash[i] += extra
                    cash_slack -= extra
                    if cash_slack <= 1e-6:
                        break

    final_kg = np.zeros(_N_PROGRAMS, dtype=np.float64)
    for i in range(_N_PROGRAMS):
        if not _LAUNCH_MASK[i]:
            continue
        if kg_demands[i] <= 0.0:
            continue
        cash_kg = 0.0
        if cash_caps[i] > 0.0:
            cash_kg = kg_demands[i] * (final_cash[i] / cash_caps[i])
        slot_kg = (
            ship_funded[i] * kg_per_ship_yr if kg_per_ship_yr > 0.0 else kg_demands[i]
        )
        final_kg[i] = min(kg_demands[i], cash_kg, slot_kg)

    ships_used = ship_funded.sum()
    cash_residual = max(0.0, pool - final_cash.sum())
    ship_idle = max(0.0, gigabay_ships - ships_used)
    return final_cash, final_kg, ship_funded, cash_residual, ship_idle


def compute_two_resource_fill(
    remaining_pool: YearVector,
    demands: FourProgramDemands,
    prior_spot_irr: FourProgramIrrs,
    assumptions: Assumptions,
    *,
    gigabay_throughput: YearVector,
    kg_per_ship_yr: YearVector,
    lm_kg_reserved: YearVector | None = None,
    total_desired_launch_kg: YearVector | None = None,
) -> TwoResourceFillResult:
    """Cash + Gigabay two-resource fill with cross-resource MIN (U2).

    Excel cell:        Cash Allocation Engine (unified spine — supersedes R27–R52, R76–R94)
    Excel label:       "▸ TOP-LEVEL IRR-WEIGHTED ALLOCATION"
    Architecture ref:  PRD §5.2 unified engine + U2
    Principle:         2 (prior-yr IRR; cash + launch one pass)

    Formula: Cash + Gigabay two-resource fill with cross-resource MIN (U2).

    """
    prior_avg = compute_two_year_avg_prior_irr(prior_spot_irr)
    shares = compute_soft_floor_shares(prior_avg, assumptions)

    cash_caps = _as_array(demands.cash_caps)
    kg_dem = _as_array(demands.kg)
    share_arr = _as_array(shares)

    alloc_cash = np.zeros((_N_PROGRAMS, HORIZON_YEARS), dtype=np.float64)
    alloc_kg = np.zeros((_N_PROGRAMS, HORIZON_YEARS), dtype=np.float64)
    ships_used = np.zeros(HORIZON_YEARS, dtype=np.float64)
    cash_res = np.zeros(HORIZON_YEARS, dtype=np.float64)
    ship_idle = np.zeros(HORIZON_YEARS, dtype=np.float64)
    capped_share = np.zeros((_N_PROGRAMS, HORIZON_YEARS), dtype=np.float64)
    binding = np.zeros(HORIZON_YEARS, dtype=np.float64)

    lm = (
        lm_kg_reserved.values if lm_kg_reserved is not None else np.zeros(HORIZON_YEARS)
    )
    spine_total = (
        total_desired_launch_kg.values
        if total_desired_launch_kg is not None
        else kg_dem.sum(axis=0)
    )

    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        pool = remaining_pool.values[t]
        if year == FIRST_YEAR or pool <= 0.0:
            continue

        final_cash, final_kg, ship_alloc, c_res, s_idle = _reconcile_year(
            pool,
            gigabay_throughput.values[t],
            share_arr[:, t],
            cash_caps[:, t],
            kg_dem[:, t],
            kg_per_ship_yr.values[t],
        )
        alloc_cash[:, t] = final_cash
        alloc_kg[:, t] = final_kg
        ships_used[t] = ship_alloc.sum()
        cash_res[t] = c_res
        ship_idle[t] = s_idle

        total_alloc = final_cash.sum()
        if total_alloc > 0.0:
            capped_share[:, t] = final_cash / total_alloc

        launch_kg_cap = gigabay_throughput.values[t] * kg_per_ship_yr.values[t]
        cap_after_lm = max(0.0, launch_kg_cap - lm[t])
        binding[t] = (
            1.0 if spine_total[t] > cap_after_lm and cap_after_lm > 0.0 else 0.0
        )

    return TwoResourceFillResult(
        prior_irr_avg=prior_avg,
        shares=shares,
        capped_shares=_from_array(capped_share),
        allocated_cash=_from_array(alloc_cash),
        allocated_kg=_from_array(alloc_kg),
        ship_slots_used=YearVector(ships_used),
        cash_residual=YearVector(cash_res),
        ship_slots_idle=YearVector(ship_idle),
        kg_binding_flag=YearVector(binding),
    )


def kg_per_ship_year(
    assumptions: Assumptions, launch_per_launch_upmass: YearVector
) -> YearVector:
    """Annual kg throughput per Starship ship slot (payload × cadence).

    Excel cell:        Facilities Build!D19
    Excel label:       "Installed Starship build capacity (ships/yr): rate-limited ramp"
    Architecture ref:  PRD D8 Gigabay throughput
    Principle:         12 (predetermined capacity inputs)

    Formula: Annual kg throughput per Starship ship slot (payload × cadence).

    """
    cadence = assumption_scalar(
        assumptions,
        cl.LAUNCHES_PER_STARSHIP_VEHICLE_PER_YEAR_CADENCE_VARIANT_BLEND_USED_FOR_SIZING,
    )
    return YearVector(launch_per_launch_upmass.values * cadence)
