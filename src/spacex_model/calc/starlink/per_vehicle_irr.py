"""Per-vehicle marginal IRR engines — V2 BB, V2 DTC, V3 BB, V3 DTC (PRD §4.3 / §15)."""

from __future__ import annotations

from typing import Literal

import numpy as np

from spacex_model.calc.allocator.types import QueueSubBlockIrrs
from spacex_model.calc.starlink import vehicle_pools as vp
from spacex_model.calc.starlink.module import StarlinkInputs
from spacex_model.calc.starlink.vehicle_pools import VehiclePoolSpec
from spacex_model.domain.assumption_helpers import assumption_scalar
from spacex_model.domain.irr import IrrResult, compute_irr_engine
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions

__all__ = [
    "IrrResult",
    "compute_irr_engine",
    "compute_v2_bb_irr",
    "compute_v2_dtc_irr",
    "compute_v3_bb_irr",
    "compute_v3_dtc_irr",
    "build_starlink_vehicle_irrs",
]


def _variable_cost_pct(assumptions: Assumptions) -> float:
    ground = assumption_scalar(assumptions, "Starlink ground ops % of revenue", default=0.04)
    insurance = assumption_scalar(assumptions, "Starlink insurance % of revenue", default=0.01)
    other = assumption_scalar(assumptions, "Starlink other COGS % of revenue", default=0.02)
    return ground + insurance + other


def _annual_da_mm(spec: VehiclePoolSpec, assumptions: Assumptions) -> float:
    bb_life = assumption_scalar(
        assumptions, "Satellite useful life — V2 Mini (years)", default=5.0
    )
    dep = assumption_scalar(
        assumptions,
        "Satellite Dep per kg — base year ($/kg/yr)",
        default=128.8,
    )
    scale = bb_life / max(spec.useful_life_years, 1)
    return dep * scale * spec.mass_kg / 1e6


def _annual_gross_mm(
    spec: VehiclePoolSpec,
    assumptions: Assumptions,
    *,
    band: Literal["bb", "dtc"],
) -> float:
    if band == "bb":
        rev_per_gbps = assumption_scalar(
            assumptions,
            "Starshield Rev per Gbps — base year ($/Gbps)",
            default=164699.0,
        )
        return spec.bb_gbps_per_sat * rev_per_gbps / 1e6
    arpu = assumption_scalar(assumptions, "DTC ARPU ($/sub/mo, year-row)", default=16.0)
    return arpu * 12.0 / 1e6


def _engine_for_pool(
    spec: VehiclePoolSpec,
    assumptions: Assumptions,
    *,
    band: Literal["bb", "dtc"],
) -> IrrResult:
    """Shared per-sat IRR engine for one vehicle pool."""
    gross = _annual_gross_mm(spec, assumptions, band=band)
    net = gross * (1.0 - _variable_cost_pct(assumptions)) - _annual_da_mm(spec, assumptions)
    n = spec.useful_life_years
    rev = np.full(n, max(net, 0.0), dtype=np.float64)
    return compute_irr_engine(spec.unit_cost_mm, rev, horizon_n=n)


def _irr_year_vector(result: IrrResult) -> YearVector:
    return YearVector.constant(result.blended)


def compute_v2_bb_irr(inputs: StarlinkInputs) -> YearVector:
    """V2 BB per-sat blended IRR engine.

    Excel cell:        Starlink!— (V2 BB pool)
    Excel label:       "V2 BB Blended IRR"
    Architecture ref:  §8.4 per-vehicle IRR
    Principle:         2 (per-unit marginal IRR)

    """
    spec = vp._pool_spec_v2_bb(inputs.assumptions)
    return _irr_year_vector(_engine_for_pool(spec, inputs.assumptions, band="bb"))


def compute_v2_dtc_irr(inputs: StarlinkInputs) -> YearVector:
    """V2 DTC per-sat blended IRR engine.

    Excel cell:        Starlink!— (V2 DTC pool)
    Excel label:       "V2 DTC Blended IRR"
    Architecture ref:  §8.4 per-vehicle IRR
    Principle:         2 (per-unit marginal IRR)

    """
    spec = vp._pool_spec_v2_dtc(inputs.assumptions)
    return _irr_year_vector(_engine_for_pool(spec, inputs.assumptions, band="dtc"))


def compute_v3_bb_irr(inputs: StarlinkInputs) -> YearVector:
    """V3 BB per-sat blended IRR engine.

    Excel cell:        Starlink!— (V3 BB pool)
    Excel label:       "V3 BB Blended IRR"
    Architecture ref:  §8.4 per-vehicle IRR
    Principle:         2 (per-unit marginal IRR)

    """
    spec = vp._pool_spec_v3_bb(inputs.assumptions)
    return _irr_year_vector(_engine_for_pool(spec, inputs.assumptions, band="bb"))


def compute_v3_dtc_irr(inputs: StarlinkInputs) -> YearVector:
    """V3 DTC per-sat blended IRR engine.

    Excel cell:        Starlink!— (V3 DTC pool)
    Excel label:       "V3 DTC Blended IRR"
    Architecture ref:  §8.4 per-vehicle IRR
    Principle:         2 (per-unit marginal IRR)

    """
    spec = vp._pool_spec_v3_dtc(inputs.assumptions)
    return _irr_year_vector(_engine_for_pool(spec, inputs.assumptions, band="dtc"))


def build_starlink_vehicle_irrs(inputs: StarlinkInputs) -> QueueSubBlockIrrs:
    """Roll four Starlink pool IRR year-vectors into a queue sub-block slice.

    Excel cell:        Allocator!D153:AC156 (Starlink vehicle IRR rows)
    Excel label:       "V2 BB / V2 DTC / V3 BB / V3 DTC Blended IRR"
    Architecture ref:  §8.4 per-vehicle IRR
    Principle:         2 (per-unit marginal IRR drives sigmoid weights)

    Non-Starlink slots in the returned struct are zeroed for irr_display roll-up.

    """
    z = YearVector.zeros()
    return QueueSubBlockIrrs(
        customer_launch=z,
        starlink_v2_bb=compute_v2_bb_irr(inputs),
        starlink_v2_dtc=compute_v2_dtc_irr(inputs),
        starlink_v3_bb=compute_v3_bb_irr(inputs),
        starlink_v3_dtc=compute_v3_dtc_irr(inputs),
        odc=z,
        ai_stack=z,
    )
