"""Map canonical Excel labels to model-computed values for divergence reporting."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.domain.year_vector import YearVector

if TYPE_CHECKING:
    from spacex_model.engine.pipeline import ModelResult

# V4.113 tab names (legacy V2.16 aliases retained for diagnostic compat)
_MODULE_SHEETS: dict[str, str] = {
    "Customer Launch": "customer_launch",
    "Starlink": "starlink",
    "ODC": "ai_compute",
    "AI Stack": "ai_compute",
    "AI - Compute": "ai_compute",
    "Lunar Mars": "lunar_mars",
    "Lunar - Mars": "lunar_mars",
}

_ALLOCATOR_OUT_FIELDS: dict[str, str] = {
    "Total Revenue ($mm)": "total_revenue",
    "Module EBITDA ($mm)": "module_ebitda",
    "Module FCF ($mm)": "module_fcf",
    "Module CapEx ($mm)": "module_capex",
    "Capital deployed ($mm)": "capital_deployed",
    "Spot IRR": "spot_irr",
    "Forward IRR (Y+2)": "forward_irr",
    "Blended IRR": "blended_irr",
    "Capacity Demand (kg-to-LEO)": "capacity_demand_kg",
}

_GROUP_PNL_FIELDS: dict[str, str] = {
    "Group Revenue ($mm)": "group_revenue_net",
    "Group Gross Profit ($mm)": "group_gross_profit",
    "Group EBITDA ($mm)": "group_ebitda",
    "Group D&A ($mm)": "group_da",
    "Group EBIT ($mm)": "group_ebit",
    "Taxes ($mm)": "taxes",
    "NOPAT ($mm)": "nopat",
    "Total OpEx ($mm)": "total_opex",
    "Total Group CapEx ($mm)": "total_group_capex",
    "Group FCF ($mm)": "group_fcf",
    "Mars/Moon strategic carve-out ($mm/yr)": "mars_carveout",
}

_LAUNCH_CAPACITY_FIELDS: dict[str, str] = {
    "F9 launches per year": "f9_launches",
    "F9 fleet end-of-year": "f9_fleet_eoy",
    "F9 manufactured per year (boosters)": "f9_manufactured",
    "Total Starship launches per year": "total_starship_launches",
    "Total Annual Capacity (kg-to-LEO)": "total_annual_capacity_kg",
    "Blended cost per Starship vehicle": "blended_cost_per_starship_vehicle",
    "Annual vehicle D&A ($mm)": "annual_vehicle_da",
    "At-cost launch services rate ($mm/launch)": "starship_at_cost_rate",
}

# V4.113 Vehicle Build tab — same engine outputs, relabeled rows.
_VEHICLE_BUILD_LAUNCH_FIELDS: dict[str, str] = {
    "F9 launches per year": "f9_launches",
    "Starship launches per year": "total_starship_launches",
    "Total launch capacity (kg)": "total_annual_capacity_kg",
    "F9 fleet EoY (boosters)": "f9_fleet_eoy",
    "F9 boosters built per year": "f9_manufactured",
    "Starship at-cost rate, fully reusable ($mm/launch)": "starship_at_cost_rate",
}

_LAUNCH_CAPACITY_SHEETS = frozenset({"Launch Capacity", "Vehicle Build"})

_ALLOCATOR_SHEETS = frozenset({"Allocator", "Cash Allocation Engine"})

_ALLOCATOR_FIELDS: dict[str, str] = {
    cl.CASH_BOY_MM: "cash_boy",
    "Available cash for IRR queue ($mm)": "available_cash",
    cl.CASH_AVAILABLE_FOR_YEAR_MM: "available_cash",
    "Mars/Moon strategic carve-out ($mm/yr)": "mars_carveout",
    "Vehicle build claim ($mm)": "vehicle_build_claim",
    "Year-N non-module claims ($mm)": "non_module_claims",
    cl.POOL_AFTER_QUEUE_GATE_MM: "pool_after_gate",
    cl.REMAINING_POOL_FOR_IRR_WEIGHTED_ALLOCATION_MM_GATED_TO_0_IN_THE_2025_ANCHOR_YEAR_ALLOCATION_OPERATIVE_2026_ONWARD: "remaining_pool",
    cl.ALLOCATED_CASH_TO_STARLINK_MM: "allocated_final_starlink",
    cl.ALLOCATED_CASH_TO_CUSTOMER_LAUNCH_MM: "allocated_final_customer_launch",
    cl.ALLOCATED_CASH_TO_AI_COMPUTE_MM: "allocated_final_ai_compute",
    cl.KG_BINDING_FLAG_1_CAPACITY_BINDS: "kg_binding_flag",
}

_CASH_ALLOC_LABELS: dict[str, str] = {
    "Customer Launch cash allocation": "customer_launch",
    "Starlink V2 BB cash allocation": "starlink_v2_bb",
    "Starlink V2 DTC cash allocation": "starlink_v2_dtc",
    "Starlink V3 BB cash allocation": "starlink_v3_bb",
    "Starlink V3 DTC cash allocation": "starlink_v3_dtc",
    "ODC cash allocation": "odc",
    "AI Stack cash allocation": "ai_stack",
}

_KG_ALLOC_LABELS: dict[str, str] = {
    "Customer Launch kg allocation": "customer_launch",
    "Starlink V3 BB kg allocation": "starlink_v3_bb",
    "Starlink V3 DTC kg allocation": "starlink_v3_dtc",
    "ODC kg allocation": "odc",
    "AI Stack kg allocation": "ai_stack",
}

_CAE_SPOT_IRR: dict[str, tuple[str, str]] = {
    cl.SPOT_IRR_STARLINK: ("starlink", "spot_irr"),
    cl.SPOT_IRR_CUSTOMER_LAUNCH: ("customer_launch", "spot_irr"),
    cl.SPOT_IRR_AI_COMPUTE: ("ai_compute", "spot_irr"),
    cl.SPOT_IRR_ODC_PRIOR_YR: ("ai_compute", "spot_irr"),
    cl.SPOT_IRR_TERRESTRIAL_PRIOR_YR: ("ai_compute", "spot_irr"),
}


def _year_value(vec: YearVector | None, year: int) -> float | None:
    if vec is None:
        return None
    return float(vec.at(year))


def _module_field(result: ModelResult, module_key: str, field: str, year: int) -> float:
    mod: AllocatorOut = result.module_outputs[module_key]
    return _year_value(getattr(mod, field), year)  # type: ignore[arg-type]


_UNIT_SUFFIX_RE = re.compile(r"\s*\(\$mm\)|\s*\(%\)|\s*\(count\)", re.I)
_RESTATED_RE = re.compile(r"\s*—\s*restated", re.I)


def normalize_label(label: str) -> str:
    """Strip unit suffixes, section markers, and punctuation for tolerant matching."""
    s = label.strip()
    if s.startswith("▸"):
        s = s.lstrip("▸ ").strip()
    s = _UNIT_SUFFIX_RE.sub("", s)
    s = _RESTATED_RE.sub("", s)
    s = re.sub(r"[^\w\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def labels_match(a: str, b: str) -> bool:
    """Exact or normalized label equality."""
    return a == b or normalize_label(a) == normalize_label(b)


def find_label_row(labels: dict[int, str], label: str) -> int | None:
    """Find row index for a label using exact then normalized match."""
    for row_idx, lbl in labels.items():
        if labels_match(lbl, label):
            return row_idx
    return None


def lookup_by_label(result: ModelResult, sheet: str, label: str, year: int) -> float | None:
    """Resolve a canonical label to a model-computed value, or None if unmapped."""
    if year < FIRST_YEAR or year > LAST_YEAR:
        return None

    module_key = _MODULE_SHEETS.get(sheet)
    if module_key and label in _ALLOCATOR_OUT_FIELDS:
        return _module_field(result, module_key, _ALLOCATOR_OUT_FIELDS[label], year)

    if sheet == "Group P&L" and label in _GROUP_PNL_FIELDS:
        return _year_value(getattr(result.group_pnl, _GROUP_PNL_FIELDS[label]), year)

    if sheet in _LAUNCH_CAPACITY_SHEETS:
        field = _LAUNCH_CAPACITY_FIELDS.get(label) or _VEHICLE_BUILD_LAUNCH_FIELDS.get(label)
        if field:
            return _year_value(getattr(result.launch_capacity, field), year)

    if sheet in _ALLOCATOR_SHEETS:
        if label in _ALLOCATOR_FIELDS:
            return _year_value(getattr(result.allocator, _ALLOCATOR_FIELDS[label]), year)
        if label in _CASH_ALLOC_LABELS:
            field = _CASH_ALLOC_LABELS[label]
            return _year_value(getattr(result.allocator.cash, field), year)
        if label in _KG_ALLOC_LABELS:
            field = _KG_ALLOC_LABELS[label]
            return _year_value(getattr(result.allocator.kg, field), year)
        if label in _CAE_SPOT_IRR:
            mod_key, attr = _CAE_SPOT_IRR[label]
            return _module_field(result, mod_key, attr, year)

    # Cross-sheet module IRR labels on legacy Allocator tab
    _module_irr_labels = {
        "Customer Launch Blended IRR": ("customer_launch", "blended_irr"),
        "ODC Blended IRR": ("ai_compute", "blended_irr"),
        "AI Stack Blended IRR": ("ai_compute", "blended_irr"),
    }
    if sheet in _ALLOCATOR_SHEETS and label in _module_irr_labels:
        mod_key, attr = _module_irr_labels[label]
        return _module_field(result, mod_key, attr, year)

    return None


def mapped_label_count() -> int:
    """Count of resolvable label mappings (for coverage reporting)."""
    return (
        len(_MODULE_SHEETS) * len(_ALLOCATOR_OUT_FIELDS)
        + len(_GROUP_PNL_FIELDS)
        + len(_LAUNCH_CAPACITY_FIELDS)
        + len(_ALLOCATOR_FIELDS)
        + len(_CASH_ALLOC_LABELS)
        + len(_KG_ALLOC_LABELS)
        + len(_CAE_SPOT_IRR)
        + len(
            {
                "Customer Launch Blended IRR",
                "ODC Blended IRR",
                "AI Stack Blended IRR",
            }
        )
    )


LabelResolver = Callable[["ModelResult", str, str, int], float | None]
