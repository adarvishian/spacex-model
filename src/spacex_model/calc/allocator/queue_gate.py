"""Queue gate — reserve non-module claims before IRR queue (CAE R13–R21)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class QueueGateResult:
    """CAE queue gate claim breakdown."""

    corp_sga: YearVector
    shared_rd: YearVector
    corp_capex: YearVector
    spectrum_capex: YearVector
    taxes: YearVector
    vehicle_build_claim: YearVector
    non_module_claims_total: YearVector
    pool_after_gate: YearVector


def compute_queue_gate(
    cash_available: YearVector,
    *,
    corp_sga: YearVector,
    shared_rd: YearVector,
    corp_capex: YearVector,
    spectrum_capex: YearVector,
    taxes: YearVector,
    vehicle_build_claim: YearVector,
) -> QueueGateResult:
    """Reserve corporate claims; LM carve-out applied separately in carve_out.py.

    Excel cell:        Cash Allocation Engine!D20:D21
    Excel label:       "Queue gate non-module claims total ($mm)" … "Pool after queue gate ($mm)"
    Architecture ref:  §2.3 queue gate
    Principle:         4 (non-module claims reserved before IRR queue)

    """
    total = (
        corp_sga.values
        + shared_rd.values
        + corp_capex.values
        + spectrum_capex.values
        + taxes.values
        + vehicle_build_claim.values
    )
    pool = np.maximum(0.0, cash_available.values - total)
    return QueueGateResult(
        corp_sga=corp_sga,
        shared_rd=shared_rd,
        corp_capex=corp_capex,
        spectrum_capex=spectrum_capex,
        taxes=taxes,
        vehicle_build_claim=vehicle_build_claim,
        non_module_claims_total=YearVector(total),
        pool_after_gate=YearVector(pool),
    )


def compute_non_module_claims(
    opex: YearVector,
    corp_capex: YearVector,
    spectrum_capex: YearVector,
    taxes: YearVector,
    mars_carveout: YearVector,
    vehicle_build_claim: YearVector,
) -> YearVector:
    """Legacy sum including LM carve-out — used by conservation checks.
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
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
    """Available cash for IRR queue after non-module claims (legacy alias).
    Excel cell:        V4.113 (canonical label registry)
    Excel label:       (see module docstring)
    Architecture ref:  PRD V4.113 §2 / context.md §6
    Principle:         6 (one-tab-one-module)
"""
    available = np.maximum(0.0, cash_boy.values - non_module_claims.values)
    return YearVector(available)
