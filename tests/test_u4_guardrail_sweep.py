"""Sprint U4 gate — Conservation R14 repair + supersession sweep (F6 remediation)."""

from __future__ import annotations

import importlib
from pathlib import Path

import numpy as np
import pytest

from spacex_model.calc.allocator.cash_pool import compute_bridge_drawdown, compute_ipo_drawdown
from spacex_model.calc.allocator.conservation import (
    AllocatorConservationInputs,
    compute_allocator_conservation,
    compute_r14_cash_flow_identity,
)
from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.config.settings import get_settings
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.pipeline import run_base_case
from spacex_model.linters.canonical_labels import find_inline_label_literals

REPO = Path(__file__).resolve().parents[1]
EDGE_YEARS = (2025, 2028, 2030, 2035, 2040)

SUPERSEDED_MODULES = (
    "spacex_model.calc.allocator.sigmoid_cash",
    "spacex_model.calc.allocator.sigmoid_kg",
    "spacex_model.calc.allocator.kg_rationing",
    "spacex_model.calc.allocator.water_fill",
    "spacex_model.calc.allocator.level2_split",
)


def test_u4_superseded_modules_retired() -> None:
    """§9 supersession sweep — legacy CAE shims no longer importable."""
    for name in SUPERSEDED_MODULES:
        with pytest.raises(ModuleNotFoundError):
            importlib.import_module(name)


def test_u4_r14_ok_every_year() -> None:
    """Conservation R14 green every year 2025–2040 (F6 repaired)."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    result = run_base_case(wb, write_outputs=False)
    assert result.conservation.r14_ok
    r14 = result.conservation.residuals_by_check.get("R14", {})
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        assert abs(r14.get(year, 0.0)) < 1.0, f"R14 failed {year}={r14.get(year)}"


def test_u4_allocator_identities() -> None:
    """Unified spine identities: alloc bounds, slots, deploy, leftovers."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    result = run_base_case(wb, write_outputs=False)
    assert result.conservation.allocator_ok
    for check in ("alloc_bounds", "slot_bounds", "odc_deploy_identity", "leftovers_parked"):
        assert check in result.conservation.residuals_by_check


def test_u4_r14_bridge_ipo_reconciliation() -> None:
    """R14 reconciles R11 double-count of bridge/IPO vs R8-chained cash_eoy."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    result = run_base_case(wb, write_outputs=False)
    alloc = result.allocator
    assert alloc.debt is not None
    r14 = compute_r14_cash_flow_identity(
        cash_eoy=alloc.cash_eoy,
        cash_available=alloc.cash_available_for_year,
        group_fcf=result.group_pnl.group_fcf,
        terafab_interest=alloc.debt.terafab.interest,
        terafab_repayment=alloc.debt.terafab.repayment,
        odc_draw=alloc.debt.odc.draw,
        odc_interest=alloc.debt.odc.interest,
        odc_repayment=alloc.debt.odc.repayment,
        bridge_drawdown=compute_bridge_drawdown(result.assumptions),
        ipo_drawdown=compute_ipo_drawdown(result.assumptions),
    )
    for year in EDGE_YEARS:
        assert abs(r14[year]) < 1.0


def test_u4_conservation_all_ok() -> None:
    """Full pipeline conservation green after R14 repair + supersession sweep."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    result = run_base_case(wb, write_outputs=False)
    assert result.conservation.all_ok
    for year in EDGE_YEARS:
        assert result.conservation.r108_ok_by_year[year] == "OK"


def test_u4_five_times_stable() -> None:
    """5× round-trip stability — deterministic pipeline hash unchanged."""
    wb = get_settings().workbook_path
    if not wb.exists():
        pytest.skip("V4.113 workbook not present")
    hashes = [
        run_base_case(wb, write_outputs=False).audit["outputs_hash"] for _ in range(5)
    ]
    assert len(set(hashes)) == 1


def test_u4_softmax_shares_still_diagnostic() -> None:
    """R3 xlsx diagnostic helper retained; superseded allocation path retired."""
    from spacex_model.calc.allocator.priority import compute_softmax_shares

    assert callable(compute_softmax_shares)


def test_u4_inline_labels_scope() -> None:
    """U4-scope allocator modules use cl.* registry."""
    violations = find_inline_label_literals()
    u4_modules = {
        "allocator/conservation.py",
        "allocator/brain.py",
        "allocator/debt_facilities.py",
    }
    u4_violations = [v for v in violations if any(m in v for m in u4_modules)]
    assert u4_violations == [], "\n".join(u4_violations[:15])
