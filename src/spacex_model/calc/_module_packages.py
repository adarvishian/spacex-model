"""P&L module packages subject to Phase B scaffolding linters."""

from __future__ import annotations

from pathlib import Path

# Package name → path to module.py (vending-machine orchestrator)
PNL_MODULE_PACKAGES: dict[str, Path] = {
    "customer_launch": Path("customer_launch") / "module.py",
    "starlink": Path("starlink") / "module.py",
    "odc": Path("odc") / "module.py",
    "ai_stack": Path("ai_stack") / "module.py",
    "lunar_mars": Path("lunar_mars") / "module.py",
}

CALC_ROOT = Path(__file__).resolve().parent
