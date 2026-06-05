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
    # Inclusive row filter when a V4.113 tab hosts multiple audit views (e.g. OpEx ⊂ Group P&L).
    row_range: tuple[int, int] | None = None


# V4.113 workbook tab names — legacy V2.16 slugs retained for stable audit URLs.
SHEETS: tuple[SheetMeta, ...] = (
    SheetMeta("assumptions", "Assumptions", "Assumptions", 525, 36, "input"),
    SheetMeta("allocator", "Allocator", "Cash Allocation Engine", 124, 31, "allocation"),
    SheetMeta("launch_capacity", "Launch Capacity", "Vehicle Build", 93, 31, "allocation"),
    SheetMeta("customer_launch", "Customer Launch", "Customer Launch", 125, 31, "output"),
    SheetMeta("starlink", "Starlink", "Starlink", 166, 29, "output"),
    SheetMeta(
        "starlink_capacity",
        "Starlink Capacity",
        "Starlink",
        35,
        29,
        "output",
        row_range=(45, 177),
    ),
    SheetMeta(
        "odc",
        "ODC",
        "AI - Compute",
        55,
        29,
        "output",
        row_range=(28, 82),
        enabled=False,
    ),
    SheetMeta("ai_stack", "AI Stack", "AI - Compute", 230, 29, "output"),
    SheetMeta("lunar_mars", "Lunar Mars", "Lunar - Mars", 98, 32, "output"),
    SheetMeta("group_pnl", "Group P&L", "Group P&L", 92, 56, "pnl"),
    SheetMeta("opex", "OpEx", "Group P&L", 19, 29, "pnl", row_range=(31, 49)),
    SheetMeta("capex", "CapEx", "Group P&L", 7, 29, "pnl", row_range=(79, 85)),
    SheetMeta("valuation", "Valuation", "SoTP - Valuation", 89, 29, "valuation"),
    SheetMeta("demand_curves", "Demand Curves", "Demand Curves", 134, 36, "demand"),
    SheetMeta("run_audit", "Run Audit", "Run Audit", 0, 0, "conservation"),
)

_BY_SLUG: dict[str, SheetMeta] = {s.slug: s for s in SHEETS}
_BY_WORKBOOK_SHEET: dict[str, tuple[SheetMeta, ...]] = {}
for _meta in SHEETS:
    _BY_WORKBOOK_SHEET.setdefault(_meta.source_sheet, ())
    _BY_WORKBOOK_SHEET[_meta.source_sheet] = (*_BY_WORKBOOK_SHEET[_meta.source_sheet], _meta)


def get_sheet(slug: str) -> SheetMeta | None:
    return _BY_SLUG.get(slug)


def sheet_for_name(name: str) -> SheetMeta | None:
    """Resolve an Excel tab name to audit metadata (prefers full-tab views over row slices)."""
    matches = _BY_WORKBOOK_SHEET.get(name, ())
    if not matches:
        return None
    for meta in matches:
        if meta.row_range is None:
            return meta
    return matches[0]


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
