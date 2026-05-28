"""Hypothesis-driven Block A invariant tests per PRD §7.5 / §10.9."""

from __future__ import annotations

import os
from pathlib import Path

import hypothesis
import hypothesis.strategies as st
import pytest

from spacex_model.config.constants import CONSERVATION_RESIDUAL_TOLERANCE_MM, FIRST_YEAR, LAST_YEAR
from spacex_model.engine.conservation import check_allocation_bounds
from spacex_model.engine.iterative_solver import NonConvergenceError
from spacex_model.engine.pipeline import run_pipeline
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.inputs.scenarios import apply_assumption_overrides
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.mc.sampler import list_variable_labels

REPO = Path(__file__).resolve().parents[2]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"

HYPOTHESIS_MAX_EXAMPLES = int(os.environ.get("HYPOTHESIS_MAX_EXAMPLES", "200"))
HYPOTHESIS_DEADLINE_MS = int(os.environ.get("HYPOTHESIS_DEADLINE_MS", "10000"))

_PERTURBABLE_SCALAR_LABELS = (
    "TAM inflation rate (annual)",
    "Real GNI growth rate (% per year)",
    "Mars carve-out % of prior-year Group FCF",
    "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)",
    "Tax rate (corporate, US federal + state blended)",
)

_BASE_ASSUMPTIONS = None
_MC_LABELS: tuple[str, ...] = ()
if WORKBOOK.exists():
    _ingest = ingest_workbook(WORKBOOK)
    _BASE_ASSUMPTIONS = assumptions_from_ingest(_ingest)
    _MC_LABELS = tuple(list_variable_labels(_BASE_ASSUMPTIONS))


@st.composite
def valid_assumptions_perturbation(draw: st.DrawFn) -> dict[str, float | dict[int, float]]:
    """Scale scalar and year-row Assumptions per PRD §7.5."""
    overrides: dict[str, float | dict[int, float]] = {}
    for label in _PERTURBABLE_SCALAR_LABELS:
        overrides[label] = draw(st.floats(min_value=0.9, max_value=1.1))

    if _MC_LABELS:
        picked = draw(st.lists(st.sampled_from(_MC_LABELS), min_size=1, max_size=3, unique=True))
        base = _BASE_ASSUMPTIONS
        assert base is not None
        for label in picked:
            row = base.by_label.get(label)
            if row is None:
                continue
            if row.year_values:
                year_overrides: dict[int, float] = {}
                for year in range(FIRST_YEAR, LAST_YEAR + 1):
                    val = row.year_values.get(year)
                    if isinstance(val, (int, float)):
                        year_overrides[year] = float(val) * draw(
                            st.floats(min_value=0.95, max_value=1.05)
                        )
                if year_overrides:
                    overrides[label] = year_overrides
            else:
                val = row.scalar()
                if val is not None:
                    overrides[label] = val * draw(st.floats(min_value=0.95, max_value=1.05))
    return overrides


def _apply_perturbation(base, overrides: dict[str, float | dict[int, float]]):
    resolved: dict[str, float | dict[int, float]] = {}
    for label, perturb in overrides.items():
        row = base.by_label.get(label)
        if row is None:
            continue
        if isinstance(perturb, dict):
            resolved[label] = perturb
            continue
        if not isinstance(perturb, float):
            continue
        val = row.scalar()
        if val is not None:
            resolved[label] = val * perturb
    return apply_assumption_overrides(base, resolved)


def _run_perturbed(overrides: dict[str, float | dict[int, float]]):
    assert _BASE_ASSUMPTIONS is not None
    perturbed = _apply_perturbation(_BASE_ASSUMPTIONS, overrides)
    result = run_pipeline(workbook_path=WORKBOOK, assumptions=perturbed, write_outputs=False)
    return result, perturbed


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
@pytest.mark.slow
@hypothesis.given(overrides=valid_assumptions_perturbation())
@hypothesis.settings(
    max_examples=HYPOTHESIS_MAX_EXAMPLES,
    deadline=HYPOTHESIS_DEADLINE_MS,
    suppress_health_check=[hypothesis.HealthCheck.too_slow],
)
def test_conservation_holds_under_perturbation(
    overrides: dict[str, float | dict[int, float]],
) -> None:
    """Block A invariants hold under valid Assumptions perturbations."""
    try:
        result, _ = _run_perturbed(overrides)
    except NonConvergenceError:
        hypothesis.assume(False)

    bounds = check_allocation_bounds(result.allocator.cash, result.allocator.available_cash)
    assert result.conservation.all_ok, f"R108 broken under perturbation {overrides}"
    assert bounds.all_ok, f"Allocation bounds broken under perturbation {overrides}"

    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        for check_row, by_year in result.conservation.residuals_by_check.items():
            if check_row in ("R109", "R110"):
                continue
            residual = by_year.get(year, 0.0)
            assert abs(residual) < CONSERVATION_RESIDUAL_TOLERANCE_MM, (
                f"{check_row} {year}: {residual} under {overrides}"
            )
