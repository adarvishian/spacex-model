"""Starlink P&L module."""

from spacex_model.calc.starlink.module import compute_allocator_out
from spacex_model.calc.starlink.per_vehicle_irr import (
    build_starlink_vehicle_irrs,
    compute_v2_bb_irr,
    compute_v2_dtc_irr,
    compute_v3_bb_irr,
    compute_v3_dtc_irr,
)

__all__ = [
    "compute_allocator_out",
    "build_starlink_vehicle_irrs",
    "compute_v2_bb_irr",
    "compute_v2_dtc_irr",
    "compute_v3_bb_irr",
    "compute_v3_dtc_irr",
]
