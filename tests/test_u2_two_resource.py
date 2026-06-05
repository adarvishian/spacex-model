"""Sprint U2 gate — unified two-resource allocator (F2 remediation)."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.brain import AllocatorInputs, compute_allocator
from spacex_model.calc.allocator.cae_demands import aggregate_cae_demands, four_program_demands
from spacex_model.calc.allocator.cap_base import CapBaseInputs, compute_cap_base
from spacex_model.calc.allocator.demand_builders import compute_exogenous_demands
from spacex_model.calc.allocator.irr_display import compute_four_program_prior_irrs
from spacex_model.calc.allocator.priority import ModuleSpotIrrs
from spacex_model.calc.allocator.priority import (
    FourProgramIrrs,
    ModuleSpotIrrs,
    compute_soft_floor_shares,
    compute_two_year_avg_prior_irr,
)
from spacex_model.calc.allocator.two_resource_fill import (
    compute_two_resource_fill,
    kg_per_ship_year,
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


def _cap_base_from_xlsx(ingest, assumptions) -> CapBaseInputs:
    sub = compute_exogenous_demands(assumptions)
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    mods = {k: AllocatorOut.zeros() for k in ("customer_launch", "starlink", "ai_compute", "lunar_mars")}
    return CapBaseInputs(
        assumptions=assumptions,
        sub_demands=sub,
        module_outputs=mods,
        facilities_build=fb,
        starlink_headroom_sats=label_year_vector(
            ingest, "Starlink", cl.DEMAND_SATURATION_DEPLOYMENT_HEADROOM_SATS
        ),
        starlink_blended_slug_mm=label_year_vector(
            ingest,
            "Starlink",
            cl.BLENDED_NEW_SAT_CAPEX_SLUG_MM_SAT_MEMO_ONLY_FEEDS_CAE_R88_CAP_NO_LONGER_DRIVES_DEPLOYMENT,
        ),
        odc_target_sats=label_year_vector(ingest, "AI - Compute", "Sats added (target)"),
        terr_target_mw=label_year_vector(ingest, "AI - Compute", "Memo: Terr MW demand-implied (pre-cash)"),
        odc_demand_buildable_override=label_year_vector(
            ingest, "AI - Compute", cl.ODC_DEMAND_BUILDABLE_CAPEX_MM
        ),
        terr_demand_buildable_override=label_year_vector(
            ingest, "AI - Compute", cl.TERR_DEMAND_BUILDABLE_CAPEX_MM
        ),
    )


def _allocator_result(ingest, assumptions):
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    mods = {k: AllocatorOut.zeros() for k in ("customer_launch", "starlink", "ai_compute", "lunar_mars")}
    mods["customer_launch"] = replace(
        AllocatorOut.zeros(),
        module_capex=label_year_vector(
            ingest, "Customer Launch", "Module CapEx total ($mm)   ◄ Allocator OUT"
        ),
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
        )
    )


def test_u2_four_program_soft_floor_shares_sum_to_one(assumptions) -> None:
    """Four-program shares respect 5% floor and sum to 1."""
    prior = FourProgramIrrs(
        starlink=YearVector.constant(0.25),
        odc=YearVector.constant(0.35),
        terrestrial=YearVector.constant(0.15),
        customer_launch=YearVector.constant(0.10),
    )
    avg = compute_two_year_avg_prior_irr(prior)
    shares = compute_soft_floor_shares(avg, assumptions)
    year = 2030
    total = (
        shares.starlink.at(year)
        + shares.odc.at(year)
        + shares.terrestrial.at(year)
        + shares.customer_launch.at(year)
    )
    assert total == pytest.approx(1.0, abs=1e-6)
    assert shares.customer_launch.at(year) >= 0.05


def test_u2_alloc_sum_le_pool(ingest, assumptions) -> None:
    """Σ allocated cash ≤ remaining pool every year."""
    result = _allocator_result(ingest, assumptions)
    assert result.remaining_pool is not None
    for t in range(HORIZON_YEARS):
        pool = result.remaining_pool.values[t]
        total = sum(
            getattr(result.cash, f).values[t]
            for f in result.cash.__dataclass_fields__
            if f != "as_tuple"
        )
        assert total <= pool + 1.0


def test_u2_ship_slots_le_gigabay(ingest, assumptions) -> None:
    """Σ ship slots used ≤ Gigabay throughput."""
    result = _allocator_result(ingest, assumptions)
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    assert result.ship_slots_used is not None
    for year in EDGE_YEARS:
        if year == FIRST_YEAR:
            continue
        cap = fb.gigabay_installed_capacity.at(year)
        used = result.ship_slots_used.at(year)
        assert used <= cap + 0.01


def test_u2_cl_share_never_dominates_2030(assumptions) -> None:
    """F2 fix: high-IRR CL with tiny absorbable demand cannot take ~80% capped share."""
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    prior = FourProgramIrrs(
        starlink=YearVector.constant(0.20),
        odc=YearVector.constant(0.20),
        terrestrial=YearVector.constant(0.15),
        customer_launch=YearVector.constant(0.60),
    )
    four_dem = four_program_demands(
        ModuleSpotIrrs(
            starlink=YearVector.constant(50_000.0),
            customer_launch=YearVector.constant(500.0),
            ai_compute=YearVector.constant(30_000.0),
        ),
        YearVector.constant(20_000.0),
        YearVector.constant(10_000.0),
        aggregate_cae_demands(assumptions, compute_exogenous_demands(assumptions), {}).unified_kg,
        compute_exogenous_demands(assumptions),
    )
    pool = YearVector.constant(100_000.0)
    fb_cap = YearVector.constant(50.0)
    fill = compute_two_resource_fill(
        pool,
        four_dem,
        prior,
        assumptions,
        gigabay_throughput=fb_cap,
        kg_per_ship_yr=kg_per_ship_year(assumptions, lc.per_launch_upmass_kg),
    )
    assert fill.capped_shares.customer_launch.at(2030) < 0.80
    assert fill.capped_shares.starlink.at(2030) > 0.10


def test_u2_cash_kg_reconciled_not_independent(ingest, assumptions) -> None:
    """Cash and kg allocation share one pass — kg tracks cash binding (F2 fixed)."""
    result = _allocator_result(ingest, assumptions)
    year = 2030
    cl_cash = result.allocated_final_customer_launch.at(year) if result.allocated_final_customer_launch else 0.0
    cl_kg = result.kg.customer_launch.at(year)
    sl_cash = result.allocated_final_starlink.at(year) if result.allocated_final_starlink else 0.0
    sl_kg = result.kg.starlink_v3_bb.at(year) + result.kg.starlink_v3_dtc.at(year)
    sub = compute_exogenous_demands(assumptions)
    unified = aggregate_cae_demands(assumptions, sub, {}).unified_kg
    if cl_cash < 1.0:
        assert cl_kg < unified.customer_launch.at(year) * 0.5 + 1.0
    if sl_cash > 100.0:
        assert sl_kg > 0.0


def test_u2_negative_irr_floor_only(assumptions) -> None:
    """F3: negative-IRR program gets floor share only, not softmax overweight."""
    prior = FourProgramIrrs(
        starlink=YearVector.constant(0.30),
        odc=YearVector.constant(0.30),
        terrestrial=YearVector.constant(0.30),
        customer_launch=YearVector.constant(-0.50),
    )
    shares = compute_soft_floor_shares(compute_two_year_avg_prior_irr(prior), assumptions)
    assert shares.customer_launch.at(2030) == pytest.approx(0.05, abs=0.01)


def test_u2_four_program_prior_irrs_distinct(ingest, assumptions) -> None:
    """ODC and Terrestrial are first-class — not AI roll-up."""
    mods = {k: AllocatorOut.zeros() for k in ("customer_launch", "starlink", "ai_compute", "lunar_mars")}
    mods["ai_compute"] = replace(
        AllocatorOut.zeros(),
        spot_irr=label_year_vector(ingest, CAE, cl.SPOT_IRR_ODC_PRIOR_YR),
    )
    prior = compute_four_program_prior_irrs(mods, assumptions)
    assert prior.odc.at(2030) != prior.terrestrial.at(2030)


def test_u2_kg_not_pro_rata_vs_cash(ingest, assumptions) -> None:
    """U2 supersedes pro-rata kg — cash-heavy program gets matching kg when slot-bound."""
    cap = compute_cap_base(_cap_base_from_xlsx(ingest, assumptions))
    sub = compute_exogenous_demands(assumptions)
    cae_dem = aggregate_cae_demands(assumptions, sub, {})
    four_dem = four_program_demands(
        cap.growth_caps,
        cap.odc_demand_buildable,
        cap.terr_demand_buildable,
        cae_dem.unified_kg,
        sub,
    )
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    prior = FourProgramIrrs(
        starlink=YearVector.constant(0.40),
        odc=YearVector.constant(0.30),
        terrestrial=YearVector.constant(0.20),
        customer_launch=YearVector.constant(0.05),
    )
    pool = YearVector(np.full(HORIZON_YEARS, 10_000.0))
    fill = compute_two_resource_fill(
        pool,
        four_dem,
        prior,
        assumptions,
        gigabay_throughput=fb.gigabay_installed_capacity,
        kg_per_ship_yr=kg_per_ship_year(assumptions, lc.per_launch_upmass_kg),
    )
    year = 2030

    def _pro_rata_kg(desired: ModuleSpotIrrs, cap_kg: float) -> float:
        dem = desired.starlink.at(year) + desired.customer_launch.at(year) + desired.ai_compute.at(year)
        if dem <= 0.0 or cap_kg <= 0.0:
            return 0.0
        return cap_kg * desired.customer_launch.at(year) / dem

    pro_rata_cl_kg = _pro_rata_kg(cae_dem.kg, lc.total_annual_capacity_kg.at(year))
    unified_cl_kg = fill.allocated_kg.customer_launch.at(year)
    assert unified_cl_kg != pytest.approx(pro_rata_cl_kg, rel=0.05) or fill.allocated_cash.customer_launch.at(year) < 100.0


def test_u2_2025_frozen_anchor(assumptions) -> None:
    """2025 column unchanged — allocation operative 2026+ only."""
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
    total_cash = sum(
        getattr(result.cash, f).at(FIRST_YEAR)
        for f in result.cash.__dataclass_fields__
        if f != "as_tuple"
    )
    assert total_cash == pytest.approx(0.0, abs=1.0)


def test_u2_conservation_ok() -> None:
    """Full pipeline conservation green after two-resource allocator."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    result = run_base_case(wb, write_outputs=False)
    assert result.conservation.all_ok


def test_u2_five_times_stable() -> None:
    """5× round-trip stability — deterministic pipeline hash unchanged."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    hashes = [
        run_base_case(wb, write_outputs=False).audit["outputs_hash"] for _ in range(5)
    ]
    assert len(set(hashes)) == 1


def test_u2_inline_labels_scope() -> None:
    """U2-scope allocator modules use cl.* registry."""
    violations = find_inline_label_literals()
    u2_modules = {
        "allocator/two_resource_fill.py",
        "allocator/brain.py",
        "allocator/priority.py",
        "allocator/irr_display.py",
        "allocator/cae_demands.py",
    }
    u2_violations = [v for v in violations if any(m in v for m in u2_modules)]
    assert u2_violations == [], "\n".join(u2_violations[:15])
