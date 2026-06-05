"""Aggregate exogenous demands into CAE 3-module + Level-2 shape."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.demand_spine import UnifiedKgDemands, compute_unified_kg_demands
from spacex_model.calc.allocator.priority import FourProgramIrrs, ModuleSpotIrrs
from spacex_model.calc.allocator.two_resource_fill import FourProgramDemands
from spacex_model.calc.allocator.types import QueueSubBlockDemands
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class CaeDemands:
    """CAE desired cash/kg for three modules and Level-2 ODC/Terr."""

    cash: ModuleSpotIrrs
    kg: ModuleSpotIrrs
    unified_kg: UnifiedKgDemands
    odc_cash: YearVector
    terrestrial_cash: YearVector


def aggregate_cae_demands(
    assumptions: Assumptions,
    sub_demands: QueueSubBlockDemands,
    module_outputs: dict[str, AllocatorOut],
) -> CaeDemands:
    """Roll seven sub-block demands into CAE three-module totals.

    Excel cell:        Cash Allocation Engine!D113:D115
    Excel label:       "Desired cash: Starlink ($mm)" … "Desired cash: AI-Compute ($mm)"
    Architecture ref:  §2.3 desired cash rows; U0 unified kg spine
    Principle:         12 (exogenous demand only)

    """
    _ = module_outputs  # kg spine is exogenous only (U0); cash roll-up unchanged
    sl_cash = (
        sub_demands.starlink_v2_bb_cash.values
        + sub_demands.starlink_v2_dtc_cash.values
        + sub_demands.starlink_v3_bb_cash.values
        + sub_demands.starlink_v3_dtc_cash.values
    )
    unified = compute_unified_kg_demands(assumptions, sub_demands)

    return CaeDemands(
        cash=ModuleSpotIrrs(
            starlink=YearVector(sl_cash),
            customer_launch=sub_demands.customer_launch_cash,
            ai_compute=YearVector(
                sub_demands.odc_cash.values + sub_demands.ai_stack_cash.values
            ),
        ),
        kg=unified.as_module_spot_irrs(),
        unified_kg=unified,
        odc_cash=sub_demands.odc_cash,
        terrestrial_cash=sub_demands.ai_stack_cash,
    )


def four_program_demands(
    cap_base_growth: ModuleSpotIrrs,
    cap_odc: YearVector,
    cap_terr: YearVector,
    unified_kg: UnifiedKgDemands,
    sub_demands: QueueSubBlockDemands,
) -> FourProgramDemands:
    """Map cap-base + unified kg spine into four first-class program demands (U2).

    Excel cell:        Cash Allocation Engine!D64:D66 + D99:D102
    Excel label:       "Cap: Starlink max deployable ($mm)" … "Desired launch kg: Starlink"
    Architecture ref:  PRD U2 two-resource fill inputs
    Principle:         12 (exogenous demand; growth slice only)

    """
    return FourProgramDemands(
        cash_caps=FourProgramIrrs(
            starlink=cap_base_growth.starlink,
            odc=cap_odc,
            terrestrial=cap_terr,
            customer_launch=cap_base_growth.customer_launch,
        ),
        kg=FourProgramIrrs(
            starlink=unified_kg.starlink,
            odc=sub_demands.odc_kg,
            terrestrial=YearVector.zeros(),
            customer_launch=unified_kg.customer_launch,
        ),
    )


def four_cash_to_sub_blocks(
    four_cash: FourProgramIrrs,
    sub_demands: QueueSubBlockDemands,
) -> tuple[YearVector, YearVector, YearVector, YearVector, YearVector, YearVector, YearVector]:
    """Split four-program cash into seven legacy sub-blocks for pipeline consumers.

    Excel cell:        Cash Allocation Engine!D39:D41 (sub-block roll-up)
    Excel label:       "Allocated cash to Starlink ($mm)" … seven sub-blocks
    Architecture ref:  PRD U2 four-program → legacy pipeline consumers
    Principle:         6 (one-tab-one-module; shim until sub-blocks retire)

    """
    module_cash = ModuleSpotIrrs(
        starlink=four_cash.starlink,
        customer_launch=four_cash.customer_launch,
        ai_compute=YearVector(four_cash.odc.values + four_cash.terrestrial.values),
    )
    return cae_cash_to_sub_blocks(
        module_cash,
        four_cash.odc,
        four_cash.terrestrial,
        sub_demands,
    )


def four_kg_to_sub_blocks(
    four_kg: FourProgramIrrs,
    sub_demands: QueueSubBlockDemands,
) -> tuple[YearVector, YearVector, YearVector, YearVector, YearVector]:
    """Split four-program kg into five legacy kg sub-blocks.

    Excel cell:        Cash Allocation Engine!D50:D52 (sub-block roll-up)
    Excel label:       "Launch capacity allotment: Starlink (kg)" … five sub-blocks
    Architecture ref:  PRD U2 four-program → legacy pipeline consumers
    Principle:         6 (one-tab-one-module; shim until sub-blocks retire)

    """
    module_kg = ModuleSpotIrrs(
        starlink=four_kg.starlink,
        customer_launch=four_kg.customer_launch,
        ai_compute=YearVector(four_kg.odc.values + four_kg.terrestrial.values),
    )
    return cae_kg_to_sub_blocks(module_kg, sub_demands)


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
