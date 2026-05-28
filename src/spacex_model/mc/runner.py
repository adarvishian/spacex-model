"""joblib-parallel MC runner with checkpointed parquet store — PRD §8.3."""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from joblib import Parallel, delayed

from spacex_model.config.settings import get_settings
from spacex_model.engine.iterative_solver import NonConvergenceError
from spacex_model.engine.pipeline import run_pipeline
from spacex_model.inputs.assumptions import Assumptions, assumptions_from_ingest
from spacex_model.inputs.demand_curves import DemandCurves, demand_curves_from_ingest
from spacex_model.io.excel_ingest import IngestResult, ingest_workbook
from spacex_model.mc.results import TRIAL_METRIC_KEYS, extract_trial_metrics, write_trials_parquet
from spacex_model.mc.sampler import TrialSamples, apply_trial_samples, sample_trial


@dataclass
class McRunConfig:
    """Monte Carlo run configuration."""

    trials: int = 10_000
    base_seed: int = 42
    n_jobs: int = -1
    checkpoint_interval: int = 1000
    scenario_name: str = "base_case"


@dataclass
class McRunResult:
    """Completed MC study artifacts."""

    run_id: str
    scenario: str
    trials_requested: int
    trials_completed: int
    trials_converged: int
    wall_clock_sec: float
    output_dir: Path
    trials_parquet: Path
    audit: dict[str, Any] = field(default_factory=dict)


def _run_single_trial(
    trial_idx: int,
    *,
    base_assumptions: Assumptions,
    demand_curves: DemandCurves,
    ingest: IngestResult,
    base_seed: int,
) -> dict[str, Any]:
    """Execute one MC trial (worker-safe)."""
    trial = sample_trial(base_assumptions, trial_idx=trial_idx, base_seed=base_seed)
    perturbed = apply_trial_samples(base_assumptions, trial)
    row: dict[str, Any] = {
        "trial_idx": trial_idx,
        "seed": trial.seed,
        "error": None,
    }
    try:
        result = run_pipeline(
            assumptions=perturbed,
            ingest=ingest,
            demand_curves=demand_curves,
            write_outputs=False,
        )
        row.update(extract_trial_metrics(result))
    except NonConvergenceError as exc:
        row["error"] = str(exc)
        row["converged"] = False
        row["solver_iterations"] = 0
        for key in TRIAL_METRIC_KEYS:
            if key not in row:
                row[key] = float("nan") if key != "converged" else False
    return row


def run_mc_trials(
    trial_indices: list[int],
    *,
    base_assumptions: Assumptions,
    demand_curves: DemandCurves,
    ingest: IngestResult,
    base_seed: int,
    n_jobs: int = 1,
) -> list[dict[str, Any]]:
    """Run a subset of MC trial indices (used for serverless batching)."""
    if not trial_indices:
        return []
    worker = delayed(_run_single_trial)
    return Parallel(n_jobs=n_jobs)(
        worker(
            idx,
            base_assumptions=base_assumptions,
            demand_curves=demand_curves,
            ingest=ingest,
            base_seed=base_seed,
        )
        for idx in trial_indices
    )


def run_mc(
    *,
    workbook_path: Path | None = None,
    config: McRunConfig | None = None,
    run_id: str | None = None,
) -> McRunResult:
    """Run full MC study with checkpointed parquet writes."""
    settings = get_settings()
    cfg = config or McRunConfig()
    path = workbook_path or settings.workbook_path
    if not path.exists():
        raise FileNotFoundError(f"Workbook not found: {path}")

    rid = run_id or str(uuid.uuid4())[:8]
    out_dir = settings.outputs_dir / "mc" / cfg.scenario_name / rid
    out_dir.mkdir(parents=True, exist_ok=True)

    t0 = time.perf_counter()
    ingest = ingest_workbook(path)
    base_assumptions = assumptions_from_ingest(ingest)
    demand = demand_curves_from_ingest(ingest)

    worker = delayed(_run_single_trial)
    batch_size = max(1, cfg.checkpoint_interval)
    all_rows: list[dict[str, Any]] = []

    for batch_start in range(0, cfg.trials, batch_size):
        batch_end = min(batch_start + batch_size, cfg.trials)
        indices = list(range(batch_start, batch_end))
        batch_rows = Parallel(n_jobs=cfg.n_jobs)(
            worker(
                idx,
                base_assumptions=base_assumptions,
                demand_curves=demand,
                ingest=ingest,
                base_seed=cfg.base_seed,
            )
            for idx in indices
        )
        all_rows.extend(batch_rows)
        ckpt = out_dir / f"checkpoint_{batch_end}.parquet"
        write_trials_parquet(all_rows, ckpt)

    trials_path = out_dir / "trials.parquet"
    write_trials_parquet(all_rows, trials_path)

    converged = sum(1 for r in all_rows if r.get("converged"))
    elapsed = time.perf_counter() - t0
    audit = {
        "run_id": rid,
        "phase": "F",
        "scenario": cfg.scenario_name,
        "trials": cfg.trials,
        "base_seed": cfg.base_seed,
        "trials_converged": converged,
        "non_convergence_rate": 1.0 - converged / max(len(all_rows), 1),
        "wall_clock_sec": round(elapsed, 3),
        "workbook": str(path),
    }
    (out_dir / "audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

    return McRunResult(
        run_id=rid,
        scenario=cfg.scenario_name,
        trials_requested=cfg.trials,
        trials_completed=len(all_rows),
        trials_converged=converged,
        wall_clock_sec=elapsed,
        output_dir=out_dir,
        trials_parquet=trials_path,
        audit=audit,
    )
