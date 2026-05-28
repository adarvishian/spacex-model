"""Phase B module scaffolding tests."""

from __future__ import annotations

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.ai_stack import compute_allocator_out as ai_stack_out
from spacex_model.calc.lunar_mars import compute_allocator_out as lunar_mars_out
from spacex_model.calc.odc import compute_allocator_out as odc_out
from spacex_model.calc.starlink import compute_allocator_out as sl_out
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.engine.pipeline import run_base_case


def test_allocator_out_contract_stubs_zero() -> None:
    for out in (odc_out(), ai_stack_out(), lunar_mars_out()):
        assert isinstance(out, AllocatorOut)
        assert out.total_revenue.values.sum() == 0.0
        assert out.module_fcf.values.sum() == 0.0
        assert len(out.total_revenue) == HORIZON_YEARS


def test_module_ebitda_equals_gross_profit() -> None:
    from spacex_model.calc.starlink.module import StarlinkInputs
    from spacex_model.inputs.demand_curves import demand_curves_stub
    from spacex_model.inputs.assumptions import Assumptions

    out = sl_out(StarlinkInputs(assumptions=Assumptions(), demand_curves=demand_curves_stub()))
    assert (out.module_ebitda.values == out.gross_profit.values).all()


def test_base_case_pipeline_phase_e() -> None:
    result = run_base_case(write_outputs=False)
    assert result.audit.get("phase") == "E"
    assert result.solver_trace.converged
    assert len(result.module_outputs) == 5
    assert result.module_outputs["starlink"].total_revenue.at(2025) > 0.0
