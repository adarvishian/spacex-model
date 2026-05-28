"""Reconciliation harness — stress scenarios + divergence per Phase E."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from spacex_model.config.settings import get_settings
from spacex_model.engine.conservation import check_allocation_bounds
from spacex_model.engine.pipeline import ModelResult, run_pipeline
from spacex_model.io.divergence import DivergenceReport, build_divergence_report, finalize_triage

STRESS_SCENARIOS: tuple[str, ...] = ("base_case", "bear", "bull", "mars_share")


@dataclass
class ReconciliationHarnessResult:
    """Aggregate result from Phase E reconciliation harness."""

    scenario_results: dict[str, ModelResult] = field(default_factory=dict)
    divergence: DivergenceReport | None = None
    stress_convergence: dict[str, bool] = field(default_factory=dict)
    stress_block_a: dict[str, bool] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    @property
    def all_stress_converged(self) -> bool:
        return all(self.stress_convergence.values())

    @property
    def all_stress_block_a(self) -> bool:
        return all(self.stress_block_a.values())

    @property
    def zero_open_triage_a_or_d(self) -> bool:
        if self.divergence is None:
            return False
        return len(self.divergence.open_type_a) == 0 and len(self.divergence.open_type_d) == 0

    def summary(self) -> dict[str, Any]:
        return {
            "scenarios_run": list(self.scenario_results.keys()),
            "stress_convergence": self.stress_convergence,
            "stress_block_a": self.stress_block_a,
            "divergence_matching": self.divergence.matching_count if self.divergence else 0,
            "divergence_diverging": self.divergence.diverging_count if self.divergence else 0,
            "open_type_a": len(self.divergence.open_type_a) if self.divergence else 0,
            "open_type_d": len(self.divergence.open_type_d) if self.divergence else 0,
            "errors": self.errors,
        }


def run_reconciliation_harness(
    *,
    scenarios: tuple[str, ...] = STRESS_SCENARIOS,
    write_outputs: bool = False,
) -> ReconciliationHarnessResult:
    """Run Base Case + stress scenarios; build divergence report from Base Case."""
    settings = get_settings()
    harness = ReconciliationHarnessResult()
    base_result: ModelResult | None = None

    for name in scenarios:
        scenario_path = settings.scenarios_dir / f"{name}.yaml"
        if not scenario_path.exists():
            harness.errors.append(f"Missing scenario file: {scenario_path}")
            continue
        try:
            result = run_pipeline(scenario_path=scenario_path, write_outputs=write_outputs)
            harness.scenario_results[name] = result
            bounds = check_allocation_bounds(result.allocator.cash, result.allocator.available_cash)
            harness.stress_convergence[name] = result.solver_trace.converged
            harness.stress_block_a[name] = result.conservation.all_ok and bounds.all_ok
            if name == "base_case":
                base_result = result
        except Exception as exc:  # noqa: BLE001 — harness collects errors
            harness.errors.append(f"{name}: {exc}")
            harness.stress_convergence[name] = False
            harness.stress_block_a[name] = False

    if base_result is not None:
        report = build_divergence_report(base_result)
        harness.divergence = finalize_triage(report, base_result)

    return harness
