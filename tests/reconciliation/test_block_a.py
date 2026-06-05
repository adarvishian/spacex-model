"""Block A structural invariant tests — PRD §7.1 / §10.3."""

from __future__ import annotations

import pytest

from spacex_model.calc.allocator.priority import FourProgramIrrs
from spacex_model.calc.allocator.two_resource_fill import FourProgramDemands, compute_two_resource_fill
from spacex_model.calc.allocator.two_resource_fill import kg_per_ship_year
from spacex_model.calc.launch_capacity import LaunchCapacityInputs, compute_launch_capacity
from spacex_model.config.constants import (
    FIRST_YEAR,
    LAST_YEAR,
    SOLVER_MAX_ITERATIONS,
    SOLVER_TOLERANCE,
)
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.conservation import check_allocation_bounds, check_kg_allocation_bounds
from spacex_model.engine.pipeline import ModelResult


def test_solver_converges(model_result: ModelResult) -> None:
    """V4.113 contract: queue gate converges within 1000 iter @ 1e-7 (PRD §2.2)."""
    assert model_result.solver_trace.converged
    assert model_result.solver_trace.iterations < SOLVER_MAX_ITERATIONS
    assert model_result.solver_trace.max_residual < SOLVER_TOLERANCE


def test_allocation_bounds(model_result: ModelResult) -> None:
    bounds = check_allocation_bounds(
        model_result.allocator.cash,
        model_result.allocator.available_cash,
    )
    assert bounds.all_ok


def test_kg_allocation_bounds(model_result: ModelResult) -> None:
    bounds = check_kg_allocation_bounds(
        model_result.allocator.kg,
        model_result.allocator.capacity_available_kg,
    )
    assert bounds.all_ok


def test_cash_boy_2025_without_bridge(model_result: ModelResult) -> None:
    # P1-1: bridge moved to 2026; 2025 Cash BoY = S-1 starting cash only
    assert model_result.allocator.cash_boy.at(FIRST_YEAR) == pytest.approx(11_385.0, rel=0.01)


def test_cash_boy_2026_with_bridge(model_result: ModelResult) -> None:
    # P1-1: $20B bridge receipt in 2026 (MDA §6.5)
    assert model_result.allocator.cash_boy.at(2026) >= 11_385.0


def test_mars_carveout_floor_2025(model_result: ModelResult) -> None:
    assert model_result.group_pnl.mars_carveout.at(FIRST_YEAR) == pytest.approx(1000.0)


def test_conservation_all_ok_all_years(model_result: ModelResult) -> None:
    """Conservation tab ALL-OK equivalent every year 2025–2040."""
    assert model_result.conservation.all_ok
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        assert model_result.conservation.r108_ok_by_year[year] == "OK"


def test_audit_outputs_hash_and_peak_memory(model_result: ModelResult) -> None:
    assert "outputs_hash" in model_result.audit
    assert len(model_result.audit["outputs_hash"]) == 64
    assert model_result.audit["peak_memory_mb"] > 0


def test_negative_irr_module_receives_floor_only_cash_allocation() -> None:
    """Negative-IRR program limited to soft floor (D1) — not full pool share."""
    from spacex_model.inputs.assumptions import assumptions_from_ingest
    from spacex_model.io.excel_ingest import ingest_workbook
    from spacex_model.config.settings import get_settings

    assumptions = assumptions_from_ingest(ingest_workbook(get_settings().workbook_path))
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    pool = YearVector.constant(10_000.0)
    prior = FourProgramIrrs(
        starlink=YearVector.constant(0.40),
        odc=YearVector.constant(-0.05),
        terrestrial=YearVector.constant(0.20),
        customer_launch=YearVector.constant(0.30),
    )
    four_dem = FourProgramDemands(
        cash_caps=prior,
        kg=FourProgramIrrs.zeros(),
    )
    fill = compute_two_resource_fill(
        pool,
        four_dem,
        prior,
        assumptions,
        gigabay_throughput=YearVector.zeros(),
        kg_per_ship_yr=kg_per_ship_year(assumptions, lc.per_launch_upmass_kg),
    )
    odc_alloc = fill.allocated_cash.odc.at(2030)
    cl_alloc = fill.allocated_cash.customer_launch.at(2030)
    assert odc_alloc <= pool.at(2030) * 0.06 + 1.0
    assert cl_alloc > odc_alloc
