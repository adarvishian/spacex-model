"""Apply S-1 adherence overrides on top of V4.131 Assumptions ingest (P0 + P1)."""

from __future__ import annotations

from typing import Any

from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.inputs.assumptions import (
    AssumptionInput,
    Assumptions,
    AssumptionsSection,
)
from spacex_model.inputs.s1_profiles import (
    broadband_arpu_sub_mo,
    s1_ai_segment_revenue_mm,
    starship_customer_launch_price_mm,
)
from spacex_model.inputs.scenarios import apply_assumption_overrides

_INJECTION_SECTIONS: dict[str, str] = {
    cl.BROADBAND_ARPU_SUB_MO_YEAR_ROW: "§3 Starlink",
    cl.S1_AI_SEGMENT_REVENUE_YEAR_ROW: "§7 AI - Compute",
    cl.STARSHIP_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH_YEAR_ROW: "§4 Customer Launch",
}


def _year_dict(vec) -> dict[int, float]:
    return {FIRST_YEAR + i: float(vec[i]) for i in range(HORIZON_YEARS)}


def _inject_labels(
    assumptions: Assumptions, injections: dict[str, AssumptionInput]
) -> Assumptions:
    new_by_label = dict(assumptions.by_label)
    for label, row in injections.items():
        new_by_label[label] = row

    def _rebuild(section: AssumptionsSection) -> AssumptionsSection:
        inputs = dict(section.inputs)
        for label, row in injections.items():
            if row.section == section.section_id or label in inputs:
                inputs[label] = row
        return section.model_copy(update={"inputs": inputs})

    return Assumptions(
        global_=assumptions.global_,
        allocator=_rebuild(assumptions.allocator),
        capacity=_rebuild(assumptions.capacity),
        customer_launch=_rebuild(assumptions.customer_launch),
        starlink=_rebuild(assumptions.starlink),
        odc=_rebuild(assumptions.odc),
        ai_stack=_rebuild(assumptions.ai_stack),
        lunar_mars=_rebuild(assumptions.lunar_mars),
        opex=_rebuild(assumptions.opex),
        capex=_rebuild(assumptions.capex),
        valuation=_rebuild(assumptions.valuation),
        mc_ranges=assumptions.mc_ranges,
        by_label=new_by_label,
    )


def s1_adherence_override_map() -> dict[str, Any]:
    """Canonical S-1 override payload (mirrored in scenarios/s1_adherence.yaml)."""
    return {
        cl.BROADBAND_ARPU_SUB_MO_YEAR_ROW: _year_dict(broadband_arpu_sub_mo()),
        cl.S1_AI_SEGMENT_REVENUE_YEAR_ROW: _year_dict(s1_ai_segment_revenue_mm()),
        cl.STARSHIP_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH_YEAR_ROW: _year_dict(
            starship_customer_launch_price_mm()
        ),
    }


def apply_s1_adherence_overrides(assumptions: Assumptions) -> Assumptions:
    """Apply §7.2 P0 + §7.3 P1 where workbook rows exist but S-1 disclosure wins."""
    override_map = s1_adherence_override_map()
    injections: dict[str, AssumptionInput] = {}
    for label, override in override_map.items():
        if label in assumptions.by_label:
            continue
        year_values = override if isinstance(override, dict) else {}
        base = float(year_values.get(FIRST_YEAR, next(iter(year_values.values()), 0.0)))
        injections[label] = AssumptionInput(
            label=label,
            section=_INJECTION_SECTIONS.get(label, "§1 Global"),
            base_case=base,
            year_values=year_values,
            notes="S-1 adherence P0/P1",
        )
    if injections:
        assumptions = _inject_labels(assumptions, injections)
    return apply_assumption_overrides(assumptions, override_map)
