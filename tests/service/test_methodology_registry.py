"""Sprint 2 — methodology & formula registry acceptance."""

from __future__ import annotations

from typing import Any

import pytest

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_base_case
from spacex_model.linters.docstrings import find_missing_formula_tags
from spacex_model.service.methodology_registry import (
    clear_methodology_cache,
    iter_non_stub_derived_row_keys,
    lookup_methodology,
)
from spacex_model.service.sheets_meta import SHEETS
from spacex_model.service.stub_registry import PLACEHOLDER_SLUGS


@pytest.fixture(scope="module")
def base_result() -> Any:
    workbook = get_settings().workbook_path
    if not workbook.exists():
        pytest.skip(f"workbook not found: {workbook}")
    return run_base_case(workbook, write_outputs=False)


def test_docstring_formula_coverage_gate() -> None:
    """Every public calc function carries a Formula: tag."""
    violations = find_missing_formula_tags()
    assert violations == [], "\n".join(violations[:30])


def test_non_stub_derived_rows_resolve_methodology(base_result: Any) -> None:
    """Every derived non-stub grid row resolves formula, principle, rule; principle ≠ rule."""
    clear_methodology_cache()
    missing: list[str] = []
    bad_principle_rule: list[str] = []
    placeholder_formulas: list[str] = []

    for lineage_key, sheet, _slug, _row, label in iter_non_stub_derived_row_keys(base_result):
        rec = lookup_methodology(lineage_key, sheet=sheet, label=label)
        if rec is None:
            missing.append(f"{lineage_key} ({label[:40]})")
            continue
        if not rec.formula_expression.strip():
            missing.append(f"{lineage_key}: empty formula")
        if not rec.principle.strip() or rec.principle == "—":
            missing.append(f"{lineage_key}: empty principle")
        if not rec.rule.strip() or rec.rule == "—":
            missing.append(f"{lineage_key}: empty rule")
        if rec.principle.strip() == rec.rule.strip():
            bad_principle_rule.append(lineage_key)
        formula_lower = rec.formula_expression.lower()
        if "see architecture" in formula_lower:
            placeholder_formulas.append(lineage_key)

    assert missing == [], f"missing methodology ({len(missing)}): {missing[:15]}"
    assert bad_principle_rule == [], f"principle == rule: {bad_principle_rule[:15]}"
    assert placeholder_formulas == [], f"placeholder formulas: {placeholder_formulas[:15]}"


def test_sampled_mapped_lineage_keys(base_result: Any) -> None:
    """Mapped module/group keys resolve with real expressions."""
    clear_methodology_cache()
    samples = [
        "group.group_revenue_net",
        "group.group_ebitda",
        "module.starlink.total_revenue",
        "module.starlink.module_fcf",
    ]
    for key in samples:
        rec = lookup_methodology(key)
        assert rec is not None, key
        assert any(op in rec.formula_expression for op in ("=", "−", "-", "+", "Σ"))
        assert rec.principle != rec.rule


def test_at_least_one_derived_row_per_non_placeholder_sheet(base_result: Any) -> None:
    """Registry resolves ≥1 derived row per active sheet."""
    clear_methodology_cache()
    checked: set[str] = set()
    for lineage_key, sheet, slug, _row, label in iter_non_stub_derived_row_keys(base_result):
        if slug in checked:
            continue
        rec = lookup_methodology(lineage_key, sheet=sheet, label=label)
        assert rec is not None
        assert rec.formula_expression
        checked.add(slug)

    expected = {
        m.slug
        for m in SHEETS
        if m.slug not in PLACEHOLDER_SLUGS and m.slug not in {"run_audit", "assumptions"}
    }
    assert checked == expected, f"missing sheets: {expected - checked}"
