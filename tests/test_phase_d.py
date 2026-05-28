"""Phase D — Allocator brain + iterative solver integration tests."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from spacex_model.config.constants import FIRST_YEAR
from spacex_model.engine.conservation import check_allocation_bounds
from spacex_model.engine.pipeline import run_base_case
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"


def _within(actual: float, target: float, tolerance: float) -> bool:
    if target == 0:
        return abs(actual) <= tolerance * 1000
    return abs(actual - target) / abs(target) <= tolerance


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_solver_converges_base_case() -> None:
    result = run_base_case(write_outputs=False)
    assert result.solver_trace.converged
    assert result.solver_trace.iterations < 100
    assert result.solver_trace.max_residual < 0.001


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_allocation_bounds_block_a() -> None:
    result = run_base_case(write_outputs=False)
    bounds = check_allocation_bounds(
        result.allocator.cash,
        result.allocator.available_cash,
    )
    assert bounds.all_ok


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_cash_boy_2025_with_bridge() -> None:
    result = run_base_case(write_outputs=False)
    assert result.allocator.cash_boy.at(FIRST_YEAR) == pytest.approx(25_000.0, rel=0.01)


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_mars_carveout_floor_2025() -> None:
    result = run_base_case(write_outputs=False)
    assert result.group_pnl.mars_carveout.at(FIRST_YEAR) == pytest.approx(1000.0)


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_block_b_group_revenue_2025() -> None:
    result = run_base_case(write_outputs=False)
    rev = result.group_pnl.group_revenue_net.at(FIRST_YEAR)
    assert _within(rev, 14_650.0, 0.05), f"Group revenue 2025: {rev:,.0f}"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_block_b_total_opex_2025() -> None:
    result = run_base_case(write_outputs=False)
    opex = result.group_pnl.total_opex.at(FIRST_YEAR)
    assert _within(opex, 4_476.0, 0.05), f"Total OpEx 2025: {opex:,.0f}"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_block_b_total_capex_2025() -> None:
    result = run_base_case(write_outputs=False)
    capex = result.group_pnl.total_group_capex.at(FIRST_YEAR)
    assert _within(capex, 6_345.0, 0.05), f"Total Group CapEx 2025: {capex:,.0f}"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_block_c_no_nan_or_inf() -> None:
    result = run_base_case(write_outputs=False)
    for name, vec in result.all_year_vectors():
        assert not np.any(np.isnan(vec)), f"{name} contains NaN"
        assert not np.any(np.isinf(vec)), f"{name} contains inf"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_block_c_starship_launches_2025_zero() -> None:
    result = run_base_case(write_outputs=False)
    assert result.starship_launches(FIRST_YEAR) == 0.0


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_odc_zero_deployment_d6() -> None:
    result = run_base_case(write_outputs=False)
    assert result.module_outputs["odc"].total_revenue.at(FIRST_YEAR) == 0.0


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_conservation_r108_ok_all_years() -> None:
    result = run_base_case(write_outputs=False)
    assert result.conservation.all_ok


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_switching_rd_odc_2025() -> None:
    ingest = ingest_workbook(WORKBOOK)
    assumptions = assumptions_from_ingest(ingest)
    result = run_base_case(write_outputs=False)
    from spacex_model.calc.opex import OpExInputs, compute_opex

    opex = compute_opex(
        OpExInputs(assumptions=assumptions, module_outputs=result.module_outputs)
    )
    assert opex.odc_rd.at(FIRST_YEAR) >= 200.0
