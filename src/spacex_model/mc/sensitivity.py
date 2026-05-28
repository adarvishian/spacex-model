"""MC sensitivity — tornado, PRCC, 1D sweeps, 2D table per PRD §8.5."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy import stats

from spacex_model.config.constants import FIRST_YEAR
from spacex_model.engine.iterative_solver import NonConvergenceError
from spacex_model.engine.pipeline import run_pipeline
from spacex_model.inputs.assumptions import Assumptions
from spacex_model.inputs.demand_curves import DemandCurves
from spacex_model.inputs.mc_ranges import DistributionType
from spacex_model.inputs.scenarios import apply_assumption_overrides
from spacex_model.io.excel_ingest import IngestResult
from spacex_model.mc.distributions import distribution_std
from spacex_model.mc.results import extract_trial_metrics
from spacex_model.mc.sampler import TrialSamples, list_variable_labels, samples_to_input_matrix


@dataclass(frozen=True, slots=True)
class TornadoBar:
    """One tornado chart bar — ±1σ perturbation on a single input."""

    label: str
    low_ev: float
    high_ev: float
    base_ev: float
    delta: float


@dataclass(frozen=True, slots=True)
class PrccEntry:
    """Partial rank correlation coefficient for one input."""

    label: str
    prcc: float
    p_value: float


def _run_ev(
    assumptions: Assumptions,
    *,
    ingest: IngestResult,
    demand: DemandCurves,
    overrides: dict[str, Any] | None = None,
) -> float:
    if overrides:
        assumptions = apply_assumption_overrides(assumptions, overrides)
    try:
        result = run_pipeline(
            assumptions=assumptions,
            ingest=ingest,
            demand_curves=demand,
            write_outputs=False,
        )
        return float(extract_trial_metrics(result)["group_ev_2025_b"])
    except NonConvergenceError:
        return float("nan")


def _ev_delta(base_ev: float, perturbed_ev: float) -> float:
    if not np.isfinite(perturbed_ev):
        return 0.0
    return abs(perturbed_ev - base_ev)


def tornado_sensitivity(
    assumptions: Assumptions,
    *,
    ingest: IngestResult,
    demand: DemandCurves,
    labels: list[str] | None = None,
    top_n: int = 10,
) -> list[TornadoBar]:
    """Deterministic ±1σ perturbations ranked by |Δ Group EV|."""
    base_ev = _run_ev(assumptions, ingest=ingest, demand=demand)
    target_labels = labels or list_variable_labels(assumptions)
    bars: list[TornadoBar] = []

    for label in target_labels:
        meta = assumptions.mc_ranges.by_label.get(label)
        row = assumptions.by_label.get(label)
        if meta is None or row is None or not meta.distribution:
            continue
        if meta.distribution in (DistributionType.FIXED, DistributionType.FIXED_YEARROW):
            continue
        base = row.scalar() or 0.0
        sigma = distribution_std(
            meta.distribution,
            base=base,
            low=meta.mc_min,
            high=meta.mc_max,
        )
        if sigma <= 0:
            continue
        low_ev = _run_ev(
            assumptions,
            ingest=ingest,
            demand=demand,
            overrides={label: base - sigma},
        )
        high_ev = _run_ev(
            assumptions,
            ingest=ingest,
            demand=demand,
            overrides={label: base + sigma},
        )
        if not np.isfinite(low_ev) and not np.isfinite(high_ev):
            continue
        delta = max(_ev_delta(base_ev, low_ev), _ev_delta(base_ev, high_ev))
        bars.append(
            TornadoBar(
                label=label,
                low_ev=low_ev,
                high_ev=high_ev,
                base_ev=base_ev,
                delta=delta,
            )
        )

    bars.sort(key=lambda b: b.delta, reverse=True)
    return bars[:top_n]


def prcc_sensitivity(
    trials: list[TrialSamples],
    output_values: np.ndarray,
    *,
    labels: list[str] | None = None,
) -> list[PrccEntry]:
    """Partial rank correlation between inputs and Group EV."""
    clean_mask = np.isfinite(output_values)
    y = output_values[clean_mask]
    if y.size < 3:
        return []

    label_list = labels or []
    if not label_list and trials:
        keys: set[str] = set()
        for t in trials:
            keys.update(t.overrides)
        label_list = sorted(keys)

    x = samples_to_input_matrix(trials, label_list)[clean_mask]
    y_rank = stats.rankdata(y)
    entries: list[PrccEntry] = []

    for j, label in enumerate(label_list):
        col = x[:, j]
        if np.std(col) < 1e-12:
            continue
        x_rank = stats.rankdata(col)
        r, p = stats.pearsonr(x_rank, y_rank)
        entries.append(PrccEntry(label=label, prcc=float(r), p_value=float(p)))

    entries.sort(key=lambda e: abs(e.prcc), reverse=True)
    return entries


def sweep_1d(
    assumptions: Assumptions,
    *,
    ingest: IngestResult,
    demand: DemandCurves,
    label: str,
    grid: list[float] | None = None,
    n_points: int = 11,
) -> list[dict[str, float]]:
    """Deterministic 1D sweep on one Assumptions input."""
    meta = assumptions.mc_ranges.by_label.get(label)
    row = assumptions.by_label.get(label)
    if row is None:
        msg = f"Unknown label: {label!r}"
        raise KeyError(msg)
    base = row.scalar() or 0.0
    lo = float(meta.mc_min) if meta and meta.mc_min is not None else base * 0.8
    hi = float(meta.mc_max) if meta and meta.mc_max is not None else base * 1.2
    points = grid if grid is not None else list(np.linspace(lo, hi, n_points))
    out: list[dict[str, float]] = []
    for val in points:
        ev = _run_ev(assumptions, ingest=ingest, demand=demand, overrides={label: float(val)})
        out.append({"value": float(val), "group_ev_2025_b": ev})
    return out


def sweep_2d_table(
    assumptions: Assumptions,
    *,
    ingest: IngestResult,
    demand: DemandCurves,
    row_label: str,
    col_label: str,
    grid_size: int = 5,
) -> dict[str, Any]:
    """5×5 (or grid_size²) sensitivity table — Architecture §14.5."""
    row_meta = assumptions.mc_ranges.by_label.get(row_label)
    col_meta = assumptions.mc_ranges.by_label.get(col_label)
    row_inp = assumptions.by_label.get(row_label)
    col_inp = assumptions.by_label.get(col_label)
    if row_inp is None or col_inp is None:
        msg = "2D sweep requires valid Assumptions labels"
        raise KeyError(msg)

    r_base = row_inp.scalar() or 0.0
    c_base = col_inp.scalar() or 0.0
    r_lo = float(row_meta.mc_min) if row_meta and row_meta.mc_min is not None else r_base * 0.8
    r_hi = float(row_meta.mc_max) if row_meta and row_meta.mc_max is not None else r_base * 1.2
    c_lo = float(col_meta.mc_min) if col_meta and col_meta.mc_min is not None else c_base * 0.8
    c_hi = float(col_meta.mc_max) if col_meta and col_meta.mc_max is not None else c_base * 1.2

    row_grid = np.linspace(r_lo, r_hi, grid_size)
    col_grid = np.linspace(c_lo, c_hi, grid_size)
    matrix = np.zeros((grid_size, grid_size), dtype=np.float64)

    for i, rv in enumerate(row_grid):
        for j, cv in enumerate(col_grid):
            matrix[i, j] = _run_ev(
                assumptions,
                ingest=ingest,
                demand=demand,
                overrides={row_label: float(rv), col_label: float(cv)},
            )

    return {
        "row_label": row_label,
        "col_label": col_label,
        "row_values": row_grid.tolist(),
        "col_values": col_grid.tolist(),
        "group_ev_2025_b": matrix.tolist(),
        "base_case": {
            row_label: r_base,
            col_label: c_base,
            "group_ev_2025_b": _run_ev(assumptions, ingest=ingest, demand=demand),
        },
    }


# Default 2D axes per PRD §8.5 / Architecture §14.5
DEFAULT_2D_ROW = "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)"
DEFAULT_2D_COL = "TAM inflation rate (annual)"
