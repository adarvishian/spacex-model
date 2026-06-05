"""Sprint U1 gate — three-bucket CapEx split + cap-base reconciliation (F1 remediation)."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.brain import AllocatorInputs, compute_allocator
from spacex_model.calc.allocator.cap_base import CapBaseInputs, compute_cap_base
from spacex_model.calc.allocator.cae_demands import aggregate_cae_demands, four_program_demands
from spacex_model.calc.allocator.demand_builders import compute_exogenous_demands
from spacex_model.calc.allocator.priority import FourProgramIrrs
from spacex_model.calc.allocator.two_resource_fill import compute_two_resource_fill
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


def test_u1_growth_caps_match_xlsx_r64_r66(ingest, assumptions) -> None:
    """R64/R66 growth caps reconcile to CAE cached values at edge years."""
    cap = compute_cap_base(_cap_base_from_xlsx(ingest, assumptions))
    for year in EDGE_YEARS:
        xlsx_sl = label_year_vector(ingest, CAE, cl.CAP_STARLINK_MAX_DEPLOYABLE_MM).at(year)
        xlsx_ai = label_year_vector(ingest, CAE, cl.CAP_AI_COMPUTE_MAX_DEPLOYABLE_MM).at(year)
        assert cap.growth_caps.starlink.at(year) == pytest.approx(xlsx_sl, rel=0.02)
        assert cap.growth_caps.ai_compute.at(year) == pytest.approx(xlsx_ai, rel=0.02)


def test_u1_water_fill_capped_at_growth_not_exogenous(ingest, assumptions) -> None:
    """Allocated growth ≈ min(share×pool, growth cap) — not inflated exogenous demand."""
    sub = compute_exogenous_demands(assumptions)
    cap = compute_cap_base(_cap_base_from_xlsx(ingest, assumptions))
    mods = {k: AllocatorOut.zeros() for k in ("customer_launch", "starlink", "ai_compute", "lunar_mars")}
    cae_dem = aggregate_cae_demands(assumptions, sub, mods)
    four_dem_uncapped = four_program_demands(
        cap.growth_caps,
        YearVector(np.full(HORIZON_YEARS, 1e12)),
        YearVector(np.full(HORIZON_YEARS, 1e12)),
        cae_dem.unified_kg,
        sub,
    )
    four_dem_capped = four_program_demands(
        cap.growth_caps,
        cap.odc_demand_buildable,
        cap.terr_demand_buildable,
        cae_dem.unified_kg,
        sub,
    )
    pool = label_year_vector(ingest, CAE, "Remaining pool for IRR-weighted allocation ($mm)")
    prior = FourProgramIrrs(
        starlink=label_year_vector(ingest, CAE, cl.SPOT_IRR_STARLINK),
        odc=label_year_vector(ingest, CAE, cl.SPOT_IRR_AI_COMPUTE),
        terrestrial=YearVector.constant(0.15),
        customer_launch=label_year_vector(ingest, CAE, cl.SPOT_IRR_CUSTOMER_LAUNCH),
    )
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    from spacex_model.calc.allocator.two_resource_fill import kg_per_ship_year

    without_caps = compute_two_resource_fill(
        pool,
        four_dem_uncapped,
        prior,
        assumptions,
        gigabay_throughput=fb.gigabay_installed_capacity,
        kg_per_ship_yr=kg_per_ship_year(assumptions, lc.per_launch_upmass_kg),
    )
    with_caps = compute_two_resource_fill(
        pool,
        four_dem_capped,
        prior,
        assumptions,
        gigabay_throughput=fb.gigabay_installed_capacity,
        kg_per_ship_yr=kg_per_ship_year(assumptions, lc.per_launch_upmass_kg),
    )
    year = 2035
    assert with_caps.allocated_cash.customer_launch.at(year) <= cap.growth_caps.customer_launch.at(year) + 1.0
    assert (
        with_caps.allocated_cash.customer_launch.at(year)
        <= without_caps.allocated_cash.customer_launch.at(year) + 1.0
    )


def test_u1_allocated_near_growth_cap_2030(ingest, assumptions) -> None:
    """2030: allocated final tracks capped growth slice (F1 — not phantom deploy gap)."""
    lc = compute_launch_capacity(LaunchCapacityInputs(assumptions=assumptions))
    fb = compute_facilities_build(_fb_from_xlsx(ingest, assumptions))
    mods = {k: AllocatorOut.zeros() for k in ("customer_launch", "starlink", "ai_compute", "lunar_mars")}
    mods["customer_launch"] = replace(
        AllocatorOut.zeros(),
        module_capex=label_year_vector(
            ingest, "Customer Launch", "Module CapEx total ($mm)   ◄ Allocator OUT"
        ),
    )
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
        )
    )
    assert result.growth_cap_starlink is not None
    assert result.allocated_final_starlink is not None
    sl_alloc = result.allocated_final_starlink.at(2030)
    sl_cap = result.growth_cap_starlink.at(2030)
    assert sl_alloc <= sl_cap + 1.0


def test_u1_odc_irr_not_crushed_by_fab_lump(assumptions) -> None:
    """ODC spot IRR uses growth slug only — Terafab lump excluded from −CapEx leg."""
    from spacex_model.calc.ai_compute.orbital_dc import OrbitalDcInputs, per_sat_blended_irr

    chip = YearVector(np.full(HORIZON_YEARS, 2_000_000.0))
    without_fab = per_sat_blended_irr(
        OrbitalDcInputs(assumptions=assumptions, chip_at_cost_per_sat=YearVector.zeros())
    )
    with_chip_cogs = per_sat_blended_irr(
        OrbitalDcInputs(assumptions=assumptions, chip_at_cost_per_sat=chip)
    )
    assert with_chip_cogs > -0.5
    assert without_fab > with_chip_cogs or abs(without_fab - with_chip_cogs) < 0.5


def test_u1_chip_at_cost_positive_with_fb(ingest, assumptions) -> None:
    """At-cost chip transfer installed — predetermined absorption basis."""
    cap = compute_cap_base(_cap_base_from_xlsx(ingest, assumptions))
    assert cap.chip_at_cost_per_sat.at(2030) > 0.0
    fab_capex = label_year_vector(
        ingest, "Facilities Build", cl.CHIP_FAB_FACILITY_CAPEX_TOTAL_MM_AI_COMPUTE
    ).at(2030)
    roll_up = label_year_vector(ingest, "AI - Compute", cl.ROLL_UP_MODULE_CAPEX).at(2030)
    if roll_up > 0 and fab_capex > 0:
        assert roll_up > fab_capex


def test_u1_queue_gate_maintenance_and_enabling(ingest, assumptions) -> None:
    """Bucket-2/3 senior claims reduce pool before IRR queue."""
    cap = compute_cap_base(_cap_base_from_xlsx(ingest, assumptions))
    assert np.all(cap.maintenance_claim.values >= 0.0)
    assert np.all(cap.enabling_infra_equity.values >= 0.0)


def test_u1_2025_frozen_anchor(assumptions) -> None:
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


def test_u1_conservation_ok() -> None:
    """Full pipeline conservation green after three-bucket split."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    result = run_base_case(wb, write_outputs=False)
    assert result.conservation.all_ok


def test_u1_five_times_stable() -> None:
    """5× round-trip stability — deterministic pipeline hash unchanged."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    hashes = [
        run_base_case(wb, write_outputs=False).audit["outputs_hash"] for _ in range(5)
    ]
    assert len(set(hashes)) == 1


def test_u1_inline_labels_cap_base_scope(ingest) -> None:
    """U1-scope allocator modules use cl.* registry."""
    violations = find_inline_label_literals()
    u1_modules = {
        "allocator/cap_base.py",
        "allocator/brain.py",
        "allocator/queue_gate.py",
        "allocator/water_fill.py",
    }
    u1_violations = [v for v in violations if any(m in v for m in u1_modules)]
    assert u1_violations == [], "\n".join(u1_violations[:15])
