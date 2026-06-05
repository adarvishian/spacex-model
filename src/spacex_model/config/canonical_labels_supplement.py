"""Port-only canonical labels — not in V4.113 workbook; supersede when workbook adds them."""

from __future__ import annotations

from typing import Final

# S-1 adherence / pre-R1 calc references (P1 backlog)
F9_BOOSTER_ACCOUNTING_DEPRECIATION_CAP_FLIGHTS: Final[str] = (
    "F9 booster accounting depreciation cap (flights)"
)
LAUNCH_SERVICES_REVENUE_SHARE_YEAR_ROW: Final[str] = (
    "Launch Services revenue share of external CL rev — year-row"
)
STARSHIP_PRECOMMERCIAL_RD_MM_YEAR_ROW: Final[str] = (
    "Starship pre-commercialization R&D ($mm/yr) — year-row"
)
STARSHIELD_S1_GOV_CONNECTIVITY_SCOPE_FACTOR: Final[str] = (
    "Starshield S-1 Government Connectivity scope factor"
)
CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_KG_DEMAND_STUB_KG: Final[str] = (
    "Customer Launch external Starship kg demand (stub, kg)"
)
CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_LAUNCHES_STUB: Final[str] = (
    "Customer Launch external Starship launches (stub)"
)

# R1 — V2.16 labels pending full V4.113 row re-resolution (use cl.* not inline literals)
SATELLITE_USEFUL_LIFE_V2_MINI_YEARS: Final[str] = "Satellite useful life — V2 Mini (years)"
SATELLITE_USEFUL_LIFE_V3_YEARS: Final[str] = "Satellite useful life — V3 (years)"
SATELLITE_DEP_PER_KG_ANNUAL_DECAY_RATE: Final[str] = "Satellite Dep per kg — annual decay rate"
V2_MINI_COST_PER_KG_BASE_YEAR: Final[str] = "V2 Mini cost per kg — base year ($/kg)"
LEGACY_V1_V1_5_DA_USEFUL_LIFE_YRS: Final[str] = "Legacy V1/V1.5 D&A useful life (yrs)"
LEGACY_V1_V1_5_BANDWIDTH_END_2025_GBPS: Final[str] = "Legacy V1/V1.5 Bandwidth — end-2025 (Gbps)"
LEGACY_V1_V1_5_DA_BASELINE_MM_2025: Final[str] = "Legacy V1/V1.5 D&A baseline ($mm, 2025 anchor)"
STARLINK_GROUND_OPS_PCT_REV: Final[str] = "Starlink ground ops % of revenue"
STARLINK_INSURANCE_PCT_REV: Final[str] = "Starlink insurance % of revenue"
STARLINK_OTHER_COGS_PCT_REV: Final[str] = "Starlink other COGS % of revenue"
STARSHIELD_RESERVED_PCT_START: Final[str] = "Starshield Reserved % — start"
STARSHIELD_RESERVED_PCT_FLOOR: Final[str] = "Starshield Reserved % — floor"
STARSHIELD_RESERVED_PCT_DECAY_RATE: Final[str] = "Starshield Reserved % — decay rate"
STARSHIELD_REV_PER_GBPS_BASE_YEAR: Final[str] = "Starshield Rev per Gbps — base year ($/Gbps)"
STARSHIELD_REV_PER_GBPS_DECAY_RATE: Final[str] = "Starshield Rev per Gbps — decay rate"
SUBSIDY_MIX_PCT_NET_ADDS: Final[str] = "Subsidy mix (% of net adds subsidized)"
TERMINAL_RETAIL_PRICE_SUBSIDIZED: Final[str] = "Terminal retail price ($, subsidized)"
TERMINAL_RETAIL_PRICE_NON_SUBSIDIZED: Final[str] = "Terminal retail price ($, non-subsidized)"
TOTAL_CUSTOMER_LAUNCH_MARKET_CAGR: Final[str] = "Total customer launch market CAGR (% growth/yr)"
CUSTOMER_LAUNCH_DEPRECIATION_USEFUL_LIFE_YEARS: Final[str] = (
    "Customer Launch depreciation useful life (years)"
)
LUNAR_LABOUR_SHARE_SURFACE_PAYLOAD_YEAR_ROW: Final[str] = (
    "Lunar labour share of surface payload — year-row"
)
MARS_LABOUR_SHARE_SURFACE_PAYLOAD_YEAR_ROW: Final[str] = (
    "Mars labour share of surface payload — year-row"
)
ODC_EXTERNAL_COMPUTE_SHARE_CUSTOMERS_YEAR_ROW: Final[str] = (
    "ODC external compute share to customers % — year-row"
)
ODC_FLEET_DESIGN_LIFE_YEARS: Final[str] = "ODC fleet design life (years)"
COREWEAVE_BASELINE_ANCHOR_YEAR_ROW: Final[str] = (
    "CoreWeave baseline anchor ($B/GW_IT/yr, 2026) — year-row"
)
ORBITAL_PUE_UPLIFT_VS_TERRESTRIAL: Final[str] = "Orbital PUE uplift vs terrestrial"
ODC_UTILIZATION_FACTOR: Final[str] = "ODC utilization factor"
CHIP_TDP_PER_CHIP_W_YEAR_ROW: Final[str] = "Chip TDP per chip (W) — year-row"
CHIP_FP8_PERFORMANCE_TFLOPS_YEAR_ROW: Final[str] = "Chip FP8 performance per chip (TFLOPS) — year-row"
WORKLOAD_MIX_INFERENCE_SHARE: Final[str] = "Workload mix — inference share"
PRICE_PER_H100_GPU_HR_YEAR_ROW: Final[str] = "Price per H100-equiv GPU-hr ($) — year-row"
CREDENCE_ON_MODEL_A_PR_A: Final[str] = "Credence on Model A (Pr(A))"
BB_SHARE_OF_ODC_BANDWIDTH_CLAIM: Final[str] = "BB-share of ODC bandwidth claim"
GBPS_PER_GWH_ODC_COMPUTE_ENERGY: Final[str] = "Gbps per GWh/yr of ODC compute energy"
ODC_GROUND_OPS_PCT_REV: Final[str] = "ODC ground ops % of revenue"
S1_AI_SEGMENT_REVENUE_YEAR_ROW: Final[str] = "S-1 AI segment revenue ($mm) — year-row"
ANTHROPIC_COMPUTE_REVENUE_YEAR_ROW: Final[str] = (
    "Anthropic compute services revenue ($mm) — year-row"
)
TERRESTRIAL_AI_CAPEX_YEAR_ROW: Final[str] = "Terrestrial AI data-center CapEx ($mm) — year-row"
TAM_INFLATION_RATE_ANNUAL: Final[str] = "TAM inflation rate (annual)"
GNI_PER_CAPITA_GROWTH_RATE_ANNUAL: Final[str] = "GNI per capita growth rate (annual)"
V2_MINI_BANDWIDTH_PER_SAT_BB_GBPS: Final[str] = "V2 Mini Bandwidth per Sat — BB (Gbps)"
V2_MINI_BANDWIDTH_PER_SAT_DTC_GBPS: Final[str] = "V2 Mini Bandwidth per Sat — DTC (Gbps)"
SATS_PER_F9_LAUNCH_V2_BB: Final[str] = "Sats per F9 launch — V2 BB"
SATS_PER_F9_LAUNCH_V2_DTC: Final[str] = "Sats per F9 launch — V2 DTC"
V2_MINI_BB_HISTORICAL_BASELINE_SOY_2025: Final[str] = "V2 Mini BB historical baseline (SoY 2025)"
V2_MINI_DTC_HISTORICAL_BASELINE_SOY_2025: Final[str] = "V2 Mini DTC historical baseline (SoY 2025)"
V3_BB_BANDWIDTH_PER_SAT_BASE_YEAR_GBPS: Final[str] = "V3 BB Bandwidth per Sat — base year (Gbps)"
V3_DTC_BANDWIDTH_PER_SAT_GBPS: Final[str] = "V3 DTC Bandwidth per Sat (Gbps)"
SATS_PER_STARSHIP_LAUNCH_V3_BB: Final[str] = "Sats per Starship launch — V3 BB"
SATS_PER_STARSHIP_LAUNCH_V3_DTC: Final[str] = "Sats per Starship launch — V3 DTC"
V3_BB_SATS_LAUNCHED_2025: Final[str] = "V3 BB Sats Launched 2025"
V3_DTC_SATS_LAUNCHED_2025: Final[str] = "V3 DTC Sats Launched 2025"
V3_BB_FIRST_LAUNCH_YEAR: Final[str] = "V3 BB first launch year"
V3_DTC_FIRST_LAUNCH_YEAR: Final[str] = "V3 DTC first launch year"
V2_PHASE_OUT_YEAR: Final[str] = "V2 phase-out year (no V2 BB / V2 DTC launches from this year)"
V2_MINI_BB_ACTIVE_SATS_END_2025: Final[str] = "V2 Mini BB Active Sats — end-2025"
V2_MINI_DTC_ACTIVE_SATS_END_2025: Final[str] = "V2 Mini DTC Active Sats — end-2025"
LEGACY_V1_V1_5_ACTIVE_BANDWIDTH_YEAR_ROW: Final[str] = (
    "Legacy V1/V1.5 Active Bandwidth (Gbps, year-row runoff)"
)

# R2 — V2.16 CapEx row pending V4.113 Assumptions re-resolution
CORPORATE_HISTORICAL_CAPITAL_BASE_MM: Final[str] = "Corporate historical capital base ($mm)"
