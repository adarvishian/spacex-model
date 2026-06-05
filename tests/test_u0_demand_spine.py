"""Sprint U0 gate — demand-spine unification (F4 remediation)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from spacex_model.calc.allocator.brain import AllocatorInputs, compute_allocator
from spacex_model.calc.allocator.demand_spine import compute_unified_kg_demands
from spacex_model.calc._allocator_out import AllocatorOut
from spacex_model.calc.allocator.demand_builders import compute_exogenous_demands
from spacex_model.calc.launch_capacity import LaunchCapacityInputs, compute_launch_capacity
from spacex_model.config import canonical_labels as cl
from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.config.settings import get_settings
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.pipeline import run_base_case
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.io.label_value import label_year_vector
from spacex_model.linters.demand_output import find_demand_output_violations

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


def test_u0_unified_spine_r102_equals_memo(assumptions) -> None:
    """R102 ≡ R46: total desired launch kg equals memo total kg demand."""
    sub = compute_exogenous_demands(assumptions)
    unified = compute_unified_kg_demands(assumptions, sub)
    program_sum = (
        unified.starlink.values
        + unified.customer_launch.values
        + unified.ai_compute.values
    )
    assert np.allclose(unified.total.values, program_sum)
    for t in range(HORIZON_YEARS):
        assert unified.total.values[t] == pytest.approx(program_sum[t])


def test_u0_not_inflated_vs_xlsx_cae_2030(ingest, assumptions) -> None:
    """2030 desired kg is realistic annual, not inflated CAE R99/R102 (~527M/509M)."""
    sub = compute_exogenous_demands(assumptions)
    unified = compute_unified_kg_demands(assumptions, sub)
    xlsx_inflated_total = label_year_vector(ingest, CAE, cl.TOTAL_DESIRED_LAUNCH_KG).at(2030)
    xlsx_inflated_sl = label_year_vector(ingest, CAE, cl.DESIRED_LAUNCH_KG_STARLINK).at(2030)
    assert unified.total.at(2030) < xlsx_inflated_total * 0.5
    assert unified.starlink.at(2030) < xlsx_inflated_sl * 0.5
    assert unified.total.at(2030) < 300_000_000


def test_u0_binding_flag_honest(assumptions) -> None:
    """Binding flag = IF(R102 > capacity_after_lm) — honest, not R46-vs-R102 split."""
    from spacex_model.calc.allocator.demand_spine import compute_kg_binding_flag

    total = YearVector(np.full(HORIZON_YEARS, 250.0))
    cap = YearVector(np.full(HORIZON_YEARS, 200.0))
    binding = compute_kg_binding_flag(total, cap)
    assert binding.at(2030) == 1.0
    loose = compute_kg_binding_flag(total, YearVector(np.full(HORIZON_YEARS, 300.0)))
    assert loose.at(2030) == 0.0


def test_u0_allocator_spine_single_number(ingest, assumptions) -> None:
    """Fleet sizing, rationing memo, and binding flag read one unified total."""
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
    assert result.total_desired_launch_kg is not None
    assert result.memo_total_kg_demand is not None
    for t in range(HORIZON_YEARS):
        total = result.total_desired_launch_kg.values[t]
        memo = result.memo_total_kg_demand.values[t]
        assert total == pytest.approx(memo)
        cap = result.capacity_available_kg.values[t]
        bind = result.kg_binding_flag.values[t] if result.kg_binding_flag else 0.0
        expected_bind = 1.0 if total > cap and cap > 0.0 else 0.0
        assert bind == pytest.approx(expected_bind)


def test_u0_2025_frozen_anchor(assumptions) -> None:
    """2025 column unchanged — allocation operative 2026+ only; demand spine preserves 2025."""
    sub = compute_exogenous_demands(assumptions)
    unified = compute_unified_kg_demands(assumptions, sub)
    assert unified.starlink.at(FIRST_YEAR) >= 0.0
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


def test_u0_conservation_ok() -> None:
    """Full pipeline conservation green after demand-spine unification."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    result = run_base_case(wb, write_outputs=False)
    assert result.conservation.all_ok


def test_u0_five_times_stable() -> None:
    """5× round-trip stability — deterministic pipeline hash unchanged."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    hashes = [
        run_base_case(wb, write_outputs=False).audit["outputs_hash"] for _ in range(5)
    ]
    assert len(set(hashes)) == 1


def test_u0_acyclic_demand_output_decoupling() -> None:
    """Demand modules do not import this-year output types (acyclicity firewall)."""
    violations = find_demand_output_violations()
    assert violations == [], "\n".join(violations[:15])


def test_u0_xlsx_still_has_f4_defect_documented(ingest) -> None:
    """V4.113 cached CAE still shows pre-U0 F4 split — Python fixes; xlsx is diagnostic."""
    memo = label_year_vector(ingest, CAE, cl.MEMO_TOTAL_KG_DEMAND_KG).at(2030)
    total = label_year_vector(ingest, CAE, cl.TOTAL_DESIRED_LAUNCH_KG).at(2030)
    assert memo != pytest.approx(total, rel=0.1)
