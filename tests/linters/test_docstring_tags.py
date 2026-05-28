"""§7.4 four-tag docstring linter tests."""

from __future__ import annotations

from spacex_model.linters.docstrings import find_missing_docstring_tags


def test_phase_b_public_calc_functions_have_four_tags() -> None:
    violations = find_missing_docstring_tags()
    assert violations == [], "\n".join(violations)
