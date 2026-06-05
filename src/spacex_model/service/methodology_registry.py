"""Methodology & formula registry — PRD §6 / Lineage Trust Sprint 2.

Single source for Formula panel + Sources panel fields, extracted from calc
docstrings with a curated display overlay.
"""

from __future__ import annotations

import ast
import re
import tomllib
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from spacex_model.engine.label_lookup import normalize_label
from spacex_model.linters.docstrings import (
    CALC_ROOT,
    iter_public_calc_functions,
    parse_docstring_tags,
)
from spacex_model.service.grid import _LABEL_LINEAGE
from spacex_model.service.stub_registry import PLACEHOLDER_SLUGS

_REPO_ROOT = Path(__file__).resolve().parents[3]
_OVERLAY_PATH = _REPO_ROOT / "docs" / "methodology_overlay.toml"

_SHEET_FROM_CELL = re.compile(r"^([A-Za-z][\w \-]+)!")


@dataclass(frozen=True, slots=True)
class MethodologyRecord:
    """Display-ready methodology for one lineage surface."""

    formula_expression: str
    architecture_section: str
    method_statement: str
    principle: str
    rule: str
    calc_key: str | None = None


def _sheet_from_excel_cell(excel_cell: str) -> str:
    match = _SHEET_FROM_CELL.match(excel_cell.strip())
    return match.group(1).strip() if match else ""


def _calc_key(module_path: str, function: str) -> str:
    if module_path.startswith("spacex_model."):
        module_path = module_path.removeprefix("spacex_model.")
    return f"calc.{module_path}.{function}"


def _first_architecture_section(arch_ref: str) -> str:
    token = re.search(r"§\d+(?:\.\d+)?", arch_ref)
    return token.group(0) if token else arch_ref.strip()


def _infer_formula_from_label(label: str, architecture_section: str) -> str:
    lower = label.lower()
    if "module ebitda" in lower:
        return "Module EBITDA = Total Revenue − Total COGS"
    if "module fcf" in lower:
        return "Module FCF = Module EBITDA − Module CapEx + D&A add-back"
    if "total revenue" in lower:
        return f"{label} = Σ component revenue lines"
    if "total cogs" in lower or ("cogs" in lower and "$mm" in label):
        return f"{label} = Σ direct production cost lines"
    if "gross profit" in lower:
        return "Gross Profit = Total Revenue − Total COGS"
    if "blended irr" in lower or "spot irr" in lower:
        return f"{label} = marginal IRR from unit cash flows"
    if "group ebitda" in lower:
        return "Group EBITDA = Group Gross Profit − Total OpEx"
    if "group fcf" in lower:
        return "Group FCF = NOPAT + D&A − Total Group CapEx − Mars carve-out"
    if "group revenue" in lower:
        return "Group Revenue = Σ module revenues − inter-module eliminations"
    if "cash boy" in lower or "cash eoy" in lower:
        return f"{label} = prior balance + inflows − outflows"
    if "allocated cash" in lower:
        return f"{label} = IRR-weighted share of remaining pool"
    if "capacity" in lower and "kg" in lower:
        return f"{label} = launch capacity after strategic reservations"
    if "conservation" in lower or " check" in lower:
        return f"{label} = Σ inflows − Σ outflows (must ≈ 0)"
    if "payload" in lower or "per launch" in lower:
        return f"{label} = rated payload × utilization factor"
    if "capex" in lower or "cap ex" in lower:
        return f"{label} = Σ module and corporate capital expenditure lines"
    if "opex" in lower or "op ex" in lower or "sga" in lower or "r&d" in lower:
        return f"{label} = Σ operating expense lines for the scope"
    if "depreciation" in lower or "d&a" in lower:
        return f"{label} = Σ scheduled depreciation and amortization"
    section = architecture_section or "architecture spec"
    return f"{label} = computed per {section}"


def _infer_method_statement(label: str, architecture_section: str) -> str:
    lower = label.lower()
    if "revenue" in lower:
        return "Vending-machine revenue build from unit economics and exogenous demand"
    if "cogs" in lower or "gross profit" in lower:
        return "Direct production costs only; gross profit = revenue − COGS"
    if "ebitda" in lower or "fcf" in lower:
        return "Module or group cash walk: EBITDA → CapEx → FCF"
    if "irr" in lower:
        return "Per-unit marginal IRR drives allocator priority weights"
    if "allocated" in lower or "pool" in lower:
        return "IRR-ranked cash/kg allocation after queue gate and carve-out"
    if "cash" in lower:
        return "Cash pool identity: BoY chaining with inflows and claims"
    if "capacity" in lower or "launch" in lower:
        return "Fleet and pad capacity identity from vehicle build schedule"
    return f"Computed per {architecture_section or 'Architecture & Methodology'}"


def _default_rule_for_section(section: str, section_rules: dict[str, str]) -> str:
    if section in section_rules:
        return section_rules[section]
    base = section.split(".")[0] if section else ""
    if base in section_rules:
        return section_rules[base]
    return section_rules.get(
        "default",
        "Rule 1 — One concept per write; every formula traces to its source cell",
    )


def _load_overlay() -> dict[str, object]:
    if not _OVERLAY_PATH.exists():
        return {}
    return tomllib.loads(_OVERLAY_PATH.read_text(encoding="utf-8"))


def _overlay_calc_entry(overlay: dict[str, object], calc_key: str) -> dict[str, str]:
    calc = overlay.get("calc", {})
    if isinstance(calc, dict):
        entry = calc.get(calc_key, {})
        if isinstance(entry, dict):
            return {str(k): str(v) for k, v in entry.items()}
    return {}


def _overlay_label_entry(
    overlay: dict[str, object], sheet: str, label: str
) -> dict[str, str]:
    grid = overlay.get("label", {})
    norm = normalize_label(label)
    if isinstance(grid, dict):
        sheet_bucket = grid.get(sheet, {})
        if isinstance(sheet_bucket, dict):
            entry = sheet_bucket.get(norm, {})
            if isinstance(entry, dict):
                return {str(k): str(v) for k, v in entry.items()}
    return {}


def _overlay_lineage_entry(overlay: dict[str, object], lineage_key: str) -> dict[str, str]:
    lineage = overlay.get("lineage", {})
    if isinstance(lineage, dict):
        entry = lineage.get(lineage_key, {})
        if isinstance(entry, dict):
            return {str(k): str(v) for k, v in entry.items()}
    return {}


def _merge_record(
    *,
    formula: str,
    architecture_section: str,
    principle: str,
    calc_key: str | None,
    overlay: dict[str, object],
    sheet: str = "",
    label: str = "",
    lineage_key: str = "",
) -> MethodologyRecord:
    section_rules_raw = overlay.get("section_rules", {})
    section_rules: dict[str, str] = (
        {str(k): str(v) for k, v in section_rules_raw.items()}
        if isinstance(section_rules_raw, dict)
        else {}
    )

    ovl: dict[str, str] = {}
    if calc_key:
        ovl.update(_overlay_calc_entry(overlay, calc_key))
    if sheet and label:
        ovl.update(_overlay_label_entry(overlay, sheet, label))
    if lineage_key:
        ovl.update(_overlay_lineage_entry(overlay, lineage_key))

    arch = ovl.get("architecture_section", architecture_section)
    method = ovl.get(
        "method_statement",
        _infer_method_statement(label, arch) if label else f"Method per {arch}",
    )
    rule = ovl.get("rule", _default_rule_for_section(arch, section_rules))
    formula_out = ovl.get("formula_expression", formula)
    principle_out = ovl.get("principle", principle or "—")

    return MethodologyRecord(
        formula_expression=formula_out,
        architecture_section=arch,
        method_statement=method,
        principle=principle_out,
        rule=rule,
        calc_key=calc_key,
    )


def _build_indexes() -> tuple[
    dict[str, MethodologyRecord],
    dict[tuple[str, str], MethodologyRecord],
    dict[str, MethodologyRecord],
]:
    overlay = _load_overlay()
    by_lineage: dict[str, MethodologyRecord] = {}
    by_label: dict[tuple[str, str], MethodologyRecord] = {}
    by_calc: dict[str, MethodologyRecord] = {}

    for path, node in iter_public_calc_functions():
        rel = path.relative_to(CALC_ROOT)
        module_path = "calc." + str(rel.with_suffix("")).replace("/", ".")
        doc = ast.get_docstring(node) or ""
        tags = parse_docstring_tags(doc)
        if not tags.get("formula"):
            continue

        formula = tags["formula"].split("\n")[0].strip().rstrip(".")
        arch = _first_architecture_section(tags.get("architecture_ref", ""))
        principle = tags.get("principle", "")
        ck = f"{module_path}.{node.name}"

        record = _merge_record(
            formula=formula,
            architecture_section=arch,
            principle=principle,
            calc_key=ck,
            overlay=overlay,
            label=tags.get("excel_label", ""),
            sheet=_sheet_from_excel_cell(tags.get("excel_cell", "")),
        )
        by_calc[ck] = record

        sheet = _sheet_from_excel_cell(tags.get("excel_cell", ""))
        label = tags.get("excel_label", "")
        if sheet and label:
            by_label[(sheet, normalize_label(label))] = record

    for (sheet, label), lineage_key in _LABEL_LINEAGE.items():
        norm = normalize_label(label)
        if (sheet, norm) in by_label:
            by_lineage[lineage_key] = by_label[(sheet, norm)]
        elif lineage_key not in by_lineage:
            arch = "§3"
            by_lineage[lineage_key] = _merge_record(
                formula=_infer_formula_from_label(label, arch),
                architecture_section=arch,
                principle="8 (module vending-machine framing)",
                calc_key=None,
                overlay=overlay,
                sheet=sheet,
                label=label,
                lineage_key=lineage_key,
            )

    return by_lineage, by_label, by_calc


@lru_cache(maxsize=1)
def get_methodology_indexes() -> tuple[
    dict[str, MethodologyRecord],
    dict[tuple[str, str], MethodologyRecord],
    dict[str, MethodologyRecord],
]:
    return _build_indexes()


def _strip_year_from_grid_key(key: str) -> str:
    parts = key.split(".")
    if len(parts) >= 4 and parts[0] == "grid" and parts[-1].isdigit():
        return ".".join(parts[:-1])
    return key


def lookup_methodology(
    lineage_key: str,
    *,
    sheet: str | None = None,
    label: str | None = None,
    section_ref: str | None = None,
) -> MethodologyRecord | None:
    """Resolve methodology for a lineage key (year-suffixed grid keys supported)."""
    by_lineage, by_label, _ = get_methodology_indexes()
    overlay = _load_overlay()

    if lineage_key in by_lineage:
        return by_lineage[lineage_key]

    ovl = _overlay_lineage_entry(overlay, lineage_key)
    if ovl.get("formula_expression"):
        return _merge_record(
            formula=ovl["formula_expression"],
            architecture_section=ovl.get("architecture_section", section_ref or "§3"),
            principle=ovl.get("principle", "—"),
            calc_key=None,
            overlay=overlay,
            sheet=sheet or "",
            label=label or "",
            lineage_key=lineage_key,
        )

    base_key = _strip_year_from_grid_key(lineage_key)
    if base_key != lineage_key and base_key in by_lineage:
        return by_lineage[base_key]

    if sheet and label:
        hit = by_label.get((sheet, normalize_label(label)))
        if hit:
            return hit
        arch = section_ref or "§3"
        if section_ref and section_ref.startswith("§"):
            arch = _first_architecture_section(section_ref)
        default_principle = "8 (vending-machine module framing)"
        if "allocator" in (lineage_key or "") or sheet == "Cash Allocation Engine":
            default_principle = "4 (cash queue gate reserves non-module claims)"
        elif "group" in (lineage_key or "").lower() or sheet == "Group P&L":
            default_principle = "9 (internal flows eliminate at Group P&L)"
        return _merge_record(
            formula=_infer_formula_from_label(label, arch),
            architecture_section=arch,
            principle=default_principle,
            calc_key=None,
            overlay=overlay,
            sheet=sheet,
            label=label,
            lineage_key=lineage_key,
        )

    return None


def iter_non_stub_derived_row_keys(
    result: object,
) -> list[tuple[str, str, str, int, str]]:
    """Yield (lineage_key, sheet, slug, row, label) for each derived non-stub grid row."""
    from spacex_model.service.grid import build_grid_payload
    from spacex_model.service.sheets_meta import SHEETS

    rows_out: list[tuple[str, str, str, int, str]] = []
    for meta in SHEETS:
        if meta.slug in PLACEHOLDER_SLUGS or meta.slug == "run_audit":
            continue
        grid = build_grid_payload(meta, result)  # type: ignore[arg-type]
        for row in grid["rows"]:
            if row.get("is_header"):
                continue
            if row["cell_kinds"][0] != "derived":
                continue
            lineage_key = row["lineage_keys"][0]
            rows_out.append(
                (
                    lineage_key,
                    meta.source_sheet,
                    meta.slug,
                    int(row["row_index"]),
                    str(row["label"]),
                )
            )
    return rows_out


def clear_methodology_cache() -> None:
    """Invalidate cached registry (tests)."""
    get_methodology_indexes.cache_clear()
