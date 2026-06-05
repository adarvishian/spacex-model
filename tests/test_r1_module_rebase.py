"""Sprint R1 gate — V4.113 module re-base."""

from __future__ import annotations

from spacex_model.calc.ai_compute import AiComputeInputs, compute_allocator_out as ai_compute_out
from spacex_model.calc.segment_pnl import SegmentPnlInputs, compute_segment_pnl, segment_tieouts_ok
from spacex_model.config.constants import HORIZON_YEARS
from spacex_model.config.settings import get_settings
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.inputs.demand_curves import demand_curves_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.linters.canonical_labels import find_inline_label_literals
from spacex_model.linters.vending_machine import find_vending_machine_violations


def test_r1_module_package_inventory() -> None:
    """Four P&L modules mirror V4.113 tabs (CL, Starlink, AI-Compute, Lunar-Mars)."""
    from spacex_model.calc._module_packages import PNL_MODULE_PACKAGES

    assert set(PNL_MODULE_PACKAGES) == {
        "customer_launch",
        "starlink",
        "ai_compute",
        "lunar_mars",
    }


def test_r1_vending_machine_framing() -> None:
    violations = find_vending_machine_violations()
    assert violations == [], "\n".join(violations)


def test_r1_ai_compute_merged_module() -> None:
    out = ai_compute_out()
    assert len(out.total_revenue) == HORIZON_YEARS
    assert out.total_revenue.values.sum() == 0.0


def test_r1_inline_labels_reduced_in_r1_modules() -> None:
    """R1-scope modules use cl.* — remaining literals deferred to R2/R3 (allocator, capex, launch)."""
    violations = find_inline_label_literals()
    r1_modules = {
        "starlink/",
        "customer_launch/",
        "lunar_mars/",
        "ai_compute/",
        "group_pnl.py",
        "segment_pnl.py",
        "internal_flows/",
    }
    r1_violations = [v for v in violations if any(m in v for m in r1_modules)]
    assert r1_violations == [], "\n".join(r1_violations[:15])


def test_r1_segment_pnl_tieouts_stub() -> None:
    from spacex_model.calc._allocator_out import AllocatorOut
    from spacex_model.calc.group_pnl import GroupPnlResult
    from spacex_model.domain.year_vector import YearVector
    from spacex_model.engine.conservation import ConservationResult, InternalEliminations

    z = YearVector.zeros()
    mods = {k: AllocatorOut.zeros() for k in ("customer_launch", "starlink", "ai_compute", "lunar_mars")}
    group = GroupPnlResult(
        module_revenue_gross=z,
        group_revenue_net=z,
        module_cogs_gross=z,
        group_cogs_net=z,
        group_gross_profit=z,
        total_opex=z,
        group_ebitda=z,
        group_da=z,
        group_ebit=z,
        taxes=z,
        nopat=z,
        total_da_addback=z,
        total_group_capex=z,
        mars_carveout=z,
        group_fcf=z,
        adjusted_ebitda=z,
        conservation=ConservationResult(
            r108_ok_by_year={2025: "OK"},
            residuals_by_check={},
        ),
    )
    seg = compute_segment_pnl(
        SegmentPnlInputs(
            group_pnl=group,
            module_outputs=mods,
            eliminations=InternalEliminations(launch_services=z, bandwidth=z, compute=z),
        )
    )
    assert segment_tieouts_ok(seg)


def test_r1_workbook_ingest_for_modules() -> None:
    path = get_settings().workbook_path
    if not path.exists():
        return
    ingest = ingest_workbook(path)
    assumptions = assumptions_from_ingest(ingest)
    demand = demand_curves_from_ingest(ingest)
    assert demand.bb_breakpoints_q.size > 0
    assert assumptions.tax_rate > 0
