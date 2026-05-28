"""Durable MC job store for serverless — progress via repeated GET /runs/mc/{id} polls."""

from __future__ import annotations

import json
import pickle
import time
import uuid
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_base_case
from spacex_model.inputs.assumptions import Assumptions, assumptions_from_ingest
from spacex_model.inputs.demand_curves import DemandCurves, demand_curves_from_ingest
from spacex_model.io.excel_ingest import IngestResult, ingest_workbook
from spacex_model.mc.aggregator import aggregate_trials
from spacex_model.mc.results import extract_trial_metrics, read_trials_parquet, write_trials_parquet
from spacex_model.mc.runner import McRunConfig, run_mc_trials
from spacex_model.service.serializers import serialize_mc_aggregation

_STATUS_QUEUED = "queued"
_STATUS_RUNNING = "running"
_STATUS_COMPLETED = "completed"
_STATUS_FAILED = "failed"


@dataclass
class _JobState:
    job_id: str
    status: str
    trials: int
    trials_done: int
    base_seed: int
    scenario_name: str
    include_tornado: bool
    tornado_top: int
    workbook_path: str
    error: str | None = None
    created_at: float = 0.0


def _jobs_root() -> Path:
    return get_settings().outputs_dir / "jobs"


def _job_dir(job_id: str) -> Path:
    return _jobs_root() / job_id


def _state_path(job_id: str) -> Path:
    return _job_dir(job_id) / "state.json"


def _context_path(job_id: str) -> Path:
    return _job_dir(job_id) / "context.pkl"


def _trials_path(job_id: str) -> Path:
    return _job_dir(job_id) / "trials.parquet"


def _load_state(job_id: str) -> _JobState:
    data = json.loads(_state_path(job_id).read_text(encoding="utf-8"))
    return _JobState(**data)


def _save_state(state: _JobState) -> None:
    path = _state_path(state.job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(state), indent=2), encoding="utf-8")


def _load_context(job_id: str) -> tuple[IngestResult, Assumptions, DemandCurves]:
    with _context_path(job_id).open("rb") as fh:
        ingest, assumptions, demand = pickle.load(fh)
    return ingest, assumptions, demand


def _save_context(job_id: str, ingest: IngestResult, assumptions: Assumptions, demand: DemandCurves) -> None:
    path = _context_path(job_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        pickle.dump((ingest, assumptions, demand), fh, protocol=pickle.HIGHEST_PROTOCOL)


def _append_trials(job_id: str, new_rows: list[dict[str, Any]]) -> None:
    path = _trials_path(job_id)
    if path.exists():
        existing = read_trials_parquet(path).to_pylist()
        rows = existing + new_rows
    else:
        rows = new_rows
    write_trials_parquet(rows, path)


def create_serverless_job(
    *,
    trials: int,
    base_seed: int,
    scenario_name: str,
    include_tornado: bool,
    tornado_top: int,
    workbook_path: Path,
) -> str:
    """Create a queued MC job on disk; execution advances on status polls."""
    settings = get_settings()
    trials = min(trials, settings.mc_serverless_max_trials)
    job_id = str(uuid.uuid4())[:8]
    out = _job_dir(job_id)
    out.mkdir(parents=True, exist_ok=True)
    state = _JobState(
        job_id=job_id,
        status=_STATUS_QUEUED,
        trials=trials,
        trials_done=0,
        base_seed=base_seed,
        scenario_name=scenario_name,
        include_tornado=include_tornado,
        tornado_top=tornado_top,
        workbook_path=str(workbook_path),
        created_at=time.time(),
    )
    _save_state(state)
    return job_id


def _finalize_job(state: _JobState) -> dict[str, Any]:
    settings = get_settings()
    path = Path(state.workbook_path)
    table = read_trials_parquet(_trials_path(state.job_id))
    base = run_base_case(workbook_path=path, write_outputs=False)
    base_metrics = extract_trial_metrics(base)
    agg = aggregate_trials(table, base_metrics=base_metrics)

    out_dir = settings.outputs_dir / "mc" / state.scenario_name / state.job_id
    out_dir.mkdir(parents=True, exist_ok=True)
    trials_path = out_dir / "trials.parquet"
    write_trials_parquet(table.to_pylist(), trials_path)

    converged = sum(1 for r in table.to_pylist() if r.get("converged"))
    payload: dict[str, Any] = {
        "job_id": state.job_id,
        "run_id": state.job_id,
        "scenario": state.scenario_name,
        "trials_completed": state.trials,
        "trials_converged": converged,
        "wall_clock_sec": round(time.time() - state.created_at, 3),
        "aggregation": serialize_mc_aggregation(agg),
        "trials_parquet": str(trials_path),
        "serverless": True,
    }
    if state.include_tornado:
        payload["tornado_note"] = (
            "Tornado skipped on serverless (timeout). Use GET /api/runs/{run_id}/tornado after a deterministic run."
        )
    (out_dir / "aggregation.json").write_text(
        json.dumps(payload["aggregation"], indent=2),
        encoding="utf-8",
    )
    return payload


@dataclass
class ServerlessMcSnapshot:
    """Lightweight job view returned from the on-disk store (no import from jobs.py)."""

    job_id: str
    status: str
    config: McRunConfig
    error: str | None = None
    result: dict[str, Any] | None = None
    output_dir: Path | None = None


def advance_serverless_job(job_id: str) -> ServerlessMcSnapshot | None:
    """Run the next MC batch (if needed) and return current job snapshot."""
    if not _state_path(job_id).exists():
        return None

    state = _load_state(job_id)
    cfg = McRunConfig(
        trials=state.trials,
        base_seed=state.base_seed,
        scenario_name=state.scenario_name,
    )

    if state.status == _STATUS_COMPLETED:
        result_path = _job_dir(job_id) / "result.json"
        result = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else None
        return ServerlessMcSnapshot(
            job_id=job_id,
            status=_STATUS_COMPLETED,
            config=cfg,
            result=result,
            output_dir=get_settings().outputs_dir / "mc" / state.scenario_name / job_id,
        )

    if state.status == _STATUS_FAILED:
        return ServerlessMcSnapshot(job_id=job_id, status=_STATUS_FAILED, config=cfg, error=state.error)

    settings = get_settings()
    batch = max(1, settings.mc_serverless_batch_trials)

    try:
        state.status = _STATUS_RUNNING
        _save_state(state)

        if not _context_path(job_id).exists():
            ingest = ingest_workbook(Path(state.workbook_path))
            assumptions = assumptions_from_ingest(ingest)
            demand = demand_curves_from_ingest(ingest)
            _save_context(job_id, ingest, assumptions, demand)

        ingest, assumptions, demand = _load_context(job_id)
        start = state.trials_done
        end = min(start + batch, state.trials)
        indices = list(range(start, end))
        if indices:
            rows = run_mc_trials(
                indices,
                base_assumptions=assumptions,
                demand_curves=demand,
                ingest=ingest,
                base_seed=state.base_seed,
                n_jobs=1,
            )
            _append_trials(job_id, rows)
            state.trials_done = end

        if state.trials_done >= state.trials:
            result = _finalize_job(state)
            (_job_dir(job_id) / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
            state.status = _STATUS_COMPLETED
            _save_state(state)
            return ServerlessMcSnapshot(
                job_id=job_id,
                status=_STATUS_COMPLETED,
                config=cfg,
                result=result,
                output_dir=get_settings().outputs_dir / "mc" / state.scenario_name / job_id,
            )

        state.status = _STATUS_RUNNING
        _save_state(state)
        return ServerlessMcSnapshot(job_id=job_id, status=_STATUS_RUNNING, config=cfg)

    except Exception as exc:
        state.status = _STATUS_FAILED
        state.error = str(exc)
        _save_state(state)
        return ServerlessMcSnapshot(job_id=job_id, status=_STATUS_FAILED, config=cfg, error=str(exc))


def get_serverless_job(job_id: str, *, advance: bool = True) -> ServerlessMcSnapshot | None:
    if not _state_path(job_id).exists():
        return None
    if advance:
        return advance_serverless_job(job_id)
    state = _load_state(job_id)
    cfg = McRunConfig(
        trials=state.trials,
        base_seed=state.base_seed,
        scenario_name=state.scenario_name,
    )
    snap = ServerlessMcSnapshot(job_id=job_id, status=state.status, config=cfg, error=state.error)
    if state.status == _STATUS_COMPLETED:
        result_path = _job_dir(job_id) / "result.json"
        if result_path.exists():
            snap.result = json.loads(result_path.read_text(encoding="utf-8"))
    return snap


def serverless_job_progress(job_id: str) -> dict[str, int] | None:
    if not _state_path(job_id).exists():
        return None
    state = _load_state(job_id)
    return {"trials_done": state.trials_done, "trials": state.trials}
