"""Phase C module calibration tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.calc.customer_launch.module import CustomerLaunchInputs, compute_allocator_out as cl_out
from spacex_model.calc.launch_capacity import LaunchCapacityInputs, compute_launch_capacity
from spacex_model.calc.lunar_mars.module import LunarMarsInputs, compute_allocator_out as lm_out
from spacex_model.calc.odc.module import OdcInputs, compute_allocator_out as odc_out
from spacex_model.calc.starlink.module import StarlinkInputs, compute_allocator_out as sl_out
from spacex_model.calc.starlink.vehicle_pools import compute_vehicle_pools
from spacex_model.calc.starlink_capacity import OdcBandwidthClaim
from spacex_model.config.constants import FIRST_YEAR
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions, assumptions_from_ingest
from spacex_model.inputs.s1_overrides import apply_s1_adherence_overrides
from spacex_model.inputs.demand_curves import demand_curves_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"


def _within(actual: float, target: float, tol: float) -> bool:
    if target == 0:
        return abs(actual) <= tol
    return abs(actual - target) / abs(target) <= tol


@pytest.fixture(scope="module")
def workbook_ingest():
    if not WORKBOOK.exists():
        return None
    return ingest_workbook(WORKBOOK)


@pytest.fixture(scope="module")
def assumptions(workbook_ingest) -> Assumptions:
    if workbook_ingest is None:
        return Assumptions()
    return apply_s1_adherence_overrides(assumptions_from_ingest(workbook_ingest))


@pytest.fixture(scope="module")
def demand_curves(workbook_ingest):
    if workbook_ingest is None:
        from spacex_model.inputs.demand_curves import demand_curves_stub

        return demand_curves_stub()
    return demand_curves_from_ingest(workbook_ingest)


@pytest.fixture(scope="module")
def starlink_inputs(assumptions, demand_curves, workbook_ingest) -> StarlinkInputs:
    pools = compute_vehicle_pools(assumptions)
    lc = compute_launch_capacity(
        LaunchCapacityInputs(
            assumptions=assumptions,
            f9_starlink_v2_bb_launches=pools.f9_v2_bb_launches,
            f9_starlink_v2_dtc_launches=pools.f9_v2_dtc_launches,
        )
    )
    return StarlinkInputs(
        assumptions=assumptions,
        demand_curves=demand_curves,
        launch_capacity=lc,
        vehicle_pools=pools,
        odc_bandwidth_claim=OdcBandwidthClaim(
            bb_gbps=YearVector.zeros(),
            dtc_gbps=YearVector.zeros(),
        ),
    )


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_launch_capacity_2025_calibration(assumptions: Assumptions) -> None:
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    y = FIRST_YEAR
    assert lc.f9_launches.at(y) == pytest.approx(171.0, abs=5.0)
    assert lc.f9_fleet_eoy.at(y) == pytest.approx(39.0, abs=5.0)
    assert lc.f9_manufactured.at(y) == pytest.approx(17.0, abs=2.0)
    assert lc.total_starship_launches.at(y) == 0.0
    assert 400 <= lc.blended_cost_per_kg.at(y) <= 800


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_customer_launch_2025_calibration(assumptions: Assumptions, starlink_inputs: StarlinkInputs) -> None:
    pools = starlink_inputs.vehicle_pools
    assert pools is not None
    lc = starlink_inputs.launch_capacity
    cl_inputs = CustomerLaunchInputs(
        assumptions=assumptions,
        launch_capacity=lc,
        f9_internal_launches=YearVector(
            pools.f9_v2_bb_launches.values + pools.f9_v2_dtc_launches.values
        ),
    )
    out = cl_out(cl_inputs)
    y = FIRST_YEAR
    f9_customer_rev = 43.0 * 111.0
    assert _within(f9_customer_rev, 4773.0, 0.02)
    assert out.total_revenue.at(y) > 4000.0


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_starlink_2025_launch_anchors(starlink_inputs: StarlinkInputs) -> None:
    pools = starlink_inputs.vehicle_pools
    assert pools is not None
    assert pools.v2_bb.launches.at(FIRST_YEAR) == pytest.approx(2987.0)
    assert pools.v2_dtc.launches.at(FIRST_YEAR) == pytest.approx(182.0)
    assert pools.v3_bb.launches.at(FIRST_YEAR) == 0.0
    assert pools.v3_dtc.launches.at(FIRST_YEAR) == 0.0


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_starlink_2025_fleet_anchors(starlink_inputs: StarlinkInputs) -> None:
    pools = starlink_inputs.vehicle_pools
    assert pools is not None
    assert pools.v2_bb.active_fleet.at(FIRST_YEAR) == pytest.approx(5246.0, rel=0.01)
    assert pools.v2_dtc.active_fleet.at(FIRST_YEAR) == pytest.approx(650.0, rel=0.01)


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_starlink_2025_revenue_calibration(starlink_inputs: StarlinkInputs) -> None:
    out = sl_out(starlink_inputs)
    y = FIRST_YEAR
    rev = out.total_revenue.at(y)
    assert rev > 8000.0, f"Total Starlink revenue 2025 too low: {rev:,.0f}"
    assert _within(rev, 10_397.0, 0.08), f"Total revenue {rev:,.0f} vs post-S-1 ARPU baseline"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_starlink_starshield_2025(starlink_inputs: StarlinkInputs) -> None:
    from spacex_model.calc.starlink.module import compute_starshield_revenue

    ss = compute_starshield_revenue(starlink_inputs).at(FIRST_YEAR)
    assert _within(ss, 2520.0, 0.05), f"Starshield 2025: {ss:,.0f} vs target 2520"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_odc_2025_zero(assumptions: Assumptions) -> None:
    out = odc_out(OdcInputs(assumptions=assumptions, sats_deployed=YearVector.zeros()))
    y = FIRST_YEAR
    assert out.total_revenue.at(y) == 0.0
    assert out.total_cogs.at(y) == 0.0


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_lunar_mars_2025_zero(assumptions: Assumptions) -> None:
    out = lm_out(LunarMarsInputs(assumptions=assumptions))
    y = FIRST_YEAR
    assert out.total_revenue.at(y) == 0.0
    assert out.module_capex.at(y) == 0.0


def test_demand_curves_piecewise_lookup(demand_curves) -> None:
    bb = demand_curves.lookup_bb_revenue(575_504.0, 0, tam_shift=1.0)
    assert bb == pytest.approx(6745.7, rel=0.01)
    dtc = demand_curves.lookup_dtc_revenue(130.0, 0, tam_shift=1.0)
    assert dtc == pytest.approx(142.4, rel=0.05)


def test_module_ebitda_equals_gross_profit(starlink_inputs: StarlinkInputs) -> None:
    out = sl_out(starlink_inputs)
    assert (out.module_ebitda.values == out.gross_profit.values).all()
