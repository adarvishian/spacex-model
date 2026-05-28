"""First-year (2025) historical override per Architecture §2.16."""

from __future__ import annotations

import numpy as np

from spacex_model.calc.allocator.types import CashAllocations, KgAllocations
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector


def _override_year(values: YearVector, year: int, amount: float) -> YearVector:
    vec = values.values.copy()
    idx = year - FIRST_YEAR
    vec[idx] = max(vec[idx], amount)
    return YearVector(vec)


def cap_cash_allocations_to_available(
    cash: CashAllocations,
    available_cash: YearVector,
) -> CashAllocations:
    """Scale each year so Σ cash allocations ≤ available (Block A invariant).

    Excel cell:        Allocator!D29:AC29
    Excel label:       "Available cash for IRR queue ($mm)"
    Architecture ref:  §6.2 queue gate
    Principle:         4 (non-module claims reserved before IRR queue)

    """
    fields = list(CashAllocations.zeros().__dataclass_fields__)
    if "as_tuple" in fields:
        fields.remove("as_tuple")
    arrays = {name: getattr(cash, name).values.copy() for name in fields}
    for t in range(HORIZON_YEARS):
        total = sum(arrays[name][t] for name in fields)
        avail = available_cash.values[t]
        if total > avail and total > 0:
            scale = avail / total
            for name in fields:
                arrays[name][t] *= scale
    return CashAllocations(**{name: YearVector(arrays[name]) for name in fields})


def apply_first_year_override(
    cash: CashAllocations,
    kg: KgAllocations,
    historical_2025: dict[str, float],
) -> tuple[CashAllocations, KgAllocations]:
    """Replace 2025 allocator outputs with Mach33-anchored historical actuals.

    Excel cell:        Allocator!D88:AC88 (V2 BB cash allocation)
    Excel label:       "Starlink V2 BB cash allocation ($mm)"
    Architecture ref:  §2.16 (first-year override convention)
    Principle:         12 (2025 locked; allocator drives 2026+ only)

    Keys match CashAllocations / KgAllocations field names (e.g. ``starlink_v2_bb``).

    """
    cash_fields = {
        "customer_launch": cash.customer_launch,
        "starlink_v2_bb": cash.starlink_v2_bb,
        "starlink_v2_dtc": cash.starlink_v2_dtc,
        "starlink_v3_bb": cash.starlink_v3_bb,
        "starlink_v3_dtc": cash.starlink_v3_dtc,
        "odc": cash.odc,
        "ai_stack": cash.ai_stack,
    }
    kg_fields = {
        "customer_launch": kg.customer_launch,
        "starlink_v3_bb": kg.starlink_v3_bb,
        "starlink_v3_dtc": kg.starlink_v3_dtc,
        "odc": kg.odc,
        "ai_stack": kg.ai_stack,
    }

    for key, vec in cash_fields.items():
        if key in historical_2025:
            cash_fields[key] = _override_year(vec, FIRST_YEAR, historical_2025[key])
    for key, vec in kg_fields.items():
        if key in historical_2025:
            kg_fields[key] = _override_year(vec, FIRST_YEAR, historical_2025[key])

    return (
        CashAllocations(**cash_fields),
        KgAllocations(**kg_fields),
    )
