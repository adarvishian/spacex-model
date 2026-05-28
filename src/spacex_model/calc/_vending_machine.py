"""Vending-machine P&L helpers — Revenue → COGS → EBITDA → CapEx → FCF."""

from __future__ import annotations

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.domain.year_vector import YearVector


def compute_gross_profit(revenue: YearVector, cogs: YearVector) -> YearVector:
    """Gross profit = revenue − COGS (Module EBITDA label equals this per Principle 7).

    Excel cell:        — (shared helper)
    Excel label:       "Gross Profit ($mm)"
    Architecture ref:  §3 module framing
    Principle:         7 (Module EBITDA = Gross Profit)

    """
    return YearVector(revenue.values - cogs.values)


def compute_module_ebitda(gross_profit: YearVector) -> YearVector:
    """Module EBITDA equals gross profit; no R&D / SG&A / tax on module tabs.

    Excel cell:        — (shared helper)
    Excel label:       "Module EBITDA ($mm)"
    Architecture ref:  §3 module framing
    Principle:         7 (Module EBITDA = Gross Profit)

    """
    return gross_profit


def compute_module_fcf(
    module_ebitda: YearVector,
    module_capex: YearVector,
    *,
    module_da_addback: YearVector | None = None,
) -> YearVector:
    """Module FCF = EBITDA + module D&A add-back − Module CapEx.

    Excel cell:        — (shared helper)
    Excel label:       "Module FCF ($mm)"
    Architecture ref:  §3 module FCF definition
    Principle:         8 (pre-tax module FCF)

    """
    da = module_da_addback if module_da_addback is not None else YearVector.zeros()
    return YearVector(module_ebitda.values + da.values - module_capex.values)


def build_allocator_out(
    *,
    revenue: YearVector,
    cogs: YearVector,
    capex: YearVector,
    capital_deployed: YearVector | None = None,
    capacity_demand_kg: YearVector | None = None,
    spot_irr: YearVector | None = None,
    forward_irr: YearVector | None = None,
    blended_irr: YearVector | None = None,
    module_da_addback: YearVector | None = None,
) -> AllocatorOut:
    """Assemble the 11-row Allocator OUT contract from vending-machine sections.

    Excel cell:        — (shared helper)
    Excel label:       "CENTRAL ALLOCATOR OUTPUTS"
    Architecture ref:  §4 Allocator OUT contract
    Principle:         3 (canonical cross-tab labels)

    """
    gross = compute_gross_profit(revenue, cogs)
    ebitda = compute_module_ebitda(gross)
    fcf = compute_module_fcf(ebitda, capex, module_da_addback=module_da_addback)
    z = YearVector.zeros()
    return AllocatorOut(
        total_revenue=revenue,
        total_cogs=cogs,
        gross_profit=gross,
        module_ebitda=ebitda,
        module_capex=capex,
        module_fcf=fcf,
        capital_deployed=capital_deployed if capital_deployed is not None else z,
        capacity_demand_kg=capacity_demand_kg if capacity_demand_kg is not None else z,
        spot_irr=spot_irr if spot_irr is not None else z,
        forward_irr=forward_irr if forward_irr is not None else z,
        blended_irr=blended_irr if blended_irr is not None else z,
    )
