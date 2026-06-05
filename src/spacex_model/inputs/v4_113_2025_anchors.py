"""V4.113 Assumptions 2025 calibration anchors — frozen anchor year per PRD §1."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.config import canonical_labels as cl


@dataclass(frozen=True, slots=True)
class AnchorSpec:
    name: str
    target: float
    tolerance_pct: float
    assumptions_label: str | None = None


V4_113_INGEST_ANCHORS_2025: tuple[AnchorSpec, ...] = (
    AnchorSpec(
        "Starting cash EoY 2024",
        11_385.0,
        0.0,
        cl.STARTING_CASH_POSITION_EOY_2024_MM,
    ),
    AnchorSpec(
        "Tax rate",
        0.21,
        0.0,
        cl.TAX_RATE_CORPORATE_US_FEDERAL_STATE_BLENDED,
    ),
    AnchorSpec(
        "Broadband ARPU 2025",
        81.0,
        0.0,
        cl.BROADBAND_ARPU_SUB_MO_YEAR_ROW,
    ),
    AnchorSpec(
        "F9 customer launch price 2025",
        54.8,
        0.05,
        cl.F9_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH,
    ),
    AnchorSpec(
        "AI segment total revenue 2025",
        3_201.0,
        0.02,
        cl.MEMO_AI_SEGMENT_TOTAL_REVENUE_2025_M,
    ),
)
