"""Starlink Capacity — bandwidth aggregation and at-cost pool rates (PRD §4.3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector

if TYPE_CHECKING:
    from spacex_model.calc.starlink.vehicle_pools import VehiclePoolsResult


@dataclass(frozen=True, slots=True)
class OdcBandwidthClaim:
    """ODC internal bandwidth claim read from ODC module."""

    bb_gbps: YearVector
    dtc_gbps: YearVector


@dataclass(frozen=True, slots=True)
class StarlinkCapacityInputs:
    """Upstream inputs for Starlink Capacity tab."""

    pools: VehiclePoolsResult
    constellation_da_mm: YearVector
    ground_ops_mm: YearVector
    spectrum_amort_mm: YearVector
    odc_claim: OdcBandwidthClaim | None = None


@dataclass(frozen=True, slots=True)
class StarlinkCapacityResult:
    """Canonical Starlink Capacity outputs."""

    total_bb_gbps: YearVector
    total_dtc_gbps: YearVector
    available_bb_gbps: YearVector
    available_dtc_gbps: YearVector
    bb_pool_cost_basis_mm: YearVector
    dtc_pool_cost_basis_mm: YearVector
    bb_at_cost_rate_per_gbps: YearVector
    dtc_at_cost_rate_per_gbps: YearVector


def compute_starlink_capacity(inputs: StarlinkCapacityInputs) -> StarlinkCapacityResult:
    """Aggregate Gbps, subtract ODC claim, compute pool at-cost rates.

    Excel cell:        Starlink Capacity!D11:D50
    Excel label:       "BB pool at-cost rate ($/Gbps/yr)"
    Architecture ref:  §8.5 / §7.2
    Principle:         9 (fully-allocated internal transfer pricing)

    """
    pools = inputs.pools
    odc_bb = inputs.odc_claim.bb_gbps.values if inputs.odc_claim else np.zeros(HORIZON_YEARS)
    odc_dtc = inputs.odc_claim.dtc_gbps.values if inputs.odc_claim else np.zeros(HORIZON_YEARS)

    total_bb = pools.total_bb_gbps.values
    total_dtc = pools.total_dtc_gbps.values
    avail_bb = np.maximum(0.0, total_bb - odc_bb)
    avail_dtc = np.maximum(0.0, total_dtc - odc_dtc)

    bb_share = np.where(total_bb > 0, total_bb / np.maximum(total_bb, 1e-12), 0.0)
    dtc_share = np.where(total_dtc > 0, total_dtc / np.maximum(total_bb + total_dtc, 1e-12), 0.0)

    bb_pool_cost = (
        inputs.constellation_da_mm.values * bb_share
        + inputs.ground_ops_mm.values * bb_share
        + inputs.spectrum_amort_mm.values
    )
    dtc_pool_cost = inputs.constellation_da_mm.values * dtc_share + inputs.ground_ops_mm.values * (
        1.0 - bb_share
    )

    bb_rate = np.nan_to_num(
        np.where(total_bb > 0, bb_pool_cost * 1e6 / np.maximum(total_bb, 1e-12), 0.0)
    )
    dtc_rate = np.nan_to_num(
        np.where(total_dtc > 0, dtc_pool_cost * 1e6 / np.maximum(total_dtc, 1e-12), 0.0)
    )

    return StarlinkCapacityResult(
        total_bb_gbps=pools.total_bb_gbps,
        total_dtc_gbps=pools.total_dtc_gbps,
        available_bb_gbps=YearVector(avail_bb),
        available_dtc_gbps=YearVector(avail_dtc),
        bb_pool_cost_basis_mm=YearVector(bb_pool_cost),
        dtc_pool_cost_basis_mm=YearVector(dtc_pool_cost),
        bb_at_cost_rate_per_gbps=YearVector(bb_rate),
        dtc_at_cost_rate_per_gbps=YearVector(dtc_rate),
    )
