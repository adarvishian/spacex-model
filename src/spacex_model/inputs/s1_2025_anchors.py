"""S-1 / V4.131 2025 calibration anchors.

V4.131 re-baseline (R0): ingest-time checks use V4.131 Assumptions labels.
Legacy tuples retained for Block B diagnostic comparison (R4).
"""

from __future__ import annotations

from spacex_model.config import canonical_labels as cl
from spacex_model.inputs.v4_131_2025_anchors import (
    AnchorSpec,
    V4_131_INGEST_ANCHORS_2025,
)

# Active ingest-time anchor set (V4.131).
S1_INGEST_ANCHORS_2025 = V4_131_INGEST_ANCHORS_2025

# Legacy Q4'25 anchors retained for diagnostic comparison only.
Q4_25_HISTORICAL_ANCHORS_2025: tuple[AnchorSpec, ...] = (
    AnchorSpec("Group Revenue (Q4'25)", 14_650, 0.05),
    AnchorSpec(
        "Starting cash EoY 2024 (Q4'25)",
        5_000,
        0.0,
        cl.STARTING_CASH_POSITION_EOY_2024_MM,
    ),
)
