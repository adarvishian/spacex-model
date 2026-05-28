"""FastAPI service — scenario runs, MC jobs, audit endpoints per PRD §9 / Phase G."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_pipeline
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.inputs.demand_curves import demand_curves_from_ingest
from spacex_model.inputs.scenarios import load_scenario
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.mc.distributions import reference_percentiles
from spacex_model.mc.sensitivity import tornado_sensitivity
from spacex_model.service.auth import require_api_key
from spacex_model.service.cache import get_cache
from spacex_model.service.jobs import JobStatus, get_job_manager
from spacex_model.service.lineage import lookup_lineage
from spacex_model.service.models import DeterministicRunRequest, McSubmitRequest
from spacex_model.service.serializers import (
    serialize_assumption_catalog,
    serialize_lineage_index,
    serialize_model_result,
    serialize_tornado,
)

app = FastAPI(
    title="Mach33 SpaceX Valuation Model",
    description="Deterministic scenario runs, Monte Carlo, and audit lineage API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _git_sha() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=_repo_root(),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _scenario_path(name: str) -> Path:
    settings = get_settings()
    path = settings.scenarios_dir / f"{name}.yaml"
    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Scenario not found: {name}")
    return path


def _cache_key(scenario: str, overrides: dict[str, Any]) -> str:
    raw = json.dumps({"scenario": scenario, "overrides": overrides}, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:24]


def _validate_overrides(
    assumptions: Any,
    overrides: dict[str, Any],
) -> list[dict[str, str]]:
    """Warn when overrides fall outside MC P10-P90 envelope."""
    warnings: list[dict[str, str]] = []
    for label, raw in overrides.items():
        meta = assumptions.mc_ranges.by_label.get(label)
        row = assumptions.by_label.get(label)
        if meta is None or row is None:
            continue
        if not meta.distribution or meta.mc_min is None or meta.mc_max is None:
            continue
        base = row.scalar() or 0.0
        try:
            pct = reference_percentiles(
                meta.distribution,
                base=base,
                low=meta.mc_min,
                high=meta.mc_max,
                n_samples=5000,
                seed=0,
            )
        except Exception:
            continue
        val = float(raw) if isinstance(raw, (int, float)) else base
        if val < pct["p10"]:
            warnings.append(
                {
                    "label": label,
                    "value": str(val),
                    "message": f"Below MC P10 ({pct['p10']:.4g})",
                }
            )
        elif val > pct["p90"]:
            warnings.append(
                {
                    "label": label,
                    "value": str(val),
                    "message": f"Above MC P90 ({pct['p90']:.4g})",
                }
            )
    return warnings


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "Mach33 SpaceX Valuation Model", "health": "/health"}


@app.get("/health")
def health() -> dict[str, Any]:
    settings = get_settings()
    return {
        "status": "ok",
        "workbook_exists": settings.workbook_path.exists(),
        "git_sha": _git_sha(),
    }


@app.get("/scenarios", dependencies=[Depends(require_api_key)])
def list_scenarios() -> list[dict[str, str]]:
    settings = get_settings()
    out: list[dict[str, str]] = []
    for path in sorted(settings.scenarios_dir.glob("*.yaml")):
        spec = load_scenario(path)
        out.append(
            {
                "name": spec.name,
                "description": spec.description,
                "path": str(path.relative_to(_repo_root())),
            }
        )
    return out


@app.get("/assumptions/catalog", dependencies=[Depends(require_api_key)])
def assumptions_catalog() -> list[dict[str, Any]]:
    settings = get_settings()
    if not settings.workbook_path.exists():
        raise HTTPException(status_code=503, detail="Workbook not available")
    ingest = ingest_workbook(settings.workbook_path)
    assumptions = assumptions_from_ingest(ingest)
    return serialize_assumption_catalog(assumptions)


@app.get("/lineage", dependencies=[Depends(require_api_key)])
def lineage_index() -> list[dict[str, Any]]:
    return serialize_lineage_index()


@app.get("/lineage/{key}", dependencies=[Depends(require_api_key)])
def lineage_detail(key: str) -> dict[str, Any]:
    entry = lookup_lineage(key)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Unknown lineage key: {key}")
    return entry.to_dict()


@app.post("/runs/deterministic", dependencies=[Depends(require_api_key)])
def run_deterministic(body: DeterministicRunRequest) -> dict[str, Any]:
    settings = get_settings()
    if not settings.workbook_path.exists():
        raise HTTPException(status_code=503, detail="Workbook not available")

    cache = get_cache()
    key = _cache_key(body.scenario, body.overrides)
    if body.use_cache:
        cached = cache.get(key)
        if cached is not None:
            return {**cached, "cached": True}

    scenario_path = _scenario_path(body.scenario)

    ingest = ingest_workbook(settings.workbook_path)
    base_assumptions = assumptions_from_ingest(ingest)
    override_warnings = _validate_overrides(base_assumptions, body.overrides)

    result = run_pipeline(
        scenario_path=scenario_path,
        extra_overrides=body.overrides or None,
        write_outputs=True,
    )

    payload = serialize_model_result(result, cached=False)
    payload["override_warnings"] = override_warnings
    cache.set(key, payload, ttl_sec=settings.cache_ttl_sec)
    return payload


@app.get("/runs/{run_id}", dependencies=[Depends(require_api_key)])
def get_run(run_id: str) -> dict[str, Any]:
    settings = get_settings()
    audit_path = settings.outputs_dir / run_id / "audit.json"
    if not audit_path.exists():
        raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    return {"run_id": run_id, "audit": audit}


@app.get("/runs/{run_id}/audit", dependencies=[Depends(require_api_key)])
def get_run_audit(run_id: str) -> dict[str, Any]:
    settings = get_settings()
    out_dir = settings.outputs_dir / run_id
    audit_path = out_dir / "audit.json"
    if not audit_path.exists():
        raise HTTPException(status_code=404, detail=f"Audit not found: {run_id}")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    solver_path = out_dir / "solver_trace.json"
    solver = None
    if solver_path.exists():
        solver = json.loads(solver_path.read_text(encoding="utf-8"))
    return {"run_id": run_id, "audit": audit, "solver_trace": solver}


@app.get("/runs/{run_id}/tornado", dependencies=[Depends(require_api_key)])
def get_run_tornado(
    run_id: str,
    top_n: int = Query(default=10, ge=1, le=50),
) -> dict[str, Any]:
    settings = get_settings()
    if not settings.workbook_path.exists():
        raise HTTPException(status_code=503, detail="Workbook not available")
    ingest = ingest_workbook(settings.workbook_path)
    assumptions = assumptions_from_ingest(ingest)
    demand = demand_curves_from_ingest(ingest)
    bars = tornado_sensitivity(assumptions, ingest=ingest, demand=demand, top_n=top_n)
    return {"run_id": run_id, "tornado": serialize_tornado(bars)}


@app.post("/runs/mc", dependencies=[Depends(require_api_key)])
def submit_mc(body: McSubmitRequest) -> dict[str, Any]:
    settings = get_settings()
    if not settings.workbook_path.exists():
        raise HTTPException(status_code=503, detail="Workbook not available")
    job_id = get_job_manager().submit_mc(
        trials=body.trials,
        base_seed=body.base_seed,
        n_jobs=body.n_jobs,
        scenario_name=body.scenario,
        include_tornado=body.include_tornado,
        tornado_top=body.tornado_top,
        workbook_path=settings.workbook_path,
    )
    return {"job_id": job_id, "status": JobStatus.QUEUED.value}


@app.get("/runs/mc/{job_id}", dependencies=[Depends(require_api_key)])
def get_mc_job(job_id: str) -> dict[str, Any]:
    job = get_job_manager().get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"MC job not found: {job_id}")
    response: dict[str, Any] = {
        "job_id": job.job_id,
        "status": job.status.value,
    }
    if job.error:
        response["error"] = job.error
    if job.result:
        response["result"] = job.result
    return response


def create_app() -> FastAPI:
    return app
