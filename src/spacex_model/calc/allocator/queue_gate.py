"""Queue gate — reserve non-module claims before IRR queue (Architecture §6.2)."""

from __future__ import annotations

import numpy as np

from spacex_model.domain.year_vector import YearVector


def compute_non_module_claims(
    opex: YearVector,
    corp_capex: YearVector,
    spectrum_capex: YearVector,
    taxes: YearVector,
    mars_carveout: YearVector,
    vehicle_build_claim: YearVector,
) -> YearVector:
    """Sum year-N non-module cash claims reserved off-the-top.

    Excel cell:        Allocator!D18:AC18
    Excel label:       "Year-N non-module claims ($mm)"
    Architecture ref:  §6.2 (queue gate)
    Principle:         4 (non-module claims reserved before IRR queue)

    """
    total = (
        opex.values
        + corp_capex.values
        + spectrum_capex.values
        + taxes.values
        + mars_carveout.values
        + vehicle_build_claim.values
    )
    return YearVector(total)


def available_cash_for_irr_queue(
    cash_boy: YearVector,
    non_module_claims: YearVector,
) -> YearVector:
    """Available cash for the IRR queue after non-module claims.

    Excel cell:        Allocator!D29:AC29
    Excel label:       "Available cash for IRR queue ($mm)"
    Architecture ref:  §6.2 (queue gate)
    Principle:         4 (queue gate for non-module claims is LOAD-BEARING)

    Formula: max(0, Cash_BoY − non_module_claims).

    """
    available = np.maximum(0.0, cash_boy.values - non_module_claims.values)
    return YearVector(available)
