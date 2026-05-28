"""Central IRR display — roll-up from module Allocator OUT (Architecture §6)."""

from __future__ import annotations

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.types import QueueSubBlockIrrs
from spacex_model.domain.year_vector import YearVector


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
