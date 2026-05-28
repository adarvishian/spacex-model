"""§2.1 vending-machine linter — modules must not import OpEx / taxes."""

from __future__ import annotations

import ast
from pathlib import Path

from spacex_model.calc._module_packages import CALC_ROOT, PNL_MODULE_PACKAGES

FORBIDDEN_IMPORT_ROOTS = frozenset(
    {
        "spacex_model.calc.opex",
        "spacex_model.calc.group_pnl",
    }
)

FORBIDDEN_NAME_FRAGMENTS = frozenset({"tax", "corporate_overhead"})

REQUIRED_FUNCTIONS = frozenset(
    {
        "compute_revenue",
        "compute_cogs",
        "compute_gross_profit",
        "compute_capex",
        "compute_fcf",
    }
)


def _module_paths() -> list[Path]:
    return [CALC_ROOT / rel for rel in PNL_MODULE_PACKAGES.values()]


def find_vending_machine_violations() -> list[str]:
    """Return human-readable violation messages (empty if clean)."""
    errors: list[str] = []
    for path in _module_paths():
        rel = path.relative_to(CALC_ROOT)
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        defined = {
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }
        missing = REQUIRED_FUNCTIONS - defined
        if missing:
            errors.append(f"{rel}: missing vending-machine functions {sorted(missing)}")

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    errors.extend(_check_import(rel, alias.name))
            elif isinstance(node, ast.ImportFrom) and node.module:
                errors.extend(_check_import(rel, node.module))
                for alias in node.names:
                    if any(frag in alias.name.lower() for frag in FORBIDDEN_NAME_FRAGMENTS):
                        errors.append(
                            f"{rel}: forbidden import name {alias.name!r} from {node.module}"
                        )
    return errors


def _check_import(rel: Path, module: str) -> list[str]:
    out: list[str] = []
    if module in FORBIDDEN_IMPORT_ROOTS or any(
        module.startswith(root + ".") for root in FORBIDDEN_IMPORT_ROOTS
    ):
        out.append(f"{rel}: forbidden import {module!r}")
    leaf = module.rsplit(".", 1)[-1]
    if any(frag in leaf.lower() for frag in FORBIDDEN_NAME_FRAGMENTS):
        out.append(f"{rel}: forbidden import module {module!r}")
    return out
