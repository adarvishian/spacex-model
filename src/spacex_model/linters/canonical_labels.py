"""§2.4 canonical-label registry linter."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from spacex_model.config.canonical_labels import CANONICAL_LABELS

CALC_ROOT = Path(__file__).resolve().parents[1] / "calc"

# Excel-like labels: capitalized phrase with unit paren or common row suffixes
LABEL_LIKE = re.compile(
    r"^[A-Z][A-Za-z0-9 /+\-–—'’.%$,×→]+(\([^)]+\)|\s*—\s*year-row|\s*IRR)$"
)

SKIP_LITERAL_SUBSTRINGS = frozenset(
    {
        "Phase C",
        "Phase B",
        "v1.x",
        "Architecture ref:",
        "Excel cell:",
        "Excel label:",
        "Principle:",
    }
)

SCAN_GLOBS = ("**/*.py",)


def find_inline_label_literals() -> list[str]:
    """String literals in calc/ that look like Excel labels but are not in the registry."""
    errors: list[str] = []
    for path in sorted(CALC_ROOT.rglob("*.py")):
        if path.name.startswith("_") and path.name != "_allocator_out.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            text = node.value.strip()
            if len(text) < 8 or any(skip in text for skip in SKIP_LITERAL_SUBSTRINGS):
                continue
            if not LABEL_LIKE.match(text):
                continue
            if text not in CANONICAL_LABELS:
                rel = path.relative_to(CALC_ROOT)
                errors.append(f"{rel}: unregistered label literal {text!r}")
    return errors


def find_workbook_labels_missing_from_registry(
    labels_by_sheet: dict[str, tuple[str, ...]],
    *,
    intentionally_unused: frozenset[str],
) -> list[str]:
    """Labels from xlsx column A not in CANONICAL_LABELS or intentionally_unused."""
    errors: list[str] = []
    for sheet, labels in labels_by_sheet.items():
        for label in labels:
            if label in CANONICAL_LABELS or label in intentionally_unused:
                continue
            errors.append(f"{sheet}: label not in registry: {label!r}")
    return errors
