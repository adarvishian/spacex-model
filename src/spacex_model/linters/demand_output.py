"""§2.2 demand/output decoupling linter."""

from __future__ import annotations

import ast
from pathlib import Path

from spacex_model.calc._module_packages import CALC_ROOT, PNL_MODULE_PACKAGES

FORBIDDEN_NAMES = frozenset({"OutputResult"})


def _demand_paths() -> list[Path]:
    return [CALC_ROOT / pkg / "demand.py" for pkg in PNL_MODULE_PACKAGES]


def find_demand_output_violations() -> list[str]:
    """Demand modules must not reference OutputResult or output_* names."""
    errors: list[str] = []
    for path in _demand_paths():
        rel = path.relative_to(CALC_ROOT)
        if not path.exists():
            errors.append(f"{rel}: missing demand.py")
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and "output" in node.module:
                errors.append(f"{rel}: imports from output module {node.module!r}")
            if isinstance(node, ast.Name):
                if node.id in FORBIDDEN_NAMES or node.id.startswith("output_"):
                    errors.append(f"{rel}: forbidden reference to {node.id!r}")
            if isinstance(node, ast.Attribute) and node.attr.startswith("output_"):
                errors.append(f"{rel}: forbidden attribute {node.attr!r}")
        source = path.read_text(encoding="utf-8")
        if "from spacex_model.calc" in source and ".output" in source:
            errors.append(f"{rel}: imports output submodule")
    return errors
