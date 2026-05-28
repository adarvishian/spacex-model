"""CapEx layer — module aggregation, corporate CapEx, spectrum per Architecture §13 / PRD §5.3."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import CONSERVATION_RESIDUAL_TOLERANCE_MM, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import (
    assumption_scalar,
    assumption_year_vector,
    year_chained_cumulative,
)
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions

_MODULE_KEYS = ("customer_launch", "starlink", "odc", "ai_stack", "lunar_mars")

_CORPORATE_LINES: tuple[tuple[str, str, str, float, float, float], ...] = (
    (
        cl.HQ_BUILDINGS_CAPEX_MM_YR_FLAT,
        cl.HQ_BUILDINGS_USEFUL_LIFE_YEARS,
        "Corporate historical capital base ($mm)",
        0.45,
        50.0,
        30.0,
    ),
    (
        cl.CORPORATE_IT_CAPEX_MM_YR_FLAT,
        cl.CORPORATE_IT_USEFUL_LIFE_YEARS,
        "Corporate historical capital base ($mm)",
        0.15,
        30.0,
        7.0,
    ),
    (
        cl.GENERAL_ENGINEERING_FACILITIES_CAPEX_MM_YR_FLAT,
        cl.GENERAL_ENGINEERING_FACILITIES_LIFE_YEARS,
        "Corporate historical capital base ($mm)",
        0.20,
        20.0,
        20.0,
    ),
    (
        cl.OTHER_CORPORATE_CAPEX_MM_YR_FLAT,
        cl.OTHER_CORPORATE_USEFUL_LIFE_YEARS,
        "Corporate historical capital base ($mm)",
        0.20,
        10.0,
        20.0,
    ),
)


@dataclass(frozen=True, slots=True)
class CapExInputs:
    """Inputs for CapEx tab — module Allocator OUT dict + Assumptions."""

    assumptions: Assumptions
    module_outputs: dict[str, AllocatorOut]
    vehicle_build_claim: YearVector | None = None
    module_da_in_cogs: dict[str, YearVector] | None = None


@dataclass(frozen=True, slots=True)
class CapExResult:
    """CapEx tab outputs."""

    customer_launch_module_capex: YearVector
    starlink_module_capex: YearVector
    odc_module_capex: YearVector
    ai_stack_module_capex: YearVector
    lunar_mars_module_capex: YearVector
    total_module_capex: YearVector
    hq_capex: YearVector
    it_capex: YearVector
    general_engineering_capex: YearVector
    other_corporate_capex: YearVector
    total_corporate_capex: YearVector
    corporate_da: YearVector
    spectrum_capex: YearVector
    cumulative_spectrum_intangible: YearVector
    spectrum_amortization: YearVector
    vehicle_build_claim: YearVector
    total_group_capex: YearVector
    total_group_da: YearVector


def _module_capex(outputs: dict[str, AllocatorOut], key: str) -> YearVector:
    if key in outputs:
        return outputs[key].module_capex
    return YearVector.zeros()


def _flat_annual_capex(assumptions: Assumptions, label: str, default: float) -> YearVector:
    annual = assumption_scalar(assumptions, label, default=default)
    return YearVector.constant(annual)


def compute_module_capex(inputs: CapExInputs) -> dict[str, YearVector]:
    """Read Module CapEx ($mm) from each module Allocator OUT row.

    Excel cell:        CapEx!D11:D15
    Excel label:       "Module CapEx ($mm)"
    Architecture ref:  §13.1 module CapEx aggregation
    Principle:         3 (canonical label INDEX/MATCH)

    """
    out = inputs.module_outputs
    return {
        "customer_launch": _module_capex(out, "customer_launch"),
        "starlink": _module_capex(out, "starlink"),
        "odc": _module_capex(out, "odc"),
        "ai_stack": _module_capex(out, "ai_stack"),
        "lunar_mars": _module_capex(out, "lunar_mars"),
    }


def compute_total_module_capex(module_capex: dict[str, YearVector]) -> YearVector:
    """Sum of five module Module CapEx rows.

    Excel cell:        CapEx!D17
    Excel label:       "Total Module CapEx ($mm)"
    Architecture ref:  §13.1
    Principle:         3 (canonical cross-tab labels)

    """
    total = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for key in _MODULE_KEYS:
        total += module_capex[key].values
    return YearVector(total)


def compute_corporate_capex(inputs: CapExInputs) -> tuple[YearVector, YearVector, YearVector, YearVector, YearVector]:
    """Corporate CapEx flat year-rows from Assumptions §10.

    Excel cell:        CapEx!D20:D23
    Excel label:       "Total Corporate CapEx ($mm)"
    Architecture ref:  §13.2 corporate CapEx
    Principle:         12 (flat year-row reads)

    """
    a = inputs.assumptions
    hq = _flat_annual_capex(a, cl.HQ_BUILDINGS_CAPEX_MM_YR_FLAT, 50.0)
    it = _flat_annual_capex(a, cl.CORPORATE_IT_CAPEX_MM_YR_FLAT, 30.0)
    gen = _flat_annual_capex(a, cl.GENERAL_ENGINEERING_FACILITIES_CAPEX_MM_YR_FLAT, 20.0)
    other = _flat_annual_capex(a, cl.OTHER_CORPORATE_CAPEX_MM_YR_FLAT, 10.0)
    total = YearVector(hq.values + it.values + gen.values + other.values)
    return hq, it, gen, other, total


def compute_corporate_da(inputs: CapExInputs) -> YearVector:
    """Corporate D&A = Σ cumulative category CapEx ÷ useful life (straight-line).

    Excel cell:        CapEx!D37
    Excel label:       "Total Corporate D&A ($mm)"
    Architecture ref:  §13.2 corporate D&A schedule
    Principle:         12 (Rule 23 exception: cumulative CapEx running sum)

    """
    a = inputs.assumptions
    hist_base = assumption_scalar(a, "Corporate historical capital base ($mm)", default=2000.0)
    da_total = np.zeros(HORIZON_YEARS, dtype=np.float64)

    for capex_label, life_label, _, share, default_annual, default_life in _CORPORATE_LINES:
        annual = assumption_scalar(a, capex_label, default=default_annual)
        life = assumption_scalar(a, life_label, default=default_life)
        if life <= 0:
            continue
        initial = hist_base * share + annual
        cumulative = year_chained_cumulative(np.full(HORIZON_YEARS, annual), initial=initial - annual)
        da_total += cumulative / life

    return YearVector(da_total)


def compute_spectrum_capex(inputs: CapExInputs) -> YearVector:
    """EchoStar mid-band spectrum CapEx year-row from Assumptions.

    Excel cell:        CapEx!D36
    Excel label:       "EchoStar mid-band CapEx ($mm) — year-row"
    Architecture ref:  §13.3 spectrum CapEx
    Principle:         12 (anchor year-row from Assumptions)

    """
    row = assumption_year_vector(
        inputs.assumptions,
        cl.ECHOSTAR_MID_BAND_CAPEX_MM_YEAR_ROW,
        default=0.0,
    )
    if row.at(2025) == 0.0 and row.values.sum() == 0.0:
        from spacex_model.inputs.s1_profiles import echostar_spectrum_capex_mm

        row = YearVector(echostar_spectrum_capex_mm())
    return row


def compute_spectrum_amortization(
    spectrum_capex: YearVector,
    assumptions: Assumptions,
) -> tuple[YearVector, YearVector]:
    """Cumulative spectrum intangible and annual amortization ÷ useful life.

    Excel cell:        CapEx!D38
    Excel label:       "Annual spectrum amortization ($mm)"
    Architecture ref:  §13.3 spectrum amortization
    Principle:         12 (Rule 23 exception: cumulative running sum)

    """
    life = assumption_scalar(assumptions, cl.SPECTRUM_USEFUL_LIFE_YEARS, default=15.0)
    cumulative = year_chained_cumulative(spectrum_capex.values)
    if life <= 0:
        z = YearVector.zeros()
        return YearVector(cumulative), z
    amort = YearVector(cumulative / life)
    return YearVector(cumulative), amort


def compute_capex(inputs: CapExInputs) -> CapExResult:
    """Assemble CapEx tab: module + corporate + spectrum + vehicle build claim.

    Excel cell:        CapEx!D45
    Excel label:       "Total Group CapEx ($mm)"
    Architecture ref:  §13 CapEx tab
    Principle:         4 (queue gate reserves non-module claims first)

    """
    module_capex = compute_module_capex(inputs)
    total_module = compute_total_module_capex(module_capex)
    hq, it, gen, other, total_corp = compute_corporate_capex(inputs)
    corporate_da = compute_corporate_da(inputs)
    spectrum = compute_spectrum_capex(inputs)
    cumulative_spectrum, spectrum_amort = compute_spectrum_amortization(spectrum, inputs.assumptions)
    vehicle = inputs.vehicle_build_claim or YearVector.zeros()

    total_group_capex = YearVector(
        total_module.values + total_corp.values + spectrum.values + vehicle.values
    )

    module_da_sum = np.zeros(HORIZON_YEARS, dtype=np.float64)
    if inputs.module_da_in_cogs:
        for vec in inputs.module_da_in_cogs.values():
            module_da_sum += vec.values

    total_group_da = YearVector(
        module_da_sum + corporate_da.values + spectrum_amort.values
    )

    return CapExResult(
        customer_launch_module_capex=module_capex["customer_launch"],
        starlink_module_capex=module_capex["starlink"],
        odc_module_capex=module_capex["odc"],
        ai_stack_module_capex=module_capex["ai_stack"],
        lunar_mars_module_capex=module_capex["lunar_mars"],
        total_module_capex=total_module,
        hq_capex=hq,
        it_capex=it,
        general_engineering_capex=gen,
        other_corporate_capex=other,
        total_corporate_capex=total_corp,
        corporate_da=corporate_da,
        spectrum_capex=spectrum,
        cumulative_spectrum_intangible=cumulative_spectrum,
        spectrum_amortization=spectrum_amort,
        vehicle_build_claim=vehicle,
        total_group_capex=total_group_capex,
        total_group_da=total_group_da,
    )


def capex_conservation_ok(
    result: CapExResult,
    module_outputs: dict[str, AllocatorOut],
) -> bool:
    """Verify Total Module CapEx equals sum of module rows within tolerance.

    Excel cell:        CapEx!R101 proxy
    Excel label:       "CapEx check"
    Architecture ref:  §15.2 conservation block
    Principle:         19 (R101 module CapEx aggregation)

    """
    module_sum = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for key in _MODULE_KEYS:
        module_sum += _module_capex(module_outputs, key).values
    residual = np.abs(result.total_module_capex.values - module_sum)
    return bool(np.all(residual <= CONSERVATION_RESIDUAL_TOLERANCE_MM))
