"""Forbid silent default= fallbacks on assumption_scalar() in calc/ (audit M2.4)."""

from __future__ import annotations

import ast
from pathlib import Path

from spacex_model.calc._module_packages import CALC_ROOT


def _call_name(node: ast.Call) -> str | None:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def find_assumption_scalar_defaults() -> list[str]:
    """Return violations: assumption_scalar(..., default=...) under calc/."""
    errors: list[str] = []
    for path in sorted(CALC_ROOT.rglob("*.py")):
        rel = path.relative_to(CALC_ROOT)
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if (
                not isinstance(node, ast.Call)
                or _call_name(node) != "assumption_scalar"
            ):
                continue
            for kw in node.keywords:
                if kw.arg == "default":
                    errors.append(
                        f"{rel}:{kw.lineno}: assumption_scalar must not use default= "
                        "(missing inputs must fail at ingest)"
                    )
    return errors
