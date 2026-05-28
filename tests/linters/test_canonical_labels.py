"""§2.4 canonical-label registry linter tests."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.config.canonical_labels import CANONICAL_LABELS, LABELS_BY_SHEET
from spacex_model.linters.canonical_labels import (
    find_inline_label_literals,
    find_workbook_labels_missing_from_registry,
)

REPO = Path(__file__).resolve().parents[2]


def _load_intentionally_unused() -> frozenset[str]:
    path = REPO / "docs" / "intentionally_unused_labels.md"
    if not path.exists():
        return frozenset()
    labels: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("- ") and len(line) > 2:
            labels.add(line[2:].strip())
    return frozenset(labels)


def test_no_inline_label_literals_in_calc() -> None:
    violations = find_inline_label_literals()
    assert violations == [], "\n".join(violations)


def test_registry_contains_all_workbook_labels() -> None:
    unused = _load_intentionally_unused()
    violations = find_workbook_labels_missing_from_registry(LABELS_BY_SHEET, intentionally_unused=unused)
    assert violations == [], "\n".join(violations[:20])


def test_canonical_labels_nonempty() -> None:
    assert len(CANONICAL_LABELS) > 500
