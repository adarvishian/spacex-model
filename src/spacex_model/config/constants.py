"""Model-wide constants per Architecture §2 and PRD §2.11."""

from __future__ import annotations

FIRST_YEAR = 2025
LAST_YEAR = 2050
HORIZON_YEARS = LAST_YEAR - FIRST_YEAR + 1  # 26

SOLVER_MAX_ITERATIONS = 115  # S-1 P0 terrestrial CapEx extends Cash BoY↔FCF loop (~111 iter)
SOLVER_TOLERANCE = 0.001
SOLVER_DAMPING = 0.5

CONSERVATION_RESIDUAL_TOLERANCE_MM = 1.0

# Assumptions tab column mapping (V2.16 layout)
COL_BASE_CASE = 2  # B
COL_NOTES = 3  # C
COL_MC_MIN = 33  # AG
COL_MC_MAX = 34  # AH
COL_MC_DISTRIBUTION = 35  # AI
COL_MC_NOTES = 36  # AJ
