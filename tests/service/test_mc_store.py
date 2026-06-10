"""Serverless MC store — JSON context and parquet append."""

from __future__ import annotations

import json
from pathlib import Path

import pyarrow.parquet as pq

from spacex_model.mc.results import TRIAL_METRIC_KEYS, append_trials_parquet
from spacex_model.service import mc_store


def _sample_row(trial_idx: int) -> dict:
    row: dict = {"trial_idx": trial_idx, "converged": True, "solver_iterations": 100}
    for key in TRIAL_METRIC_KEYS:
        if key not in row:
            row[key] = float(trial_idx)
    return row


def test_context_is_json_not_pickle(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SPACEX_MODEL_OUTPUTS_DIR", str(tmp_path))
    job_id = mc_store.create_serverless_job(
        trials=1,
        base_seed=1,
        scenario_name="base_case",
        include_tornado=False,
        tornado_top=5,
        workbook_path=Path("/tmp/fake.xlsx"),
    )
    ctx_path = tmp_path / "jobs" / job_id / "context.json"
    mc_store._save_context(job_id, Path(__file__))
    assert ctx_path.exists()
    payload = json.loads(ctx_path.read_text(encoding="utf-8"))
    assert "workbook_path" in payload
    assert "workbook_mtime" in payload
    assert not (tmp_path / "jobs" / job_id / "context.pkl").exists()


def test_append_trials_avoids_pylist_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "trials.parquet"
    append_trials_parquet([_sample_row(0)], path)
    append_trials_parquet([_sample_row(1)], path)
    table = pq.read_table(path)
    assert table.num_rows == 2
