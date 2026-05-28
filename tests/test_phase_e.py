"""Phase E — reconciliation hardening + divergence report tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_pipeline
from spacex_model.engine.reconciliation import STRESS_SCENARIOS, run_reconciliation_harness
from spacex_model.inputs.scenarios import apply_assumption_overrides, load_scenario
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.inputs.assumptions import assumptions_from_ingest

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
@pytest.mark.parametrize("scenario_name", STRESS_SCENARIOS)
def test_stress_scenario_converges(scenario_name: str) -> None:
    """Each stress scenario converges with Block A passing."""
    settings = get_settings()
    path = settings.scenarios_dir / f"{scenario_name}.yaml"
    result = run_pipeline(scenario_path=path, write_outputs=False)
    assert result.solver_trace.converged
    assert result.solver_trace.iterations < 100
    assert result.solver_trace.max_residual < 0.001
    assert result.conservation.all_ok


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_scenario_overrides_apply() -> None:
    ingest = ingest_workbook(WORKBOOK)
    base = assumptions_from_ingest(ingest)
    spec = load_scenario(get_settings().scenarios_dir / "bear.yaml")
    updated = apply_assumption_overrides(base, spec.overrides)
    mars_pct = updated.lookup_scalar("Mars carve-out % of prior-year Group FCF")
    assert mars_pct == pytest.approx(0.25)


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_mars_share_scenario_higher_carveout_pct() -> None:
    ingest = ingest_workbook(WORKBOOK)
    base = assumptions_from_ingest(ingest)
    spec = load_scenario(get_settings().scenarios_dir / "mars_share.yaml")
    updated = apply_assumption_overrides(base, spec.overrides)
    assert updated.lookup_scalar("Mars carve-out % of prior-year Group FCF") == pytest.approx(0.35)


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_reconciliation_harness_pass() -> None:
    harness = run_reconciliation_harness(write_outputs=False)
    assert not harness.errors
    assert harness.all_stress_converged
    assert harness.all_stress_block_a
    assert harness.zero_open_triage_a_or_d
    assert harness.divergence is not None
    assert harness.divergence.mapped_count > 100
