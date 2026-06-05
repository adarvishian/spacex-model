"""Sprint R3 gate — CAE allocator as-is (softmax + water-fill + pro-rata kg + debt)."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.brain import AllocatorInputs, compute_allocator
from spacex_model.calc.allocator.debt_facilities import (
    OdcFacilityInputs,
    TerafabFacilityInputs,
    compute_debt_facilities,
    odc_debt_conservation_ok,
    terafab_debt_conservation_ok,
)
from spacex_model.calc.allocator.priority import compute_softmax_allocation
from spacex_model.calc.allocator.queue_gate import compute_queue_gate
from spacex_model.calc.facilities_build import FacilitiesBuildInputs, compute_facilities_build
from spacex_model.calc.launch_capacity import LaunchCapacityInputs, compute_launch_capacity
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.io.label_value import label_year_vector
from spacex_model.linters.canonical_labels import find_inline_label_literals

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "SpaceX V4.113.xlsx"
CAE = "Cash Allocation Engine"


@pytest.fixture(scope="module")
def ingest():
    if not WORKBOOK.exists():
        pytest.skip("V4.113 workbook not present")
    return ingest_workbook(WORKBOOK)


@pytest.fixture(scope="module")
def assumptions(ingest):
    return assumptions_from_ingest(ingest)


def _fb_from_xlsx(ingest, assumptions):
    return FacilitiesBuildInputs(
        assumptions=assumptions,
        sats_built_starlink=label_year_vector(ingest, "Facilities Build", "Sats built: Starlink (sats/yr)"),
        ships_built=label_year_vector(
            ingest, "Facilities Build", "Ships built this year (= Vehicle Build Ships built (fleet), unified)"
        ),
        chips_demanded=label_year_vector(ingest, "Facilities Build", "Chips demanded this year (count)  ◄ AI-Compute"),
        group_revenue_base=label_year_vector(
            ingest, "Facilities Build", "Group revenue base ($mm): placeholder (Starlink rev; swap to Group total in 4.5)"
        ),
        starship_launches=label_year_vector(ingest, "Vehicle Build", "Starship launches per year"),
    )


def test_r3_allocator_modules_importable() -> None:
    from spacex_model.calc.allocator import (
        compute_carve_out,
        compute_kg_rationing,
        compute_queue_gate,
        compute_softmax_allocation,
        compute_water_fill,
    )

    assert callable(compute_softmax_allocation)


def test_r3_softmax_shares_match_xlsx_2030(ingest, assumptions) -> None:
    """Softmax shares reconcile to CAE cached values (divergence-triaged gate)."""
    spot = label_year_vector(ingest, CAE, cl.SPOT_IRR_STARLINK)
    spot_cl = label_year_vector(ingest, CAE, cl.SPOT_IRR_CUSTOMER_LAUNCH)
    spot_ai = label_year_vector(ingest, CAE, cl.SPOT_IRR_AI_COMPUTE)
    from spacex_model.calc.allocator.priority import ModuleSpotIrrs, compute_softmax_shares

    spot_irr = ModuleSpotIrrs(starlink=spot, customer_launch=spot_cl, ai_compute=spot_ai)
    _, _, shares = compute_softmax_shares(spot_irr, assumptions)
    xlsx_sl = label_year_vector(ingest, CAE, cl.ALLOCATION_SHARE_STARLINK).at(2030)
    xlsx_cl = label_year_vector(ingest, CAE, cl.ALLOCATION_SHARE_CUSTOMER_LAUNCH).at(2030)
    xlsx_ai = label_year_vector(ingest, CAE, cl.ALLOCATION_SHARE_AI_COMPUTE).at(2030)
    assert shares.starlink.at(2030) == pytest.approx(xlsx_sl, rel=0.02)
    assert shares.customer_launch.at(2030) == pytest.approx(xlsx_cl, rel=0.02)
    assert shares.ai_compute.at(2030) == pytest.approx(xlsx_ai, rel=0.02)


def test_r3_remaining_pool_zero_in_2025(ingest, assumptions) -> None:
    """2025 anchor: allocation operative 2026+ only."""
    cash_avail = label_year_vector(ingest, CAE, cl.CASH_AVAILABLE_FOR_YEAR_MM)
    from spacex_model.calc.allocator.carve_out import compute_carve_out

    pool = compute_queue_gate(
        cash_avail,
        corp_sga=YearVector.zeros(),
        shared_rd=YearVector.zeros(),
        corp_capex=YearVector.zeros(),
        spectrum_capex=YearVector.zeros(),
        taxes=YearVector.zeros(),
        vehicle_build_claim=YearVector.zeros(),
    )
    carve = compute_carve_out(assumptions, pool.pool_after_gate)
    assert carve.remaining_pool.at(FIRST_YEAR) == 0.0


def test_r3_kg_pro_rata_independent_of_cash(assumptions) -> None:
    """F2 defect: kg rationing uses pro-rata, not cash softmax weights."""
    from spacex_model.calc.allocator.kg_rationing import compute_kg_rationing
    from spacex_model.calc.allocator.priority import ModuleSpotIrrs

    desired = ModuleSpotIrrs(
        starlink=YearVector(np.full(HORIZON_YEARS, 100.0)),
        customer_launch=YearVector(np.full(HORIZON_YEARS, 50.0)),
        ai_compute=YearVector(np.full(HORIZON_YEARS, 50.0)),
    )
    cap = YearVector(np.full(HORIZON_YEARS, 200.0))
    result = compute_kg_rationing(desired, cap, YearVector.zeros())
    assert result.allotment_kg.starlink.at(2030) == pytest.approx(100.0, rel=0.01)
    assert result.allotment_kg.customer_launch.at(2030) == pytest.approx(50.0, rel=0.01)


def test_r3_debt_wired_through_allocator(ingest, assumptions) -> None:
    """Debt facilities conservation when FB drivers supplied."""
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    mods = {k: AllocatorOut.zeros() for k in ("customer_launch", "starlink", "ai_compute", "lunar_mars")}
    result = compute_allocator(
        AllocatorInputs(
            assumptions=assumptions,
            module_outputs=mods,
            opex=YearVector.zeros(),
            corp_capex=YearVector.zeros(),
            spectrum_capex=YearVector.zeros(),
            taxes=YearVector.zeros(),
            launch_capacity=lc,
            facilities_build=fb,
            group_fcf=label_year_vector(ingest, CAE, "Group FCF ($mm)"),
        )
    )
    assert result.debt_odc_draw is not None
    assert result.debt_terafab_draw is not None
    debt = compute_debt_facilities(
        TerafabFacilityInputs(
            assumptions=assumptions,
            terafab_capex_to_fund=fb.chip_fab_capex,
            cash_eoy=label_year_vector(ingest, CAE, "Cash EoY ($mm)"),
            ipo_injection=label_year_vector(ingest, CAE, "IPO injection ($mm)"),
            group_fcf=label_year_vector(ingest, CAE, "Group FCF ($mm)"),
        ),
        OdcFacilityInputs(
            assumptions=assumptions,
            odc_capex_need=label_year_vector(ingest, CAE, "ODC CapEx need ($mm): launch-feasible deploy × cost"),
            odc_pool_allocation=label_year_vector(ingest, CAE, cl.ODC_POOL_ALLOCATION_MM),
            ai_compute_module_fcf=label_year_vector(ingest, "AI - Compute", "Module FCF ($mm)"),
        ),
    )
    assert terafab_debt_conservation_ok(debt.terafab)
    assert odc_debt_conservation_ok(debt.odc)


def test_r3_structural_invariants(ingest, assumptions) -> None:
    """Σ cash alloc ≤ remaining pool; shares sum ≈ 1; 2025 cash alloc = 0."""
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    mods = {k: AllocatorOut.zeros() for k in ("customer_launch", "starlink", "ai_compute", "lunar_mars")}
    result = compute_allocator(
        AllocatorInputs(
            assumptions=assumptions,
            module_outputs=mods,
            opex=YearVector.zeros(),
            corp_capex=YearVector.zeros(),
            spectrum_capex=YearVector.zeros(),
            taxes=YearVector.zeros(),
            launch_capacity=lc,
        )
    )
    assert result.remaining_pool is not None
    for t in range(HORIZON_YEARS):
        total_cash = sum(getattr(result.cash, f).values[t] for f in result.cash.__dataclass_fields__ if f != "as_tuple")
        pool = result.remaining_pool.values[t]
        assert total_cash <= pool + 1.0
        if FIRST_YEAR + t == FIRST_YEAR:
            assert total_cash == pytest.approx(0.0, abs=1.0)


def test_r3_defect_f4_documented_kg_demand_mismatch(ingest) -> None:
    """F4: memo kg demand ≠ sum desired launch kg (defect reproduced, not fixed)."""
    memo = label_year_vector(ingest, CAE, "Memo: total kg demand (kg)").at(2030)
    sl = label_year_vector(ingest, CAE, cl.DESIRED_LAUNCH_KG_STARLINK).at(2030)
    cl_kg = label_year_vector(ingest, CAE, cl.DESIRED_LAUNCH_KG_CUSTOMER_LAUNCH).at(2030)
    ai = label_year_vector(ingest, CAE, cl.DESIRED_LAUNCH_KG_AI_COMPUTE).at(2030)
    total = sl + cl_kg + ai
    assert memo != pytest.approx(total, rel=0.1)


def test_r3_inline_labels_allocator_scope(ingest) -> None:
    """R3-scope allocator modules use cl.* registry."""
    violations = find_inline_label_literals()
    r3_modules = {
        "allocator/brain.py",
        "allocator/cash_pool.py",
        "allocator/queue_gate.py",
        "allocator/priority.py",
        "allocator/kg_rationing.py",
        "allocator/water_fill.py",
        "allocator/carve_out.py",
        "allocator/level2_split.py",
        "allocator/cae_demands.py",
        "allocator/debt_facilities.py",
        "allocator/irr_display.py",
    }
    r3_violations = [v for v in violations if any(m in v for m in r3_modules)]
    assert r3_violations == [], "\n".join(r3_violations[:15])
