"""Terrestrial DC + AI Apps sub-lines within AI - Compute (ex-AI Stack)."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.config import canonical_labels as cl
from spacex_model.domain.assumption_helpers import assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions
from spacex_model.inputs.s1_profiles import (
    anthropic_compute_revenue_mm,
    s1_ai_segment_revenue_mm,
    terrestrial_ai_capex_mm,
)

_S1_AI_COGS_RATIO_2025 = 2_178.0 / 3_201.0


@dataclass(frozen=True, slots=True)
class TerrestrialInputs:
    """Terrestrial DC + legacy AI Apps revenue inputs."""

    assumptions: Assumptions


def _ai_apps_revenue(inputs: TerrestrialInputs) -> YearVector:
    row = inputs.assumptions.lookup(cl.S1_AI_SEGMENT_REVENUE_YEAR_ROW)
    if row is not None and row.year_values:
        return assumption_year_vector(inputs.assumptions, cl.S1_AI_SEGMENT_REVENUE_YEAR_ROW)
    return YearVector(s1_ai_segment_revenue_mm())


def _terrestrial_dc_revenue(inputs: TerrestrialInputs) -> YearVector:
    row = inputs.assumptions.lookup(cl.ANTHROPIC_COMPUTE_REVENUE_YEAR_ROW)
    if row is not None and row.year_values:
        return assumption_year_vector(inputs.assumptions, cl.ANTHROPIC_COMPUTE_REVENUE_YEAR_ROW)
    return YearVector(anthropic_compute_revenue_mm())


def compute_ai_apps_revenue(inputs: TerrestrialInputs) -> YearVector:
    """AI Apps external revenue (legacy S-1 AI segment line).

    Excel cell:        AI - Compute!—
    Excel label:       "Revenue: AI Apps"
    Architecture ref:  §9 unified AI - Compute
    Principle:         8 (vending-machine module)
    
    Formula: AI Apps external revenue (legacy S-1 AI segment line).

    """
    return _ai_apps_revenue(inputs)


def compute_terrestrial_dc_revenue(inputs: TerrestrialInputs) -> YearVector:
    """Terrestrial DC external revenue (Anthropic compute services).

    Excel cell:        AI - Compute!—
    Excel label:       "Revenue: Terrestrial DC"
    Architecture ref:  §9 unified AI - Compute
    Principle:         8 (vending-machine module)
    
    Formula: Terrestrial DC external revenue (Anthropic compute services).

    """
    return _terrestrial_dc_revenue(inputs)


def compute_terrestrial_revenue(inputs: TerrestrialInputs) -> YearVector:
    """Terrestrial DC + AI Apps combined revenue.

    Excel cell:        AI - Compute!—
    Excel label:       "Revenue: Terrestrial"
    Architecture ref:  §9 unified AI - Compute
    Principle:         8 (vending-machine module)
    
    Formula: Terrestrial DC + AI Apps combined revenue.

    """
    return YearVector(
        _ai_apps_revenue(inputs).values + _terrestrial_dc_revenue(inputs).values
    )


def compute_terrestrial_cogs(inputs: TerrestrialInputs) -> YearVector:
    """Terrestrial COGS from S-1 ratio + Anthropic cost share.

    Excel cell:        AI - Compute!—
    Excel label:       "COGS: Terrestrial"
    Architecture ref:  §9 unified COGS
    Principle:         9 (S-1 adherence path)
    
    Formula: Terrestrial COGS from S-1 ratio + Anthropic cost share.

    """
    legacy_rev = _ai_apps_revenue(inputs)
    anthropic_rev = _terrestrial_dc_revenue(inputs)
    legacy_cogs = legacy_rev.values * _S1_AI_COGS_RATIO_2025
    anthropic_cogs = anthropic_rev.values * 0.85
    return YearVector(legacy_cogs + anthropic_cogs)


def compute_terrestrial_capex(inputs: TerrestrialInputs) -> YearVector:
    """Terrestrial data-center CapEx year-row (COLOSSUS path).

    Excel cell:        Assumptions!—
    Excel label:       "Terrestrial AI (COLOSSUS) CapEx ($mm) — year-row"
    Architecture ref:  §10 CapEx
    Principle:         8 (vending-machine module)
    
    Formula: Terrestrial data-center CapEx year-row (COLOSSUS path).

    """
    row = inputs.assumptions.lookup(cl.TERRESTRIAL_AI_CAPEX_YEAR_ROW)
    if row is not None and row.year_values:
        return assumption_year_vector(inputs.assumptions, cl.TERRESTRIAL_AI_CAPEX_YEAR_ROW)
    return YearVector(terrestrial_ai_capex_mm())
