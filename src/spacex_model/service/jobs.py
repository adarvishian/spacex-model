"""Background MC job manager — Phase G."""

from __future__ import annotations

import json
import threading
import uuid
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_base_case
from spacex_model.mc.aggregator import aggregate_trials
from spacex_model.mc.results import extract_trial_metrics, read_trials_parquet
from spacex_model.mc.runner import McRunConfig, run_mc
from spacex_model.mc.sensitivity import tornado_sensitivity
from spacex_model.service.serializers import serialize_mc_aggregation, serialize_tornado


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class McJob:
    job_id: str
    status: JobStatus = JobStatus.QUEUED
    config: McRunConfig = field(default_factory=McRunConfig)
    error: str | None = None
    result: dict[str, Any] | None = None
    output_dir: Path | None = None


class JobManager:
    """In-process background job queue for MC studies."""

    def __init__(self) -> None:
        self._jobs: dict[str, McJob] = {}
        self._lock = threading.Lock()

    def submit_mc(
        self,
        *,
        trials: int = 10_000,
        base_seed: int = 42,
        n_jobs: int = -1,
        scenario_name: str = "base_case",
        include_tornado: bool = False,
        tornado_top: int = 10,
        workbook_path: Path | None = None,
    ) -> str:
        job_id = str(uuid.uuid4())[:8]
        cfg = McRunConfig(
            trials=trials,
            base_seed=base_seed,
            n_jobs=n_jobs,
            scenario_name=scenario_name,
        )
        job = McJob(job_id=job_id, config=cfg)
        with self._lock:
            self._jobs[job_id] = job

        thread = threading.Thread(
            target=self._run_mc_job,
            args=(job_id, cfg, include_tornado, tornado_top, workbook_path),
            daemon=True,
        )
        thread.start()
        return job_id

    def get(self, job_id: str) -> McJob | None:
        with self._lock:
            return self._jobs.get(job_id)

    def _run_mc_job(
        self,
        job_id: str,
        cfg: McRunConfig,
        include_tornado: bool,
        tornado_top: int,
        workbook_path: Path | None,
    ) -> None:
        settings = get_settings()
        path = workbook_path or settings.workbook_path
        with self._lock:
            job = self._jobs[job_id]
            job.status = JobStatus.RUNNING

        try:
            mc = run_mc(workbook_path=path, config=cfg, run_id=job_id)
            table = read_trials_parquet(mc.trials_parquet)
            base = run_base_case(workbook_path=path, write_outputs=False)
            base_metrics = extract_trial_metrics(base)
            agg = aggregate_trials(table, base_metrics=base_metrics)

            payload: dict[str, Any] = {
                "job_id": job_id,
                "run_id": mc.run_id,
                "scenario": mc.scenario,
                "trials_completed": mc.trials_completed,
                "trials_converged": mc.trials_converged,
                "wall_clock_sec": mc.wall_clock_sec,
                "audit": mc.audit,
                "aggregation": serialize_mc_aggregation(agg),
                "trials_parquet": str(mc.trials_parquet),
            }

            if include_tornado:
                from spacex_model.inputs.assumptions import assumptions_from_ingest
                from spacex_model.inputs.demand_curves import demand_curves_from_ingest
                from spacex_model.io.excel_ingest import ingest_workbook

                ingest = ingest_workbook(path)
                assumptions = assumptions_from_ingest(ingest)
                demand = demand_curves_from_ingest(ingest)
                bars = tornado_sensitivity(
                    assumptions,
                    ingest=ingest,
                    demand=demand,
                    top_n=tornado_top,
                )
                payload["tornado"] = serialize_tornado(bars)

            with self._lock:
                job = self._jobs[job_id]
                job.status = JobStatus.COMPLETED
                job.result = payload
                job.output_dir = mc.output_dir

            audit_path = mc.output_dir / "aggregation.json"
            audit_path.write_text(json.dumps(payload["aggregation"], indent=2), encoding="utf-8")

        except Exception as exc:
            with self._lock:
                job = self._jobs[job_id]
                job.status = JobStatus.FAILED
                job.error = str(exc)


_manager: JobManager | None = None


def get_job_manager() -> JobManager:
    global _manager
    if _manager is None:
        _manager = JobManager()
    return _manager
