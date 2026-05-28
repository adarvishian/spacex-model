"""ODC module — orbital compute vending-machine P&L (Phase C).

Architecture §20.8 / PRD §4.4.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc._vending_machine import build_allocator_out
from spacex_model.calc.starlink_capacity import StarlinkCapacityResult
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.irr import compute_irr_engine
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class OdcInputs:
    """Upstream inputs for ODC module."""

    assumptions: Assumptions
    starlink_capacity: StarlinkCapacityResult | None = None
    sats_deployed: YearVector | None = None


def _per_sat_model_a_revenue_mm(assumptions: Assumptions, year_index: int) -> float:
    """Model A: energy-anchored revenue per sat per year ($mm).

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Per-sat Model A revenue ($mm/yr)"
    Architecture ref:  §9.2 Model A
    Principle:         8 (vending-machine module)

    """
    compute_kw = assumption_scalar(assumptions, "Compute power per sat (kW)", default=140.0)
    coreweave = assumption_year_vector(
        assumptions, "CoreWeave baseline anchor ($B/GW_IT/yr, 2026) — year-row", default=12.0
    )
    pue_uplift = assumption_scalar(assumptions, "Orbital PUE uplift vs terrestrial", default=1.12 / 1.4)
    util = assumption_scalar(assumptions, "ODC utilization factor", default=0.85)
    gw = compute_kw / 1e6
    baseline = coreweave.values[year_index] if year_index < HORIZON_YEARS else coreweave.at(FIRST_YEAR)
    return gw * baseline * pue_uplift * util * 1000.0


def _per_sat_model_b_revenue_mm(assumptions: Assumptions, year_index: int) -> float:
    """Model B: η-anchored GPU-hour revenue per sat per year ($mm).

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Per-sat Model B revenue ($mm/yr)"
    Architecture ref:  §9.2 Model B
    Principle:         8 (vending-machine module)

    """
    compute_kw = assumption_scalar(assumptions, "Compute power per sat (kW)", default=140.0)
    chip_tdp = assumption_year_vector(assumptions, "Chip TDP per chip (W) — year-row", default=700.0)
    chip_fp8 = assumption_year_vector(
        assumptions, "Chip FP8 performance per chip (TFLOPS) — year-row", default=1979.0
    )
    util = assumption_scalar(assumptions, "ODC utilization factor", default=0.85)
    ecr = assumption_scalar(assumptions, "Effective Compute Ratio (ECR)", default=0.6)
    mix = assumption_scalar(assumptions, "Workload mix — inference share", default=0.85)
    price_gpu_hr = assumption_year_vector(
        assumptions, "Price per H100-equiv GPU-hr ($) — year-row", default=2.0
    )

    tdp = chip_tdp.values[year_index]
    fp8 = chip_fp8.values[year_index]
    if tdp <= 0:
        return 0.0
    price = price_gpu_hr.values[year_index]
    billable = (compute_kw * 1000.0 / tdp) * fp8 / 1e6 * 8760.0 * util * ecr * mix * price / 1e6
    return billable


def per_sat_combined_revenue_mm(assumptions: Assumptions, year_index: int) -> float:
    """Credence-weighted Model A/B per-sat revenue ($mm/yr).

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Per-sat combined revenue ($mm/yr)"
    Architecture ref:  §9.2 dual revenue
    Principle:         8 (Pr(A) credence-weighted)

    """
    pr_a = assumption_scalar(assumptions, "Credence on Model A (Pr(A))", default=0.6)
    a = _per_sat_model_a_revenue_mm(assumptions, year_index)
    b = _per_sat_model_b_revenue_mm(assumptions, year_index)
    return pr_a * a + (1.0 - pr_a) * b


def per_sat_bandwidth_cost_mm(
    assumptions: Assumptions,
    starlink_capacity: StarlinkCapacityResult | None,
    year_index: int,
) -> float:
    """Per-sat bandwidth services cost from Starlink Capacity pool rates.

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Bandwidth services cost ($mm)"
    Architecture ref:  §7.2 / §9.4
    Principle:         9 (at-cost internal bandwidth)

    """
    if starlink_capacity is None:
        return 0.0
    bb_share = assumption_scalar(assumptions, "BB-share of ODC bandwidth claim", default=0.5)
    gbps_per_gwh = assumption_scalar(assumptions, "Gbps per GWh/yr of ODC compute energy", default=0.05)
    compute_kw = assumption_scalar(assumptions, "Compute power per sat (kW)", default=140.0)
    gbps_per_sat = gbps_per_gwh * compute_kw
    bb_rate = starlink_capacity.bb_at_cost_rate_per_gbps.values[year_index] / 1e6
    dtc_rate = starlink_capacity.dtc_at_cost_rate_per_gbps.values[year_index] / 1e6
    return bb_share * gbps_per_sat * bb_rate + (1.0 - bb_share) * gbps_per_sat * dtc_rate


def per_sat_net_marginal_revenue_mm(
    assumptions: Assumptions,
    starlink_capacity: StarlinkCapacityResult | None,
    year_index: int,
) -> float:
    """Combined revenue minus opex and bandwidth per sat ($mm/yr).

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Per-sat net marginal revenue ($mm/yr)"
    Architecture ref:  §9.4 IRR engine input
    Principle:         2 (per-unit marginal IRR)

    """
    combined = per_sat_combined_revenue_mm(assumptions, year_index)
    ground = assumption_scalar(assumptions, "ODC ground ops % of revenue", default=0.05)
    insurance = assumption_scalar(assumptions, "ODC insurance % of revenue", default=0.01)
    other = assumption_scalar(assumptions, "ODC other COGS % of revenue", default=0.03)
    opex = combined * (ground + insurance + other)
    bandwidth = per_sat_bandwidth_cost_mm(assumptions, starlink_capacity, year_index)
    return combined - opex - bandwidth


def _fleet_from_deployment(deployed: YearVector | None) -> YearVector:
    if deployed is None:
        return YearVector.zeros()
    fleet = np.zeros(HORIZON_YEARS, dtype=np.float64)
    active = 0.0
    for t in range(HORIZON_YEARS):
        active += deployed.values[t]
        fleet[t] = active
    return YearVector(fleet)


def odc_bandwidth_claim(inputs: OdcInputs) -> tuple[YearVector, YearVector]:
    """BB and DTC Gbps claim for Starlink Capacity (fleet × per-sat Gbps).

    Excel cell:        ODC!— (Phase C)
    Excel label:       "ODC BB Gbps demand"
    Architecture ref:  §7.2
    Principle:         3 (canonical cross-tab labels)

    """
    fleet = _fleet_from_deployment(inputs.sats_deployed)
    bb_share = assumption_scalar(inputs.assumptions, "BB-share of ODC bandwidth claim", default=0.5)
    gbps = assumption_scalar(inputs.assumptions, "Gbps per GWh/yr of ODC compute energy", default=0.05)
    compute_kw = assumption_scalar(inputs.assumptions, "Compute power per sat (kW)", default=140.0)
    per_sat = gbps * compute_kw
    bb = fleet.values * per_sat * bb_share
    dtc = fleet.values * per_sat * (1.0 - bb_share)
    return YearVector(bb), YearVector(dtc)


def compute_revenue(inputs: OdcInputs | None = None) -> YearVector:
    """External + internal compute revenue; zero fleet under D6 Base Case.

    Excel cell:        ODC!D— (Phase C)
    Excel label:       "Total Revenue ($mm)"
    Architecture ref:  §20.8 ODC revenue
    Principle:         8 (vending-machine module)

    """
    if inputs is None:
        return YearVector.zeros()
    deployed = inputs.sats_deployed or YearVector.zeros()
    external_share = assumption_year_vector(
        inputs.assumptions, "ODC external compute share to customers % — year-row", default=0.05
    )
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        if deployed.values[t] <= 0:
            continue
        ext_rev = per_sat_combined_revenue_mm(inputs.assumptions, t) * external_share.values[t]
        values[t] = ext_rev * deployed.values[t]
    return YearVector(values)


def compute_cogs(inputs: OdcInputs | None = None) -> YearVector:
    """Bandwidth, launch, sat D&A COGS — zero at zero deployment.

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Total COGS ($mm)"
    Architecture ref:  §20.8 ODC COGS
    Principle:         9 (at-cost internal bandwidth from Starlink Capacity)

    """
    if inputs is None:
        return YearVector.zeros()
    deployed = inputs.sats_deployed or YearVector.zeros()
    values = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        if deployed.values[t] <= 0:
            continue
        bw = per_sat_bandwidth_cost_mm(inputs.assumptions, inputs.starlink_capacity, t)
        values[t] = bw * deployed.values[t]
    return YearVector(values)


def compute_gross_profit(inputs: OdcInputs | None = None) -> YearVector:
    """Gross profit = revenue − COGS.

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Gross Profit ($mm)"
    Architecture ref:  §3 module framing
    Principle:         7 (Module EBITDA = Gross Profit)

    """
    if inputs is None:
        return YearVector.zeros()
    return YearVector(compute_revenue(inputs).values - compute_cogs(inputs).values)


def compute_capex(inputs: OdcInputs | None = None) -> YearVector:
    """Satellite manufacturing + launch CapEx at zero deployment.

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Module CapEx ($mm)"
    Architecture ref:  §20.8 ODC CapEx
    Principle:         8 (no corp overhead on module)

    """
    if inputs is None:
        return YearVector.zeros()
    return YearVector.zeros()


def compute_fcf(inputs: OdcInputs | None = None) -> YearVector:
    """Module FCF = EBITDA − CapEx (zero under D6 verdict).

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Module FCF ($mm)"
    Architecture ref:  §3 module FCF
    Principle:         8 (pre-tax module FCF)

    """
    if inputs is None:
        return YearVector.zeros()
    return YearVector(compute_gross_profit(inputs).values - compute_capex(inputs).values)


def per_sat_blended_irr(inputs: OdcInputs) -> float:
    """Per-sat blended IRR for 2025 gate (expected ≤ 0 per D6).

    Excel cell:        ODC!— (Phase C)
    Excel label:       "Blended IRR"
    Architecture ref:  §9.4
    Principle:         2 (per-unit marginal IRR)

    """
    a = inputs.assumptions
    cost = 50.0
    if a.lookup("V3 BB sat unit cost ($mm/sat)") is not None:
        cost = assumption_scalar(a, "V3 BB sat unit cost ($mm/sat)", default=50.0)
    n = int(assumption_scalar(a, "ODC fleet design life (years)", default=5.0))
    rev = np.array(
        [per_sat_net_marginal_revenue_mm(a, inputs.starlink_capacity, t) for t in range(n)],
        dtype=np.float64,
    )
    result = compute_irr_engine(cost, rev, horizon_n=n)
    return result.blended


def compute_allocator_out(inputs: OdcInputs | None = None) -> AllocatorOut:
    """Allocator OUT contract — zeros under negative-IRR D6 verdict.

    Excel cell:        ODC!— (Phase C)
    Excel label:       "CENTRAL ALLOCATOR OUTPUTS"
    Architecture ref:  §20.8 Allocator OUT
    Principle:         3 (canonical labels via registry)

    """
    if inputs is None:
        z = YearVector.zeros()
        return build_allocator_out(revenue=z, cogs=z, capex=z)

    revenue = compute_revenue(inputs)
    cogs = compute_cogs(inputs)
    capex = compute_capex(inputs)
    irr_val = per_sat_blended_irr(inputs)
    irr_vec = YearVector.constant(max(irr_val, -1.0))
    return build_allocator_out(
        revenue=revenue,
        cogs=cogs,
        capex=capex,
        spot_irr=irr_vec,
        forward_irr=irr_vec,
        blended_irr=irr_vec,
    )
