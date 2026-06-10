"""Milestone 2.4 — no silent default= on assumption_scalar in calc/."""

from __future__ import annotations

from spacex_model.linters.assumption_defaults import find_assumption_scalar_defaults


def test_no_assumption_scalar_defaults_in_calc() -> None:
    violations = find_assumption_scalar_defaults()
    assert violations == [], "\n".join(violations[:20])
