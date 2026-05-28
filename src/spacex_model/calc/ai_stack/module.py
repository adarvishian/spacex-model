"""AI Stack module — S-1 AI segment + Anthropic compute (P0-7/8) with vending-machine framing.

Architecture §12 / S-1 Adherence Audit §7.2 P0-7, P0-8.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc._vending_machine import build_allocator_out
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions
from spacex_model.inputs.s1_profiles import (
    anthropic_compute_revenue_mm,
    s1_ai_segment_revenue_mm,
    terrestrial_ai_capex_mm,
)

_S1_AI_REVENUE_LABEL = "S-1 AI segment revenue ($mm) — year-row"
_ANTHROPIC_REVENUE_LABEL = "Anthropic compute services revenue ($mm) — year-row"
_TERRESTRIAL_CAPEX_LABEL = "Terrestrial AI data-center CapEx ($mm) — year-row"
_S1_AI_COGS_RATIO_2025 = 2_178.0 / 3_201.0  # S-1 FY2025 AI segment cost of revenue / revenue


@dataclass(frozen=True, slots=True)
class AIStackInputs:
    """Inputs for AI Stack — Assumptions year-rows for S-1 disclosed lines."""

    assumptions: Assumptions


def _ai_segment_revenue(inputs: AIStackInputs) -> YearVector:
    """xAI / X advertising + subscriptions legacy line (S-1 AI segment revenue)."""
    row = inputs.assumptions.lookup(_S1_AI_REVENUE_LABEL)
    if row is not None and row.year_values:
        return assumption_year_vector(inputs.assumptions, _S1_AI_REVENUE_LABEL)
    return YearVector(s1_ai_segment_revenue_mm())


def _anthropic_revenue(inputs: AIStackInputs) -> YearVector:
    """Anthropic Cloud Services Agreement ($1.25B/mo from May 2026)."""
    row = inputs.assumptions.lookup(_ANTHROPIC_REVENUE_LABEL)
    if row is not None and row.year_values:
        return assumption_year_vector(inputs.assumptions, _ANTHROPIC_REVENUE_LABEL)
    return YearVector(anthropic_compute_revenue_mm())


def compute_revenue(inputs: AIStackInputs | None = None) -> YearVector:
    """Total revenue — S-1 AI segment + Anthropic compute services.

    Excel cell:        AI Stack!— (S-1 adherence)
    Excel label:       "Total Revenue ($mm)"
    Architecture ref:  §12 AI Stack; S-1 MDA §1.5
    Principle:         8 (vending-machine)

    """
    if inputs is None:
        return YearVector.zeros()
    legacy = _ai_segment_revenue(inputs)
    anthropic = _anthropic_revenue(inputs)
    return YearVector(legacy.values + anthropic.values)


def compute_cogs(inputs: AIStackInputs | None = None) -> YearVector:
    """COGS — S-1 FY2025 AI segment cost ratio on legacy line; Anthropic at 85% of rev.

    Excel cell:        AI Stack!— (S-1 adherence)
    Excel label:       "Total COGS ($mm)"
    Architecture ref:  §7.3 internal compute transfer (ODC at-cost when live)
    Principle:         9 (at-cost internal compute)

    """
    if inputs is None:
        return YearVector.zeros()
    legacy_rev = _ai_segment_revenue(inputs)
    anthropic_rev = _anthropic_revenue(inputs)
    legacy_cogs = legacy_rev.values * _S1_AI_COGS_RATIO_2025
    anthropic_cogs = anthropic_rev.values * 0.85
    return YearVector(legacy_cogs + anthropic_cogs)


def compute_gross_profit(inputs: AIStackInputs | None = None) -> YearVector:
    """Gross profit = revenue − COGS.

    Excel cell:        AI Stack!— (S-1 adherence)
    Excel label:       "Gross Profit ($mm)"
    Architecture ref:  §3 module framing
    Principle:         7 (Module EBITDA = Gross Profit)

    """
    return YearVector(compute_revenue(inputs).values - compute_cogs(inputs).values)


def compute_capex(inputs: AIStackInputs | None = None) -> YearVector:
    """Terrestrial AI (COLOSSUS) CapEx — S-1 MDA §5.4 year-row.

    Excel cell:        CapEx / AI Stack bridge
    Excel label:       "Terrestrial AI data-center CapEx ($mm) — year-row"
    Architecture ref:  §13 CapEx; S-1 AI segment CapEx
    Principle:         8 (module CapEx separate from corp)

    """
    if inputs is None:
        return YearVector.zeros()
    row = inputs.assumptions.lookup(_TERRESTRIAL_CAPEX_LABEL)
    if row is not None and row.year_values:
        return assumption_year_vector(inputs.assumptions, _TERRESTRIAL_CAPEX_LABEL)
    return YearVector(terrestrial_ai_capex_mm())


def compute_fcf(inputs: AIStackInputs | None = None) -> YearVector:
    """Module FCF = EBITDA − CapEx (no D&A add-back on terrestrial build in v1).

    Excel cell:        AI Stack!— (S-1 adherence)
    Excel label:       "Module FCF ($mm)"
    Architecture ref:  §3 module FCF
    Principle:         8 (pre-tax module FCF)

    """
    ebitda = compute_gross_profit(inputs)
    return YearVector(ebitda.values - compute_capex(inputs).values)


def compute_allocator_out(inputs: AIStackInputs | None = None) -> AllocatorOut:
    """Allocator OUT — AI Stack with S-1 revenue and terrestrial CapEx.

    Excel cell:        AI Stack!— (S-1 adherence)
    Excel label:       "CENTRAL ALLOCATOR OUTPUTS"
    Architecture ref:  §12 AI Stack OUT
    Principle:         3 (canonical labels via registry)

    """
    if inputs is None:
        z = YearVector.zeros()
        return build_allocator_out(revenue=z, cogs=z, capex=z)

    return build_allocator_out(
        revenue=compute_revenue(inputs),
        cogs=compute_cogs(inputs),
        capex=compute_capex(inputs),
        capacity_demand_kg=YearVector.zeros(),
    )
