"""Sheet registry for audit grid — FRONTEND_PRD §4.1 / §8.1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

LifecycleStage = Literal[
    "input",
    "demand",
    "allocation",
    "output",
    "pnl",
    "conservation",
    "valuation",
]


@dataclass(frozen=True, slots=True)
class SheetMeta:
    slug: str
    display_name: str
    source_sheet: str
    row_cap: int
    col_cap: int
    lifecycle_stage: LifecycleStage
    enabled: bool = True


SHEETS: tuple[SheetMeta, ...] = (
    SheetMeta("assumptions", "Assumptions", "Assumptions", 350, 36, "input"),
    SheetMeta("allocator", "Allocator", "Allocator", 171, 31, "allocation"),
    SheetMeta("launch_capacity", "Launch Capacity", "Launch Capacity", 80, 29, "allocation"),
    SheetMeta("customer_launch", "Customer Launch", "Customer Launch", 210, 31, "output"),
    SheetMeta("starlink", "Starlink", "Starlink", 235, 29, "output"),
    SheetMeta("starlink_capacity", "Starlink Capacity", "Starlink Capacity", 50, 29, "output"),
    SheetMeta("odc", "ODC", "ODC", 210, 29, "output"),
    SheetMeta("ai_stack", "AI Stack", "AI Stack", 210, 29, "output"),
    SheetMeta("lunar_mars", "Lunar Mars", "Lunar Mars", 212, 32, "output"),
    SheetMeta("group_pnl", "Group P&L", "Group P&L", 125, 56, "pnl"),
    SheetMeta("opex", "OpEx", "OpEx", 60, 29, "pnl"),
    SheetMeta("capex", "CapEx", "CapEx", 47, 29, "pnl"),
    SheetMeta("valuation", "Valuation", "Valuation", 6, 29, "valuation"),
    SheetMeta("demand_curves", "Demand Curves", "Demand Curves", 145, 36, "demand"),
    SheetMeta("run_audit", "Run Audit", "Run Audit", 0, 0, "conservation"),
)

_BY_SLUG: dict[str, SheetMeta] = {s.slug: s for s in SHEETS}
_BY_NAME: dict[str, SheetMeta] = {s.source_sheet: s for s in SHEETS}


def get_sheet(slug: str) -> SheetMeta | None:
    return _BY_SLUG.get(slug)


def sheet_for_name(name: str) -> SheetMeta | None:
    return _BY_NAME.get(name)


def serialize_sheets_list() -> list[dict[str, Any]]:
    return [
        {
            "slug": s.slug,
            "display_name": s.display_name,
            "source_sheet": s.source_sheet,
            "row_count": s.row_cap,
            "col_count": s.col_cap,
            "lifecycle_stage": s.lifecycle_stage,
            "enabled": s.enabled,
            "is_run_audit": s.slug == "run_audit",
        }
        for s in SHEETS
    ]
