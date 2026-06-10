"""Milestone 1.4 — service-layer security hardening tests."""

from __future__ import annotations

import pytest


@pytest.fixture
def client():
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from spacex_model.service.api import app

    return TestClient(app)


def test_serverless_unauth_post_returns_401(client, monkeypatch) -> None:
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.delenv("SPACEX_MODEL_API_KEY", raising=False)
    res = client.post(
        "/api/runs/deterministic", json={"scenario": "base_case", "overrides": {}}
    )
    assert res.status_code == 401
    assert "key" in res.json()["detail"].lower()


def test_serverless_post_with_valid_key(client, monkeypatch) -> None:
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.setenv("SPACEX_MODEL_API_KEY", "test-secret-key")
    res = client.post(
        "/api/runs/deterministic",
        json={"scenario": "base_case", "overrides": {}},
        headers={"X-API-Key": "test-secret-key"},
    )
    # 200 when workbook present, 503 when not — auth must pass either way.
    assert res.status_code in (200, 503)


def test_serverless_get_health_stays_open(client, monkeypatch) -> None:
    monkeypatch.setenv("VERCEL", "1")
    monkeypatch.delenv("SPACEX_MODEL_API_KEY", raising=False)
    res = client.get("/api/health")
    assert res.status_code == 200


def test_scenario_path_traversal_rejected(client) -> None:
    res = client.post(
        "/api/runs/deterministic",
        json={"scenario": "../etc/passwd", "overrides": {}},
    )
    assert res.status_code == 400
    assert "Invalid scenario name" in res.json()["detail"]


@pytest.mark.parametrize("name", ["foo/bar", "foo..bar", ""])
def test_scenario_name_invalid_chars_rejected(client, name: str) -> None:
    res = client.post(
        "/api/runs/deterministic",
        json={"scenario": name, "overrides": {}},
    )
    assert res.status_code in (400, 422)


def test_deterministic_error_detail_sanitized(client, monkeypatch) -> None:
    monkeypatch.setattr(
        "spacex_model.service.api.run_pipeline",
        lambda **kwargs: (_ for _ in ()).throw(KeyError("secret_internal_label")),
    )
    monkeypatch.setattr(
        "spacex_model.service.api.ingest_workbook",
        lambda path: object(),
    )
    monkeypatch.setattr(
        "spacex_model.service.api.assumptions_from_ingest",
        lambda ingest: type(
            "A", (), {"mc_ranges": type("M", (), {"by_label": {}})(), "by_label": {}}
        )(),
    )
    res = client.post(
        "/api/runs/deterministic",
        json={"scenario": "base_case", "overrides": {}, "use_cache": False},
    )
    assert res.status_code == 400
    detail = res.json()["detail"]
    assert detail == "Invalid request parameter"
    assert "secret_internal_label" not in detail


def test_calibration_status_endpoint(client) -> None:
    res = client.get("/api/client/calibration-status")
    assert res.status_code == 200
    body = res.json()
    assert body["pending_count"] == 11
    assert body["calibrated"] is False
    assert "Group Revenue 2025" in body["pending_anchors"]
