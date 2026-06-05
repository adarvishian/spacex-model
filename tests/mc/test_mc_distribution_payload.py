"""Sprint 5 — MC distribution payload (histogram, FCF fan, provenance)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_base_case
from spacex_model.mc.aggregator import (
    aggregate_trials,
    build_group_ev_histogram,
    build_group_fcf_fan,
    summarize_metric,
)
from spacex_model.mc.results import FCF_FAN_PERCENTILES, extract_trial_metrics, read_trials_parquet
from spacex_model.mc.runner import McRunConfig, run_mc
from spacex_model.service.serializers import serialize_mc_aggregation

REPO = Path(__file__).resolve().parents[2]
MC_ARTIFACT = REPO / "frontend" / "public" / "data" / "base_case_mc.json"
BASE_SEED = 42
SMALL_TRIALS = 16


@pytest.fixture(scope="module")
def workbook() -> Path:
    path = get_settings().workbook_path
    if not path.exists():
        pytest.skip(f"Workbook not present: {path}")
    return path


@pytest.fixture(scope="module")
def small_mc_run(workbook: Path) -> tuple[object, dict[str, float]]:
    cfg = McRunConfig(
        trials=SMALL_TRIALS,
        base_seed=BASE_SEED,
        n_jobs=2,
        checkpoint_interval=8,
    )
    mc = run_mc(workbook_path=workbook, config=cfg)
    table = read_trials_parquet(mc.trials_parquet)
    base = run_base_case(workbook_path=workbook, write_outputs=False)
    base_metrics = extract_trial_metrics(base)
    return table, base_metrics


def test_aggregation_exposes_histogram_fan_and_provenance(small_mc_run) -> None:
    table, base_metrics = small_mc_run
    agg = aggregate_trials(table, base_metrics=base_metrics, base_seed=BASE_SEED)
    payload = serialize_mc_aggregation(agg)

    assert payload["n_trials"] == SMALL_TRIALS
    assert payload["n_converged"] >= 1
    assert payload["base_seed"] == BASE_SEED
    assert payload["convergence_status"] in {"converged", "partial", "failed"}

    hist = payload["group_ev_histogram"]
    assert hist["metric"] == "group_ev_2025_b"
    assert len(hist["bin_edges"]) == hist["n_bins"] + 1
    assert len(hist["counts"]) == hist["n_bins"]
    assert sum(hist["counts"]) == agg.n_converged

    fan = payload["group_fcf_fan"]
    assert fan["years"] == list(range(FIRST_YEAR, LAST_YEAR + 1))
    for key in ("p5", "p25", "p50", "p75", "p95"):
        assert len(fan[key]) == len(fan["years"])
    assert len(fan["base_case"]) == len(fan["years"])


def test_histogram_matches_engine_values(small_mc_run) -> None:
    table, base_metrics = small_mc_run
    agg = aggregate_trials(table, base_metrics=base_metrics, base_seed=BASE_SEED)
    ev_summary = agg.metrics["group_ev_2025_b"]

    mask = table.column("converged").to_numpy(zero_copy_only=False)
    ev_col = table.column("group_ev_2025_b").to_numpy(zero_copy_only=False)
    arr = np.asarray(ev_col, dtype=np.float64)
    arr = arr[np.array([bool(x) for x in mask], dtype=bool)]
    arr = arr[np.isfinite(arr)]

    hist = build_group_ev_histogram(arr)
    assert hist is not None
    assert sum(hist.counts) == arr.size

    base_ev = base_metrics.get("group_ev_2025_b")
    manual = summarize_metric(arr, metric="group_ev_2025_b", base_case=base_ev)
    assert ev_summary.p50 == pytest.approx(manual.p50)
    assert ev_summary.p5 == pytest.approx(manual.p5)
    assert ev_summary.p95 == pytest.approx(manual.p95)
    assert ev_summary.cvar_5 == pytest.approx(manual.cvar_5)


def test_fcf_fan_percentiles_match_manual(small_mc_run) -> None:
    table, base_metrics = small_mc_run
    mask_col = table.column("converged").to_numpy(zero_copy_only=False)
    mask = np.array([bool(x) for x in mask_col], dtype=bool)

    fan = build_group_fcf_fan(table, mask=mask, base_metrics=base_metrics)
    assert fan is not None

    year = 2030
    key = f"group_fcf_{year}_mm"
    arr = np.asarray(table.column(key).to_numpy(zero_copy_only=False), dtype=np.float64)[mask]
    clean = arr[np.isfinite(arr)]
    pct = np.percentile(clean, FCF_FAN_PERCENTILES)
    idx = fan.years.index(year)
    assert fan.p50[idx] == pytest.approx(float(pct[2]))
    assert fan.p5[idx] == pytest.approx(float(pct[0]))
    assert fan.p95[idx] == pytest.approx(float(pct[4]))


@pytest.mark.skipif(not MC_ARTIFACT.exists(), reason="base_case_mc.json not precomputed")
def test_precache_artifact_has_distribution_payload() -> None:
    import json

    data = json.loads(MC_ARTIFACT.read_text(encoding="utf-8"))
    assert data["base_seed"] == BASE_SEED
    assert data["trials"] >= 1
    agg = data["aggregation"]
    assert "group_ev_histogram" in agg
    assert "group_fcf_fan" in agg
    assert agg["n_trials"] == data["trials"]
    ev = agg["metrics"]["group_ev_2025_b"]
    assert ev["p5"] <= ev["p50"] <= ev["p95"]
