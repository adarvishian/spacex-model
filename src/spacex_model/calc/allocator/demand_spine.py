"""Unified exogenous kg demand spine — one deployable-demand per program (U0 / F4).

De-inflates Starlink desired kg: realistic deployment × mass, not saturation-headroom × mass.
R102 ≡ memo total kg demand; fleet sizing, rationing, and binding flag read the same total.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc.allocator.priority import ModuleSpotIrrs
from spacex_model.calc.allocator.types import QueueSubBlockDemands
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class UnifiedKgDemands:
    """One exogenous kg demand per CAE module; total ≡ memo (R102 ≡ R46)."""

    starlink: YearVector
    customer_launch: YearVector
    ai_compute: YearVector
    total: YearVector

    def as_module_spot_irrs(self) -> ModuleSpotIrrs:
        return ModuleSpotIrrs(
            starlink=self.starlink,
            customer_launch=self.customer_launch,
            ai_compute=self.ai_compute,
        )

    def forward_kg_by_program(self, lunar_mars_kg: YearVector | None = None) -> dict[str, YearVector]:
        """Vehicle-build forward aggregate — VB R104 spine (retired orphan R67)."""
        z = YearVector.zeros()
        return {
            "starlink": self.starlink,
            "customer_launch": self.customer_launch,
            "odc": self.ai_compute,
            "lunar_mars": lunar_mars_kg or z,
        }


def compute_kg_binding_flag(
    total_desired_launch_kg: YearVector,
    capacity_after_lm: YearVector,
) -> YearVector:
    """Honest kg-binding flag: IF(R102 > capacity_after_lm) — U0 / superseded R49.

    Excel cell:        Cash Allocation Engine!D49
    Excel label:       "Kg demand binding flag (1 = binding)"
    Architecture ref:  PRD U0 demand-spine; U4 retired pro-rata R49 shim
    Principle:         12 (reads unified R102 total, not inflated R46)

    """
    binding = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        cap = capacity_after_lm.values[t]
        td = total_desired_launch_kg.values[t]
        binding[t] = 1.0 if td > cap and cap > 0.0 else 0.0
    return YearVector(binding)


def _sub_block_starlink_kg(sub_demands: QueueSubBlockDemands) -> YearVector:
    return YearVector(
        sub_demands.starlink_v3_bb_kg.values + sub_demands.starlink_v3_dtc_kg.values
    )


def _sub_block_ai_kg(sub_demands: QueueSubBlockDemands) -> YearVector:
    return YearVector(sub_demands.odc_kg.values + sub_demands.ai_stack_kg.values)


def compute_starlink_exogenous_kg_demand(
    assumptions: Assumptions,
    sub_demands: QueueSubBlockDemands,
) -> YearVector:
    """Realistic Starlink launch kg — deployment trajectory × mass, not saturation headroom.

    Excel cell:        Starlink!D159 (Kg demand year N+1)
    Excel label:       "Kg demand year N+1"
    Architecture ref:  U0 demand-spine (de-inflate CAE R99)
    Principle:         12 (exogenous demand only; no saturation-headroom inflation)

    """
    sub_kg = _sub_block_starlink_kg(sub_demands)
    if np.any(sub_kg.values > 0.0):
        return sub_kg

    v3_mass = assumption_scalar(assumptions, cl.V3_MASS_KG, default=2000.0)
    v3_bb_launches = assumption_year_vector(
        assumptions, cl.V3_BB_LAUNCHES_PER_YEAR_STUB_TRAJECTORY, default=0.0
    ).values
    v3_dtc_launches = assumption_year_vector(
        assumptions, cl.V3_DTC_LAUNCHES_PER_YEAR_STUB_TRAJECTORY, default=0.0
    ).values
    realistic = (v3_bb_launches + v3_dtc_launches) * v3_mass

    v2_mass = assumption_scalar(assumptions, cl.V2_MINI_MASS_KG, default=575.0)
    bb_anchor = assumption_scalar(assumptions, cl.V2_MINI_BB_SATS_LAUNCHED_2025, default=2987.0)
    dtc_anchor = assumption_scalar(assumptions, cl.V2_MINI_DTC_SATS_LAUNCHED_2025, default=182.0)
    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        if year == FIRST_YEAR:
            realistic[t] = max(realistic[t], (bb_anchor + dtc_anchor) * v2_mass)

    return YearVector(realistic)


def compute_customer_launch_exogenous_kg_demand(
    assumptions: Assumptions,
    sub_demands: QueueSubBlockDemands,
) -> YearVector:
    """Customer Launch kg demand year N+1 — external Starship launches × payload.

    Excel cell:        Customer Launch!D115
    Excel label:       "Kg demand year N+1"
    Architecture ref:  U0 demand-spine
    Principle:         12 (exogenous demand only)

    """
    if np.any(sub_demands.customer_launch_kg.values > 0.0):
        return sub_demands.customer_launch_kg

    upmass = assumption_scalar(
        assumptions,
        cl.STARSHIP_PAYLOAD_2025_BASELINE_KG_TO_LEO_FULLY_REUSABLE_MODE,
        default=100_000.0,
    )
    launches = assumption_year_vector(
        assumptions,
        cl.CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_LAUNCHES_STUB,
        default=0.0,
    ).values
    kg_traj = assumption_year_vector(
        assumptions,
        cl.CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_KG_DEMAND_STUB_KG,
        default=0.0,
    ).values
    return YearVector(np.maximum(kg_traj, launches * upmass))


def compute_ai_compute_exogenous_kg_demand(
    assumptions: Assumptions,
    sub_demands: QueueSubBlockDemands,
) -> YearVector:
    """AI-Compute orbital kg demand year N+1 (Terrestrial is cash-only).

    Excel cell:        AI - Compute!D15
    Excel label:       "Kg demand year N+1"
    Architecture ref:  U0 demand-spine
    Principle:         12 (exogenous demand only)

    """
    sub_kg = _sub_block_ai_kg(sub_demands)
    if np.any(sub_kg.values > 0.0):
        return sub_kg
    return assumption_year_vector(assumptions, cl.ODC_KG_DEMAND_LARGE_DEFAULT_KG, default=0.0)


def compute_unified_kg_demands(
    assumptions: Assumptions,
    sub_demands: QueueSubBlockDemands,
) -> UnifiedKgDemands:
    """One realistic exogenous deployable-demand per program; total ≡ memo (R102 ≡ R46).

    Excel cell:        Cash Allocation Engine!D99:D102 / D46
    Excel label:       "Desired launch kg: Starlink" … "Total desired launch kg"
    Architecture ref:  PRD U0 / F4 demand-spine unification
    Principle:         12 (demand⊥output; no saturation-headroom inflation)

    """
    starlink = compute_starlink_exogenous_kg_demand(assumptions, sub_demands)
    customer_launch = compute_customer_launch_exogenous_kg_demand(assumptions, sub_demands)
    ai_compute = compute_ai_compute_exogenous_kg_demand(assumptions, sub_demands)
    total = YearVector(
        starlink.values + customer_launch.values + ai_compute.values
    )
    return UnifiedKgDemands(
        starlink=starlink,
        customer_launch=customer_launch,
        ai_compute=ai_compute,
        total=total,
    )
