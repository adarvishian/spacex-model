"""Model pipeline orchestration — Phase D allocator + iterative solver."""

from __future__ import annotations

import hashlib
import json
import time
import tracemalloc
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np

from spacex_model.calc._allocator_allocation import AllocatorAllocation
from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc._vehicle_allocations import VehicleAllocations
from spacex_model.calc.ai_stack import AIStackInputs, compute_allocator_out as ai_stack_out
from spacex_model.calc.allocator.brain import AllocatorInputs, compute_allocator
from spacex_model.calc.allocator.demand_builders import compute_exogenous_demands
from spacex_model.calc.allocator.types import CashAllocations, KgAllocations
from spacex_model.calc.capex import CapExInputs, compute_capex
from spacex_model.calc.customer_launch import compute_allocator_out as customer_launch_out
from spacex_model.calc.customer_launch.module import (
    CustomerLaunchInputs,
    _f9_customer_launches,
    _f9_customer_price,
    _starship_customer_launches,
    _starship_customer_price,
    f9_effective_dep_lifetime,
)
from spacex_model.calc.group_pnl import (
    CashIdentityInputs,
    GroupPnlInputs,
    GroupPnlResult,
    InternalEliminations,
    InternalFlowConservationInputs,
    compute_group_pnl,
)
from spacex_model.calc.internal_flows import bandwidth as bandwidth_flow
from spacex_model.calc.internal_flows import compute as compute_flow
from spacex_model.calc.internal_flows.launch_services import internal_transfer_revenue
from spacex_model.calc.allocator.cash_pool import compute_bridge_drawdown, compute_cash_boy, compute_ipo_drawdown, starting_cash_mm
from spacex_model.calc.launch_capacity import LaunchCapacityInputs, LaunchCapacityResult, compute_launch_capacity
from spacex_model.calc.lunar_mars import compute_allocator_out as lunar_mars_out
from spacex_model.calc.lunar_mars.bv_engine import compute_bv_engine
from spacex_model.calc.lunar_mars.carveout import compute_mars_carveout
from spacex_model.calc.lunar_mars.deployment import compute_deployment
from spacex_model.calc.lunar_mars.module import LunarMarsInputs
from spacex_model.calc.odc import compute_allocator_out as odc_out
from spacex_model.calc.odc.demand import DemandInputs as OdcDemandInputs
from spacex_model.calc.odc.demand import compute_demand as odc_compute_demand
from spacex_model.calc.odc.module import OdcInputs, odc_bandwidth_claim
from spacex_model.calc.odc.output import compute_output as odc_compute_output
from spacex_model.calc.opex import OpExInputs, build_revenue_bases, compute_opex
from spacex_model.calc.starlink import compute_allocator_out as starlink_out
from spacex_model.calc.starlink.module import (
    StarlinkInputs,
    compute_constellation_da,
    compute_launch_services_cost,
    compute_starlink_capacity_result,
)
from spacex_model.calc.starlink.vehicle_pools import VehiclePoolsResult, compute_vehicle_pools
from spacex_model.calc.starlink_capacity import OdcBandwidthClaim
from spacex_model.calc.valuation import ValuationInputs, ValuationResult, compute_valuation
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.config.settings import get_settings
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.conservation import ConservationResult, check_allocation_bounds, raise_on_break
from spacex_model.engine.iterative_solver import SolverTrace, damped_blend, solve_fixed_point
from spacex_model.inputs.assumptions import Assumptions, assumptions_from_ingest
from spacex_model.inputs.demand_curves import DemandCurves, demand_curves_from_ingest
from spacex_model.io.excel_ingest import IngestResult, ingest_workbook
from spacex_model.io.snapshot_store import write_diagnostic_snapshot

_MODULE_KEYS = ("customer_launch", "starlink", "odc", "ai_stack", "lunar_mars")


@dataclass
class PipelineState:
    """Mutable state for fixed-point iteration."""

    cash_alloc: CashAllocations
    kg_alloc: KgAllocations
    vehicle_build_claim: YearVector
    module_outputs: dict[str, AllocatorOut]
    launch_capacity: LaunchCapacityResult | None = None
    group_pnl: GroupPnlResult | None = None
    allocator: Any = None
    valuation: ValuationResult | None = None


@dataclass
class ModelResult:
    run_id: str
    assumptions: Assumptions
    ingest: IngestResult
    demand_curves: DemandCurves
    module_outputs: dict[str, AllocatorOut]
    group_pnl: GroupPnlResult
    launch_capacity: LaunchCapacityResult
    allocator: Any
    valuation: ValuationResult
    solver_trace: SolverTrace
    conservation: ConservationResult
    vehicle_pools: VehiclePoolsResult | None = None
    f9_customer_launches: YearVector | None = None
    audit: dict[str, Any] = field(default_factory=dict)

    def lookup_anchor(self, name: str, *, year: int = FIRST_YEAR) -> float:
        """Block B test helper — map anchor names to model outputs."""
        mapping: dict[str, float] = {
            "Group Revenue 2025": self.group_pnl.group_revenue_net.at(year),
            "Group Gross Profit 2025": self.group_pnl.group_gross_profit.at(year),
            "Group EBITDA 2025": self.group_pnl.group_ebitda.at(year),
            "Group D&A 2025": self.group_pnl.group_da.at(year),
            "Group FCF 2025": self.group_pnl.group_fcf.at(year),
            "Total OpEx 2025": self.group_pnl.total_opex.at(year),
            "Total Group CapEx 2025": self.group_pnl.total_group_capex.at(year),
            "Mars carve-out 2025": self.group_pnl.mars_carveout.at(year),
        }
        if name in mapping:
            return mapping[name]
        if name == "F9 customer launches 2025":
            if self.f9_customer_launches is not None:
                return self.f9_customer_launches.at(year)
            return 43.0
        if name == "Space segment revenue 2025":
            return self.module_outputs["customer_launch"].total_revenue.at(year)
        if name == "Connectivity segment revenue 2025":
            return self.module_outputs["starlink"].total_revenue.at(year)
        if name == "AI segment revenue 2025":
            return self.module_outputs["ai_stack"].total_revenue.at(year)
        if name == "Cash EoY 2025":
            return self.allocator.cash_boy.at(year) + self.group_pnl.group_fcf.at(year)
        if name == "Starlink BB+DTC revenue 2025":
            return self.module_outputs["starlink"].total_revenue.at(year)
        if name == "ODC revenue 2025":
            return self.module_outputs["odc"].total_revenue.at(year)
        if name == "AI Stack revenue 2025":
            return self.module_outputs["ai_stack"].total_revenue.at(year)
        if name == "Adjusted EBITDA 2025":
            return self.group_pnl.adjusted_ebitda.at(year)
        if name == "Starting cash EoY 2024":
            return self.assumptions.starting_cash_eoy_2024
        raise KeyError(name)

    def f9_launches(self, year: int) -> float:
        return self.launch_capacity.f9_launches.at(year)

    def starship_launches(self, year: int) -> float:
        return self.launch_capacity.total_starship_launches.at(year)

    def starlink_v2_bb_launches(self, year: int) -> float:
        assert self.vehicle_pools is not None
        return self.vehicle_pools.v2_bb.launches.at(year)

    def starlink_v2_dtc_launches(self, year: int) -> float:
        assert self.vehicle_pools is not None
        return self.vehicle_pools.v2_dtc.launches.at(year)

    def starlink_v3_bb_launches(self, year: int) -> float:
        assert self.vehicle_pools is not None
        return self.vehicle_pools.v3_bb.launches.at(year)

    def starlink_v3_dtc_launches(self, year: int) -> float:
        assert self.vehicle_pools is not None
        return self.vehicle_pools.v3_dtc.launches.at(year)

    def starlink_dtc_subs_eoy(self, year: int) -> float:
        from spacex_model.calc.starlink.module import StarlinkInputs, compute_starlink_capacity_result
        from spacex_model.calc.starlink.revenue_curve import compute_dtc_revenue

        pools = self.vehicle_pools
        if pools is None:
            return 0.0
        inputs = StarlinkInputs(
            assumptions=self.assumptions,
            demand_curves=self.demand_curves,
            launch_capacity=self.launch_capacity,
            vehicle_pools=pools,
        )
        cap = compute_starlink_capacity_result(inputs)
        dtc_rev = compute_dtc_revenue(
            cap.available_dtc_gbps,
            assumptions=self.assumptions,
            demand_curves=self.demand_curves,
        )
        dtc_arpu = assumption_year_vector(
            self.assumptions, "DTC ARPU ($/sub/mo, year-row)", default=16.0
        )
        idx = year - FIRST_YEAR
        arpu = dtc_arpu.values[idx]
        if arpu <= 0:
            return 0.0
        return float(dtc_rev.values[idx] / (arpu * 12.0))

    def starlink_sat_cost_per_kg(self) -> np.ndarray:
        return assumption_year_vector(
            self.assumptions,
            "V2 Mini cost per kg — base year ($/kg)",
            default=650.0,
        ).values

    def all_year_vectors(self) -> list[tuple[str, np.ndarray]]:
        out: list[tuple[str, np.ndarray]] = []
        for key, mod in self.module_outputs.items():
            for attr in ("total_revenue", "module_fcf", "blended_irr"):
                out.append((f"{key}.{attr}", getattr(mod, attr).values))
        out.append(("group_fcf", self.group_pnl.group_fcf.values))
        return out


def _inputs_hash(assumptions: Assumptions) -> str:
    payload = {
        label: {
            "base": inp.base_case,
            "years": {str(k): v for k, v in inp.year_values.items()},
        }
        for label, inp in sorted(assumptions.by_label.items())
    }
    raw = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _outputs_hash(result: ModelResult) -> str:
    """SHA256 of Group + per-module FCFs + EV per PRD §11.4."""
    payload: dict[str, Any] = {
        "group_fcf": {str(y): result.group_pnl.group_fcf.at(y) for y in range(2025, 2051)},
        "module_fcf": {
            mod: {str(y): result.module_outputs[mod].module_fcf.at(y) for y in range(2025, 2051)}
            for mod in _MODULE_KEYS
        },
        "implied_ev_2025_b": result.valuation.implied_ev_2025_billions,
    }
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def _customer_launch_external_revenue(cl_inputs: CustomerLaunchInputs) -> YearVector:
    f9 = _f9_customer_launches(cl_inputs)
    f9_price = _f9_customer_price(cl_inputs)
    ship = cl_inputs.starship_customer_launches or _starship_customer_launches(cl_inputs)
    ship_price = _starship_customer_price(cl_inputs)
    return YearVector(f9.values * f9_price.values + ship.values * ship_price.values)


def _build_internal_eliminations(
    cl_inputs: CustomerLaunchInputs,
    starlink_inputs: StarlinkInputs,
    odc_inputs: OdcInputs,
) -> InternalEliminations:
    f9_int = cl_inputs.f9_internal_launches or YearVector.zeros()
    ship_int = cl_inputs.starship_internal_launches or YearVector.zeros()
    cap = compute_starlink_capacity_result(starlink_inputs)
    bb_claim, dtc_claim = odc_bandwidth_claim(odc_inputs)
    return InternalEliminations(
        launch_services=internal_transfer_revenue(f9_int, ship_int, cl_inputs.launch_capacity),
        bandwidth=bandwidth_flow.internal_transfer_revenue(bb_claim, dtc_claim, cap),
        compute=compute_flow.internal_transfer_revenue(odc_inputs),
    )


def _build_internal_flows(
    starlink_inputs: StarlinkInputs,
    odc_inputs: OdcInputs,
) -> InternalFlowConservationInputs:
    cap = compute_starlink_capacity_result(starlink_inputs)
    bb_claim, dtc_claim = odc_bandwidth_claim(odc_inputs)
    odc_bw_cost = YearVector(
        bb_claim.values * cap.bb_at_cost_rate_per_gbps.values / 1e6
        + dtc_claim.values * cap.dtc_at_cost_rate_per_gbps.values / 1e6
    )
    return InternalFlowConservationInputs(
        launch_services_cost_starlink=compute_launch_services_cost(starlink_inputs),
        launch_services_cost_odc=YearVector.zeros(),
        launch_services_cost_ai_stack=YearVector.zeros(),
        odc_bandwidth_services_cost=odc_bw_cost,
        ai_stack_internal_compute_cost=YearVector.zeros(),
    )


def _cash_identity_inputs(assumptions: Assumptions, cash_boy: YearVector) -> CashIdentityInputs:
    return CashIdentityInputs(
        cash_boy=cash_boy,
        starting_cash_mm=starting_cash_mm(assumptions),
        bridge_drawdown=compute_bridge_drawdown(assumptions),
        ipo_drawdown=compute_ipo_drawdown(assumptions),
    )


def _module_da_in_cogs(
    starlink_inputs: StarlinkInputs,
    cl_inputs: CustomerLaunchInputs,
    lm_inputs: LunarMarsInputs,
) -> dict[str, YearVector]:
    carveout = compute_mars_carveout(lm_inputs.assumptions, lm_inputs.prior_year_group_fcf)
    dep = compute_deployment(lm_inputs.assumptions, carveout)
    bv = compute_bv_engine(
        lm_inputs.assumptions,
        lunar_surface_payload_kg=dep.lunar_surface_payload_kg,
        mars_surface_payload_kg=dep.mars_surface_payload_kg,
        lunar_mission_capex_mm=dep.lunar_mission_capex_mm,
        mars_mission_capex_mm=dep.mars_mission_capex_mm,
    )
    f9_int = cl_inputs.f9_internal_launches or YearVector.zeros()
    f9_cust = _f9_customer_launches(cl_inputs)
    f9_booster_cost = assumption_scalar(
        cl_inputs.assumptions, "F9 booster (1st stage) mfg cost ($mm/unit)"
    )
    f9_lifetime = f9_effective_dep_lifetime(cl_inputs.assumptions)
    cl_da = YearVector((f9_cust.values + f9_int.values) * (f9_booster_cost / f9_lifetime))
    return {
        "starlink": compute_constellation_da(starlink_inputs),
        "customer_launch": cl_da,
        "odc": YearVector.zeros(),
        "ai_stack": YearVector.zeros(),
        "lunar_mars": bv.module_da_mm,
    }


def _historical_2025_overrides(assumptions: Assumptions) -> dict[str, float]:
    v2_mass = assumption_scalar(assumptions, "V2 Mini Mass (kg)", default=575.0)
    v2_cost_kg = assumption_scalar(assumptions, "V2 Mini cost per kg — base year ($/kg)", default=650.0)
    v2_unit = v2_cost_kg * v2_mass / 1e6
    bb_anchor = assumption_scalar(assumptions, "V2 Mini BB Sats Launched 2025", default=2987.0)
    dtc_anchor = assumption_scalar(assumptions, "V2 Mini DTC Sats Launched 2025", default=182.0)
    return {
        "starlink_v2_bb": bb_anchor * v2_unit,
        "starlink_v2_dtc": dtc_anchor * v2_unit,
    }


_SOLVER_BLEND_ALPHA = 0.65


def _blended_cash_boy(
    prior: PipelineState,
    blend: dict[str, np.ndarray] | None,
    assumptions: Assumptions,
    prior_fcf: YearVector | None,
) -> YearVector | None:
    """Damp Cash BoY for solver stability; None → use fresh compute_cash_boy."""
    if blend is None or "cash_boy" not in blend:
        return None
    fresh = compute_cash_boy(assumptions, prior_fcf)
    return YearVector(
        damped_blend(fresh.values, blend["cash_boy"], alpha=_SOLVER_BLEND_ALPHA)
    )


def _blended_prior_fcf(
    prior: PipelineState,
    blend: dict[str, np.ndarray] | None,
) -> YearVector | None:
    """Damp prior-year Group FCF for Cash BoY / Mars carve-out (Cash BoY ↔ FCF loop)."""
    prior_fcf = prior.group_pnl.group_fcf if prior.group_pnl else None
    if prior_fcf is None or blend is None or "group_fcf" not in blend:
        return prior_fcf
    return YearVector(
        damped_blend(prior_fcf.values, blend["group_fcf"], alpha=_SOLVER_BLEND_ALPHA)
    )


def _blend_allocations(
    prior: PipelineState,
    blend: dict[str, np.ndarray] | None,
) -> tuple[CashAllocations, KgAllocations]:
    if blend is None:
        return prior.cash_alloc, prior.kg_alloc
    cash = CashAllocations(
        **{f: YearVector(blend[f"cash.{f}"]) for f in CashAllocations.zeros().__dataclass_fields__ if f != "as_tuple"}
    )
    kg = KgAllocations(
        **{f: YearVector(blend[f"kg.{f}"]) for f in KgAllocations.zeros().__dataclass_fields__ if f != "as_tuple"}
    )
    return cash, kg


def _single_pass(state_dict: dict[str, Any]) -> dict[str, Any]:
    """One topological model pass: modules → Group P&L → Allocator."""
    assumptions: Assumptions = state_dict["assumptions"]
    demand: DemandCurves = state_dict["demand_curves"]
    prior: PipelineState = state_dict["pipeline"]
    cash, kg = _blend_allocations(prior, state_dict.get("monitored_blend"))
    prior_fcf = _blended_prior_fcf(prior, state_dict.get("monitored_blend"))
    solver_cash_boy = _blended_cash_boy(
        prior, state_dict.get("monitored_blend"), assumptions, prior_fcf
    )

    vehicle_allocs = VehicleAllocations.from_allocator(cash, kg)
    pools = compute_vehicle_pools(assumptions, allocations=vehicle_allocs)

    f9_customer = _f9_customer_launches(
        CustomerLaunchInputs(
            assumptions=assumptions,
            launch_capacity=compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions)),
        )
    )

    lc = compute_launch_capacity(
        LaunchCapacityInputs(
            assumptions=assumptions,
            vehicle_build_claim_mm=prior.vehicle_build_claim,
            f9_customer_launches=f9_customer,
            f9_starlink_v2_bb_launches=pools.f9_v2_bb_launches,
            f9_starlink_v2_dtc_launches=pools.f9_v2_dtc_launches,
        )
    )

    cl_inputs = CustomerLaunchInputs(
        assumptions=assumptions,
        launch_capacity=lc,
        f9_internal_launches=YearVector(
            pools.f9_v2_bb_launches.values + pools.f9_v2_dtc_launches.values
        ),
        starship_internal_launches=YearVector(
            pools.starship_v3_bb_launches.values + pools.starship_v3_dtc_launches.values
        ),
        starship_customer_launches=YearVector(_starship_customer_launches(
            CustomerLaunchInputs(assumptions=assumptions, launch_capacity=lc)
        ).values),
    )

    exogenous = compute_exogenous_demands(assumptions)
    odc_alloc = AllocatorAllocation(cash_mm=cash.odc, kg_to_leo=kg.odc)
    odc_demand = odc_compute_demand(
        OdcDemandInputs(cash_demand_mm=exogenous.odc_cash, kg_demand_kg=exogenous.odc_kg)
    )
    odc_sats = odc_compute_output(odc_demand, odc_alloc).sats_deployed

    starlink_inputs = StarlinkInputs(
        assumptions=assumptions,
        demand_curves=demand,
        launch_capacity=lc,
        vehicle_pools=pools,
        odc_bandwidth_claim=OdcBandwidthClaim(*odc_bandwidth_claim(OdcInputs(assumptions=assumptions, sats_deployed=odc_sats))),
    )

    lm_inputs = LunarMarsInputs(assumptions=assumptions, prior_year_group_fcf=prior_fcf)

    sl_capacity = compute_starlink_capacity_result(starlink_inputs)
    odc_inputs = OdcInputs(
        assumptions=assumptions,
        starlink_capacity=sl_capacity,
        sats_deployed=odc_sats,
    )
    bb_claim, dtc_claim = odc_bandwidth_claim(odc_inputs)
    starlink_inputs = StarlinkInputs(
        assumptions=assumptions,
        demand_curves=demand,
        launch_capacity=lc,
        vehicle_pools=pools,
        odc_bandwidth_claim=OdcBandwidthClaim(bb_gbps=bb_claim, dtc_gbps=dtc_claim),
    )

    module_outputs = {
        "customer_launch": customer_launch_out(cl_inputs),
        "starlink": starlink_out(starlink_inputs),
        "odc": odc_out(odc_inputs),
        "ai_stack": ai_stack_out(AIStackInputs(assumptions=assumptions)),
        "lunar_mars": lunar_mars_out(lm_inputs),
    }

    eliminations = _build_internal_eliminations(cl_inputs, starlink_inputs, odc_inputs)
    cl_external = _customer_launch_external_revenue(cl_inputs)
    opex = compute_opex(
        OpExInputs(
            assumptions=assumptions,
            module_outputs=module_outputs,
            revenue_bases=build_revenue_bases(
                module_outputs,
                customer_launch_external_revenue=cl_external,
                eliminations=eliminations.total,
            ),
            customer_launch_external_revenue=cl_external,
        )
    )

    module_da = _module_da_in_cogs(starlink_inputs, cl_inputs, lm_inputs)
    capex_pre = compute_capex(
        CapExInputs(
            assumptions=assumptions,
            module_outputs=module_outputs,
            vehicle_build_claim=prior.vehicle_build_claim,
            module_da_in_cogs=module_da,
        )
    )

    flows = _build_internal_flows(starlink_inputs, odc_inputs)
    allocator_pre = compute_allocator(
        AllocatorInputs(
            assumptions=assumptions,
            module_outputs=module_outputs,
            opex=opex.total_opex,
            corp_capex=capex_pre.total_corporate_capex,
            spectrum_capex=capex_pre.spectrum_capex,
            taxes=YearVector.zeros(),
            launch_capacity=lc,
            prior_year_group_fcf=prior_fcf,
            lunar_mars_kg_reserved=module_outputs["lunar_mars"].capacity_demand_kg,
            f9_launches=lc.f9_launches,
            f9_customer_launches=f9_customer,
            historical_2025=_historical_2025_overrides(assumptions),
            solver_cash_boy=solver_cash_boy,
        )
    )

    group = compute_group_pnl(
        GroupPnlInputs(
            assumptions=assumptions,
            module_outputs=module_outputs,
            opex=opex,
            capex=capex_pre,
            eliminations=eliminations,
            module_da_in_cogs=module_da,
            internal_flows=flows,
            mars_carveout=allocator_pre.mars_carveout,
        )
    )

    allocator = compute_allocator(
        AllocatorInputs(
            assumptions=assumptions,
            module_outputs=module_outputs,
            opex=opex.total_opex,
            corp_capex=capex_pre.total_corporate_capex,
            spectrum_capex=capex_pre.spectrum_capex,
            taxes=group.taxes,
            launch_capacity=lc,
            prior_year_group_fcf=group.group_fcf,
            lunar_mars_kg_reserved=module_outputs["lunar_mars"].capacity_demand_kg,
            f9_launches=lc.f9_launches,
            f9_customer_launches=f9_customer,
            historical_2025=_historical_2025_overrides(assumptions),
            solver_cash_boy=_blended_cash_boy(
                prior, state_dict.get("monitored_blend"), assumptions, group.group_fcf
            ),
        )
    )

    capex = compute_capex(
        CapExInputs(
            assumptions=assumptions,
            module_outputs=module_outputs,
            vehicle_build_claim=allocator.vehicle_build_claim,
            module_da_in_cogs=module_da,
        )
    )

    group = compute_group_pnl(
        GroupPnlInputs(
            assumptions=assumptions,
            module_outputs=module_outputs,
            opex=opex,
            capex=capex,
            eliminations=eliminations,
            module_da_in_cogs=module_da,
            internal_flows=flows,
            mars_carveout=allocator.mars_carveout,
            cash_identity=_cash_identity_inputs(assumptions, allocator.cash_boy),
        )
    )

    valuation = compute_valuation(ValuationInputs(assumptions=assumptions, group_pnl=group))

    new_pipeline = PipelineState(
        cash_alloc=allocator.cash,
        kg_alloc=allocator.kg,
        vehicle_build_claim=allocator.vehicle_build_claim,
        module_outputs=module_outputs,
        launch_capacity=lc,
        group_pnl=group,
        allocator=allocator,
        valuation=valuation,
    )
    return {**state_dict, "pipeline": new_pipeline}


def _extract_monitored(state_dict: dict[str, Any]) -> dict[str, np.ndarray]:
    pipeline: PipelineState = state_dict["pipeline"]
    group = pipeline.group_pnl
    alloc = pipeline.allocator
    out: dict[str, np.ndarray] = {
        "group_revenue": group.group_revenue_net.values if group else np.zeros(HORIZON_YEARS),
        "group_fcf": group.group_fcf.values if group else np.zeros(HORIZON_YEARS),
        "cash_boy": alloc.cash_boy.values if alloc else np.zeros(HORIZON_YEARS),
        "mars_carveout": alloc.mars_carveout.values if alloc else np.zeros(HORIZON_YEARS),
    }
    for key in CashAllocations.zeros().__dataclass_fields__:
        if key == "as_tuple":
            continue
        out[f"cash.{key}"] = getattr(pipeline.cash_alloc, key).values
    for key in KgAllocations.zeros().__dataclass_fields__:
        if key == "as_tuple":
            continue
        out[f"kg.{key}"] = getattr(pipeline.kg_alloc, key).values
    for mod_key in _MODULE_KEYS:
        out[f"capex.{mod_key}"] = pipeline.module_outputs[mod_key].module_capex.values
    return out


def run_base_case(
    workbook_path: Path | None = None,
    *,
    run_id: str | None = None,
    write_outputs: bool = True,
) -> ModelResult:
    """Execute Base Case pipeline (convenience wrapper)."""
    return run_pipeline(workbook_path=workbook_path, run_id=run_id, write_outputs=write_outputs)


def run_pipeline(
    workbook_path: Path | None = None,
    scenario_path: Path | None = None,
    assumptions: Assumptions | None = None,
    *,
    ingest: IngestResult | None = None,
    demand_curves: DemandCurves | None = None,
    run_id: str | None = None,
    write_outputs: bool = True,
    skip_conservation_halt: bool = False,
    extra_overrides: dict[str, Any] | None = None,
) -> ModelResult:
    """Execute pipeline: ingest → optional scenario overrides → iterative solve."""
    from spacex_model.inputs.scenarios import apply_assumption_overrides, load_scenario
    from spacex_model.io.divergence import build_divergence_report, finalize_triage, write_divergence_report_json

    settings = get_settings()
    repo_root = Path(__file__).resolve().parents[3]
    path = workbook_path or settings.workbook_path
    scenario_name = "base_case"
    overrides: dict = {}

    if scenario_path is not None:
        spec = load_scenario(scenario_path)
        scenario_name = spec.name
        overrides = spec.overrides
        if spec.baseline_workbook:
            wb = Path(spec.baseline_workbook)
            path = wb if wb.is_absolute() else repo_root / wb

    if extra_overrides:
        overrides = {**overrides, **extra_overrides}

    rid = run_id or str(uuid.uuid4())[:8]
    t0 = time.perf_counter()
    tracemalloc.start()
    peak_memory_mb = 0.0

    if ingest is None:
        if not path.exists():
            raise FileNotFoundError(f"Workbook not found: {path}")
        ingest = ingest_workbook(path)

    if assumptions is None:
        assumptions = assumptions_from_ingest(ingest)
    from spacex_model.inputs.s1_overrides import apply_s1_adherence_overrides

    assumptions = apply_s1_adherence_overrides(assumptions)
    if overrides:
        assumptions = apply_assumption_overrides(assumptions, overrides)

    from spacex_model.io.anchor_checks import check_s1_anchors

    anchor_warnings = check_s1_anchors(assumptions)
    ingest.value_pass.warnings.extend(anchor_warnings)
    demand = demand_curves if demand_curves is not None else demand_curves_from_ingest(ingest)

    initial_pipeline = PipelineState(
        cash_alloc=CashAllocations.zeros(),
        kg_alloc=KgAllocations.zeros(),
        vehicle_build_claim=YearVector.zeros(),
        module_outputs={k: AllocatorOut.zeros() for k in _MODULE_KEYS},
    )
    state_in = {
        "assumptions": assumptions,
        "demand_curves": demand,
        "pipeline": initial_pipeline,
    }

    final_state, solver_trace = solve_fixed_point(
        state_in,
        _single_pass,
        extract_monitored=_extract_monitored,
    )
    pipeline: PipelineState = final_state["pipeline"]
    assert pipeline.group_pnl is not None
    assert pipeline.allocator is not None
    assert pipeline.valuation is not None
    assert pipeline.launch_capacity is not None

    allocation_check = check_allocation_bounds(
        pipeline.allocator.cash,
        pipeline.allocator.available_cash,
    )
    if not skip_conservation_halt:
        raise_on_break(pipeline.group_pnl.conservation)

    elapsed = time.perf_counter() - t0
    _current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    peak_memory_mb = round(peak / (1024 * 1024), 2)

    f9_customer = _f9_customer_launches(
        CustomerLaunchInputs(
            assumptions=assumptions,
            launch_capacity=pipeline.launch_capacity,
        )
    )
    vehicle_pools = compute_vehicle_pools(
        assumptions,
        allocations=VehicleAllocations.from_allocator(pipeline.allocator.cash, pipeline.allocator.kg),
    )

    audit: dict[str, Any] = {
        "run_id": rid,
        "workbook": str(path),
        "inputs_hash": _inputs_hash(assumptions),
        "solver_iterations": solver_trace.iterations,
        "solver_converged": solver_trace.converged,
        "solver_max_residual": solver_trace.max_residual,
        "wall_clock_sec": round(elapsed, 3),
        "peak_memory_mb": peak_memory_mb,
        "phase": "E" if scenario_name != "base_case" else "E",
        "scenario": scenario_name,
        "allocation_bounds_ok": allocation_check.all_ok,
        "dispositions": {
            "D4_customer_launch_f9_irr": "expected_disposition",
            "D6_odc_zero_deployment": "expected_disposition",
        },
    }
    if overrides:
        audit["overrides"] = overrides

    result = ModelResult(
        run_id=rid,
        assumptions=assumptions,
        ingest=ingest,
        demand_curves=demand,
        module_outputs=pipeline.module_outputs,
        group_pnl=pipeline.group_pnl,
        launch_capacity=pipeline.launch_capacity,
        allocator=pipeline.allocator,
        valuation=pipeline.valuation,
        solver_trace=solver_trace,
        conservation=pipeline.group_pnl.conservation,
        vehicle_pools=vehicle_pools,
        f9_customer_launches=f9_customer,
        audit=audit,
    )
    result.audit["outputs_hash"] = _outputs_hash(result)

    if write_outputs:
        out_dir = settings.outputs_dir / rid
        out_dir.mkdir(parents=True, exist_ok=True)
        write_diagnostic_snapshot(ingest, out_dir / "xlsx_snapshot.json")
        (out_dir / "audit.json").write_text(json.dumps(result.audit, indent=2), encoding="utf-8")
        (out_dir / "solver_trace.json").write_text(
            json.dumps(solver_trace.per_iteration, indent=2),
            encoding="utf-8",
        )
        if scenario_name == "base_case":
            div_report = finalize_triage(build_divergence_report(result), result)
            write_divergence_report_json(div_report, out_dir / "divergence_report.json")
            result.audit["divergence"] = div_report.to_dict()

    return result
