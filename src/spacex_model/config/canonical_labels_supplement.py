"""Port-only canonical labels — remapped for SpaceX V4.131 (2026-06-10 rebase)."""

from __future__ import annotations

from typing import Final

# V4.131 Assumptions remaps (label strings changed; constant names retained for code stability)
BB_SHARE_OF_ODC_BANDWIDTH_CLAIM: Final[str] = "BB-share of bandwidth (ratio)"
CHIP_TDP_PER_CHIP_W_YEAR_ROW: Final[str] = "Chip TDP CAGR (post-2027, W/chip)"
CHIP_FP8_PERFORMANCE_TFLOPS_YEAR_ROW: Final[str] = "Chip FP8 per chip CAGR (/yr): smooth curve"
COREWEAVE_BASELINE_ANCHOR_YEAR_ROW: Final[str] = (
    "Comp anchor: AI/Compute standalone (CoreWeave-anchored)"
)
S1_AI_SEGMENT_REVENUE_YEAR_ROW: Final[str] = "S-1 AI (≙ xAI, consolidated): Revenue ($mm)"
ANTHROPIC_COMPUTE_REVENUE_YEAR_ROW: Final[str] = (
    "Anthropic compute services revenue ($mm) — year-row"
)
TERRESTRIAL_AI_CAPEX_YEAR_ROW: Final[str] = "Memo: Terrestrial AI compute draw (GW): year-row"
# ECHOSTAR: keep canonical_labels.py label; missing from V4.131 ingest → s1_profiles fallback in capex.py
PRE_IPO_BRIDGE_DRAWDOWN_YEAR: Final[str] = "Launch-pacing year (apply caps in this year only)"
WORKLOAD_MIX_INFERENCE_SHARE: Final[str] = "Effective Compute Ratio (ratio)"
ODC_UTILIZATION_FACTOR: Final[str] = "Utilization ceiling (%)"
ORBITAL_PUE_UPLIFT_VS_TERRESTRIAL: Final[str] = "Orbital PUE"
GBPS_PER_GWH_ODC_COMPUTE_ENERGY: Final[str] = "Gbps per GWh/yr"
STARLINK_GROUND_OPS_PCT_REV: Final[str] = "Ground/network opex pct rev"
STARLINK_INSURANCE_PCT_REV: Final[str] = "Asset insurance COGS (% of revenue)"
STARLINK_OTHER_COGS_PCT_REV: Final[str] = "Asset insurance COGS (% of revenue)"
STARSHIELD_REV_PER_GBPS_BASE_YEAR: Final[str] = "Starshield $/Gbps ($/Gbps-yr)"
STARSHIELD_REV_PER_GBPS_DECAY_RATE: Final[str] = "Starshield Gbps growth (frac)"
STARSHIELD_RESERVED_PCT_START: Final[str] = "Starshield utilization (frac)"
STARSHIELD_RESERVED_PCT_FLOOR: Final[str] = "Starshield utilization (frac)"
STARSHIELD_RESERVED_PCT_DECAY_RATE: Final[str] = "Starshield Gbps growth (frac)"
TOTAL_CUSTOMER_LAUNCH_MARKET_CAGR: Final[str] = "Commercial launch market CAGR"
DTC_ARPU_SUB_MO_YEAR_ROW: Final[str] = "Broadband ARPU floor ($/mo)"
TAM_INFLATION_RATE_ANNUAL: Final[str] = "Terminal growth rate g (group + most modules)"
AI_STACK_R_D_START_OF_AI_STACK_REV: Final[str] = "AI Stack R&D start pct"
AI_STACK_R_D_END_STATE_FLOOR: Final[str] = "AI Stack R&D floor pct"
AI_STACK_R_D_CAGR_TAPER: Final[str] = "AI Stack R&D CAGR"
ODC_R_D_START_OF_ODC_REV: Final[str] = "ODC R&D start pct"
ODC_R_D_END_STATE_FLOOR: Final[str] = "ODC R&D floor pct"
ODC_R_D_CAGR_TAPER: Final[str] = "ODC R&D CAGR"
SALES_MARKETING_START_OF_STARLINK_STARSHIELD_CUSTOMER_LAUNCH_EXT_REV: Final[str] = (
    "Sales & Marketing: start % of (Starlink+Starshield+CL ext) rev"
)
LAUNCHES_PER_STARSHIP_VEHICLE_PER_YEAR_CADENCE_VARIANT_BLEND_USED_FOR_SIZING: Final[
    str
] = "Starship booster cadence for pre-build sizing (flights/yr)"
SATELLITE_USEFUL_LIFE_V2_MINI_YEARS: Final[str] = "Sat operational life L (years)"
SATELLITE_USEFUL_LIFE_V3_YEARS: Final[str] = "Sat operational life L (years)"
SATELLITE_DEP_PER_KG_ANNUAL_DECAY_RATE: Final[str] = "Satellite cost per kg: learning rate"
V2_MINI_COST_PER_KG_BASE_YEAR: Final[str] = "Satellite cost per kg: base year ($/kg)"
LEGACY_V1_V1_5_BANDWIDTH_END_2025_GBPS: Final[str] = "Legacy V1 Gbps per sat"
LEGACY_V1_V1_5_DA_BASELINE_MM_2025: Final[str] = "Legacy V1 Gbps per sat"
LEGACY_V1_V1_5_DA_USEFUL_LIFE_YRS: Final[str] = "Sat operational life L (years)"
STARLINK_GROUND_OPS_PCT_REV_ALIAS: Final[str] = "Ground/network opex pct rev"
V2_MINI_BANDWIDTH_PER_SAT_BB_GBPS: Final[str] = "V2 BB Gbps per sat"
V2_MINI_BANDWIDTH_PER_SAT_DTC_GBPS: Final[str] = "V2 BB Gbps per sat"
V2_MINI_BB_ACTIVE_SATS_END_2025: Final[str] = "V2 Mini BB sats end-2025"
V2_MINI_BB_HISTORICAL_BASELINE_SOY_2025: Final[str] = "V2 Mini BB sats end-2025"
V2_MINI_DTC_ACTIVE_SATS_END_2025: Final[str] = "V2 DTC active sats end-2025"
V2_MINI_DTC_HISTORICAL_BASELINE_SOY_2025: Final[str] = "V2 DTC active sats end-2025"
V3_BB_BANDWIDTH_PER_SAT_BASE_YEAR_GBPS: Final[str] = "V3 BB Gbps per sat"
V3_DTC_BANDWIDTH_PER_SAT_GBPS: Final[str] = "Effective DTC Gbps per sat (revenue calibration)"
SATS_PER_F9_LAUNCH_V2_BB: Final[str] = "F9 sats per launch (V2 packing)"
SATS_PER_F9_LAUNCH_V2_DTC: Final[str] = "F9 sats per launch (V2 packing)"
V3_BB_FIRST_LAUNCH_YEAR: Final[str] = "V3 Starlink launch trigger year"
V3_DTC_FIRST_LAUNCH_YEAR: Final[str] = "V3 Starlink launch trigger year"
V2_PHASE_OUT_YEAR: Final[str] = "V3 Starlink launch trigger year"
F9_BOOSTER_ACCOUNTING_DEPRECIATION_CAP_FLIGHTS: Final[str] = "F9 booster economic life (years)"
STARSHIELD_S1_GOV_CONNECTIVITY_SCOPE_FACTOR: Final[str] = "SpaceX government market share %"
SUBSIDY_MIX_PCT_NET_ADDS: Final[str] = "Terminal kits per net subscriber add"
TERMINAL_RETAIL_PRICE_SUBSIDIZED: Final[str] = "Blended kit sale price ($/kit)"
TERMINAL_RETAIL_PRICE_NON_SUBSIDIZED: Final[str] = "Blended kit sale price ($/kit)"
ODC_GROUND_OPS_PCT_REV: Final[str] = "Ground-network ops COGS (% of revenue)"
ODC_FLEET_DESIGN_LIFE_YEARS: Final[str] = "Sat operational life L (years)"
PRICE_PER_H100_GPU_HR_YEAR_ROW: Final[str] = "F_ref: reference compute unit (TFLOPS, H100 FP8)"
CUSTOMER_LAUNCH_DEPRECIATION_USEFUL_LIFE_YEARS: Final[str] = "Launch pad useful life (years)"
SATELLITE_USEFUL_LIFE_V2_DTC_YEARS: Final[str] = "Sat operational life L (years)"
SATELLITE_USEFUL_LIFE_V3_DTC_YEARS: Final[str] = "Sat operational life L (years)"
LEGACY_V1_GBPS_PER_SAT: Final[str] = "Legacy V1 Gbps per sat"
LEGACY_V1_5_GBPS_PER_SAT: Final[str] = "Legacy V1.5 Gbps per sat"
STARSHIP_PAYLOAD_2025_BASELINE_KG_TO_LEO_FULLY_REUSABLE_MODE: Final[str] = (
    "Starship payload for pre-build sizing (kg)"
)
CUSTOMER_LAUNCH_MODULE_SG_A_OF_EXTERNAL_REV: Final[str] = (
    "Customer Launch module SG&A (% of external rev)"
)
V2_MINI_MASS_KG: Final[str] = "V2 BB sat mass (kg)"
V3_MASS_KG: Final[str] = "V3 BB sat mass (kg)"
V2_MINI_BB_SATS_LAUNCHED_2025: Final[str] = "V2 Mini BB sats end-2025"
V2_MINI_DTC_SATS_LAUNCHED_2025: Final[str] = "V2 DTC active sats end-2025"
