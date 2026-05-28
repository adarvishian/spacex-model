"""Phase F — Monte Carlo engine tests per PRD §8.6."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_base_case
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.inputs.mc_ranges import DistributionType
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.mc.aggregator import aggregate_trials
from spacex_model.mc.distributions import (
    reference_percentiles,
    sample_value,
    scipy_reference_percentiles,
)
from spacex_model.mc.results import extract_trial_metrics, read_trials_parquet
from spacex_model.mc.runner import McRunConfig, run_mc
from spacex_model.mc.sampler import apply_trial_samples, list_variable_labels, sample_trial
from spacex_model.mc.sensitivity import sweep_1d, tornado_sensitivity

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"


@pytest.mark.parametrize(
    ("dist", "base", "low", "high"),
    [
        (DistributionType.TRIANGLE, 10.0, 5.0, 20.0),
        (DistributionType.UNIFORM, 10.0, 5.0, 20.0),
        (DistributionType.LOGNORMAL, 10.0, 6.0, 18.0),
        (DistributionType.DISCRETE, 2027.0, 2026.0, 2028.0),
    ],
)
def test_distribution_percentiles_match_scipy(dist, base, low, high) -> None:
    impl = reference_percentiles(dist, base=base, low=low, high=high, n_samples=20_000, seed=1)
    ref = scipy_reference_percentiles(dist, base=base, low=low, high=high, n_samples=20_000, seed=1)
    for key in ("p10", "p50", "p90"):
        assert impl[key] == pytest.approx(ref[key], rel=0.08), f"{dist} {key}"


def test_fixed_distribution_returns_base() -> None:
    rng = np.random.default_rng(0)
    sv = sample_value(
        DistributionType.FIXED,
        base_case=42.0,
        year_values={},
        mc_min=None,
        mc_max=None,
        rng=rng,
    )
    assert sv.scalar == 42.0


def test_triangle_yearrow_multiplier() -> None:
    rng = np.random.default_rng(7)
    sv = sample_value(
        DistributionType.TRIANGLE_YEARROW,
        base_case=100.0,
        year_values={2025: 100.0, 2026: 200.0},
        mc_min=80.0,
        mc_max=120.0,
        rng=rng,
    )
    assert sv.year_values is not None
    assert 2025 in sv.year_values
    assert sv.year_values[2026] == pytest.approx(2.0 * sv.year_values[2025])


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_sample_trial_reproducible() -> None:
    ingest = ingest_workbook(WORKBOOK)
    assumptions = assumptions_from_ingest(ingest)
    a = sample_trial(assumptions, trial_idx=5, base_seed=99)
    b = sample_trial(assumptions, trial_idx=5, base_seed=99)
    assert a.overrides == b.overrides
    assert len(a.overrides) > 0


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_mc_trial_pipeline_converges() -> None:
    from spacex_model.engine.pipeline import run_pipeline
    from spacex_model.inputs.demand_curves import demand_curves_from_ingest
    from spacex_model.inputs.scenarios import apply_assumption_overrides

    ingest = ingest_workbook(WORKBOOK)
    assumptions = assumptions_from_ingest(ingest)
    perturbed = apply_assumption_overrides(
        assumptions,
        {"TAM inflation rate (annual)": 0.028},
    )
    demand = demand_curves_from_ingest(ingest)
    result = run_pipeline(
        assumptions=perturbed,
        ingest=ingest,
        demand_curves=demand,
        write_outputs=False,
    )
    metrics = extract_trial_metrics(result)
    assert result.solver_trace.converged
    assert np.isfinite(metrics["group_ev_2025_b"])


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_mc_small_run_and_aggregate() -> None:
    mc = run_mc(
        workbook_path=WORKBOOK,
        config=McRunConfig(trials=8, base_seed=1, n_jobs=2, checkpoint_interval=4),
    )
    assert mc.trials_completed == 8
    assert mc.trials_converged >= 1
    assert mc.trials_parquet.exists()
    table = read_trials_parquet(mc.trials_parquet)
    base = run_base_case(workbook_path=WORKBOOK, write_outputs=False)
    agg = aggregate_trials(table, base_metrics=extract_trial_metrics(base))
    assert agg.n_trials == 8
    assert agg.n_converged >= 1
    ev = agg.metrics["group_ev_2025_b"]
    assert ev.p5 <= ev.p50 <= ev.p95
    assert np.isfinite(ev.cvar_5)


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_variable_labels_non_empty() -> None:
    ingest = ingest_workbook(WORKBOOK)
    assumptions = assumptions_from_ingest(ingest)
    labels = list_variable_labels(assumptions)
    assert len(labels) > 50


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_sweep_1d() -> None:
    ingest = ingest_workbook(WORKBOOK)
    assumptions = assumptions_from_ingest(ingest)
    from spacex_model.inputs.demand_curves import demand_curves_from_ingest

    demand = demand_curves_from_ingest(ingest)
    points = sweep_1d(
        assumptions,
        ingest=ingest,
        demand=demand,
        label="TAM inflation rate (annual)",
        grid=[0.02, 0.025, 0.03],
    )
    assert len(points) == 3
    assert all(np.isfinite(p["group_ev_2025_b"]) for p in points)


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
@pytest.mark.slow
def test_tornado_top_one() -> None:
    ingest = ingest_workbook(WORKBOOK)
    assumptions = assumptions_from_ingest(ingest)
    from spacex_model.inputs.demand_curves import demand_curves_from_ingest

    demand = demand_curves_from_ingest(ingest)
    bars = tornado_sensitivity(
        assumptions,
        ingest=ingest,
        demand=demand,
        labels=["TAM inflation rate (annual)"],
        top_n=1,
    )
    assert len(bars) == 1
    assert bars[0].delta >= 0
