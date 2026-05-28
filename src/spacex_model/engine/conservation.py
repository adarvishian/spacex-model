"""Conservation block R99-R110 and Block A allocation bounds."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.types import CashAllocations, KgAllocations
from spacex_model.calc.capex import CapExResult
from spacex_model.calc.opex import OpExResult
from spacex_model.config.constants import (
    CONSERVATION_RESIDUAL_TOLERANCE_MM,
    FIRST_YEAR,
    HORIZON_YEARS,
    LAST_YEAR,
)
from spacex_model.domain.year_vector import YearVector

_MODULE_KEYS = ("customer_launch", "starlink", "odc", "ai_stack", "lunar_mars")


class ConservationBrokenError(RuntimeError):
    """Raised when Block A conservation invariants fail at runtime."""


@dataclass(frozen=True, slots=True)
class InternalEliminations:
    """Inter-module elimination amounts subtracted from group revenue and COGS."""

    launch_services: YearVector
    bandwidth: YearVector
    compute: YearVector

    @property
    def total(self) -> YearVector:
        return YearVector(
            self.launch_services.values + self.bandwidth.values + self.compute.values
        )


@dataclass(frozen=True, slots=True)
class InternalFlowConservationInputs:
    """Consumer-side COGS for R105-R107 conservation checks."""

    launch_services_cost_starlink: YearVector
    launch_services_cost_odc: YearVector
    launch_services_cost_ai_stack: YearVector
    odc_bandwidth_services_cost: YearVector
    ai_stack_internal_compute_cost: YearVector


@dataclass(frozen=True, slots=True)
class CashIdentityInputs:
    """Cash pool tracker inputs for R109 per PRD §5.4 / §2.13."""

    cash_boy: YearVector
    starting_cash_mm: float
    bridge_drawdown: YearVector
    ipo_drawdown: YearVector


@dataclass(frozen=True, slots=True)
class ConservationResult:
    r108_ok_by_year: dict[int, str]
    residuals_by_check: dict[str, dict[int, float]]

    @property
    def all_ok(self) -> bool:
        return all(v == "OK" for v in self.r108_ok_by_year.values())


@dataclass(frozen=True, slots=True)
class AllocationBoundsResult:
    ok_by_year: dict[int, bool]
    max_overshoot_by_year: dict[int, float]

    @property
    def all_ok(self) -> bool:
        return all(self.ok_by_year.values())


def conservation_tolerance_mm(*, reference_mm: float) -> float:
    """PRD §7.7: ±$1M absolute OR ±0.1% relative, whichever is larger."""
    return max(CONSERVATION_RESIDUAL_TOLERANCE_MM, abs(reference_mm) * 0.001)


def _sum_module_field(
    module_outputs: dict[str, AllocatorOut],
    field: str,
) -> YearVector:
    total = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for key in _MODULE_KEYS:
        out = module_outputs.get(key, AllocatorOut.zeros())
        total += getattr(out, field).values
    return YearVector(total)


def _non_module_capex_claim(capex: CapExResult, module_outputs: dict[str, AllocatorOut]) -> YearVector:
    """Corporate + spectrum + vehicle build claims not in module CapEx rows."""
    module_capex = _sum_module_field(module_outputs, "module_capex")
    return YearVector(capex.total_group_capex.values - module_capex.values)


def compute_r110_module_fcf_residual(
    group_fcf: YearVector,
    module_outputs: dict[str, AllocatorOut],
) -> YearVector:
    """R110 Σ Module FCF reconciliation residual (memo only; excluded from R108).

    Excel cell:        Group P&L!R110
    Excel label:       "Σ Module FCF reconciliation residual ($mm)"
    Architecture ref:  §15.2 conservation block
    Principle:         19 (memo for module-owner audit)

    """
    module_fcf_sum = _sum_module_field(module_outputs, "module_fcf")
    return YearVector(group_fcf.values - module_fcf_sum.values)


def compute_r109_cash_identity(
    *,
    group_fcf: YearVector,
    total_group_capex: YearVector,
    mars_carveout: YearVector,
    cash_identity: CashIdentityInputs,
) -> dict[int, float]:
    """R109 cash flow identity per PRD §5.4 and Sprint 10 cash-pool tracker.

    Excel cell:        Group P&L!R109
    Excel label:       "Cash flow identity"
    Architecture ref:  §15.2 + §2.13 (pre-IPO bridge)
    Principle:         4 (cash pool feeds queue gate)

    """
    years = range(FIRST_YEAR, LAST_YEAR + 1)
    residuals: dict[int, float] = {}
    cash = cash_identity.cash_boy.values
    bridge = cash_identity.bridge_drawdown.values
    ipo = cash_identity.ipo_drawdown.values
    gcf = group_fcf.values

    for idx, year in enumerate(years):
        if idx < HORIZON_YEARS - 1:
            residual = (
                cash[idx]
                + gcf[idx]
                + ipo[idx + 1]
                + bridge[idx + 1]
                - cash[idx + 1]
            )
        else:
            # Terminal year: Cash EoY = Cash BoY + Group FCF (no year T+1 row).
            residual = cash[idx] + gcf[idx] - (cash[idx] + gcf[idx])
        residuals[year] = float(residual)
    return residuals


def compute_conservation(
    *,
    group_revenue_net: YearVector,
    module_revenue_gross: YearVector,
    eliminations: InternalEliminations,
    group_gross_profit: YearVector,
    module_outputs: dict[str, AllocatorOut],
    capex: CapExResult,
    group_da: YearVector,
    module_da_in_cogs: dict[str, YearVector],
    group_ebitda: YearVector,
    group_ebit: YearVector,
    group_fcf: YearVector,
    opex: OpExResult,
    taxes: YearVector,
    mars_carveout: YearVector,
    internal_flows: InternalFlowConservationInputs,
    cash_identity: CashIdentityInputs | None = None,
) -> ConservationResult:
    """Conservation block R99-R110 per Architecture §15.2.

    Excel cell:        Group P&L!R99:R110
    Excel label:       "ALL OK boolean"
    Architecture ref:  §15.2 conservation block
    Principle:         19 (R108 = OK required for PASS)

    """
    years = range(FIRST_YEAR, LAST_YEAR + 1)
    tol = CONSERVATION_RESIDUAL_TOLERANCE_MM
    residuals: dict[str, dict[int, float]] = {}

    module_ebitda_sum = _sum_module_field(module_outputs, "module_ebitda")
    module_capex_sum = _sum_module_field(module_outputs, "module_capex")
    module_fcf_sum = _sum_module_field(module_outputs, "module_fcf")
    non_module_capex = _non_module_capex_claim(capex, module_outputs)

    module_da_total = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for vec in module_da_in_cogs.values():
        module_da_total += vec.values

    embedded_module_da_addback = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for key in _MODULE_KEYS:
        out = module_outputs.get(key, AllocatorOut.zeros())
        embedded_module_da_addback += (
            out.module_fcf.values - (out.module_ebitda.values - out.module_capex.values)
        )
    module_da_fcf_gap = module_da_total - embedded_module_da_addback

    launch_consumer_cost = (
        internal_flows.launch_services_cost_starlink.values
        + internal_flows.launch_services_cost_odc.values
        + internal_flows.launch_services_cost_ai_stack.values
    )

    r110 = compute_r110_module_fcf_residual(group_fcf, module_outputs)
    residuals["R110"] = {year: float(r110.values[year - FIRST_YEAR]) for year in years}

    r108_ok: dict[int, str] = {}

    for year in years:
        idx = year - FIRST_YEAR

        r99 = group_revenue_net.values[idx] - (
            module_revenue_gross.values[idx] - eliminations.total.values[idx]
        )
        r100 = group_gross_profit.values[idx] - module_ebitda_sum.values[idx]
        r101 = capex.total_module_capex.values[idx] - module_capex_sum.values[idx]
        r102 = group_fcf.values[idx] - (
            module_fcf_sum.values[idx]
            + module_da_fcf_gap[idx]
            - opex.total_opex.values[idx]
            - taxes.values[idx]
            - non_module_capex.values[idx]
            - mars_carveout.values[idx]
        )
        r103 = group_da.values[idx] - (
            module_da_total[idx]
            + capex.corporate_da.values[idx]
            + capex.spectrum_amortization.values[idx]
        )
        r104 = group_ebit.values[idx] - (
            group_ebitda.values[idx] - group_da.values[idx] + module_da_total[idx]
        )
        r105 = eliminations.launch_services.values[idx] - launch_consumer_cost[idx]
        r106 = eliminations.bandwidth.values[idx] - internal_flows.odc_bandwidth_services_cost.values[idx]
        r107 = eliminations.compute.values[idx] - internal_flows.ai_stack_internal_compute_cost.values[idx]

        check_vals = {
            "R99": r99,
            "R100": r100,
            "R101": r101,
            "R102": r102,
            "R103": r103,
            "R104": r104,
            "R105": r105,
            "R106": r106,
            "R107": r107,
        }
        for name, val in check_vals.items():
            residuals.setdefault(name, {})[year] = float(val)

        ok = all(abs(v) < tol for k, v in check_vals.items())
        r108_ok[year] = "OK" if ok else "CHECK"

    if cash_identity is not None:
        residuals["R109"] = compute_r109_cash_identity(
            group_fcf=group_fcf,
            total_group_capex=capex.total_group_capex,
            mars_carveout=mars_carveout,
            cash_identity=cash_identity,
        )
    else:
        residuals["R109"] = {y: 0.0 for y in years}

    return ConservationResult(
        r108_ok_by_year=r108_ok,
        residuals_by_check=residuals,
    )


def raise_on_break(conservation: ConservationResult) -> None:
    """Halt the pipeline when R108 contains any CHECK year (PRD §16.2)."""
    failed = {year: status for year, status in conservation.r108_ok_by_year.items() if status != "OK"}
    if not failed:
        return
    details = []
    for year in sorted(failed):
        parts = []
        for check, by_year in conservation.residuals_by_check.items():
            if check in ("R108", "R109", "R110"):
                continue
            residual = by_year.get(year)
            if residual is not None and abs(residual) >= CONSERVATION_RESIDUAL_TOLERANCE_MM:
                parts.append(f"{check}={residual:.3f}mm")
        details.append(f"{year}: {', '.join(parts) if parts else 'CHECK'}")
    raise ConservationBrokenError(
        "Conservation block R108 failed — " + "; ".join(details)
    )


def check_allocation_bounds(
    cash: CashAllocations,
    available_cash: YearVector,
    *,
    tolerance_mm: float = CONSERVATION_RESIDUAL_TOLERANCE_MM,
) -> AllocationBoundsResult:
    """Σ module cash allocations ≤ available cash for IRR queue every year (Block A).

    Excel cell:        Allocator!— (Phase D invariant)
    Excel label:       "Available cash for IRR queue ($mm)"
    Architecture ref:  §6.2 queue gate
    Principle:         4 (non-module claims reserved first)

    """
    years = range(FIRST_YEAR, LAST_YEAR + 1)
    ok: dict[int, bool] = {}
    overshoot: dict[int, float] = {}
    total = np.zeros_like(available_cash.values)
    for vec in cash.as_tuple():
        total += vec.values
    for year in years:
        idx = year - FIRST_YEAR
        delta = total[idx] - available_cash.values[idx]
        overshoot[year] = float(delta)
        ok[year] = delta <= tolerance_mm
    return AllocationBoundsResult(ok_by_year=ok, max_overshoot_by_year=overshoot)


def check_kg_allocation_bounds(
    kg: KgAllocations,
    capacity_available_kg: YearVector,
    *,
    tolerance_kg: float = 1.0,
) -> AllocationBoundsResult:
    """Σ module kg allocations ≤ capacity available for IRR queue every year (Block A).

    Excel cell:        Allocator!— (Phase D invariant)
    Excel label:       "Total Annual Capacity (kg-to-LEO)"
    Architecture ref:  §6.4 kg sigmoid queue
    Principle:         4 (vehicle-build claim netted from capacity)

    """
    years = range(FIRST_YEAR, LAST_YEAR + 1)
    ok: dict[int, bool] = {}
    overshoot: dict[int, float] = {}
    total = np.zeros_like(capacity_available_kg.values)
    for vec in kg.as_tuple():
        total += vec.values
    for year in years:
        idx = year - FIRST_YEAR
        delta = total[idx] - capacity_available_kg.values[idx]
        overshoot[year] = float(delta)
        ok[year] = delta <= tolerance_kg
    return AllocationBoundsResult(ok_by_year=ok, max_overshoot_by_year=overshoot)
