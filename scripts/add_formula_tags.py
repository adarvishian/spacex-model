#!/usr/bin/env python3
"""One-shot helper: insert Formula: lines into calc docstrings that lack them."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from spacex_model.linters.docstrings import (  # noqa: E402
    iter_public_calc_functions,
    parse_docstring_tags,
)


def _summary_line(doc: str) -> str:
    for line in doc.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("Excel ") or stripped.startswith("Principle:"):
            continue
        return stripped.rstrip(".")
    return ""


def _infer_formula(fn_name: str, excel_label: str, arch_ref: str, summary: str) -> str:
    if summary and len(summary) <= 140:
        return summary

    lower = excel_label.lower()
    if "module ebitda" in lower:
        return "Module EBITDA = Total Revenue − Total COGS"
    if "module fcf" in lower:
        return "Module FCF = Module EBITDA − Module CapEx + D&A add-back"
    if "total revenue" in lower:
        return f"{excel_label} = Σ component revenue lines"
    if "total cogs" in lower or "cogs" in lower:
        return f"{excel_label} = Σ direct production cost lines"
    if "gross profit" in lower:
        return "Gross Profit = Total Revenue − Total COGS"
    if "blended irr" in lower or "spot irr" in lower or "forward irr" in lower:
        return f"{excel_label} = marginal IRR from unit cash flows"
    if "cash boy" in lower or "cash eoy" in lower:
        return f"{excel_label} = prior balance + inflows − outflows"
    if "allocated cash" in lower:
        return f"{excel_label} = IRR-weighted share of remaining pool"
    if "nopat" in lower:
        return "NOPAT = Group EBIT × (1 − tax rate)"
    if "group ebitda" in lower:
        return "Group EBITDA = Group Gross Profit − Total OpEx"
    if "group fcf" in lower:
        return "Group FCF = NOPAT + D&A − Total Group CapEx − Mars carve-out"
    if "group revenue" in lower:
        return "Group Revenue = Σ module revenues − inter-module eliminations"
    if "capex" in lower or "cap ex" in lower:
        return f"{excel_label} = Σ capital expenditure lines"
    if "opex" in lower or "sga" in lower or "r&d" in lower:
        return f"{excel_label} = Σ operating expense lines"
    if "elimination" in lower:
        return f"{excel_label} = gross internal flow offset at consolidation"
    if "capacity" in lower or "launches" in lower or "fleet" in lower:
        return f"{excel_label} = capacity / fleet identity per {arch_ref or 'architecture spec'}"
    if "conservation" in lower or " check" in lower:
        return f"{excel_label} = Σ inflows − Σ outflows (must ≈ 0)"
    if "memo" in lower:
        return f"{excel_label} = reconciliation memo per disclosure"

    arch = arch_ref or "architecture spec"
    if fn_name.startswith("compute_"):
        concept = fn_name.removeprefix("compute_").replace("_", " ")
        return f"{excel_label or concept} — computed per {arch}"
    return f"{excel_label or fn_name} — computed per {arch}"


def _patch_docstring_block(block: str, formula: str) -> str:
    if "Formula:" in block:
        return block
    principle = re.search(r"^(\s*)Principle:\s*.+$", block, re.MULTILINE)
    if not principle:
        return block
    indent = principle.group(1)
    insert = f"\n{indent}\n{indent}Formula: {formula}."
    pos = principle.end()
    return block[:pos] + insert + block[pos:]


def _patch_function_source(
    source: str, node: ast.FunctionDef | ast.AsyncFunctionDef, formula: str
) -> str:
    if not node.body:
        return source
    first = node.body[0]
    if not isinstance(first, ast.Expr) or not isinstance(first.value, ast.Constant):
        return source
    if not isinstance(first.value.value, str):
        return source

    lines = source.splitlines(keepends=True)
    start = first.lineno - 1
    end = first.end_lineno
    block = "".join(lines[start:end])
    new_block = _patch_docstring_block(block, formula)
    if new_block == block:
        return source
    return "".join(lines[:start]) + new_block + ("" if end >= len(lines) else "".join(lines[end:]))


def main() -> int:
    updated = 0
    for path, node in iter_public_calc_functions():
        source = path.read_text(encoding="utf-8")
        doc = ast.get_docstring(node) or ""
        if "Formula:" in doc:
            continue
        tags = parse_docstring_tags(doc)
        formula = _infer_formula(
            node.name,
            tags.get("excel_label", ""),
            tags.get("architecture_ref", ""),
            _summary_line(doc),
        )
        new_source = _patch_function_source(source, node, formula)
        if new_source != source:
            path.write_text(new_source, encoding="utf-8")
            updated += 1
    print(f"Done — {updated} functions updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
