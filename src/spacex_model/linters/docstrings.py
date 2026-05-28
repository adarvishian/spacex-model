"""§7.4 / §11.2 four-tag docstring linter."""

from __future__ import annotations

import ast
from collections.abc import Iterable
from pathlib import Path

REQUIRED_TAGS = (
    "Excel cell:",
    "Excel label:",
    "Architecture ref:",
    "Principle:",
)

CALC_ROOT = Path(__file__).resolve().parents[1] / "calc"


def iter_calc_sources() -> Iterable[Path]:
    """Walk all public calc modules; skip private root helpers (_*.py)."""
    for path in sorted(CALC_ROOT.rglob("*.py")):
        if path.parent == CALC_ROOT and path.name.startswith("_"):
            continue
        yield path


def find_missing_docstring_tags() -> list[str]:
    """Public top-level functions in calc/ must have four docstring tags."""
    errors: list[str] = []
    for path in iter_calc_sources():
        rel = path.relative_to(CALC_ROOT)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("_"):
                continue
            doc = ast.get_docstring(node) or ""
            for tag in REQUIRED_TAGS:
                if tag not in doc:
                    errors.append(f"{rel}::{node.name}: missing docstring tag {tag!r}")
    return errors
