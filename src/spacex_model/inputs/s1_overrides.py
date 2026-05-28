"""Apply S-1 adherence overrides on top of V2.16 Assumptions ingest (P0 + P1)."""

from __future__ import annotations

from typing import Any

from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.inputs.assumptions import AssumptionInput, Assumptions, AssumptionsSection
from spacex_model.inputs.s1_profiles import (
    BRIDGE_DRAWDOWN_YEAR,
    anthropic_compute_revenue_mm,
    broadband_arpu_sub_mo,
    echostar_spectrum_capex_mm,
    f9_customer_launches_per_year,
    impairment_charges_mm,
    launch_services_revenue_share,
    restructuring_charges_mm,
    s1_ai_segment_revenue_mm,
    share_based_compensation_mm,
    starship_customer_launch_price_mm,
    starship_customer_launches_per_year,
    starship_precommercial_rd_mm,
    starshield_gov_connectivity_scope_factor,
    terrestrial_ai_capex_mm,
)
from spacex_model.inputs.scenarios import apply_assumption_overrides


def _year_dict(vec) -> dict[int, float]:
    return {FIRST_YEAR + i: float(vec[i]) for i in range(HORIZON_YEARS)}


def _inject_labels(assumptions: Assumptions, injections: dict[str, AssumptionInput]) -> Assumptions:
    """Add or replace Assumptions rows (for labels missing from V2.16)."""
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
        cl.STARTING_CASH_POSITION_EOY_2024_MM: 11_385.0,
        cl.BROADBAND_ARPU_SUB_MO_YEAR_ROW: _year_dict(broadband_arpu_sub_mo()),
        cl.ECHOSTAR_MID_BAND_CAPEX_MM_YEAR_ROW: _year_dict(echostar_spectrum_capex_mm()),
        cl.F9_CUSTOMER_LAUNCHES_PER_YEAR: _year_dict(f9_customer_launches_per_year()),
        "S-1 AI segment revenue ($mm) — year-row": _year_dict(s1_ai_segment_revenue_mm()),
        "Anthropic compute services revenue ($mm) — year-row": _year_dict(
            anthropic_compute_revenue_mm()
        ),
        "Terrestrial AI data-center CapEx ($mm) — year-row": _year_dict(terrestrial_ai_capex_mm()),
        cl.PRE_IPO_BRIDGE_DRAWDOWN_YEAR: float(BRIDGE_DRAWDOWN_YEAR),
        cl.SATELLITE_USEFUL_LIFE_V2_DTC_YEARS: 3.0,
        cl.SATELLITE_USEFUL_LIFE_V3_DTC_YEARS: 3.0,
        cl.F9_BOOSTER_ACCOUNTING_DEPRECIATION_CAP_FLIGHTS: 25.0,
        cl.STARSHIP_PRECOMMERCIAL_RD_MM_YEAR_ROW: _year_dict(starship_precommercial_rd_mm()),
        cl.STARSHIP_CUSTOMER_LAUNCHES_PER_YEAR: _year_dict(starship_customer_launches_per_year()),
        cl.STARSHIP_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH_YEAR_ROW: _year_dict(
            starship_customer_launch_price_mm()
        ),
        cl.LAUNCH_SERVICES_REVENUE_SHARE_YEAR_ROW: _year_dict(launch_services_revenue_share()),
        cl.STARSHIELD_S1_GOV_CONNECTIVITY_SCOPE_FACTOR: starshield_gov_connectivity_scope_factor(),
        cl.SHARE_BASED_COMPENSATION_MM_YEAR_ROW: _year_dict(share_based_compensation_mm()),
        cl.RESTRUCTURING_CHARGES_MM_YEAR_ROW: _year_dict(restructuring_charges_mm()),
        cl.IMPAIRMENT_CHARGES_MM_YEAR_ROW: _year_dict(impairment_charges_mm()),
    }


_P1_INJECTION_SPECS: tuple[tuple[str, str, object], ...] = (
    (cl.F9_CUSTOMER_LAUNCHES_PER_YEAR, "§4 Customer Launch", f9_customer_launches_per_year()),
    ("S-1 AI segment revenue ($mm) — year-row", "§7 AI Stack", s1_ai_segment_revenue_mm()),
    (
        "Anthropic compute services revenue ($mm) — year-row",
        "§7 AI Stack",
        anthropic_compute_revenue_mm(),
    ),
    (
        "Terrestrial AI data-center CapEx ($mm) — year-row",
        "§10 CapEx",
        terrestrial_ai_capex_mm(),
    ),
    (cl.STARSHIP_PRECOMMERCIAL_RD_MM_YEAR_ROW, "§12 OpEx", starship_precommercial_rd_mm()),
    (cl.STARSHIP_CUSTOMER_LAUNCHES_PER_YEAR, "§4 Customer Launch", starship_customer_launches_per_year()),
    (
        cl.STARSHIP_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH_YEAR_ROW,
        "§4 Customer Launch",
        starship_customer_launch_price_mm(),
    ),
    (
        cl.LAUNCH_SERVICES_REVENUE_SHARE_YEAR_ROW,
        "§4 Customer Launch",
        launch_services_revenue_share(),
    ),
    (cl.SHARE_BASED_COMPENSATION_MM_YEAR_ROW, "§15 Group P&L", share_based_compensation_mm()),
    (cl.RESTRUCTURING_CHARGES_MM_YEAR_ROW, "§15 Group P&L", restructuring_charges_mm()),
    (cl.IMPAIRMENT_CHARGES_MM_YEAR_ROW, "§15 Group P&L", impairment_charges_mm()),
)


def apply_s1_adherence_overrides(assumptions: Assumptions) -> Assumptions:
    """Apply §7.2 P0 + §7.3 P1 backlog: S-1 wins for disclosed Assumptions values."""
    injections: dict[str, AssumptionInput] = {}
    for label, section, vec in _P1_INJECTION_SPECS:
        if label not in assumptions.by_label:
            base = float(vec[0]) if hasattr(vec, "__getitem__") else None
            injections[label] = AssumptionInput(
                label=label,
                section=section,
                base_case=base,
                year_values=_year_dict(vec) if hasattr(vec, "__len__") else {},
                notes="S-1 adherence audit P0/P1",
            )

    for label, default in (
        (cl.F9_BOOSTER_ACCOUNTING_DEPRECIATION_CAP_FLIGHTS, 25.0),
        (cl.SATELLITE_USEFUL_LIFE_V2_DTC_YEARS, 3.0),
        (cl.SATELLITE_USEFUL_LIFE_V3_DTC_YEARS, 3.0),
        (cl.PRE_IPO_BRIDGE_DRAWDOWN_YEAR, float(BRIDGE_DRAWDOWN_YEAR)),
        (cl.STARSHIELD_S1_GOV_CONNECTIVITY_SCOPE_FACTOR, starshield_gov_connectivity_scope_factor()),
    ):
        if label not in assumptions.by_label:
            injections[label] = AssumptionInput(
                label=label,
                section="§1 Global",
                base_case=default,
                notes="S-1 adherence audit P1",
            )

    if injections:
        assumptions = _inject_labels(assumptions, injections)

    return apply_assumption_overrides(assumptions, s1_adherence_override_map())
