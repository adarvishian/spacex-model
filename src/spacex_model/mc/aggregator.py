"""MC output aggregation — percentiles, CVaR, convergence diagnostics per PRD §8.4."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pyarrow as pa

from spacex_model.mc.results import TRIAL_METRIC_KEYS

PERCENTILE_LEVELS = (5, 10, 25, 50, 75, 90, 95)


@dataclass
class MetricSummary:
    """Percentile bands and tail metrics for one output."""

    metric: str
    p5: float
    p10: float
    p25: float
    p50: float
    p75: float
    p90: float
    p95: float
    mean: float
    std: float
    cvar_5: float
    base_case: float | None = None

    def to_dict(self) -> dict[str, float | str | None]:
        return {
            "metric": self.metric,
            "p5": self.p5,
            "p10": self.p10,
            "p25": self.p25,
            "p50": self.p50,
            "p75": self.p75,
            "p90": self.p90,
            "p95": self.p95,
            "mean": self.mean,
            "std": self.std,
            "cvar_5": self.cvar_5,
            "base_case": self.base_case,
        }


@dataclass
class McAggregation:
    """Full MC aggregation package."""

    n_trials: int
    n_converged: int
    metrics: dict[str, MetricSummary] = field(default_factory=dict)
    convergence_trace: dict[str, list[float]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_trials": self.n_trials,
            "n_converged": self.n_converged,
            "metrics": {k: v.to_dict() for k, v in self.metrics.items()},
            "convergence_trace": self.convergence_trace,
        }


def _cvar_5(values: np.ndarray) -> float:
    """Conditional VaR at 5% — mean of lowest 5% tail."""
    if values.size == 0:
        return float("nan")
    cutoff = np.percentile(values, 5)
    tail = values[values <= cutoff]
    return float(np.mean(tail)) if tail.size else float(cutoff)


def summarize_metric(values: np.ndarray, *, metric: str, base_case: float | None = None) -> MetricSummary:
    clean = values[np.isfinite(values)]
    if clean.size == 0:
        nan = float("nan")
        return MetricSummary(
            metric=metric,
            p5=nan,
            p10=nan,
            p25=nan,
            p50=nan,
            p75=nan,
            p90=nan,
            p95=nan,
            mean=nan,
            std=nan,
            cvar_5=nan,
            base_case=base_case,
        )
    pct = np.percentile(clean, PERCENTILE_LEVELS)
    return MetricSummary(
        metric=metric,
        p5=float(pct[0]),
        p10=float(pct[1]),
        p25=float(pct[2]),
        p50=float(pct[3]),
        p75=float(pct[4]),
        p90=float(pct[5]),
        p95=float(pct[6]),
        mean=float(np.mean(clean)),
        std=float(np.std(clean)),
        cvar_5=_cvar_5(clean),
        base_case=base_case,
    )


def max_drawdown_vs_base(values: np.ndarray, base: float) -> float:
    """Largest negative deviation from Base Case across trials."""
    clean = values[np.isfinite(values)]
    if clean.size == 0 or not np.isfinite(base):
        return float("nan")
    return float(np.min(clean) - base)


def convergence_diagnostics(values: np.ndarray, checkpoints: tuple[int, ...] = (100, 500, 1000, 5000)) -> dict[str, list[float]]:
    """Running mean and std at trial checkpoints."""
    clean = values[np.isfinite(values)]
    trace: dict[str, list[float]] = {"trial_counts": [], "running_mean": [], "running_std": []}
    for n in checkpoints:
        if n > clean.size:
            continue
        subset = clean[:n]
        trace["trial_counts"].append(float(n))
        trace["running_mean"].append(float(np.mean(subset)))
        trace["running_std"].append(float(np.std(subset)))
    return trace


def _converged_mask(table: pa.Table) -> np.ndarray | None:
    if "converged" not in table.column_names:
        return None
    col = table.column("converged").to_numpy(zero_copy_only=False)
    return np.array([bool(x) for x in col], dtype=bool)


def aggregate_trials(
    table: pa.Table,
    *,
    base_metrics: dict[str, float] | None = None,
) -> McAggregation:
    """Aggregate parquet trial table into percentile bands."""
    mask = _converged_mask(table)
    n_converged = int(np.sum(mask)) if mask is not None else table.num_rows
    metrics: dict[str, MetricSummary] = {}
    conv_trace: dict[str, list[float]] = {}

    for key in TRIAL_METRIC_KEYS:
        if key in ("converged", "solver_iterations"):
            continue
        if key not in table.column_names:
            continue
        arr = np.asarray(table.column(key).to_numpy(zero_copy_only=False), dtype=np.float64)
        if mask is not None:
            arr = arr[mask]
        base = base_metrics.get(key) if base_metrics else None
        metrics[key] = summarize_metric(arr, metric=key, base_case=base)
        if key == "group_ev_2025_b":
            conv_trace = convergence_diagnostics(arr)

    return McAggregation(
        n_trials=int(table.num_rows),
        n_converged=n_converged,
        metrics=metrics,
        convergence_trace=conv_trace,
    )
