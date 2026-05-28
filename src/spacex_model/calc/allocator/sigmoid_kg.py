"""Sigmoid kg IRR queue — 5 sub-blocks per Architecture §6.4 / §20.2."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from spacex_model.calc.allocator.sigmoid_cash import _sigmoid_blend_year
from spacex_model.calc.allocator.types import KgAllocations, QueueSubBlockDemands, QueueSubBlockIrrs
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector


def compute_sigmoid_kg_allocations(
    capacity_available_kg: YearVector,
    demands: QueueSubBlockDemands,
    irrs: QueueSubBlockIrrs,
    *,
    sigmoid_k: float = 2.0,
) -> KgAllocations:
    """IRR-priority sigmoid kg allocations across five queue sub-blocks.

    Excel cell:        Allocator!D116:AC116 (per sub-block kg proposed allocation)
    Excel label:       "Proposed kg allocation (kg-to-LEO)"
    Architecture ref:  §6.4 / §20.2 (kg sigmoid queue; V2 not in kg queue)
    Principle:         2 (IRR-priority sigmoid blend; negative IRR → zero)

    """
    demand_list = demands.kg_tuple()
    irr_blocks = irrs.as_tuple()
    irr_list: Sequence[YearVector] = (
        irr_blocks[0],
        irr_blocks[3],
        irr_blocks[4],
        irr_blocks[5],
        irr_blocks[6],
    )
    n_blocks = len(demand_list)
    out = np.zeros((n_blocks, HORIZON_YEARS), dtype=np.float64)

    for t in range(HORIZON_YEARS):
        alloc = _sigmoid_blend_year(
            capacity_available_kg.values[t],
            [d.values[t] for d in demand_list],
            [i.values[t] for i in irr_list],
            sigmoid_k=sigmoid_k,
        )
        for i, value in enumerate(alloc):
            out[i, t] = value

    blocks = [YearVector(out[i]) for i in range(n_blocks)]
    return KgAllocations(
        customer_launch=blocks[0],
        starlink_v3_bb=blocks[1],
        starlink_v3_dtc=blocks[2],
        odc=blocks[3],
        ai_stack=blocks[4],
    )
