"""Sigmoid cash IRR queue — 7 sub-blocks per Architecture §6.3 / §20.2."""

from __future__ import annotations

from typing import Sequence

import numpy as np

from spacex_model.calc.allocator.types import CashAllocations, QueueSubBlockDemands, QueueSubBlockIrrs
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector


def _sigmoid_blend_year(
    available: float,
    demands: Sequence[float],
    irrs: Sequence[float],
    *,
    sigmoid_k: float,
) -> list[float]:
    """Per-year sigmoid: weight = MAX(IRR,0)^k; allocation = MIN(masked_demand, pool × share)."""
    n = len(demands)
    masked = [
        demands[i] if irrs[i] > 0.0 else 0.0
        for i in range(n)
    ]
    weights = [
        max(irrs[i], 0.0) ** sigmoid_k if demands[i] > 0.0 else 0.0
        for i in range(n)
    ]
    total_w = sum(weights)
    if available <= 0.0 or total_w <= 0.0:
        return [0.0] * n
    shares = [w / total_w for w in weights]
    return [min(masked[i], available * shares[i]) for i in range(n)]


def compute_sigmoid_cash_allocations(
    available_cash: YearVector,
    demands: QueueSubBlockDemands,
    irrs: QueueSubBlockIrrs,
    *,
    sigmoid_k: float = 2.0,
) -> CashAllocations:
    """IRR-priority sigmoid cash allocations across seven queue sub-blocks.

    Excel cell:        Allocator!D50:AC50 (per sub-block proposed allocation)
    Excel label:       "Proposed cash allocation ($mm)"
    Architecture ref:  §6.3 / §20.2 (cash sigmoid queue)
    Principle:         2 (IRR-priority sigmoid blend; negative IRR → zero)

    """
    demand_list = demands.cash_tuple()
    irr_list = irrs.as_tuple()
    n_blocks = len(demand_list)
    out = np.zeros((n_blocks, HORIZON_YEARS), dtype=np.float64)

    for t in range(HORIZON_YEARS):
        alloc = _sigmoid_blend_year(
            available_cash.values[t],
            [d.values[t] for d in demand_list],
            [i.values[t] for i in irr_list],
            sigmoid_k=sigmoid_k,
        )
        for i, value in enumerate(alloc):
            out[i, t] = value

    blocks = [YearVector(out[i]) for i in range(n_blocks)]
    return CashAllocations(
        customer_launch=blocks[0],
        starlink_v2_bb=blocks[1],
        starlink_v2_dtc=blocks[2],
        starlink_v3_bb=blocks[3],
        starlink_v3_dtc=blocks[4],
        odc=blocks[5],
        ai_stack=blocks[6],
    )
