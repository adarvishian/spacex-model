"""MC equivalence harness — PRD_MC_Performance_2026-06-05 §3."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from spacex_model.config.constants import SOLVER_TOLERANCE
from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import (
    copy_pipeline_state,
    pipeline_state_from_result,
    run_pipeline,
    run_pipeline_mc,
)
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.inputs.demand_curves import demand_curves_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.mc.aggregator import aggregate_trials, compare_aggregations
from spacex_model.mc.results import TRIAL_METRIC_KEYS, extract_trial_metrics, read_trials_parquet
from spacex_model.mc.runner import McRunConfig, run_mc
from spacex_model.mc.sampler import apply_trial_samples, sample_trial

REPO = Path(__file__).resolve().parents[2]
GOLDEN_DIR = REPO / "tests" / "golden"
GOLDEN_STEM = "mc_baseline_seed42_2000"
PER_TRIAL_SAMPLE = 32


@pytest.fixture(scope="module")
def workbook() -> Path:
    path = get_settings().workbook_path
    if not path.exists():
        pytest.skip(f"Workbook not present: {path}")
    return path


@pytest.fixture(scope="module")
def ingest_bundle(workbook: Path):
    ingest = ingest_workbook(workbook)
    base_assumptions = assumptions_from_ingest(ingest)
    demand = demand_curves_from_ingest(ingest)
    return ingest, base_assumptions, demand


def _golden_paths() -> tuple[Path, Path]:
    return (
        GOLDEN_DIR / f"{GOLDEN_STEM}.parquet",
        GOLDEN_DIR / f"{GOLDEN_STEM}_agg.json",
    )


@pytest.fixture(scope="module")
def golden_agg(workbook: Path):
    _, agg_json = _golden_paths()
    if not agg_json.exists():
        pytest.skip(f"Golden baseline not found: {agg_json}. Run scripts/generate_mc_golden.py")
    return json.loads(agg_json.read_text(encoding="utf-8"))


def _metrics_match(a: dict, b: dict, *, atol: float = 0.0) -> list[str]:
    failures: list[str] = []
    for key in TRIAL_METRIC_KEYS:
        if key in ("converged", "solver_iterations"):
            continue
        va, vb = a.get(key), b.get(key)
        if va is None or vb is None:
            continue
        if isinstance(va, bool) or isinstance(vb, bool):
            if va != vb:
                failures.append(f"{key}: {va} vs {vb}")
            continue
        if not np.isfinite(va) and not np.isfinite(vb):
            continue
        if not np.isclose(va, vb, rtol=0, atol=atol):
            failures.append(f"{key}: {va} vs {vb} (atol={atol})")
    return failures


def test_mc_lite_matches_full_per_trial(workbook: Path, ingest_bundle) -> None:
    """WS-A: MC-lite path produces bit-identical metrics vs full pipeline."""
    ingest, base_assumptions, demand = ingest_bundle
    failures: list[str] = []

    for trial_idx in range(PER_TRIAL_SAMPLE):
        trial = sample_trial(base_assumptions, trial_idx=trial_idx, base_seed=42)
        perturbed = apply_trial_samples(base_assumptions, trial)
        full = run_pipeline(
            assumptions=perturbed,
            ingest=ingest,
            demand_curves=demand,
            write_outputs=False,
        )
        lite = run_pipeline_mc(
            assumptions=perturbed,
            ingest=ingest,
            demand_curves=demand,
        )
        full_m = extract_trial_metrics(full)
        lite_m = extract_trial_metrics(lite)
        failures.extend(_metrics_match(lite_m, full_m))

    assert not failures, "MC-lite divergences:\n" + "\n".join(failures[:20])


def test_warm_start_matches_cold_per_trial(workbook: Path, ingest_bundle) -> None:
    """WS-B: warm-start converges to same fixed point as cold-start."""
    ingest, base_assumptions, demand = ingest_bundle
    base_result = run_pipeline_mc(assumptions=base_assumptions, ingest=ingest, demand_curves=demand)
    warm_state = copy_pipeline_state(pipeline_state_from_result(base_result))
    atol = 10 * SOLVER_TOLERANCE
    failures: list[str] = []
    warm_iters: list[int] = []
    cold_iters: list[int] = []

    for trial_idx in range(PER_TRIAL_SAMPLE):
        trial = sample_trial(base_assumptions, trial_idx=trial_idx, base_seed=42)
        perturbed = apply_trial_samples(base_assumptions, trial)
        cold = run_pipeline_mc(assumptions=perturbed, ingest=ingest, demand_curves=demand)
        warm = run_pipeline_mc(
            assumptions=perturbed,
            ingest=ingest,
            demand_curves=demand,
            initial_state=copy_pipeline_state(warm_state),
        )
        cold_m = extract_trial_metrics(cold)
        warm_m = extract_trial_metrics(warm)
        failures.extend(_metrics_match(warm_m, cold_m, atol=atol))
        warm_iters.append(int(warm_m["solver_iterations"]))
        cold_iters.append(int(cold_m["solver_iterations"]))

    assert not failures, "Warm-start divergences:\n" + "\n".join(failures[:20])
    assert np.mean(warm_iters) <= np.mean(cold_iters), (
        f"Warm-start should not increase iterations: warm={np.mean(warm_iters):.1f} cold={np.mean(cold_iters):.1f}"
    )


@pytest.mark.slow
def test_optimized_mc_matches_golden_aggregate(workbook: Path, golden_agg: dict) -> None:
    """§3.2: optimized MC (lite+warm) stays within tolerance of golden baseline."""
    parquet_path, _ = _golden_paths()
    if not parquet_path.exists():
        pytest.skip(f"Golden parquet not found: {parquet_path}")

    golden_table = read_trials_parquet(parquet_path)
    golden_meta_agg = golden_agg["aggregation"]

    mc = run_mc(
        workbook_path=workbook,
        config=McRunConfig(
            trials=golden_agg["trials"],
            base_seed=golden_agg["base_seed"],
            n_jobs=-1,
            checkpoint_interval=max(100, golden_agg["trials"] // 10),
            sampling="mc",
            warm_start=True,
            mc_lite=True,
            adaptive=False,
            conservation_audit_every=0,
        ),
        run_id="equiv_test",
    )
    cand_table = read_trials_parquet(mc.trials_parquet)

    from spacex_model.engine.pipeline import run_base_case

    base = run_base_case(workbook_path=workbook, write_outputs=False)
    base_metrics = extract_trial_metrics(base)

    golden_agg_obj = aggregate_trials(golden_table, base_metrics=base_metrics, base_seed=golden_agg["base_seed"])
    cand_agg_obj = aggregate_trials(cand_table, base_metrics=base_metrics, base_seed=golden_agg["base_seed"])

    failures = compare_aggregations(cand_agg_obj, golden_agg_obj)
    base_nc = golden_agg["non_convergence_rate"]
    cand_nc = mc.audit["non_convergence_rate"]
    if abs(cand_nc - base_nc) > 0.005:
        failures.append(f"non_convergence_rate: {cand_nc} vs {base_nc}")

    assert not failures, "Aggregate equivalence failures:\n" + "\n".join(failures[:30])


def test_qmc_sampling_produces_valid_trials(workbook: Path, ingest_bundle) -> None:
    """WS-C: QMC path samples without error and converges."""
    ingest, base_assumptions, demand = ingest_bundle
    from spacex_model.mc.sampler import generate_sobol_unit_cube, list_variable_labels

    labels = list_variable_labels(base_assumptions)
    cube = generate_sobol_unit_cube(8, len(labels), base_seed=42)
    for trial_idx in range(8):
        trial = sample_trial(base_assumptions, trial_idx=trial_idx, base_seed=42, sampling="qmc", qmc_point=cube[trial_idx])
        perturbed = apply_trial_samples(base_assumptions, trial)
        result = run_pipeline_mc(assumptions=perturbed, ingest=ingest, demand_curves=demand)
        metrics = extract_trial_metrics(result)
        assert metrics["converged"]


def test_adaptive_stopping_on_golden_replay(golden_agg: dict) -> None:
    """WS-D: adaptive rule would have stopped early on golden prefix."""
    parquet_path, _ = _golden_paths()
    if not parquet_path.exists():
        pytest.skip(f"Golden parquet not found: {parquet_path}")

    from spacex_model.mc.aggregator import running_adaptive_diagnostics

    table = read_trials_parquet(parquet_path)
    ev = np.asarray(table.column("group_ev_2025_b").to_numpy(zero_copy_only=False), dtype=np.float64)
    diag = running_adaptive_diagnostics(
        ev,
        checkpoint_size=200,
        eps=0.0025,
        consecutive=2,
        min_trials=512,
    )
    assert diag["stop_at"] is not None, "Adaptive rule should stabilize before 2000 trials on golden"
    assert diag["stop_at"] < golden_agg["trials"]
