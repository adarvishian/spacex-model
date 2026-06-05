"""joblib-parallel MC runner with checkpointed parquet store — PRD §8.3."""

from __future__ import annotations

import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import numpy as np
from joblib import Parallel, delayed

from spacex_model.config.settings import get_settings
from spacex_model.engine.iterative_solver import NonConvergenceError
from spacex_model.engine.pipeline import (
    PipelineState,
    copy_pipeline_state,
    pipeline_state_from_result,
    run_pipeline,
    run_pipeline_mc,
)
from spacex_model.inputs.assumptions import Assumptions, assumptions_from_ingest
from spacex_model.inputs.demand_curves import DemandCurves, demand_curves_from_ingest
from spacex_model.io.excel_ingest import IngestResult, ingest_workbook
from spacex_model.mc.aggregator import running_adaptive_diagnostics
from spacex_model.mc.results import TRIAL_METRIC_KEYS, extract_trial_metrics, write_trials_parquet
from spacex_model.mc.sampler import apply_trial_samples, generate_sobol_unit_cube, list_variable_labels, sample_trial

logger = logging.getLogger(__name__)


@dataclass
class McRunConfig:
    """Monte Carlo run configuration."""

    trials: int = 10_000
    base_seed: int = 42
    n_jobs: int = -1
    checkpoint_interval: int = 1000
    scenario_name: str = "base_case"
    sampling: Literal["mc", "qmc"] = "mc"
    warm_start: bool = True
    mc_lite: bool = True
    adaptive: bool = False
    adaptive_min_trials: int = 512
    adaptive_max_trials: int = 2000
    adaptive_eps: float = 0.0025
    adaptive_consecutive: int = 2
    conservation_audit_every: int = 100


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


def _resolve_pipeline_runner(*, mc_lite: bool):
    return run_pipeline_mc if mc_lite else run_pipeline


def _run_single_trial(
    trial_idx: int,
    *,
    base_assumptions: Assumptions,
    demand_curves: DemandCurves,
    ingest: IngestResult,
    base_seed: int,
    cfg: McRunConfig,
    warm_start_state: PipelineState | None,
    qmc_point: Any = None,
) -> dict[str, Any]:
    """Execute one MC trial (worker-safe)."""
    trial = sample_trial(
        base_assumptions,
        trial_idx=trial_idx,
        base_seed=base_seed,
        sampling=cfg.sampling,
        qmc_point=qmc_point,
    )
    perturbed = apply_trial_samples(base_assumptions, trial)
    row: dict[str, Any] = {
        "trial_idx": trial_idx,
        "seed": trial.seed,
        "error": None,
        "cold_retry": False,
    }
    pipeline_fn = _resolve_pipeline_runner(mc_lite=cfg.mc_lite)

    attempts = (True, False) if cfg.warm_start and warm_start_state is not None else (False,)
    for attempt, use_warm in enumerate(attempts):
        if attempt > 0:
            row["cold_retry"] = True
        try:
            kwargs: dict[str, Any] = {
                "assumptions": perturbed,
                "ingest": ingest,
                "demand_curves": demand_curves,
            }
            if cfg.mc_lite:
                kwargs["initial_state"] = copy_pipeline_state(warm_start_state) if use_warm and warm_start_state else None
            else:
                kwargs["write_outputs"] = False
                kwargs["initial_state"] = copy_pipeline_state(warm_start_state) if use_warm and warm_start_state else None
            result = pipeline_fn(**kwargs)
            row.update(extract_trial_metrics(result))
            if row.get("cold_retry"):
                logger.warning("Trial %d required cold-start retry after warm-start failure", trial_idx)
            break
        except NonConvergenceError as exc:
            if attempt + 1 < len(attempts):
                continue
            row["error"] = str(exc)
            row["converged"] = False
            row["solver_iterations"] = 0
            for key in TRIAL_METRIC_KEYS:
                if key not in row:
                    row[key] = float("nan") if key != "converged" else False
    return row


def _conservation_audit_trial(
    trial_idx: int,
    *,
    base_assumptions: Assumptions,
    demand_curves: DemandCurves,
    ingest: IngestResult,
    base_seed: int,
    cfg: McRunConfig,
    warm_start_state: PipelineState | None,
    qmc_point: Any = None,
) -> None:
    """Run full pipeline with conservation halt on audit cadence trials."""
    trial = sample_trial(
        base_assumptions,
        trial_idx=trial_idx,
        base_seed=base_seed,
        sampling=cfg.sampling,
        qmc_point=qmc_point,
    )
    perturbed = apply_trial_samples(base_assumptions, trial)
    result = run_pipeline(
        assumptions=perturbed,
        ingest=ingest,
        demand_curves=demand_curves,
        write_outputs=False,
        initial_state=copy_pipeline_state(warm_start_state) if cfg.warm_start and warm_start_state else None,
    )
    if not result.conservation.all_ok:
        msg = f"Conservation audit failed at trial {trial_idx}"
        raise RuntimeError(msg)


def _build_qmc_cube(cfg: McRunConfig, assumptions: Assumptions) -> np.ndarray | None:
    if cfg.sampling != "qmc":
        return None
    labels = list_variable_labels(assumptions)
    n = cfg.adaptive_max_trials if cfg.adaptive else cfg.trials
    return generate_sobol_unit_cube(n, len(labels), base_seed=cfg.base_seed)


def _trial_qmc_point(qmc_cube: np.ndarray | None, trial_idx: int) -> Any:
    if qmc_cube is None:
        return None
    return qmc_cube[trial_idx]


def run_mc_trials(
    trial_indices: list[int],
    *,
    base_assumptions: Assumptions,
    demand_curves: DemandCurves,
    ingest: IngestResult,
    base_seed: int,
    n_jobs: int = 1,
    cfg: McRunConfig | None = None,
    warm_start_state: PipelineState | None = None,
) -> list[dict[str, Any]]:
    """Run a subset of MC trial indices (used for serverless batching)."""
    if not trial_indices:
        return []
    run_cfg = cfg or McRunConfig(base_seed=base_seed)
    worker = delayed(_run_single_trial)
    return Parallel(n_jobs=n_jobs)(
        worker(
            idx,
            base_assumptions=base_assumptions,
            demand_curves=demand_curves,
            ingest=ingest,
            base_seed=base_seed,
            cfg=run_cfg,
            warm_start_state=warm_start_state,
            qmc_point=None,
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

    qmc_cube = _build_qmc_cube(cfg, base_assumptions)
    warm_start_state: PipelineState | None = None
    if cfg.warm_start:
        base_kwargs: dict[str, Any] = {
            "assumptions": base_assumptions,
            "ingest": ingest,
            "demand_curves": demand,
        }
        if not cfg.mc_lite:
            base_kwargs["write_outputs"] = False
        base_solve = _resolve_pipeline_runner(mc_lite=cfg.mc_lite)(**base_kwargs)
        warm_start_state = copy_pipeline_state(pipeline_state_from_result(base_solve))

    worker = delayed(_run_single_trial)
    batch_size = max(1, cfg.checkpoint_interval)
    all_rows: list[dict[str, Any]] = []
    trials_target = cfg.adaptive_max_trials if cfg.adaptive else cfg.trials
    adaptive_trace: list[dict[str, Any]] = []
    stopped_early = False
    stop_at: int | None = None

    for batch_start in range(0, trials_target, batch_size):
        batch_end = min(batch_start + batch_size, trials_target)
        indices = list(range(batch_start, batch_end))

        for idx in indices:
            if cfg.conservation_audit_every > 0 and (idx == 0 or idx % cfg.conservation_audit_every == 0):
                _conservation_audit_trial(
                    idx,
                    base_assumptions=base_assumptions,
                    demand_curves=demand,
                    ingest=ingest,
                    base_seed=cfg.base_seed,
                    cfg=cfg,
                    warm_start_state=warm_start_state,
                    qmc_point=_trial_qmc_point(qmc_cube, idx),
                )

        batch_rows = Parallel(n_jobs=cfg.n_jobs)(
            worker(
                idx,
                base_assumptions=base_assumptions,
                demand_curves=demand,
                ingest=ingest,
                base_seed=cfg.base_seed,
                cfg=cfg,
                warm_start_state=warm_start_state,
                qmc_point=_trial_qmc_point(qmc_cube, idx),
            )
            for idx in indices
        )
        all_rows.extend(batch_rows)
        ckpt = out_dir / f"checkpoint_{batch_end}.parquet"
        write_trials_parquet(all_rows, ckpt)

        if cfg.adaptive and len(all_rows) >= cfg.adaptive_min_trials:
            ev = np.asarray([r.get("group_ev_2025_b", float("nan")) for r in all_rows], dtype=np.float64)
            diag = running_adaptive_diagnostics(
                ev,
                checkpoint_size=batch_size,
                eps=cfg.adaptive_eps,
                consecutive=cfg.adaptive_consecutive,
                min_trials=cfg.adaptive_min_trials,
            )
            adaptive_trace.append(diag)
            if diag["should_stop"] and len(all_rows) >= cfg.adaptive_min_trials:
                stop_at = int(diag["stop_at"] or len(all_rows))
                all_rows = all_rows[:stop_at]
                stopped_early = True
                break

        if not cfg.adaptive and batch_end >= cfg.trials:
            break

    trials_path = out_dir / "trials.parquet"
    write_trials_parquet(all_rows, trials_path)

    converged = sum(1 for r in all_rows if r.get("converged"))
    cold_retries = sum(1 for r in all_rows if r.get("cold_retry"))
    elapsed = time.perf_counter() - t0
    audit = {
        "run_id": rid,
        "phase": "F",
        "scenario": cfg.scenario_name,
        "trials": cfg.trials,
        "trials_completed": len(all_rows),
        "trials_requested": trials_target,
        "base_seed": cfg.base_seed,
        "trials_converged": converged,
        "non_convergence_rate": 1.0 - converged / max(len(all_rows), 1),
        "wall_clock_sec": round(elapsed, 3),
        "workbook": str(path),
        "sampling": cfg.sampling,
        "warm_start": cfg.warm_start,
        "mc_lite": cfg.mc_lite,
        "adaptive": cfg.adaptive,
        "adaptive_stopped_early": stopped_early,
        "adaptive_stop_at": stop_at,
        "adaptive_trace": adaptive_trace,
        "cold_retries": cold_retries,
        "conservation_audit_every": cfg.conservation_audit_every,
    }
    (out_dir / "audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

    return McRunResult(
        run_id=rid,
        scenario=cfg.scenario_name,
        trials_requested=cfg.trials if not cfg.adaptive else trials_target,
        trials_completed=len(all_rows),
        trials_converged=converged,
        wall_clock_sec=elapsed,
        output_dir=out_dir,
        trials_parquet=trials_path,
        audit=audit,
    )
