"""Phase C integration tests — Group P&L 2025 calibration with mocked module outputs."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc._vending_machine import build_allocator_out
from spacex_model.calc.capex import CapExInputs, compute_capex
from spacex_model.calc.group_pnl import (
    GroupPnlInputs,
    InternalEliminations,
    InternalFlowConservationInputs,
    compute_group_pnl,
)
from spacex_model.calc.opex import OpExInputs, build_revenue_bases, compute_opex
from spacex_model.calc.valuation import ValuationInputs, compute_valuation
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import Assumptions, assumptions_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook

REPO = Path(__file__).resolve().parents[2]
WORKBOOK = REPO / "Pre Existing Model Package" / "01_Current_State" / "SpaceX Model V2.16.xlsx"

# Sprint Roadmap §6.8 revised Block B targets (PRD D1)
TARGET_GROUP_REVENUE_2025 = 14_650
TARGET_GROUP_EBITDA_2025 = 4_904
TARGET_GROUP_FCF_2025 = -2_569
TARGET_TOTAL_OPEX_2025 = 4_476
TARGET_TOTAL_CAPEX_2025 = 6_345
TARGET_IMPLIED_EV_2025_B = 146.5

TOL_REVENUE = 0.05
TOL_EBITDA = 0.05
TOL_FCF = 0.10
TOL_OPEX = 0.05
TOL_CAPEX = 0.05
TOL_EV = 0.05


def _vec(y2025: float, *, rest: float = 0.0) -> YearVector:
    values = np.full(HORIZON_YEARS, rest, dtype=np.float64)
    values[0] = y2025
    return YearVector(values)


def _build_sprint9_mock_modules() -> dict[str, AllocatorOut]:
    """Mock module OUT rows matching Sprint 9 §3.1 verification (2025 column)."""
    starlink = build_allocator_out(
        revenue=_vec(10_854),
        cogs=_vec(4_463),
        capex=_vec(1_202),
        module_da_addback=_vec(707),
    )
    customer_launch = build_allocator_out(
        revenue=_vec(6_572),
        cogs=_vec(3_500),
        capex=_vec(33),
        module_da_addback=_vec(101),
    )
    zeros = build_allocator_out(
        revenue=YearVector.zeros(),
        cogs=YearVector.zeros(),
        capex=YearVector.zeros(),
    )
    return {
        "starlink": starlink,
        "customer_launch": customer_launch,
        "odc": zeros,
        "ai_stack": zeros,
        "lunar_mars": zeros,
    }


def _sprint9_group_inputs(
    assumptions: Assumptions,
    module_outputs: dict[str, AllocatorOut],
) -> GroupPnlInputs:
    """Wire OpEx + CapEx + Group P&L inputs for Sprint 9 calibrated 2025 pass."""
    elim = InternalEliminations(
        launch_services=_vec(2_290),
        bandwidth=YearVector.zeros(),
        compute=YearVector.zeros(),
    )
    revenue_bases = build_revenue_bases(
        module_outputs,
        customer_launch_external_revenue=_vec(4_290),
        eliminations=elim.total,
    )
    opex = compute_opex(
        OpExInputs(
            assumptions=assumptions,
            module_outputs=module_outputs,
            revenue_bases=revenue_bases,
            customer_launch_external_revenue=_vec(4_290),
        )
    )
    capex = compute_capex(
        CapExInputs(
            assumptions=assumptions,
            module_outputs=module_outputs,
            module_da_in_cogs={
                "starlink": _vec(707),
                "customer_launch": _vec(101),
            },
        )
    )
    flows = InternalFlowConservationInputs(
        launch_services_cost_starlink=_vec(2_290),
        launch_services_cost_odc=YearVector.zeros(),
        launch_services_cost_ai_stack=YearVector.zeros(),
        odc_bandwidth_services_cost=YearVector.zeros(),
        ai_stack_internal_compute_cost=YearVector.zeros(),
    )
    return GroupPnlInputs(
        assumptions=assumptions,
        module_outputs=module_outputs,
        opex=opex,
        capex=capex,
        eliminations=elim,
        module_da_in_cogs={
            "starlink": _vec(707),
            "customer_launch": _vec(101),
        },
        internal_flows=flows,
        mars_carveout=_vec(1_000),
    )


def _within_tolerance(actual: float, target: float, tolerance: float) -> bool:
    if target == 0:
        return abs(actual) <= tolerance * 1000
    return abs(actual - target) / abs(target) <= tolerance


@pytest.fixture(scope="module")
def assumptions_from_workbook() -> Assumptions | None:
    if not WORKBOOK.exists():
        return None
    ingest = ingest_workbook(WORKBOOK)
    return assumptions_from_ingest(ingest)


def test_group_pnl_conservation_ok_sprint9_mocks(
    assumptions_from_workbook: Assumptions | None,
) -> None:
    """R108 = OK all years with Sprint 9–calibrated mocked module outputs."""
    assumptions = assumptions_from_workbook or Assumptions()
    modules = _build_sprint9_mock_modules()
    result = compute_group_pnl(_sprint9_group_inputs(assumptions, modules))

    assert result.conservation.all_ok
    assert result.conservation.r108_ok_by_year[FIRST_YEAR] == "OK"
    for check in ("R99", "R100", "R101", "R103", "R104", "R105", "R106", "R107"):
        residual = result.conservation.residuals_by_check[check][FIRST_YEAR]
        assert abs(residual) < 1.0, f"{check} residual {residual}"


def test_group_pnl_2025_calibration_sprint9_mocks(
    assumptions_from_workbook: Assumptions | None,
) -> None:
    """Block B §6.8 revised anchors for Group P&L walk (mocked module OUT)."""
    assumptions = assumptions_from_workbook or Assumptions()
    modules = _build_sprint9_mock_modules()
    result = compute_group_pnl(_sprint9_group_inputs(assumptions, modules))
    y = FIRST_YEAR

    rev = result.group_revenue_net.at(y)
    assert _within_tolerance(rev, TARGET_GROUP_REVENUE_2025, TOL_REVENUE), (
        f"Group revenue 2025: {rev:,.0f} vs target {TARGET_GROUP_REVENUE_2025:,.0f}"
    )

    ebitda = result.group_ebitda.at(y)
    assert _within_tolerance(ebitda, TARGET_GROUP_EBITDA_2025, TOL_EBITDA), (
        f"Group EBITDA 2025: {ebitda:,.0f} vs target {TARGET_GROUP_EBITDA_2025:,.0f}"
    )

    fcf = result.group_fcf.at(y)
    assert _within_tolerance(fcf, TARGET_GROUP_FCF_2025, TOL_FCF), (
        f"Group FCF 2025: {fcf:,.0f} vs target {TARGET_GROUP_FCF_2025:,.0f}"
    )

    opex = result.total_opex.at(y)
    assert _within_tolerance(opex, TARGET_TOTAL_OPEX_2025, TOL_OPEX), (
        f"Total OpEx 2025: {opex:,.0f} vs target {TARGET_TOTAL_OPEX_2025:,.0f}"
    )

    capex = result.total_group_capex.at(y)
    assert _within_tolerance(capex, TARGET_TOTAL_CAPEX_2025, TOL_CAPEX), (
        f"Total Group CapEx 2025: {capex:,.0f} vs target {TARGET_TOTAL_CAPEX_2025:,.0f}"
    )


def test_valuation_implied_ev_2025_sprint9_mocks(
    assumptions_from_workbook: Assumptions | None,
) -> None:
    """Implied EV 2025 = 10× Group Revenue net ($146.5B ±5%)."""
    assumptions = assumptions_from_workbook or Assumptions()
    modules = _build_sprint9_mock_modules()
    group = compute_group_pnl(_sprint9_group_inputs(assumptions, modules))
    valuation = compute_valuation(ValuationInputs(assumptions=assumptions, group_pnl=group))

    assert _within_tolerance(
        valuation.implied_ev_2025_billions,
        TARGET_IMPLIED_EV_2025_B,
        TOL_EV,
    ), f"Implied EV 2025: ${valuation.implied_ev_2025_billions:.1f}B"


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_opex_switching_rd_odc_2025(assumptions_from_workbook: Assumptions | None) -> None:
    """ODC R&D floor = $200M when revenue is zero (PRD §2.14 enforcement)."""
    assert assumptions_from_workbook is not None
    modules = _build_sprint9_mock_modules()
    result = compute_opex(
        OpExInputs(
            assumptions=assumptions_from_workbook,
            module_outputs=modules,
        )
    )
    assert result.odc_rd.at(FIRST_YEAR) >= 200.0


@pytest.mark.skipif(not WORKBOOK.exists(), reason="V2.16 workbook not present")
def test_capex_spectrum_2025_exact(assumptions_from_workbook: Assumptions | None) -> None:
    """Spectrum CapEx 2025 = $5B exact per §5.3 calibration."""
    assert assumptions_from_workbook is not None
    modules = _build_sprint9_mock_modules()
    capex = compute_capex(
        CapExInputs(
            assumptions=assumptions_from_workbook,
            module_outputs=modules,
        )
    )
    assert capex.spectrum_capex.at(FIRST_YEAR) == pytest.approx(5000.0, rel=0.01)
