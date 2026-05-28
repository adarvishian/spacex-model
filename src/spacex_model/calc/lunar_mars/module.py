"""Lunar Mars module — strategic carve-out vending-machine P&L (Phase C).

Architecture §11 / PRD §4.6. Pre-revenue; BV engine separate from Group D&A per §2.10.
"""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc._vending_machine import build_allocator_out
from spacex_model.calc.lunar_mars.bv_engine import BvEngineResult, compute_bv_engine
from spacex_model.calc.lunar_mars.carveout import compute_mars_carveout
from spacex_model.calc.lunar_mars.deployment import DeploymentResult, compute_deployment
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class LunarMarsInputs:
    """Upstream inputs for Lunar Mars module."""

    assumptions: Assumptions
    prior_year_group_fcf: YearVector | None = None


def _deployment(inputs: LunarMarsInputs) -> DeploymentResult:
    carveout = compute_mars_carveout(inputs.assumptions, inputs.prior_year_group_fcf)
    return compute_deployment(inputs.assumptions, carveout)


def _bv(inputs: LunarMarsInputs) -> BvEngineResult:
    dep = _deployment(inputs)
    return compute_bv_engine(
        inputs.assumptions,
        lunar_surface_payload_kg=dep.lunar_surface_payload_kg,
        mars_surface_payload_kg=dep.mars_surface_payload_kg,
        lunar_mission_capex_mm=dep.lunar_mission_capex_mm,
        mars_mission_capex_mm=dep.mars_mission_capex_mm,
    )


def compute_revenue(inputs: LunarMarsInputs | None = None) -> YearVector:
    """Revenue = 0 every year (pre-revenue strategic module).

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "Total Revenue ($mm)"
    Architecture ref:  §11 Lunar Mars
    Principle:         8 (vending-machine framing; no IRR queue)

    """
    return YearVector.zeros()


def compute_cogs(inputs: LunarMarsInputs | None = None) -> YearVector:
    """Mission ops % of CapEx only; no BV depreciation in COGS per §20.5.

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "Total COGS ($mm)"
    Architecture ref:  §20.5 LM COGS
    Principle:         8 (BV decay is memo-only for Valuation)

    """
    if inputs is None:
        return YearVector.zeros()
    dep = _deployment(inputs)
    lunar_ops = assumption_scalar(inputs.assumptions, "Module operating cost — Lunar (% of Lunar CapEx)", default=0.05)
    mars_ops = assumption_scalar(inputs.assumptions, "Module operating cost — Mars (% of Mars CapEx)", default=0.05)
    mission_capex = dep.lunar_mission_capex_mm.values + dep.mars_mission_capex_mm.values
    cogs = dep.lunar_mission_capex_mm.values * lunar_ops + dep.mars_mission_capex_mm.values * mars_ops
    _ = mission_capex
    return YearVector(cogs)


def compute_gross_profit(inputs: LunarMarsInputs | None = None) -> YearVector:
    """Gross profit = revenue − COGS (negative COGS-only in steady state).

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "Gross Profit ($mm)"
    Architecture ref:  §3 module framing
    Principle:         7 (Module EBITDA = Gross Profit)

    """
    if inputs is None:
        return YearVector.zeros()
    return YearVector(compute_revenue(inputs).values - compute_cogs(inputs).values)


def compute_capex(inputs: LunarMarsInputs | None = None) -> YearVector:
    """Annual carve-out cash deployed as Module CapEx (zero before first mission year).

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "Module CapEx ($mm)"
    Architecture ref:  §11 carve-out deployment
    Principle:         22 (Mars carve-out off the top)

    """
    if inputs is None:
        return YearVector.zeros()
    dep = _deployment(inputs)
    return YearVector(dep.lunar_mission_capex_mm.values + dep.mars_mission_capex_mm.values)


def compute_fcf(inputs: LunarMarsInputs | None = None) -> YearVector:
    """Module FCF = EBITDA + Module D&A − CapEx.

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "Module FCF ($mm)"
    Architecture ref:  §20.5 LM FCF
    Principle:         8 (pre-tax module FCF)

    """
    if inputs is None:
        return YearVector.zeros()
    ebitda = compute_gross_profit(inputs)
    capex = compute_capex(inputs)
    da = _bv(inputs).module_da_mm
    return YearVector(ebitda.values + da.values - capex.values)


def compute_allocator_out(inputs: LunarMarsInputs | None = None) -> AllocatorOut:
    """Allocator OUT — IRR rows = 0; not in IRR queue.

    Excel cell:        Lunar Mars!— (Phase C)
    Excel label:       "CENTRAL ALLOCATOR OUTPUTS"
    Architecture ref:  §11 Allocator OUT
    Principle:         3 (canonical labels via registry)

    """
    if inputs is None:
        z = YearVector.zeros()
        return build_allocator_out(revenue=z, cogs=z, capex=z, capacity_demand_kg=z)

    revenue = compute_revenue(inputs)
    cogs = compute_cogs(inputs)
    capex = compute_capex(inputs)
    dep = _deployment(inputs)
    da = _bv(inputs).module_da_mm
    z = YearVector.zeros()
    return build_allocator_out(
        revenue=revenue,
        cogs=cogs,
        capex=capex,
        capacity_demand_kg=dep.capacity_demand_kg,
        spot_irr=z,
        forward_irr=z,
        blended_irr=z,
        module_da_addback=da,
    )
