"""Sprint R2 gate — Facilities Build + Terafab/ODC debt layer."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from spacex_model.calc.allocator.debt_facilities import (
    OdcFacilityInputs,
    TerafabFacilityInputs,
    compute_debt_facilities,
    compute_odc_facility,
    compute_terafab_facility,
    odc_debt_conservation_ok,
    terafab_debt_conservation_ok,
)
from spacex_model.calc.facilities_build import (
    FacilitiesBuildInputs,
    compute_facilities_build,
    facilities_conservation_ok,
)
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import CONSERVATION_RESIDUAL_TOLERANCE_MM, FIRST_YEAR, HORIZON_YEARS
from spacex_model.config.settings import get_settings
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.io.label_value import label_year_value, label_year_vector
from spacex_model.linters.canonical_labels import find_inline_label_literals

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "SpaceX V4.113.xlsx"
FB = "Facilities Build"
CAE = "Cash Allocation Engine"


@pytest.fixture(scope="module")
def ingest():
    if not WORKBOOK.exists():
        pytest.skip("V4.113 workbook not present")
    return ingest_workbook(WORKBOOK)


@pytest.fixture(scope="module")
def assumptions(ingest):
    return assumptions_from_ingest(ingest)


def _fb_inputs(ingest, assumptions) -> FacilitiesBuildInputs:
    """Drive FB from xlsx cached cross-tab reads (R2 isolation gate)."""
    return FacilitiesBuildInputs(
        assumptions=assumptions,
        sats_built_starlink=label_year_vector(ingest, FB, "Sats built: Starlink (sats/yr)"),
        ships_built=label_year_vector(
            ingest, FB, "Ships built this year (= Vehicle Build Ships built (fleet), unified)"
        ),
        boosters_built=label_year_vector(
            ingest, FB, "Boosters built this year (= Vehicle Build Boosters built (fleet))"
        ),
        chips_demanded=label_year_vector(ingest, FB, "Chips demanded this year (count)  ◄ AI-Compute"),
        group_revenue_base=label_year_vector(
            ingest, FB, "Group revenue base ($mm): placeholder (Starlink rev; swap to Group total in 4.5)"
        ),
        starship_launches=label_year_vector(ingest, "Vehicle Build", "Starship launches per year"),
    )


def test_r2_facilities_build_module_importable() -> None:
    from spacex_model.calc import facilities_build

    assert hasattr(facilities_build, "compute_facilities_build")


def test_r2_debt_facilities_module_importable() -> None:
    from spacex_model.calc.allocator import debt_facilities

    assert hasattr(debt_facilities, "compute_debt_facilities")


def test_r2_fb_conservation_gate(ingest, assumptions) -> None:
    """FB R44 ≤ 0 every year when driven by xlsx cross-tab reads."""
    result = compute_facilities_build(_fb_inputs(ingest, assumptions))
    assert facilities_conservation_ok(result)
    xlsx_r44 = label_year_vector(ingest, FB, cl.CONSERVATION_MAX_BUCKET_CUM_D_A_CUM_CAPEX_MUST_BE_0)
    for t in range(HORIZON_YEARS):
        assert result.conservation_max_bucket.values[t] <= CONSERVATION_RESIDUAL_TOLERANCE_MM + 1e-6
        # Structural gate: Python conservation must match xlsx sign (≤ 0)
        if xlsx_r44.values[t] != 0.0:
            assert result.conservation_max_bucket.values[t] <= max(0.0, xlsx_r44.values[t]) + 50.0


def test_r2_terafab_debt_conservation_gate(ingest, assumptions) -> None:
    """CAE R111: Σdraw − Σrepay − balance = 0."""
    fb = compute_facilities_build(_fb_inputs(ingest, assumptions))
    terafab = compute_terafab_facility(
        TerafabFacilityInputs(
            assumptions=assumptions,
            terafab_capex_to_fund=fb.chip_fab_capex,
            cash_eoy=label_year_vector(ingest, CAE, "Cash EoY ($mm)"),
            ipo_injection=label_year_vector(ingest, CAE, "IPO injection ($mm)"),
            group_fcf=label_year_vector(ingest, CAE, "Group FCF ($mm)"),
        )
    )
    assert terafab_debt_conservation_ok(terafab)
    xlsx = label_year_vector(ingest, CAE, cl.CONSERVATION_DRAW_REPAY_BALANCE_MUST_0)
    for t in range(1, HORIZON_YEARS):
        if xlsx.values[t] != 0.0:
            assert abs(terafab.conservation_draw_repay_balance.values[t]) <= CONSERVATION_RESIDUAL_TOLERANCE_MM


def test_r2_odc_debt_conservation_gate(ingest, assumptions) -> None:
    """CAE R140: ODC Σdraw − Σrepay − balance = 0."""
    odc = compute_odc_facility(
        OdcFacilityInputs(
            assumptions=assumptions,
            odc_capex_need=label_year_vector(ingest, CAE, "ODC CapEx need ($mm): launch-feasible deploy × cost"),
            odc_pool_allocation=label_year_vector(ingest, CAE, "ODC pool allocation ($mm)"),
            ai_compute_module_fcf=label_year_vector(ingest, "AI - Compute", "Module FCF ($mm)"),
        )
    )
    assert odc_debt_conservation_ok(odc)
    xlsx = label_year_vector(ingest, CAE, cl.CONSERVATION_ODC_DRAW_REPAY_BALANCE_MUST_0)
    for t in range(HORIZON_YEARS):
        if xlsx.values[t] != 0.0:
            assert abs(odc.conservation_draw_repay_balance.values[t]) <= CONSERVATION_RESIDUAL_TOLERANCE_MM


def test_r2_gigabay_capacity_positive(ingest, assumptions) -> None:
    result = compute_facilities_build(_fb_inputs(ingest, assumptions))
    assert result.gigabay_installed_capacity.values[0] > 0
    xlsx = label_year_vector(ingest, FB, "Installed Starship build capacity (ships/yr): rate-limited ramp")
    assert result.gigabay_installed_capacity.at(FIRST_YEAR) == pytest.approx(xlsx.at(FIRST_YEAR), rel=0.05)


def test_r2_capex_ai_compute_module_key(assumptions) -> None:
    from spacex_model.calc._allocator_out import AllocatorOut
    from spacex_model.calc.capex import CapExInputs, compute_capex

    mods = {
        "customer_launch": AllocatorOut.zeros(),
        "starlink": AllocatorOut.zeros(),
        "ai_compute": AllocatorOut.zeros(),
        "lunar_mars": AllocatorOut.zeros(),
    }
    result = compute_capex(CapExInputs(assumptions=assumptions, module_outputs=mods))
    assert len(result.ai_compute_module_capex) == HORIZON_YEARS


def test_r2_inline_labels_r2_scope(ingest) -> None:
    """R2-scope modules use cl.* — allocator literals deferred to R3."""
    violations = find_inline_label_literals()
    r2_modules = {
        "facilities_build.py",
        "debt_facilities.py",
        "capex.py",
    }
    r2_violations = [v for v in violations if any(m in v for m in r2_modules)]
    assert r2_violations == [], "\n".join(r2_violations[:15])


def test_r2_debt_facilities_combined(ingest, assumptions) -> None:
    fb = compute_facilities_build(_fb_inputs(ingest, assumptions))
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
            odc_pool_allocation=label_year_vector(ingest, CAE, "ODC pool allocation ($mm)"),
            ai_compute_module_fcf=label_year_vector(ingest, "AI - Compute", "Module FCF ($mm)"),
        ),
    )
    assert terafab_debt_conservation_ok(debt.terafab)
    assert odc_debt_conservation_ok(debt.odc)
