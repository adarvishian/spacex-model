"""Demand Curves piecewise-linear evaluator — BB + DTC breakpoints from workbook."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.config.constants import HORIZON_YEARS


def piecewise_linear_lookup(
    quantity: float,
    breakpoints_q: np.ndarray,
    breakpoints_rev: np.ndarray,
    *,
    clip_below_zero: bool = False,
    scale_to_mm: float = 1.0,
) -> float:
    """Piecewise-linear interpolation with saturation at table min/max.

    Excel cell:        Demand Curves!— (evaluator)
    Excel label:       "Starlink BB/DTC Revenue from curve ($mm)"
    Architecture ref:  §8.4 / Sprint 10.5
    Principle:         3 (canonical Demand Curves tab)

    """
    if quantity <= 0:
        return 0.0
    q = np.asarray(breakpoints_q, dtype=np.float64)
    r = np.asarray(breakpoints_rev, dtype=np.float64)
    if q.size == 0:
        return 0.0
    if quantity <= q[0]:
        if clip_below_zero:
            return 0.0
        if q[0] <= 0:
            return float(r[0]) / scale_to_mm
        return float(r[0] * (quantity / q[0])) / scale_to_mm
    if quantity >= q[-1]:
        return float(r[-1]) / scale_to_mm
    idx = int(np.searchsorted(q, quantity, side="right"))
    q0, q1 = q[idx - 1], q[idx]
    r0, r1 = r[idx - 1], r[idx]
    if q1 == q0:
        return float(r0) / scale_to_mm
    rev = r0 + (quantity - q0) * (r1 - r0) / (q1 - q0)
    return float(rev) / scale_to_mm


@dataclass(frozen=True, slots=True)
class DemandCurves:
    """BB + DTC breakpoint tables ingested from Demand Curves tab."""

    bb_breakpoints_q: np.ndarray
    bb_breakpoints_rev: np.ndarray
    dtc_breakpoints_q: np.ndarray
    dtc_breakpoints_rev: np.ndarray

    def lookup_bb_revenue(self, gbps: float, year_index: int, *, tam_shift: float = 1.0) -> float:
        """BB revenue ($mm) from Available BB Gbps × TAM shift.

        Excel cell:        Demand Curves!D144
        Excel label:       "Starlink BB Revenue from curve ($mm)"
        Architecture ref:  §8.4
        Principle:         3 (piecewise-linear Demand Curves)

        """
        _ = year_index
        base = piecewise_linear_lookup(
            gbps,
            self.bb_breakpoints_q,
            self.bb_breakpoints_rev,
            scale_to_mm=1_000_000.0,
        )
        return base * tam_shift

    def lookup_dtc_revenue(self, gbps: float, year_index: int, *, tam_shift: float = 1.0) -> float:
        """DTC revenue ($mm) from Available DTC Gbps × TAM shift.

        Excel cell:        Demand Curves!D145
        Excel label:       "Starlink DTC Revenue from curve ($mm)"
        Architecture ref:  §8.4
        Principle:         3 (piecewise-linear Demand Curves)

        """
        _ = year_index
        base = piecewise_linear_lookup(
            gbps,
            self.dtc_breakpoints_q,
            self.dtc_breakpoints_rev,
            clip_below_zero=False,
            scale_to_mm=1.0,
        )
        return base * tam_shift


def demand_curves_from_ingest(ingest: object) -> DemandCurves:
    """Build DemandCurves from excel ingest Demand Curves pass."""
    from spacex_model.io.excel_ingest import IngestResult

    if not isinstance(ingest, IngestResult) or ingest.demand_curves is None:
        return demand_curves_stub()
    dc = ingest.demand_curves
    if not dc.bb_breakpoints or not dc.dtc_breakpoints:
        return demand_curves_stub()
    return DemandCurves(
        bb_breakpoints_q=np.array([b.quantity_gbps for b in dc.bb_breakpoints]),
        bb_breakpoints_rev=np.array([b.revenue for b in dc.bb_breakpoints]),
        dtc_breakpoints_q=np.array([b.quantity_gbps for b in dc.dtc_breakpoints]),
        dtc_breakpoints_rev=np.array([b.revenue for b in dc.dtc_breakpoints]),
    )


def demand_curves_stub() -> DemandCurves:
    """Minimal two-point tables for pipeline smoke tests without workbook."""
    return DemandCurves(
        bb_breakpoints_q=np.array([100_000.0, 200_000.0]),
        bb_breakpoints_rev=np.array([2_936_307_032.0, 3_747_517_779.0]),
        dtc_breakpoints_q=np.array([280.2, 560.3]),
        dtc_breakpoints_rev=np.array([307.0, 613.0]),
    )
