"""§2.2 demand/output decoupling linter tests."""

from __future__ import annotations

from spacex_model.linters.demand_output import find_demand_output_violations


def test_demand_modules_decoupled_from_output() -> None:
    violations = find_demand_output_violations()
    assert violations == [], "\n".join(violations)
