"""MC output aggregation — percentiles, CVaR, convergence diagnostics per PRD §8.4."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
import pyarrow as pa

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.mc.results import (
    FCF_FAN_PERCENTILES,
    GROUP_EV_HISTOGRAM_BINS,
    TRIAL_METRIC_KEYS,
    group_fcf_year_keys,
)

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
class HistogramBins:
    """Histogram for a scalar MC output (Group EV)."""

    metric: str
    bin_edges: list[float]
    counts: list[int]
    n_bins: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric": self.metric,
            "bin_edges": self.bin_edges,
            "counts": self.counts,
            "n_bins": self.n_bins,
        }


@dataclass
class GroupFcfFan:
    """Percentile bands for Group FCF by forecast year."""

    years: list[int]
    p5: list[float]
    p25: list[float]
    p50: list[float]
    p75: list[float]
    p95: list[float]
    base_case: list[float | None]

    def to_dict(self) -> dict[str, Any]:
        return {
            "years": self.years,
            "p5": self.p5,
            "p25": self.p25,
            "p50": self.p50,
            "p75": self.p75,
            "p95": self.p95,
            "base_case": self.base_case,
        }


@dataclass
class McAggregation:
    """Full MC aggregation package."""

    n_trials: int
    n_converged: int
    base_seed: int = 42
    convergence_status: str = "unknown"
    metrics: dict[str, MetricSummary] = field(default_factory=dict)
    convergence_trace: dict[str, list[float]] = field(default_factory=dict)
    group_ev_histogram: HistogramBins | None = None
    group_fcf_fan: GroupFcfFan | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "n_trials": self.n_trials,
            "n_converged": self.n_converged,
            "base_seed": self.base_seed,
            "convergence_status": self.convergence_status,
            "metrics": {k: v.to_dict() for k, v in self.metrics.items()},
            "convergence_trace": self.convergence_trace,
        }
        if self.group_ev_histogram is not None:
            out["group_ev_histogram"] = self.group_ev_histogram.to_dict()
        if self.group_fcf_fan is not None:
            out["group_fcf_fan"] = self.group_fcf_fan.to_dict()
        return out


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


def _convergence_status(n_trials: int, n_converged: int) -> str:
    if n_trials <= 0:
        return "empty"
    if n_converged == n_trials:
        return "converged"
    if n_converged == 0:
        return "failed"
    return "partial"


def build_group_ev_histogram(
    values: np.ndarray,
    *,
    metric: str = "group_ev_2025_b",
    n_bins: int = GROUP_EV_HISTOGRAM_BINS,
) -> HistogramBins | None:
    """Histogram bins for Group EV distribution (no engine recompute)."""
    clean = values[np.isfinite(values)]
    if clean.size == 0:
        return None
    if float(np.ptp(clean)) < 1e-9:
        center = float(np.mean(clean))
        return HistogramBins(
            metric=metric,
            bin_edges=[center - 0.5, center + 0.5],
            counts=[int(clean.size)],
            n_bins=1,
        )
    effective_bins = min(n_bins, max(1, len(np.unique(clean)) // 2))
    counts, edges = np.histogram(clean, bins=effective_bins)
    return HistogramBins(
        metric=metric,
        bin_edges=[float(x) for x in edges],
        counts=[int(x) for x in counts],
        n_bins=n_bins,
    )


def build_group_fcf_fan(
    table: pa.Table,
    *,
    mask: np.ndarray | None = None,
    base_metrics: dict[str, float] | None = None,
) -> GroupFcfFan | None:
    """Percentile-by-year fan for Group FCF from existing trial columns."""
    years = list(range(FIRST_YEAR, LAST_YEAR + 1))
    keys = group_fcf_year_keys()
    if not any(key in table.column_names for key in keys):
        return None

    fan_pct: dict[str, list[float]] = {f"p{p}": [] for p in FCF_FAN_PERCENTILES}
    base_case: list[float | None] = []

    for year, key in zip(years, keys, strict=True):
        if key not in table.column_names:
            for pct_key in fan_pct:
                fan_pct[pct_key].append(float("nan"))
            base_case.append(base_metrics.get(key) if base_metrics else None)
            continue
        arr = np.asarray(table.column(key).to_numpy(zero_copy_only=False), dtype=np.float64)
        if mask is not None:
            arr = arr[mask]
        clean = arr[np.isfinite(arr)]
        if clean.size == 0:
            for pct_key in fan_pct:
                fan_pct[pct_key].append(float("nan"))
        else:
            pct = np.percentile(clean, FCF_FAN_PERCENTILES)
            for idx, p in enumerate(FCF_FAN_PERCENTILES):
                fan_pct[f"p{p}"].append(float(pct[idx]))
        base_case.append(base_metrics.get(key) if base_metrics else None)

    return GroupFcfFan(
        years=years,
        p5=fan_pct["p5"],
        p25=fan_pct["p25"],
        p50=fan_pct["p50"],
        p75=fan_pct["p75"],
        p95=fan_pct["p95"],
        base_case=base_case,
    )


MONITORED_ADAPTIVE_METRICS = ("group_ev_2025_b",)


def _relative_change(a: float, b: float) -> float:
    """Relative change between two values; 0 if both near zero."""
    if not np.isfinite(a) or not np.isfinite(b):
        return float("inf")
    denom = max(abs(a), abs(b), 1e-12)
    return abs(a - b) / denom


def running_adaptive_diagnostics(
    ev_values: np.ndarray,
    *,
    checkpoint_size: int,
    eps: float = 0.0025,
    consecutive: int = 2,
    min_trials: int = 512,
) -> dict[str, Any]:
    """Checkpoint percentile trace and stopping recommendation for adaptive MC."""
    clean = ev_values[np.isfinite(ev_values)]
    n = int(clean.size)
    trace: list[dict[str, float]] = []
    stable_streak = 0
    stop_at: int | None = None

    if n < min_trials or checkpoint_size <= 0:
        return {
            "checkpoints": trace,
            "stable_streak": 0,
            "stop_at": None,
            "should_stop": False,
        }

    prev_p5: float | None = None
    prev_p50: float | None = None
    prev_std: float | None = None
    for end in range(checkpoint_size, n + 1, checkpoint_size):
        subset = clean[:end]
        p5 = float(np.percentile(subset, 5))
        p50 = float(np.percentile(subset, 50))
        std = float(np.std(subset))
        entry = {
            "trials": float(end),
            "p5": p5,
            "p50": p50,
            "std": std,
        }
        trace.append(entry)

        if prev_p5 is not None and prev_p50 is not None and prev_std is not None:
            stable = (
                _relative_change(p5, prev_p5) < eps
                and _relative_change(p50, prev_p50) < eps
                and _relative_change(std, prev_std) < eps
            )
            stable_streak = stable_streak + 1 if stable else 0
            if stable_streak >= consecutive and end >= min_trials and stop_at is None:
                stop_at = end
        prev_p5, prev_p50, prev_std = p5, p50, std

    return {
        "checkpoints": trace,
        "stable_streak": stable_streak,
        "stop_at": stop_at,
        "should_stop": stop_at is not None,
    }


def compare_aggregations(
    candidate: McAggregation,
    baseline: McAggregation,
    *,
    rel_tol: float = 0.005,
    abs_tol_mm: float = 1.0,
) -> list[str]:
    """Return list of metric/percentile failures vs baseline (§3.2 harness)."""
    failures: list[str] = []
    pct_keys = ("p5", "p25", "p50", "p75", "p95")

    for key, base_summary in baseline.metrics.items():
        cand_summary = candidate.metrics.get(key)
        if cand_summary is None:
            failures.append(f"missing metric {key}")
            continue
        for pct in pct_keys:
            base_val = getattr(base_summary, pct)
            cand_val = getattr(cand_summary, pct)
            if not np.isfinite(base_val) and not np.isfinite(cand_val):
                continue
            if not np.isfinite(cand_val):
                failures.append(f"{key}.{pct}: candidate non-finite")
                continue
            rel = _relative_change(cand_val, base_val)
            abs_diff = abs(cand_val - base_val)
            tol = rel_tol
            if abs(base_val) < 10.0 and "_fcf_" in key:
                tol = max(rel_tol, abs_tol_mm / max(abs(base_val), abs_tol_mm))
            if rel > tol and abs_diff > abs_tol_mm:
                failures.append(f"{key}.{pct}: {cand_val} vs {base_val} (rel={rel:.4f})")

        for stat in ("mean",):
            base_val = getattr(base_summary, stat)
            cand_val = getattr(cand_summary, stat)
            if np.isfinite(base_val) and np.isfinite(cand_val):
                if _relative_change(cand_val, base_val) > rel_tol:
                    failures.append(f"{key}.{stat}: {cand_val} vs {base_val}")
        if key == "group_ev_2025_b":
            base_val = base_summary.cvar_5
            cand_val = cand_summary.cvar_5
            if np.isfinite(base_val) and np.isfinite(cand_val):
                if _relative_change(cand_val, base_val) > rel_tol:
                    failures.append(f"{key}.cvar_5: {cand_val} vs {base_val}")

    return failures


def aggregate_trials(
    table: pa.Table,
    *,
    base_metrics: dict[str, float] | None = None,
    base_seed: int = 42,
) -> McAggregation:
    """Aggregate parquet trial table into percentile bands."""
    mask = _converged_mask(table)
    n_converged = int(np.sum(mask)) if mask is not None else table.num_rows
    n_trials = int(table.num_rows)
    metrics: dict[str, MetricSummary] = {}
    conv_trace: dict[str, list[float]] = {}
    ev_histogram: HistogramBins | None = None

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
            ev_histogram = build_group_ev_histogram(arr, metric=key)

    fcf_fan = build_group_fcf_fan(table, mask=mask, base_metrics=base_metrics)

    return McAggregation(
        n_trials=n_trials,
        n_converged=n_converged,
        base_seed=base_seed,
        convergence_status=_convergence_status(n_trials, n_converged),
        metrics=metrics,
        convergence_trace=conv_trace,
        group_ev_histogram=ev_histogram,
        group_fcf_fan=fcf_fan,
    )
