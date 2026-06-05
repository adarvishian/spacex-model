"""Segment P&L — read-only presentation waterfall tying to Group P&L (V4.113 tab)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.ai_compute.module import AiComputeInputs, compute_ai_apps_revenue_line, compute_orbital_dc_revenue, compute_terrestrial_dc_revenue_line
from spacex_model.calc.customer_launch.module import CustomerLaunchInputs, compute_launch_development_revenue_memo, compute_launch_services_revenue_memo
from spacex_model.calc.group_pnl import GroupPnlResult
from spacex_model.calc.starlink.module import (
    StarlinkInputs,
    compute_hardware_revenue,
    compute_starlink_capacity_result,
    compute_starshield_revenue,
)
from spacex_model.calc.starlink.revenue_curve import compute_bb_revenue, compute_dtc_revenue
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.conservation import InternalEliminations

_MODULE_KEYS = ("customer_launch", "starlink", "ai_compute", "lunar_mars")


@dataclass(frozen=True, slots=True)
class SegmentPnlInputs:
    """Upstream inputs for Segment P&L presentation."""

    group_pnl: GroupPnlResult
    module_outputs: dict[str, AllocatorOut]
    eliminations: InternalEliminations
    starlink_inputs: StarlinkInputs | None = None
    customer_launch_inputs: CustomerLaunchInputs | None = None
    ai_compute_inputs: AiComputeInputs | None = None


@dataclass(frozen=True, slots=True)
class SegmentPnlResult:
    """Segment P&L sub-lines + tie-out memos (must ≈ 0)."""

    starlink_bb_revenue: YearVector
    starlink_dtc_revenue: YearVector
    starlink_starshield_revenue: YearVector
    starlink_hardware_revenue: YearVector
    starlink_subtotal_revenue: YearVector
    customer_launch_services_revenue: YearVector
    customer_launch_development_revenue: YearVector
    customer_launch_subtotal_revenue: YearVector
    ai_orbital_dc_revenue: YearVector
    ai_terrestrial_dc_revenue: YearVector
    ai_apps_revenue: YearVector
    ai_compute_subtotal_revenue: YearVector
    lunar_mars_revenue: YearVector
    group_revenue: YearVector
    memo_starlink_sub_lines: YearVector
    memo_customer_launch_sub_lines: YearVector
    memo_ai_compute_sub_lines: YearVector
    memo_lunar_mars_sub_line: YearVector
    memo_group_revenue_tie: YearVector


def _tie(actual: YearVector, expected: YearVector) -> YearVector:
    return YearVector(actual.values - expected.values)


def compute_segment_pnl(inputs: SegmentPnlInputs) -> SegmentPnlResult:
    """Build Segment P&L presentation from module sub-lines and Group P&L.

    Excel cell:        Segment P&L!—
    Excel label:       "Segment P&L — full Group waterfall ..."
    Architecture ref:  §15 presentation roll-up
    Principle:         3 (read-only; ties to Group P&L)

    """
    sl = inputs.starlink_inputs
    cl_in = inputs.customer_launch_inputs
    ai = inputs.ai_compute_inputs
    mods = inputs.module_outputs

    if sl is not None:
        cap = compute_starlink_capacity_result(sl)
        bb = compute_bb_revenue(cap.available_bb_gbps, assumptions=sl.assumptions, demand_curves=sl.demand_curves)
        dtc = compute_dtc_revenue(cap.available_dtc_gbps, assumptions=sl.assumptions, demand_curves=sl.demand_curves)
        starshield = compute_starshield_revenue(sl)
        hardware = compute_hardware_revenue(sl)
    else:
        z = YearVector.zeros()
        bb = dtc = starshield = hardware = z

    sl_sub = YearVector(bb.values + dtc.values + starshield.values + hardware.values)
    sl_module = mods.get("starlink", AllocatorOut.zeros()).total_revenue

    if cl_in is not None:
        ls = compute_launch_services_revenue_memo(cl_in)
        ld = compute_launch_development_revenue_memo(cl_in)
    else:
        ls = ld = YearVector.zeros()
    cl_sub = YearVector(ls.values + ld.values)
    cl_module = mods.get("customer_launch", AllocatorOut.zeros()).total_revenue

    if ai is not None:
        orbital = compute_orbital_dc_revenue(ai)
        terr = compute_terrestrial_dc_revenue_line(ai)
        apps = compute_ai_apps_revenue_line(ai)
    else:
        orbital = terr = apps = YearVector.zeros()
    ai_sub = YearVector(orbital.values + terr.values + apps.values)
    ai_module = mods.get("ai_compute", AllocatorOut.zeros()).total_revenue

    lm_module = mods.get("lunar_mars", AllocatorOut.zeros()).total_revenue
    group_rev = inputs.group_pnl.group_revenue_net

    return SegmentPnlResult(
        starlink_bb_revenue=bb,
        starlink_dtc_revenue=dtc,
        starlink_starshield_revenue=starshield,
        starlink_hardware_revenue=hardware,
        starlink_subtotal_revenue=sl_sub,
        customer_launch_services_revenue=ls,
        customer_launch_development_revenue=ld,
        customer_launch_subtotal_revenue=cl_sub,
        ai_orbital_dc_revenue=orbital,
        ai_terrestrial_dc_revenue=terr,
        ai_apps_revenue=apps,
        ai_compute_subtotal_revenue=ai_sub,
        lunar_mars_revenue=lm_module,
        group_revenue=group_rev,
        memo_starlink_sub_lines=_tie(sl_sub, sl_module),
        memo_customer_launch_sub_lines=_tie(cl_sub, cl_module),
        memo_ai_compute_sub_lines=_tie(ai_sub, ai_module),
        memo_lunar_mars_sub_line=_tie(lm_module, lm_module),
        memo_group_revenue_tie=_tie(group_rev, group_rev),
    )


def segment_tieouts_ok(result: SegmentPnlResult, *, tolerance_mm: float = 1.0) -> bool:
    """True when all Segment P&L tie-out memos are within tolerance.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    checks = (
        result.memo_starlink_sub_lines,
        result.memo_customer_launch_sub_lines,
        result.memo_ai_compute_sub_lines,
        result.memo_lunar_mars_sub_line,
        result.memo_group_revenue_tie,
    )
    for vec in checks:
        if float(np.max(np.abs(vec.values))) > tolerance_mm:
            return False
    return True
