"""Block D architecture spec coverage — PRD §7.4."""

from __future__ import annotations

from spacex_model.linters.architecture_coverage import find_uncovered_architecture_sections
from spacex_model.linters.docstrings import find_missing_docstring_tags


def test_every_public_calc_function_has_full_docstring() -> None:
    violations = find_missing_docstring_tags()
    assert violations == [], "\n".join(violations)


def test_every_architecture_section_has_code_coverage() -> None:
    uncovered = find_uncovered_architecture_sections()
    assert uncovered == [], f"Architecture sections without code refs: {uncovered}"
