"""Block A structural invariant tests — PRD §7.1 / §10.3."""

from __future__ import annotations

import pytest

from spacex_model.calc.allocator.sigmoid_cash import compute_sigmoid_cash_allocations
from spacex_model.calc.allocator.types import QueueSubBlockDemands, QueueSubBlockIrrs
from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.conservation import check_allocation_bounds, check_kg_allocation_bounds
from spacex_model.engine.pipeline import ModelResult


def test_solver_converges(model_result: ModelResult) -> None:
    assert model_result.solver_trace.converged
    assert model_result.solver_trace.iterations < 115
    assert model_result.solver_trace.max_residual < 0.001


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


def test_conservation_r108_ok_all_years(model_result: ModelResult) -> None:
    assert model_result.conservation.all_ok
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        assert model_result.conservation.r108_ok_by_year[year] == "OK"


def test_audit_outputs_hash_and_peak_memory(model_result: ModelResult) -> None:
    assert "outputs_hash" in model_result.audit
    assert len(model_result.audit["outputs_hash"]) == 64
    assert model_result.audit["peak_memory_mb"] > 0


def test_negative_irr_module_receives_zero_cash_allocation() -> None:
    """Blended IRR ≤ 0 → zero cash allocation every year (PRD §7.1 strict cutoff)."""
    z = YearVector.zeros()
    odc_demand = YearVector.constant(5000.0)
    positive = YearVector.constant(0.25)
    negative = YearVector.constant(-0.01)
    demands = QueueSubBlockDemands(
        customer_launch_cash=positive,
        starlink_v2_bb_cash=z,
        starlink_v2_dtc_cash=z,
        starlink_v3_bb_cash=z,
        starlink_v3_dtc_cash=z,
        odc_cash=odc_demand,
        ai_stack_cash=z,
        customer_launch_kg=z,
        starlink_v3_bb_kg=z,
        starlink_v3_dtc_kg=z,
        odc_kg=z,
        ai_stack_kg=z,
    )
    irrs = QueueSubBlockIrrs(
        customer_launch=positive,
        starlink_v2_bb=positive,
        starlink_v2_dtc=positive,
        starlink_v3_bb=positive,
        starlink_v3_dtc=positive,
        odc=negative,
        ai_stack=positive,
    )
    available = YearVector.constant(10_000.0)
    alloc = compute_sigmoid_cash_allocations(available, demands, irrs)
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        assert alloc.odc.at(year) == 0.0
        assert alloc.customer_launch.at(year) > 0.0
