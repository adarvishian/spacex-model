"""Milestone 2.2 — unit tests for decomposed pipeline stages.

Skipped when pipeline is on the pre-05c34af monolithic pass (M1.3 convergence revert).
"""

from __future__ import annotations

import pytest

from spacex_model.calc.allocator.types import CashAllocations, KgAllocations
from spacex_model.config.settings import get_settings
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine import pipeline as pipeline_mod
from spacex_model.engine.pipeline import PipelineState, _blend_allocations, _zero_initial_pipeline
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.io.excel_ingest import clear_ingest_cache, ingest_workbook

_pass_blend_context = getattr(pipeline_mod, "_pass_blend_context", None)
_pass_capacity_layer = getattr(pipeline_mod, "_pass_capacity_layer", None)
HAS_DECOMPOSED_STAGES = _pass_blend_context is not None and _pass_capacity_layer is not None

decomposed_stages = pytest.mark.skipif(
    not HAS_DECOMPOSED_STAGES,
    reason="Pipeline lacks decomposed stages (M1.3 cc78fcf revert)",
)


@pytest.fixture
def assumptions():
    path = get_settings().workbook_path
    if not path.exists():
        pytest.skip(f"Workbook not present: {path}")
    clear_ingest_cache()
    return assumptions_from_ingest(ingest_workbook(path))


def test_blend_allocations_returns_prior_when_no_blend() -> None:
    prior = _zero_initial_pipeline()
    cash, kg = _blend_allocations(prior, None)
    assert cash is prior.cash_alloc
    assert kg is prior.kg_alloc


def test_blend_allocations_applies_monitored_blend() -> None:
    prior = _zero_initial_pipeline()
    blend = {
        "cash.starlink_v2_bb": prior.cash_alloc.starlink_v2_bb.values * 0.5,
        "cash.starlink_v2_dtc": prior.cash_alloc.starlink_v2_dtc.values,
        "cash.starlink_v3_bb": prior.cash_alloc.starlink_v3_bb.values,
        "cash.starlink_v3_dtc": prior.cash_alloc.starlink_v3_dtc.values,
        "cash.odc": prior.cash_alloc.odc.values,
        "cash.ai_stack": prior.cash_alloc.ai_stack.values,
        "cash.customer_launch": prior.cash_alloc.customer_launch.values,
        "kg.starlink_v3_bb": prior.kg_alloc.starlink_v3_bb.values,
        "kg.starlink_v3_dtc": prior.kg_alloc.starlink_v3_dtc.values,
        "kg.odc": prior.kg_alloc.odc.values,
        "kg.ai_stack": prior.kg_alloc.ai_stack.values,
        "kg.customer_launch": prior.kg_alloc.customer_launch.values,
    }
    cash, kg = _blend_allocations(prior, blend)
    assert isinstance(cash, CashAllocations)
    assert isinstance(kg, KgAllocations)
    assert cash.starlink_v2_bb.at(2025) == pytest.approx(
        prior.cash_alloc.starlink_v2_bb.at(2025) * 0.5
    )


@decomposed_stages
def test_pass_blend_context_produces_solver_fields(assumptions) -> None:
    prior = _zero_initial_pipeline()
    blend = _pass_blend_context(prior, assumptions, None)
    assert blend.solver_cash_boy is None
    assert blend.prior_fcf is None


@decomposed_stages
def test_pass_capacity_layer_wires_launch_and_pools(assumptions) -> None:
    prior = _zero_initial_pipeline()
    blend = _pass_blend_context(prior, assumptions, None)
    capacity = _pass_capacity_layer(assumptions, prior, blend)
    assert capacity.lc.f9_launches.at(2025) >= 0
    assert capacity.pools.f9_v2_bb_launches is not None
    assert isinstance(capacity.f9_customer, YearVector)


@decomposed_stages
def test_pass_capacity_layer_customer_launch_inputs(assumptions) -> None:
    prior = PipelineState(
        cash_alloc=CashAllocations.zeros(),
        kg_alloc=KgAllocations.zeros(),
        vehicle_build_claim=YearVector.zeros(),
        module_outputs=_zero_initial_pipeline().module_outputs,
    )
    blend = _pass_blend_context(prior, assumptions, None)
    capacity = _pass_capacity_layer(assumptions, prior, blend)
    assert capacity.cl_inputs.launch_capacity is capacity.lc
