"""Sprint R4 gate — reconciliation blocks A/B/C/D + divergence triage vs V4.131."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.config.constants import (
    FIRST_YEAR,
    LAST_YEAR,
    SOLVER_MAX_ITERATIONS,
    SOLVER_TOLERANCE,
)
from spacex_model.config.settings import get_settings
from spacex_model.engine.conservation import (
    check_allocation_bounds,
    check_kg_allocation_bounds,
)
from spacex_model.engine.pipeline import run_base_case
from spacex_model.inputs.block_b_anchors import BLOCK_B_CALIBRATION_PENDING_BUDGET
from spacex_model.inputs.v4_131_2025_anchors import V4_131_INGEST_ANCHORS_2025
from spacex_model.io.divergence import build_divergence_report, finalize_triage
from spacex_model.linters.assumption_defaults import find_assumption_scalar_defaults
from spacex_model.linters.architecture_coverage import (
    find_uncovered_architecture_sections,
)
from spacex_model.linters.docstrings import find_missing_docstring_tags
from spacex_model.testing.block_b_anchors import (
    BLOCK_B_CALIBRATION_PENDING,
    load_block_b_anchors_v1,
)

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = get_settings().workbook_path


@pytest.fixture(scope="module")
def base_case():
    if not WORKBOOK.exists():
        pytest.skip("V4.131 workbook not present")
    return run_base_case(WORKBOOK, write_outputs=False)


def test_r4_workbook_is_v4_131() -> None:
    assert WORKBOOK.name == "SpaceX V4.131.xlsx"
    assert WORKBOOK.exists()


def test_r4_block_a_solver_contract(base_case) -> None:
    trace = base_case.solver_trace
    assert trace.converged
    assert trace.iterations < SOLVER_MAX_ITERATIONS
    assert trace.max_residual < SOLVER_TOLERANCE


def test_r4_block_a_allocation_bounds(base_case) -> None:
    cash_bounds = check_allocation_bounds(
        base_case.allocator.cash,
        base_case.allocator.available_cash,
    )
    kg_bounds = check_kg_allocation_bounds(
        base_case.allocator.kg,
        base_case.allocator.capacity_available_kg,
    )
    assert cash_bounds.all_ok
    assert kg_bounds.all_ok


def test_r4_block_a_conservation_all_years(base_case) -> None:
    assert base_case.conservation.all_ok
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        assert base_case.conservation.r108_ok_by_year[year] == "OK"


def test_r4_block_b_ingest_anchors(base_case) -> None:
    """V4.131 Assumptions 2025 frozen anchors (PRD §1 / §2)."""
    for anchor in V4_131_INGEST_ANCHORS_2025:
        if not anchor.assumptions_label:
            continue
        row = base_case.assumptions.by_label[anchor.assumptions_label]
        actual = row.scalar()
        if actual is None and row.year_values.get(FIRST_YEAR) is not None:
            actual = float(row.year_values[FIRST_YEAR])
        if anchor.tolerance_pct == 0:
            assert actual == pytest.approx(anchor.target)
        else:
            assert actual == pytest.approx(anchor.target, rel=anchor.tolerance_pct)


def test_r4_block_b_pending_budget_shrink_only() -> None:
    """Pending anchor list may shrink but must not grow without explicit budget approval (M1.2)."""
    assert len(BLOCK_B_CALIBRATION_PENDING) <= BLOCK_B_CALIBRATION_PENDING_BUDGET
    assert BLOCK_B_CALIBRATION_PENDING_BUDGET == 11


def test_r4_block_b_s1_hard_anchors(base_case) -> None:
    """Non-xfail S-1 disclosure anchors that must halt if broken."""
    for anchor in load_block_b_anchors_v1():
        if anchor.name in BLOCK_B_CALIBRATION_PENDING:
            continue
        actual = base_case.lookup_anchor(anchor.name)
        assert (
            anchor.halt_low <= actual <= anchor.halt_high
        ), f"{anchor.name}: {actual} not in [{anchor.halt_low}, {anchor.halt_high}]"


def test_r4_block_c_no_nan_inf(base_case) -> None:
    import numpy as np

    for name, vec in base_case.all_year_vectors():
        assert not np.any(np.isnan(vec)), name
        assert not np.any(np.isinf(vec)), name


def test_r4_block_d_docstrings() -> None:
    violations = find_missing_docstring_tags()
    assert violations == [], "\n".join(violations[:20])


def test_r4_block_d_architecture_coverage() -> None:
    uncovered = find_uncovered_architecture_sections()
    assert uncovered == [], f"Uncovered sections: {uncovered}"


def test_r4_block_d_no_assumption_scalar_defaults() -> None:
    violations = find_assumption_scalar_defaults()
    assert violations == [], "\n".join(violations[:20])


def test_r4_divergence_all_triaged(base_case) -> None:
    """Every mapped divergence classified — no open type-A or type-D."""
    report = finalize_triage(build_divergence_report(base_case), base_case)
    assert report.mapped_count > 0
    assert len(report.open_type_a) == 0
    assert len(report.open_type_d) == 0
    untriaged_open = [
        e for e in report.entries if not e.within_tolerance and e.triage.value == "open"
    ]
    assert untriaged_open == []


def test_r4_defects_f1_f6_documented_not_fixed(base_case) -> None:
    """R4 reproduces known allocator defects — remediation is U0–U4 scope."""
    alloc = base_case.allocator
    # F4: fixed in Python U0 (total ≡ memo); xlsx cached CAE may still diverge
    assert alloc.total_desired_launch_kg is not None
    assert alloc.memo_total_kg_demand is not None
    assert alloc.capacity_available_kg is not None
    # F5: ODC debt draw field present (bypass spine — as-is R2/R3)
    assert hasattr(alloc, "debt_odc_draw")
    # F6: R14 facility-flow identity repaired in U4
    assert base_case.conservation.r14_ok
    assert base_case.conservation.all_ok
