"""ODC strategic seed — pre-revenue ramp off both pools, graduates on lagged IRR (U3 / D4)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc.allocator.priority import _soft_floor
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class StrategicSeedInputs:
    """Predetermined inputs for ODC pre-revenue seed (acyclic)."""

    assumptions: Assumptions
    odc_demand_buildable: YearVector
    odc_kg_demand: YearVector
    prior_odc_irr: YearVector
    pool_after_carveout: YearVector


@dataclass(frozen=True, slots=True)
class StrategicSeedResult:
    """Senior ODC seed claim — cash + kg reserved before growth allocation."""

    cash_claim: YearVector
    kg_reserved: YearVector
    graduated: YearVector
    remaining_pool: YearVector


def _graduation_irr(assumptions: Assumptions) -> float:
    return _soft_floor(assumptions)


def _ramp_fraction(year: int, first_build_year: int, ramp_years: int) -> float:
    if year < first_build_year:
        return 0.0
    if ramp_years <= 0:
        return 1.0
    elapsed = year - first_build_year + 1
    return min(1.0, elapsed / ramp_years)


def compute_strategic_seed(inputs: StrategicSeedInputs) -> StrategicSeedResult:
    """ODC pre-revenue seed — senior claim after LM carve-out, sunsets on prior-yr IRR.

    Excel cell:        Cash Allocation Engine (U3 Python senior claim — folded into spine)
    Excel label:       "ODC strategic seed cash ($mm)"
    Architecture ref:  PRD §5.2 + D4 strategic seed
    Principle:         2 (prior-yr IRR graduation; no this-year returns)

    Formula: ODC pre-revenue seed — senior claim after LM carve-out, sunsets on prior-yr IRR.

    """
    a = inputs.assumptions
    first_build = int(assumption_scalar(a, cl.AI_ODC_FIRST_COMPUTE_SAT_BUILD_YEAR))
    ramp_years = 3
    grad_irr = _graduation_irr(a)

    cash_claim = np.zeros(HORIZON_YEARS, dtype=np.float64)
    kg_reserved = np.zeros(HORIZON_YEARS, dtype=np.float64)
    graduated = np.zeros(HORIZON_YEARS, dtype=np.float64)
    remaining = inputs.pool_after_carveout.values.copy()

    buildable = inputs.odc_demand_buildable.values
    kg_demand = inputs.odc_kg_demand.values
    prior_irr = inputs.prior_odc_irr.values

    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        if year == FIRST_YEAR:
            continue

        if t > 0 and prior_irr[t - 1] >= grad_irr:
            graduated[t] = 1.0
            continue

        ramp = _ramp_fraction(year, first_build, ramp_years)
        if ramp <= 0.0:
            continue

        target_cash = buildable[t] * ramp
        target_kg = kg_demand[t] * ramp
        claim = min(target_cash, max(0.0, remaining[t]))
        cash_claim[t] = claim
        kg_reserved[t] = target_kg if claim > 0.0 else 0.0
        remaining[t] = max(0.0, remaining[t] - claim)

    return StrategicSeedResult(
        cash_claim=YearVector(cash_claim),
        kg_reserved=YearVector(kg_reserved),
        graduated=YearVector(graduated),
        remaining_pool=YearVector(remaining),
    )
