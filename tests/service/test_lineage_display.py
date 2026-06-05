"""Sprint 3 — L2 + L4 formula display & Sources panel acceptance."""

from __future__ import annotations

import json
import math
import re
from typing import Any

import pytest

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_base_case
from spacex_model.service.grid import build_grid_payload
from spacex_model.service.lineage_enrich import enrich_lineage
from spacex_model.service.sheets_meta import SHEETS
from spacex_model.service.stub_registry import PLACEHOLDER_SLUGS

_FORMULA_OPS = ("=", "−", "-", "+", "Σ", "×")


def _finite(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def _formula_has_operator(formula: str) -> bool:
    return any(op in formula for op in _FORMULA_OPS)


def _operand_overlap(formula: str, resolved_inputs: list[dict[str, Any]]) -> bool:
    """True when at least one resolved-input label token appears in the formula."""
    if not resolved_inputs:
        return True
    rhs = formula.split("=", 1)[-1].lower()
    for ri in resolved_inputs:
        label = str(ri.get("label", "")).lower()
        tokens = [t for t in re.split(r"[\s$()]+", label) if len(t) > 3]
        if any(t in rhs for t in tokens):
            return True
    return len(resolved_inputs) == 0


@pytest.fixture(scope="module")
def base_result() -> Any:
    workbook = get_settings().workbook_path
    if not workbook.exists():
        pytest.skip(f"workbook not found: {workbook}")
    return run_base_case(workbook, write_outputs=False)


def test_sources_payload_never_contains_code_paths(base_result: Any) -> None:
    """Sources methodology must not expose Python module paths."""
    violations: list[str] = []

    for meta in SHEETS:
        if meta.slug in PLACEHOLDER_SLUGS or meta.slug == "run_audit":
            continue
        grid = build_grid_payload(meta, base_result)
        for row in grid["rows"]:
            if row.get("is_header"):
                continue
            for year_idx, year in enumerate(grid["years"]):
                if row["cell_kinds"][year_idx] != "derived":
                    continue
                enriched = enrich_lineage(
                    row["lineage_keys"][year_idx],
                    base_result,
                    year=year,
                    sheet=meta.source_sheet,
                    row=row["row_index"],
                    sheet_slug=meta.slug,
                )
                sources_blob = json.dumps(enriched.get("sources", {}))
                if "spacex_model." in sources_blob:
                    violations.append(f"{meta.slug}!R{row['row_index']} {year}")

    assert violations == [], f"code paths in sources ({len(violations)}): {violations[:10]}"


def test_sampled_derived_formula_and_sources_per_sheet(base_result: Any) -> None:
    """Derived cells: real formula, concrete spec section, distinct principle/rule."""
    checked: set[str] = set()
    bad_formulas: list[str] = []
    bad_sources: list[str] = []

    for meta in SHEETS:
        if meta.slug in PLACEHOLDER_SLUGS or meta.slug == "run_audit":
            continue
        grid = build_grid_payload(meta, base_result)
        for row in grid["rows"]:
            if row.get("is_header"):
                continue
            for year_idx, year in enumerate(grid["years"]):
                if meta.slug in checked:
                    break
                if row["cell_kinds"][year_idx] != "derived":
                    continue
                display = row["year_values"][year_idx]
                if not _finite(display):
                    continue

                enriched = enrich_lineage(
                    row["lineage_keys"][year_idx],
                    base_result,
                    year=year,
                    sheet=meta.source_sheet,
                    row=row["row_index"],
                    sheet_slug=meta.slug,
                )
                formula = enriched.get("formula_expression", "")
                if "see architecture" in formula.lower():
                    bad_formulas.append(f"{meta.slug}: {formula[:60]}")
                if not _formula_has_operator(formula):
                    bad_formulas.append(f"{meta.slug}: no operator in {formula[:60]}")

                sources = enriched.get("sources") or {}
                meth = sources.get("methodology") or {}
                spec = str(meth.get("spec_section", ""))
                if not spec.startswith("§"):
                    bad_sources.append(f"{meta.slug}: spec_section={spec!r}")
                if meth.get("principle") == meth.get("rule"):
                    bad_sources.append(f"{meta.slug}: principle == rule")
                if "module" in meth:
                    bad_sources.append(f"{meta.slug}: module field present")
                if not meth.get("method_statement"):
                    bad_sources.append(f"{meta.slug}: missing method_statement")

                resolved = enriched.get("resolved_inputs") or []
                if not _operand_overlap(formula, resolved):
                    bad_sources.append(
                        f"{meta.slug}: formula operands mismatch resolved_inputs"
                    )

                checked.add(meta.slug)
                break

    expected = {
        m.slug
        for m in SHEETS
        if m.slug not in PLACEHOLDER_SLUGS and m.slug not in {"run_audit", "assumptions"}
    }
    assert checked == expected, f"missing sheets: {expected - checked}"
    assert bad_formulas == [], bad_formulas[:10]
    assert bad_sources == [], bad_sources[:10]


def test_stub_cells_allow_architecture_placeholder(base_result: Any) -> None:
    """Stub registry cells may use the Architecture placeholder formula."""
    found_stub = False
    for meta in SHEETS:
        if meta.slug not in PLACEHOLDER_SLUGS:
            continue
        grid = build_grid_payload(meta, base_result)
        for row in grid["rows"]:
            if row.get("is_header"):
                continue
            if row["cell_kinds"][0] != "stub":
                continue
            enriched = enrich_lineage(
                row["lineage_keys"][0],
                base_result,
                year=grid["years"][0],
                sheet=meta.source_sheet,
                row=row["row_index"],
                sheet_slug=meta.slug,
            )
            assert enriched["cell_kind"] == "stub"
            assert "see architecture" in enriched["formula_expression"].lower()
            found_stub = True
            break
        if found_stub:
            break
    assert found_stub, "expected at least one stub cell in placeholder tabs"
