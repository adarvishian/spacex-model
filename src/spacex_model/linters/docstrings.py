"""§7.4 / §11.2 four-tag docstring linter."""

from __future__ import annotations

import ast
import re
from collections.abc import Iterable
from pathlib import Path

REQUIRED_TAGS = (
    "Excel cell:",
    "Excel label:",
    "Architecture ref:",
    "Principle:",
)

FORMULA_TAG = "Formula:"

_TAG_PATTERNS = {
    "excel_cell": re.compile(r"Excel cell:\s*(.+)", re.MULTILINE),
    "excel_label": re.compile(r'Excel label:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE),
    "architecture_ref": re.compile(r"Architecture ref:\s*(.+)", re.MULTILINE),
    "principle": re.compile(r"Principle:\s*(.+)", re.MULTILINE),
    "formula": re.compile(r"Formula:\s*(.+)", re.MULTILINE | re.DOTALL),
}

CALC_ROOT = Path(__file__).resolve().parents[1] / "calc"


def iter_calc_sources() -> Iterable[Path]:
    """Walk all public calc modules; skip private root helpers (_*.py)."""
    for path in sorted(CALC_ROOT.rglob("*.py")):
        if path.parent == CALC_ROOT and path.name.startswith("_"):
            continue
        yield path


def parse_docstring_tags(doc: str) -> dict[str, str]:
    """Extract four-tag block + Formula: line from a calc function docstring."""
    out: dict[str, str] = {}
    for tag, pattern in _TAG_PATTERNS.items():
        match = pattern.search(doc)
        if match:
            out[tag] = match.group(1).strip()
    return out


def iter_public_calc_functions() -> Iterable[tuple[Path, ast.FunctionDef | ast.AsyncFunctionDef]]:
    """Yield (source_path, AST node) for every public top-level calc function."""
    for path in iter_calc_sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            is_fn = isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            if is_fn and not node.name.startswith("_"):
                yield path, node


def find_missing_docstring_tags() -> list[str]:
    """Public top-level functions in calc/ must have four docstring tags."""
    errors: list[str] = []
    for path, node in iter_public_calc_functions():
        rel = path.relative_to(CALC_ROOT)
        doc = ast.get_docstring(node) or ""
        for tag in REQUIRED_TAGS:
            if tag not in doc:
                errors.append(f"{rel}::{node.name}: missing docstring tag {tag!r}")
    return errors


def find_missing_formula_tags() -> list[str]:
    """Public calc functions must carry a Formula: tag (§6 methodology registry gate)."""
    errors: list[str] = []
    for path, node in iter_public_calc_functions():
        rel = path.relative_to(CALC_ROOT)
        doc = ast.get_docstring(node) or ""
        if FORMULA_TAG not in doc:
            errors.append(f"{rel}::{node.name}: missing docstring tag {FORMULA_TAG!r}")
    return errors
