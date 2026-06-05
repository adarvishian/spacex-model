"""Sprint U3 gate — strategic seed + debt re-scope (F5 remediation)."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.brain import AllocatorInputs, compute_allocator
from spacex_model.calc.allocator.debt_facilities import (
    OdcFacilityInputs,
    TerafabFacilityInputs,
    compute_debt_facilities,
    compute_odc_facility,
    compute_terafab_facility,
    terafab_debt_conservation_ok,
)
from spacex_model.calc.allocator.strategic_seed import (
    StrategicSeedInputs,
    compute_strategic_seed,
)
from spacex_model.calc.facilities_build import FacilitiesBuildInputs, compute_facilities_build
from spacex_model.calc.launch_capacity import LaunchCapacityInputs, compute_launch_capacity
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.config.settings import get_settings
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.pipeline import run_base_case
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.io.label_value import label_year_vector
from spacex_model.linters.canonical_labels import find_inline_label_literals

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "SpaceX V4.113.xlsx"
CAE = "Cash Allocation Engine"
EDGE_YEARS = (2025, 2030, 2035, 2040)


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


def _allocator_result(ingest, assumptions):
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    mods = {k: AllocatorOut.zeros() for k in ("customer_launch", "starlink", "ai_compute", "lunar_mars")}
    mods["customer_launch"] = replace(
        AllocatorOut.zeros(),
        spot_irr=label_year_vector(ingest, CAE, cl.SPOT_IRR_CUSTOMER_LAUNCH),
    )
    mods["starlink"] = replace(
        AllocatorOut.zeros(),
        spot_irr=label_year_vector(ingest, CAE, cl.SPOT_IRR_STARLINK),
    )
    mods["ai_compute"] = replace(
        AllocatorOut.zeros(),
        spot_irr=label_year_vector(ingest, CAE, cl.SPOT_IRR_ODC_PRIOR_YR),
    )
    return compute_allocator(
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


def test_u3_seed_deploys_pre_graduation(assumptions) -> None:
    """Strategic seed deploys ODC ramp before prior-yr IRR graduation."""
    buildable = YearVector(np.linspace(0.0, 20_000.0, HORIZON_YEARS))
    kg = YearVector(np.linspace(0.0, 10_000_000.0, HORIZON_YEARS))
    pool = YearVector.constant(50_000.0)
    prior = YearVector.constant(0.02)
    seed = compute_strategic_seed(
        StrategicSeedInputs(
            assumptions=assumptions,
            odc_demand_buildable=buildable,
            odc_kg_demand=kg,
            prior_odc_irr=prior,
            pool_after_carveout=pool,
        )
    )
    assert seed.cash_claim.at(2030) > 0.0
    assert seed.kg_reserved.at(2030) > 0.0


def test_u3_seed_sunsets_on_graduation(assumptions) -> None:
    """Seed sunsets once prior-yr ODC IRR crosses graduation hurdle."""
    buildable = YearVector.constant(10_000.0)
    kg = YearVector.constant(5_000_000.0)
    pool = YearVector.constant(50_000.0)
    prior = YearVector.zeros()
    prior.values[5:] = 0.20
    seed = compute_strategic_seed(
        StrategicSeedInputs(
            assumptions=assumptions,
            odc_demand_buildable=buildable,
            odc_kg_demand=kg,
            prior_odc_irr=prior,
            pool_after_carveout=pool,
        )
    )
    year_after_grad = 2025 + 6
    assert seed.graduated.at(year_after_grad) == pytest.approx(1.0)
    assert seed.cash_claim.at(year_after_grad) == pytest.approx(0.0, abs=1.0)


def test_u3_odc_facility_no_bypass(assumptions) -> None:
    """F5 fix: ODC facility draw always zero — no pool bypass."""
    odc = compute_odc_facility(
        OdcFacilityInputs(
            assumptions=assumptions,
            odc_capex_need=YearVector.constant(30_000.0),
            odc_pool_allocation=YearVector.constant(1_000.0),
        )
    )
    assert np.all(odc.draw.values == 0.0)


def test_u3_odc_no_double_fund(ingest, assumptions) -> None:
    """ODC total = seed + pool alloc; debt draw not added."""
    result = _allocator_result(ingest, assumptions)
    year = 2030
    assert result.strategic_seed_cash is not None
    assert result.allocated_final_odc is not None
    assert result.debt_odc_draw is not None
    pool_alloc = result.allocated_final_odc.at(year) - result.strategic_seed_cash.at(year)
    assert pool_alloc >= 0.0
    assert result.debt_odc_draw.at(year) == pytest.approx(0.0)
    assert result.odc_total_cash.at(year) == pytest.approx(
        result.allocated_final_odc.at(year), rel=1e-6
    )


def test_u3_terafab_debt_conservation(ingest, assumptions) -> None:
    """Terafab Σdraw − Σrepay − balance = 0 with chip-transfer repayment."""
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    terafab = compute_terafab_facility(
        TerafabFacilityInputs(
            assumptions=assumptions,
            terafab_capex_to_fund=fb.chip_fab_capex,
            group_fcf=label_year_vector(ingest, CAE, "Group FCF ($mm)"),
            chip_transfer_revenue=label_year_vector(
                ingest, "AI - Compute", cl.CHIP_PURCHASES_INTERNAL_TRANSFER_MM
            ),
        )
    )
    assert terafab_debt_conservation_ok(terafab)


def test_u3_terafab_cash_neutral_end_state(ingest, assumptions) -> None:
    """Terafab project debt: ending balance ≈ 0 (principal recovered over fab life)."""
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    terafab = compute_terafab_facility(
        TerafabFacilityInputs(
            assumptions=assumptions,
            terafab_capex_to_fund=fb.chip_fab_capex,
            group_fcf=label_year_vector(ingest, CAE, "Group FCF ($mm)"),
            chip_transfer_revenue=label_year_vector(
                ingest, "AI - Compute", cl.CHIP_PURCHASES_INTERNAL_TRANSFER_MM
            ),
        )
    )
    assert terafab.balance_eoy.at(2040) == pytest.approx(0.0, abs=500.0)


def test_u3_2025_frozen_anchor(assumptions) -> None:
    """2025 seed and allocation frozen at anchor."""
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
    assert result.strategic_seed_cash is not None
    assert result.strategic_seed_cash.at(FIRST_YEAR) == pytest.approx(0.0, abs=1.0)


def test_u3_conservation_ok() -> None:
    """Full pipeline conservation green after seed + debt re-scope."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    result = run_base_case(wb, write_outputs=False)
    assert result.conservation.all_ok


def test_u3_five_times_stable() -> None:
    """5× round-trip stability — deterministic pipeline hash unchanged."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    hashes = [
        run_base_case(wb, write_outputs=False).audit["outputs_hash"] for _ in range(5)
    ]
    assert len(set(hashes)) == 1


def test_u3_r2_odc_debt_gate_still_passes(assumptions) -> None:
    """Folded ODC facility retains Σdraw−Σrepay−balance = 0 identity."""
    odc = compute_odc_facility(
        OdcFacilityInputs(
            assumptions=assumptions,
            odc_capex_need=YearVector.zeros(),
            odc_pool_allocation=YearVector.zeros(),
        )
    )
    assert np.all(odc.conservation_draw_repay_balance.values == 0.0)


def test_u3_inline_labels_scope() -> None:
    """U3-scope allocator modules use cl.* registry."""
    violations = find_inline_label_literals()
    u3_modules = {
        "allocator/strategic_seed.py",
        "allocator/debt_facilities.py",
        "allocator/brain.py",
    }
    u3_violations = [v for v in violations if any(m in v for m in u3_modules)]
    assert u3_violations == [], "\n".join(u3_violations[:15])
