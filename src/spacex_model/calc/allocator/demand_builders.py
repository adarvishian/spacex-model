"""Exogenous queue demand builders — Sprint 11f Option A (Architecture §6.5)."""

from __future__ import annotations

import numpy as np

from spacex_model.calc.allocator.types import QueueSubBlockDemands
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


def _learning_multiplier(assumptions: Assumptions) -> np.ndarray:
    lr = assumption_scalar(assumptions, cl.SATELLITE_COST_PER_KG_LEARNING_RATE, default=0.0)
    offsets = np.arange(HORIZON_YEARS, dtype=np.float64)
    return np.power(1.0 + lr, offsets)


def _unit_cost_mm_vec(
    assumptions: Assumptions,
    unit_cost_label: str,
    *,
    cost_kg: float,
    mass_kg: float,
) -> np.ndarray:
    """Unit cost ($mm/sat) with cost_kg × mass fallback when Assumptions row is empty."""
    vec = assumption_year_vector(assumptions, unit_cost_label, default=0.0).values
    fallback = cost_kg * mass_kg / 1e6
    if np.all(vec == 0.0):
        return np.full(HORIZON_YEARS, fallback, dtype=np.float64)
    return np.where(vec > 0.0, vec, fallback)


def _v2_vehicle_cash_demand(
    assumptions: Assumptions,
    *,
    launch_anchor_label: str,
    unit_cost_label: str,
    facility_per_sat_label: str,
    default_anchor: float,
    cost_kg: float,
    mass_kg: float,
) -> tuple[YearVector, np.ndarray]:
    """Anchor launches × learning × (unit cost + facility) — Sprint 11f Option A."""
    anchor = assumption_scalar(assumptions, launch_anchor_label, default=default_anchor)
    unit_cost = _unit_cost_mm_vec(
        assumptions, unit_cost_label, cost_kg=cost_kg, mass_kg=mass_kg
    )
    facility = assumption_year_vector(assumptions, facility_per_sat_label, default=0.0).values
    learn = _learning_multiplier(assumptions)
    launch_equiv = anchor * learn
    cash = launch_equiv * (unit_cost + facility)
    return YearVector(cash), launch_equiv


def _v3_vehicle_cash_kg_demand(
    assumptions: Assumptions,
    *,
    stub_trajectory_label: str,
    unit_cost_label: str,
    facility_per_sat_label: str,
    mass_kg: float,
) -> tuple[YearVector, YearVector, np.ndarray]:
    """V3 stub launch trajectory × unit cost + facility; kg = launches × mass."""
    launches = assumption_year_vector(assumptions, stub_trajectory_label, default=0.0).values
    unit_cost = assumption_year_vector(assumptions, unit_cost_label, default=0.0).values
    facility = assumption_year_vector(assumptions, facility_per_sat_label, default=0.0).values
    cash = launches * (unit_cost + facility)
    kg = launches * mass_kg
    return YearVector(cash), YearVector(kg), launches


def compute_exogenous_demands(assumptions: Assumptions) -> QueueSubBlockDemands:
    """Build exogenous cash/kg queue demands from anchors and assumptions.

    Excel cell:        Allocator!D48:AC48 (V2 BB cash demand row)
    Excel label:       "Starlink V2 BB cash demand ($mm)"
    Architecture ref:  §6.5 / §20.3 (Sprint 11f Option A)
    Principle:         12 (demand purely exogenous; output never feeds back)

    """
    a = assumptions
    learn = _learning_multiplier(a)

    cost_kg = assumption_scalar(a, cl.SATELLITE_COST_PER_KG_BASE_YEAR_KG, default=650.0)
    v2_mass = assumption_scalar(a, cl.V2_MINI_MASS_KG, default=575.0)

    v2_bb_cash, v2_bb_launches = _v2_vehicle_cash_demand(
        a,
        launch_anchor_label=cl.V2_MINI_BB_SATS_LAUNCHED_2025,
        unit_cost_label=cl.V2_BB_SAT_UNIT_COST_MM_SAT,
        facility_per_sat_label=cl.V2_BB_FACILITY_CAPEX_PER_SAT_MM_SAT,
        default_anchor=2987.0,
        cost_kg=cost_kg,
        mass_kg=v2_mass,
    )
    v2_dtc_cash, v2_dtc_launches = _v2_vehicle_cash_demand(
        a,
        launch_anchor_label=cl.V2_MINI_DTC_SATS_LAUNCHED_2025,
        unit_cost_label=cl.V2_DTC_SAT_UNIT_COST_MM_SAT,
        facility_per_sat_label=cl.V2_DTC_FACILITY_CAPEX_PER_SAT_MM_SAT,
        default_anchor=182.0,
        cost_kg=cost_kg,
        mass_kg=v2_mass,
    )

    v3_mass = assumption_scalar(a, cl.V3_MASS_KG, default=2000.0)
    v3_bb_cash, v3_bb_kg, _ = _v3_vehicle_cash_kg_demand(
        a,
        stub_trajectory_label=cl.V3_BB_LAUNCHES_PER_YEAR_STUB_TRAJECTORY,
        unit_cost_label=cl.V3_BB_SAT_UNIT_COST_MM_SAT,
        facility_per_sat_label=cl.V3_BB_FACILITY_CAPEX_PER_SAT_MM_SAT,
        mass_kg=v3_mass,
    )
    v3_dtc_cash, v3_dtc_kg, _ = _v3_vehicle_cash_kg_demand(
        a,
        stub_trajectory_label=cl.V3_DTC_LAUNCHES_PER_YEAR_STUB_TRAJECTORY,
        unit_cost_label=cl.V3_DTC_SAT_UNIT_COST_MM_SAT,
        facility_per_sat_label=cl.V3_DTC_FACILITY_CAPEX_PER_SAT_MM_SAT,
        mass_kg=v3_mass,
    )

    cl_cash_default = assumption_year_vector(
        a,
        cl.CUSTOMER_LAUNCH_CASH_DEMAND_LARGE_DEFAULT_MM,
        default=0.0,
    )
    cl_rev_pct = assumption_scalar(
        a,
        "Customer Launch ground equipment CapEx % of revenue",
        default=0.005,
    )
    cl_rev_traj = assumption_year_vector(
        a,
        cl.CUSTOMER_LAUNCH_REVENUE_TRAJECTORY_STUB_MM,
        default=0.0,
    )
    cl_from_rev = cl_rev_traj.values * cl_rev_pct
    cl_cash = YearVector(np.where(cl_from_rev > 0, cl_from_rev, cl_cash_default.values))

    cl_kg_traj = assumption_year_vector(
        a,
        cl.CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_KG_DEMAND_STUB_KG,
        default=0.0,
    )
    upmass = assumption_scalar(
        a,
        cl.STARSHIP_PAYLOAD_2025_BASELINE_KG_TO_LEO_FULLY_REUSABLE_MODE,
        default=100_000.0,
    )
    cl_launches = assumption_year_vector(
        a,
        cl.CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_LAUNCHES_STUB,
        default=0.0,
    )
    cl_kg = YearVector(np.maximum(cl_kg_traj.values, cl_launches.values * upmass))

    odc_cash = assumption_year_vector(a, cl.ODC_CASH_DEMAND_LARGE_DEFAULT_MM, default=0.0)
    odc_kg = assumption_year_vector(a, cl.ODC_KG_DEMAND_LARGE_DEFAULT_KG, default=0.0)

    ai_cash = YearVector.zeros()
    ai_kg = YearVector.zeros()

    _ = v2_bb_launches, v2_dtc_launches, learn

    return QueueSubBlockDemands(
        customer_launch_cash=cl_cash,
        starlink_v2_bb_cash=v2_bb_cash,
        starlink_v2_dtc_cash=v2_dtc_cash,
        starlink_v3_bb_cash=v3_bb_cash,
        starlink_v3_dtc_cash=v3_dtc_cash,
        odc_cash=odc_cash,
        ai_stack_cash=ai_cash,
        customer_launch_kg=cl_kg,
        starlink_v3_bb_kg=v3_bb_kg,
        starlink_v3_dtc_kg=v3_dtc_kg,
        odc_kg=odc_kg,
        ai_stack_kg=ai_kg,
    )
