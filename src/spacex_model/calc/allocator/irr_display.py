"""Central IRR display — roll-up from module Allocator OUT (Architecture §6)."""

from __future__ import annotations

import numpy as np

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.ai_compute.orbital_dc import OrbitalDcInputs, per_sat_blended_irr
from spacex_model.calc.allocator.cap_base import compute_chip_at_cost_per_sat
from spacex_model.calc.allocator.priority import FourProgramIrrs, ModuleSpotIrrs
from spacex_model.calc.allocator.types import QueueSubBlockIrrs
from spacex_model.calc.facilities_build import FacilitiesBuildResult
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.assumption_helpers import assumption_scalar, assumption_year_vector
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions


def _prior_year(values: np.ndarray) -> np.ndarray:
    out = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(1, HORIZON_YEARS):
        out[t] = values[t - 1]
    return out


def compute_module_spot_irrs(module_outputs: dict[str, AllocatorOut]) -> ModuleSpotIrrs:
    """Prior-year spot IRR for CAE softmax (acyclicity firewall).

    Excel cell:        Cash Allocation Engine!D28:D30
    Excel label:       "Spot IRR: Starlink" … "Spot IRR: AI-Compute"
    Architecture ref:  §5.3 acyclicity (prior-yr IRR only)
    Principle:         2 (per-unit marginal IRR drives allocation weights)

    """
    cl = module_outputs.get("customer_launch", AllocatorOut.zeros())
    sl = module_outputs.get("starlink", AllocatorOut.zeros())
    ai = module_outputs.get("ai_compute")
    if ai is None:
        odc = module_outputs.get("odc", AllocatorOut.zeros())
        ai_stack = module_outputs.get("ai_stack", AllocatorOut.zeros())
        ai_irr = np.maximum(odc.spot_irr.values, ai_stack.spot_irr.values)
    else:
        ai_irr = ai.spot_irr.values

    return ModuleSpotIrrs(
        starlink=YearVector(_prior_year(sl.spot_irr.values)),
        customer_launch=YearVector(_prior_year(cl.spot_irr.values)),
        ai_compute=YearVector(_prior_year(ai_irr)),
    )


def _terrestrial_spot_irr(assumptions: Assumptions) -> YearVector:
    """Predetermined terrestrial marginal IRR proxy (cash-only program).

    Excel cell:        Cash Allocation Engine!D78
    Excel label:       "Spot IRR: Terrestrial (prior yr)"
    Architecture ref:  U2 four first-class programs
    Principle:         2 (predetermined prior-yr signal; no this-year deployment)

    """
    margin = assumption_year_vector(assumptions, cl.MARGIN_PER_MW_PER_YR_MM, default=0.0).values
    slug = assumption_scalar(assumptions, cl.CAPEX_SLUG_PER_MW_MM, default=20.0)
    if slug <= 0.0:
        return YearVector.zeros()
    return YearVector(np.clip(margin / slug, -1.0, 2.0))


def compute_four_program_prior_irrs(
    module_outputs: dict[str, AllocatorOut],
    assumptions: Assumptions,
    *,
    facilities_build: FacilitiesBuildResult | None = None,
    chip_at_cost_per_sat: YearVector | None = None,
) -> FourProgramIrrs:
    """Prior-year spot IRR for {Starlink, ODC, Terr, CL} — retires AI roll-up + Level-2.

    Excel cell:        Cash Allocation Engine!D28:D30 + D77:D78
    Excel label:       "Spot IRR: Starlink" … "Spot IRR: Terrestrial (prior yr)"
    Architecture ref:  PRD U2 four first-class programs
    Principle:         2 (acyclicity firewall — prior-yr IRR only)

    """
    cl_out = module_outputs.get("customer_launch", AllocatorOut.zeros())
    sl_out = module_outputs.get("starlink", AllocatorOut.zeros())
    ai = module_outputs.get("ai_compute")

    if ai is not None and np.any(ai.spot_irr.values != 0.0):
        odc_irr = ai.spot_irr.values
    else:
        chip = chip_at_cost_per_sat or compute_chip_at_cost_per_sat(assumptions, facilities_build)
        odc_scalar = per_sat_blended_irr(
            OrbitalDcInputs(assumptions=assumptions, chip_at_cost_per_sat=chip)
        )
        odc_irr = np.full(HORIZON_YEARS, max(odc_scalar, -1.0), dtype=np.float64)

    terr_irr = _terrestrial_spot_irr(assumptions).values

    return FourProgramIrrs(
        starlink=YearVector(_prior_year(sl_out.spot_irr.values)),
        odc=YearVector(_prior_year(odc_irr)),
        terrestrial=YearVector(_prior_year(terr_irr)),
        customer_launch=YearVector(_prior_year(cl_out.spot_irr.values)),
    )


def roll_up_module_irrs(
    module_outputs: dict[str, AllocatorOut],
    *,
    starlink_vehicle_irrs: QueueSubBlockIrrs | None = None,
) -> QueueSubBlockIrrs:
    """Roll up blended IRR year-vectors for cash sigmoid queue sub-blocks.

    Excel cell:        Allocator!D153:AC153
    Excel label:       "Customer Launch Blended IRR"
    Architecture ref:  §6 central IRR display
    Principle:         2 (per-unit marginal IRR drives sigmoid weights)

    Uses per-vehicle Starlink IRRs when provided; otherwise falls back to module-level.

    """
    cl = module_outputs.get("customer_launch", AllocatorOut.zeros())
    sl = module_outputs.get("starlink", AllocatorOut.zeros())
    ai_compute = module_outputs.get("ai_compute")
    if ai_compute is not None:
        odc = ai_compute
        ai = AllocatorOut.zeros()
    else:
        odc = module_outputs.get("odc", AllocatorOut.zeros())
        ai = module_outputs.get("ai_stack", AllocatorOut.zeros())

    if starlink_vehicle_irrs is not None:
        sl_v2_bb = starlink_vehicle_irrs.starlink_v2_bb
        sl_v2_dtc = starlink_vehicle_irrs.starlink_v2_dtc
        sl_v3_bb = starlink_vehicle_irrs.starlink_v3_bb
        sl_v3_dtc = starlink_vehicle_irrs.starlink_v3_dtc
    else:
        sl_blended = sl.blended_irr
        sl_v2_bb = sl_blended
        sl_v2_dtc = sl_blended
        sl_v3_bb = sl_blended
        sl_v3_dtc = sl_blended

    return QueueSubBlockIrrs(
        customer_launch=cl.blended_irr,
        starlink_v2_bb=sl_v2_bb,
        starlink_v2_dtc=sl_v2_dtc,
        starlink_v3_bb=sl_v3_bb,
        starlink_v3_dtc=sl_v3_dtc,
        odc=odc.blended_irr,
        ai_stack=ai.blended_irr,
    )
