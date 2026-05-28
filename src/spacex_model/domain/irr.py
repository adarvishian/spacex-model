"""Per-unit marginal IRR engine per Architecture §5 / PRD §2.6."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from spacex_model.domain.units import IrrDecimal

IRR_CUTOFF = -1.0
_IRR_GUESSES = (-0.9, -0.5, -0.1, 0.0, 0.05, 0.1, 0.15, 0.25, 0.5, 1.0, 2.0)


@dataclass(frozen=True, slots=True)
class IrrResult:
    spot: IrrDecimal
    forward: IrrDecimal
    blended: IrrDecimal


def _npv(rate: float, cashflows: np.ndarray) -> float:
    periods = np.arange(len(cashflows), dtype=np.float64)
    return float(np.sum(cashflows / np.power(1.0 + rate, periods)))


def _irr_newton(cashflows: np.ndarray, guess: float, *, tol: float = 1e-7, max_iter: int = 50) -> float | None:
    rate = guess
    for _ in range(max_iter):
        periods = np.arange(len(cashflows), dtype=np.float64)
        denom = np.power(1.0 + rate, periods)
        npv = np.sum(cashflows / denom)
        d_npv = np.sum(-periods * cashflows / (denom * (1.0 + rate)))
        if abs(d_npv) < 1e-15:
            return None
        step = npv / d_npv
        rate -= step
        if abs(npv) < tol:
            return rate
        if rate <= -0.9999:
            rate = -0.9999
    return rate if abs(_npv(rate, cashflows)) < tol * 10 else None


def _solve_irr(cashflows: np.ndarray) -> float:
    """Multi-start Newton IRR; Excel cutoff convention for degenerate streams."""
    if len(cashflows) < 2:
        return IRR_CUTOFF
    if np.all(cashflows <= 0):
        return IRR_CUTOFF
    if np.all(cashflows >= 0):
        return 0.0
    best: float | None = None
    best_npv = float("inf")
    for guess in _IRR_GUESSES:
        root = _irr_newton(cashflows, guess)
        if root is None:
            continue
        npv_abs = abs(_npv(root, cashflows))
        if npv_abs < best_npv:
            best_npv = npv_abs
            best = root
    return best if best is not None else IRR_CUTOFF


def compute_irr_engine(
    cost_per_unit: float,
    net_marginal_revenue: np.ndarray,
    forward_weight: float = 0.7,
    horizon_n: int = 5,
) -> IrrResult:
    """Per-unit marginal IRR: CF = [−cost, rev(T+1)…rev(T+N)]; blended = 0.3×Spot + 0.7×Forward.

    Excel cell:        (module-specific)
    Excel label:       Spot IRR / Forward IRR / Blended IRR
    Architecture ref:  §5
    Principle:         2 (per-unit marginal IRR)

    """
    n = min(horizon_n, len(net_marginal_revenue))
    rev = net_marginal_revenue[:n]

    spot_cf = np.concatenate(([-cost_per_unit], rev))
    spot = _solve_irr(spot_cf)

    forward_cf = np.concatenate(([-cost_per_unit], np.zeros(2), rev[: max(0, n - 2)]))
    if len(forward_cf) < 2:
        forward_cf = np.array([-cost_per_unit, rev[0] if n else 0.0])
    forward = _solve_irr(forward_cf)

    spot_w = 1.0 - forward_weight
    blended = spot_w * spot + forward_weight * forward
    return IrrResult(spot=spot, forward=forward, blended=blended)
