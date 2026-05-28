"""Map canonical Excel labels to model-computed values for divergence reporting."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.domain.year_vector import YearVector

if TYPE_CHECKING:
    from spacex_model.engine.pipeline import ModelResult

_MODULE_SHEETS: dict[str, str] = {
    "Customer Launch": "customer_launch",
    "Starlink": "starlink",
    "ODC": "odc",
    "AI Stack": "ai_stack",
    "Lunar Mars": "lunar_mars",
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

_ALLOCATOR_FIELDS: dict[str, str] = {
    "Cash BoY ($mm)": "cash_boy",
    "Available cash for IRR queue ($mm)": "available_cash",
    "Mars/Moon strategic carve-out ($mm/yr)": "mars_carveout",
    "Vehicle build claim ($mm)": "vehicle_build_claim",
    "Year-N non-module claims ($mm)": "non_module_claims",
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


def _year_value(vec: YearVector, year: int) -> float:
    return float(vec.at(year))


def _module_field(result: ModelResult, module_key: str, field: str, year: int) -> float:
    mod: AllocatorOut = result.module_outputs[module_key]
    return _year_value(getattr(mod, field), year)


def lookup_by_label(result: ModelResult, sheet: str, label: str, year: int) -> float | None:
    """Resolve a canonical label to a model-computed value, or None if unmapped."""
    if year < FIRST_YEAR or year > LAST_YEAR:
        return None

    module_key = _MODULE_SHEETS.get(sheet)
    if module_key and label in _ALLOCATOR_OUT_FIELDS:
        return _module_field(result, module_key, _ALLOCATOR_OUT_FIELDS[label], year)

    if sheet == "Group P&L" and label in _GROUP_PNL_FIELDS:
        return _year_value(getattr(result.group_pnl, _GROUP_PNL_FIELDS[label]), year)

    if sheet == "Launch Capacity" and label in _LAUNCH_CAPACITY_FIELDS:
        return _year_value(getattr(result.launch_capacity, _LAUNCH_CAPACITY_FIELDS[label]), year)

    if sheet == "Allocator":
        if label in _ALLOCATOR_FIELDS:
            return _year_value(getattr(result.allocator, _ALLOCATOR_FIELDS[label]), year)
        if label in _CASH_ALLOC_LABELS:
            field = _CASH_ALLOC_LABELS[label]
            return _year_value(getattr(result.allocator.cash, field), year)
        if label in _KG_ALLOC_LABELS:
            field = _KG_ALLOC_LABELS[label]
            return _year_value(getattr(result.allocator.kg, field), year)

    # Cross-sheet module IRR labels on Allocator tab
    _module_irr_labels = {
        "Customer Launch Blended IRR": ("customer_launch", "blended_irr"),
        "ODC Blended IRR": ("odc", "blended_irr"),
        "AI Stack Blended IRR": ("ai_stack", "blended_irr"),
    }
    if sheet == "Allocator" and label in _module_irr_labels:
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
        + 3
    )


LabelResolver = Callable[["ModelResult", str, str, int], float | None]
