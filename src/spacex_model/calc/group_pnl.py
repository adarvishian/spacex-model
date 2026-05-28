"""Group P&L — consolidated walk + conservation block R99-R108 per Architecture §15 / PRD §5.4."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.capex import CapExResult
from spacex_model.calc.opex import OpExResult
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import (
    FIRST_YEAR,
    HORIZON_YEARS,
    LAST_YEAR,
)
from spacex_model.domain.assumption_helpers import assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.conservation import (
    CashIdentityInputs,
    ConservationResult,
    InternalEliminations,
    InternalFlowConservationInputs,
    compute_conservation,
)
from spacex_model.inputs.assumptions import Assumptions

_MODULE_KEYS = ("customer_launch", "starlink", "odc", "ai_stack", "lunar_mars")

__all__ = (
    "CashIdentityInputs",
    "ConservationResult",
    "GroupPnlInputs",
    "GroupPnlResult",
    "InternalEliminations",
    "InternalFlowConservationInputs",
    "compute_group_pnl",
)


@dataclass(frozen=True, slots=True)
class GroupPnlInputs:
    """Full upstream inputs for Group P&L walk."""

    assumptions: Assumptions
    module_outputs: dict[str, AllocatorOut]
    opex: OpExResult
    capex: CapExResult
    eliminations: InternalEliminations
    module_da_in_cogs: dict[str, YearVector]
    internal_flows: InternalFlowConservationInputs
    mars_carveout: YearVector | None = None
    cash_identity: CashIdentityInputs | None = None


@dataclass(frozen=True, slots=True)
class GroupPnlResult:
    """Group P&L tab outputs."""

    module_revenue_gross: YearVector
    group_revenue_net: YearVector
    module_cogs_gross: YearVector
    group_cogs_net: YearVector
    group_gross_profit: YearVector
    total_opex: YearVector
    group_ebitda: YearVector
    group_da: YearVector
    group_ebit: YearVector
    taxes: YearVector
    nopat: YearVector
    total_da_addback: YearVector
    total_group_capex: YearVector
    mars_carveout: YearVector
    group_fcf: YearVector
    adjusted_ebitda: YearVector
    conservation: ConservationResult


def _sum_module_field(
    module_outputs: dict[str, AllocatorOut],
    field: str,
) -> YearVector:
    total = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for key in _MODULE_KEYS:
        out = module_outputs.get(key, AllocatorOut.zeros())
        total += getattr(out, field).values
    return YearVector(total)


def compute_module_revenue_gross(module_outputs: dict[str, AllocatorOut]) -> YearVector:
    """Σ module Total Revenue ($mm) before eliminations.

    Excel cell:        Group P&L!D8
    Excel label:       "Σ Module revenue (gross, pre-elim) ($mm)"
    Architecture ref:  §15.1 group revenue build
    Principle:         9 (internal transfer 4-step pattern)

    """
    return _sum_module_field(module_outputs, "total_revenue")


def compute_group_revenue_net(
    module_revenue_gross: YearVector,
    eliminations: InternalEliminations,
) -> YearVector:
    """Group revenue net of inter-module eliminations.

    Excel cell:        Group P&L!D10
    Excel label:       "GROUP REVENUE NET OF ELIMS ($mm)"
    Architecture ref:  §15.1
    Principle:         9 (elimination row subtracts once)

    """
    return YearVector(module_revenue_gross.values - eliminations.total.values)


def compute_module_cogs_gross(module_outputs: dict[str, AllocatorOut]) -> YearVector:
    """Σ module Total COGS ($mm) before eliminations.

    Excel cell:        Group P&L!D13
    Excel label:       "Σ Module COGS (gross, pre-elim) ($mm)"
    Architecture ref:  §15.1 group COGS build
    Principle:         9 (internal transfers in consumer COGS)

    """
    return _sum_module_field(module_outputs, "total_cogs")


def compute_group_cogs_net(
    module_cogs_gross: YearVector,
    eliminations: InternalEliminations,
) -> YearVector:
    """Group COGS net of inter-module eliminations.

    Excel cell:        Group P&L!D15
    Excel label:       "Group COGS (net of elims) ($mm)"
    Architecture ref:  §15.1
    Principle:         9 (elimination symmetry)

    """
    return YearVector(module_cogs_gross.values - eliminations.total.values)


def compute_group_gross_profit(
    group_revenue_net: YearVector,
    group_cogs_net: YearVector,
) -> YearVector:
    """Group Gross Profit = net revenue − net COGS (= Σ module EBITDA when elims balance).

    Excel cell:        Group P&L!D18
    Excel label:       "Group Gross Profit ($mm)"
    Architecture ref:  §15.1
    Principle:         7 (module EBITDA = gross profit)

    """
    return YearVector(group_revenue_net.values - group_cogs_net.values)


def compute_group_ebitda(
    group_gross_profit: YearVector,
    opex: OpExResult,
) -> YearVector:
    """Group EBITDA = Group Gross Profit − Total OpEx.

    Excel cell:        Group P&L!D26
    Excel label:       "Group EBITDA ($mm)"
    Architecture ref:  §15.1
    Principle:         8 (OpEx only at group level)

    """
    return YearVector(group_gross_profit.values - opex.total_opex.values)


def compute_group_da(
    module_da_in_cogs: dict[str, YearVector],
    capex: CapExResult,
) -> YearVector:
    """Group D&A = Σ module D&A in COGS + Corporate D&A + Spectrum amort.

    Excel cell:        Group P&L!D28
    Excel label:       "Group D&A ($mm)"
    Architecture ref:  §15.1 / §13.4
    Principle:         10 (LM BV decay is NOT Group D&A)

    """
    module_da = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for vec in module_da_in_cogs.values():
        module_da += vec.values
    total = module_da + capex.corporate_da.values + capex.spectrum_amortization.values
    return YearVector(total)


def compute_group_ebit(
    group_ebitda: YearVector,
    capex: CapExResult,
) -> YearVector:
    """Group EBIT = EBITDA − Corporate D&A − Spectrum amort (module D&A already in COGS).

    Excel cell:        Group P&L!D30
    Excel label:       "Group EBIT ($mm)"
    Architecture ref:  §15.1
    Principle:         7 (no double-count of module D&A at EBIT)

    """
    return YearVector(
        group_ebitda.values
        - capex.corporate_da.values
        - capex.spectrum_amortization.values
    )


def compute_taxes(group_ebit: YearVector, tax_rate: float) -> YearVector:
    """Taxes = MAX(0, Group EBIT) × tax rate.

    Excel cell:        Group P&L!D32
    Excel label:       "Taxes ($mm)"
    Architecture ref:  §15.1
    Principle:         8 (corporate tax at group level only)

    """
    return YearVector(np.maximum(0.0, group_ebit.values) * tax_rate)


def compute_nopat(group_ebit: YearVector, taxes: YearVector) -> YearVector:
    """NOPAT = Group EBIT − Taxes.

    Excel cell:        Group P&L!D34
    Excel label:       "NOPAT ($mm)"
    Architecture ref:  §15.1
    Principle:         8 (post-tax operating profit)

    """
    return YearVector(group_ebit.values - taxes.values)


def compute_total_da_addback(
    module_da_in_cogs: dict[str, YearVector],
    capex: CapExResult,
) -> YearVector:
    """Total D&A add-back for FCF = module D&A + corporate D&A + spectrum amort.

    Excel cell:        Group P&L!D39
    Excel label:       "Total D&A add-back ($mm)"
    Architecture ref:  §15.1 FCF walk
    Principle:         8 (non-cash add-back at FCF)

    """
    module_da = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for vec in module_da_in_cogs.values():
        module_da += vec.values
    total = module_da + capex.corporate_da.values + capex.spectrum_amortization.values
    return YearVector(total)


def compute_group_fcf(
    nopat: YearVector,
    total_da_addback: YearVector,
    total_group_capex: YearVector,
    mars_carveout: YearVector,
) -> YearVector:
    """GROUP FCF = NOPAT + D&A add-back − Group CapEx − Mars carve-out (Lock a).

    Excel cell:        Group P&L!D50
    Excel label:       "GROUP FCF ($mm)"
    Architecture ref:  §15.1 + Sprint 9 Lock a
    Principle:         22 (Mars carve-out as real cash drain)

    """
    return YearVector(
        nopat.values + total_da_addback.values - total_group_capex.values - mars_carveout.values
    )


def compute_adjusted_ebitda(
    group_gross_profit: YearVector,
    total_opex: YearVector,
    group_da: YearVector,
    assumptions: Assumptions,
) -> YearVector:
    """S-1 non-GAAP Adj EBITDA memo — MDA §6.8 (P1-7).

    Excel cell:        Group P&L!— (Adj EBITDA memo)
    Excel label:       "Adjusted EBITDA ($mm) — S-1 reconciliation"
    Architecture ref:  §15 Group P&L + MDA §6.8
    Principle:         3 (non-GAAP cross-check; port EBITDA unchanged)

    Formula: operating income + D&A + SBC + restructuring + impairment.
    Operating income ≈ gross profit − OpEx − restructuring − impairment.

    """
    restructuring = assumption_year_vector(
        assumptions, cl.RESTRUCTURING_CHARGES_MM_YEAR_ROW, default=0.0
    )
    impairment = assumption_year_vector(
        assumptions, cl.IMPAIRMENT_CHARGES_MM_YEAR_ROW, default=0.0
    )
    sbc = assumption_year_vector(
        assumptions, cl.SHARE_BASED_COMPENSATION_MM_YEAR_ROW, default=0.0
    )
    operating_income = YearVector(
        group_gross_profit.values
        - total_opex.values
        - restructuring.values
        - impairment.values
    )
    return YearVector(
        operating_income.values
        + group_da.values
        + sbc.values
        + restructuring.values
        + impairment.values
    )


def compute_group_pnl(inputs: GroupPnlInputs) -> GroupPnlResult:
    """Full Group P&L walk from module outputs through FCF.

    Excel cell:        Group P&L!D10:D50
    Excel label:       "GROUP P&L -- consolidated Revenue / EBITDA ..."
    Architecture ref:  §15 Group P&L walk
    Principle:         19 (conservation block must read OK)

    """
    module_rev = compute_module_revenue_gross(inputs.module_outputs)
    group_rev = compute_group_revenue_net(module_rev, inputs.eliminations)
    module_cogs = compute_module_cogs_gross(inputs.module_outputs)
    group_cogs = compute_group_cogs_net(module_cogs, inputs.eliminations)
    gross_profit = compute_group_gross_profit(group_rev, group_cogs)
    ebitda = compute_group_ebitda(gross_profit, inputs.opex)
    group_da = compute_group_da(inputs.module_da_in_cogs, inputs.capex)
    ebit = compute_group_ebit(ebitda, inputs.capex)
    taxes = compute_taxes(ebit, inputs.assumptions.tax_rate)
    nopat = compute_nopat(ebit, taxes)
    da_addback = compute_total_da_addback(inputs.module_da_in_cogs, inputs.capex)
    mars = inputs.mars_carveout or YearVector.constant(1000.0)
    fcf = compute_group_fcf(nopat, da_addback, inputs.capex.total_group_capex, mars)
    adj_ebitda = compute_adjusted_ebitda(
        gross_profit, inputs.opex.total_opex, group_da, inputs.assumptions
    )

    conservation = compute_conservation(
        group_revenue_net=group_rev,
        module_revenue_gross=module_rev,
        eliminations=inputs.eliminations,
        group_gross_profit=gross_profit,
        module_outputs=inputs.module_outputs,
        capex=inputs.capex,
        group_da=group_da,
        module_da_in_cogs=inputs.module_da_in_cogs,
        group_ebitda=ebitda,
        group_ebit=ebit,
        group_fcf=fcf,
        opex=inputs.opex,
        taxes=taxes,
        mars_carveout=mars,
        internal_flows=inputs.internal_flows,
        cash_identity=inputs.cash_identity,
    )

    return GroupPnlResult(
        module_revenue_gross=module_rev,
        group_revenue_net=group_rev,
        module_cogs_gross=module_cogs,
        group_cogs_net=group_cogs,
        group_gross_profit=gross_profit,
        total_opex=inputs.opex.total_opex,
        group_ebitda=ebitda,
        group_da=group_da,
        group_ebit=ebit,
        taxes=taxes,
        nopat=nopat,
        total_da_addback=da_addback,
        total_group_capex=inputs.capex.total_group_capex,
        mars_carveout=mars,
        group_fcf=fcf,
        adjusted_ebitda=adj_ebitda,
        conservation=conservation,
    )
