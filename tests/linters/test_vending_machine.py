"""§2.1 vending-machine framing linter tests."""

from __future__ import annotations

from spacex_model.linters.vending_machine import find_vending_machine_violations


def test_pnl_modules_have_vending_machine_sections() -> None:
    violations = find_vending_machine_violations()
    assert violations == [], "\n".join(violations)
