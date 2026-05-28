"""FastAPI service — scenario runs, MC jobs, audit endpoints per PRD §9 / Phase G."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

from spacex_model.config.settings import get_repo_root, get_settings, is_serverless
from spacex_model.engine.pipeline import ModelResult, run_pipeline
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.inputs.demand_curves import demand_curves_from_ingest
from spacex_model.inputs.scenarios import load_scenario
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.mc.distributions import reference_percentiles
from spacex_model.mc.sensitivity import tornado_sensitivity
from spacex_model.service.auth import require_api_key
from spacex_model.service.cache import get_cache
from spacex_model.service.jobs import JobStatus, get_job_manager
from spacex_model.service.mc_store import serverless_job_progress
from spacex_model.service.grid import build_grid_payload
from spacex_model.service.lineage import lookup_lineage
from spacex_model.service.lineage_enrich import enrich_lineage
from spacex_model.service.lineage_graph import build_lineage_graph
from spacex_model.service.lineage_history import fetch_change_history, history_cache_key
from spacex_model.service.run_audit_payload import build_run_audit_payload
from spacex_model.io.scenario_export import (
    export_active_scenario_xlsx,
    export_scenario_pack_xlsx as build_scenario_pack_xlsx,
    run_for_export,
)
from spacex_model.service.client_config import (
    CLIENT_SCENARIO_IDS,
    client_overrides_to_canonical,
    decode_share_state,
    encode_share_state,
    scenario_card_overrides_human,
    serialize_input_whitelist,
    validate_client_overrides,
)
from spacex_model.service.models import (
    ClientShareValidateRequest,
    DeterministicRunRequest,
    ExportScenarioPackRequest,
    ExportScenarioRequest,
    McSubmitRequest,
)
from spacex_model.service.run_store import get_run_store
from spacex_model.service.serializers import (
    serialize_assumption_catalog,
    serialize_lineage_index,
    serialize_model_result,
    serialize_tornado,
)
from spacex_model.service.sheets_meta import get_sheet, serialize_sheets_list

app = FastAPI(
    title="Mach33 SpaceX Valuation Model",
    description="Deterministic scenario runs, Monte Carlo, and audit lineage API",
    version="0.1.0",
)

router = APIRouter(prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _repo_root() -> Path:
    return get_repo_root()


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


def _ui_dir() -> Path | None:
    root = get_repo_root()
    for relative in ("static/ui", "public"):
        candidate = root / relative
        if (candidate / "index.html").is_file():
            return candidate
    return None


@router.get("/health")
def health() -> dict[str, Any]:
    settings = get_settings()
    ui = _ui_dir()
    return {
        "status": "ok",
        "workbook_exists": settings.workbook_path.exists(),
        "git_sha": _git_sha(),
        "repo_root": str(get_repo_root()),
        "ui_available": ui is not None,
        "serverless": is_serverless(),
    }


@router.get("/scenarios", dependencies=[Depends(require_api_key)])
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


@router.get("/assumptions/catalog", dependencies=[Depends(require_api_key)])
def assumptions_catalog() -> list[dict[str, Any]]:
    settings = get_settings()
    if not settings.workbook_path.exists():
        raise HTTPException(status_code=503, detail="Workbook not available")
    ingest = ingest_workbook(settings.workbook_path)
    assumptions = assumptions_from_ingest(ingest)
    return serialize_assumption_catalog(assumptions)


@router.get("/lineage", dependencies=[Depends(require_api_key)])
def lineage_index() -> list[dict[str, Any]]:
    return serialize_lineage_index()


def _store_run(run_id: str, payload: dict[str, Any], result: ModelResult) -> None:
    cache = get_cache()
    cache.set(f"run:{run_id}", payload, ttl_sec=get_settings().cache_ttl_sec)
    get_run_store().put(run_id, result)


def _resolve_model_result(
    run_id: str,
    *,
    scenario: str | None = None,
    overrides: dict[str, Any] | None = None,
) -> ModelResult:
    """Load ModelResult from run store, cache, or re-execute scenario (serverless-safe)."""
    store = get_run_store()
    result = store.get(run_id)
    if result is not None:
        return result

    cached = get_cache().get(f"run:{run_id}")
    sc = scenario or (cached.get("scenario") if cached else None) or "base_case"
    ov = overrides
    if ov is None and cached:
        audit = cached.get("audit") or {}
        if isinstance(audit.get("overrides"), dict):
            ov = audit["overrides"]

    result = run_pipeline(
        scenario_path=_scenario_path(sc),
        extra_overrides=ov or None,
        write_outputs=False,
    )
    store.put(run_id, result)
    return result


def _embed_audit_grids(result: ModelResult, payload: dict[str, Any]) -> None:
    """Attach Starlink grid to deterministic payload — avoids a second pipeline on Vercel."""
    starlink = get_sheet("starlink")
    if starlink is None or not starlink.enabled:
        return
    grid = build_grid_payload(starlink, result)
    payload["audit_grids"] = {"starlink": grid}
    cache = get_cache()
    cache.set(f"grid:{result.run_id}:starlink", grid, ttl_sec=3600)


@router.get("/sheets", dependencies=[Depends(require_api_key)])
def list_sheets() -> list[dict[str, Any]]:
    return serialize_sheets_list()


@router.get("/sheets/{sheet_slug}/grid", dependencies=[Depends(require_api_key)])
def sheet_grid(
    sheet_slug: str,
    run_id: str = Query(..., description="Deterministic run id"),
    scenario: str | None = Query(default=None, description="Scenario fallback for serverless"),
) -> dict[str, Any]:
    meta = get_sheet(sheet_slug)
    if meta is None or meta.slug == "run_audit":
        raise HTTPException(status_code=404, detail=f"Sheet not found: {sheet_slug}")

    cache = get_cache()
    grid_cache_key = f"grid:{run_id}:{sheet_slug}"
    cached_grid = cache.get(grid_cache_key)
    if cached_grid is not None:
        return cached_grid

    result = _resolve_model_result(run_id, scenario=scenario)
    payload = build_grid_payload(meta, result)
    cache.set(grid_cache_key, payload, ttl_sec=3600)
    return payload


@router.get("/lineage/{key}/history", dependencies=[Depends(require_api_key)])
def lineage_history(key: str, limit: int = Query(default=20, ge=1, le=100)) -> dict[str, Any]:
    cache = get_cache()
    cache_key = history_cache_key(key)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    base = lookup_lineage(key)
    module_path = base.module_path if base else None
    function = base.function if base else None
    entries = fetch_change_history(key, module_path=module_path, function=function, limit=limit)
    payload = {"key": key, "entries": entries, "total": len(entries)}
    cache.set(cache_key, payload, ttl_sec=900)
    return payload


@router.get("/lineage/{key}/graph", dependencies=[Depends(require_api_key)])
def lineage_graph(
    key: str,
    run_id: str = Query(..., description="Deterministic run id"),
    depth: int = Query(default=2, ge=1, le=4),
    year: int | None = Query(default=None, ge=2025, le=2050),
    sheet: str | None = Query(default=None),
    row: int | None = Query(default=None),
    scenario: str | None = Query(default=None, description="Scenario fallback for serverless"),
) -> dict[str, Any]:
    try:
        result = _resolve_model_result(run_id, scenario=scenario)
        return build_lineage_graph(
            key,
            result,
            depth=depth,
            year=year,
            sheet=sheet,
            row=row,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown lineage key: {key}") from None


@router.get("/runs/{run_id}/audit-dashboard", dependencies=[Depends(require_api_key)])
def run_audit_dashboard(
    run_id: str,
    scenario: str | None = Query(default=None, description="Scenario fallback for serverless"),
) -> dict[str, Any]:
    cache = get_cache()
    cache_key = f"audit_dashboard:{run_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    result = _resolve_model_result(run_id, scenario=scenario)
    payload = build_run_audit_payload(result)
    cache.set(cache_key, payload, ttl_sec=3600)
    return payload


@router.get("/lineage/{key}", dependencies=[Depends(require_api_key)])
def lineage_detail(
    key: str,
    run_id: str | None = Query(default=None),
    year: int | None = Query(default=None, ge=2025, le=2050),
    sheet: str | None = Query(default=None),
    row: int | None = Query(default=None),
    scenario: str | None = Query(default=None, description="Scenario fallback for serverless"),
) -> dict[str, Any]:
    if run_id:
        try:
            result = _resolve_model_result(run_id, scenario=scenario)
            return enrich_lineage(
                key,
                result,
                year=year,
                sheet=sheet,
                row=row,
            )
        except KeyError:
            raise HTTPException(status_code=404, detail=f"Unknown lineage key: {key}") from None

    entry = lookup_lineage(key)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"Unknown lineage key: {key}")
    return entry.to_dict()


@router.post("/runs/deterministic", dependencies=[Depends(require_api_key)])
def run_deterministic(body: DeterministicRunRequest) -> dict[str, Any]:
    settings = get_settings()
    if not settings.workbook_path.exists():
        raise HTTPException(status_code=503, detail="Workbook not available")

    merged_overrides: dict[str, Any] = dict(body.overrides)
    if body.client_overrides:
        errors = validate_client_overrides(body.client_overrides)
        if errors:
            raise HTTPException(status_code=400, detail={"errors": errors})
        merged_overrides.update(client_overrides_to_canonical(body.client_overrides))

    cache = get_cache()
    key = _cache_key(body.scenario, merged_overrides)
    scenario_path = _scenario_path(body.scenario)
    if body.use_cache:
        cached = cache.get(key)
        if cached is not None:
            out = {**cached, "cached": True}
            rid = cached.get("run_id")
            if rid and get_run_store().get(rid) is None:
                try:
                    result = run_pipeline(
                        scenario_path=scenario_path,
                        extra_overrides=merged_overrides or None,
                        write_outputs=False,
                    )
                    get_run_store().put(rid, result)
                    if is_serverless() and "audit_grids" not in out:
                        _embed_audit_grids(result, out)
                except Exception:
                    pass
            return out

    ingest = ingest_workbook(settings.workbook_path)
    base_assumptions = assumptions_from_ingest(ingest)
    override_warnings = _validate_overrides(base_assumptions, merged_overrides)

    result = run_pipeline(
        scenario_path=scenario_path,
        extra_overrides=merged_overrides or None,
        write_outputs=not is_serverless(),
    )

    payload = serialize_model_result(result, cached=False)
    payload["override_warnings"] = override_warnings
    cache.set(key, payload, ttl_sec=settings.cache_ttl_sec)
    _store_run(result.run_id, payload, result)
    _embed_audit_grids(result, payload)
    return payload


@router.get("/runs/{run_id}", dependencies=[Depends(require_api_key)])
def get_run(run_id: str) -> dict[str, Any]:
    settings = get_settings()
    audit_path = settings.outputs_dir / run_id / "audit.json"
    if not audit_path.exists():
        raise HTTPException(status_code=404, detail=f"Run not found: {run_id}")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    return {"run_id": run_id, "audit": audit}


@router.get("/runs/{run_id}/audit", dependencies=[Depends(require_api_key)])
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


@router.get("/runs/{run_id}/tornado", dependencies=[Depends(require_api_key)])
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


@router.post("/runs/mc", dependencies=[Depends(require_api_key)])
def submit_mc(body: McSubmitRequest) -> dict[str, Any]:
    settings = get_settings()
    if not settings.workbook_path.exists():
        raise HTTPException(status_code=503, detail="Workbook not available")
    trials = body.trials
    include_tornado = body.include_tornado
    if is_serverless():
        trials = min(trials, settings.mc_serverless_max_trials)
        # Tornado runs dozens of full pipelines; defer to GET /runs/{id}/tornado on serverless.
        include_tornado = False
    job_id = get_job_manager().submit_mc(
        trials=trials,
        base_seed=body.base_seed,
        n_jobs=1 if is_serverless() else body.n_jobs,
        scenario_name=body.scenario,
        include_tornado=include_tornado,
        tornado_top=body.tornado_top,
        workbook_path=settings.workbook_path,
    )
    out: dict[str, Any] = {"job_id": job_id, "status": JobStatus.QUEUED.value}
    if is_serverless():
        out["execution"] = "batched"
        out["hint"] = "Poll GET /api/runs/mc/{job_id} until status is completed (each poll runs a batch)."
    return out


@router.get("/runs/mc/{job_id}", dependencies=[Depends(require_api_key)])
def get_mc_job(job_id: str) -> dict[str, Any]:
    job = get_job_manager().get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail=f"MC job not found: {job_id}")
    response: dict[str, Any] = {
        "job_id": job.job_id,
        "status": job.status.value,
    }
    progress = serverless_job_progress(job_id)
    if progress is not None:
        response["progress"] = progress
    if job.error:
        response["error"] = job.error
    if job.result:
        response["result"] = job.result
    return response


def _preview_ev_for_scenario(scenario: str, overrides: dict[str, Any] | None = None) -> float | None:
    """Best-effort Group EV from cache without running pipeline."""
    cache = get_cache()
    key = _cache_key(scenario, overrides or {})
    cached = cache.get(key)
    if cached and "valuation" in cached:
        ev = cached["valuation"].get("group_ev_2025_b")
        return float(ev) if ev is not None else None
    return None


@router.get("/client/scenarios", dependencies=[Depends(require_api_key)])
def client_scenarios() -> list[dict[str, Any]]:
    """Curated Base / Bear / Bull cards for Client Mode."""
    out: list[dict[str, Any]] = []
    for name in CLIENT_SCENARIO_IDS:
        path = _scenario_path(name)
        spec = load_scenario(path)
        preview = _preview_ev_for_scenario(name, spec.overrides)
        out.append(
            {
                "id": name,
                "name": name.replace("_", " ").title(),
                "description": spec.description.strip() or f"{name} scenario",
                "key_inputs": scenario_card_overrides_human(name, spec.overrides),
                "group_ev_2025_b": preview,
            }
        )
    return out


@router.get("/client/inputs/whitelist", dependencies=[Depends(require_api_key)])
def client_inputs_whitelist() -> list[dict[str, Any]]:
    return serialize_input_whitelist()


@router.post("/client/validate-share", dependencies=[Depends(require_api_key)])
def client_validate_share(body: ClientShareValidateRequest) -> dict[str, Any]:
    errors = validate_client_overrides(body.overrides)
    if errors:
        raise HTTPException(status_code=400, detail={"errors": errors})
    canonical = client_overrides_to_canonical(body.overrides)
    return {
        "ok": True,
        "scenario": body.scenario,
        "canonical_overrides": canonical,
        "share_token": encode_share_state(body.scenario, body.overrides),
    }


@router.get("/client/decode-share", dependencies=[Depends(require_api_key)])
def client_decode_share(s: str = Query(..., min_length=1)) -> dict[str, Any]:
    try:
        payload = decode_share_state(s)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "scenario": payload.scenario,
        "overrides": payload.overrides,
        "canonical_overrides": client_overrides_to_canonical(payload.overrides),
    }


@router.get("/client/methodology", dependencies=[Depends(require_api_key)])
def client_methodology_download() -> Response:
    """Methodology one-pager (text until tagged-release PDF asset ships)."""
    text = (
        "Mach33 SpaceX Valuation Model — Methodology Summary\n"
        "====================================================\n\n"
        "This model values SpaceX on a sum-of-parts basis across Customer Launch, "
        "Starlink, ODC, AI Stack, and Lunar/Mars modules, with group-level P&L "
        "conservation and a 2025–2050 horizon.\n\n"
        "Scenarios (Base, Bear, Bull) apply vetted macro and carve-out assumptions. "
        "Custom scenarios adjust a bounded subset of Monte Carlo inputs; outputs are "
        "deterministic given those inputs.\n\n"
        "For cell-level derivations and audit trails, use Audit Mode in the web app.\n"
        "Authority: Architecture & Methodology spec and context.md constitutional locks.\n"
    )
    return Response(
        content=text.encode("utf-8"),
        media_type="text/plain; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="mach33_methodology_one_pager.txt"'
        },
    )


@router.post("/exports/scenario.xlsx", dependencies=[Depends(require_api_key)])
def export_scenario_xlsx(body: ExportScenarioRequest) -> Response:
    settings = get_settings()
    if not settings.workbook_path.exists():
        raise HTTPException(status_code=503, detail="Workbook not available")

    canonical_ov: dict[str, Any] = {}
    if body.overrides:
        errors = validate_client_overrides(body.overrides)
        if errors:
            raise HTTPException(status_code=400, detail={"errors": errors})
        canonical_ov = client_overrides_to_canonical(body.overrides)

    if body.run_id:
        try:
            result = _resolve_model_result(
                body.run_id,
                scenario=body.scenario,
                overrides=canonical_ov or None,
            )
        except Exception as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
    else:
        path = _scenario_path(body.scenario)
        spec = load_scenario(path)
        merged = {**spec.overrides, **canonical_ov}
        result = run_for_export(path, extra_overrides=merged or None)

    spec = load_scenario(_scenario_path(body.scenario))
    data = export_active_scenario_xlsx(
        result,
        scenario_name=body.scenario.replace("_", " ").title(),
        description=spec.description.strip(),
        base_url=body.public_base_url,
    )
    filename = f"spacex_{body.scenario}.xlsx"
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/exports/scenario_pack.xlsx", dependencies=[Depends(require_api_key)])
def export_scenario_pack_xlsx(body: ExportScenarioPackRequest) -> Response:
    settings = get_settings()
    if not settings.workbook_path.exists():
        raise HTTPException(status_code=503, detail="Workbook not available")

    allowed = set(CLIENT_SCENARIO_IDS)
    names = [n for n in body.scenarios if n in allowed]
    if not names:
        raise HTTPException(status_code=400, detail="No valid scenarios in pack request")

    results: dict[str, ModelResult] = {}
    descriptions: dict[str, str] = {}
    for name in names:
        path = _scenario_path(name)
        spec = load_scenario(path)
        descriptions[name] = spec.description.strip()
        results[name] = run_for_export(path, extra_overrides=spec.overrides or None)

    data = build_scenario_pack_xlsx(
        results,
        descriptions,
        base_url=body.public_base_url,
    )
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="spacex_scenario_pack.xlsx"'},
    )


def _mount_ui() -> None:
    """Serve Vite build output when present (tracked static/ui/ on Vercel)."""
    ui = _ui_dir()
    if ui is None:
        return
    index = ui / "index.html"
    assets = ui / "assets"

    @app.get("/", include_in_schema=False)
    def serve_ui_index() -> FileResponse:
        return FileResponse(index)

    if assets.is_dir():
        app.mount("/assets", StaticFiles(directory=assets), name="ui-assets")


_mount_ui()

app.include_router(router)


def _mount_spa_fallback() -> None:
    """Client-side routes (/audit/*, /client/*) — same index.html as Vercel SPA rewrite."""
    ui = _ui_dir()
    if ui is None:
        return
    index = ui / "index.html"

    @app.get("/{full_path:path}", include_in_schema=False)
    def spa_fallback(full_path: str) -> FileResponse:
        if full_path.startswith("api") or full_path.startswith("assets/"):
            raise HTTPException(status_code=404, detail="Not found")
        return FileResponse(index)


_mount_spa_fallback()


def create_app() -> FastAPI:
    return app
