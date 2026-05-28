"""S-1 audited 2025 calibration anchors (Form S-1 filed 2026-05-20).

Replaces Q4'25-derived anchors for Block B and ingest-time warnings per
SpaceX_Modeler_S1_Adherence_Audit_2026-05-28.docx §7.2 P0-6 / P0-11.
"""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.config import canonical_labels as cl


@dataclass(frozen=True, slots=True)
class AnchorSpec:
    name: str
    target: float
    tolerance_pct: float
    assumptions_label: str | None = None


# Ingest-time cross-checks (scalar Assumptions rows with S-1 targets).
S1_INGEST_ANCHORS_2025: tuple[AnchorSpec, ...] = (
    AnchorSpec(
        "Starting cash EoY 2024",
        11_385.0,
        0.0,
        cl.STARTING_CASH_POSITION_EOY_2024_MM,
    ),
    AnchorSpec(
        "F9 customer launches 2025",
        43.0,
        0.0,
        cl.F9_CUSTOMER_LAUNCHES_PER_YEAR,
    ),
    AnchorSpec(
        "F9 customer launch price 2025",
        111.0,
        0.05,
        cl.F9_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH_2025_ANCHOR,
    ),
    AnchorSpec(
        "S-1 AI segment revenue 2025",
        3_201.0,
        0.02,
        "S-1 AI segment revenue ($mm) — year-row",
    ),
    AnchorSpec(
        "Broadband ARPU 2025",
        81.0,
        0.05,
        cl.BROADBAND_ARPU_SUB_MO_YEAR_ROW,
    ),
)


# Legacy Q4'25 anchors retained for diagnostic comparison only.
Q4_25_HISTORICAL_ANCHORS_2025: tuple[AnchorSpec, ...] = (
    AnchorSpec("Group Revenue (Q4'25)", 14_650, 0.05),
    AnchorSpec("Starting cash EoY 2024 (Q4'25)", 5_000, 0.0, cl.STARTING_CASH_POSITION_EOY_2024_MM),
)
