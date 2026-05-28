"""Q4'25 anchors — superseded by S-1 audited anchors for Block B / ingest checks.

See s1_2025_anchors.py and docs/DEV_LOG.md (2026-05-28 S-1 P0 pass).
"""

from __future__ import annotations

from spacex_model.inputs.s1_2025_anchors import AnchorSpec, S1_INGEST_ANCHORS_2025

# Backward-compatible export name used by older tests/docs.
Q4_25_ANCHORS_2025 = S1_INGEST_ANCHORS_2025

__all__ = ["AnchorSpec", "Q4_25_ANCHORS_2025", "S1_INGEST_ANCHORS_2025"]
