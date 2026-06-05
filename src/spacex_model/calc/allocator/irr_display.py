"""Central IRR display — roll-up from module Allocator OUT (Architecture §6)."""

from __future__ import annotations

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.priority import ModuleSpotIrrs
from spacex_model.calc.allocator.types import QueueSubBlockIrrs
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector


def _prior_year(values: np.ndarray) -> np.ndarray:
    out = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(1, HORIZON_YEARS):
        out[t] = values[t - 1]
    return out


def compute_module_spot_irrs(module_outputs: dict[str, AllocatorOut]) -> ModuleSpotIrrs:
    """Prior-year spot IRR for CAE softmax (acyclicity firewall).

    Excel cell:        Cash Allocation Engine!D28:D30
    Excel label:       "Spot IRR: Starlink" … "Spot IRR: AI-Compute"
    Architecture ref:  §5.3 acyclicity (prior-yr IRR only)
    Principle:         2 (per-unit marginal IRR drives allocation weights)

    """
    cl = module_outputs.get("customer_launch", AllocatorOut.zeros())
    sl = module_outputs.get("starlink", AllocatorOut.zeros())
    ai = module_outputs.get("ai_compute")
    if ai is None:
        odc = module_outputs.get("odc", AllocatorOut.zeros())
        ai_stack = module_outputs.get("ai_stack", AllocatorOut.zeros())
        ai_irr = np.maximum(odc.spot_irr.values, ai_stack.spot_irr.values)
    else:
        ai_irr = ai.spot_irr.values

    return ModuleSpotIrrs(
        starlink=YearVector(_prior_year(sl.spot_irr.values)),
        customer_launch=YearVector(_prior_year(cl.spot_irr.values)),
        ai_compute=YearVector(_prior_year(ai_irr)),
    )


def compute_level2_spot_irrs(module_outputs: dict[str, AllocatorOut]) -> tuple[YearVector, YearVector]:
    """Prior-year ODC / Terrestrial spot IRR for Level-2 split.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    ai = module_outputs.get("ai_compute")
    if ai is not None:
        return (
            YearVector(_prior_year(ai.spot_irr.values)),
            YearVector(_prior_year(ai.spot_irr.values * 0.0)),
        )
    odc = module_outputs.get("odc", AllocatorOut.zeros())
    terr = module_outputs.get("ai_stack", AllocatorOut.zeros())
    return (
        YearVector(_prior_year(odc.spot_irr.values)),
        YearVector(_prior_year(terr.spot_irr.values)),
    )


def roll_up_module_irrs(
    module_outputs: dict[str, AllocatorOut],
    *,
    starlink_vehicle_irrs: QueueSubBlockIrrs | None = None,
) -> QueueSubBlockIrrs:
    """Roll up blended IRR year-vectors for cash sigmoid queue sub-blocks.

    Excel cell:        Allocator!D153:AC153
    Excel label:       "Customer Launch Blended IRR"
    Architecture ref:  §6 central IRR display
    Principle:         2 (per-unit marginal IRR drives sigmoid weights)

    Uses per-vehicle Starlink IRRs when provided; otherwise falls back to module-level.

    """
    cl = module_outputs.get("customer_launch", AllocatorOut.zeros())
    sl = module_outputs.get("starlink", AllocatorOut.zeros())
    ai_compute = module_outputs.get("ai_compute")
    if ai_compute is not None:
        odc = ai_compute
        ai = AllocatorOut.zeros()
    else:
        odc = module_outputs.get("odc", AllocatorOut.zeros())
        ai = module_outputs.get("ai_stack", AllocatorOut.zeros())

    if starlink_vehicle_irrs is not None:
        sl_v2_bb = starlink_vehicle_irrs.starlink_v2_bb
        sl_v2_dtc = starlink_vehicle_irrs.starlink_v2_dtc
        sl_v3_bb = starlink_vehicle_irrs.starlink_v3_bb
        sl_v3_dtc = starlink_vehicle_irrs.starlink_v3_dtc
    else:
        sl_blended = sl.blended_irr
        sl_v2_bb = sl_blended
        sl_v2_dtc = sl_blended
        sl_v3_bb = sl_blended
        sl_v3_dtc = sl_blended

    return QueueSubBlockIrrs(
        customer_launch=cl.blended_irr,
        starlink_v2_bb=sl_v2_bb,
        starlink_v2_dtc=sl_v2_dtc,
        starlink_v3_bb=sl_v3_bb,
        starlink_v3_dtc=sl_v3_dtc,
        odc=odc.blended_irr,
        ai_stack=ai.blended_irr,
    )
