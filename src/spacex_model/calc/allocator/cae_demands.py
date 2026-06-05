"""Aggregate exogenous demands into CAE 3-module + Level-2 shape."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.priority import ModuleSpotIrrs
from spacex_model.calc.allocator.types import QueueSubBlockDemands
from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class CaeDemands:
    """CAE desired cash/kg for three modules and Level-2 ODC/Terr."""

    cash: ModuleSpotIrrs
    kg: ModuleSpotIrrs
    odc_cash: YearVector
    terrestrial_cash: YearVector


def aggregate_cae_demands(
    sub_demands: QueueSubBlockDemands,
    module_outputs: dict[str, AllocatorOut],
) -> CaeDemands:
    """Roll seven sub-block demands into CAE three-module totals.

    Excel cell:        Cash Allocation Engine!D113:D115
    Excel label:       "Desired cash: Starlink ($mm)" … "Desired cash: AI-Compute ($mm)"
    Architecture ref:  §2.3 desired cash rows
    Principle:         12 (exogenous demand only)

    """
    sl_cash = (
        sub_demands.starlink_v2_bb_cash.values
        + sub_demands.starlink_v2_dtc_cash.values
        + sub_demands.starlink_v3_bb_cash.values
        + sub_demands.starlink_v3_dtc_cash.values
    )
    sl_kg = (
        sub_demands.starlink_v3_bb_kg.values
        + sub_demands.starlink_v3_dtc_kg.values
    )
    ai = module_outputs.get("ai_compute")
    if ai is not None:
        inflated_sl = ai.capacity_demand_kg.values * 0.0  # placeholder
        _ = inflated_sl
    # CAE R99–R101 uses inflated fleet-sizing kg (defect F4); use module capacity + sub-block kg
    sl_kg_inflated = np.maximum(
        sl_kg,
        module_outputs.get("starlink", AllocatorOut.zeros()).capacity_demand_kg.values,
    )
    cl_kg = np.maximum(
        sub_demands.customer_launch_kg.values,
        module_outputs.get("customer_launch", AllocatorOut.zeros()).capacity_demand_kg.values,
    )
    ai_kg = np.maximum(
        sub_demands.odc_kg.values + sub_demands.ai_stack_kg.values,
        module_outputs.get("ai_compute", AllocatorOut.zeros()).capacity_demand_kg.values,
    )

    return CaeDemands(
        cash=ModuleSpotIrrs(
            starlink=YearVector(sl_cash),
            customer_launch=sub_demands.customer_launch_cash,
            ai_compute=YearVector(
                sub_demands.odc_cash.values + sub_demands.ai_stack_cash.values
            ),
        ),
        kg=ModuleSpotIrrs(
            starlink=YearVector(sl_kg_inflated),
            customer_launch=YearVector(cl_kg),
            ai_compute=YearVector(ai_kg),
        ),
        odc_cash=sub_demands.odc_cash,
        terrestrial_cash=sub_demands.ai_stack_cash,
    )


def cae_cash_to_sub_blocks(
    cae_cash: ModuleSpotIrrs,
    level2_odc: YearVector,
    level2_terrestrial: YearVector,
    sub_demands: QueueSubBlockDemands,
) -> tuple[YearVector, YearVector, YearVector, YearVector, YearVector, YearVector, YearVector]:
    """Split CAE module cash back into seven legacy sub-blocks for pipeline consumers.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    sl_parts = [
        sub_demands.starlink_v2_bb_cash.values,
        sub_demands.starlink_v2_dtc_cash.values,
        sub_demands.starlink_v3_bb_cash.values,
        sub_demands.starlink_v3_dtc_cash.values,
    ]
    sl_total_dem = sum(sl_parts)
    sl_alloc = cae_cash.starlink.values
    out_sl = []
    with np.errstate(divide="ignore", invalid="ignore"):
        for part in sl_parts:
            ratio = np.where(sl_total_dem > 0.0, part / sl_total_dem, 0.25)
            out_sl.append(sl_alloc * ratio)
    return (
        YearVector(cae_cash.customer_launch.values),
        YearVector(out_sl[0]),
        YearVector(out_sl[1]),
        YearVector(out_sl[2]),
        YearVector(out_sl[3]),
        level2_odc,
        level2_terrestrial,
    )


def cae_kg_to_sub_blocks(
    kg: ModuleSpotIrrs,
    sub_demands: QueueSubBlockDemands,
) -> tuple[YearVector, YearVector, YearVector, YearVector, YearVector]:
    """Split CAE kg allotments into five legacy kg sub-blocks.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    v3_parts = [
        sub_demands.starlink_v3_bb_kg.values,
        sub_demands.starlink_v3_dtc_kg.values,
    ]
    v3_total = v3_parts[0] + v3_parts[1]
    sl_kg = kg.starlink.values
    with np.errstate(divide="ignore", invalid="ignore"):
        v3_bb = np.where(v3_total > 0.0, sl_kg * v3_parts[0] / v3_total, sl_kg * 0.5)
        v3_dtc = sl_kg - v3_bb

        odc_parts = [sub_demands.odc_kg.values, sub_demands.ai_stack_kg.values]
        odc_total = odc_parts[0] + odc_parts[1]
        ai_kg = kg.ai_compute.values
        odc_kg = np.where(odc_total > 0.0, ai_kg * odc_parts[0] / odc_total, ai_kg * 0.5)
    ai_stack_kg = ai_kg - odc_kg

    return (
        kg.customer_launch,
        YearVector(v3_bb),
        YearVector(v3_dtc),
        YearVector(odc_kg),
        YearVector(ai_stack_kg),
    )
