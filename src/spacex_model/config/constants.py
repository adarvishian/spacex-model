"""Model-wide constants per Architecture §2 and PRD V4.113 §2.2."""

from __future__ import annotations

FIRST_YEAR = 2025
LAST_YEAR = 2040
HORIZON_YEARS = LAST_YEAR - FIRST_YEAR + 1  # 16

SOLVER_MAX_ITERATIONS = 1000  # V4.113 iterateCount (queue gate only)
SOLVER_TOLERANCE = 1e-7
SOLVER_DAMPING = 0.5

CONSERVATION_RESIDUAL_TOLERANCE_MM = 1.0

# Assumptions tab column mapping (V4.113 layout — same AG/AJ MC block)
COL_BASE_CASE = 2  # B
COL_NOTES = 3  # C
COL_MC_MIN = 33  # AG
COL_MC_MAX = 34  # AH
COL_MC_DISTRIBUTION = 35  # AI
COL_MC_NOTES = 36  # AJ
