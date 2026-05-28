"""Phase G — FastAPI service + Web UI tests."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"


@pytest.fixture
def client():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from spacex_model.service.api import app

    return TestClient(app)


def test_health(client) -> None:
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"


def test_list_scenarios(client) -> None:
    res = client.get("/api/scenarios")
    assert res.status_code == 200
    names = {s["name"] for s in res.json()}
    assert "base_case" in names
    assert "bear" in names


def test_lineage_index(client) -> None:
    res = client.get("/api/lineage")
    assert res.status_code == 200
    keys = {e["key"] for e in res.json()}
    assert "group.group_fcf" in keys


def test_lineage_detail(client) -> None:
    res = client.get("/api/lineage/group.group_fcf")
    assert res.status_code == 200
    body = res.json()
    assert body["function"]
    assert "GROUP FCF" in body["excel_label"]


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_deterministic_run_and_cache(client) -> None:
    from spacex_model.service.cache import get_cache

    get_cache().delete("test")  # warm cache module
    payload = {"scenario": "base_case", "overrides": {}, "use_cache": True}
    res1 = client.post("/api/runs/deterministic", json=payload)
    assert res1.status_code == 200
    body1 = res1.json()
    assert body1["run_id"]
    assert "valuation" in body1
    assert body1["valuation"]["group_ev_2025_b"] > 0
    assert "group" in body1
    assert "modules" in body1

    res2 = client.post("/api/runs/deterministic", json=payload)
    assert res2.status_code == 200
    body2 = res2.json()
    assert body2.get("cached") is True


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_in_memory_cache_roundtrip() -> None:
    from spacex_model.service.cache import InMemoryCache

    cache = InMemoryCache(max_entries=2)
    cache.set("a", {"x": 1})
    assert cache.get("a") == {"x": 1}
    cache.delete("a")
    assert cache.get("a") is None


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
@pytest.mark.slow
def test_mc_job_submit(client) -> None:
    res = client.post(
        "/api/runs/mc",
        json={"trials": 4, "base_seed": 1, "n_jobs": 1, "include_tornado": False},
    )
    assert res.status_code == 200
    job_id = res.json()["job_id"]

    import time

    status = "queued"
    for _ in range(120):
        poll = client.get(f"/api/runs/mc/{job_id}")
        assert poll.status_code == 200
        status = poll.json()["status"]
        if status in ("completed", "failed"):
            break
        time.sleep(1)

    assert status == "completed", poll.json()


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_tornado_skips_non_convergence(monkeypatch) -> None:
    from spacex_model.engine.iterative_solver import NonConvergenceError
    from spacex_model.inputs.assumptions import assumptions_from_ingest
    from spacex_model.inputs.demand_curves import demand_curves_from_ingest
    from spacex_model.io.excel_ingest import ingest_workbook
    from spacex_model.mc.sensitivity import _run_ev, tornado_sensitivity

    ingest = ingest_workbook(WORKBOOK)
    assumptions = assumptions_from_ingest(ingest)
    demand = demand_curves_from_ingest(ingest)

    def fail_pipeline(*args, **kwargs):
        raise NonConvergenceError(
            "Solver did not converge in 100 iterations (max_residual=0.01, holder=cash_boy)"
        )

    monkeypatch.setattr("spacex_model.mc.sensitivity.run_pipeline", fail_pipeline)

    assert np.isnan(
        _run_ev(
            assumptions,
            ingest=ingest,
            demand=demand,
            overrides={"TAM inflation rate (annual)": 0.05},
        )
    )
    bars = tornado_sensitivity(
        assumptions,
        ingest=ingest,
        demand=demand,
        labels=["TAM inflation rate (annual)"],
        top_n=1,
    )
    assert bars == []


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
@pytest.mark.slow
def test_serverless_mc_batched(client, monkeypatch, tmp_path) -> None:
    """Serverless path runs trials across polls instead of one long invocation."""
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("SPACEX_MODEL_OUTPUTS_DIR", str(tmp_path / "outputs"))

    from spacex_model.service import jobs as jobs_mod

    jobs_mod._manager = None

    res = client.post(
        "/api/runs/mc",
        json={"trials": 3, "base_seed": 1, "n_jobs": 1, "include_tornado": False},
    )
    assert res.status_code == 200
    assert res.json().get("execution") == "batched"
    job_id = res.json()["job_id"]

    import time

    status = "queued"
    for _ in range(60):
        poll = client.get(f"/api/runs/mc/{job_id}")
        assert poll.status_code == 200
        body = poll.json()
        status = body["status"]
        if status in ("completed", "failed"):
            break
        time.sleep(0.5)

    assert status == "completed", poll.json()
    assert poll.json()["progress"]["trials_done"] == 3


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_list_sheets(client) -> None:
    res = client.get("/api/sheets")
    assert res.status_code == 200
    slugs = {s["slug"] for s in res.json()}
    assert "starlink" in slugs
    assert "assumptions" in slugs


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
@pytest.mark.slow
def test_starlink_grid_and_extended_lineage(client) -> None:
    run = client.post(
        "/api/runs/deterministic",
        json={"scenario": "base_case", "overrides": {}, "use_cache": True},
    )
    assert run.status_code == 200
    run_id = run.json()["run_id"]

    grid = client.get(f"/api/sheets/starlink/grid?run_id={run_id}")
    assert grid.status_code == 200
    body = grid.json()
    assert body["sheet"] == "starlink"
    assert len(body["rows"]) > 0
    assert len(body["years"]) == 26

    detail = client.get(
        f"/api/lineage/module.starlink.total_revenue?run_id={run_id}&year=2030"
    )
    assert detail.status_code == 200
    ext = detail.json()
    assert ext["formula_expression"]
    assert ext["lifecycle_stage"]
    assert "resolved_inputs" in ext


def test_frontend_package_exists() -> None:
    pkg = REPO / "frontend" / "package.json"
    assert pkg.exists()
    import json

    data = json.loads(pkg.read_text(encoding="utf-8"))
    assert "vite" in data.get("devDependencies", {})
