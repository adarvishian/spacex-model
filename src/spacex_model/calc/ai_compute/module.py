"""AI - Compute module — unified ODC + Terrestrial DC + AI Apps vending-machine P&L.

Architecture §9 / V4.113 AI - Compute tab (merges V2.16 ODC + AI Stack).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc._vending_machine import build_allocator_out
from spacex_model.calc.ai_compute.orbital_dc import (
    OrbitalDcInputs,
    compute_orbital_cogs,
    compute_orbital_revenue,
    orbital_bandwidth_claim,
    per_sat_blended_irr,
)
from spacex_model.calc.allocator.cap_base import compute_chip_at_cost_per_sat
from spacex_model.calc.facilities_build import FacilitiesBuildResult
from spacex_model.calc.ai_compute.terrestrial import (
    TerrestrialInputs,
    compute_ai_apps_revenue,
    compute_terrestrial_capex,
    compute_terrestrial_cogs,
    compute_terrestrial_dc_revenue,
    compute_terrestrial_revenue,
)
from spacex_model.calc.starlink_capacity import StarlinkCapacityResult
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


@dataclass(frozen=True, slots=True)
class AiComputeInputs:
    """Upstream inputs for unified AI - Compute module."""

    assumptions: Assumptions
    starlink_capacity: StarlinkCapacityResult | None = None
    sats_deployed: YearVector | None = None
    facilities_build: FacilitiesBuildResult | None = None
    chip_at_cost_per_sat: YearVector | None = None


def _chip_at_cost(inputs: AiComputeInputs) -> YearVector:
    if inputs.chip_at_cost_per_sat is not None:
        return inputs.chip_at_cost_per_sat
    return compute_chip_at_cost_per_sat(inputs.assumptions, inputs.facilities_build)


def _orbital(inputs: AiComputeInputs) -> OrbitalDcInputs:
    return OrbitalDcInputs(
        assumptions=inputs.assumptions,
        starlink_capacity=inputs.starlink_capacity,
        sats_deployed=inputs.sats_deployed,
        chip_at_cost_per_sat=_chip_at_cost(inputs),
    )


def _terrestrial(inputs: AiComputeInputs) -> TerrestrialInputs:
    return TerrestrialInputs(assumptions=inputs.assumptions)


def odc_bandwidth_claim(inputs: AiComputeInputs) -> tuple[YearVector, YearVector]:
    """Re-export for Starlink Capacity / internal-flow wiring.

    Excel cell:        AI - Compute!—
    Excel label:       "ODC BB Gbps demand"
    Architecture ref:  §7.2
    Principle:         3 (canonical cross-tab labels)
    
    Formula: Re-export for Starlink Capacity / internal-flow wiring.

    """
    return orbital_bandwidth_claim(_orbital(inputs))


def compute_revenue(inputs: AiComputeInputs | None = None) -> YearVector:
    """Total revenue — Orbital DC + Terrestrial DC + AI Apps.

    Excel cell:        AI - Compute!—
    Excel label:       "Revenue: AI - Compute"
    Architecture ref:  §9 unified AI - Compute
    Principle:         8 (vending-machine module)
    
    Formula: Total revenue — Orbital DC + Terrestrial DC + AI Apps.

    """
    if inputs is None:
        return YearVector.zeros()
    orbital = compute_orbital_revenue(_orbital(inputs))
    terrestrial = compute_terrestrial_revenue(_terrestrial(inputs))
    return YearVector(orbital.values + terrestrial.values)


def compute_orbital_dc_revenue(inputs: AiComputeInputs) -> YearVector:
    """Sub-line: Orbital DC external revenue.

    Excel cell:        AI - Compute!—
    Excel label:       "Revenue: Orbital DC"
    Architecture ref:  §9 unified AI - Compute
    Principle:         8 (vending-machine module)
    
    Formula: Sub-line: Orbital DC external revenue.

    """
    return compute_orbital_revenue(_orbital(inputs))


def compute_terrestrial_dc_revenue_line(inputs: AiComputeInputs) -> YearVector:
    """Sub-line: Terrestrial DC external revenue.

    Excel cell:        AI - Compute!—
    Excel label:       "Revenue: Terrestrial DC"
    Architecture ref:  §9 unified AI - Compute
    Principle:         8 (vending-machine module)
    
    Formula: Sub-line: Terrestrial DC external revenue.

    """
    return compute_terrestrial_dc_revenue(_terrestrial(inputs))


def compute_ai_apps_revenue_line(inputs: AiComputeInputs) -> YearVector:
    """Sub-line: AI Apps external revenue.

    Excel cell:        AI - Compute!—
    Excel label:       "Revenue: AI Apps"
    Architecture ref:  §9 unified AI - Compute
    Principle:         8 (vending-machine module)
    
    Formula: Sub-line: AI Apps external revenue.

    """
    return compute_ai_apps_revenue(_terrestrial(inputs))


def compute_cogs(inputs: AiComputeInputs | None = None) -> YearVector:
    """Total COGS — orbital bandwidth + terrestrial cost ratio.

    Excel cell:        AI - Compute!—
    Excel label:       "COGS: AI - Compute"
    Architecture ref:  §9 unified COGS
    Principle:         9 (at-cost internal transfers)
    
    Formula: Total COGS — orbital bandwidth + terrestrial cost ratio.

    """
    if inputs is None:
        return YearVector.zeros()
    orbital = compute_orbital_cogs(_orbital(inputs))
    terrestrial = compute_terrestrial_cogs(_terrestrial(inputs))
    return YearVector(orbital.values + terrestrial.values)


def compute_gross_profit(inputs: AiComputeInputs | None = None) -> YearVector:
    """Gross profit = revenue − COGS.

    Excel cell:        AI - Compute!—
    Excel label:       "Gross Profit ($mm)"
    Architecture ref:  §3 module framing
    Principle:         7 (Module EBITDA = Gross Profit)
    
    Formula: Gross profit = revenue − COGS.

    """
    if inputs is None:
        return YearVector.zeros()
    return YearVector(compute_revenue(inputs).values - compute_cogs(inputs).values)


def compute_capex(inputs: AiComputeInputs | None = None) -> YearVector:
    """Growth-slice Module CapEx — demand-buildable only; Terafab excluded (bucket 2).

    Excel cell:        AI - Compute!—
    Excel label:       "Module CapEx ($mm)"
    Architecture ref:  §9 unified AI - Compute + U1 three-bucket split
    Principle:         8 (vending-machine module; enabling infra out of IRR base)
    
    Formula: Growth-slice Module CapEx — demand-buildable only; Terafab excluded (bucket 2).

    """
    if inputs is None:
        return YearVector.zeros()
    return compute_terrestrial_capex(_terrestrial(inputs))


def compute_fcf(inputs: AiComputeInputs | None = None) -> YearVector:
    """Module FCF = EBITDA − CapEx.

    Excel cell:        AI - Compute!—
    Excel label:       "Module FCF ($mm)"
    Architecture ref:  §3 module framing
    Principle:         8 (vending-machine module)
    
    Formula: Module FCF = EBITDA − CapEx.

    """
    if inputs is None:
        return YearVector.zeros()
    return YearVector(compute_gross_profit(inputs).values - compute_capex(inputs).values)


def compute_allocator_out(inputs: AiComputeInputs | None = None) -> AllocatorOut:
    """Allocator OUT — blended orbital IRR + terrestrial revenue.

    Excel cell:        AI - Compute!—
    Excel label:       "CENTRAL ALLOCATOR OUTPUTS"
    Architecture ref:  §9 Allocator OUT (V4.113 CAE AI-Compute roll-up)
    Principle:         3 (canonical labels via registry)
    
    Formula: Allocator OUT — blended orbital IRR + terrestrial revenue.

    """
    if inputs is None:
        z = YearVector.zeros()
        return build_allocator_out(revenue=z, cogs=z, capex=z)

    revenue = compute_revenue(inputs)
    cogs = compute_cogs(inputs)
    capex = compute_capex(inputs)
    irr_val = per_sat_blended_irr(_orbital(inputs))
    irr_vec = YearVector.constant(max(irr_val, -1.0))
    return build_allocator_out(
        revenue=revenue,
        cogs=cogs,
        capex=capex,
        spot_irr=irr_vec,
        forward_irr=irr_vec,
        blended_irr=irr_vec,
    )

