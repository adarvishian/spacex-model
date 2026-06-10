"""Milestone 1.4 — serverless smoke: ingest, deterministic run, MC polls, lineage history."""

from __future__ import annotations

import os
import stat
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
WORKBOOK = REPO / "SpaceX V4.131.xlsx"


@pytest.fixture
def serverless_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("SPACEX_MODEL_API_KEY", "test-serverless-key")
    monkeypatch.setenv("SPACEX_MODEL_OUTPUTS_DIR", str(tmp_path / "outputs"))
    monkeypatch.delenv("SPACEX_MODEL_CELL_HISTORY_DIR", raising=False)

    from spacex_model.io import excel_ingest
    from spacex_model.service import jobs as jobs_mod

    excel_ingest._ingest_cache.clear()
    jobs_mod._manager = None


@pytest.fixture
def serverless_client(serverless_env: None):
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from spacex_model.service.api import app

    return TestClient(app)


def test_cell_history_write_dir_routes_to_tmp_on_serverless(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.delenv("SPACEX_MODEL_CELL_HISTORY_DIR", raising=False)

    from spacex_model.io.snapshot_store import cell_history_read_dir, cell_history_write_dir

    assert cell_history_write_dir() == Path("/tmp/spacex_model/cell_history")
    assert cell_history_read_dir().name == "cell_history"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V4.131 workbook not present")
def test_ingest_succeeds_when_repo_data_is_readonly(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """MC-2 guard: cell history must not write under read-only repo root."""
    readonly_root = tmp_path / "repo"
    readonly_root.mkdir()
    (readonly_root / "scenarios").mkdir()
    (readonly_root / "pyproject.toml").write_text("[project]\nname = 'test'\n", encoding="utf-8")
    data_dir = readonly_root / "data" / "cell_history"
    data_dir.mkdir(parents=True)
    os.chmod(data_dir, stat.S_IRUSR | stat.S_IXUSR)

    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("SPACEX_MODEL_REPO_ROOT", str(readonly_root))
    monkeypatch.delenv("SPACEX_MODEL_CELL_HISTORY_DIR", raising=False)

    from spacex_model.io import excel_ingest

    excel_ingest._ingest_cache.clear()

    from spacex_model.io.excel_ingest import ingest_workbook
    from spacex_model.io.snapshot_store import cell_history_write_dir

    assert cell_history_write_dir().as_posix().startswith("/tmp/spacex_model/")
    result = ingest_workbook(WORKBOOK)
    assert result.workbook_path == WORKBOOK


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V4.131 workbook not present")
def test_ingest_cell_history_failure_is_non_fatal(monkeypatch: pytest.MonkeyPatch) -> None:
    from spacex_model.io import excel_ingest

    excel_ingest._ingest_cache.clear()

    def _raise_oserror(*args, **kwargs):
        raise OSError("Read-only file system")

    monkeypatch.setattr(
        "spacex_model.io.snapshot_store.record_ingest_changes",
        _raise_oserror,
    )

    from spacex_model.io.excel_ingest import ingest_workbook

    result = ingest_workbook(WORKBOOK)
    assert result.workbook_path == WORKBOOK


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V4.131 workbook not present")
@pytest.mark.slow
def test_serverless_api_smoke_deterministic_mc_lineage(serverless_client) -> None:
    headers = {"X-API-Key": "test-serverless-key"}

    det = serverless_client.post(
        "/api/runs/deterministic",
        json={"scenario": "base_case", "overrides": {}, "use_cache": False},
        headers=headers,
    )
    assert det.status_code == 200, det.text
    body = det.json()
    assert body["run_id"]
    assert body["valuation"]["group_ev_2025_b"] > 0

    mc = serverless_client.post(
        "/api/runs/mc",
        json={"trials": 3, "base_seed": 42, "n_jobs": 1, "include_tornado": False},
        headers=headers,
    )
    assert mc.status_code == 200, mc.text
    assert mc.json().get("execution") == "batched"
    job_id = mc.json()["job_id"]

    poll_body: dict = {}
    status = "queued"
    deadline = time.monotonic() + 120.0
    while time.monotonic() < deadline:
        poll = serverless_client.get(f"/api/runs/mc/{job_id}", headers=headers)
        assert poll.status_code == 200, poll.text
        poll_body = poll.json()
        status = poll_body["status"]
        if status in ("completed", "failed"):
            break
        time.sleep(0.25)

    assert status == "completed", poll_body
    assert poll_body["progress"]["trials_done"] == 3

    hist = serverless_client.get(
        "/api/lineage/group.group_revenue_net/history",
        headers=headers,
    )
    assert hist.status_code == 200
    assert "entries" in hist.json()
