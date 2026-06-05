"""Canonical label registry — append-only per PRD §2.4 / Rule 10.

Extracted from: SpaceX V4.113.xlsx
Regenerate via: python scripts/extract_canonical_labels.py
"""

from __future__ import annotations

from typing import Final

# fmt: off

BY_MODULE: Final[str] = "(by module)"
COLS_C_F_AS_OF: Final[str] = "(cols C:F = as-of)"
RETIRED: Final[str] = "(retired)"
RETIRED_NBV_REPORTED_AS_TOTAL_ON_R115_OUTPUT_BV_MEMO_ON_R76_R77: Final[str] = "(retired: NBV reported as total on R115; output-BV memo on R76/R77)"
L_7_BUCKETS_SAT_MFG_REDMOND_STARSHIP_VEHICLE_GIGABAY_100_YR_PADS_ENGINES_TERMINALS_TOGGLE_OFF_GROUND_STATIONS_HQ_GROUP_EXPOSES_CAPEX_D_A_TOTALS_BY_LABEL: Final[str] = "7 buckets: sat-mfg (Redmond), Starship-vehicle (Gigabay @100/yr), pads, engines, terminals (toggle-OFF), ground stations, HQ→Group. Exposes CapEx + D&A totals by label."
ADCS_AVIONICS_SAT: Final[str] = "ADCS+avionics $/sat"
AI_COMPUTE: Final[str] = "AI - Compute"
AI_COMPUTE_AI_APPS_EXTERNAL: Final[str] = "AI - Compute — AI Apps (external)"
AI_COMPUTE_ORBITAL_DC_EXTERNAL: Final[str] = "AI - Compute — Orbital DC (external)"
AI_COMPUTE_TERRESTRIAL_DC_EXTERNAL: Final[str] = "AI - Compute — Terrestrial DC (external)"
AI_COMPUTE_TOTAL: Final[str] = "AI - Compute — total"
AI_APPS_CAC_CUSTOMER: Final[str] = "AI Apps CAC ($/customer)"
AI_APPS_GPU_HR_PER_TRILLION_TOKENS: Final[str] = "AI Apps GPU-hr per trillion tokens"
AI_APPS_ATTRIBUTED_COMPUTE_CAPITAL_PER_SUB: Final[str] = "AI Apps attributed compute capital per sub ($)"
AI_APPS_REVENUE_MM: Final[str] = "AI Apps revenue ($mm)"
AI_APPS_SERVED_GPU_HRS_CAPPED: Final[str] = "AI Apps served (GPU-hrs, capped)"
AI_APPS_SHARE_OF_DC_COMPUTE: Final[str] = "AI Apps share of DC compute"
AI_APPS_SUBS_M: Final[str] = "AI Apps subs (M)"
AI_APPS_TOKENS_T: Final[str] = "AI Apps tokens (T)"
AI_APPS_TOKENS_PER_QUERY_INTENSITY_CAGR: Final[str] = "AI Apps tokens-per-query intensity CAGR"
AI_APPS_PAYING_USERS_M: Final[str] = "AI Apps: paying users (M)"
AI_APPS_TOTAL_REVENUE_MM: Final[str] = "AI Apps: total revenue ($mm)"
AI_APPS_TOTAL_TOKENS_T: Final[str] = "AI Apps: total tokens (T)"
AI_STACK_RETIRED_SUPERSEDED_BY_THE_AI_COMPUTE_SECTION_MEMOS_BELOW_RETAINED: Final[str] = "AI STACK — RETIRED, superseded by the AI/Compute section. Memos below retained."
AI_STACK_R_D_CAGR: Final[str] = "AI Stack R&D CAGR"
AI_STACK_R_D_FLOOR_PCT: Final[str] = "AI Stack R&D floor pct"
AI_STACK_R_D_START_PCT: Final[str] = "AI Stack R&D start pct"
AI_STACK_INSURANCE_PCT_REV: Final[str] = "AI Stack insurance pct rev"
AI_STACK_OTHER_COGS_PCT_REV: Final[str] = "AI Stack other COGS pct rev"
AI_COMPUTE_DEMAND_REFERENCE_M_H100_EQ_GPU_SEED_ANCHORED_S_CURVE_A8_5: Final[str] = "AI compute demand reference (M H100-eq GPU): seed-anchored S-curve (A8.5)"
AI_COMPUTE_DEMAND_CURVE_ELASTICITY_B: Final[str] = "AI compute demand-curve elasticity b"
AI_ORBITAL_COMPUTE_TAM_CEILING_M_H100_EQ_GPU: Final[str] = "AI orbital compute TAM ceiling (M H100-eq GPU)"
AI_ORBITAL_COMPUTE_ADOPTION_STEEPNESS_K: Final[str] = "AI orbital compute adoption steepness k"
AI_COMPUTE_ODC: Final[str] = "AI-Compute / ODC"
AI_ODC_FIRST_COMPUTE_SAT_BUILD_YEAR: Final[str] = "AI: ODC first compute-sat build year"
AIAPPS_API_ARPU_ACCT_YR: Final[str] = "AIApps API: ARPU ($/acct/yr)"
AIAPPS_API_ARPU_CAGR_YR: Final[str] = "AIApps API: ARPU CAGR (/yr)"
AIAPPS_API_TOKENS_USER_2025_M_YR: Final[str] = "AIApps API: tokens/user 2025 (M/yr)"
AIAPPS_API_TOKENS_USER_CAGR_YR: Final[str] = "AIApps API: tokens/user CAGR (/yr)"
AIAPPS_API_USER_CAGR_YR: Final[str] = "AIApps API: user CAGR (/yr)"
AIAPPS_API_USERS_2025_M: Final[str] = "AIApps API: users 2025 (M)"
AIAPPS_ADS_ARPU_USER_YR: Final[str] = "AIApps Ads: ARPU ($/user/yr)"
AIAPPS_ADS_ARPU_CAGR_YR: Final[str] = "AIApps Ads: ARPU CAGR (/yr)"
AIAPPS_AGENTIC_ARPU_USER_YR: Final[str] = "AIApps Agentic: ARPU ($/user/yr)"
AIAPPS_AGENTIC_ARPU_CAGR_YR: Final[str] = "AIApps Agentic: ARPU CAGR (/yr)"
AIAPPS_AGENTIC_TOKENS_USER_2025_M_YR: Final[str] = "AIApps Agentic: tokens/user 2025 (M/yr)"
AIAPPS_AGENTIC_TOKENS_USER_CAGR_YR: Final[str] = "AIApps Agentic: tokens/user CAGR (/yr)"
AIAPPS_AGENTIC_USER_CAGR_YR: Final[str] = "AIApps Agentic: user CAGR (/yr)"
AIAPPS_AGENTIC_USERS_2025_M: Final[str] = "AIApps Agentic: users 2025 (M)"
AIAPPS_ENT_ARPU_SEAT_YR: Final[str] = "AIApps Ent: ARPU ($/seat/yr)"
AIAPPS_ENT_ARPU_CAGR_YR: Final[str] = "AIApps Ent: ARPU CAGR (/yr)"
AIAPPS_ENT_SEATS_2025_M: Final[str] = "AIApps Ent: seats 2025 (M)"
AIAPPS_ENT_TOKENS_USER_2025_M_YR: Final[str] = "AIApps Ent: tokens/user 2025 (M/yr)"
AIAPPS_ENT_TOKENS_USER_CAGR_YR: Final[str] = "AIApps Ent: tokens/user CAGR (/yr)"
AIAPPS_ENT_USER_CAGR_YR: Final[str] = "AIApps Ent: user CAGR (/yr)"
AIAPPS_FREE_ARPU_USER_YR: Final[str] = "AIApps Free: ARPU ($/user/yr)"
AIAPPS_FREE_ARPU_CAGR_YR: Final[str] = "AIApps Free: ARPU CAGR (/yr)"
AIAPPS_FREE_TOKENS_USER_2025_M_YR: Final[str] = "AIApps Free: tokens/user 2025 (M/yr)"
AIAPPS_FREE_TOKENS_USER_CAGR_YR: Final[str] = "AIApps Free: tokens/user CAGR (/yr)"
AIAPPS_FREE_USER_CAGR_YR: Final[str] = "AIApps Free: user CAGR (/yr)"
AIAPPS_FREE_USERS_2025_M: Final[str] = "AIApps Free: users 2025 (M)"
AIAPPS_INDIV_ARPU_USER_YR: Final[str] = "AIApps Indiv: ARPU ($/user/yr)"
AIAPPS_INDIV_ARPU_CAGR_YR: Final[str] = "AIApps Indiv: ARPU CAGR (/yr)"
AIAPPS_INDIV_TOKENS_USER_2025_M_YR: Final[str] = "AIApps Indiv: tokens/user 2025 (M/yr)"
AIAPPS_INDIV_TOKENS_USER_CAGR_YR: Final[str] = "AIApps Indiv: tokens/user CAGR (/yr)"
AIAPPS_INDIV_USER_CAGR_YR: Final[str] = "AIApps Indiv: user CAGR (/yr)"
AIAPPS_INDIV_USERS_2025_M: Final[str] = "AIApps Indiv: users 2025 (M)"
AIAPPS_MERCHANT_IAAS_DEMAND_SCALE: Final[str] = "AIApps Merchant IaaS demand scale (×)"
ALL_OK_R108_EQUIVALENT: Final[str] = "ALL OK (R108-equivalent)"
ALLOCATOR: Final[str] = "ALLOCATOR"
ACCRUAL_CASH_FCF_RECONCILIATION: Final[str] = "Accrual↔cash FCF reconciliation"
ACTIVE_RETAIL_SATS_BB_DTC_EOY: Final[str] = "Active retail sats (BB + DTC, EoY)"
ACTIVE_SAT_FLEET_EOY: Final[str] = "Active sat fleet (EoY)"
ACTIVE_GEN_BB_CAPEX_SLUG_MM_SAT: Final[str] = "Active-gen BB CapEx slug ($mm/sat)"
ACTIVE_GEN_BB_SPOT_IRR_PRIOR_YR: Final[str] = "Active-gen BB Spot IRR (prior yr)"
ACTIVE_GEN_DTC_CAPEX_SLUG_MM_SAT: Final[str] = "Active-gen DTC CapEx slug ($mm/sat)"
ACTIVE_GEN_DTC_SPOT_IRR_PRIOR_YR: Final[str] = "Active-gen DTC Spot IRR (prior yr)"
ADS_ARPU_USER_YR: Final[str] = "Ads: ARPU ($/user/yr)"
ADS_MONETIZABLE_BASE_M: Final[str] = "Ads: monetizable base (M)"
ADS_REVENUE_MM: Final[str] = "Ads: revenue ($mm)"
AGENTIC_CODING_ARPU_USER_YR: Final[str] = "Agentic coding: ARPU ($/user/yr)"
AGENTIC_CODING_REVENUE_MM: Final[str] = "Agentic coding: revenue ($mm)"
AGENTIC_CODING_TOKENS_T: Final[str] = "Agentic coding: tokens (T)"
AGENTIC_CODING_TOKENS_USER_M_YR: Final[str] = "Agentic coding: tokens/user (M/yr)"
AGENTIC_CODING_USERS_M: Final[str] = "Agentic coding: users (M)"
ALLOCATED_CASH_TO_AI_COMPUTE_MM: Final[str] = "Allocated cash to AI-Compute ($mm)"
ALLOCATED_CASH_TO_CUSTOMER_LAUNCH_MM: Final[str] = "Allocated cash to Customer Launch ($mm)"
ALLOCATED_CASH_TO_STARLINK_MM: Final[str] = "Allocated cash to Starlink ($mm)"
ALLOCATED_CASH_ODC_MM: Final[str] = "Allocated cash → ODC ($mm)"
ALLOCATED_CASH_TERRESTRIAL_MM: Final[str] = "Allocated cash → Terrestrial ($mm)"
ALLOCATED_FINAL_AI_COMPUTE_MM: Final[str] = "Allocated final: AI-Compute ($mm)"
ALLOCATED_FINAL_CUSTOMER_LAUNCH_MM: Final[str] = "Allocated final: Customer Launch ($mm)"
ALLOCATED_FINAL_STARLINK_MM: Final[str] = "Allocated final: Starlink ($mm)"
ALLOCATION_SHARE_AI_COMPUTE: Final[str] = "Allocation share: AI-Compute"
ALLOCATION_SHARE_CUSTOMER_LAUNCH: Final[str] = "Allocation share: Customer Launch"
ALLOCATION_SHARE_STARLINK: Final[str] = "Allocation share: Starlink"
ALLOCATION_SHARE_ORBITAL_ODC: Final[str] = "Allocation share: orbital (ODC)"
ALLOCATION_SHARE_TERRESTRIAL: Final[str] = "Allocation share: terrestrial"
ALLOCATION_SHARPNESS_TOP_LEVEL_3_MODULE_BLEND: Final[str] = "Allocation sharpness β (top-level 3-module blend)"
ALLOCATION_SHARPNESS_AI_ORBITAL_TERRESTRIAL_SUB_SPLIT: Final[str] = "Allocation sharpness β: AI orbital / terrestrial sub-split"
ALLOCATION_SHARPNESS_STARLINK_BROADBAND_DIRECT_TO_CELL_SUB_SPLIT: Final[str] = "Allocation sharpness β: Starlink broadband / direct-to-cell sub-split"
ALLOCATION_WEIGHT_BROADBAND_V2_ERA_1: Final[str] = "Allocation weight: broadband (V2 era = 1)"
ALLOCATION_WEIGHT_DIRECT_TO_CELL: Final[str] = "Allocation weight: direct-to-cell"
ALLOCATOR_MIN_SOFTMAX_SHARE_FLOOR_PER_MODULE_FRAC: Final[str] = "Allocator min softmax share floor per module (frac)"
ANNUAL_TAM_SHIFT_MULTIPLIER: Final[str] = "Annual TAM shift multiplier"
ANNUAL_ESCALATOR_RATE_DERIVED_YEAR_ROW: Final[str] = "Annual escalator rate (derived, year-row)"
AS_OF_VALUATION_DATES: Final[str] = "As-of valuation dates →"
ASSET_INSURANCE_COGS_MM: Final[str] = "Asset insurance COGS ($mm)"
ASSET_INSURANCE_COGS_OF_REVENUE: Final[str] = "Asset insurance COGS (% of revenue)"
ASSET_LIFE_L_AI_APPS_YRS: Final[str] = "Asset life L: AI Apps (yrs)"
ASSET_LIFE_L_AI_COMPUTE_AI_APPS_YEARS: Final[str] = "Asset life L: AI/Compute AI Apps (years)"
ASSET_LIFE_L_AI_COMPUTE_ORBITAL_DC_YEARS: Final[str] = "Asset life L: AI/Compute Orbital DC (years)"
ASSET_LIFE_L_AI_COMPUTE_TERRESTRIAL_DC_YEARS: Final[str] = "Asset life L: AI/Compute Terrestrial DC (years)"
ASSET_LIFE_L_CUSTOMER_LAUNCH_F9_YEARS: Final[str] = "Asset life L: Customer Launch F9 (years)"
ASSET_LIFE_L_CUSTOMER_LAUNCH_STARSHIP_YEARS: Final[str] = "Asset life L: Customer Launch Starship (years)"
ASSET_LIFE_L_ORBITAL_DC_YRS: Final[str] = "Asset life L: Orbital DC (yrs)"
ASSET_LIFE_L_TERRESTRIAL_DC_YRS: Final[str] = "Asset life L: Terrestrial DC (yrs)"
ATTRIBUTED_R_D: Final[str] = "Attributed R&D"
ATTRIBUTED_R_D_MM: Final[str] = "Attributed R&D ($mm)"
ATTRIBUTED_R_D_MM_ALLOCATOR_OUT: Final[str] = "Attributed R&D ($mm)   ◄ Allocator OUT"
ATTRIBUTED_R_D_MM_COMPONENT_OF_MODULE_OPEX_TOTAL_ROW_87: Final[str] = "Attributed R&D ($mm): component of Module OpEx total (row 87)"
ATTRIBUTED_R_D_AI_COMPUTE: Final[str] = "Attributed R&D: AI - Compute"
ATTRIBUTED_R_D_CUSTOMER_LAUNCH: Final[str] = "Attributed R&D: Customer Launch"
ATTRIBUTED_R_D_CUSTOMER_LAUNCH_STARSHIP_R_D_LIFTED_TO_SHARED: Final[str] = "Attributed R&D: Customer Launch (Starship R&D lifted to Shared)"
ATTRIBUTED_R_D_LUNAR_MARS: Final[str] = "Attributed R&D: Lunar - Mars"
AVG_GBPS_BB_AT_Q_PRICE_AT_Q: Final[str] = "Avg $/Gbps BB at Q (price-at-Q)"
AVG_GBPS_DTC_AT_Q_PRICE_AT_Q: Final[str] = "Avg $/Gbps DTC at Q (price-at-Q)"
BB_BANDWIDTH_GBPS_BY_COHORT: Final[str] = "BB BANDWIDTH (Gbps by cohort)"
BB_BOY_SUBSCRIBERS_M: Final[str] = "BB BoY subscribers (M)"
BB_DEMAND_CURVE_PIECEWISE_LINEAR_Q_REVENUE_LOOKUP: Final[str] = "BB DEMAND CURVE (piecewise-linear Q→Revenue lookup)"
BB_EOY_SUBSCRIBERS_REVENUE_IMPLIED_LEVEL_M_STABILISED: Final[str] = "BB EoY subscribers (= revenue-implied level, M): stabilised"
BB_FLEET_ACTIVE_SATS_BY_COHORT: Final[str] = "BB FLEET (active sats by cohort)"
BB_GBPS_AVAILABLE_FOR_EXTERNAL_STARLINK_REVENUE: Final[str] = "BB Gbps available for external Starlink revenue"
BB_Q_BREAKPOINT_1_GBPS: Final[str] = "BB Q breakpoint #1 (Gbps)"
BB_Q_BREAKPOINT_10_GBPS: Final[str] = "BB Q breakpoint #10 (Gbps)"
BB_Q_BREAKPOINT_11_GBPS: Final[str] = "BB Q breakpoint #11 (Gbps)"
BB_Q_BREAKPOINT_12_GBPS: Final[str] = "BB Q breakpoint #12 (Gbps)"
BB_Q_BREAKPOINT_13_GBPS: Final[str] = "BB Q breakpoint #13 (Gbps)"
BB_Q_BREAKPOINT_14_GBPS: Final[str] = "BB Q breakpoint #14 (Gbps)"
BB_Q_BREAKPOINT_15_GBPS: Final[str] = "BB Q breakpoint #15 (Gbps)"
BB_Q_BREAKPOINT_16_GBPS: Final[str] = "BB Q breakpoint #16 (Gbps)"
BB_Q_BREAKPOINT_17_GBPS: Final[str] = "BB Q breakpoint #17 (Gbps)"
BB_Q_BREAKPOINT_18_GBPS: Final[str] = "BB Q breakpoint #18 (Gbps)"
BB_Q_BREAKPOINT_19_GBPS: Final[str] = "BB Q breakpoint #19 (Gbps)"
BB_Q_BREAKPOINT_2_GBPS: Final[str] = "BB Q breakpoint #2 (Gbps)"
BB_Q_BREAKPOINT_20_GBPS: Final[str] = "BB Q breakpoint #20 (Gbps)"
BB_Q_BREAKPOINT_21_GBPS: Final[str] = "BB Q breakpoint #21 (Gbps)"
BB_Q_BREAKPOINT_22_GBPS: Final[str] = "BB Q breakpoint #22 (Gbps)"
BB_Q_BREAKPOINT_23_GBPS: Final[str] = "BB Q breakpoint #23 (Gbps)"
BB_Q_BREAKPOINT_24_GBPS: Final[str] = "BB Q breakpoint #24 (Gbps)"
BB_Q_BREAKPOINT_25_GBPS: Final[str] = "BB Q breakpoint #25 (Gbps)"
BB_Q_BREAKPOINT_26_GBPS: Final[str] = "BB Q breakpoint #26 (Gbps)"
BB_Q_BREAKPOINT_27_GBPS: Final[str] = "BB Q breakpoint #27 (Gbps)"
BB_Q_BREAKPOINT_28_GBPS: Final[str] = "BB Q breakpoint #28 (Gbps)"
BB_Q_BREAKPOINT_29_GBPS: Final[str] = "BB Q breakpoint #29 (Gbps)"
BB_Q_BREAKPOINT_3_GBPS: Final[str] = "BB Q breakpoint #3 (Gbps)"
BB_Q_BREAKPOINT_30_GBPS: Final[str] = "BB Q breakpoint #30 (Gbps)"
BB_Q_BREAKPOINT_31_GBPS: Final[str] = "BB Q breakpoint #31 (Gbps)"
BB_Q_BREAKPOINT_32_GBPS: Final[str] = "BB Q breakpoint #32 (Gbps)"
BB_Q_BREAKPOINT_33_GBPS: Final[str] = "BB Q breakpoint #33 (Gbps)"
BB_Q_BREAKPOINT_34_GBPS: Final[str] = "BB Q breakpoint #34 (Gbps)"
BB_Q_BREAKPOINT_35_GBPS: Final[str] = "BB Q breakpoint #35 (Gbps)"
BB_Q_BREAKPOINT_36_GBPS: Final[str] = "BB Q breakpoint #36 (Gbps)"
BB_Q_BREAKPOINT_37_GBPS: Final[str] = "BB Q breakpoint #37 (Gbps)"
BB_Q_BREAKPOINT_38_GBPS: Final[str] = "BB Q breakpoint #38 (Gbps)"
BB_Q_BREAKPOINT_39_GBPS: Final[str] = "BB Q breakpoint #39 (Gbps)"
BB_Q_BREAKPOINT_4_GBPS: Final[str] = "BB Q breakpoint #4 (Gbps)"
BB_Q_BREAKPOINT_40_GBPS: Final[str] = "BB Q breakpoint #40 (Gbps)"
BB_Q_BREAKPOINT_41_GBPS: Final[str] = "BB Q breakpoint #41 (Gbps)"
BB_Q_BREAKPOINT_42_GBPS: Final[str] = "BB Q breakpoint #42 (Gbps)"
BB_Q_BREAKPOINT_43_GBPS: Final[str] = "BB Q breakpoint #43 (Gbps)"
BB_Q_BREAKPOINT_44_GBPS: Final[str] = "BB Q breakpoint #44 (Gbps)"
BB_Q_BREAKPOINT_45_GBPS: Final[str] = "BB Q breakpoint #45 (Gbps)"
BB_Q_BREAKPOINT_46_GBPS: Final[str] = "BB Q breakpoint #46 (Gbps)"
BB_Q_BREAKPOINT_47_GBPS: Final[str] = "BB Q breakpoint #47 (Gbps)"
BB_Q_BREAKPOINT_48_GBPS: Final[str] = "BB Q breakpoint #48 (Gbps)"
BB_Q_BREAKPOINT_49_GBPS: Final[str] = "BB Q breakpoint #49 (Gbps)"
BB_Q_BREAKPOINT_5_GBPS: Final[str] = "BB Q breakpoint #5 (Gbps)"
BB_Q_BREAKPOINT_50_GBPS: Final[str] = "BB Q breakpoint #50 (Gbps)"
BB_Q_BREAKPOINT_51_GBPS: Final[str] = "BB Q breakpoint #51 (Gbps)"
BB_Q_BREAKPOINT_52_GBPS: Final[str] = "BB Q breakpoint #52 (Gbps)"
BB_Q_BREAKPOINT_53_GBPS: Final[str] = "BB Q breakpoint #53 (Gbps)"
BB_Q_BREAKPOINT_54_GBPS: Final[str] = "BB Q breakpoint #54 (Gbps)"
BB_Q_BREAKPOINT_55_GBPS: Final[str] = "BB Q breakpoint #55 (Gbps)"
BB_Q_BREAKPOINT_56_GBPS: Final[str] = "BB Q breakpoint #56 (Gbps)"
BB_Q_BREAKPOINT_6_GBPS: Final[str] = "BB Q breakpoint #6 (Gbps)"
BB_Q_BREAKPOINT_7_GBPS: Final[str] = "BB Q breakpoint #7 (Gbps)"
BB_Q_BREAKPOINT_8_GBPS: Final[str] = "BB Q breakpoint #8 (Gbps)"
BB_Q_BREAKPOINT_9_GBPS: Final[str] = "BB Q breakpoint #9 (Gbps)"
BB_TAM_UPLIFT_MULTIPLIER_DATA_INTENSITY_DERIVED_YEAR_ROW: Final[str] = "BB TAM uplift multiplier (data-intensity, derived year-row)"
BB_TAM_UPLIFT_RAMP_END_YRS_FROM_2025: Final[str] = "BB TAM uplift ramp-end (yrs from 2025)"
BB_TAM_UPLIFT_TARGET_DATA_INTENSITY_VALUE_PER_CONNECTION: Final[str] = "BB TAM uplift target: data-intensity / value-per-connection (×)"
BB_ACTIVE_GBPS_V2_V3_COMBINED: Final[str] = "BB active Gbps (V2+V3 combined)"
BB_DEMAND_CURVE_LEVEL_MULTIPLIER: Final[str] = "BB demand curve level multiplier"
BB_NET_ADDS_M: Final[str] = "BB net adds (M)"
BB_POOL_AT_COST_GBPS_YR: Final[str] = "BB pool at-cost $/Gbps/yr"
BB_SUBSCRIBERS_REVENUE_IMPLIED_LEVEL_M: Final[str] = "BB subscribers: revenue-implied level (M)"
BB_SHARE_OF_BANDWIDTH_RATIO: Final[str] = "BB-share of bandwidth (ratio)"
BANDWIDTH: Final[str] = "Bandwidth"
BANDWIDTH_COST_MM: Final[str] = "Bandwidth cost ($mm)"
BANDWIDTH_PEERING_COST_PER_GBPS_MM_GBPS_YR: Final[str] = "Bandwidth/peering cost per Gbps ($mm/Gbps-yr)"
BASE_TURNAROUND_TIME_PER_BOOSTER_YEARS_FLIGHT: Final[str] = "Base turnaround time per booster (years/flight)"
BATTERY_SAT: Final[str] = "Battery $/sat"
BILLABLE_H100_EQ_GPU_HRS: Final[str] = "Billable H100-eq GPU-hrs"
BILLABLE_H100_EQ_GPU_HRS_SAT: Final[str] = "Billable H100-eq GPU-hrs/sat"
BLENDED_KIT_SALE_PRICE_KIT: Final[str] = "Blended kit sale price ($/kit)"
BLENDED_NEW_SAT_CAPEX_SLUG_MM_SAT_MEMO_ONLY_FEEDS_CAE_R88_CAP_NO_LONGER_DRIVES_DEPLOYMENT: Final[str] = "Blended new-sat CapEx slug ($mm/sat): MEMO ONLY (feeds CAE R88 cap; no longer drives deployment)"
BLENDED_NEW_SAT_MASS_KG_SAT_SHARE_WEIGHTED_REGIME_GATED_ACYCLIC: Final[str] = "Blended new-sat mass (kg/sat): share-weighted, regime-gated (acyclic)"
BOOSTER_BUILD_CAPEX_MM: Final[str] = "Booster build CapEx ($mm)"
BOOSTER_CADENCE_FLOOR_FLIGHTS_YR_OPERATIONAL: Final[str] = "Booster cadence floor (flights/yr, operational)"
BOOSTER_FLEET_BOY_UNITS: Final[str] = "Booster fleet BoY (units)"
BOOSTER_FLEET_EOY_UNITS: Final[str] = "Booster fleet EoY (units)"
BOOSTER_MFG_PER_STACK_MM: Final[str] = "Booster mfg per stack ($mm)"
BOOSTERS_BUILT_FLEET: Final[str] = "Boosters built (fleet)"
BOOSTERS_BUILT_THIS_YEAR_VEHICLE_BUILD_BOOSTERS_BUILT_FLEET: Final[str] = "Boosters built this year (= Vehicle Build Boosters built (fleet))"
BOOSTERS_NEEDED_FLEET: Final[str] = "Boosters needed (fleet)"
BOOSTERS_RETIRED_FLEET: Final[str] = "Boosters retired (fleet)"
BOUNDARY_TIE_FACILITIES_BUILD_CHIPS_ODC_R55_TERR_R94_TOGGLE_MUST_0: Final[str] = "Boundary tie: 'Facilities Build' chips − (ODC R55 + Terr R94)×toggle; must = 0"
BROADBAND_ARPU_SUB_MO_YEAR_ROW: Final[str] = "Broadband ARPU ($/sub/mo): year-row"
CAC_SLUG_PER_CUSTOMER: Final[str] = "CAC slug per customer ($)"
CAPACITY_STARSHIP_F9: Final[str] = "CAPACITY (Starship + F9)"
CAPACITY_CAPEX_TRANSFER_REVENUE: Final[str] = "CAPACITY + CapEx + TRANSFER REVENUE"
CAPEX_CORPORATE_SPECTRUM_MODULE_AGGREGATION: Final[str] = "CAPEX (corporate + spectrum + module aggregation)"
COGS: Final[str] = "COGS"
COGS_MM: Final[str] = "COGS ($mm)"
COGS_TOTAL: Final[str] = "COGS total"
COGS_TOTAL_MM: Final[str] = "COGS total ($mm)"
COGS_TOTAL_MM_ALLOCATOR_OUT: Final[str] = "COGS total ($mm)   ◄ Allocator OUT"
COGS_AI_COMPUTE: Final[str] = "COGS: AI - Compute"
COGS_CUSTOMER_LAUNCH: Final[str] = "COGS: Customer Launch"
COGS_LUNAR_MARS: Final[str] = "COGS: Lunar - Mars"
COGS_STARLINK: Final[str] = "COGS: Starlink"
CONSERVATION_IDENTITY_CHECKS: Final[str] = "CONSERVATION: identity checks"
CUM_UPMASS_FLEET_ROLL_FORWARD: Final[str] = "CUM-UPMASS + FLEET ROLL-FORWARD"
CUSTOMER_LAUNCH: Final[str] = "CUSTOMER LAUNCH"
CADENCE_CEILING_FLIGHTS_BOOSTER_YEAR: Final[str] = "Cadence ceiling (flights/booster/year)"
CAP_SCALE_FACTOR_1_PRO_RATA: Final[str] = "Cap scale factor (≤1, pro-rata)"
CAP_AI_COMPUTE_MAX_DEPLOYABLE_MM: Final[str] = "Cap: AI-Compute max deployable ($mm)"
CAP_CUSTOMER_LAUNCH_MAX_DEPLOYABLE_MM: Final[str] = "Cap: Customer Launch max deployable ($mm)"
CAP_STARLINK_MAX_DEPLOYABLE_MM: Final[str] = "Cap: Starlink max deployable ($mm)"
CAPEX_MM: Final[str] = "CapEx ($mm)"
CAPEX_FACILITY_CHIPS_MM: Final[str] = "CapEx - facility + chips ($mm)"
CAPEX_SAT_FLEET_INCL_CHIPS_MM: Final[str] = "CapEx - sat fleet incl chips ($mm)"
CAPEX_SLUG_PER_MW_MM: Final[str] = "CapEx slug per MW ($mm)"
CAPEX_SLUG_PER_SAT_MM: Final[str] = "CapEx slug per sat ($mm)"
CAPEX_AI_COMPUTE: Final[str] = "CapEx: AI - Compute"
CAPEX_CORPORATE: Final[str] = "CapEx: Corporate"
CAPEX_CUSTOMER_LAUNCH: Final[str] = "CapEx: Customer Launch"
CAPEX_LUNAR_MARS: Final[str] = "CapEx: Lunar - Mars"
CAPEX_STARLINK: Final[str] = "CapEx: Starlink"
CAPACITY_GBPS: Final[str] = "Capacity (Gbps)"
CAPACITY_AVAILABLE_AFTER_LM_KG: Final[str] = "Capacity available after LM (kg)"
CAPITAL_DEPLOYED_CUMULATIVE: Final[str] = "Capital Deployed (cumulative)"
CAPITAL_LIFETIME_BV_STRAIGHT_LINE_DEP_YRS: Final[str] = "Capital lifetime: BV straight-line dep (yrs)"
CAPITAL_LIFETIME_BV_STRAIGHT_LINE_DEPRECIATION_YEARS: Final[str] = "Capital lifetime: BV straight-line depreciation (years)"
CAPPED_AI_COMPUTE_MM: Final[str] = "Capped: AI-Compute ($mm)"
CAPPED_CUSTOMER_LAUNCH_MM: Final[str] = "Capped: Customer Launch ($mm)"
CAPPED_STARLINK_MM: Final[str] = "Capped: Starlink ($mm)"
CARVE_OUT_OF_PRIOR_YEAR_GROUP_FCF: Final[str] = "Carve-out % of prior-year Group FCF"
CARVE_OUT_IRR_SIGNAL_AVG_PRIOR_YR_SPOT_IRR_3_MODULES: Final[str] = "Carve-out IRR signal: avg prior-yr spot IRR (3 modules)"
CARVE_OUT_IRR_RESPONSE_CEILING_MAX_CARVE_OUT_AT_LOW_ANCHOR: Final[str] = "Carve-out IRR-response ceiling % (max carve-out at low anchor)"
CARVE_OUT_IRR_RESPONSE_HIGH_IRR_ANCHOR_BASE_AT_ABOVE: Final[str] = "Carve-out IRR-response high-IRR anchor (base % at/above)"
CARVE_OUT_IRR_RESPONSE_LOW_IRR_ANCHOR_CEILING_AT_BELOW: Final[str] = "Carve-out IRR-response low-IRR anchor (ceiling % at/below)"
CARVE_OUT_IRR_RESPONSE_RAMP_0_1: Final[str] = "Carve-out IRR-response ramp [0,1]"
CARVE_OUT_IRR_RESPONSE_START_YEAR: Final[str] = "Carve-out IRR-response start year"
CARVE_OUT_CASH_RECEIPT_MM: Final[str] = "Carve-out cash receipt ($mm)"
CARVE_OUT_EFFECTIVE_IRR_RESPONSIVE: Final[str] = "Carve-out effective % (IRR-responsive)"
CARVE_OUT_FLOOR_MM_YR: Final[str] = "Carve-out floor ($mm/yr)"
CARVE_OUT_PRE_2028_R_D_ONLY_OVERRIDE_MM_YR: Final[str] = "Carve-out pre-2028 R&D-only override ($mm/yr)"
CASH_BOY_MM: Final[str] = "Cash BoY ($mm)"
CASH_EOY_MM: Final[str] = "Cash EoY ($mm)"
CASH_AVAILABLE_FOR_YEAR_MM: Final[str] = "Cash available for year ($mm)"
CASH_BB_MM: Final[str] = "Cash → BB ($mm)"
CASH_DTC_MM: Final[str] = "Cash → DTC ($mm)"
CASH_FLOW_IDENTITY: Final[str] = "Cash-flow identity"
CHIP_FP8_DENSITY_CAGR_POST_2030: Final[str] = "Chip FP8 density CAGR (post-2030)"
CHIP_FP8_PER_CHIP_TFLOPS: Final[str] = "Chip FP8 per chip (TFLOPS)"
CHIP_FP8_PER_CHIP_CAGR_YR_SMOOTH_CURVE: Final[str] = "Chip FP8 per chip CAGR (/yr): smooth curve"
CHIP_TDP_CAGR_POST_2027_W_CHIP: Final[str] = "Chip TDP CAGR (post-2027, W/chip)"
CHIP_TDP_PER_CHIP_W: Final[str] = "Chip TDP per chip (W)"
CHIP_COST_ASP_CHIP_DERIVED: Final[str] = "Chip cost ASP ($/chip): derived"
CHIP_COST_AT_COST_SAT: Final[str] = "Chip cost at-cost ($/sat)"
CHIP_COST_BASIS_TFLOPS_GEN_ANCHOR_2025: Final[str] = "Chip cost basis ($/TFLOPS, gen anchor @2025)"
CHIP_COST_PER_TFLOPS_DECLINE_RATE_G_PER_FLOP_A8_2: Final[str] = "Chip cost-per-TFLOPS decline rate g (per-FLOP, A8.2)"
CHIP_OPERATING_TEMP_K: Final[str] = "Chip operating temp (K)"
CHIP_PERF_PER_WATT_CAGR_YR: Final[str] = "Chip perf-per-watt CAGR (/yr)"
CHIP_PERF_PER_WATT_ANCHOR_2025_TFLOPS_W: Final[str] = "Chip perf-per-watt anchor 2025 (TFLOPS/W)"
CHIP_PURCHASE_INTERNAL_MM: Final[str] = "Chip purchase internal ($mm)"
CHIP_PURCHASES_INTERNAL_TRANSFER_MM: Final[str] = "Chip purchases (internal transfer) ($mm)"
CHIP_FAB_FACILITY_CAPEX_TOTAL_MM_AI_COMPUTE: Final[str] = "Chip-fab facility CapEx total ($mm)  ◄ AI-Compute"
CHIP_FAB_FACILITY_D_A_TOTAL_MM_AI_COMPUTE: Final[str] = "Chip-fab facility D&A total ($mm)  ◄ AI-Compute"
CHIPS_DEMANDED_THIS_YEAR_COUNT_AI_COMPUTE: Final[str] = "Chips demanded this year (count)  ◄ AI-Compute"
CHIPS_DEPLOYED_COUNT: Final[str] = "Chips deployed (count)"
CHIPS_PER_SAT: Final[str] = "Chips per sat"
COMMERCIAL_LAUNCH_MARKET_SIZE_MM_YEAR_YEAR_ROW: Final[str] = "Commercial launch market size ($mm/year): year-row"
COMMERCIAL_LAUNCH_MARKET_SIZE_MM_YR: Final[str] = "Commercial launch market size ($mm/yr)"
COMMS_ISL_SET_SAT: Final[str] = "Comms ISL set $/sat"
COMP_ANCHOR_AI_STACK_STANDALONE: Final[str] = "Comp anchor: AI Stack standalone"
COMP_ANCHOR_AI_COMPUTE_STANDALONE_COREWEAVE_ANCHORED: Final[str] = "Comp anchor: AI/Compute standalone (CoreWeave-anchored)"
COMP_ANCHOR_CUSTOMER_LAUNCH_STANDALONE_ROCKET_LAB: Final[str] = "Comp anchor: Customer Launch standalone (Rocket Lab)"
COMP_ANCHOR_GROUP_EV_BRANT_INTERNAL: Final[str] = "Comp anchor: Group EV (Brant internal)"
COMP_ANCHOR_GROUP_EV_MORGAN_STANLEY_PUBLIC: Final[str] = "Comp anchor: Group EV (Morgan Stanley public)"
COMP_ANCHOR_LUNAR_MARS_NASA_HLS_LIFETIME: Final[str] = "Comp anchor: Lunar / Mars (NASA HLS lifetime)"
COMP_ANCHOR_STARLINK_STANDALONE_BERNSTEIN_JPM: Final[str] = "Comp anchor: Starlink standalone (Bernstein/JPM)"
COMPUTE_BUILD_HEADROOM_BUFFER_FRAC: Final[str] = "Compute build headroom buffer (frac)"
COMPUTE_POWER_PER_SAT_KW: Final[str] = "Compute power per sat (kW)"
COMPUTE_TRANSFER_DC_INTERNAL_REV_AI_APPS_COGS_0: Final[str] = "Compute transfer: DC internal rev − AI Apps COGS (=0)"
CONSERVATION_LEVEL_2_CASH_TIE_ALLOCATED_DESIRED_NO_CREATION_0_OK_A8_3: Final[str] = "Conservation: Level-2 cash tie: allocated ≤ desired, no creation (≥0 = OK), A8.3"
CONSERVATION_ODC_DRAW_REPAY_BALANCE_MUST_0: Final[str] = "Conservation: ODC Σdraw − Σrepay − balance (must = 0)"
CONSERVATION_FAB_CHIPS_DC_CHIPS_TOGGLE_MUST_0: Final[str] = "Conservation: fab chips − DC chips×toggle; must = 0"
CONSERVATION_MAX_BUCKET_CUM_D_A_CUM_CAPEX_MUST_BE_0: Final[str] = "Conservation: max bucket (cum D&A − cum CapEx): must be ≤ 0"
CONSERVATION_DRAW_REPAY_BALANCE_MUST_0: Final[str] = "Conservation: Σdraw − Σrepay − balance (must = 0)"
CONSTELLATION_BANDWIDTH_GBPS: Final[str] = "Constellation Bandwidth (Gbps)"
CONSTELLATION_D_A_MM: Final[str] = "Constellation D&A ($mm)"
CORPORATE: Final[str] = "Corporate"
CORPORATE_INFRASTRUCTURE_CAPEX_TOTAL_MM: Final[str] = "Corporate & infrastructure CapEx total ($mm)"
CORPORATE_INFRASTRUCTURE_D_A_TOTAL_MM: Final[str] = "Corporate & infrastructure D&A total ($mm)"
CORPORATE_CAPEX_MM: Final[str] = "Corporate CapEx ($mm)"
CORPORATE_SG_A: Final[str] = "Corporate SG&A"
CORPORATE_SG_A_MM: Final[str] = "Corporate SG&A ($mm)"
CORPORATE_IT_HQ_CAPEX_MM: Final[str] = "Corporate, IT & HQ CapEx ($mm)"
CORPORATE_IT_HQ_CAPEX_OF_GROUP_REVENUE: Final[str] = "Corporate, IT & HQ CapEx (% of Group revenue)"
CUM_STARSHIP_BOOSTERS_BUILT_CUMULATIVE_FROM_0: Final[str] = "Cum Starship boosters built (cumulative, from 0)"
CUM_STARSHIP_BOOSTERS_RETIRED_CUMULATIVE_FROM_0: Final[str] = "Cum Starship boosters retired (cumulative, from 0)"
CUM_STARSHIP_EXPERIENCE_UNITS_WRIGHT_S_LAW_COST_BASIS_INCL_2024_BASELINE_F9_INHERITED_SEED_NOT_THE_STANDING_FLEET: Final[str] = "Cum Starship experience units (Wright's-Law cost basis, incl. 2024 baseline + F9-inherited seed; NOT the standing fleet)"
CUM_STARSHIP_SHIPS_BUILT_CUMULATIVE_FROM_0: Final[str] = "Cum Starship ships built (cumulative, from 0)"
CUM_STARSHIP_SHIPS_RETIRED_CUMULATIVE_FROM_0: Final[str] = "Cum Starship ships retired (cumulative, from 0)"
CUM_STARSHIP_UPMASS_FLEET_END_OF_YEAR_KG: Final[str] = "Cum Starship upmass (fleet, end-of-year, kg)"
CUMULATIVE_MODULE_CAPEX_MM: Final[str] = "Cumulative Module CapEx ($mm)"
CUMULATIVE_MODULE_D_A_MM: Final[str] = "Cumulative Module D&A ($mm)"
CUMULATIVE_STARLINK_SATS_BUILT_SATS: Final[str] = "Cumulative Starlink sats built (sats)"
CUMULATIVE_SATS_TARGET_WL: Final[str] = "Cumulative sats (target, WL)"
CUSTOMER_LAUNCH_2: Final[str] = "Customer Launch"
CUSTOMER_LAUNCH_COMMERCIAL: Final[str] = "Customer Launch (commercial)"
CUSTOMER_LAUNCH_F9: Final[str] = "Customer Launch F9"
CUSTOMER_LAUNCH_R_D_CAGR: Final[str] = "Customer Launch R&D % (CAGR)"
CUSTOMER_LAUNCH_R_D_FLOOR: Final[str] = "Customer Launch R&D % (floor)"
CUSTOMER_LAUNCH_R_D_START: Final[str] = "Customer Launch R&D % (start)"
CUSTOMER_LAUNCH_R_D_CAGR_TAPER: Final[str] = "Customer Launch R&D: CAGR (taper)"
CUSTOMER_LAUNCH_R_D_END_STATE_FLOOR: Final[str] = "Customer Launch R&D: end-state % (floor)"
CUSTOMER_LAUNCH_R_D_START_OF_EXTERNAL_REV: Final[str] = "Customer Launch R&D: start % of external rev"
CUSTOMER_LAUNCH_MODULE_SG_A_OF_EXTERNAL_REV: Final[str] = "Customer Launch module SG&A (% of external rev)"
CUSTOMER_LAUNCH_MODULE_MODULE_SPACE_SEGMENT_2_STREAM_REVENUE_4_086M_FULL_WATERFALL_R_D_ABOVE_EBITDA_SEPARATE_F9_STARSHIP_D_A_SPOT_IRR_PER_LAUNCH_D_A_INTERFACE: Final[str] = "Customer Launch module — module = Space segment · 2-stream revenue $4,086M · full waterfall, R&D above EBITDA · separate F9 + Starship D&A · Spot IRR · per-launch D&A interface"
CUSTOMER_LAUNCH_LAUNCH_DEVELOPMENT: Final[str] = "Customer Launch — Launch & Development"
CUSTOMER_LAUNCH_LAUNCH_SERVICES: Final[str] = "Customer Launch — Launch Services"
CUSTOMER_LAUNCH_TOTAL: Final[str] = "Customer Launch — total"
CUSTOMER_SERVICE_FLAT_OF_STARLINK_SUBSCRIPTION_REV: Final[str] = "Customer Service: flat % of Starlink subscription rev"
CUSTOMER_SUPPORT_BILLING_MM: Final[str] = "Customer support & billing ($mm)"
D_A: Final[str] = "D&A"
D_A_MM: Final[str] = "D&A ($mm)"
D_A_LUNAR_MARS_BOOK_VALUE_GUARD: Final[str] = "D&A + Lunar-Mars book-value guard"
D_A_TOTAL_MM: Final[str] = "D&A total ($mm)"
D_A_TOTAL_MM_ALLOCATOR_OUT: Final[str] = "D&A total ($mm)   ◄ Allocator OUT"
D_A_AI_COMPUTE: Final[str] = "D&A: AI - Compute"
D_A_CORPORATE_FACILITIES: Final[str] = "D&A: Corporate / facilities"
D_A_CUSTOMER_LAUNCH: Final[str] = "D&A: Customer Launch"
D_A_LUNAR_MARS: Final[str] = "D&A: Lunar - Mars"
D_A_STARLINK: Final[str] = "D&A: Starlink"
DF_AS_OF2026_2026_1_000: Final[str] = "DF as-of2026 @2026 = 1.000"
DF_AS_OF2040_2040_1_000: Final[str] = "DF as-of2040 @2040 = 1.000"
DF_AS_OF_2026: Final[str] = "DF: as-of 2026"
DF_AS_OF_2030: Final[str] = "DF: as-of 2030"
DF_AS_OF_2035: Final[str] = "DF: as-of 2035"
DF_AS_OF_2040: Final[str] = "DF: as-of 2040"
DTC_ARPU_SUB_MO_YEAR_ROW: Final[str] = "DTC ARPU ($/sub/mo): year-row"
DTC_DEMAND_CURVE_PIECEWISE_LINEAR_Q_REVENUE_LOOKUP: Final[str] = "DTC DEMAND CURVE (piecewise-linear Q→Revenue lookup)"
DTC_FLEET_BANDWIDTH: Final[str] = "DTC FLEET + BANDWIDTH"
DTC_GBPS_AVAILABLE_FOR_EXTERNAL_STARLINK_REVENUE: Final[str] = "DTC Gbps available for external Starlink revenue"
DTC_Q_BREAKPOINT_1_GBPS: Final[str] = "DTC Q breakpoint #1 (Gbps)"
DTC_Q_BREAKPOINT_10_GBPS: Final[str] = "DTC Q breakpoint #10 (Gbps)"
DTC_Q_BREAKPOINT_11_GBPS: Final[str] = "DTC Q breakpoint #11 (Gbps)"
DTC_Q_BREAKPOINT_12_GBPS: Final[str] = "DTC Q breakpoint #12 (Gbps)"
DTC_Q_BREAKPOINT_13_GBPS: Final[str] = "DTC Q breakpoint #13 (Gbps)"
DTC_Q_BREAKPOINT_14_GBPS: Final[str] = "DTC Q breakpoint #14 (Gbps)"
DTC_Q_BREAKPOINT_15_GBPS: Final[str] = "DTC Q breakpoint #15 (Gbps)"
DTC_Q_BREAKPOINT_16_GBPS: Final[str] = "DTC Q breakpoint #16 (Gbps)"
DTC_Q_BREAKPOINT_17_GBPS: Final[str] = "DTC Q breakpoint #17 (Gbps)"
DTC_Q_BREAKPOINT_18_GBPS: Final[str] = "DTC Q breakpoint #18 (Gbps)"
DTC_Q_BREAKPOINT_19_GBPS: Final[str] = "DTC Q breakpoint #19 (Gbps)"
DTC_Q_BREAKPOINT_2_GBPS: Final[str] = "DTC Q breakpoint #2 (Gbps)"
DTC_Q_BREAKPOINT_20_GBPS: Final[str] = "DTC Q breakpoint #20 (Gbps)"
DTC_Q_BREAKPOINT_21_GBPS: Final[str] = "DTC Q breakpoint #21 (Gbps)"
DTC_Q_BREAKPOINT_22_GBPS: Final[str] = "DTC Q breakpoint #22 (Gbps)"
DTC_Q_BREAKPOINT_23_GBPS: Final[str] = "DTC Q breakpoint #23 (Gbps)"
DTC_Q_BREAKPOINT_24_GBPS: Final[str] = "DTC Q breakpoint #24 (Gbps)"
DTC_Q_BREAKPOINT_25_GBPS: Final[str] = "DTC Q breakpoint #25 (Gbps)"
DTC_Q_BREAKPOINT_26_GBPS: Final[str] = "DTC Q breakpoint #26 (Gbps)"
DTC_Q_BREAKPOINT_27_GBPS: Final[str] = "DTC Q breakpoint #27 (Gbps)"
DTC_Q_BREAKPOINT_28_GBPS: Final[str] = "DTC Q breakpoint #28 (Gbps)"
DTC_Q_BREAKPOINT_29_GBPS: Final[str] = "DTC Q breakpoint #29 (Gbps)"
DTC_Q_BREAKPOINT_3_GBPS: Final[str] = "DTC Q breakpoint #3 (Gbps)"
DTC_Q_BREAKPOINT_30_GBPS: Final[str] = "DTC Q breakpoint #30 (Gbps)"
DTC_Q_BREAKPOINT_31_GBPS: Final[str] = "DTC Q breakpoint #31 (Gbps)"
DTC_Q_BREAKPOINT_32_GBPS: Final[str] = "DTC Q breakpoint #32 (Gbps)"
DTC_Q_BREAKPOINT_33_GBPS: Final[str] = "DTC Q breakpoint #33 (Gbps)"
DTC_Q_BREAKPOINT_34_GBPS: Final[str] = "DTC Q breakpoint #34 (Gbps)"
DTC_Q_BREAKPOINT_35_GBPS: Final[str] = "DTC Q breakpoint #35 (Gbps)"
DTC_Q_BREAKPOINT_36_GBPS: Final[str] = "DTC Q breakpoint #36 (Gbps)"
DTC_Q_BREAKPOINT_37_GBPS: Final[str] = "DTC Q breakpoint #37 (Gbps)"
DTC_Q_BREAKPOINT_38_GBPS: Final[str] = "DTC Q breakpoint #38 (Gbps)"
DTC_Q_BREAKPOINT_39_GBPS: Final[str] = "DTC Q breakpoint #39 (Gbps)"
DTC_Q_BREAKPOINT_4_GBPS: Final[str] = "DTC Q breakpoint #4 (Gbps)"
DTC_Q_BREAKPOINT_40_GBPS: Final[str] = "DTC Q breakpoint #40 (Gbps)"
DTC_Q_BREAKPOINT_41_GBPS: Final[str] = "DTC Q breakpoint #41 (Gbps)"
DTC_Q_BREAKPOINT_42_GBPS: Final[str] = "DTC Q breakpoint #42 (Gbps)"
DTC_Q_BREAKPOINT_43_GBPS: Final[str] = "DTC Q breakpoint #43 (Gbps)"
DTC_Q_BREAKPOINT_44_GBPS: Final[str] = "DTC Q breakpoint #44 (Gbps)"
DTC_Q_BREAKPOINT_45_GBPS: Final[str] = "DTC Q breakpoint #45 (Gbps)"
DTC_Q_BREAKPOINT_46_GBPS: Final[str] = "DTC Q breakpoint #46 (Gbps)"
DTC_Q_BREAKPOINT_47_GBPS: Final[str] = "DTC Q breakpoint #47 (Gbps)"
DTC_Q_BREAKPOINT_48_GBPS: Final[str] = "DTC Q breakpoint #48 (Gbps)"
DTC_Q_BREAKPOINT_49_GBPS: Final[str] = "DTC Q breakpoint #49 (Gbps)"
DTC_Q_BREAKPOINT_5_GBPS: Final[str] = "DTC Q breakpoint #5 (Gbps)"
DTC_Q_BREAKPOINT_50_GBPS: Final[str] = "DTC Q breakpoint #50 (Gbps)"
DTC_Q_BREAKPOINT_51_GBPS: Final[str] = "DTC Q breakpoint #51 (Gbps)"
DTC_Q_BREAKPOINT_52_GBPS: Final[str] = "DTC Q breakpoint #52 (Gbps)"
DTC_Q_BREAKPOINT_53_GBPS: Final[str] = "DTC Q breakpoint #53 (Gbps)"
DTC_Q_BREAKPOINT_54_GBPS: Final[str] = "DTC Q breakpoint #54 (Gbps)"
DTC_Q_BREAKPOINT_55_GBPS: Final[str] = "DTC Q breakpoint #55 (Gbps)"
DTC_Q_BREAKPOINT_56_GBPS: Final[str] = "DTC Q breakpoint #56 (Gbps)"
DTC_Q_BREAKPOINT_57_GBPS: Final[str] = "DTC Q breakpoint #57 (Gbps)"
DTC_Q_BREAKPOINT_58_GBPS: Final[str] = "DTC Q breakpoint #58 (Gbps)"
DTC_Q_BREAKPOINT_59_GBPS: Final[str] = "DTC Q breakpoint #59 (Gbps)"
DTC_Q_BREAKPOINT_6_GBPS: Final[str] = "DTC Q breakpoint #6 (Gbps)"
DTC_Q_BREAKPOINT_60_GBPS: Final[str] = "DTC Q breakpoint #60 (Gbps)"
DTC_Q_BREAKPOINT_61_GBPS: Final[str] = "DTC Q breakpoint #61 (Gbps)"
DTC_Q_BREAKPOINT_7_GBPS: Final[str] = "DTC Q breakpoint #7 (Gbps)"
DTC_Q_BREAKPOINT_8_GBPS: Final[str] = "DTC Q breakpoint #8 (Gbps)"
DTC_Q_BREAKPOINT_9_GBPS: Final[str] = "DTC Q breakpoint #9 (Gbps)"
DTC_TAM_UPLIFT_MULTIPLIER_STARLINK_MOBILE_DERIVED_YEAR_ROW: Final[str] = "DTC TAM uplift multiplier (Starlink Mobile, derived year-row)"
DTC_TAM_UPLIFT_RAMP_END_YRS_FROM_2025: Final[str] = "DTC TAM uplift ramp-end (yrs from 2025)"
DTC_TAM_UPLIFT_TARGET_STARLINK_MOBILE_PREMIUM: Final[str] = "DTC TAM uplift target: Starlink Mobile premium (×)"
DTC_ACTIVE_GBPS_V2_V3_COMBINED: Final[str] = "DTC active Gbps (V2+V3 combined)"
DTC_AVG_SUBSCRIBERS_IMPLIED_M: Final[str] = "DTC avg subscribers (implied, M)"
DTC_DEMAND_CURVE_LEVEL_MULTIPLIER: Final[str] = "DTC demand curve level multiplier"
DTC_POOL_AT_COST_GBPS_YR: Final[str] = "DTC pool at-cost $/Gbps/yr"
DEMAND_CURVES_STARLINK_BB_DTC_PIECEWISE_LINEAR_LOOKUP: Final[str] = "Demand Curves: Starlink BB + DTC piecewise-linear lookup"
DEMAND_CURVE_ESCALATOR_START_RATE_ANNUAL: Final[str] = "Demand curve escalator: start rate (annual)"
DEMAND_CURVE_ESCALATOR_TAPER_END_YRS_FROM_2025: Final[str] = "Demand curve escalator: taper end (yrs from 2025)"
DEMAND_CURVE_ESCALATOR_TERMINAL_RATE_ANNUAL: Final[str] = "Demand curve escalator: terminal rate (annual)"
DEMAND_BUILDABLE_CAPEX_MM: Final[str] = "Demand-buildable CapEx ($mm)"
DEMAND_SATURATION_DEPLOYMENT_HEADROOM_SATS: Final[str] = "Demand-saturation deployment headroom (sats)"
DEMAND_VS_SUPPLY_CHECK_NOT_A_CAP: Final[str] = "Demand-vs-supply CHECK (not a cap)"
DEPLOYABLE_AREA_PENALTY_KG_M: Final[str] = "Deployable area penalty (kg/m²)"
DEPLOYMENT_CAP_MIN_DEMAND_LAUNCH_PACING_SATS: Final[str] = "Deployment cap: MIN(demand, launch, pacing) (sats)"
DESIRED_BB_SATS_PRE_CAP: Final[str] = "Desired BB sats (pre-cap)"
DESIRED_DTC_SATS_PRE_CAP: Final[str] = "Desired DTC sats (pre-cap)"
DESIRED_STARSHIP_LAUNCHES_CURRENT_YR: Final[str] = "Desired Starship launches (current yr)"
DESIRED_CASH_ODC_MM: Final[str] = "Desired cash → ODC ($mm)"
DESIRED_CASH_TERRESTRIAL_MM: Final[str] = "Desired cash → Terrestrial ($mm)"
DESIRED_CASH_AI_COMPUTE_MM: Final[str] = "Desired cash: AI-Compute ($mm)"
DESIRED_CASH_CUSTOMER_LAUNCH_MM: Final[str] = "Desired cash: Customer Launch ($mm)"
DESIRED_CASH_STARLINK_MM: Final[str] = "Desired cash: Starlink ($mm)"
DESIRED_LAUNCH_KG_AI_COMPUTE: Final[str] = "Desired launch kg: AI-Compute"
DESIRED_LAUNCH_KG_CUSTOMER_LAUNCH: Final[str] = "Desired launch kg: Customer Launch"
DESIRED_LAUNCH_KG_STARLINK: Final[str] = "Desired launch kg: Starlink"
DEVELOPER_API_ARPU_ACCT_YR: Final[str] = "Developer/API: ARPU ($/acct/yr)"
DEVELOPER_API_REVENUE_MM: Final[str] = "Developer/API: revenue ($mm)"
DEVELOPER_API_TOKENS_T: Final[str] = "Developer/API: tokens (T)"
DEVELOPER_API_TOKENS_USER_M_YR: Final[str] = "Developer/API: tokens/user (M/yr)"
DEVELOPER_API_USERS_M: Final[str] = "Developer/API: users (M)"
EBIT_MM: Final[str] = "EBIT ($mm)"
EBIT_CONSISTENCY: Final[str] = "EBIT consistency"
EBIT_AI_COMPUTE: Final[str] = "EBIT: AI - Compute"
EBIT_CORPORATE: Final[str] = "EBIT: Corporate"
EBIT_CUSTOMER_LAUNCH: Final[str] = "EBIT: Customer Launch"
EBIT_LUNAR_MARS: Final[str] = "EBIT: Lunar - Mars"
EBIT_STARLINK: Final[str] = "EBIT: Starlink"
EBITDA_MARGIN_MEMO: Final[str] = "EBITDA Margin % (memo)"
EBITDA_FOOT: Final[str] = "EBITDA foot"
EBITDA_AI_COMPUTE: Final[str] = "EBITDA: AI - Compute"
EBITDA_CORPORATE: Final[str] = "EBITDA: Corporate"
EBITDA_CUSTOMER_LAUNCH: Final[str] = "EBITDA: Customer Launch"
EBITDA_LUNAR_MARS: Final[str] = "EBITDA: Lunar - Mars"
EBITDA_STARLINK: Final[str] = "EBITDA: Starlink"
EFFECTIVE_COMPUTE_RATIO_RATIO: Final[str] = "Effective Compute Ratio (ratio)"
EFFECTIVE_DTC_GBPS_PER_SAT_REVENUE_CALIBRATION: Final[str] = "Effective DTC Gbps per sat (revenue calibration)"
EFFECTIVE_COMPUTE_H100_EQ_VINTAGE_LOCKED: Final[str] = "Effective compute (H100-eq, vintage-locked)"
ELIMINATION_CONSERVATION_RULE_21: Final[str] = "Elimination conservation (Rule 21)"
ENGINE_FACILITY_BASE_CAPACITY_2025_ENGINES_YR: Final[str] = "Engine facility base capacity 2025 (engines/yr)"
ENGINE_FACILITY_CAPACITY_ENGINES_YR_PER_INCREMENT: Final[str] = "Engine facility capacity (engines/yr per increment)"
ENGINE_FACILITY_COST_PER_CAPACITY_INCREMENT_MM: Final[str] = "Engine facility cost per capacity increment ($mm)"
ENGINE_FACILITY_USEFUL_LIFE_YEARS: Final[str] = "Engine facility useful life (years)"
ENGINES_DEMANDED_THIS_YEAR_SHIPS_ENGINES_VEHICLE: Final[str] = "Engines demanded this year (= ships × engines/vehicle)"
ENTERPRISE_ARPU_SEAT_YR: Final[str] = "Enterprise: ARPU ($/seat/yr)"
ENTERPRISE_REVENUE_MM: Final[str] = "Enterprise: revenue ($mm)"
ENTERPRISE_SEATS_M: Final[str] = "Enterprise: seats (M)"
ENTERPRISE_TOKENS_T: Final[str] = "Enterprise: tokens (T)"
ENTERPRISE_TOKENS_USER_M_YR: Final[str] = "Enterprise: tokens/user (M/yr)"
ENVIRONMENTAL_HEAT_LOAD_Q_ENV_W_M: Final[str] = "Environmental heat load q_env (W/m²)"
EXPLICIT_PV_TIE_SUBTOTAL_VS_MODULES_0: Final[str] = "Explicit-PV tie (subtotal vs Σ modules) = 0"
EXTERNAL_COMMERCIAL_LAUNCH_DEMAND_COUNT: Final[str] = "External commercial launch demand (count)"
EXTERNAL_COMPUTE_2025_SEED_M_H100_EQ_GPU: Final[str] = "External compute 2025 seed (M H100-eq GPU)"
EXTERNAL_COMPUTE_DEMAND_GPU_HRS_H100_EQ: Final[str] = "External compute demand (GPU-hrs, H100-eq)"
EXTERNAL_GOVERNMENT_LAUNCH_DEMAND_COUNT: Final[str] = "External government launch demand (count)"
EXTERNAL_REVENUE_MM: Final[str] = "External revenue ($mm)"
F9: Final[str] = "F9"
F9_2ND_STAGE_MFG_COST_MM_UNIT: Final[str] = "F9 2nd stage mfg cost ($mm/unit)"
F9_INTERNAL_VS_CUSTOMER_RECONCILIATION_MEMO: Final[str] = "F9 INTERNAL-VS-CUSTOMER RECONCILIATION (memo)"
F9_SPOT_IRR_REPORTING_ONLY_EXCLUDED_FROM_ALLOCATION: Final[str] = "F9 Spot IRR (reporting only, excluded from allocation)"
F9_STARLINK_LAUNCH_CAP_ANNUALIZED_LAUNCHES_YR_DERIVED: Final[str] = "F9 Starlink launch cap, annualized (launches/yr): derived"
F9_STARLINK_LAUNCHES_YTD_IN_PACING_YEAR_ACTUAL: Final[str] = "F9 Starlink launches YTD in pacing year (actual)"
F9_WRIGHT_S_LAW_MFG_LEARNING_RATE: Final[str] = "F9 Wright's Law mfg learning rate"
F9_ANNUAL_CADENCE_PER_BOOSTER_IN_SERVICE: Final[str] = "F9 annual cadence per booster in service"
F9_AT_COST_RATE_PER_LAUNCH_MM: Final[str] = "F9 at-cost rate per launch ($mm)"
F9_AVERAGE_REALIZED_PAYLOAD_PER_LAUNCH_KG: Final[str] = "F9 average realized payload per launch (kg)"
F9_BASE_BOOSTER_BUILD_RATE_BOOSTERS_YEAR_PRE_V3_TRIGGER: Final[str] = "F9 base booster build rate (boosters/year, pre-V3-trigger)"
F9_BOOSTER_1ST_STAGE_MFG_COST_MM_UNIT: Final[str] = "F9 booster (1st stage) mfg cost ($mm/unit)"
F9_BOOSTER_BUILD_COST_MM: Final[str] = "F9 booster build cost ($mm)"
F9_BOOSTER_ECONOMIC_LIFE_YEARS: Final[str] = "F9 booster economic life (years)"
F9_BOOSTER_FLEET_EOY: Final[str] = "F9 booster fleet EoY"
F9_BOOSTER_REFURB_OF_MFG: Final[str] = "F9 booster refurb % of mfg"
F9_BOOSTERS_BUILT_YR: Final[str] = "F9 boosters built (yr)"
F9_BOOSTERS_BUILT_PER_YEAR: Final[str] = "F9 boosters built per year"
F9_BOOSTERS_RETIRED_YR: Final[str] = "F9 boosters retired (yr)"
F9_BOOSTERS_RETIRED_PER_YEAR: Final[str] = "F9 boosters retired per year"
F9_BUILD_RATE_DECAY_WINDOW_YEARS: Final[str] = "F9 build-rate decay window (years)"
F9_CADENCE_AT_COST_RATES_GLIDE_PATH_SEPARATE_FROM_COMMERCIAL_PRICE: Final[str] = "F9 cadence + at-cost rates + glide path (separate from commercial price)"
F9_CADENCE_PER_BOOSTER_FLIGHTS_YEAR: Final[str] = "F9 cadence per booster (flights/year)"
F9_CADENCE_PER_BOOSTER_FLIGHTS_YEAR_FLAT: Final[str] = "F9 cadence per booster (flights/year, flat)"
F9_CADENCE_PER_BOOSTER_FLIGHTS_YR: Final[str] = "F9 cadence per booster (flights/yr)"
F9_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH: Final[str] = "F9 customer launch price ($mm/launch)"
F9_CUSTOMER_LAUNCHES_RESIDUAL: Final[str] = "F9 customer launches (residual)"
F9_CUSTOMER_LAUNCHES_PER_YEAR: Final[str] = "F9 customer launches per year"
F9_FAIRING_COST_NET_OF_75_RECOVERY_MM_FLIGHT: Final[str] = "F9 fairing cost net of 75% recovery ($mm/flight)"
F9_FLEET_BOY_BOOSTERS: Final[str] = "F9 fleet BoY (boosters)"
F9_FLEET_EOY_BOOSTERS: Final[str] = "F9 fleet EoY (boosters)"
F9_INTERNAL_LAUNCHES_PER_YEAR_STARLINK_DRIVEN: Final[str] = "F9 internal launches per year (Starlink-driven)"
F9_LAUNCH_CAPACITY_LAUNCHES_YR: Final[str] = "F9 launch capacity (launches/yr)"
F9_LAUNCHES_V2_STARLINK_FINAL_YEAR: Final[str] = "F9 launches V2-Starlink final year"
F9_LAUNCHES_GLIDE_PATH_PER_YEAR: Final[str] = "F9 launches glide path (per year)"
F9_LAUNCHES_PER_YEAR: Final[str] = "F9 launches per year"
F9_LIFETIME_REUSES_PER_BOOSTER: Final[str] = "F9 lifetime reuses per booster"
F9_OWNED_VEHICLE_D_A_MM: Final[str] = "F9 owned-vehicle D&A ($mm)"
F9_OWNED_VEHICLE_D_A_PER_LAUNCH_MM_INTERFACE_TO_STARLINK: Final[str] = "F9 owned-vehicle D&A per launch ($mm)            ◄ interface to Starlink"
F9_OWNED_VEHICLE_BUILD_CAPEX: Final[str] = "F9 owned-vehicle build CapEx"
F9_OWNED_VEHICLE_BUILD_CAPEX_MM_ALLOCATOR_OUT: Final[str] = "F9 owned-vehicle build CapEx ($mm)   ◄ Allocator OUT"
F9_PAYLOAD_PER_LAUNCH_KG: Final[str] = "F9 payload per launch (kg)"
F9_PAYLOAD_TO_LEO_KG: Final[str] = "F9 payload to LEO (kg)"
F9_PER_LAUNCH_OPS_COST_MM: Final[str] = "F9 per-launch ops cost ($mm)"
F9_SATS_PER_LAUNCH_V2_PACKING: Final[str] = "F9 sats per launch (V2 packing)"
F9_STARTING_FLEET_AT_2025_SOY_BOOSTERS: Final[str] = "F9 starting fleet at 2025 SoY (boosters)"
F9_TOTAL_LAUNCH_CAPACITY_LAUNCHES_YR: Final[str] = "F9 total launch capacity (launches/yr)"
F9_VARIABLE_COST_PER_LAUNCH_MM_LAUNCH: Final[str] = "F9 variable cost per launch ($mm/launch)"
F9_VEHICLE_LIFE_L_YEARS: Final[str] = "F9 vehicle life L (years)"
F9_CAPEX_SLUG_PER_VEHICLE_MM: Final[str] = "F9: CapEx slug per vehicle ($mm)"
F9_MARGIN_PER_VEHICLE_PER_YR_MM_EX_D_A: Final[str] = "F9: margin per vehicle per yr ($mm, ex-D&A)"
F9_REVENUE_PER_VEHICLE_PER_YR_MM: Final[str] = "F9: revenue per vehicle per yr ($mm)"
FCF_MM: Final[str] = "FCF ($mm)"
FCF_FOOT_VS_NOPAT_D_A_CAPEX_WALK: Final[str] = "FCF foot vs NOPAT+D&A−CapEx walk"
FCF_IDENTITY_EBIT_D_A_CAPEX_FCF_0: Final[str] = "FCF identity: (EBIT + D&A − CapEx) − FCF (=0)"
FCF_REPAYMENT_SWEEP_OF_EXCESS_FCF: Final[str] = "FCF repayment sweep (% of excess FCF)"
FCF_AI_COMPUTE: Final[str] = "FCF: AI - Compute"
FCF_CORPORATE_COST_CENTRE: Final[str] = "FCF: Corporate (cost centre)"
FCF_CUSTOMER_LAUNCH: Final[str] = "FCF: Customer Launch"
FCF_CUSTOMER_LAUNCH_EX_STARSHIP_R_D_LIFTED_TO_CORPORATE: Final[str] = "FCF: Customer Launch (ex-Starship R&D; lifted to corporate)"
FCF_GROUP_DCF_SUBTOTAL_SL_CL_AI_CORP_EXCL_L_M: Final[str] = "FCF: Group DCF subtotal (SL+CL+AI+Corp; excl L/M)"
FCF_LUNAR_MARS: Final[str] = "FCF: Lunar - Mars"
FCF_STARLINK: Final[str] = "FCF: Starlink"
FCF_LESS_CORPORATE: Final[str] = "FCF: less corporate"
FCF_LESS_CORPORATE_SG_A_SHARED_R_D_SPECTRUM_TAXES_CORP_CAPEX: Final[str] = "FCF: less corporate (SG&A+shared R&D+spectrum+taxes+corp CapEx)"
FLEET_PRODUCTION_STANDING_FLEET_RECONCILIATION: Final[str] = "FLEET PRODUCTION ↔ STANDING-FLEET RECONCILIATION"
FLEET_WRIGHT_S_COST_CURVES_CONFIG_LINES: Final[str] = "FLEET WRIGHT'S COST CURVES + CONFIG LINES"
F_REF_REFERENCE_COMPUTE_UNIT_TFLOPS_H100_FP8: Final[str] = "F_ref: reference compute unit (TFLOPS, H100 FP8)"
FAB_SLUG_COST_ONLINE_YEAR_MM: Final[str] = "Fab slug cost (online-year, $mm)"
FACILITIES_BUILD_CAPACITY_STEP_FACILITY_CAPEX_ENGINE: Final[str] = "Facilities Build: capacity-step facility CapEx engine"
FACILITY_GROUND_CAPEX_MM: Final[str] = "Facility / ground CapEx ($mm)"
FACILITY_GROUND_D_A_MM: Final[str] = "Facility / ground D&A ($mm)"
FACILITY_BALANCE_EOY_MM: Final[str] = "Facility balance EoY ($mm)"
FACILITY_DRAW_MM: Final[str] = "Facility draw ($mm)"
FACILITY_INTEREST_MM: Final[str] = "Facility interest ($mm)"
FACILITY_REPAYMENT_MM: Final[str] = "Facility repayment ($mm)"
FINAL_BB_SATS: Final[str] = "Final BB sats"
FINAL_DTC_SATS: Final[str] = "Final DTC sats"
FIRST_MISSION_YEAR_LUNAR_MARS: Final[str] = "First mission year (Lunar Mars)"
FLAG_REV_MODULE_SOTP_0_AS_OF2026_EBITDA_CNT_EXPECT_0: Final[str] = "Flag: rev-module SoTP<0, as-of2026 EBITDA (cnt, expect 0)"
FLAG_REV_MODULE_SOTP_0_AS_OF2026_EXIT_CNT_EXPECT_0: Final[str] = "Flag: rev-module SoTP<0, as-of2026 Exit (cnt, expect 0)"
FLAG_REV_MODULE_SOTP_0_AS_OF2026_GORDON_CNT_EXPECT_0: Final[str] = "Flag: rev-module SoTP<0, as-of2026 Gordon (cnt, expect 0)"
FLEET_ENERGY_GWH_YR: Final[str] = "Fleet energy (GWh/yr)"
FLEET_GROSS_COMPUTE_REVENUE_MM: Final[str] = "Fleet gross compute revenue ($mm)"
FREE_ARPU_USER_YR: Final[str] = "Free: ARPU ($/user/yr)"
FREE_REVENUE_MM: Final[str] = "Free: revenue ($mm)"
FREE_TOKENS_T: Final[str] = "Free: tokens (T)"
FREE_TOKENS_USER_M_YR: Final[str] = "Free: tokens/user (M/yr)"
FREE_USERS_M: Final[str] = "Free: users (M)"
FULLY_ALLOCATED_COST_MM: Final[str] = "Fully-allocated cost ($mm)"
GLOBAL: Final[str] = "GLOBAL"
GPU_EFFECTIVE_CAPACITY_DEGRADATION_PER_YR: Final[str] = "GPU effective-capacity degradation (per yr)"
GPU_FLEET_EOY_15Y_COHORT: Final[str] = "GPU fleet (EoY, 15y cohort)"
GPU_RETIREMENTS_15Y_COHORT: Final[str] = "GPU retirements (15y cohort)"
GPU_HR_PRICE_GPU_HR: Final[str] = "GPU-hr price ($/GPU-hr)"
GPU_HR_PRICE_GPU_HR_BASE_PRE_DAMPENER: Final[str] = "GPU-hr price ($/GPU-hr): base (pre-dampener)"
GPU_HR_PRICE_CAGR: Final[str] = "GPU-hr price CAGR"
GPU_HRS_REQUIRED_H100_EQ: Final[str] = "GPU-hrs required (H100-eq)"
GPUS_ADDED_COUNT: Final[str] = "GPUs added (count)"
GROUP_EV_EBITDA_MULT_B: Final[str] = "GROUP EV: EBITDA-mult ($B)"
GROUP_EV_EBITDA_MULT_MM: Final[str] = "GROUP EV: EBITDA-mult ($mm)"
GROUP_EV_EXIT_MULT_B: Final[str] = "GROUP EV: Exit-mult ($B)"
GROUP_EV_EXIT_MULT_MM: Final[str] = "GROUP EV: Exit-mult ($mm)"
GROUP_EV_GORDON_B: Final[str] = "GROUP EV: Gordon ($B)"
GROUP_EV_GORDON_MM: Final[str] = "GROUP EV: Gordon ($mm)"
GROUP_P_L_SEGMENT_CONSOLIDATION: Final[str] = "GROUP P&L: segment consolidation"
GBPS_DEMAND: Final[str] = "Gbps demand"
GBPS_PER_GWH_YR: Final[str] = "Gbps per GWh/yr"
GENERAL_ADMINISTRATIVE_CAGR_TAPER: Final[str] = "General & Administrative: CAGR (taper)"
GENERAL_ADMINISTRATIVE_END_STATE_FLOOR: Final[str] = "General & Administrative: end-state % (floor)"
GENERAL_ADMINISTRATIVE_START_OF_GROUP_REV: Final[str] = "General & Administrative: start % of group rev"
GIGABAY_BASE_CAPACITY_2025_SHIPS_YR: Final[str] = "Gigabay base capacity 2025 (ships/yr)"
GIGABAY_INSTALLED_STARSHIP_BUILD_CAPACITY_SHIPS_YR_ASSUMPTIONS: Final[str] = "Gigabay installed Starship build capacity (ships/yr)  ◄ Assumptions"
GOVERNMENT_LAUNCH_MARKET_SIZE_MM_YEAR_YEAR_ROW: Final[str] = "Government launch market size ($mm/year): year-row"
GOVERNMENT_LAUNCH_MARKET_SIZE_MM_YR: Final[str] = "Government launch market size ($mm/yr)"
GRAND_TOTAL: Final[str] = "Grand total"
GROSS_PROFIT: Final[str] = "Gross Profit"
GROSS_PROFIT_MM: Final[str] = "Gross Profit ($mm)"
GROSS_PROFIT_MM_ALLOCATOR_OUT: Final[str] = "Gross Profit ($mm)   ◄ Allocator OUT"
GROSS_PROFIT_AI_COMPUTE: Final[str] = "Gross Profit: AI - Compute"
GROSS_PROFIT_CUSTOMER_LAUNCH: Final[str] = "Gross Profit: Customer Launch"
GROSS_PROFIT_LUNAR_MARS: Final[str] = "Gross Profit: Lunar - Mars"
GROSS_PROFIT_STARLINK: Final[str] = "Gross Profit: Starlink"
GROSS_COMPUTE_REVENUE_MM: Final[str] = "Gross compute revenue ($mm)"
GROUND_NETWORK: Final[str] = "Ground / network"
GROUND_STATION_CAPEX_THIS_YEAR_MM: Final[str] = "Ground station CapEx this year ($mm)"
GROUND_STATION_BUILD_CAPEX_PER_STATION_MM: Final[str] = "Ground station build CapEx per station ($mm)"
GROUND_STATION_USEFUL_LIFE_YEARS: Final[str] = "Ground station useful life (years)"
GROUND_STATIONS_BUILT_PER_YEAR_PLACEHOLDER_FLAT: Final[str] = "Ground stations built per year (placeholder, flat)"
GROUND_STATIONS_BUILT_THIS_YEAR: Final[str] = "Ground stations built this year"
GROUND_NETWORK_OPS_COGS_MM: Final[str] = "Ground-network ops COGS ($mm)"
GROUND_NETWORK_OPS_COGS_OF_REVENUE: Final[str] = "Ground-network ops COGS (% of revenue)"
GROUND_FACILITY_CAPEX: Final[str] = "Ground/facility CapEx"
GROUND_FACILITY_CAPEX_MM_ALLOCATOR_OUT: Final[str] = "Ground/facility CapEx ($mm)   ◄ Allocator OUT"
GROUND_NETWORK_COST_MM: Final[str] = "Ground/network cost ($mm)"
GROUND_NETWORK_OPEX_PCT_REV: Final[str] = "Ground/network opex pct rev"
GROUP_COGS_MM: Final[str] = "Group COGS ($mm)"
GROUP_CAPEX_ACCRUAL_MM: Final[str] = "Group CapEx: accrual ($mm)"
GROUP_D_A_MM: Final[str] = "Group D&A ($mm)"
GROUP_EBIT_MM: Final[str] = "Group EBIT ($mm)"
GROUP_EBITDA_MM: Final[str] = "Group EBITDA ($mm)"
GROUP_EV_ANCHOR_BRANT_INTERNAL: Final[str] = "Group EV anchor: Brant (internal)"
GROUP_EV_ANCHOR_MORGAN_STANLEY_PUBLIC: Final[str] = "Group EV anchor: Morgan Stanley (public)"
GROUP_EV_EBITDA_MULTIPLE: Final[str] = "Group EV: EBITDA-multiple"
GROUP_EV_EXIT_MULTIPLE: Final[str] = "Group EV: Exit-multiple"
GROUP_EV_EXIT_MULTIPLE_REVENUE: Final[str] = "Group EV: Exit-multiple (revenue)"
GROUP_EV_GORDON: Final[str] = "Group EV: Gordon"
GROUP_EV_GORDON_PERPETUITY_GROWTH: Final[str] = "Group EV: Gordon (perpetuity-growth)"
GROUP_FCF_MM: Final[str] = "Group FCF ($mm)"
GROUP_FCF_ACCRUAL_WALK_MM: Final[str] = "Group FCF: accrual walk ($mm)"
GROUP_FCF_NORMALIZED_WALK_NOPAT_D_A_CAPEX_MM: Final[str] = "Group FCF: normalized walk (NOPAT+D&A−CapEx) ($mm)"
GROUP_GROSS_PROFIT_MM: Final[str] = "Group Gross Profit ($mm)"
GROUP_REVENUE_MM: Final[str] = "Group Revenue ($mm)"
GROUP_REVENUE_TOTAL: Final[str] = "Group Revenue — total"
GROUP_TAXES_MM: Final[str] = "Group Taxes ($mm)"
GROUP_WACC: Final[str] = "Group WACC"
GROUP_REVENUE_BASE_MM_PLACEHOLDER_STARLINK_REV_SWAP_TO_GROUP_TOTAL_IN_4_5: Final[str] = "Group revenue base ($mm): placeholder (Starlink rev; swap to Group total in 4.5)"
HQ_FACILITY_CAPEX_MM_GROUP_P_L: Final[str] = "HQ facility CapEx ($mm)  ◄ Group P&L"
HQ_FACILITY_CAPEX_OF_REVENUE: Final[str] = "HQ facility CapEx (% of revenue)"
HQ_FACILITY_D_A_MM_GROUP_P_L: Final[str] = "HQ facility D&A ($mm)  ◄ Group P&L"
HQ_FACILITY_USEFUL_LIFE_YEARS: Final[str] = "HQ facility useful life (years)"
HARDWARE_KIT_COGS_MM: Final[str] = "Hardware / kit COGS ($mm)"
HARDWARE_KIT_REVENUE_MM: Final[str] = "Hardware / kit revenue ($mm)"
HARDWARE_REPLACEMENT_COST_FACTOR_KG_LANDED_DECLINING: Final[str] = "Hardware replacement cost factor ($/kg landed): declining"
HARDWARE_VALUE_ADD_KG_LANDED: Final[str] = "Hardware value-add ($/kg landed)"
HEADROOM_AI_COMPUTE_MM: Final[str] = "Headroom: AI-Compute ($mm)"
HEADROOM_CUSTOMER_LAUNCH_MM: Final[str] = "Headroom: Customer Launch ($mm)"
HEADROOM_STARLINK_MM: Final[str] = "Headroom: Starlink ($mm)"
HEAT_TRANSPORT_KG_KW_GLIDE_A8_7: Final[str] = "Heat transport (kg/kW, glide): A8.7"
HEAT_TRANSPORT_ANCHOR_2025_KG_KW: Final[str] = "Heat transport anchor 2025 (kg/kW)"
HEAT_TRANSPORT_MATURE_KG_KW: Final[str] = "Heat transport mature (kg/kW)"
HELPER_L_M_BV_MULT_2040_UNDISCOUNTED_MM: Final[str] = "Helper: L/M BV×mult @2040 (undiscounted) $mm"
HELPER_NORMTERMFCF_SL_CL_AI_CORP_MM: Final[str] = "Helper: Σ NormTermFCF (SL+CL+AI+Corp) $mm"
HIGHER_RANK_CAPS_AHEAD_OF_AI_COMPUTE_MM: Final[str] = "Higher-rank caps ahead of AI-Compute ($mm)"
HIGHER_RANK_CAPS_AHEAD_OF_CUSTOMER_LAUNCH_MM: Final[str] = "Higher-rank caps ahead of Customer Launch ($mm)"
HIGHER_RANK_CAPS_AHEAD_OF_STARLINK_MM: Final[str] = "Higher-rank caps ahead of Starlink ($mm)"
HOURS_PER_YEAR_AI_COMPUTE_UTILIZATION: Final[str] = "Hours per year (AI/Compute utilization)"
IPO_INJECTION_MM: Final[str] = "IPO injection ($mm)"
IPO_INJECTION_AMOUNT_MM: Final[str] = "IPO injection amount ($mm)"
IPO_INJECTION_YEAR: Final[str] = "IPO injection year"
INDIVIDUAL_PAID_ARPU_USER_YR: Final[str] = "Individual paid: ARPU ($/user/yr)"
INDIVIDUAL_PAID_REVENUE_MM: Final[str] = "Individual paid: revenue ($mm)"
INDIVIDUAL_PAID_TOKENS_T: Final[str] = "Individual paid: tokens (T)"
INDIVIDUAL_PAID_TOKENS_USER_M_YR: Final[str] = "Individual paid: tokens/user (M/yr)"
INDIVIDUAL_PAID_USERS_M: Final[str] = "Individual paid: users (M)"
INFRASTRUCTURE_USEFUL_LIFE_YEARS: Final[str] = "Infrastructure useful life (years)"
INSTALLED_STARSHIP_BUILD_CAPACITY_SHIPS_YR_RATE_LIMITED_RAMP: Final[str] = "Installed Starship build capacity (ships/yr): rate-limited ramp"
INSTALLED_ENGINE_FACILITY_CAPACITY_ENGINES_YR_EOY_RATCHET_CURRENT_DEMAND_MEMO: Final[str] = "Installed engine-facility capacity (engines/yr): EoY ratchet, ≥ current demand, memo"
INSTALLED_FAB_CAPACITY_WSPM_EOY_RATCHET_PHASE_STEP: Final[str] = "Installed fab capacity (wspm): EoY ratchet / phase step"
INSTALLED_LAUNCH_PADS_STARSHIP_CUMULATIVE_BASE_MEMO: Final[str] = "Installed launch pads (Starship): cumulative, ≥ base, memo"
INSTALLED_SAT_FACTORY_CAPACITY_SATS_YR_EOY_RATCHET_CURRENT_BUILD: Final[str] = "Installed sat-factory capacity (sats/yr): EoY ratchet, ≥ current build"
INSTALLED_TERMINAL_FACTORY_CAPACITY_KITS_YR_CUMULATIVE_MEMO: Final[str] = "Installed terminal-factory capacity (kits/yr): cumulative, memo"
INTEGRATION_TEST_SAT: Final[str] = "Integration & Test $/sat"
INTERNAL_BANDWIDTH_ELIMINATED_ODC_STARLINK: Final[str] = "Internal bandwidth eliminated, ODC→Starlink"
INTERNAL_COMPUTE_ELIMINATED_ODC_AI: Final[str] = "Internal compute eliminated, ODC→AI"
INTERNAL_COMPUTE_SHARE: Final[str] = "Internal compute share"
INTERNAL_LAUNCH_SERVICES_RETIRED_BY_4_5_INVERSION: Final[str] = "Internal launch services: RETIRED by 4.5 inversion"
INTERNAL_SHARE: Final[str] = "Internal share"
INTERNAL_TRANSFER_REVENUE_MM: Final[str] = "Internal transfer revenue ($mm)"
KG_DEMAND_YEAR_N_KG: Final[str] = "Kg demand year N (kg)"
KG_DEMAND_YEAR_N_1: Final[str] = "Kg demand year N+1"
KG_DEMAND_YEAR_N_1_OFF_THE_TOP_RESERVATION: Final[str] = "Kg demand year N+1 (off-the-top reservation)"
LAUNCHES_PER_YEAR_F9_GLIDE_PATH_STARSHIP_DEMAND_PULLED: Final[str] = "LAUNCHES PER YEAR (F9 glide path + Starship demand-pulled)"
LM_KG_RESERVED_OFF_TOP_KG: Final[str] = "LM kg reserved off-top (kg)"
LR_SUBSYSTEMS_LEARNING_RATE_PER_DOUBLING: Final[str] = "LR subsystems (learning rate, per doubling)"
LUNAR_MARS_STRATEGIC_CARVE_OUT_NOT_IN_THE_IRR_QUEUE: Final[str] = "LUNAR / MARS (strategic carve-out: not in the IRR queue)"
LUNAR_ACTIVE_LABOUR_FLEET_EOY_RUNNING_SUM_NET_RETIRE: Final[str] = "LUNAR active labour fleet EoY (running sum, net retire)"
LUNAR_ANNUAL_BV_CONTRIBUTION_MM_YR: Final[str] = "LUNAR annual BV contribution ($mm/yr)"
LUNAR_ANNUAL_HARDWARE_VALUE_ADD_MM_YR: Final[str] = "LUNAR annual hardware value-add ($mm/yr)"
LUNAR_ANNUAL_PRODUCTION_OUTPUT_MM_YR: Final[str] = "LUNAR annual production output ($mm/yr)"
LUNAR_ECONOMIC_OUTPUT_PROXY_MM_MEMO_ONLY_NOT_USED_IN_VALUATION: Final[str] = "LUNAR economic-output proxy ($mm): MEMO ONLY, NOT used in valuation"
LUNAR_LABOUR_UNITS_RETIRED_THIS_YEAR_COHORT_LOOKBACK: Final[str] = "LUNAR labour units retired this year (cohort lookback)"
LABOUR_ANNUAL_OUTPUT_PER_UNIT_THIS_YEAR_MM_YR: Final[str] = "Labour annual output per unit this year ($mm/yr)"
LABOUR_ANNUAL_OUTPUT_PER_UNIT_BASE_YEAR_MM_YR: Final[str] = "Labour annual output per unit, base year ($mm/yr)"
LABOUR_UNIT_BASE_HOURLY_OUTPUT_HR: Final[str] = "Labour unit base hourly output ($/hr)"
LABOUR_UNIT_BASE_HOURLY_OUTPUT_HR_BURDENED_22_0_7: Final[str] = "Labour unit base hourly output ($/hr; burdened $22/0.7)"
LABOUR_UNIT_COST_UNIT: Final[str] = "Labour unit cost ($/unit)"
LABOUR_UNIT_COST_UNIT_DECLINING_CURVE: Final[str] = "Labour unit cost ($/unit): declining curve"
LABOUR_UNIT_DAILY_WORKING_HOURS: Final[str] = "Labour unit daily working hours"
LABOUR_UNIT_MASS_KG: Final[str] = "Labour unit mass (kg)"
LABOUR_UNIT_OPERATIONAL_LIFESPAN_ON_SURFACE_YEARS: Final[str] = "Labour unit operational lifespan on surface (years)"
LABOUR_UNIT_PRODUCTIVITY_FACTOR: Final[str] = "Labour unit productivity factor"
LABOUR_UNIT_PRODUCTIVITY_FACTOR_VS_HUMAN_BASELINE: Final[str] = "Labour unit productivity factor vs human baseline"
LABOUR_UNIT_PRODUCTIVITY_LEARNING_RATE_YR: Final[str] = "Labour unit productivity learning rate (%/yr)"
LABOUR_UNIT_USEFUL_LIFE_YRS: Final[str] = "Labour unit useful life (yrs)"
LAUNCH_DEVELOPMENT_REVENUE_MM: Final[str] = "Launch & Development revenue ($mm)"
LAUNCH_DEVELOPMENT_REVENUE_MM_YR: Final[str] = "Launch & Development revenue ($mm/yr)"
LAUNCH_DEVELOPMENT_REVENUE_MM_YR_YEAR_ROW: Final[str] = "Launch & Development revenue ($mm/yr): year-row"
LAUNCH_FACILITY_D_A_MM: Final[str] = "Launch / facility D&A ($mm)"
LAUNCH_VEHICLE_FACILITY_CAPEX_MM: Final[str] = "Launch / vehicle facility CapEx ($mm)"
LAUNCH_VEHICLE_FACILITY_D_A_MM: Final[str] = "Launch / vehicle facility D&A ($mm)"
LAUNCH_DASHBOARD_ACTUAL_LAUNCHES_FLOWN_BY_MODULE_PER_YEAR: Final[str] = "Launch Dashboard — actual launches flown, by module, per year"
LAUNCH_IRR_SLUG_WORKING_CAPITAL_OF_BUILD: Final[str] = "Launch IRR slug working-capital % of build"
LAUNCH_SERVICES_REVENUE_MM: Final[str] = "Launch Services revenue ($mm)"
LAUNCH_CAPACITY_ALLOTMENT_AI_COMPUTE_KG: Final[str] = "Launch capacity allotment: AI-Compute (kg)"
LAUNCH_CAPACITY_ALLOTMENT_CUSTOMER_LAUNCH_KG: Final[str] = "Launch capacity allotment: Customer Launch (kg)"
LAUNCH_CAPACITY_ALLOTMENT_STARLINK_KG: Final[str] = "Launch capacity allotment: Starlink (kg)"
LAUNCH_COST_MM_LAUNCH: Final[str] = "Launch cost ($mm/launch)"
LAUNCH_COST_PER_SAT_MM: Final[str] = "Launch cost per sat ($mm)"
LAUNCH_DEMAND_ELASTICITY_MULTIPLIER_CAP_X: Final[str] = "Launch demand elasticity multiplier cap (x)"
LAUNCH_DEMAND_PRICE_ELASTICITY_E_EXTRA_ON_KG: Final[str] = "Launch demand price elasticity e (extra, on $/kg)"
LAUNCH_FACILITY_SHARE_FRAC: Final[str] = "Launch facility share (frac)"
LAUNCH_INSURANCE_OF_EXTERNAL_REV: Final[str] = "Launch insurance % of external rev"
LAUNCH_INSURANCE_MM: Final[str] = "Launch insurance ($mm)"
LAUNCH_OTHER_COGS_OF_EXTERNAL_REV: Final[str] = "Launch other COGS % of external rev"
LAUNCH_PAD_BUILD_UPGRADE_COST_MM_PER_PAD: Final[str] = "Launch pad build/upgrade cost ($mm per pad)"
LAUNCH_PAD_USEFUL_LIFE_YEARS: Final[str] = "Launch pad useful life (years)"
LAUNCH_PADS_BASE_IN_SERVICE_2025_STARSHIP_CAPABLE: Final[str] = "Launch pads base in service 2025 (Starship-capable)"
LAUNCH_PADS_NEEDED_STARSHIP_LAUNCHES_LAUNCHES_PAD: Final[str] = "Launch pads needed (= Starship launches ÷ launches/pad)"
LAUNCH_SERVICES: Final[str] = "Launch services"
LAUNCH_SERVICES_COST_MM: Final[str] = "Launch services cost ($mm)"
LAUNCH_VEHICLE_CALENDAR_LIFE_YEARS: Final[str] = "Launch vehicle calendar life (years)"
LAUNCH_CAPACITY_DEPLOYMENT_CEILING_SATS_SAME_YEAR_DEMAND_VS_START_OF_YEAR_CAPACITY: Final[str] = "Launch-capacity deployment ceiling (sats): same-year demand vs start-of-year capacity"
LAUNCH_INFRA_CAPACITY_INSTALLED_LAUNCHES_YR: Final[str] = "Launch-infra capacity installed (launches/yr)"
LAUNCH_KG_AVAILABLE_TARGET_RETIREMENTS_DRY_MASS_ODC: Final[str] = "Launch-kg available (= (target + retirements) × dry mass): ODC"
LAUNCH_PACING_YEAR_APPLY_CAPS_IN_THIS_YEAR_ONLY: Final[str] = "Launch-pacing year (apply caps in this year only)"
LAUNCH_SITE_INFRA_CAPEX_MM_PER_ANNUAL_LAUNCH_OF_CAPACITY: Final[str] = "Launch-site infra CapEx ($mm per annual launch of capacity)"
LAUNCH_SITE_INFRASTRUCTURE_CAPEX_MM: Final[str] = "Launch-site infrastructure CapEx ($mm)"
LAUNCH_VEHICLE_FACILITY_CAPEX_TOTAL_MM_LAUNCH_VEHICLE: Final[str] = "Launch/vehicle facility CapEx total ($mm)  ◄ launch/vehicle"
LAUNCH_VEHICLE_FACILITY_D_A_TOTAL_MM_LAUNCH_VEHICLE: Final[str] = "Launch/vehicle facility D&A total ($mm)  ◄ launch/vehicle"
LEFTOVER_CASH_MM: Final[str] = "Leftover cash ($mm)"
LEGACY_BB_GBPS: Final[str] = "Legacy BB Gbps"
LEGACY_V1_GBPS_PER_SAT: Final[str] = "Legacy V1 Gbps per sat"
LEGACY_V1_ACTIVE_SATS: Final[str] = "Legacy V1 active sats"
LEGACY_V1_ACTIVE_SATS_END_2025: Final[str] = "Legacy V1 active sats end-2025"
LEGACY_V1_BASE_DEORBIT_END_YEAR: Final[str] = "Legacy V1 base deorbit end year"
LEGACY_V1_BASE_DEORBIT_START_YEAR: Final[str] = "Legacy V1 base deorbit start year"
LEGACY_V1_SAT_MASS_KG: Final[str] = "Legacy V1 sat mass (kg)"
LEGACY_V1_5_GBPS_PER_SAT: Final[str] = "Legacy V1.5 Gbps per sat"
LEGACY_V1_5_ACTIVE_SATS: Final[str] = "Legacy V1.5 active sats"
LEGACY_V1_5_ACTIVE_SATS_END_2025: Final[str] = "Legacy V1.5 active sats end-2025"
LEGACY_V1_5_BASE_DEORBIT_END_YEAR: Final[str] = "Legacy V1.5 base deorbit end year"
LEGACY_V1_5_BASE_DEORBIT_START_YEAR: Final[str] = "Legacy V1.5 base deorbit start year"
LEGACY_V1_5_SAT_MASS_KG: Final[str] = "Legacy V1.5 sat mass (kg)"
LIFETIME_REUSES_PER_BOOSTER_YEAR_CAP: Final[str] = "Lifetime reuses per booster (year cap)"
LOOKUP_FORM_INDEX_MATCH_1_BRACKET_FIND_MANUAL_LINEAR_INTERP_NO_FORECAST_TREND_PER_MEMORY_SNAPSHOT_V3_2_4: Final[str] = "Lookup form: INDEX/MATCH(..., 1) bracket-find + manual linear interp. NO FORECAST / TREND. Per Memory Snapshot v3 §2.4."
LUNAR_PAYLOAD_AS_LABOUR_UNITS: Final[str] = "Lunar % payload as labour units"
LUNAR_MARS: Final[str] = "Lunar - Mars"
LUNAR_MARS_2: Final[str] = "Lunar / Mars"
LUNAR_MARS_BV_MULT: Final[str] = "Lunar / Mars (BV×mult)"
LUNAR_MARS_TERMINAL_BV_MULTIPLIER: Final[str] = "Lunar / Mars: terminal BV multiplier"
LUNAR_MARS_MODULE_D_A_MM: Final[str] = "Lunar Mars Module D&A ($mm)"
LUNAR_CARVE_OUT_CASH_THIS_YEAR_MM: Final[str] = "Lunar carve-out cash this year ($mm)"
LUNAR_FUEL_DEPOT_MULTIPLIER_PER_OUTBOUND_STARSHIP: Final[str] = "Lunar fuel depot multiplier per outbound Starship"
LUNAR_HARDWARE_MASS_LANDED_THIS_YEAR_KG: Final[str] = "Lunar hardware mass landed this year (kg)"
LUNAR_HARDWARE_MASS_PER_SHIP_KG: Final[str] = "Lunar hardware mass per ship (kg)"
LUNAR_LABOUR_MASS_LANDED_THIS_YEAR_KG: Final[str] = "Lunar labour mass landed this year (kg)"
LUNAR_LABOUR_MASS_PER_SHIP_KG: Final[str] = "Lunar labour mass per ship (kg)"
LUNAR_LABOUR_UNITS_LANDED_THIS_YEAR_COUNT: Final[str] = "Lunar labour units landed this year (count)"
LUNAR_LABOUR_UNITS_PER_SHIP_COUNT: Final[str] = "Lunar labour units per ship (count)"
LUNAR_PAYLOAD_PER_SURFACE_LANDED_STARSHIP_KG: Final[str] = "Lunar payload per surface-landed Starship (kg)"
LUNAR_SHARE_OF_MARS_MOON_CARVE_OUT_CASH_YEAR_ROW: Final[str] = "Lunar share of Mars/Moon carve-out cash: year-row"
LUNAR_SHARE_OF_CARVE_OUT_CASH_YEAR_ROW: Final[str] = "Lunar share of carve-out cash (year-row)"
LUNAR_SURFACE_MISSIONS_DEPLOYED_COUNT: Final[str] = "Lunar surface missions deployed (count)"
LUNAR_MARS_NET_BOOK_VALUE_MM: Final[str] = "Lunar+Mars Net Book Value ($mm)"
LUNAR_MARS_NET_BOOK_VALUE_MM_SOTP_TERMINAL_CUMCAPEX_CUM_D_A: Final[str] = "Lunar+Mars Net Book Value ($mm): SoTP terminal (cumCapEx − cum D&A)"
LUNAR_MARS_BV_MULTIPLIER: Final[str] = "Lunar/Mars BV multiplier"
LUNAR_MARS_CARVE_OUT_OF_PRIOR_YEAR_GROUP_FCF: Final[str] = "Lunar/Mars carve-out % of prior-year Group FCF"
LUNAR_MARS_CARVE_OUT_CASH_MM: Final[str] = "Lunar/Mars carve-out cash ($mm)"
LUNAR_MARS_CARVE_OUT_FLOOR_MM_YR: Final[str] = "Lunar/Mars carve-out floor ($mm/yr)"
LUNAR_MARS_CARVE_OUT_PRE_FIRST_MISSION_YEAR_R_D_ONLY_OVERRIDE_MM_YR: Final[str] = "Lunar/Mars carve-out pre-first-mission-year R&D-only override ($mm/yr)"
LUNAR_MARS_CARVE_OUT_USES_PRIOR_YEAR_FCF_0_1: Final[str] = "Lunar/Mars carve-out uses prior-year FCF (0/1)"
MARS_ACTIVE_LABOUR_FLEET_EOY_RUNNING_SUM_NET_RETIRE: Final[str] = "MARS active labour fleet EoY (running sum, net retire)"
MARS_ANNUAL_BV_CONTRIBUTION_MM_YR: Final[str] = "MARS annual BV contribution ($mm/yr)"
MARS_ANNUAL_HARDWARE_VALUE_ADD_MM_YR: Final[str] = "MARS annual hardware value-add ($mm/yr)"
MARS_ANNUAL_PRODUCTION_OUTPUT_MM_YR: Final[str] = "MARS annual production output ($mm/yr)"
MARS_ECONOMIC_OUTPUT_PROXY_MM_MEMO_ONLY_NOT_USED_IN_VALUATION: Final[str] = "MARS economic-output proxy ($mm): MEMO ONLY, NOT used in valuation"
MARS_LABOUR_UNITS_RETIRED_THIS_YEAR_COHORT_LOOKBACK: Final[str] = "MARS labour units retired this year (cohort lookback)"
MW_ADDED: Final[str] = "MW added"
MW_FLEET_EOY_15Y_COHORT: Final[str] = "MW fleet (EoY, 15y cohort)"
MW_RETIREMENTS_15Y_COHORT: Final[str] = "MW retirements (15y cohort)"
MARGIN_PER_MW_PER_YR_MM: Final[str] = "Margin per MW per yr ($mm)"
MARGIN_PER_SAT_PER_YR_MM: Final[str] = "Margin per sat per yr ($mm)"
MARS_PAYLOAD_AS_LABOUR_UNITS: Final[str] = "Mars % payload as labour units"
MARS_CARVE_OUT_CASH_THIS_YEAR_MM: Final[str] = "Mars carve-out cash this year ($mm)"
MARS_FUEL_DEPOT_MULTIPLIER_PER_OUTBOUND_STARSHIP: Final[str] = "Mars fuel depot multiplier per outbound Starship"
MARS_HARDWARE_MASS_LANDED_THIS_YEAR_KG: Final[str] = "Mars hardware mass landed this year (kg)"
MARS_HARDWARE_MASS_PER_SHIP_KG: Final[str] = "Mars hardware mass per ship (kg)"
MARS_LABOUR_MASS_LANDED_THIS_YEAR_KG: Final[str] = "Mars labour mass landed this year (kg)"
MARS_LABOUR_MASS_PER_SHIP_KG: Final[str] = "Mars labour mass per ship (kg)"
MARS_LABOUR_UNITS_LANDED_THIS_YEAR_COUNT: Final[str] = "Mars labour units landed this year (count)"
MARS_LABOUR_UNITS_PER_SHIP_COUNT: Final[str] = "Mars labour units per ship (count)"
MARS_PAYLOAD_PER_SURFACE_LANDED_STARSHIP_KG: Final[str] = "Mars payload per surface-landed Starship (kg)"
MARS_SHARE_OF_CARVE_OUT_CASH_YEAR_ROW: Final[str] = "Mars share of carve-out cash (year-row)"
MARS_SURFACE_MISSIONS_DEPLOYED_COUNT: Final[str] = "Mars surface missions deployed (count)"
MAX_STARSHIP_BUILD_CAPACITY_ADDED_PER_YEAR_SHIPS_YR: Final[str] = "Max Starship build-capacity added per year (ships/yr)"
MAX_STARSHIP_LAUNCH_CAPACITY_KG_YR_CEILING_0_OFF: Final[str] = "Max Starship launch capacity (kg/yr ceiling): 0 = off"
MEMO_RETIRED_CARVE_OUT_COMPUTED_ON_CASH_ALLOCATION_ENGINE_R24: Final[str] = "Memo: (retired: carve-out computed on Cash Allocation Engine R24)"
MEMO_2025_CAPEX_RECONCILIATION: Final[str] = "Memo: 2025 CapEx reconciliation"
MEMO_2025_D_A_RECONCILIATION: Final[str] = "Memo: 2025 D&A reconciliation"
MEMO_2025_DTC_SUB_LINE_RECONCILIATION: Final[str] = "Memo: 2025 DTC sub-line reconciliation"
MEMO_2025_EBIT_RECONCILIATION: Final[str] = "Memo: 2025 EBIT reconciliation"
MEMO_2025_REVENUE_RECONCILIATION: Final[str] = "Memo: 2025 revenue reconciliation"
MEMO_AI_COMPUTE_SUB_LINES_MODULE_REVENUE: Final[str] = "Memo: AI - Compute sub-lines − module Revenue"
MEMO_AI_APPS_PER_CUSTOMER_SPOT_IRR_DIAGNOSTIC_NO_ALLOCATION_CONSUMER: Final[str] = "Memo: AI Apps per-customer Spot IRR (diagnostic: no allocation consumer)"
MEMO_AI_EBITDA_TIE_GROUP_EBITDA_AI_R54_MODULE_AI_COMPUTE_R169_R168_MUST_0: Final[str] = "Memo: AI EBITDA tie: Group EBITDA-AI (R54) − module ('AI - Compute' R169+R168); must = 0"
MEMO_AI_KG_RATION_DIAGNOSTIC_ODC_SELF_SUPPLIES_A7_1: Final[str] = "Memo: AI kg ration (diagnostic: ODC self-supplies, A7.1)"
MEMO_AI_PLACEHOLDER_STRATEGIC_CAPEX_MM_ENGINE_TEMP: Final[str] = "Memo: AI placeholder strategic CapEx ($mm): engine, TEMP"
MEMO_AI_SEGMENT_AI_SOLUTIONS_INFRA_2025_M: Final[str] = "Memo: AI segment AI Solutions & Infra 2025 ($M)"
MEMO_AI_SEGMENT_ADJ_EBITDA_2025_M: Final[str] = "Memo: AI segment Adj EBITDA 2025 ($M)"
MEMO_AI_SEGMENT_ADVERTISING_2025_M: Final[str] = "Memo: AI segment Advertising 2025 ($M)"
MEMO_AI_SEGMENT_CAPEX_2025_M: Final[str] = "Memo: AI segment CapEx 2025 ($M)"
MEMO_AI_SEGMENT_R_D_2025_M: Final[str] = "Memo: AI segment R&D 2025 ($M)"
MEMO_AI_SEGMENT_NAMEPLATE_COMPUTE_DRAW_EOY_2025_GW: Final[str] = "Memo: AI segment nameplate compute draw EoY 2025 (GW)"
MEMO_AI_SEGMENT_TOTAL_REVENUE_2025_M: Final[str] = "Memo: AI segment total revenue 2025 ($M)"
MEMO_ACCUMULATED_DEPRECIATION_DEC_31_2025_M: Final[str] = "Memo: Accumulated depreciation Dec 31 2025 ($M)"
MEMO_ATTRIBUTED_R_D_STARLINK_IN_MODULE_OPEX_EXCL_TOTAL_R_D: Final[str] = "Memo: Attributed R&D, Starlink (in Module OpEx; excl. Total R&D)"
MEMO_ATTRIBUTED_R_D_STARLINK_NOW_IN_MODULE_OPEX_EXCL_FROM_TOTAL_R_D: Final[str] = "Memo: Attributed R&D, Starlink (now in Module OpEx; excl. from Total R&D)"
MEMO_AVERAGE_GBPS_BB_FROM_CURVE: Final[str] = "Memo: Average $/Gbps BB from curve"
MEMO_AVERAGE_GBPS_DTC_FROM_CURVE: Final[str] = "Memo: Average $/Gbps DTC from curve"
MEMO_AVG_CUSTOMER_PAYLOAD_SIZE_MT_MISSION: Final[str] = "Memo: Avg customer payload size (mt/mission)"
MEMO_CARVE_OUT_RESERVED_VS_MODULE_CAPEX_GAP_MM: Final[str] = "Memo: Carve-out reserved vs Module CapEx gap ($mm)"
MEMO_CONNECTIVITY_ADJ_EBITDA_MARGIN_2025_CALIBRATION_TARGET: Final[str] = "Memo: Connectivity Adj EBITDA margin 2025: calibration target"
MEMO_CONNECTIVITY_COGS_2025_M: Final[str] = "Memo: Connectivity COGS 2025 ($M)"
MEMO_CONNECTIVITY_COGS_2025_M_CALIBRATION: Final[str] = "Memo: Connectivity COGS 2025 ($M): calibration"
MEMO_CONNECTIVITY_CONSUMER_REVENUE_2025_M: Final[str] = "Memo: Connectivity Consumer revenue 2025 ($M)"
MEMO_CONNECTIVITY_E_G_INCL_MOBILE_REVENUE_2025_M: Final[str] = "Memo: Connectivity E&G incl Mobile revenue 2025 ($M)"
MEMO_CONNECTIVITY_R_D_2025_M: Final[str] = "Memo: Connectivity R&D 2025 ($M)"
MEMO_CONNECTIVITY_R_D_2025_M_CALIBRATION: Final[str] = "Memo: Connectivity R&D 2025 ($M): calibration"
MEMO_CONNECTIVITY_SG_A_2025_M: Final[str] = "Memo: Connectivity SG&A 2025 ($M)"
MEMO_CONNECTIVITY_SG_A_2025_M_CALIBRATION: Final[str] = "Memo: Connectivity SG&A 2025 ($M): calibration"
MEMO_CONNECTIVITY_SEGMENT_CAPEX_2025_M: Final[str] = "Memo: Connectivity segment CapEx 2025 ($M)"
MEMO_CONNECTIVITY_SEGMENT_INCOME_FROM_OPS_2025_M_CALIBRATION: Final[str] = "Memo: Connectivity segment income from ops 2025 ($M): calibration"
MEMO_COUNTRIES_SERVED: Final[str] = "Memo: Countries served"
MEMO_CUSTOMER_A_CONCENTRATION_RISK_US_GOV_NASA_DOW_CONSOL: Final[str] = "Memo: Customer A concentration risk (US Gov NASA+DoW % consol)"
MEMO_CUSTOMER_LAUNCH_SUB_LINES_MODULE_REVENUE: Final[str] = "Memo: Customer Launch sub-lines − module Revenue"
MEMO_DC_CHIPS_DEPLOYED_ODC_R55_TERR_R94: Final[str] = "Memo: DC chips deployed (ODC R55 + Terr R94)"
MEMO_DEFERRED_REVENUE_DEC_31_2025_M: Final[str] = "Memo: Deferred revenue (Dec 31 2025) ($M)"
MEMO_DEMAND_DAMPENER_PRICE_AT_Q_MIN_1_DEMAND_SUPPLY_B: Final[str] = "Memo: Demand dampener (price-at-Q, =MIN(1,(demand/supply)^b))"
MEMO_EBITDA_MARGIN: Final[str] = "Memo: EBITDA Margin %"
MEMO_ECHOSTAR_SPECTRUM_DEAL_TOTAL_M_S_1_AUDITED: Final[str] = "Memo: EchoStar spectrum deal total ($M, S-1 audited)"
MEMO_ENGINE_CASH_GROUP_FCF_MM: Final[str] = "Memo: Engine cash Group FCF ($mm)"
MEMO_ENTERPRISE_CHURN_QUALITATIVE: Final[str] = "Memo: Enterprise churn: qualitative"
MEMO_F9_AVAILABLE_CAPACITY_KG: Final[str] = "Memo: F9 available capacity (kg)"
MEMO_F9_CUSTOMER_MODEL_VS_S_1_CUSTOMER_STARSHIELD: Final[str] = "Memo: F9 customer (model) vs S-1 customer − Starshield"
MEMO_F9_CUSTOMER_LAUNCHES_CUSTOMER_LAUNCH: Final[str] = "Memo: F9 customer launches (Customer Launch)"
MEMO_F9_INTERNAL_MODEL_VS_S_1_CORE_STARLINK_STARSHIELD: Final[str] = "Memo: F9 internal (model) vs S-1 core Starlink + Starshield"
MEMO_F9_INTERNAL_LAUNCHES_STARLINK_DRIVEN: Final[str] = "Memo: F9 internal launches (Starlink-driven)"
MEMO_F9_LAUNCH_CAPACITY_LAUNCHES_YR: Final[str] = "Memo: F9 launch capacity (launches/yr)"
MEMO_F9_PRICE_SET_TO_54_8M_LANDS_2025_LAUNCH_SERVICES_2_575_6M_TARGET_2_576M_LAUNCH_DELIVERY_1_510M_REVENUE_4_085_6M_S_1_SPACE_4_086M: Final[str] = "Memo: F9 price set to $54.8M lands 2025 Launch Services = $2,575.6M (target $2,576M) + Launch & Delivery $1,510M → revenue $4,085.6M ≈ S-1 Space $4,086M."
MEMO_GROSS_MARGIN: Final[str] = "Memo: Gross Margin %"
MEMO_GROUP_D_A_2025_VARIANCE_VS_1_060M: Final[str] = "Memo: Group D&A 2025 variance vs $1,060M"
MEMO_GROUP_EBITDA_2025_VARIANCE_VS_8_690M: Final[str] = "Memo: Group EBITDA 2025 variance vs $8,690M"
MEMO_GROUP_EV_AS_OF2026_EXIT_B: Final[str] = "Memo: Group EV as-of2026 Exit $B"
MEMO_GROUP_EV_AS_OF2026_GORDON_B: Final[str] = "Memo: Group EV as-of2026 Gordon $B"
MEMO_GROUP_FCF_2025_VARIANCE_VS_3_670M: Final[str] = "Memo: Group FCF 2025 variance vs $3,670M"
MEMO_GROUP_REVENUE_GROUP_P_L_GROUP_REVENUE: Final[str] = "Memo: Group Revenue − Group P&L Group Revenue"
MEMO_GROUP_REVENUE_CLAIMS_BASE_MM: Final[str] = "Memo: Group revenue (claims base) ($mm)"
MEMO_HQ_CAPEX_2025_53M_REFERENCE: Final[str] = "Memo: HQ CapEx (2025 ≈ $53M reference)"
MEMO_INTERFACE_CONTRACT_MODULE_OUT_CANONICAL_LABELS: Final[str] = "Memo: Interface contract: Module OUT canonical labels"
MEMO_L_M_SOTP_BV_BASED_AS_OF_2026: Final[str] = "Memo: L/M SoTP (BV-based, as-of 2026)"
MEMO_L_M_STRATEGIC_PREMIUM_OVER_CASH_DRAIN_PV: Final[str] = "Memo: L/M strategic premium over cash-drain PV"
MEMO_LOSS_FROM_OPERATIONS_2025_M_CALIBRATION: Final[str] = "Memo: Loss from operations 2025 ($M): calibration"
MEMO_LUNAR_MARS_SUB_LINE_MODULE_REVENUE: Final[str] = "Memo: Lunar - Mars sub-line − module Revenue"
MEMO_LUNAR_SURFACE_MISSIONS_CUMULATIVE: Final[str] = "Memo: Lunar surface missions cumulative"
MEMO_MNO_ADDRESSABLE_POPULATION_MILLIONS: Final[str] = "Memo: MNO addressable population (millions)"
MEMO_MNO_PARTNER_COUNT: Final[str] = "Memo: MNO partner count"
MEMO_MARS_SURFACE_MISSIONS_CUMULATIVE: Final[str] = "Memo: Mars surface missions cumulative"
MEMO_MASS_TO_ORBIT_F9_KG: Final[str] = "Memo: Mass to orbit: F9 (kg)"
MEMO_MASS_TO_ORBIT_STARSHIP_KG: Final[str] = "Memo: Mass to orbit: Starship (kg)"
MEMO_ODC_CUM_DRAWS_MM: Final[str] = "Memo: ODC cum draws ($mm)"
MEMO_ODC_CUM_REPAYMENTS_MM: Final[str] = "Memo: ODC cum repayments ($mm)"
MEMO_ODC_DEMAND_SHARE_RETIRED_A8_3_DEMAND_NOT_SPLIT_ODC_PRIORITY: Final[str] = "Memo: ODC demand share: RETIRED A8.3 (demand not split; ODC-priority)"
MEMO_ODC_FIRST_DEPLOYMENT_YEAR_ANCHOR: Final[str] = "Memo: ODC first deployment year (anchor)"
MEMO_ODC_KG_BUILDABLE_DIAGNOSTIC_UNUSED_AFTER_A7_1: Final[str] = "Memo: ODC kg-buildable (diagnostic: unused after A7.1)"
MEMO_ODC_TERR_SPILLOVER_MM_A8_3_CONSUMED_BY_R114: Final[str] = "Memo: ODC→Terr spillover ($mm): A8.3 (consumed by R114)"
MEMO_OPERATING_CASH_FLOW_2025_M_CALIBRATION: Final[str] = "Memo: Operating cash flow 2025 ($M): calibration"
MEMO_P_L_IRR_CONSERVATION: Final[str] = "Memo: P&L↔IRR conservation"
MEMO_P_L_IRR_OPERATING_MARGIN: Final[str] = "Memo: P&L↔IRR operating-margin"
MEMO_PP_E_NET_DEC_31_2025_M: Final[str] = "Memo: PP&E net Dec 31 2025 ($M)"
MEMO_PV_OF_L_M_FCF_DRAIN_EMBEDDED_IN_GROUP_FCF: Final[str] = "Memo: PV of L/M FCF drain embedded in Group FCF"
MEMO_R_D_DUAL_TRACK_DIVERGENCE: Final[str] = "Memo: R&D dual-track divergence"
MEMO_REALIZED_GPU_HR_BASE_DAMPENER: Final[str] = "Memo: Realized $/GPU-hr (base × dampener)"
MEMO_SPACE_CONNECTIVITY_CAPEX_2025_M: Final[str] = "Memo: Space + Connectivity CapEx 2025 ($M)"
MEMO_SPACE_R_D_2025_M_CALIBRATION: Final[str] = "Memo: Space R&D 2025 ($M): calibration"
MEMO_SPACE_SEGMENT_CAPEX_2025_M: Final[str] = "Memo: Space segment CapEx 2025 ($M)"
MEMO_SPACE_SEGMENT_INCOME_FROM_OPS_2025_M_CALIBRATION: Final[str] = "Memo: Space segment income from ops 2025 ($M): calibration"
MEMO_SPACEX_LAUNCH_SERVICES_REV_AS_OF_EXPANDED_TAM_COHERENCE_CHECK_MUST_BE_100: Final[str] = "Memo: SpaceX Launch-Services rev as % of expanded $TAM (coherence check, must be <100%)"
MEMO_SPECTRUM_LICENCE_FEE_RENEWAL_FLAG_2042: Final[str] = "Memo: Spectrum licence fee renewal flag (2042)"
MEMO_STARLINK_SUB_LINES_MODULE_REVENUE: Final[str] = "Memo: Starlink sub-lines − module Revenue"
MEMO_STARLINK_DTC_REVENUE_EXCL_STARSHIELD: Final[str] = "Memo: Starlink+DTC revenue (excl. Starshield)"
MEMO_SUBSEQUENT_EVENTS_CHECK_S_1_A: Final[str] = "Memo: Subsequent events check (S-1/A)"
MEMO_TERR_MW_DEMAND_IMPLIED_PRE_CASH: Final[str] = "Memo: Terr MW demand-implied (pre-cash)"
MEMO_TERR_DEMAND_SHARE_RETIRED_A8_3_DEMAND_NOT_SPLIT: Final[str] = "Memo: Terr demand share: RETIRED A8.3 (demand not split)"
MEMO_TERR_SHARE_OF_NET_DEMAND_GAP_RETIRED_A8_0_1_SUPERSEDED_BY_IRR_SHARE_DEMAND_SPLIT: Final[str] = "Memo: Terr share of net demand gap: RETIRED A8.0.1 (superseded by IRR-share demand split)"
MEMO_TERRESTRIAL_AI_COMPUTE_DRAW_GW_YEAR_ROW: Final[str] = "Memo: Terrestrial AI compute draw (GW): year-row"
MEMO_TERR_ODC_SPILLOVER_MM_A8_3_CONSUMED_BY_R112: Final[str] = "Memo: Terr→ODC spillover ($mm): A8.3 (consumed by R112)"
MEMO_TESLA_FUNDED_FAB_CAPEX_1_SHARE_MM: Final[str] = "Memo: Tesla-funded fab CapEx ((1−share)) ($mm)"
MEMO_TOTAL_F9_LAUNCHES_INTERNAL_CUSTOMER: Final[str] = "Memo: Total F9 launches (internal + customer)"
MEMO_TOTAL_LUNAR_MARS_ACCUMULATED_BV_MM_SOTP_TERMINAL_INPUT: Final[str] = "Memo: Total Lunar + Mars Accumulated BV ($mm): SoTP terminal input"
MEMO_TOTAL_LUNAR_MARS_KG_LANDED_THIS_YEAR: Final[str] = "Memo: Total Lunar+Mars kg landed this year"
MEMO_TOTAL_BACKLOG_DEC_31_2025_M: Final[str] = "Memo: Total backlog (Dec 31 2025) ($M)"
MEMO_TOTAL_DEPRECIATION_2025_M_CALIBRATION: Final[str] = "Memo: Total depreciation 2025 ($M): calibration"
MEMO_TOTAL_MASS_TO_ORBIT_MT: Final[str] = "Memo: Total mass to orbit (mt)"
MEMO_TOTAL_DEMAND_VS_SUPPLY_CHECK: Final[str] = "Memo: Total-demand-vs-supply CHECK"
MEMO_VB_FLEET_CAPEX_CONSERVATION_VB_R53: Final[str] = "Memo: VB fleet CapEx conservation (=VB R53)"
MEMO_VEHICLE_BUILD_FCF_MM_MUST_0_BY_CONSTRUCTION: Final[str] = "Memo: Vehicle Build FCF ($mm): must = 0 by construction"
MEMO_AVG_LAUNCH_LS: Final[str] = "Memo: avg $/launch (LS)"
MEMO_BEST_AVAILABLE_LAUNCH_KG_INDEX_MM_KG_READINESS_BLENDED: Final[str] = "Memo: best-available launch $/kg index ($mm/kg, readiness-blended)"
MEMO_BOOSTER_FLEET_RECONCILIATION_CUM_BUILT_CUM_RETIRED_BOOSTER_FLEET_EOY_MUST_0: Final[str] = "Memo: booster fleet reconciliation ((cum built − cum retired) − Booster fleet EoY; must = 0)"
MEMO_CARVE_OUT_TIE_ENGINE_LM_RECEIPT_MUST_0: Final[str] = "Memo: carve-out tie (engine − LM receipt, must=0)"
MEMO_CASH_DEPLOYED_BY_MODULES_MM: Final[str] = "Memo: cash deployed by modules ($mm)"
MEMO_CHIP_SUPPLY_CHECK_SOFT: Final[str] = "Memo: chip-supply check (soft)"
MEMO_CUM_ACTIVE_LAUNCH_VEHICLES_F9_STARSHIP: Final[str] = "Memo: cum active launch vehicles (F9 + Starship)"
MEMO_CUM_LAUNCH_SITE_INFRA_CAPEX_MM: Final[str] = "Memo: cum launch-site infra CapEx ($mm)"
MEMO_CUMULATIVE_START_IPO_BRIDGE_FCF_FACILITY_NET_MM: Final[str] = "Memo: cumulative (Start+ΣIPO+ΣBridge+ΣFCF+Facility net) ($mm)"
MEMO_CUMULATIVE_DRAWS_MM: Final[str] = "Memo: cumulative draws ($mm)"
MEMO_CUMULATIVE_REPAYMENTS_MM: Final[str] = "Memo: cumulative repayments ($mm)"
MEMO_EXPANDED_COMMERCIAL_LAUNCH_TAM_MM_ELASTIC_BASELINE_ROW_13_MULTIPLIER: Final[str] = "Memo: expanded commercial launch $TAM ($mm, elastic — baseline row 13 × multiplier)"
MEMO_EXPANDED_GOVERNMENT_LAUNCH_TAM_MM_ELASTIC_BASELINE_ROW_14_MULTIPLIER: Final[str] = "Memo: expanded government launch $TAM ($mm, elastic — baseline row 14 × multiplier)"
MEMO_EXPLICIT_DCF_OF_GROUP_FCF_INCL_L_M_NO_TV: Final[str] = "Memo: explicit-DCF of Group FCF incl L/M (no TV)"
MEMO_EXPLICIT_DCF_OF_SOTP_MODULES_SL_CL_AI_CORP: Final[str] = "Memo: explicit-DCF of SoTP modules (SL+CL+AI+Corp)"
MEMO_FLEET_CAPEX_CONSERVATION_ENGINE_MODULE_MUST_0: Final[str] = "Memo: fleet CapEx conservation (engine − Σ module; must = 0)"
MEMO_FULL_JV_FAB_CAPEX_100_PRE_SHARE_MM: Final[str] = "Memo: full JV fab CapEx (100%, pre-share) ($mm)"
MEMO_IMPLIED_TOTAL_STARLINK_SUBSCRIBERS_BB_M_VS_S_1_8_9M: Final[str] = "Memo: implied total Starlink subscribers (BB, M) vs S-1 8.9M"
MEMO_LAUNCH_CADENCE_WRIGHT_S_LAW_IS_DRIVEN_BY_TOTAL_FLEET_CUMULATIVE_UP_MASS_ROW_76_ROW_32_STARSHIP_LAUNCHES_PAYLOAD_ALL_FLIGHTS_INTERNAL_STARLINK_COMMERCIAL_NOT_CUSTOMER_LAUNCH_FLIGHTS_ONLY_DO_NOT_REPOINT: Final[str] = "Memo: launch cadence (Wright's Law) is driven by total fleet cumulative up-mass (row 76 = Σ row 32 Starship launches × payload) — all flights, internal Starlink + commercial, not customer-launch flights only. Do not repoint."
MEMO_LAUNCH_DEMAND_ELASTICITY_MULTIPLIER_X: Final[str] = "Memo: launch demand elasticity multiplier (x)"
MEMO_LAUNCH_INFRA_ALLOCABLE_PER_VEHICLE_MM: Final[str] = "Memo: launch-infra allocable per vehicle ($mm)"
MEMO_LAUNCH_VEHICLE_CAPEX_2025_593M_REFERENCE_LOW_TODAY_STARSHIP_SHIPS_0: Final[str] = "Memo: launch/vehicle CapEx (2025 ≈ $593M reference; low today: Starship ships = 0)"
MEMO_LAUNCH_VEHICLE_FACILITY_CAPEX_FROM_FACILITIES_BUILD: Final[str] = "Memo: launch/vehicle facility CapEx (from Facilities Build)"
MEMO_NORMALIZATION_DELTA_ACCRUAL_WALK_NORMALIZED_WALK_MM: Final[str] = "Memo: normalization delta (accrual walk − normalized walk) ($mm)"
MEMO_POST_REBUILD_CAPACITY_STATE_DEMAND_CURVES_NOW_PRICES_THIS_TAB: Final[str] = "Memo: post-rebuild capacity state (Demand Curves now prices this tab)"
MEMO_RECLASSIFICATION_CONSERVATION: Final[str] = "Memo: reclassification conservation"
MEMO_ROLL_UP_CAPEX_IRR_SLUG_BASIS_FAB_ON_D_A_MM: Final[str] = "Memo: roll-up CapEx: IRR slug basis (fab on D&A) ($mm)"
MEMO_ROLL_UP_BLENDED_LIFE_L_YRS: Final[str] = "Memo: roll-up blended life L (yrs)"
MEMO_ROLL_UP_CAPEX_SLUG_PER_GPU_HR_MM: Final[str] = "Memo: roll-up capex slug per GPU-hr ($mm)"
MEMO_ROLL_UP_CUMULATIVE_CAPEX_MM: Final[str] = "Memo: roll-up cumulative CapEx ($mm)"
MEMO_ROLL_UP_MARGIN_PER_GPU_HR_MM: Final[str] = "Memo: roll-up margin per GPU-hr ($mm)"
MEMO_SATELLITE_MANUFACTURING_CAPEX_2025_200M_REFERENCE: Final[str] = "Memo: satellite-manufacturing CapEx (2025 ≈ $200M reference)"
MEMO_SHARE_SUM_MUST_1: Final[str] = "Memo: share sum (must=1)"
MEMO_SHIP_FLEET_RECONCILIATION_CUM_BUILT_CUM_RETIRED_SHIP_FLEET_EOY_MUST_0: Final[str] = "Memo: ship fleet reconciliation ((cum built − cum retired) − Ship fleet EoY; must = 0)"
MEMO_TOTAL_F9_MODEL_VS_S_1_TOTAL_171_132_INTERNAL_38_6_CUSTOMER: Final[str] = "Memo: total F9 (model) vs S-1 total 171 (132 internal + 38.6 customer)"
MEMO_TOTAL_EXTERNAL_LAUNCHES: Final[str] = "Memo: total external launches"
MEMO_TOTAL_KG_DEMAND_KG: Final[str] = "Memo: total kg demand (kg)"
MEMO_TOTAL_LAUNCH_FACILITY_CAPEX: Final[str] = "Memo: total launch + facility CapEx"
MEMO_WITHIN_AI_SHARE_SUM_1: Final[str] = "Memo: within-AI share sum (=1)"
MEMO_GROUP_FCF_CUMULATIVE_RULE_23_YR_CHAINED: Final[str] = "Memo: Σ Group FCF cumulative (Rule 23 yr-chained)"
MEMO_MODULE_OWNED_LAUNCH_CAPEX_ALL_MODULES: Final[str] = "Memo: Σ module owned launch CapEx (all modules)"
MEMO_NEW_INFRASTRUCTURE_CAPEX_EX_TERMINAL_MM: Final[str] = "Memo: Σ new infrastructure CapEx ex-terminal ($mm)"
MIDPOINT_MEAN_OF_3: Final[str] = "Midpoint (mean of 3)"
MINIMUM_CASH_BUFFER_MM: Final[str] = "Minimum cash buffer ($mm)"
MISSION_OPS_COST_LUNAR_MM: Final[str] = "Mission ops cost: Lunar ($mm)"
MISSION_OPS_COST_LUNAR_OF_LUNAR_CAPEX: Final[str] = "Mission ops cost: Lunar (% of Lunar CapEx)"
MISSION_OPS_COST_MARS_MM: Final[str] = "Mission ops cost: Mars ($mm)"
MISSION_OPS_COST_MARS_OF_MARS_CAPEX: Final[str] = "Mission ops cost: Mars (% of Mars CapEx)"
MODEL_GORDON_VS_BRANT: Final[str] = "Model (Gordon) vs Brant"
MODEL_GORDON_VS_MS: Final[str] = "Model (Gordon) vs MS"
MODEL_EV_AS_OF_2026_EXIT_MULT: Final[str] = "Model EV as-of 2026: Exit-mult"
MODEL_EV_AS_OF_2026_GORDON: Final[str] = "Model EV as-of 2026: Gordon"
MODULE_CAPEX: Final[str] = "Module CapEx"
MODULE_CAPEX_MM: Final[str] = "Module CapEx ($mm)"
MODULE_CAPEX_FCF_INPUT_MM: Final[str] = "Module CapEx (FCF input) ($mm)"
MODULE_CAPEX_TOTAL_MM: Final[str] = "Module CapEx total ($mm)"
MODULE_CAPEX_TOTAL_MM_ALLOCATOR_OUT: Final[str] = "Module CapEx total ($mm)   ◄ Allocator OUT"
MODULE_EBIT: Final[str] = "Module EBIT"
MODULE_EBIT_MM: Final[str] = "Module EBIT ($mm)"
MODULE_EBIT_MM_ALLOCATOR_OUT: Final[str] = "Module EBIT ($mm)   ◄ Allocator OUT"
MODULE_EBITDA: Final[str] = "Module EBITDA"
MODULE_EBITDA_MM: Final[str] = "Module EBITDA ($mm)"
MODULE_EBITDA_MM_ALLOCATOR_OUT: Final[str] = "Module EBITDA ($mm)   ◄ Allocator OUT"
MODULE_EBITDA_MARGIN: Final[str] = "Module EBITDA Margin %"
MODULE_FCF: Final[str] = "Module FCF"
MODULE_FCF_MM: Final[str] = "Module FCF ($mm)"
MODULE_FCF_MM_ALLOCATOR_OUT: Final[str] = "Module FCF ($mm)   ◄ Allocator OUT"
MODULE_OPEX: Final[str] = "Module OpEx"
MODULE_OPEX_MM: Final[str] = "Module OpEx ($mm)"
MODULE_OPEX_TOTAL_MM_ALLOCATOR_OUT: Final[str] = "Module OpEx total ($mm)   ◄ Allocator OUT"
MODULE_OPEX_TOTAL_INCL_R_D_MM: Final[str] = "Module OpEx total (incl. R&D) ($mm)"
MODULE_OPEX_AI_COMPUTE: Final[str] = "Module OpEx: AI - Compute"
MODULE_OPEX_CUSTOMER_LAUNCH: Final[str] = "Module OpEx: Customer Launch"
MODULE_OPEX_LUNAR_MARS: Final[str] = "Module OpEx: Lunar - Mars"
MODULE_OPEX_STARLINK: Final[str] = "Module OpEx: Starlink"
MODULE_SPOT_IRR_ALLOCATOR_OUT: Final[str] = "Module Spot IRR   ◄ Allocator OUT"
MODULE_SPOT_IRR_REV_WEIGHTED: Final[str] = "Module Spot IRR (rev-weighted)"
MODULE_OPERATING_COST_LUNAR_OF_LUNAR_CAPEX: Final[str] = "Module operating cost: Lunar (% of Lunar CapEx)"
MODULE_OPERATING_COST_MARS_OF_MARS_CAPEX: Final[str] = "Module operating cost: Mars (% of Mars CapEx)"
MONTHS_ELAPSED_IN_PACING_YEAR_FOR_ANNUALIZATION: Final[str] = "Months elapsed in pacing year (for annualization)"
MULTIPLE_AI_COMPUTE_EV_EBITDA_AT_HORIZON: Final[str] = "Multiple: AI/Compute (EV/EBITDA at horizon)"
MULTIPLE_AI_COMPUTE_EV_REV_AT_2050: Final[str] = "Multiple: AI/Compute (EV/Rev at 2050)"
MULTIPLE_CUSTOMER_LAUNCH_EV_EBITDA_AT_HORIZON: Final[str] = "Multiple: Customer Launch (EV/EBITDA at horizon)"
MULTIPLE_CUSTOMER_LAUNCH_EV_REV_AT_2050: Final[str] = "Multiple: Customer Launch (EV/Rev at 2050)"
MULTIPLE_STARLINK_EV_EBITDA_AT_HORIZON: Final[str] = "Multiple: Starlink (EV/EBITDA at horizon)"
MULTIPLE_STARLINK_EV_REV_AT_2050: Final[str] = "Multiple: Starlink (EV/Rev at 2050)"
NOPAT_MM: Final[str] = "NOPAT ($mm)"
NET_MARGIN_PER_CUSTOMER_EXCL_CAC: Final[str] = "Net margin per customer (excl CAC) ($)"
NET_NEW_CUSTOMERS_M: Final[str] = "Net-new customers (M)"
NETWORK_OPERATIONS_MM: Final[str] = "Network operations ($mm)"
NETWORK_OPS_G_A_OF_REVENUE: Final[str] = "Network ops & G&A (% of revenue)"
NEW_GIGABAY_CAPEX_THIS_YEAR_MM: Final[str] = "New Gigabay CapEx this year ($mm)"
NEW_STARSHIELD_DEPLOYMENT_SATS_YR: Final[str] = "New Starshield deployment (sats/yr)"
NEW_STARSHIP_BUILD_CAPACITY_ADDED_SHIPS_YR: Final[str] = "New Starship build-capacity added (ships/yr)"
NEW_V2_BB_DEPLOYMENT_SATS_YR: Final[str] = "New V2 BB deployment (sats/yr)"
NEW_V2_DTC_DEPLOYMENT_SATS_YR: Final[str] = "New V2 DTC deployment (sats/yr)"
NEW_V3_BB_DEPLOYMENT_SATS_YR: Final[str] = "New V3 BB deployment (sats/yr)"
NEW_V3_DTC_DEPLOYMENT_SATS_YR: Final[str] = "New V3 DTC deployment (sats/yr)"
NEW_ENGINE_FACILITY_CAPEX_THIS_YEAR_MM: Final[str] = "New engine-facility CapEx this year ($mm)"
NEW_FAB_CAPEX_THIS_YEAR_MM_3YR_WINDOW_SPREAD: Final[str] = "New fab CapEx this year ($mm): 3yr window spread"
NEW_FAB_CAPACITY_ADDED_WSPM: Final[str] = "New fab capacity added (wspm)"
NEW_LAUNCH_PAD_CAPEX_THIS_YEAR_MM: Final[str] = "New launch-pad CapEx this year ($mm)"
NEW_SAT_FACTORY_CAPEX_THIS_YEAR_MM: Final[str] = "New sat-factory CapEx this year ($mm)"
NEW_TERMINAL_FACTORY_CAPEX_THIS_YEAR_MM_TOGGLE: Final[str] = "New terminal-factory CapEx this year ($mm) × toggle"
NEXT_GEN_R_D_UPLIFT_PEAK_EXTRA_R_D_AT_GEN_JUMP: Final[str] = "Next-gen R&D uplift (peak, × extra R&D at gen jump)"
NON_THERMAL_BASE_MASS_KG_A8_7: Final[str] = "Non-thermal base mass (kg): A8.7"
ODC_CAPEX_NEED_MM_LAUNCH_FEASIBLE_DEPLOY_COST: Final[str] = "ODC CapEx need ($mm): launch-feasible deploy × cost"
ODC_R_D_CAGR: Final[str] = "ODC R&D CAGR"
ODC_R_D_FLOOR_PCT: Final[str] = "ODC R&D floor pct"
ODC_R_D_START_PCT: Final[str] = "ODC R&D start pct"
ODC_CONSTRUCTION_FACILITY_CAP_MM: Final[str] = "ODC construction facility cap ($mm)"
ODC_DEMAND_BUILDABLE_CAPEX_MM: Final[str] = "ODC demand-buildable CapEx ($mm)"
ODC_FACILITY_FCF_REPAYMENT_SWEEP: Final[str] = "ODC facility FCF repayment sweep (%)"
ODC_FACILITY_BALANCE_EOY_MM: Final[str] = "ODC facility balance EoY ($mm)"
ODC_FACILITY_DRAW_MM: Final[str] = "ODC facility draw ($mm)"
ODC_FACILITY_DRAW_WINDOW_END_YEAR: Final[str] = "ODC facility draw-window end year"
ODC_FACILITY_INTEREST_MM: Final[str] = "ODC facility interest ($mm)"
ODC_FACILITY_INTEREST_RATE_ANNUAL: Final[str] = "ODC facility interest rate (annual)"
ODC_FACILITY_REPAID_BY_YEAR: Final[str] = "ODC facility repaid-by year"
ODC_FACILITY_REPAYMENT_MM: Final[str] = "ODC facility repayment ($mm)"
ODC_INSURANCE_PCT_REV: Final[str] = "ODC insurance pct rev"
ODC_OTHER_COGS_PCT_REV: Final[str] = "ODC other COGS pct rev"
ODC_POOL_ALLOCATION_MM: Final[str] = "ODC pool allocation ($mm)"
ODC_POWER_DENSITY_KW_TON_OUTPUT_MEMO_A8_7: Final[str] = "ODC power density (kW/ton): OUTPUT memo (A8.7)"
ODC_POWER_DENSITY_RAMP_END_YEAR: Final[str] = "ODC power density ramp-end year"
ODC_PRE_LAUNCH_R_D_MM_YR_2025_27: Final[str] = "ODC pre-launch R&D ($mm/yr, 2025-27)"
ODC_SAT_FACTORY_CAPEX_MM_PER_SAT_YR_OF_CAPACITY: Final[str] = "ODC sat-factory CapEx ($mm per sat/yr of capacity)"
ODC_SAT_FACTORY_CAPACITY_INSTALLED_SATS_YR_EOY_RATCHET: Final[str] = "ODC sat-factory capacity installed (sats/yr): EoY ratchet"
ODC_SAT_MFG_FACILITY_CAPEX_MM_INFRA_GROUP: Final[str] = "ODC sat-mfg facility CapEx ($mm)  ◄ infra/Group"
ODC_SATS_BUILT_DRIVER_SATS_YR: Final[str] = "ODC sats built: driver (sats/yr)"
ODC_TARGET_FLEET_SATS_DEMAND_SHARE: Final[str] = "ODC target fleet (sats, demand-share)"
ODC_RETIRED_SUPERSEDED_BY_THE_AI_COMPUTE_SECTION_MEMOS_BELOW_RETAINED: Final[str] = "ODC — RETIRED, superseded by the AI/Compute section. Memos below retained."
OPEX_GROUP_LEVEL_MODULE_ATTRIBUTED_R_D_PARAMETERS: Final[str] = "OPEX (Group-level + module-attributed R&D parameters)"
OPEX_MM: Final[str] = "OpEx ($mm)"
ORBITAL_DC_ALLOCATED_CASH_MM_CAE_LEVEL_2: Final[str] = "Orbital DC: allocated cash ($mm) ◄ CAE Level-2"
ORBITAL_PUE: Final[str] = "Orbital PUE"
OTHER_CORPORATE_OPERATING_FLAT_OF_GROUP_REV: Final[str] = "Other corporate operating: flat % of group rev"
OTHER_LAUNCH_COGS_MM: Final[str] = "Other launch COGS ($mm)"
OTHER_NON_THERMAL_MASS_BUS_STRUCTURE_COMPUTE_KG: Final[str] = "Other non-thermal mass: bus+structure+compute (kg)"
OWNED_LAUNCH_FLEET_D_A_MM: Final[str] = "Owned launch-fleet D&A ($mm)"
OWNED_LAUNCH_VEHICLE_CAPEX_MM: Final[str] = "Owned launch-vehicle CapEx ($mm)"
PER_LAUNCH_AT_COST_RATES_MM_INTERNAL_TRANSFER_PRICING_SOURCE: Final[str] = "PER-LAUNCH AT-COST RATES ($mm): internal transfer pricing source"
PUE_BASE_TERRESTRIAL_COLO: Final[str] = "PUE_base (terrestrial colo)"
PAYING_CUSTOMERS_M: Final[str] = "Paying customers (M)"
PAYLOAD_BOOSTER_ONLY_MODE_KG_TO_LEO: Final[str] = "Payload: booster-only mode (kg-to-LEO)"
PAYLOAD_FULLY_REUSABLE_MODE_KG_TO_LEO: Final[str] = "Payload: fully reusable mode (kg-to-LEO)"
PER_SHIP_COST_LUNAR_MM_SHIP: Final[str] = "Per-ship cost: Lunar ($mm/ship)"
PER_SHIP_COST_MARS_MM_SHIP: Final[str] = "Per-ship cost: Mars ($mm/ship)"
PLACEHOLDER_AI_STRATEGIC_CAPEX_MM_TEMP_RETIRE_WHEN_AI_COMPUTE_LOADED: Final[str] = "Placeholder AI/strategic CapEx ($mm): TEMP (retire when AI-Compute loaded)"
PLACEHOLDER_AI_STRATEGIC_CAPEX_OF_GROUP_REVENUE_TEMP: Final[str] = "Placeholder AI/strategic CapEx (% of Group revenue): TEMP"
POOL_AFTER_QUEUE_GATE_MM: Final[str] = "Pool after queue gate ($mm)"
POWER_COST_KWH: Final[str] = "Power cost ($/kWh)"
POWER_COST_CAGR: Final[str] = "Power cost CAGR"
PRE_2025_ACTIVE_STARSHIELD_INSTALLED_BASE_SATS: Final[str] = "Pre-2025 active Starshield installed base (sats)"
PRE_IPO_BRIDGE_LOAN_MM: Final[str] = "Pre-IPO bridge loan ($mm)"
PRODUCTIVITY_MULTIPLIER_YEAR_ROW_ANCHOR_OFFSET: Final[str] = "Productivity multiplier (year-row, anchor-offset)"
QUEUE_GATE_NON_MODULE_CLAIMS_TOTAL_MM: Final[str] = "Queue gate non-module claims total ($mm)"
R_D_OF_REVENUE: Final[str] = "R&D % of revenue"
RETIRED_ORBITAL_DATA_CENTRE_GROUND_STATIONS_CAPEX: Final[str] = "RETIRED (orbital-data-centre ground stations CapEx)"
RETIRED_ORBITAL_DATA_CENTRE_GROUND_STATIONS_INSTALLED: Final[str] = "RETIRED (orbital-data-centre ground stations installed)"
RADIATOR_AREA_M_A8_7: Final[str] = "Radiator area (m²): A8.7"
RADIATOR_AREAL_DENSITY_KG_M_GLIDE_A8_7: Final[str] = "Radiator areal density (kg/m², glide): A8.7"
RADIATOR_AREAL_DENSITY_ANCHOR_2025_KG_M: Final[str] = "Radiator areal density anchor 2025 (kg/m²)"
RADIATOR_AREAL_DENSITY_MATURE_KG_M: Final[str] = "Radiator areal density mature (kg/m²)"
RADIATOR_DELTA_T_K: Final[str] = "Radiator delta-T (K)"
RADIATOR_EMISSIVITY_0_1: Final[str] = "Radiator emissivity (0-1)"
RADIATOR_NET_REJECTION_W_M_A8_7: Final[str] = "Radiator net rejection (W/m²): A8.7"
RANGE_MAX_MIN: Final[str] = "Range (max − min)"
RANK_KEY_AI_COMPUTE: Final[str] = "Rank key: AI-Compute"
RANK_KEY_CUSTOMER_LAUNCH: Final[str] = "Rank key: Customer Launch"
RANK_KEY_STARLINK: Final[str] = "Rank key: Starlink"
RAPTOR_ENGINES_PER_BOOSTER_SUPER_HEAVY: Final[str] = "Raptor engines per booster (Super Heavy)"
RAPTOR_ENGINES_PER_SHIP_2ND_STAGE: Final[str] = "Raptor engines per ship (2nd stage)"
READ_ONLY_DIRECT_PULLS_FROM_MODULE_TABS_EACH_MODULE_ROW_IS_THE_REALIZED_CAPPED_LAUNCH_COUNT_TOTAL_THEIR_SUM: Final[str] = "Read-only. Direct pulls from module tabs. Each module row is the realized (capped) launch count; total = their sum."
REMAINING_POOL_FOR_IRR_WEIGHTED_ALLOCATION_MM_GATED_TO_0_IN_THE_2025_ANCHOR_YEAR_ALLOCATION_OPERATIVE_2026_ONWARD: Final[str] = "Remaining pool for IRR-weighted allocation ($mm): gated to 0 in the 2025 anchor year; allocation operative 2026 onward"
REQUIRED_FAB_CAPACITY_WSPM: Final[str] = "Required fab capacity (wspm)"
REQUIRED_INSTALLED_COMPUTE_W_BUFFER_GPU_HRS: Final[str] = "Required installed compute w/ buffer (GPU-hrs)"
REVENUE: Final[str] = "Revenue"
REVENUE_ALLOCATOR_OUT: Final[str] = "Revenue   ◄ Allocator OUT"
REVENUE_MM: Final[str] = "Revenue ($mm)"
REVENUE_PER_SAT_MM_YR_INCL_ORBITAL_PUE: Final[str] = "Revenue per sat ($mm/yr, incl orbital PUE)"
REVENUE_TIE: Final[str] = "Revenue tie"
REVENUE_AI_COMPUTE: Final[str] = "Revenue: AI - Compute"
REVENUE_AI_COMPUTE_AI_APPS_EXTERNAL: Final[str] = "Revenue: AI - Compute — AI Apps (external)"
REVENUE_AI_COMPUTE_ORBITAL_DC_EXTERNAL: Final[str] = "Revenue: AI - Compute — Orbital DC (external)"
REVENUE_AI_COMPUTE_TERRESTRIAL_DC_EXTERNAL: Final[str] = "Revenue: AI - Compute — Terrestrial DC (external)"
REVENUE_CUSTOMER_LAUNCH: Final[str] = "Revenue: Customer Launch"
REVENUE_CUSTOMER_LAUNCH_LAUNCH_DEVELOPMENT: Final[str] = "Revenue: Customer Launch — Launch & Development"
REVENUE_CUSTOMER_LAUNCH_LAUNCH_SERVICES: Final[str] = "Revenue: Customer Launch — Launch Services"
REVENUE_LUNAR_MARS: Final[str] = "Revenue: Lunar - Mars"
REVENUE_STARLINK: Final[str] = "Revenue: Starlink"
REVENUE_STARLINK_BROADBAND_BB: Final[str] = "Revenue: Starlink — Broadband (BB)"
REVENUE_STARLINK_DIRECT_TO_CELL_DTC: Final[str] = "Revenue: Starlink — Direct-to-Cell (DTC)"
REVENUE_STARLINK_HARDWARE_KIT: Final[str] = "Revenue: Starlink — Hardware / kit"
REVENUE_STARLINK_STARSHIELD: Final[str] = "Revenue: Starlink — Starshield"
ROLL_UP_RECONCILIATION_TAB_MODULES_OWN_LAUNCH_CAPEX_BOOKS_NO_FCF_AGGREGATES_MODULE_OWNED_LAUNCH_CAPEX_FLEET: Final[str] = "Roll-up / reconciliation tab — modules own launch CapEx. Books no FCF; aggregates module-owned launch CapEx + fleet."
ROLL_UP_ATTRIBUTED_R_D: Final[str] = "Roll-up Attributed R&D"
ROLL_UP_COGS_CONSOL: Final[str] = "Roll-up COGS (consol)"
ROLL_UP_D_A: Final[str] = "Roll-up D&A"
ROLL_UP_GROSS_PROFIT: Final[str] = "Roll-up Gross Profit"
ROLL_UP_GROSS_MARGIN: Final[str] = "Roll-up Gross margin %"
ROLL_UP_KG_DEMAND_YEAR_N_1: Final[str] = "Roll-up Kg demand year N+1"
ROLL_UP_MODULE_CAPEX: Final[str] = "Roll-up Module CapEx"
ROLL_UP_MODULE_EBIT: Final[str] = "Roll-up Module EBIT"
ROLL_UP_MODULE_FCF: Final[str] = "Roll-up Module FCF"
ROLL_UP_MODULE_OPEX: Final[str] = "Roll-up Module OpEx"
ROLL_UP_OWNED_LAUNCH_VEHICLE_CAPEX_MM: Final[str] = "Roll-up Owned launch-vehicle CapEx ($mm)"
ROLL_UP_REVENUE_EXTERNAL_CONSOL: Final[str] = "Roll-up Revenue (external, consol)"
ROLL_UP_SPOT_MARGINAL_IRR_EXTERNAL_CONSOL: Final[str] = "Roll-up Spot marginal IRR (external, consol)"
ROLL_UP_STARSHIP_LAUNCHES_PER_YEAR_ODC_DRIVEN: Final[str] = "Roll-up Starship launches per year (ODC-driven)"
RUNNING_COST_COGS_OPEX_MM: Final[str] = "Running cost (COGS+OpEx) ($mm)"
S_M_CUSTOMER_ACQUISITION_MM: Final[str] = "S&M - customer acquisition ($mm)"
S_1_2025_SPACEX_TOTAL_CAPEX_MM: Final[str] = "S-1 2025 SpaceX total CapEx ($mm)"
SHIP_FLEET_ROLL_FORWARD_BOOSTER_SHIP_SPLIT: Final[str] = "SHIP FLEET ROLL-FORWARD (booster / ship split)"
STARLINK: Final[str] = "STARLINK"
STARSHIP_BUILD_CAPEX_SPLIT: Final[str] = "STARSHIP BUILD CapEx SPLIT"
SALES_MARKETING_MM: Final[str] = "Sales & Marketing ($mm)"
SALES_MARKETING_CAGR_TAPER: Final[str] = "Sales & Marketing: CAGR (taper)"
SALES_MARKETING_END_STATE_FLOOR: Final[str] = "Sales & Marketing: end-state % (floor)"
SALES_MARKETING_START_OF_STARLINK_STARSHIELD_CL_EXT_REV: Final[str] = "Sales & Marketing: start % of (Starlink+Starshield+CL ext) rev"
SAT_COST_KG_WRIGHT_S_FLOORED: Final[str] = "Sat cost $/kg (Wright's, floored)"
SAT_FACILITY_CAPACITY_RATIO_CAPEX_EXPONENT: Final[str] = "Sat facility capacity-ratio CapEx exponent"
SAT_FACTORY_BASE_CAPACITY_2025_SATS_YR: Final[str] = "Sat factory base capacity 2025 (sats/yr)"
SAT_FACTORY_CAPACITY_SATS_YR_PER_INCREMENT: Final[str] = "Sat factory capacity (sats/yr per increment)"
SAT_FACTORY_COST_PER_CAPACITY_INCREMENT_MM: Final[str] = "Sat factory cost per capacity increment ($mm)"
SAT_FACTORY_USEFUL_LIFE_YEARS: Final[str] = "Sat factory useful life (years)"
SAT_OPERATIONAL_LIFE_L_YEARS: Final[str] = "Sat operational life L (years)"
SAT_RETIREMENTS_5Y_COHORT: Final[str] = "Sat retirements (5y cohort)"
SAT_SOLAR_GENERATION_W: Final[str] = "Sat solar generation (W)"
SAT_THERMAL_MASS_KG_DERIVED: Final[str] = "Sat thermal mass (kg): derived"
SAT_TOTAL_COST_MM_SAT: Final[str] = "Sat total cost ($mm/sat)"
SAT_UTILIZATION_FRAC: Final[str] = "Sat utilization (frac)"
SAT_FACTORY_CAPACITY_RATIO: Final[str] = "Sat-factory capacity ratio"
SAT_MFG_FACILITY_CAPEX_TOTAL_MM_STARLINK: Final[str] = "Sat-mfg facility CapEx total ($mm)  ◄ Starlink"
SAT_MFG_FACILITY_D_A_MM_STARLINK: Final[str] = "Sat-mfg facility D&A ($mm)  ◄ Starlink"
SATELLITE_DEP_PER_KG_BASE_YEAR_KG_YR: Final[str] = "Satellite Dep per kg: base year ($/kg/yr)"
SATELLITE_BUILD_CAPEX_MM: Final[str] = "Satellite build CapEx ($mm)"
SATELLITE_COST_FLOOR_KG: Final[str] = "Satellite cost floor ($/kg)"
SATELLITE_COST_PER_KG_BASE_YEAR_KG: Final[str] = "Satellite cost per kg: base year ($/kg)"
SATELLITE_COST_PER_KG_LEARNING_RATE: Final[str] = "Satellite cost per kg: learning rate"
SATELLITE_UNIT_BUILD_CAPEX: Final[str] = "Satellite/unit build CapEx"
SATS_ADDED_TARGET: Final[str] = "Sats added (target)"
SATS_BUILT_STARLINK_SATS_YR: Final[str] = "Sats built: Starlink (sats/yr)"
SATS_DEPLOYED_ACTUAL: Final[str] = "Sats deployed (actual)"
SATS_FUNDABLE_FROM_CASH: Final[str] = "Sats fundable from cash"
SATS_FUNDABLE_FROM_LAUNCH_KG: Final[str] = "Sats fundable from launch kg"
SATS_PER_STARSHIP_LAUNCH: Final[str] = "Sats per Starship launch"
SEGMENT_P_L_FULL_GROUP_WATERFALL_WITH_REVENUE_BROKEN_TO_MODULE_SUB_SEGMENTS_READ_ONLY_PRESENTATION_TIES_TO_GROUP_P_L: Final[str] = "Segment P&L — full Group waterfall with revenue broken to module sub-segments (read-only presentation; ties to Group P&L)"
SELLING_GENERAL_ADMINISTRATIVE_MM: Final[str] = "Selling, general & administrative ($mm)"
SHARED_UNATTRIBUTABLE_R_D_MM: Final[str] = "Shared / unattributable R&D ($mm)"
SHARED_UNATTRIBUTABLE_R_D_CORPORATE: Final[str] = "Shared / unattributable R&D: corporate"
SHARED_UNATTRIBUTABLE_R_D_CORPORATE_INCL_STARSHIP_PLATFORM_R_D: Final[str] = "Shared / unattributable R&D: corporate (incl Starship platform R&D)"
SHARED_CORPORATE_R_D_MM_YR_YEAR_ROW: Final[str] = "Shared corporate R&D ($mm/yr): year-row"
SHIELDING_SAT: Final[str] = "Shielding $/sat"
SHIP_BUILD_CAPEX_MM: Final[str] = "Ship build CapEx ($mm)"
SHIP_CADENCE_FLOOR_FLIGHTS_YR_OPERATIONAL: Final[str] = "Ship cadence floor (flights/yr, operational)"
SHIP_FLEET_BOY_UNITS: Final[str] = "Ship fleet BoY (units)"
SHIP_FLEET_EOY_UNITS: Final[str] = "Ship fleet EoY (units)"
SHIP_MFG_PER_STACK_MM: Final[str] = "Ship mfg per stack ($mm)"
SHIP_REFURB_OF_MANUFACTURING: Final[str] = "Ship refurb % of manufacturing"
SHIP_TO_BOOSTER_CADENCE_RATIO: Final[str] = "Ship-to-booster cadence ratio"
SHIPS_BUILT_FLEET: Final[str] = "Ships built (fleet)"
SHIPS_BUILT_THIS_YEAR_VEHICLE_BUILD_SHIPS_BUILT_FLEET_UNIFIED: Final[str] = "Ships built this year (= Vehicle Build Ships built (fleet), unified)"
SHIPS_NEEDED_FLEET: Final[str] = "Ships needed (fleet)"
SHIPS_RETIRED_FLEET: Final[str] = "Ships retired (fleet)"
SOTP_VALUATION_DUAL_TRACK_TERMINAL_SINGLE_WACC_EV_ONLY: Final[str] = "SoTP / VALUATION: dual-track terminal · single WACC · EV only"
SOLAR_ARRAY_W: Final[str] = "Solar array $/W"
SOLAR_ARRAY_MASS_KG_A8_7: Final[str] = "Solar array mass (kg): A8.7"
SOLAR_SPECIFIC_POWER_W_KG_GLIDE_A8_7: Final[str] = "Solar specific power (W/kg, glide): A8.7"
SOLAR_SPECIFIC_POWER_ANCHOR_2025_W_KG: Final[str] = "Solar specific power anchor 2025 (W/kg)"
SOLAR_SPECIFIC_POWER_MATURE_W_KG: Final[str] = "Solar specific power mature (W/kg)"
SPACEX_COMMERCIAL_MARKET_SHARE: Final[str] = "SpaceX commercial market share"
SPACEX_COMMERCIAL_MARKET_SHARE_2: Final[str] = "SpaceX commercial market share %"
SPACEX_GOVERNMENT_MARKET_SHARE: Final[str] = "SpaceX government market share"
SPACEX_GOVERNMENT_MARKET_SHARE_2: Final[str] = "SpaceX government market share %"
SPECTRUM_LICENCE_OPEX_MM: Final[str] = "Spectrum licence OpEx ($mm)"
SPECTRUM_LICENCE_OPEX_OF_REVENUE: Final[str] = "Spectrum licence OpEx (% of revenue)"
SPECTRUM_LICENCE_FEE: Final[str] = "Spectrum licence fee"
SPECTRUM_LICENCE_FEE_MM: Final[str] = "Spectrum licence fee ($mm)"
SPILLOVER_WEIGHT_AI_COMPUTE: Final[str] = "Spillover weight: AI-Compute"
SPILLOVER_WEIGHT_CUSTOMER_LAUNCH: Final[str] = "Spillover weight: Customer Launch"
SPILLOVER_WEIGHT_STARLINK: Final[str] = "Spillover weight: Starlink"
SPOT_IRR: Final[str] = "Spot IRR"
SPOT_IRR_AI_COMPUTE: Final[str] = "Spot IRR: AI-Compute"
SPOT_IRR_CUSTOMER_LAUNCH: Final[str] = "Spot IRR: Customer Launch"
SPOT_IRR_ODC_PRIOR_YR: Final[str] = "Spot IRR: ODC (prior yr)"
SPOT_IRR_STARLINK: Final[str] = "Spot IRR: Starlink"
SPOT_IRR_TERRESTRIAL_PRIOR_YR: Final[str] = "Spot IRR: Terrestrial (prior yr)"
SPOT_MARGINAL_IRR: Final[str] = "Spot marginal IRR"
SPREAD: Final[str] = "Spread %"
SPREAD_EXIT_GORDON: Final[str] = "Spread (Exit − Gordon)"
STARFACTORY_CAPEX_THIS_YEAR_MM: Final[str] = "Starfactory CapEx this year ($mm)"
STARFACTORY_D_A_MM: Final[str] = "Starfactory D&A ($mm)"
STARFACTORY_BUILD_COST_MM: Final[str] = "Starfactory build cost ($mm)"
STARFACTORY_BUILD_WINDOW_YEARS: Final[str] = "Starfactory build window (years)"
STARLINK_2: Final[str] = "Starlink"
STARLINK_INTERNAL: Final[str] = "Starlink (internal)"
STARLINK_INTERNAL_F9: Final[str] = "Starlink (internal) F9"
STARLINK_BB_REVENUE_FROM_CURVE_MM: Final[str] = "Starlink BB Revenue from curve ($mm)"
STARLINK_BB_CAPACITY_INPUT_GBPS: Final[str] = "Starlink BB capacity input (Gbps)"
STARLINK_DTC_REVENUE_FROM_CURVE_MM: Final[str] = "Starlink DTC Revenue from curve ($mm)"
STARLINK_DTC_CAPACITY_INPUT_GBPS: Final[str] = "Starlink DTC capacity input (Gbps)"
STARLINK_R_D_AS_OF_REVENUE_FRAC: Final[str] = "Starlink R&D as % of revenue (frac)"
STARLINK_R_D_CAGR_TAPER: Final[str] = "Starlink R&D: CAGR (taper)"
STARLINK_R_D_END_STATE_FLOOR: Final[str] = "Starlink R&D: end-state % (floor)"
STARLINK_R_D_START_OF_STARLINK_STARSHIELD_REV: Final[str] = "Starlink R&D: start % of (Starlink+Starshield) rev"
STARLINK_DEPLOYMENT_2025_ANCHOR_SATS: Final[str] = "Starlink deployment 2025 anchor (sats)"
STARLINK_GROUND_NETWORK_CAPEX_MM: Final[str] = "Starlink ground-network CapEx ($mm)"
STARLINK_GROUND_NETWORK_CAPEX_OF_STARLINK_REVENUE: Final[str] = "Starlink ground-network CapEx (% of Starlink revenue)"
STARLINK_MODULE_ALLOCATED_CASH_MM_YR_LIVE_FROM_CASH_ALLOCATION_ENGINE: Final[str] = "Starlink module allocated cash ($mm/yr): live from Cash Allocation Engine"
STARLINK_MODULE_REAL_COHORTS_TOTAL_BANDWIDTH_REVENUE_FULL_WATERFALL_4_LINE_OPEX_PER_SAT_IRR: Final[str] = "Starlink module — real cohorts + total-bandwidth revenue + full waterfall + 4-line OpEx + per-sat IRR"
STARLINK_BROADBAND_BB: Final[str] = "Starlink — Broadband (BB)"
STARLINK_DIRECT_TO_CELL_DTC: Final[str] = "Starlink — Direct-to-Cell (DTC)"
STARLINK_HARDWARE_KIT: Final[str] = "Starlink — Hardware / kit"
STARLINK_STARSHIELD: Final[str] = "Starlink — Starshield"
STARLINK_TOTAL: Final[str] = "Starlink — total"
STARSHIELD_GBPS_GBPS_YR: Final[str] = "Starshield $/Gbps ($/Gbps-yr)"
STARSHIELD_GBPS_GBPS_YR_WORKING: Final[str] = "Starshield $/Gbps ($/Gbps-yr) (working)"
STARSHIELD_GBPS_GROWTH_FRAC: Final[str] = "Starshield Gbps growth (frac)"
STARSHIELD_ACTIVE_GBPS_WORKING: Final[str] = "Starshield active Gbps (working)"
STARSHIELD_ACTIVE_GBPS_YEAR_ROW: Final[str] = "Starshield active Gbps (year-row)"
STARSHIELD_REVENUE_MM: Final[str] = "Starshield revenue ($mm)"
STARSHIELD_SAT_MASS_KG: Final[str] = "Starshield sat mass (kg)"
STARSHIELD_UTILIZATION_FRAC: Final[str] = "Starshield utilization (frac)"
STARSHIELD_CAPEX_SLUG_PER_SAT_MM: Final[str] = "Starshield: CapEx slug per sat ($mm)"
STARSHIELD_ACTIVE_FLEET_EOY_SATS_WORKING: Final[str] = "Starshield: active fleet EoY (sats) (working)"
STARSHIELD_MARGIN_PER_SAT_YR_MM: Final[str] = "Starshield: margin per sat-yr ($mm)"
STARSHIP: Final[str] = "Starship"
STARSHIP_KG_EXPENDABLE_SHIP: Final[str] = "Starship $/kg, expendable ship"
STARSHIP_KG_FULLY_EXPENDABLE: Final[str] = "Starship $/kg, fully expendable"
STARSHIP_KG_FULLY_REUSABLE: Final[str] = "Starship $/kg, fully reusable"
STARSHIP_2ND_STAGE_MANUFACTURING_COST_MM_UNIT_BASE: Final[str] = "Starship 2nd-stage manufacturing cost ($mm/unit, base)"
STARSHIP_BOOSTER_CADENCE_PER_VEHICLE_IN_SERVICE: Final[str] = "Starship BOOSTER cadence per vehicle in service"
STARSHIP_F9_INHERITED_EXPERIENCE_SEED_F9_EQUIV_CUM_STACKS_AT_2025_ENTRY: Final[str] = "Starship F9-inherited experience seed (F9-equiv cum stacks at 2025 entry)"
STARSHIP_R_D_TOTAL_MM_YR_YEAR_ROW: Final[str] = "Starship R&D total ($mm/yr): year-row"
STARSHIP_SHIP_CADENCE_PER_VEHICLE_IN_SERVICE: Final[str] = "Starship SHIP cadence per vehicle in service"
STARSHIP_SPOT_IRR_COMPETES_IN_THE_IRR_WEIGHTED_ALLOCATION: Final[str] = "Starship Spot IRR (competes in the IRR-weighted allocation)"
STARSHIP_AMORTIZED_MFG_PER_LAUNCH_FULLY_REUSABLE_MM: Final[str] = "Starship amortized mfg per launch, fully reusable ($mm)"
STARSHIP_AT_COST_RATE_PER_LAUNCH_MM: Final[str] = "Starship at-cost rate per launch ($mm)"
STARSHIP_AT_COST_RATE_EXPENDABLE_SHIP_REUSABLE_BOOSTER_MM_LAUNCH: Final[str] = "Starship at-cost rate, expendable ship / reusable booster ($mm/launch)"
STARSHIP_AT_COST_RATE_FULLY_EXPENDABLE_MM_LAUNCH: Final[str] = "Starship at-cost rate, fully expendable ($mm/launch)"
STARSHIP_AT_COST_RATE_FULLY_REUSABLE_MM_LAUNCH: Final[str] = "Starship at-cost rate, fully reusable ($mm/launch)"
STARSHIP_BOOSTER_CADENCE_FOR_PRE_BUILD_SIZING_FLIGHTS_YR: Final[str] = "Starship booster cadence for pre-build sizing (flights/yr)"
STARSHIP_BOOSTER_REFURB_COST_ANCHOR_MM_FLIGHT_2024_BASELINE: Final[str] = "Starship booster refurb cost anchor ($mm/flight, 2024 baseline)"
STARSHIP_BOOSTER_REFURB_PER_FLIGHT_MM: Final[str] = "Starship booster refurb per flight ($mm)"
STARSHIP_BOOSTER_SHARE_OF_MANUFACTURING_COST_OF_STACK_MFG: Final[str] = "Starship booster share of manufacturing cost (% of stack mfg)"
STARSHIP_BUILD_COST_MM_STACK: Final[str] = "Starship build cost ($mm/stack)"
STARSHIP_BUILD_CAPACITY_CEILING_SHIPS_YR: Final[str] = "Starship build-capacity ceiling (ships/yr)"
STARSHIP_CADENCE_PER_VEHICLE_FLIGHTS_YR: Final[str] = "Starship cadence per vehicle (flights/yr)"
STARSHIP_COMMERCIAL_LAUNCHES: Final[str] = "Starship commercial launches"
STARSHIP_COMMERCIAL_READINESS_FACTOR: Final[str] = "Starship commercial-readiness factor"
STARSHIP_COMMERCIAL_READINESS_FACTOR_YEAR_ROW: Final[str] = "Starship commercial-readiness factor: year-row"
STARSHIP_COST_WL_ANCHOR_CUM_UNITS_CUM_STACKS_AT_END_2024_BASELINE: Final[str] = "Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)"
STARSHIP_CUM_UPMASS_WRIGHT_S_ANCHOR_KG: Final[str] = "Starship cum-upmass Wright's anchor (kg)"
STARSHIP_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH: Final[str] = "Starship customer launch price ($mm/launch)"
STARSHIP_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH_YEAR_ROW: Final[str] = "Starship customer launch price ($mm/launch): year-row"
STARSHIP_CUSTOMER_LAUNCHES_PER_YEAR: Final[str] = "Starship customer launches per year"
STARSHIP_FACILITY_CAPACITY_SHIPS_YR_PER_GIGABAY: Final[str] = "Starship facility capacity (ships/yr per Gigabay)"
STARSHIP_FACILITY_COST_PER_GIGABAY_INCREMENT_MM: Final[str] = "Starship facility cost per Gigabay increment ($mm)"
STARSHIP_FACILITY_USEFUL_LIFE_YEARS: Final[str] = "Starship facility useful life (years)"
STARSHIP_INTERNAL_LAUNCHES_PER_YEAR_STARLINK_DRIVEN: Final[str] = "Starship internal launches per year (Starlink-driven)"
STARSHIP_LAUNCHES_PER_PAD_PER_YEAR: Final[str] = "Starship launches per pad per year"
STARSHIP_LAUNCHES_PER_YEAR: Final[str] = "Starship launches per year"
STARSHIP_LAUNCHES_PER_YEAR_LUNAR_MARS: Final[str] = "Starship launches per year (Lunar/Mars)"
STARSHIP_LAUNCHES_PER_YEAR_ODC_DRIVEN: Final[str] = "Starship launches per year (ODC-driven)"
STARSHIP_MANUFACTURING_WL_LEARNING_RATE_REDUCTION_PER_DOUBLING_CUM_STACKS: Final[str] = "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)"
STARSHIP_MANUFACTURING_COST_ANCHOR_MM_STACK_2024_BASELINE: Final[str] = "Starship manufacturing cost anchor ($mm/stack, 2024 baseline)"
STARSHIP_MANUFACTURING_COST_PER_STACK_MM: Final[str] = "Starship manufacturing cost per stack ($mm)"
STARSHIP_OPERATIONAL_YEAR: Final[str] = "Starship operational year"
STARSHIP_OPS_FUEL_COST_ANCHOR_MM_LAUNCH_2024_BASELINE: Final[str] = "Starship ops + fuel cost anchor ($mm/launch, 2024 baseline)"
STARSHIP_OPS_FUEL_PER_LAUNCH_MM: Final[str] = "Starship ops + fuel per launch ($mm)"
STARSHIP_OPS_REFURB_WL_LEARNING_RATE_REDUCTION_PER_DOUBLING_CUM_STACKS: Final[str] = "Starship ops/refurb WL learning rate (% reduction per doubling cum stacks)"
STARSHIP_OWNED_VEHICLE_D_A_MM: Final[str] = "Starship owned-vehicle D&A ($mm)"
STARSHIP_OWNED_VEHICLE_D_A_PER_LAUNCH_MM_INTERFACE_TO_STARLINK: Final[str] = "Starship owned-vehicle D&A per launch ($mm)      ◄ interface to Starlink"
STARSHIP_OWNED_VEHICLE_BUILD_CAPEX: Final[str] = "Starship owned-vehicle build CapEx"
STARSHIP_OWNED_VEHICLE_BUILD_CAPEX_MM_ALLOCATOR_OUT: Final[str] = "Starship owned-vehicle build CapEx ($mm)   ◄ Allocator OUT"
STARSHIP_PAYLOAD_FOR_PRE_BUILD_SIZING_KG: Final[str] = "Starship payload for pre-build sizing (kg)"
STARSHIP_PAYLOAD_MAX_CAP_KG_TO_LEO_FULLY_REUSABLE: Final[str] = "Starship payload max cap (kg-to-LEO, fully reusable)"
STARSHIP_PAYLOAD_PER_LAUNCH_KG: Final[str] = "Starship payload per launch (kg)"
STARSHIP_PAYLOAD_RAMP_2030_ANCHOR_KG_TO_LEO_FULLY_REUSABLE: Final[str] = "Starship payload ramp 2030 anchor (kg-to-LEO, fully reusable)"
STARSHIP_PAYLOAD_RAMP_PLATEAU_YEAR: Final[str] = "Starship payload ramp plateau year"
STARSHIP_PAYLOAD_EXPENDABLE_SHIP_KG: Final[str] = "Starship payload, expendable ship (kg)"
STARSHIP_PAYLOAD_FULLY_EXPENDABLE_KG: Final[str] = "Starship payload, fully expendable (kg)"
STARSHIP_PAYLOAD_FULLY_REUSABLE_KG: Final[str] = "Starship payload, fully reusable (kg)"
STARSHIP_PRE_BUILD_BUFFER_MULTIPLE_X: Final[str] = "Starship pre-build buffer multiple (x)"
STARSHIP_PRE_BUILD_TARGET_PLANNED_NEXT_YR_UPMASS_KG: Final[str] = "Starship pre-build target: planned next-yr upmass (kg)"
STARSHIP_SATS_PER_LAUNCH_V3_PACKING_RETIRED_SUPERSEDED_BY_MASS_DERIVED_SATS_LAUNCH_STARLINK_R205: Final[str] = "Starship sats per launch (V3 packing): RETIRED — superseded by mass-derived sats/launch (Starlink R205)"
STARSHIP_SATS_PER_LAUNCH_V3_MASS_DERIVED: Final[str] = "Starship sats per launch (V3, mass-derived)"
STARSHIP_SHIP_REFURB_COST_ANCHOR_MM_FLIGHT_2024_BASELINE: Final[str] = "Starship ship refurb cost anchor ($mm/flight, 2024 baseline)"
STARSHIP_SHIP_REFURB_PER_FLIGHT_MM: Final[str] = "Starship ship refurb per flight ($mm)"
STARSHIP_SHIP_REUSE_LIFE_FLIGHTS_PER_SHIP: Final[str] = "Starship ship reuse life (flights per ship)"
STARSHIP_TARGET_LAUNCHES_INTERNAL_COMMERCIAL_DEMAND: Final[str] = "Starship target launches (internal + commercial demand)"
STARSHIP_TOTAL_CAPACITY_LAUNCHES_YR: Final[str] = "Starship total capacity (launches/yr)"
STARSHIP_VARIABLE_COST_PER_LAUNCH_MM_LAUNCH: Final[str] = "Starship variable cost per launch ($mm/launch)"
STARSHIP_VEHICLE_BUILD_COST_MM: Final[str] = "Starship vehicle build cost ($mm)"
STARSHIP_VEHICLE_FLEET_EOY: Final[str] = "Starship vehicle fleet EoY"
STARSHIP_VEHICLE_LIFE_L_YEARS: Final[str] = "Starship vehicle life L (years)"
STARSHIP_VEHICLES_BUILT_YR: Final[str] = "Starship vehicles built (yr)"
STARSHIP_CAPEX_SLUG_PER_VEHICLE_MM: Final[str] = "Starship: CapEx slug per vehicle ($mm)"
STARSHIP_MARGIN_PER_VEHICLE_PER_YR_MM_EX_D_A: Final[str] = "Starship: margin per vehicle per yr ($mm, ex-D&A)"
STARSHIP_REVENUE_PER_VEHICLE_PER_YR_MM: Final[str] = "Starship: revenue per vehicle per yr ($mm)"
STARTING_BOY_2025_SUBSCRIBERS_MILLIONS: Final[str] = "Starting BoY 2025 subscribers (millions)"
STARTING_CASH_POSITION_EOY_2024_MM: Final[str] = "Starting cash position EoY 2024 ($mm)"
STRUCTURE_SAT: Final[str] = "Structure $/sat"
SUBSYSTEM_COST_PRE_WL_SAT: Final[str] = "Subsystem cost pre-WL ($/sat)"
SUBSYSTEM_COST_W_WL_SAT: Final[str] = "Subsystem cost w/ WL ($/sat)"
SUBTOTAL_AI_COMPUTE_REVENUE_MM: Final[str] = "Subtotal: AI - Compute Revenue ($mm)"
SUBTOTAL_CUSTOMER_LAUNCH_REVENUE_MM: Final[str] = "Subtotal: Customer Launch Revenue ($mm)"
SUBTOTAL_LUNAR_MARS_REVENUE_MM: Final[str] = "Subtotal: Lunar - Mars Revenue ($mm)"
SUBTOTAL_STARLINK_REVENUE_MM: Final[str] = "Subtotal: Starlink Revenue ($mm)"
TOTAL_KG_DEMAND: Final[str] = "TOTAL KG DEMAND"
TAX_RATE_CORPORATE_US_FEDERAL_STATE_BLENDED: Final[str] = "Tax rate (corporate, US federal + state blended)"
TAXES_MM: Final[str] = "Taxes ($mm)"
TERAFAB_CAPEX_TO_FUND_MM: Final[str] = "Terafab CapEx to fund ($mm)"
TERAFAB_R_D_OF_CHIP_SUPPLY_GLIDE: Final[str] = "Terafab R&D % of chip-supply (glide)"
TERAFAB_R_D_CAGR: Final[str] = "Terafab R&D CAGR"
TERAFAB_R_D_FLOOR_PCT: Final[str] = "Terafab R&D floor pct"
TERAFAB_R_D_START_PCT: Final[str] = "Terafab R&D start pct"
TERAFAB_CAPACITY_PER_FAB_PHASE_WSPM_PHASE: Final[str] = "Terafab capacity per fab phase (wspm/phase)"
TERAFAB_CHIP_SUPPLY_R_D_MM_ROLL_UP_R_D: Final[str] = "Terafab chip-supply R&D ($mm) → roll-up R&D"
TERAFAB_FAB_CAPEX_BLENDED_ALL_IN_WSPM: Final[str] = "Terafab fab CapEx (blended all-in $/wspm)"
TERAFAB_FAB_CONSTRUCTION_WINDOW_YEARS: Final[str] = "Terafab fab construction window (years)"
TERAFAB_FAB_USEFUL_LIFE_DEPRECIATION_YEARS: Final[str] = "Terafab fab useful life (depreciation, years)"
TERAFAB_FACILITY_CAP_MM: Final[str] = "Terafab facility cap ($mm)"
TERAFAB_FACILITY_DRAW_WINDOW_END_YEAR: Final[str] = "Terafab facility draw-window end year"
TERAFAB_FACILITY_INTEREST_RATE_ANNUAL: Final[str] = "Terafab facility interest rate (annual)"
TERAFAB_FACILITY_REPAID_BY_YEAR: Final[str] = "Terafab facility repaid-by year"
TERAFAB_GOOD_CHIPS_PER_WSPM_PER_YR: Final[str] = "Terafab good chips per wspm per yr"
TERAFAB_PRODUCTION_COST_FRAC_CHIP_AT_COST_DC_CAPEX: Final[str] = "Terafab production cost frac (chip at-cost, → DC CapEx)"
TERAFAB_TOGGLE_1_NVIDIA_PARITY_ON_0_BUY_NVIDIA_0_5_BLEND: Final[str] = "Terafab toggle (1=NVIDIA-parity ON, 0=buy NVIDIA, 0.5=blend)"
TERAFAB_SPACEX_COST_CAPACITY_SHARE_FRAC: Final[str] = "Terafab: SpaceX cost/capacity share (frac)"
TERMINAL_COGS_PER_UNIT: Final[str] = "Terminal COGS per unit ($)"
TERMINAL_FCF_AVERAGING_WINDOW_YEARS_PRE_2050: Final[str] = "Terminal FCF averaging window (years pre-2050)"
TERMINAL_FCF_AVG_WINDOW_YRS_5: Final[str] = "Terminal FCF avg window (yrs, =5)"
TERMINAL_FACILITY_D_A_MM_TOGGLE_STARLINK: Final[str] = "Terminal facility D&A ($mm) × toggle  ◄ Starlink"
TERMINAL_FACTORY_CAPEX_TOGGLE_1_ON_0_OFF: Final[str] = "Terminal factory CapEx toggle (1=on,0=off)"
TERMINAL_FACTORY_CAPACITY_KITS_YR_PER_INCREMENT: Final[str] = "Terminal factory capacity (kits/yr per increment)"
TERMINAL_FACTORY_COST_PER_CAPACITY_INCREMENT_MM: Final[str] = "Terminal factory cost per capacity increment ($mm)"
TERMINAL_FACTORY_USEFUL_LIFE_YEARS: Final[str] = "Terminal factory useful life (years)"
TERMINAL_GROWTH_G: Final[str] = "Terminal growth g"
TERMINAL_GROWTH_RATE_G_GROUP_MOST_MODULES: Final[str] = "Terminal growth rate g (group + most modules)"
TERMINAL_KITS_DEMANDED_THIS_YEAR_PLACEHOLDER_GBPS_GROWTH_SCALED: Final[str] = "Terminal kits demanded this year (placeholder: Gbps-growth scaled)"
TERMINAL_KITS_PER_NET_SUBSCRIBER_ADD: Final[str] = "Terminal kits per net subscriber add"
TERMINAL_REPLACEMENT_RATE_INSTALLED_YR: Final[str] = "Terminal replacement rate (% installed/yr)"
TERR_DEMAND_BUILDABLE_CAPEX_MM: Final[str] = "Terr demand-buildable CapEx ($mm)"
TERR_TARGET_MW_DEMAND_SHARE: Final[str] = "Terr target MW (demand-share)"
TERRESTRIAL_MW_BUILD: Final[str] = "Terrestrial $/MW build"
TERRESTRIAL_DC_ALLOCATED_CASH_MM_CAE_LEVEL_2_DRIVES_R93: Final[str] = "Terrestrial DC: allocated cash ($mm) ◄ CAE Level-2 [drives R93]"
TERRESTRIAL_FACILITY_COST_CAGR: Final[str] = "Terrestrial facility cost CAGR"
TERRESTRIAL_TRAINING_CAPEX_MM_PRIOR_YR_AI_REVENUE_A8_5: Final[str] = "Terrestrial training CapEx ($mm): % × prior-yr AI revenue (A8.5)"
TERRESTRIAL_TRAINING_D_A_MM_CUMULATIVE_LIFE_MIN_CAPPED_A8_5: Final[str] = "Terrestrial training D&A ($mm): cumulative ÷ life, MIN-capped (A8.5)"
TERRESTRIAL_TRAINING_CARVE_OUT_OF_PRIOR_YR_AI_REVENUE: Final[str] = "Terrestrial training carve-out (% of prior-yr AI revenue)"
THERMAL_SYSTEM_KG: Final[str] = "Thermal system $/kg"
TOP_DOWN_SANITY_EX_CHIP_FAB_TOTAL_CHIP_FAB_VS_S_1_2025_CAPEX: Final[str] = "Top-down sanity ex-chip-fab: (Total − chip-fab) vs S-1 2025 capex"
TOP_DOWN_SANITY_TOTAL_FACILITY_CAPEX_VS_S_1_2025_SPACEX_CAPEX_8_000M_MUST_BE_A_FRACTION: Final[str] = "Top-down sanity: Total facility CapEx vs S-1 2025 SpaceX capex $8,000M (must be a fraction)"
TOTAL_AI_STACK_TOKENS_T: Final[str] = "Total AI-stack tokens (T)"
TOTAL_BB_REVENUE_MM: Final[str] = "Total BB revenue ($mm)"
TOTAL_DC_COMPUTE_AVAILABLE_GPU_HRS: Final[str] = "Total DC compute available (GPU-hrs)"
TOTAL_DTC_REVENUE_MM: Final[str] = "Total DTC revenue ($mm)"
TOTAL_F9_LAUNCHES: Final[str] = "Total F9 launches"
TOTAL_MODULE_OPEX_MM: Final[str] = "Total Module OpEx ($mm)"
TOTAL_R_D_MM: Final[str] = "Total R&D ($mm)"
TOTAL_REVENUE_MM: Final[str] = "Total Revenue ($mm)"
TOTAL_STARSHIP_AIRFRAMES_BUILT_BOOSTER_SHIP: Final[str] = "Total Starship airframes built (booster + ship)"
TOTAL_STARSHIP_BUILD_CAPEX_MM: Final[str] = "Total Starship build CapEx ($mm)"
TOTAL_STARSHIP_LAUNCHES: Final[str] = "Total Starship launches"
TOTAL_COMPUTE_DEMAND_GPU_HRS: Final[str] = "Total compute demand (GPU-hrs)"
TOTAL_COMPUTE_GAP_GPU_HRS_A8_3: Final[str] = "Total compute gap (GPU-hrs): A8.3"
TOTAL_CORPORATE_OPEX_MM: Final[str] = "Total corporate OpEx ($mm)"
TOTAL_DESIRED_LAUNCH_KG: Final[str] = "Total desired launch kg"
TOTAL_DESIRED_SATS_PRE_CAP: Final[str] = "Total desired sats (pre-cap)"
TOTAL_DESIRED_UPMASS_KG_FLEET_CURRENT_YR_CASH_ALLOCATION_ENGINE: Final[str] = "Total desired upmass kg (fleet, current yr)  ◄ Cash Allocation Engine"
TOTAL_EXISTING_COMPUTE_GPU_HRS_A8_3: Final[str] = "Total existing compute (GPU-hrs): A8.3"
TOTAL_FACILITY_CAPEX_MM_SAT_MFG_LAUNCH_VEHICLE_TERMINAL_HQ: Final[str] = "Total facility CapEx ($mm) = sat-mfg + launch/vehicle + terminal + HQ"
TOTAL_FLEET_LAUNCH_CAPEX_MM_INDEPENDENT_ENGINE: Final[str] = "Total fleet launch CapEx ($mm): independent (engine)"
TOTAL_INTER_MODULE_ELIMINATIONS_MM: Final[str] = "Total inter-module eliminations ($mm)"
TOTAL_LAUNCH_CAPACITY_KG: Final[str] = "Total launch capacity (kg)"
TOTAL_LAUNCH_CAPACITY_START_OF_YEAR_STOCK_KG: Final[str] = "Total launch capacity: start-of-year stock (kg)"
TOTAL_LAUNCH_KG_DEMAND_YEAR_N_1_FLEET: Final[str] = "Total launch kg demand year N+1 (fleet)"
TOTAL_NEW_STARLINK_DEPLOYMENT_SATS_YR: Final[str] = "Total new Starlink deployment (sats/yr)"
TOTAL_REVENUE_MM_2: Final[str] = "Total revenue ($mm)"
TOTAL_SAT_DRY_MASS_KG_DERIVED: Final[str] = "Total sat dry mass (kg): derived"
TRAINING_CARVE_OUT_INPUT_A8_5: Final[str] = "Training carve-out % (= input): A8.5"
TWO_SIDED_RADIATOR_FACTOR: Final[str] = "Two-sided radiator factor"
UTILIZATION: Final[str] = "Utilization (%)"
V2_BB_GBPS: Final[str] = "V2 BB Gbps"
V2_BB_GBPS_PER_SAT: Final[str] = "V2 BB Gbps per sat"
V2_BB_SAT_MASS_KG: Final[str] = "V2 BB sat mass (kg)"
V2_BB_SHARE_OF_NEW_DEPLOYMENT_FRAC: Final[str] = "V2 BB share of new deployment (frac)"
V2_BB_CAPEX_SLUG_PER_SAT_MM: Final[str] = "V2 BB: CapEx slug per sat ($mm)"
V2_BB_SPOT_IRR: Final[str] = "V2 BB: Spot IRR"
V2_BB_MARGIN_PER_SAT_YR_MM: Final[str] = "V2 BB: margin per sat-yr ($mm)"
V2_DTC_ACTIVE_SATS: Final[str] = "V2 DTC active sats"
V2_DTC_ACTIVE_SATS_END_2025: Final[str] = "V2 DTC active sats end-2025"
V2_DTC_BASE_DEORBIT_END_YEAR: Final[str] = "V2 DTC base deorbit end year"
V2_DTC_BASE_DEORBIT_START_YEAR: Final[str] = "V2 DTC base deorbit start year"
V2_DTC_EFFECTIVE_GBPS: Final[str] = "V2 DTC effective Gbps"
V2_DTC_SAT_MASS_KG: Final[str] = "V2 DTC sat mass (kg)"
V2_DTC_SHARE_OF_NEW_DEPLOYMENT_FRAC: Final[str] = "V2 DTC share of new deployment (frac)"
V2_DTC_CAPEX_SLUG_PER_SAT_MM: Final[str] = "V2 DTC: CapEx slug per sat ($mm)"
V2_DTC_SPOT_IRR: Final[str] = "V2 DTC: Spot IRR"
V2_DTC_MARGIN_PER_SAT_YR_MM: Final[str] = "V2 DTC: margin per sat-yr ($mm)"
V2_MINI_BB_ACTIVE_SATS: Final[str] = "V2 Mini BB active sats"
V2_MINI_BB_BASE_DEORBIT_END_YEAR: Final[str] = "V2 Mini BB base deorbit end year"
V2_MINI_BB_BASE_DEORBIT_START_YEAR: Final[str] = "V2 Mini BB base deorbit start year"
V2_MINI_BB_SATS_END_2025: Final[str] = "V2 Mini BB sats end-2025"
V2_LAUNCH_WINDOW_ACTIVE_1_0: Final[str] = "V2 launch window active (1/0)"
V3_BB_GBPS: Final[str] = "V3 BB Gbps"
V3_BB_GBPS_PER_SAT: Final[str] = "V3 BB Gbps per sat"
V3_BB_ACTIVE_SATS_EOY: Final[str] = "V3 BB active sats EoY"
V3_BB_SAT_MASS_KG: Final[str] = "V3 BB sat mass (kg)"
V3_BB_SHARE_OF_NEW_DEPLOYMENT_FRAC: Final[str] = "V3 BB share of new deployment (frac)"
V3_BB_CAPEX_SLUG_PER_SAT_MM: Final[str] = "V3 BB: CapEx slug per sat ($mm)"
V3_BB_SPOT_IRR: Final[str] = "V3 BB: Spot IRR"
V3_BB_MARGIN_PER_SAT_YR_MM: Final[str] = "V3 BB: margin per sat-yr ($mm)"
V3_DTC_ACTIVE_SATS_EOY: Final[str] = "V3 DTC active sats EoY"
V3_DTC_EFFECTIVE_GBPS: Final[str] = "V3 DTC effective Gbps"
V3_DTC_SAT_MASS_KG: Final[str] = "V3 DTC sat mass (kg)"
V3_DTC_SHARE_OF_NEW_DEPLOYMENT_FRAC: Final[str] = "V3 DTC share of new deployment (frac)"
V3_DTC_CAPEX_SLUG_PER_SAT_MM: Final[str] = "V3 DTC: CapEx slug per sat ($mm)"
V3_DTC_SPOT_IRR: Final[str] = "V3 DTC: Spot IRR"
V3_DTC_MARGIN_PER_SAT_YR_MM: Final[str] = "V3 DTC: margin per sat-yr ($mm)"
V3_STARLINK_LAUNCH_TRIGGER_YEAR: Final[str] = "V3 Starlink launch trigger year"
V3_DEPLOYMENT_ACTIVE_1_0: Final[str] = "V3 deployment active (1/0)"
VALUATION: Final[str] = "VALUATION"
VEHICLE_PHYSICAL_PARAMETERS_F9_STARSHIP_PAYLOAD_CADENCE: Final[str] = "VEHICLE PHYSICAL PARAMETERS (F9 + Starship payload + cadence)"
VARIABLE_LAUNCH_COGS_MM: Final[str] = "Variable launch COGS ($mm)"
VARIABLE_LAUNCH_COST_F9_MM: Final[str] = "Variable launch cost: F9 ($mm)"
VARIABLE_LAUNCH_COST_STARSHIP_MM: Final[str] = "Variable launch cost: Starship ($mm)"
VEHICLE_BUILD_CAPEX_MM: Final[str] = "Vehicle Build CapEx ($mm)"
VEHICLE_BUILD_AT_COST_TRANSFER_REVENUE_MM_RETIRED_MODULES_OWN_LAUNCH_CAPEX: Final[str] = "Vehicle Build at-cost transfer revenue ($mm) — RETIRED (modules own launch CapEx)"
VEHICLE_BUILD_DEMAND_PULLED_STARSHIP_F9_LAUNCH_CAPACITY: Final[str] = "Vehicle Build: demand-pulled Starship + F9 launch capacity"
WACC_GROUP: Final[str] = "WACC (Group)"
WACC_G_1_OK_HALT_IF_0: Final[str] = "WACC>g (1=OK; HALT if 0)"
WL_LEARNING_RATE_TURNAROUND_VS_CUM_UPMASS_DOUBLING: Final[str] = "WL learning rate: turnaround vs cum upmass doubling"
WATER_FILL_RESIDUAL_MM: Final[str] = "Water-fill residual ($mm)"
WORKING_CAPITAL_PER_SAT_MM_SAT_WC_T0: Final[str] = "Working capital per sat ($mm/sat): ΔWC T0"
WORKING_CAPITAL_WC: Final[str] = "Working capital ΔWC"
WORKING_CAPITAL_WC_MM: Final[str] = "Working capital ΔWC ($mm)"
WORKING_CAPITAL_WC_MM_ALLOCATOR_OUT: Final[str] = "Working capital ΔWC ($mm)   ◄ Allocator OUT"
WRIGHT_S_LAW_ANCHOR_CUM_SATS: Final[str] = "Wright's Law anchor cum sats"
WRIGHT_S_LAW_FLOOR_PCT_OF_BASE_SUBSYSTEM_COST: Final[str] = "Wright's Law floor pct (of base subsystem cost)"
WRIGHT_S_LAW_MULTIPLIER: Final[str] = "Wright's Law multiplier"
YEAR: Final[str] = "YEAR"
YEAR_OFFSET: Final[str] = "Year offset"
SUPERSEDED_A8_7_ODC_POWER_DENSITY_ANCHOR_2025_KW_TON: Final[str] = "[SUPERSEDED A8.7] ODC power density anchor 2025 (kW/ton)"
SUPERSEDED_A8_7_ODC_POWER_DENSITY_TARGET_KW_TON: Final[str] = "[SUPERSEDED A8.7] ODC power density target (kW/ton)"
SUPERSEDED_A8_7_SAT_BASE_MASS_NON_THERMAL_KG: Final[str] = "[SUPERSEDED A8.7] Sat base mass (non-thermal) (kg)"
EXP_IRR_BB: Final[str] = "exp(β·IRR) BB"
EXP_IRR_DTC: Final[str] = "exp(β·IRR) DTC"
EXP_IRR_AI_COMPUTE: Final[str] = "exp(β·IRR): AI-Compute"
EXP_IRR_CUSTOMER_LAUNCH: Final[str] = "exp(β·IRR): Customer Launch"
EXP_IRR_ODC: Final[str] = "exp(β·IRR): ODC"
EXP_IRR_STARLINK: Final[str] = "exp(β·IRR): Starlink"
EXP_IRR_TERRESTRIAL: Final[str] = "exp(β·IRR): Terrestrial"
G_WACC: Final[str] = "g ＼ WACC →"
KG_BINDING_FLAG_1_CAPACITY_BINDS: Final[str] = "kg-binding flag (1=capacity binds)"
LESS_INTER_MODULE_ELIMINATIONS: Final[str] = "less inter-module eliminations"
EXP_IRR: Final[str] = "Σ exp(β·IRR)"
EXP_WITHIN_AI: Final[str] = "Σ exp: within-AI"
SPILLOVER_WEIGHT: Final[str] = "Σ spillover weight"
STANDALONE_ANALYST_ANCHORS_SL_AI_CL_AISTACK_L_M: Final[str] = "Σ standalone analyst anchors (SL+AI+CL+AIStack+L/M)"
D_A_CAPEX_CHECK_1_OK: Final[str] = "Σ-D&A ≤ Σ-CapEx check (1=OK)"
REDUNDANT_AI_APPS_TAM_M_SUBS: Final[str] = "⊘ REDUNDANT — AI Apps TAM (M subs)"
REDUNDANT_AI_APPS_ADOPTION_CEILING_OF_TAM: Final[str] = "⊘ REDUNDANT — AI Apps adoption ceiling (% of TAM)"
REDUNDANT_AI_APPS_ADOPTION_STEEPNESS_K: Final[str] = "⊘ REDUNDANT — AI Apps adoption steepness k"
REDUNDANT_AI_APPS_BLENDED_ARPU_SUB_YR: Final[str] = "⊘ REDUNDANT — AI Apps blended ARPU ($/sub/yr)"
REDUNDANT_AI_APPS_BLENDED_ARPU_CAGR_YR: Final[str] = "⊘ REDUNDANT — AI Apps blended ARPU CAGR (/yr)"
REDUNDANT_AI_APPS_BLENDED_TOKENS_PER_SUB_M_SUB_YR: Final[str] = "⊘ REDUNDANT — AI Apps blended tokens per sub (M/sub/yr)"
REDUNDANT_AI_APPS_SUBS_2025_SEED_M: Final[str] = "⊘ REDUNDANT — AI Apps subs 2025 seed (M)"
REDUNDANT_AI_APPS_TOKENS_PER_SUB_CAGR_YR: Final[str] = "⊘ REDUNDANT — AI Apps tokens-per-sub CAGR (/yr)"
REDUNDANT_AI_APPS_TOKENS_PER_SUB_GROWTH_CAP: Final[str] = "⊘ REDUNDANT — AI Apps tokens-per-sub growth cap (×)"
REDUNDANT_BLENDED_ARPU_SUPERSEDED_BY_5_BUCKET_BLOCK_ROWS_224_255: Final[str] = "⊘ REDUNDANT — blended ARPU (superseded by 5-bucket block, rows 224-255)"
REDUNDANT_BLENDED_TOKENS_SUB_SUPERSEDED_BY_5_BUCKET_BLOCK_ROWS_224_255: Final[str] = "⊘ REDUNDANT — blended tokens/sub (superseded by 5-bucket block, rows 224-255)"
L_2026_LAUNCH_PACING_CASH_RESERVE: Final[str] = "▸ 2026 LAUNCH PACING & CASH RESERVE"
ABSORPTIVE_CAPACITY_WATER_FILL_TOP_LEVEL_A_REFRESH_V4_102: Final[str] = "▸ ABSORPTIVE-CAPACITY WATER-FILL (top-level, A-refresh V4.102)"
AI_COMPUTE_OUT_CONTRACT: Final[str] = "▸ AI - COMPUTE OUT CONTRACT"
AI_COMPUTE_OUT_CONTRACT_EXTENDED: Final[str] = "▸ AI - COMPUTE OUT CONTRACT — extended"
AI_COMPUTE_MODULE: Final[str] = "▸ AI / COMPUTE MODULE"
AI_APPS_5_BUCKET_DEMAND_BUILD_REPLACES_BLENDED_R116_118: Final[str] = "▸ AI APPS: 5-BUCKET DEMAND BUILD (replaces blended R116-118)"
AI_APPS_PER_CUSTOMER_YEAR_SUB_LINE_3_L_3: Final[str] = "▸ AI APPS: per customer-year (sub-line 3, L=3)"
AI_SEGMENT_DATA: Final[str] = "▸ AI segment data"
AI_COMPUTE_SHARED_DRIVERS_DERIVED_ON_TAB_NO_DEMAND_CURVE: Final[str] = "▸ AI-COMPUTE SHARED DRIVERS (derived on-tab; no demand curve)"
AI_AI_APPS: Final[str] = "▸ AI: AI Apps"
AI_AI_APPS_CONSOLIDATED_A2_2: Final[str] = "▸ AI: AI Apps (consolidated, A2.2)"
AI_AI_APPS_5_BUCKET_DEMAND_BUILD: Final[str] = "▸ AI: AI Apps 5-bucket demand build"
AI_AI_APPS_DEMAND_UPLIFT_UN_FLATTEN_ARPU_TOKENS_SUB: Final[str] = "▸ AI: AI Apps demand uplift (un-flatten ARPU + tokens/sub)"
AI_COMPUTE_DEMAND_BASIS_A8_ENDOGENISATION: Final[str] = "▸ AI: COMPUTE DEMAND BASIS (A8 endogenisation)"
AI_ORBITAL_DC_OPS_COST_RATES: Final[str] = "▸ AI: Orbital DC ops cost rates"
AI_ORBITAL_DC_PHYSICAL_ANCHORS: Final[str] = "▸ AI: Orbital DC physical anchors"
AI_ORBITAL_DC_SUBSYSTEM_UNIT_COSTS: Final[str] = "▸ AI: Orbital DC subsystem unit costs"
AI_R_D_ATTRIBUTION_GLIDES: Final[str] = "▸ AI: R&D attribution glides"
AI_TERAFAB_JV_SPLIT_CALIBRATION_A4_1: Final[str] = "▸ AI: Terafab JV split + calibration (A4.1)"
AI_TERAFAB_CHIP_FAB_FACILITIES_BUILD_A4: Final[str] = "▸ AI: Terafab chip-fab (→ Facilities Build, A4)"
AI_TERAFAB_TOGGLE: Final[str] = "▸ AI: Terafab toggle"
AI_TERRESTRIAL_DC: Final[str] = "▸ AI: Terrestrial DC"
AI_CHIP_IMPROVEMENT_LIGHTWEIGHTING_CAGRS_A8_1: Final[str] = "▸ AI: chip improvement + lightweighting CAGRs (A8.1)"
AI_COMPUTE_DEMAND_CURVE_A8_3: Final[str] = "▸ AI: compute demand curve (A8.3)"
AI_EXOGENOUS_COST_CAGRS_CAM_PORT_MC: Final[str] = "▸ AI: exogenous cost CAGRs (CAM port, MC)"
AI_EXTERNAL_COMPUTE_DEMAND_A8_ENDOGENISATION: Final[str] = "▸ AI: external compute demand (A8 endogenisation)"
AI_MERCHANT_IAAS_SUPPLY_SHARE_LEVER: Final[str] = "▸ AI: merchant-IaaS supply-share lever"
AI_ORBITAL_SERVING_S_CURVE_TRAINING_CARVE_OUT_A8_5: Final[str] = "▸ AI: orbital serving S-curve + training carve-out (A8.5)"
AI_YEAR_ROW_INPUTS_CAM_G_AF_GROUP_D_AC: Final[str] = "▸ AI: year-row inputs (Cam G:AF → Group D:AC)"
ALLOCATOR_IN_CROSS_TAB_READS: Final[str] = "▸ ALLOCATOR IN (cross-tab reads)"
ALLOCATOR_OUT_CANONICAL_LABELS_RULE_12_SOURCES: Final[str] = "▸ ALLOCATOR OUT (canonical labels: Rule 12 sources)"
ALLOCATOR_ODC_CONSTRUCTION_FACILITY_DEBT_LAYER: Final[str] = "▸ ALLOCATOR: ODC Construction Facility (debt layer)"
ALLOCATOR_TERAFAB_CONSTRUCTION_FACILITY_DEBT_LAYER: Final[str] = "▸ ALLOCATOR: Terafab Construction Facility (debt layer)"
BB_DTC_MARKET_MIX: Final[str] = "▸ BB/DTC market mix"
BLOCK_A_ALLOCATOR_IN_CROSS_TAB_READS: Final[str] = "▸ BLOCK A: ALLOCATOR IN (cross-tab reads)"
BLOCK_B_LAUNCH_DEMAND_FLEET_BUILD: Final[str] = "▸ BLOCK B: LAUNCH DEMAND & FLEET BUILD"
BLOCK_C_REVENUE_EXTERNAL_ONLY: Final[str] = "▸ BLOCK C: REVENUE (external only)"
BLOCK_D_COGS_GROSS_PROFIT: Final[str] = "▸ BLOCK D: COGS → GROSS PROFIT"
BLOCK_E_MODULE_OPEX_R_D_MODULE_EBITDA_R_D_ABOVE_EBITDA_HARD_RULE_7: Final[str] = "▸ BLOCK E: MODULE OpEx + R&D → MODULE EBITDA (R&D ABOVE EBITDA, Hard Rule 7)"
BLOCK_F_EBITDA_EBIT_ONLY_D_A_BELOW_EBITDA: Final[str] = "▸ BLOCK F: EBITDA → EBIT (only D&A below EBITDA)"
BLOCK_G_CAPEX_MODULE_FCF: Final[str] = "▸ BLOCK G: CAPEX → MODULE FCF"
BLOCK_H_PER_VEHICLE_IRR_ENGINE_V4_CANONICAL_SPOT_ONLY: Final[str] = "▸ BLOCK H: PER-VEHICLE IRR ENGINE (v4 canonical, Spot only)"
BLOCK_I_ALLOCATOR_OUT_AMENDED_CANONICAL_LABELS: Final[str] = "▸ BLOCK I: ALLOCATOR OUT (amended canonical labels)"
BLOCK_J_CONSERVATION_MEMOS_VERIFICATION_ONLY_EXCL_SUMS: Final[str] = "▸ BLOCK J, CONSERVATION MEMOS (verification only, excl. sums)"
BV_ENGINE_SOTP_VALUATION_TRACK_OFF_P_L: Final[str] = "▸ BV ENGINE: SoTP / VALUATION TRACK (off-P&L)"
BANDWIDTH_FLOW_SUPERSEDED_BY_THE_AI_COMPUTE_SECTION_SEE_ORBITAL_COMPUTE_STARLINK_ELIMINATION: Final[str] = "▸ Bandwidth flow → superseded by the AI/Compute section; see orbital-compute↔Starlink elimination"
CAPACITY_PRIORITY_ALLOCATION: Final[str] = "▸ CAPACITY-PRIORITY ALLOCATION"
CAPEX_MM_2: Final[str] = "▸ CAPEX ($mm)"
CAPEX_MODULE_FCF: Final[str] = "▸ CAPEX → MODULE FCF"
CARVE_OUT_CASH_RECEIPT_TAKEN_OFF_THE_TOP_BEFORE_THE_IRR_ALLOCATION: Final[str] = "▸ CARVE-OUT CASH RECEIPT (taken off the top, before the IRR allocation)"
CARVE_OUT_IRR_RESPONSE_OPERATIVE_2030_ONWARD: Final[str] = "▸ CARVE-OUT IRR RESPONSE (operative 2030 onward)"
CARVE_OUT_LIVE_EVERY_YEAR: Final[str] = "▸ CARVE-OUT: LIVE every year"
CASH_EOY_LIVE_EVERY_YEAR_2025_EOY_FEEDS_2026_CASH_BOY_THE_CASH_SPINE: Final[str] = "▸ CASH EoY: LIVE every year; 2025 EoY feeds 2026 Cash BoY (the cash spine)"
CASH_POOL_LIVE_EVERY_YEAR_2025_STARTING_CASH_11_385M_20B_BRIDGE: Final[str] = "▸ CASH POOL: LIVE every year (2025 = starting cash $11,385M + $20B bridge)"
CHECKS_RULE_4_5_15: Final[str] = "▸ CHECKS (Rule 4/5/15)"
CHIP_FAB_FACILITY_ENGINE_TERAFAB: Final[str] = "▸ CHIP-FAB FACILITY ENGINE (Terafab)"
CHIP_FAB_INTEGRATION_A5_TERAFAB_R_D_BOUNDARY_TIE: Final[str] = "▸ CHIP-FAB INTEGRATION (A5): Terafab R&D + boundary tie"
COGS_MM_2: Final[str] = "▸ COGS ($mm)"
COGS_GROSS_PROFIT: Final[str] = "▸ COGS → GROSS PROFIT"
COMPARABLES_CROSS_CHECK_B: Final[str] = "▸ COMPARABLES CROSS-CHECK ($B)"
CONSERVATION: Final[str] = "▸ CONSERVATION"
CONSERVATION_INTRA_TAB_MUST_0_RULE_5_21: Final[str] = "▸ CONSERVATION (intra-tab; must = 0: Rule 5/21)"
CONSERVATION_CALIBRATION: Final[str] = "▸ CONSERVATION + CALIBRATION"
CONSERVATION_MEMOS: Final[str] = "▸ CONSERVATION MEMOS"
CONSTELLATION_BUILD_REAL_COHORTS_TOTAL_BANDWIDTH: Final[str] = "▸ CONSTELLATION BUILD (real cohorts → total bandwidth)"
CORPORATE_OPEX_MM: Final[str] = "▸ CORPORATE OpEx ($mm)"
CUSTOMER_LAUNCH_MODULE_SPACE_SEGMENT_2_STREAM_REVENUE_R_D_ABOVE_EBITDA: Final[str] = "▸ CUSTOMER LAUNCH: module = Space segment, 2-stream revenue, R&D above EBITDA"
CASH_ALLOCATION_ENGINE_INPUTS: Final[str] = "▸ Cash Allocation Engine inputs"
CASH_POOL_BOUNDARY_INPUTS: Final[str] = "▸ Cash pool boundary inputs"
COMPARABLES_ANCHORS_B: Final[str] = "▸ Comparables anchors ($B)"
CONSTELLATION_OPENING_BALANCES_MACH33_HISTORICAL_ANCHORS_HARD: Final[str] = "▸ Constellation opening balances (Mach33 historical anchors: hard)"
CORPORATE_FACILITIES_CAPEX_MM_YR: Final[str] = "▸ Corporate facilities CapEx ($mm/yr)"
CORPORATE_HISTORICAL_CAPITAL_BASE: Final[str] = "▸ Corporate historical capital base"
CORPORATE_USEFUL_LIVES: Final[str] = "▸ Corporate useful lives"
CURVE_EVALUATORS_YEAR_ROW_READ_BY_THE_STARLINK_MODULE: Final[str] = "▸ Curve evaluators (year-row, read by the Starlink module)"
CUSTOMER_LAUNCH_IRR_LIFE_CLAMPS: Final[str] = "▸ Customer Launch IRR life clamps"
D_A_MM_2: Final[str] = "▸ D&A ($mm)"
DEMAND_DRIVEN_FLEET_SIZING_FORWARD_DEMAND_PULL_NO_CIRCULAR_REFERENCE: Final[str] = "▸ DEMAND-DRIVEN FLEET SIZING (forward-demand pull, no circular reference)"
DIAGNOSTIC_2025_VS_Q4_25_ANCHORS_NARROW_GATE_NON_HALT: Final[str] = "▸ DIAGNOSTIC: 2025 vs Q4'25 anchors (narrow-gate, non-halt)"
DISCOUNT_FACTORS_1_1_WACC_YEAR_ASOF_0_BEFORE_ASOF: Final[str] = "▸ DISCOUNT FACTORS: 1/(1+WACC)^(year−asof); 0 before asof"
DUAL_TRACK_SUMMARY_GROUP_EV_BY_AS_OF_B: Final[str] = "▸ DUAL-TRACK SUMMARY: Group EV by as-of ($B)"
DEORBIT_PARAMETERS: Final[str] = "▸ Deorbit parameters"
DEPRECIATION_PARAMETERS: Final[str] = "▸ Depreciation parameters"
DUAL_REVENUE_MODEL: Final[str] = "▸ Dual revenue model"
EBIT_BY_SEGMENT_MM: Final[str] = "▸ EBIT: by segment ($mm)"
EBITDA_EBIT_R_D_IS_IN_MODULE_OPEX_ABOVE_ONLY_D_A_BELOW: Final[str] = "▸ EBITDA → EBIT (R&D is in Module OpEx above; only D&A below)"
EBITDA_BY_SEGMENT_MM: Final[str] = "▸ EBITDA: by segment ($mm)"
ECHOSTAR_SPECTRUM_RECLASSIFIED_AS_RECURRING_OPEX_LICENCE_FEE: Final[str] = "▸ EchoStar spectrum reclassified as recurring OpEx licence fee"
F9_LAUNCHES_FLOWN_COUNT_YR_LEGACY_WINDING_DOWN: Final[str] = "▸ F9 LAUNCHES FLOWN (count/yr) — legacy, winding down"
F9_LAUNCH_GLIDE_PATH_CUSTOMER_LAUNCH_IN_TO_VEHICLE_BUILD: Final[str] = "▸ F9 launch glide path (Customer Launch IN to Vehicle Build)"
FACILITIES_BASE_ANCHORS_2025_STANDING_CAPACITY_SANITY_DENOMINATOR: Final[str] = "▸ FACILITIES BASE ANCHORS (2025 standing capacity + sanity denominator)"
FACILITIES_BUILD_CAPACITY_STEP_FACILITY_CAPEX: Final[str] = "▸ FACILITIES BUILD: capacity-step facility CapEx"
FREE_CASH_FLOW_BY_SEGMENT_MM: Final[str] = "▸ FREE CASH FLOW: by segment ($mm)"
FALCON_9_PHYSICAL_COST_PARAMETERS: Final[str] = "▸ Falcon 9 physical + cost parameters"
GROSS_PROFIT_MM_2: Final[str] = "▸ GROSS PROFIT ($mm)"
HQ_FACILITY_CORPORATE_GROUP: Final[str] = "▸ HQ FACILITY (CORPORATE → GROUP)"
INPUTS_READ_FROM_ASSUMPTIONS: Final[str] = "▸ INPUTS READ FROM ASSUMPTIONS"
INTER_MODULE_ELIMINATIONS_RULE_21_0_IN_CURRENT_BUILD: Final[str] = "▸ INTER-MODULE ELIMINATIONS (Rule 21: $0 in current build)"
INTERFACE_ALIASES_LABEL_FIDELITY_FOR_DOWNSTREAM_TABS: Final[str] = "▸ INTERFACE ALIASES (label-fidelity for downstream tabs)"
INTERFACE_CONTRACT_EXPOSED_LABELS: Final[str] = "▸ INTERFACE CONTRACT (exposed labels)"
INTERNAL_LAUNCHES_RETAIL_FLEET_WORKING: Final[str] = "▸ INTERNAL LAUNCHES + RETAIL FLEET (working)"
IRR_DRIVEN_COHORT_ALLOCATION_PRIOR_YEAR_SPOT_IRR_WEIGHTS_PER_COHORT_AFFORDABILITY_BROADBAND_VS_DIRECT_TO_CELL: Final[str] = "▸ IRR-DRIVEN COHORT ALLOCATION: prior-year spot IRR weights per-cohort affordability (broadband vs direct-to-cell)"
IRR_WEIGHTED_ALLOCATION_PARAMETERS: Final[str] = "▸ IRR-weighted allocation parameters"
KG_RATIONING_GATE: Final[str] = "▸ KG-RATIONING GATE"
LAUNCH_CAPEX_ROLL_UP_BOOKS_NO_FCF: Final[str] = "▸ LAUNCH CAPEX ROLL-UP (books no FCF)"
LEVEL_2_WITHIN_AI_ODC_VS_TERRESTRIAL_SPLIT_A7: Final[str] = "▸ LEVEL-2: WITHIN-AI ODC vs TERRESTRIAL SPLIT (A7)"
LUNAR_MISSION_DEPLOYMENT_FIRST_MISSION_YEAR_GATED: Final[str] = "▸ LUNAR MISSION DEPLOYMENT (first-mission-year gated)"
LUNAR_MARS_BRIDGE_GROUP_FCF_RECON_MEMO_AS_OF_2026: Final[str] = "▸ LUNAR/MARS BRIDGE & GROUP-FCF RECON (memo, as-of 2026)"
LUNAR_MARS_REPORTED_P_L: Final[str] = "▸ LUNAR–MARS REPORTED P&L"
LABOUR_UNIT_SHARED_PARAMETERS_OPTIMUS_CLASS_PROXY: Final[str] = "▸ Labour unit shared parameters (Optimus-class proxy)"
LUNAR_MARS_SHARE_OF_CARVE_OUT_CASH_DERIVED_DEPLOYMENT: Final[str] = "▸ Lunar / Mars share of carve-out cash (derived deployment)"
LUNAR_SPECIFIC: Final[str] = "▸ Lunar-specific"
LUNAR_MARS_STRATEGIC_CARVE_OUT_MONTE_CARLO_VARIABLE: Final[str] = "▸ Lunar/Mars strategic carve-out (Monte Carlo variable)"
MARS_MISSION_DEPLOYMENT_FIRST_MISSION_YEAR_GATED: Final[str] = "▸ MARS MISSION DEPLOYMENT (first-mission-year gated)"
MEMO_DIAGNOSTICS: Final[str] = "▸ MEMO / DIAGNOSTICS"
MISSING_CAPEX_BUCKETS_PRIOR_YEAR_DRIVEN_2025_CURRENT_YEAR_ANCHOR: Final[str] = "▸ MISSING-CAPEX BUCKETS (prior-year-driven; 2025 = current-year anchor)"
MISSING_CAPEX_PROGRAMS: Final[str] = "▸ MISSING-CAPEX PROGRAMS"
MODULE_FCF_DCF_INPUTS_DIRECT_FROM_GROUP_P_L_MM: Final[str] = "▸ MODULE FCF: DCF inputs (direct from Group P&L, $mm)"
MODULE_OPEX_2: Final[str] = "▸ MODULE OpEx"
MODULE_OPEX_DIRECT_MM: Final[str] = "▸ MODULE OpEx: direct ($mm)"
MODULE_ROLL_UP_CONSOLIDATED_EXTERNAL_REV_ONLY_INTERNAL_COMPUTE_TRANSFER_ELIMINATED_TERAFAB_OFF_TAB_A4_A5: Final[str] = "▸ MODULE ROLL-UP (consolidated; external rev only; internal compute transfer eliminated; Terafab off-tab → A4/A5)"
MODULE_SHARE_OF_STARSHIP_LAUNCHES: Final[str] = "▸ MODULE SHARE OF STARSHIP LAUNCHES (%)"
MODULE_SOTP_EBITDA_MULTIPLE_TERMINAL_MM: Final[str] = "▸ MODULE SoTP: EBITDA-MULTIPLE terminal, $mm"
MODULE_SOTP_EXIT_MULTIPLE_TERMINAL_MM: Final[str] = "▸ MODULE SoTP: EXIT-MULTIPLE terminal, $mm"
MODULE_SOTP_GORDON_PERPETUITY_GROWTH_TERMINAL_MM: Final[str] = "▸ MODULE SoTP: GORDON (perpetuity-growth) terminal, $mm"
MARS_SPECIFIC: Final[str] = "▸ Mars-specific"
MODULE_WIDE_PARAMETERS: Final[str] = "▸ Module-wide parameters"
NEW_S_1_DERIVED_INPUTS: Final[str] = "▸ NEW S-1 derived inputs"
NEW_STARLINK_ROWS_FROM_S_1_DISCLOSURES: Final[str] = "▸ NEW Starlink rows from S-1 disclosures"
ODC_CONSTRUCTION_FACILITY_DEBT_LAYER_FUNDS_ODC_SAT_ROLLOUT: Final[str] = "▸ ODC CONSTRUCTION FACILITY (debt layer — funds ODC sat rollout)"
ORBITAL_DC_PER_COMPUTE_SAT_YEAR_SUB_LINE_1_L_5: Final[str] = "▸ ORBITAL DC: per compute sat-year (sub-line 1, L=5)"
OPEX_CALIBRATION_TARGETS: Final[str] = "▸ OpEx calibration targets"
PER_SAT_IRR_ENGINE_V4_CANONICAL_PER_COHORT_ONE_COST_BASE: Final[str] = "▸ PER-SAT IRR ENGINE (v4 canonical): per cohort, one cost base"
PER_SHIP_COST_BUILD: Final[str] = "▸ PER-SHIP COST BUILD"
PER_MODULE_ASSET_LIFE_L_CANONICAL_IRR_FORMULA_INPUT: Final[str] = "▸ Per-module asset life L (canonical IRR formula input)"
QUEUE_GATE_LIVE_EVERY_YEAR: Final[str] = "▸ QUEUE GATE: LIVE every year"
R_D_MM: Final[str] = "▸ R&D ($mm)"
R_D_ATTRIBUTION_RULES: Final[str] = "▸ R&D attribution rules"
R_D_LUNAR_MARS_PROFILE_YEAR_ROW_PRE_REVENUE: Final[str] = "▸ R&D: Lunar/Mars ($-profile year-row, pre-revenue)"
REVENUE_2: Final[str] = "▸ REVENUE"
REVENUE_MM_2: Final[str] = "▸ REVENUE ($mm)"
REVENUE_SEGMENT_SUB_LINES_MM: Final[str] = "▸ REVENUE — SEGMENT SUB-LINES ($mm)"
S_1_NEW_CAPEX_CALIBRATION_TARGETS: Final[str] = "▸ S-1 NEW CapEx calibration targets"
S_1_DERIVED_VALUATION_TRIANGULATION_MEMOS: Final[str] = "▸ S-1 derived valuation triangulation memos"
SATELLITE_MFG_FACILITY_ENGINE_REDMOND: Final[str] = "▸ SATELLITE-MFG FACILITY ENGINE (Redmond)"
SEGMENT_MIX_OF_GROUP_REVENUE: Final[str] = "▸ SEGMENT MIX — % OF GROUP REVENUE"
SENSITIVITY_GROUP_EV_AS_OF_2026_GORDON_B: Final[str] = "▸ SENSITIVITY: Group EV as-of 2026, GORDON ($B)"
SG_A_BY_FUNCTION_GROUP_LEVEL: Final[str] = "▸ SG&A by function (Group-level)"
STARFACTORY_INITIAL_PRODUCTION_FACILITY_BASE_CAPACITY_ONE_TIME: Final[str] = "▸ STARFACTORY: initial production facility (base capacity, one-time)"
STARLINK_MODULE: Final[str] = "▸ STARLINK MODULE"
STARLINK_REAL_COHORTS_DTC_EFFECTIVE_LEVER: Final[str] = "▸ STARLINK: real cohorts + DTC effective lever"
STARSHIP_LAUNCHES_FLOWN_COUNT_YR: Final[str] = "▸ STARSHIP LAUNCHES FLOWN (count/yr)"
STARSHIP_PRODUCTION_FACILITY_STARFACTORY_GIGABAY_CAPACITY_SCALING: Final[str] = "▸ STARSHIP PRODUCTION FACILITY (Starfactory/Gigabay): capacity + scaling"
SUB_SEGMENT_MIX_OF_OWN_SEGMENT_REVENUE: Final[str] = "▸ SUB-SEGMENT MIX — % OF OWN SEGMENT REVENUE"
SUBSCRIBERS_HARDWARE: Final[str] = "▸ SUBSCRIBERS + HARDWARE"
SATELLITE_PHYSICAL: Final[str] = "▸ Satellite physical"
SHARED_UNATTRIBUTABLE_CORPORATE_R_D_GROUP_RESIDUAL: Final[str] = "▸ Shared / unattributable corporate R&D (Group, residual)"
SOTP_EV_EBITDA_MULTIPLES_TERMINAL_AT_HORIZON: Final[str] = "▸ SoTP EV/EBITDA multiples (terminal, at horizon)"
SOTP_TERMINAL_MEMO: Final[str] = "▸ SoTP TERMINAL MEMO"
SOTP_MULTIPLES_EV_REVENUE_AT_2050: Final[str] = "▸ SoTP multiples (EV/Revenue at 2050)"
STARLINK_R_D_ATTRIBUTION_RULE: Final[str] = "▸ Starlink R&D attribution rule"
STARSHIELD: Final[str] = "▸ Starshield"
STARSHIP_R_D_TOTAL_MM_YR_SPLITS_ACROSS_MODULES_BY_LAUNCH_SHARE: Final[str] = "▸ Starship R&D total ($mm/yr): splits across modules by launch share"
STARSHIP_CADENCE_WRIGHT_S_LAW_ON_CUM_UPMASS: Final[str] = "▸ Starship cadence (Wright's Law on cum upmass)"
STARSHIP_TIME_VARYING_INPUTS_YEAR_ROWS: Final[str] = "▸ Starship time-varying inputs (year-rows)"
STARSHIP_VEHICLE_PHYSICAL_COST_PARAMETERS: Final[str] = "▸ Starship vehicle physical + cost parameters"
SUBSCRIBERS_ARPU_TERMINALS_BIG_S_1_IMPACTS: Final[str] = "▸ Subscribers + ARPU + Terminals (BIG S-1 IMPACTS)"
TAXES_NOPAT_MM: Final[str] = "▸ TAXES & NOPAT ($mm)"
TERAFAB_CONSTRUCTION_FACILITY_DEBT_LAYER: Final[str] = "▸ TERAFAB CONSTRUCTION FACILITY (debt layer)"
TERMINAL_VALUE_2040_BOTH_METHODS_MM: Final[str] = "▸ TERMINAL VALUE @2040 (both methods, $mm)"
TERMINALS_BASTROP_TOGGLE_GATED: Final[str] = "▸ TERMINALS (Bastrop): toggle-gated"
TERRESTRIAL_DC_PER_MW_YEAR_SUB_LINE_2_L_15: Final[str] = "▸ TERRESTRIAL DC: per MW-year (sub-line 2, L=15)"
TIE_OUT_CHECKS_MUST_0_WITHIN_1MM: Final[str] = "▸ TIE-OUT CHECKS (must = 0 within $1mm)"
TOP_LEVEL_IRR_WEIGHTED_ALLOCATION_ALLOCATED_CASH_0_IN_THE_2025_ANCHOR_YEAR_OPERATIVE_2026_2050_SHARES_SUM_TO_1: Final[str] = "▸ TOP-LEVEL IRR-WEIGHTED ALLOCATION: allocated cash = 0 in the 2025 anchor year; operative 2026→2050 (shares sum to 1)"
TOTAL_LAUNCHES_ALL_VEHICLES_COUNT_YR: Final[str] = "▸ TOTAL LAUNCHES, ALL VEHICLES (count/yr)"
TRI_TRACK_SUMMARY_GROUP_EV_BY_AS_OF_B: Final[str] = "▸ TRI-TRACK SUMMARY: Group EV by as-of ($B)"
TERMINAL_VALUE_PARAMETERS: Final[str] = "▸ Terminal value parameters"
VEHICLE_BUILD_EXPOSURES_ADDED_2026_06_01_RESOLVE_VB_FLEET_PULLS_CANONICAL_UNIFORM_LABELS: Final[str] = "▸ VEHICLE BUILD EXPOSURES (added 2026-06-01: resolve VB fleet pulls; canonical uniform labels)"
VEHICLE_BUILD_STARSHIP_FLEET_WRIGHT_S_COST_CADENCE_FLEET_LEVEL_LAUNCH_LEARNING: Final[str] = "▸ VEHICLE BUILD: Starship fleet Wright's cost + cadence (fleet-level launch learning)"
VEHICLE_BUILD_CLAIM_DEMAND_PULLED_ONE_PERIOD_LAG: Final[str] = "▸ Vehicle build claim (demand-pulled, one-period lag)"
WACC_RISK_PREMIA: Final[str] = "▸ WACC + risk premia"
WACC_COMPONENT_MEMOS_NOT_USED_IN_FORMULAS: Final[str] = "▸ WACC component memos (not used in formulas)"
WRIGHT_S_LAW_PARAMETERS: Final[str] = "▸ Wright's Law parameters"
YEAR_ROW_COST_CURVES: Final[str] = "▸ Year-row cost curves"
A8_6_ODC_THERMAL_RECALIBRATION_KW_TON_GLIDE_DYNAMIC_TDP: Final[str] = "▸ §A8.6: ODC THERMAL RECALIBRATION (kW/ton glide + dynamic TDP)"
IRR_ALLOCATION_SOFT_FLOOR: Final[str] = "▸ §IRR allocation soft floor"

# V2.16 code-referenced labels — supersede in R1 module re-base
AI_STACK_R_D_CAGR_TAPER: Final[str] = "AI Stack R&D — CAGR (taper)"
AI_STACK_R_D_END_STATE_FLOOR: Final[str] = "AI Stack R&D — end-state % (floor)"
AI_STACK_R_D_PROFILE_MM_PRE_REVENUE_FLOOR: Final[str] = "AI Stack R&D $-profile ($mm, pre-revenue floor)"
AI_STACK_R_D_PROFILE_MM_YR_YEAR_ROW: Final[str] = "AI Stack R&D $-profile ($mm/yr) — year-row"
AI_STACK_R_D_START_OF_AI_STACK_REV: Final[str] = "AI Stack R&D — start % of AI Stack rev"
CORPORATE_IT_CAPEX_MM_YR_FLAT: Final[str] = "Corporate IT CapEx ($mm/yr, flat)"
CORPORATE_IT_USEFUL_LIFE_YEARS: Final[str] = "Corporate IT useful life (years)"
CUSTOMER_LAUNCH_CASH_DEMAND_LARGE_DEFAULT_MM: Final[str] = "Customer Launch cash demand large default ($mm)"
CUSTOMER_LAUNCH_REVENUE_TRAJECTORY_STUB_MM: Final[str] = "Customer Launch revenue trajectory stub ($mm)"
ECHOSTAR_MID_BAND_CAPEX_MM_YEAR_ROW: Final[str] = "EchoStar mid-band CapEx ($mm) — year-row"
GENERAL_ENGINEERING_FACILITIES_CAPEX_MM_YR_FLAT: Final[str] = "General engineering facilities CapEx ($mm/yr, flat)"
GENERAL_ENGINEERING_FACILITIES_LIFE_YEARS: Final[str] = "General engineering facilities life (years)"
HQ_BUILDINGS_CAPEX_MM_YR_FLAT: Final[str] = "HQ buildings CapEx ($mm/yr, flat)"
HQ_BUILDINGS_USEFUL_LIFE_YEARS: Final[str] = "HQ buildings useful life (years)"
IMPAIRMENT_CHARGES_MM_YEAR_ROW: Final[str] = "Impairment charges ($mm/yr) — year-row"
LAUNCHES_PER_STARSHIP_VEHICLE_PER_YEAR_CADENCE_VARIANT_BLEND_USED_FOR_SIZING: Final[str] = "Launches per Starship vehicle per year (cadence × variant blend, used for sizing)"
MARS_MOON_R_D_MM_YR_YEAR_ROW: Final[str] = "Mars/Moon R&D ($mm/yr) — year-row"
ODC_CASH_DEMAND_LARGE_DEFAULT_MM: Final[str] = "ODC cash demand large default ($mm)"
ODC_KG_DEMAND_LARGE_DEFAULT_KG: Final[str] = "ODC kg demand large default (kg)"
ODC_R_D_CAGR_TAPER: Final[str] = "ODC R&D — CAGR (taper)"
ODC_R_D_END_STATE_FLOOR: Final[str] = "ODC R&D — end-state % (floor)"
ODC_R_D_PROFILE_MM_PRE_REVENUE_FLOOR: Final[str] = "ODC R&D $-profile ($mm, pre-revenue floor)"
ODC_R_D_PROFILE_MM_YR_YEAR_ROW: Final[str] = "ODC R&D $-profile ($mm/yr) — year-row"
ODC_R_D_START_OF_ODC_REV: Final[str] = "ODC R&D — start % of ODC rev"
OTHER_CORPORATE_CAPEX_MM_YR_FLAT: Final[str] = "Other corporate CapEx ($mm/yr, flat)"
OTHER_CORPORATE_USEFUL_LIFE_YEARS: Final[str] = "Other corporate useful life (years)"
PRE_IPO_BRIDGE_DRAWDOWN_YEAR: Final[str] = "Pre-IPO bridge year of drawdown"
PRE_IPO_DEBT_FACILITY_MM: Final[str] = "Pre-IPO debt facility ($mm)"
RESTRUCTURING_CHARGES_MM_YEAR_ROW: Final[str] = "Restructuring charges ($mm/yr) — year-row"
R_D_MOON_MARS_MM_YR_YEAR_ROW: Final[str] = "R&D — Moon/Mars ($mm/yr) — year-row"
SALES_MARKETING_START_OF_STARLINK_STARSHIELD_CUSTOMER_LAUNCH_EXT_REV: Final[str] = "Sales & Marketing — start % of (Starlink+Starshield+Customer Launch ext) rev"
SATELLITE_USEFUL_LIFE_V2_DTC_YEARS: Final[str] = "Satellite useful life — V2 Mini DTC (years)"
SATELLITE_USEFUL_LIFE_V3_DTC_YEARS: Final[str] = "Satellite useful life — V3 DTC (years)"
SHARE_BASED_COMPENSATION_MM_YEAR_ROW: Final[str] = "Share-based compensation ($mm/yr) — year-row"
SPECTRUM_USEFUL_LIFE_YEARS: Final[str] = "Spectrum useful life (years)"
STARSHIP_PAYLOAD_2025_BASELINE_KG_TO_LEO_FULLY_REUSABLE_MODE: Final[str] = "Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)"
V2_BB_FACILITY_CAPEX_PER_SAT_MM_SAT: Final[str] = "V2 BB facility CapEx per sat ($mm/sat)"
V2_BB_SAT_UNIT_COST_MM_SAT: Final[str] = "V2 BB sat unit cost ($mm/sat)"
V2_DTC_FACILITY_CAPEX_PER_SAT_MM_SAT: Final[str] = "V2 DTC facility CapEx per sat ($mm/sat)"
V2_DTC_SAT_UNIT_COST_MM_SAT: Final[str] = "V2 DTC sat unit cost ($mm/sat)"
V2_MINI_BB_SATS_LAUNCHED_2025: Final[str] = "V2 Mini BB Sats Launched 2025"
V2_MINI_DTC_SATS_LAUNCHED_2025: Final[str] = "V2 Mini DTC Sats Launched 2025"
V2_MINI_MASS_KG: Final[str] = "V2 Mini Mass (kg)"
V3_BB_FACILITY_CAPEX_PER_SAT_MM_SAT: Final[str] = "V3 BB facility CapEx per sat ($mm/sat)"
V3_BB_LAUNCHES_PER_YEAR_STUB_TRAJECTORY: Final[str] = "V3 BB launches per year stub trajectory"
V3_BB_SAT_UNIT_COST_MM_SAT: Final[str] = "V3 BB sat unit cost ($mm/sat)"
V3_DTC_FACILITY_CAPEX_PER_SAT_MM_SAT: Final[str] = "V3 DTC facility CapEx per sat ($mm/sat)"
V3_DTC_LAUNCHES_PER_YEAR_STUB_TRAJECTORY: Final[str] = "V3 DTC launches per year stub trajectory"
V3_DTC_SAT_UNIT_COST_MM_SAT: Final[str] = "V3 DTC sat unit cost ($mm/sat)"
V3_MASS_KG: Final[str] = "V3 Mass (kg)"
VEHICLE_BUILD_LEAD_TIME_YEARS: Final[str] = "Vehicle build lead time (years)"

# fmt: on

CANONICAL_LABELS: Final[frozenset[str]] = frozenset(
    {
        "(by module)",
        "(cols C:F = as-of)",
        "(retired)",
        "(retired: NBV reported as total on R115; output-BV memo on R76/R77)",
        "7 buckets: sat-mfg (Redmond), Starship-vehicle (Gigabay @100/yr), pads, engines, terminals (toggle-OFF), ground stations, HQ→Group. Exposes CapEx + D&A totals by label.",
        "ADCS+avionics $/sat",
        "AI - Compute",
        "AI - Compute — AI Apps (external)",
        "AI - Compute — Orbital DC (external)",
        "AI - Compute — Terrestrial DC (external)",
        "AI - Compute — total",
        "AI Apps CAC ($/customer)",
        "AI Apps GPU-hr per trillion tokens",
        "AI Apps attributed compute capital per sub ($)",
        "AI Apps revenue ($mm)",
        "AI Apps served (GPU-hrs, capped)",
        "AI Apps share of DC compute",
        "AI Apps subs (M)",
        "AI Apps tokens (T)",
        "AI Apps tokens-per-query intensity CAGR",
        "AI Apps: paying users (M)",
        "AI Apps: total revenue ($mm)",
        "AI Apps: total tokens (T)",
        "AI STACK — RETIRED, superseded by the AI/Compute section. Memos below retained.",
        "AI Stack R&D CAGR",
        "AI Stack R&D floor pct",
        "AI Stack R&D start pct",
        "AI Stack insurance pct rev",
        "AI Stack other COGS pct rev",
        "AI compute demand reference (M H100-eq GPU): seed-anchored S-curve (A8.5)",
        "AI compute demand-curve elasticity b",
        "AI orbital compute TAM ceiling (M H100-eq GPU)",
        "AI orbital compute adoption steepness k",
        "AI-Compute / ODC",
        "AI: ODC first compute-sat build year",
        "AIApps API: ARPU ($/acct/yr)",
        "AIApps API: ARPU CAGR (/yr)",
        "AIApps API: tokens/user 2025 (M/yr)",
        "AIApps API: tokens/user CAGR (/yr)",
        "AIApps API: user CAGR (/yr)",
        "AIApps API: users 2025 (M)",
        "AIApps Ads: ARPU ($/user/yr)",
        "AIApps Ads: ARPU CAGR (/yr)",
        "AIApps Agentic: ARPU ($/user/yr)",
        "AIApps Agentic: ARPU CAGR (/yr)",
        "AIApps Agentic: tokens/user 2025 (M/yr)",
        "AIApps Agentic: tokens/user CAGR (/yr)",
        "AIApps Agentic: user CAGR (/yr)",
        "AIApps Agentic: users 2025 (M)",
        "AIApps Ent: ARPU ($/seat/yr)",
        "AIApps Ent: ARPU CAGR (/yr)",
        "AIApps Ent: seats 2025 (M)",
        "AIApps Ent: tokens/user 2025 (M/yr)",
        "AIApps Ent: tokens/user CAGR (/yr)",
        "AIApps Ent: user CAGR (/yr)",
        "AIApps Free: ARPU ($/user/yr)",
        "AIApps Free: ARPU CAGR (/yr)",
        "AIApps Free: tokens/user 2025 (M/yr)",
        "AIApps Free: tokens/user CAGR (/yr)",
        "AIApps Free: user CAGR (/yr)",
        "AIApps Free: users 2025 (M)",
        "AIApps Indiv: ARPU ($/user/yr)",
        "AIApps Indiv: ARPU CAGR (/yr)",
        "AIApps Indiv: tokens/user 2025 (M/yr)",
        "AIApps Indiv: tokens/user CAGR (/yr)",
        "AIApps Indiv: user CAGR (/yr)",
        "AIApps Indiv: users 2025 (M)",
        "AIApps Merchant IaaS demand scale (×)",
        "ALL OK (R108-equivalent)",
        "ALLOCATOR",
        "Accrual↔cash FCF reconciliation",
        "Active retail sats (BB + DTC, EoY)",
        "Active sat fleet (EoY)",
        "Active-gen BB CapEx slug ($mm/sat)",
        "Active-gen BB Spot IRR (prior yr)",
        "Active-gen DTC CapEx slug ($mm/sat)",
        "Active-gen DTC Spot IRR (prior yr)",
        "Ads: ARPU ($/user/yr)",
        "Ads: monetizable base (M)",
        "Ads: revenue ($mm)",
        "Agentic coding: ARPU ($/user/yr)",
        "Agentic coding: revenue ($mm)",
        "Agentic coding: tokens (T)",
        "Agentic coding: tokens/user (M/yr)",
        "Agentic coding: users (M)",
        "Allocated cash to AI-Compute ($mm)",
        "Allocated cash to Customer Launch ($mm)",
        "Allocated cash to Starlink ($mm)",
        "Allocated cash → ODC ($mm)",
        "Allocated cash → Terrestrial ($mm)",
        "Allocated final: AI-Compute ($mm)",
        "Allocated final: Customer Launch ($mm)",
        "Allocated final: Starlink ($mm)",
        "Allocation share: AI-Compute",
        "Allocation share: Customer Launch",
        "Allocation share: Starlink",
        "Allocation share: orbital (ODC)",
        "Allocation share: terrestrial",
        "Allocation sharpness β (top-level 3-module blend)",
        "Allocation sharpness β: AI orbital / terrestrial sub-split",
        "Allocation sharpness β: Starlink broadband / direct-to-cell sub-split",
        "Allocation weight: broadband (V2 era = 1)",
        "Allocation weight: direct-to-cell",
        "Allocator min softmax share floor per module (frac)",
        "Annual TAM shift multiplier",
        "Annual escalator rate (derived, year-row)",
        "As-of valuation dates →",
        "Asset insurance COGS ($mm)",
        "Asset insurance COGS (% of revenue)",
        "Asset life L: AI Apps (yrs)",
        "Asset life L: AI/Compute AI Apps (years)",
        "Asset life L: AI/Compute Orbital DC (years)",
        "Asset life L: AI/Compute Terrestrial DC (years)",
        "Asset life L: Customer Launch F9 (years)",
        "Asset life L: Customer Launch Starship (years)",
        "Asset life L: Orbital DC (yrs)",
        "Asset life L: Terrestrial DC (yrs)",
        "Attributed R&D",
        "Attributed R&D ($mm)",
        "Attributed R&D ($mm)   ◄ Allocator OUT",
        "Attributed R&D ($mm): component of Module OpEx total (row 87)",
        "Attributed R&D: AI - Compute",
        "Attributed R&D: Customer Launch",
        "Attributed R&D: Customer Launch (Starship R&D lifted to Shared)",
        "Attributed R&D: Lunar - Mars",
        "Avg $/Gbps BB at Q (price-at-Q)",
        "Avg $/Gbps DTC at Q (price-at-Q)",
        "BB BANDWIDTH (Gbps by cohort)",
        "BB BoY subscribers (M)",
        "BB DEMAND CURVE (piecewise-linear Q→Revenue lookup)",
        "BB EoY subscribers (= revenue-implied level, M): stabilised",
        "BB FLEET (active sats by cohort)",
        "BB Gbps available for external Starlink revenue",
        "BB Q breakpoint #1 (Gbps)",
        "BB Q breakpoint #10 (Gbps)",
        "BB Q breakpoint #11 (Gbps)",
        "BB Q breakpoint #12 (Gbps)",
        "BB Q breakpoint #13 (Gbps)",
        "BB Q breakpoint #14 (Gbps)",
        "BB Q breakpoint #15 (Gbps)",
        "BB Q breakpoint #16 (Gbps)",
        "BB Q breakpoint #17 (Gbps)",
        "BB Q breakpoint #18 (Gbps)",
        "BB Q breakpoint #19 (Gbps)",
        "BB Q breakpoint #2 (Gbps)",
        "BB Q breakpoint #20 (Gbps)",
        "BB Q breakpoint #21 (Gbps)",
        "BB Q breakpoint #22 (Gbps)",
        "BB Q breakpoint #23 (Gbps)",
        "BB Q breakpoint #24 (Gbps)",
        "BB Q breakpoint #25 (Gbps)",
        "BB Q breakpoint #26 (Gbps)",
        "BB Q breakpoint #27 (Gbps)",
        "BB Q breakpoint #28 (Gbps)",
        "BB Q breakpoint #29 (Gbps)",
        "BB Q breakpoint #3 (Gbps)",
        "BB Q breakpoint #30 (Gbps)",
        "BB Q breakpoint #31 (Gbps)",
        "BB Q breakpoint #32 (Gbps)",
        "BB Q breakpoint #33 (Gbps)",
        "BB Q breakpoint #34 (Gbps)",
        "BB Q breakpoint #35 (Gbps)",
        "BB Q breakpoint #36 (Gbps)",
        "BB Q breakpoint #37 (Gbps)",
        "BB Q breakpoint #38 (Gbps)",
        "BB Q breakpoint #39 (Gbps)",
        "BB Q breakpoint #4 (Gbps)",
        "BB Q breakpoint #40 (Gbps)",
        "BB Q breakpoint #41 (Gbps)",
        "BB Q breakpoint #42 (Gbps)",
        "BB Q breakpoint #43 (Gbps)",
        "BB Q breakpoint #44 (Gbps)",
        "BB Q breakpoint #45 (Gbps)",
        "BB Q breakpoint #46 (Gbps)",
        "BB Q breakpoint #47 (Gbps)",
        "BB Q breakpoint #48 (Gbps)",
        "BB Q breakpoint #49 (Gbps)",
        "BB Q breakpoint #5 (Gbps)",
        "BB Q breakpoint #50 (Gbps)",
        "BB Q breakpoint #51 (Gbps)",
        "BB Q breakpoint #52 (Gbps)",
        "BB Q breakpoint #53 (Gbps)",
        "BB Q breakpoint #54 (Gbps)",
        "BB Q breakpoint #55 (Gbps)",
        "BB Q breakpoint #56 (Gbps)",
        "BB Q breakpoint #6 (Gbps)",
        "BB Q breakpoint #7 (Gbps)",
        "BB Q breakpoint #8 (Gbps)",
        "BB Q breakpoint #9 (Gbps)",
        "BB TAM uplift multiplier (data-intensity, derived year-row)",
        "BB TAM uplift ramp-end (yrs from 2025)",
        "BB TAM uplift target: data-intensity / value-per-connection (×)",
        "BB active Gbps (V2+V3 combined)",
        "BB demand curve level multiplier",
        "BB net adds (M)",
        "BB pool at-cost $/Gbps/yr",
        "BB subscribers: revenue-implied level (M)",
        "BB-share of bandwidth (ratio)",
        "Bandwidth",
        "Bandwidth cost ($mm)",
        "Bandwidth/peering cost per Gbps ($mm/Gbps-yr)",
        "Base turnaround time per booster (years/flight)",
        "Battery $/sat",
        "Billable H100-eq GPU-hrs",
        "Billable H100-eq GPU-hrs/sat",
        "Blended kit sale price ($/kit)",
        "Blended new-sat CapEx slug ($mm/sat): MEMO ONLY (feeds CAE R88 cap; no longer drives deployment)",
        "Blended new-sat mass (kg/sat): share-weighted, regime-gated (acyclic)",
        "Booster build CapEx ($mm)",
        "Booster cadence floor (flights/yr, operational)",
        "Booster fleet BoY (units)",
        "Booster fleet EoY (units)",
        "Booster mfg per stack ($mm)",
        "Boosters built (fleet)",
        "Boosters built this year (= Vehicle Build Boosters built (fleet))",
        "Boosters needed (fleet)",
        "Boosters retired (fleet)",
        "Boundary tie: 'Facilities Build' chips − (ODC R55 + Terr R94)×toggle; must = 0",
        "Broadband ARPU ($/sub/mo): year-row",
        "CAC slug per customer ($)",
        "CAPACITY (Starship + F9)",
        "CAPACITY + CapEx + TRANSFER REVENUE",
        "CAPEX (corporate + spectrum + module aggregation)",
        "COGS",
        "COGS ($mm)",
        "COGS total",
        "COGS total ($mm)",
        "COGS total ($mm)   ◄ Allocator OUT",
        "COGS: AI - Compute",
        "COGS: Customer Launch",
        "COGS: Lunar - Mars",
        "COGS: Starlink",
        "CONSERVATION: identity checks",
        "CUM-UPMASS + FLEET ROLL-FORWARD",
        "CUSTOMER LAUNCH",
        "Cadence ceiling (flights/booster/year)",
        "Cap scale factor (≤1, pro-rata)",
        "Cap: AI-Compute max deployable ($mm)",
        "Cap: Customer Launch max deployable ($mm)",
        "Cap: Starlink max deployable ($mm)",
        "CapEx ($mm)",
        "CapEx - facility + chips ($mm)",
        "CapEx - sat fleet incl chips ($mm)",
        "CapEx slug per MW ($mm)",
        "CapEx slug per sat ($mm)",
        "CapEx: AI - Compute",
        "CapEx: Corporate",
        "CapEx: Customer Launch",
        "CapEx: Lunar - Mars",
        "CapEx: Starlink",
        "Capacity (Gbps)",
        "Capacity available after LM (kg)",
        "Capital Deployed (cumulative)",
        "Capital lifetime: BV straight-line dep (yrs)",
        "Capital lifetime: BV straight-line depreciation (years)",
        "Capped: AI-Compute ($mm)",
        "Capped: Customer Launch ($mm)",
        "Capped: Starlink ($mm)",
        "Carve-out % of prior-year Group FCF",
        "Carve-out IRR signal: avg prior-yr spot IRR (3 modules)",
        "Carve-out IRR-response ceiling % (max carve-out at low anchor)",
        "Carve-out IRR-response high-IRR anchor (base % at/above)",
        "Carve-out IRR-response low-IRR anchor (ceiling % at/below)",
        "Carve-out IRR-response ramp [0,1]",
        "Carve-out IRR-response start year",
        "Carve-out cash receipt ($mm)",
        "Carve-out effective % (IRR-responsive)",
        "Carve-out floor ($mm/yr)",
        "Carve-out pre-2028 R&D-only override ($mm/yr)",
        "Cash BoY ($mm)",
        "Cash EoY ($mm)",
        "Cash available for year ($mm)",
        "Cash → BB ($mm)",
        "Cash → DTC ($mm)",
        "Cash-flow identity",
        "Chip FP8 density CAGR (post-2030)",
        "Chip FP8 per chip (TFLOPS)",
        "Chip FP8 per chip CAGR (/yr): smooth curve",
        "Chip TDP CAGR (post-2027, W/chip)",
        "Chip TDP per chip (W)",
        "Chip cost ASP ($/chip): derived",
        "Chip cost at-cost ($/sat)",
        "Chip cost basis ($/TFLOPS, gen anchor @2025)",
        "Chip cost-per-TFLOPS decline rate g (per-FLOP, A8.2)",
        "Chip operating temp (K)",
        "Chip perf-per-watt CAGR (/yr)",
        "Chip perf-per-watt anchor 2025 (TFLOPS/W)",
        "Chip purchase internal ($mm)",
        "Chip purchases (internal transfer) ($mm)",
        "Chip-fab facility CapEx total ($mm)  ◄ AI-Compute",
        "Chip-fab facility D&A total ($mm)  ◄ AI-Compute",
        "Chips demanded this year (count)  ◄ AI-Compute",
        "Chips deployed (count)",
        "Chips per sat",
        "Commercial launch market size ($mm/year): year-row",
        "Commercial launch market size ($mm/yr)",
        "Comms ISL set $/sat",
        "Comp anchor: AI Stack standalone",
        "Comp anchor: AI/Compute standalone (CoreWeave-anchored)",
        "Comp anchor: Customer Launch standalone (Rocket Lab)",
        "Comp anchor: Group EV (Brant internal)",
        "Comp anchor: Group EV (Morgan Stanley public)",
        "Comp anchor: Lunar / Mars (NASA HLS lifetime)",
        "Comp anchor: Starlink standalone (Bernstein/JPM)",
        "Compute build headroom buffer (frac)",
        "Compute power per sat (kW)",
        "Compute transfer: DC internal rev − AI Apps COGS (=0)",
        "Conservation: Level-2 cash tie: allocated ≤ desired, no creation (≥0 = OK), A8.3",
        "Conservation: ODC Σdraw − Σrepay − balance (must = 0)",
        "Conservation: fab chips − DC chips×toggle; must = 0",
        "Conservation: max bucket (cum D&A − cum CapEx): must be ≤ 0",
        "Conservation: Σdraw − Σrepay − balance (must = 0)",
        "Constellation Bandwidth (Gbps)",
        "Constellation D&A ($mm)",
        "Corporate",
        "Corporate & infrastructure CapEx total ($mm)",
        "Corporate & infrastructure D&A total ($mm)",
        "Corporate CapEx ($mm)",
        "Corporate SG&A",
        "Corporate SG&A ($mm)",
        "Corporate, IT & HQ CapEx ($mm)",
        "Corporate, IT & HQ CapEx (% of Group revenue)",
        "Cum Starship boosters built (cumulative, from 0)",
        "Cum Starship boosters retired (cumulative, from 0)",
        "Cum Starship experience units (Wright's-Law cost basis, incl. 2024 baseline + F9-inherited seed; NOT the standing fleet)",
        "Cum Starship ships built (cumulative, from 0)",
        "Cum Starship ships retired (cumulative, from 0)",
        "Cum Starship upmass (fleet, end-of-year, kg)",
        "Cumulative Module CapEx ($mm)",
        "Cumulative Module D&A ($mm)",
        "Cumulative Starlink sats built (sats)",
        "Cumulative sats (target, WL)",
        "Customer Launch",
        "Customer Launch (commercial)",
        "Customer Launch F9",
        "Customer Launch R&D % (CAGR)",
        "Customer Launch R&D % (floor)",
        "Customer Launch R&D % (start)",
        "Customer Launch R&D: CAGR (taper)",
        "Customer Launch R&D: end-state % (floor)",
        "Customer Launch R&D: start % of external rev",
        "Customer Launch module SG&A (% of external rev)",
        "Customer Launch module — module = Space segment · 2-stream revenue $4,086M · full waterfall, R&D above EBITDA · separate F9 + Starship D&A · Spot IRR · per-launch D&A interface",
        "Customer Launch — Launch & Development",
        "Customer Launch — Launch Services",
        "Customer Launch — total",
        "Customer Service: flat % of Starlink subscription rev",
        "Customer support & billing ($mm)",
        "D&A",
        "D&A ($mm)",
        "D&A + Lunar-Mars book-value guard",
        "D&A total ($mm)",
        "D&A total ($mm)   ◄ Allocator OUT",
        "D&A: AI - Compute",
        "D&A: Corporate / facilities",
        "D&A: Customer Launch",
        "D&A: Lunar - Mars",
        "D&A: Starlink",
        "DF as-of2026 @2026 = 1.000",
        "DF as-of2040 @2040 = 1.000",
        "DF: as-of 2026",
        "DF: as-of 2030",
        "DF: as-of 2035",
        "DF: as-of 2040",
        "DTC ARPU ($/sub/mo): year-row",
        "DTC DEMAND CURVE (piecewise-linear Q→Revenue lookup)",
        "DTC FLEET + BANDWIDTH",
        "DTC Gbps available for external Starlink revenue",
        "DTC Q breakpoint #1 (Gbps)",
        "DTC Q breakpoint #10 (Gbps)",
        "DTC Q breakpoint #11 (Gbps)",
        "DTC Q breakpoint #12 (Gbps)",
        "DTC Q breakpoint #13 (Gbps)",
        "DTC Q breakpoint #14 (Gbps)",
        "DTC Q breakpoint #15 (Gbps)",
        "DTC Q breakpoint #16 (Gbps)",
        "DTC Q breakpoint #17 (Gbps)",
        "DTC Q breakpoint #18 (Gbps)",
        "DTC Q breakpoint #19 (Gbps)",
        "DTC Q breakpoint #2 (Gbps)",
        "DTC Q breakpoint #20 (Gbps)",
        "DTC Q breakpoint #21 (Gbps)",
        "DTC Q breakpoint #22 (Gbps)",
        "DTC Q breakpoint #23 (Gbps)",
        "DTC Q breakpoint #24 (Gbps)",
        "DTC Q breakpoint #25 (Gbps)",
        "DTC Q breakpoint #26 (Gbps)",
        "DTC Q breakpoint #27 (Gbps)",
        "DTC Q breakpoint #28 (Gbps)",
        "DTC Q breakpoint #29 (Gbps)",
        "DTC Q breakpoint #3 (Gbps)",
        "DTC Q breakpoint #30 (Gbps)",
        "DTC Q breakpoint #31 (Gbps)",
        "DTC Q breakpoint #32 (Gbps)",
        "DTC Q breakpoint #33 (Gbps)",
        "DTC Q breakpoint #34 (Gbps)",
        "DTC Q breakpoint #35 (Gbps)",
        "DTC Q breakpoint #36 (Gbps)",
        "DTC Q breakpoint #37 (Gbps)",
        "DTC Q breakpoint #38 (Gbps)",
        "DTC Q breakpoint #39 (Gbps)",
        "DTC Q breakpoint #4 (Gbps)",
        "DTC Q breakpoint #40 (Gbps)",
        "DTC Q breakpoint #41 (Gbps)",
        "DTC Q breakpoint #42 (Gbps)",
        "DTC Q breakpoint #43 (Gbps)",
        "DTC Q breakpoint #44 (Gbps)",
        "DTC Q breakpoint #45 (Gbps)",
        "DTC Q breakpoint #46 (Gbps)",
        "DTC Q breakpoint #47 (Gbps)",
        "DTC Q breakpoint #48 (Gbps)",
        "DTC Q breakpoint #49 (Gbps)",
        "DTC Q breakpoint #5 (Gbps)",
        "DTC Q breakpoint #50 (Gbps)",
        "DTC Q breakpoint #51 (Gbps)",
        "DTC Q breakpoint #52 (Gbps)",
        "DTC Q breakpoint #53 (Gbps)",
        "DTC Q breakpoint #54 (Gbps)",
        "DTC Q breakpoint #55 (Gbps)",
        "DTC Q breakpoint #56 (Gbps)",
        "DTC Q breakpoint #57 (Gbps)",
        "DTC Q breakpoint #58 (Gbps)",
        "DTC Q breakpoint #59 (Gbps)",
        "DTC Q breakpoint #6 (Gbps)",
        "DTC Q breakpoint #60 (Gbps)",
        "DTC Q breakpoint #61 (Gbps)",
        "DTC Q breakpoint #7 (Gbps)",
        "DTC Q breakpoint #8 (Gbps)",
        "DTC Q breakpoint #9 (Gbps)",
        "DTC TAM uplift multiplier (Starlink Mobile, derived year-row)",
        "DTC TAM uplift ramp-end (yrs from 2025)",
        "DTC TAM uplift target: Starlink Mobile premium (×)",
        "DTC active Gbps (V2+V3 combined)",
        "DTC avg subscribers (implied, M)",
        "DTC demand curve level multiplier",
        "DTC pool at-cost $/Gbps/yr",
        "Demand Curves: Starlink BB + DTC piecewise-linear lookup",
        "Demand curve escalator: start rate (annual)",
        "Demand curve escalator: taper end (yrs from 2025)",
        "Demand curve escalator: terminal rate (annual)",
        "Demand-buildable CapEx ($mm)",
        "Demand-saturation deployment headroom (sats)",
        "Demand-vs-supply CHECK (not a cap)",
        "Deployable area penalty (kg/m²)",
        "Deployment cap: MIN(demand, launch, pacing) (sats)",
        "Desired BB sats (pre-cap)",
        "Desired DTC sats (pre-cap)",
        "Desired Starship launches (current yr)",
        "Desired cash → ODC ($mm)",
        "Desired cash → Terrestrial ($mm)",
        "Desired cash: AI-Compute ($mm)",
        "Desired cash: Customer Launch ($mm)",
        "Desired cash: Starlink ($mm)",
        "Desired launch kg: AI-Compute",
        "Desired launch kg: Customer Launch",
        "Desired launch kg: Starlink",
        "Developer/API: ARPU ($/acct/yr)",
        "Developer/API: revenue ($mm)",
        "Developer/API: tokens (T)",
        "Developer/API: tokens/user (M/yr)",
        "Developer/API: users (M)",
        "EBIT ($mm)",
        "EBIT consistency",
        "EBIT: AI - Compute",
        "EBIT: Corporate",
        "EBIT: Customer Launch",
        "EBIT: Lunar - Mars",
        "EBIT: Starlink",
        "EBITDA Margin % (memo)",
        "EBITDA foot",
        "EBITDA: AI - Compute",
        "EBITDA: Corporate",
        "EBITDA: Customer Launch",
        "EBITDA: Lunar - Mars",
        "EBITDA: Starlink",
        "Effective Compute Ratio (ratio)",
        "Effective DTC Gbps per sat (revenue calibration)",
        "Effective compute (H100-eq, vintage-locked)",
        "Elimination conservation (Rule 21)",
        "Engine facility base capacity 2025 (engines/yr)",
        "Engine facility capacity (engines/yr per increment)",
        "Engine facility cost per capacity increment ($mm)",
        "Engine facility useful life (years)",
        "Engines demanded this year (= ships × engines/vehicle)",
        "Enterprise: ARPU ($/seat/yr)",
        "Enterprise: revenue ($mm)",
        "Enterprise: seats (M)",
        "Enterprise: tokens (T)",
        "Enterprise: tokens/user (M/yr)",
        "Environmental heat load q_env (W/m²)",
        "Explicit-PV tie (subtotal vs Σ modules) = 0",
        "External commercial launch demand (count)",
        "External compute 2025 seed (M H100-eq GPU)",
        "External compute demand (GPU-hrs, H100-eq)",
        "External government launch demand (count)",
        "External revenue ($mm)",
        "F9",
        "F9 2nd stage mfg cost ($mm/unit)",
        "F9 INTERNAL-VS-CUSTOMER RECONCILIATION (memo)",
        "F9 Spot IRR (reporting only, excluded from allocation)",
        "F9 Starlink launch cap, annualized (launches/yr): derived",
        "F9 Starlink launches YTD in pacing year (actual)",
        "F9 Wright's Law mfg learning rate",
        "F9 annual cadence per booster in service",
        "F9 at-cost rate per launch ($mm)",
        "F9 average realized payload per launch (kg)",
        "F9 base booster build rate (boosters/year, pre-V3-trigger)",
        "F9 booster (1st stage) mfg cost ($mm/unit)",
        "F9 booster build cost ($mm)",
        "F9 booster economic life (years)",
        "F9 booster fleet EoY",
        "F9 booster refurb % of mfg",
        "F9 boosters built (yr)",
        "F9 boosters built per year",
        "F9 boosters retired (yr)",
        "F9 boosters retired per year",
        "F9 build-rate decay window (years)",
        "F9 cadence + at-cost rates + glide path (separate from commercial price)",
        "F9 cadence per booster (flights/year)",
        "F9 cadence per booster (flights/year, flat)",
        "F9 cadence per booster (flights/yr)",
        "F9 customer launch price ($mm/launch)",
        "F9 customer launches (residual)",
        "F9 customer launches per year",
        "F9 fairing cost net of 75% recovery ($mm/flight)",
        "F9 fleet BoY (boosters)",
        "F9 fleet EoY (boosters)",
        "F9 internal launches per year (Starlink-driven)",
        "F9 launch capacity (launches/yr)",
        "F9 launches V2-Starlink final year",
        "F9 launches glide path (per year)",
        "F9 launches per year",
        "F9 lifetime reuses per booster",
        "F9 owned-vehicle D&A ($mm)",
        "F9 owned-vehicle D&A per launch ($mm)            ◄ interface to Starlink",
        "F9 owned-vehicle build CapEx",
        "F9 owned-vehicle build CapEx ($mm)   ◄ Allocator OUT",
        "F9 payload per launch (kg)",
        "F9 payload to LEO (kg)",
        "F9 per-launch ops cost ($mm)",
        "F9 sats per launch (V2 packing)",
        "F9 starting fleet at 2025 SoY (boosters)",
        "F9 total launch capacity (launches/yr)",
        "F9 variable cost per launch ($mm/launch)",
        "F9 vehicle life L (years)",
        "F9: CapEx slug per vehicle ($mm)",
        "F9: margin per vehicle per yr ($mm, ex-D&A)",
        "F9: revenue per vehicle per yr ($mm)",
        "FCF ($mm)",
        "FCF foot vs NOPAT+D&A−CapEx walk",
        "FCF identity: (EBIT + D&A − CapEx) − FCF (=0)",
        "FCF repayment sweep (% of excess FCF)",
        "FCF: AI - Compute",
        "FCF: Corporate (cost centre)",
        "FCF: Customer Launch",
        "FCF: Customer Launch (ex-Starship R&D; lifted to corporate)",
        "FCF: Group DCF subtotal (SL+CL+AI+Corp; excl L/M)",
        "FCF: Lunar - Mars",
        "FCF: Starlink",
        "FCF: less corporate",
        "FCF: less corporate (SG&A+shared R&D+spectrum+taxes+corp CapEx)",
        "FLEET PRODUCTION ↔ STANDING-FLEET RECONCILIATION",
        "FLEET WRIGHT'S COST CURVES + CONFIG LINES",
        "F_ref: reference compute unit (TFLOPS, H100 FP8)",
        "Fab slug cost (online-year, $mm)",
        "Facilities Build: capacity-step facility CapEx engine",
        "Facility / ground CapEx ($mm)",
        "Facility / ground D&A ($mm)",
        "Facility balance EoY ($mm)",
        "Facility draw ($mm)",
        "Facility interest ($mm)",
        "Facility repayment ($mm)",
        "Final BB sats",
        "Final DTC sats",
        "First mission year (Lunar Mars)",
        "Flag: rev-module SoTP<0, as-of2026 EBITDA (cnt, expect 0)",
        "Flag: rev-module SoTP<0, as-of2026 Exit (cnt, expect 0)",
        "Flag: rev-module SoTP<0, as-of2026 Gordon (cnt, expect 0)",
        "Fleet energy (GWh/yr)",
        "Fleet gross compute revenue ($mm)",
        "Free: ARPU ($/user/yr)",
        "Free: revenue ($mm)",
        "Free: tokens (T)",
        "Free: tokens/user (M/yr)",
        "Free: users (M)",
        "Fully-allocated cost ($mm)",
        "GLOBAL",
        "GPU effective-capacity degradation (per yr)",
        "GPU fleet (EoY, 15y cohort)",
        "GPU retirements (15y cohort)",
        "GPU-hr price ($/GPU-hr)",
        "GPU-hr price ($/GPU-hr): base (pre-dampener)",
        "GPU-hr price CAGR",
        "GPU-hrs required (H100-eq)",
        "GPUs added (count)",
        "GROUP EV: EBITDA-mult ($B)",
        "GROUP EV: EBITDA-mult ($mm)",
        "GROUP EV: Exit-mult ($B)",
        "GROUP EV: Exit-mult ($mm)",
        "GROUP EV: Gordon ($B)",
        "GROUP EV: Gordon ($mm)",
        "GROUP P&L: segment consolidation",
        "Gbps demand",
        "Gbps per GWh/yr",
        "General & Administrative: CAGR (taper)",
        "General & Administrative: end-state % (floor)",
        "General & Administrative: start % of group rev",
        "Gigabay base capacity 2025 (ships/yr)",
        "Gigabay installed Starship build capacity (ships/yr)  ◄ Assumptions",
        "Government launch market size ($mm/year): year-row",
        "Government launch market size ($mm/yr)",
        "Grand total",
        "Gross Profit",
        "Gross Profit ($mm)",
        "Gross Profit ($mm)   ◄ Allocator OUT",
        "Gross Profit: AI - Compute",
        "Gross Profit: Customer Launch",
        "Gross Profit: Lunar - Mars",
        "Gross Profit: Starlink",
        "Gross compute revenue ($mm)",
        "Ground / network",
        "Ground station CapEx this year ($mm)",
        "Ground station build CapEx per station ($mm)",
        "Ground station useful life (years)",
        "Ground stations built per year (placeholder, flat)",
        "Ground stations built this year",
        "Ground-network ops COGS ($mm)",
        "Ground-network ops COGS (% of revenue)",
        "Ground/facility CapEx",
        "Ground/facility CapEx ($mm)   ◄ Allocator OUT",
        "Ground/network cost ($mm)",
        "Ground/network opex pct rev",
        "Group COGS ($mm)",
        "Group CapEx: accrual ($mm)",
        "Group D&A ($mm)",
        "Group EBIT ($mm)",
        "Group EBITDA ($mm)",
        "Group EV anchor: Brant (internal)",
        "Group EV anchor: Morgan Stanley (public)",
        "Group EV: EBITDA-multiple",
        "Group EV: Exit-multiple",
        "Group EV: Exit-multiple (revenue)",
        "Group EV: Gordon",
        "Group EV: Gordon (perpetuity-growth)",
        "Group FCF ($mm)",
        "Group FCF: accrual walk ($mm)",
        "Group FCF: normalized walk (NOPAT+D&A−CapEx) ($mm)",
        "Group Gross Profit ($mm)",
        "Group Revenue ($mm)",
        "Group Revenue — total",
        "Group Taxes ($mm)",
        "Group WACC",
        "Group revenue base ($mm): placeholder (Starlink rev; swap to Group total in 4.5)",
        "HQ facility CapEx ($mm)  ◄ Group P&L",
        "HQ facility CapEx (% of revenue)",
        "HQ facility D&A ($mm)  ◄ Group P&L",
        "HQ facility useful life (years)",
        "Hardware / kit COGS ($mm)",
        "Hardware / kit revenue ($mm)",
        "Hardware replacement cost factor ($/kg landed): declining",
        "Hardware value-add ($/kg landed)",
        "Headroom: AI-Compute ($mm)",
        "Headroom: Customer Launch ($mm)",
        "Headroom: Starlink ($mm)",
        "Heat transport (kg/kW, glide): A8.7",
        "Heat transport anchor 2025 (kg/kW)",
        "Heat transport mature (kg/kW)",
        "Helper: L/M BV×mult @2040 (undiscounted) $mm",
        "Helper: Σ NormTermFCF (SL+CL+AI+Corp) $mm",
        "Higher-rank caps ahead of AI-Compute ($mm)",
        "Higher-rank caps ahead of Customer Launch ($mm)",
        "Higher-rank caps ahead of Starlink ($mm)",
        "Hours per year (AI/Compute utilization)",
        "IPO injection ($mm)",
        "IPO injection amount ($mm)",
        "IPO injection year",
        "Individual paid: ARPU ($/user/yr)",
        "Individual paid: revenue ($mm)",
        "Individual paid: tokens (T)",
        "Individual paid: tokens/user (M/yr)",
        "Individual paid: users (M)",
        "Infrastructure useful life (years)",
        "Installed Starship build capacity (ships/yr): rate-limited ramp",
        "Installed engine-facility capacity (engines/yr): EoY ratchet, ≥ current demand, memo",
        "Installed fab capacity (wspm): EoY ratchet / phase step",
        "Installed launch pads (Starship): cumulative, ≥ base, memo",
        "Installed sat-factory capacity (sats/yr): EoY ratchet, ≥ current build",
        "Installed terminal-factory capacity (kits/yr): cumulative, memo",
        "Integration & Test $/sat",
        "Internal bandwidth eliminated, ODC→Starlink",
        "Internal compute eliminated, ODC→AI",
        "Internal compute share",
        "Internal launch services: RETIRED by 4.5 inversion",
        "Internal share",
        "Internal transfer revenue ($mm)",
        "Kg demand year N (kg)",
        "Kg demand year N+1",
        "Kg demand year N+1 (off-the-top reservation)",
        "LAUNCHES PER YEAR (F9 glide path + Starship demand-pulled)",
        "LM kg reserved off-top (kg)",
        "LR subsystems (learning rate, per doubling)",
        "LUNAR / MARS (strategic carve-out: not in the IRR queue)",
        "LUNAR active labour fleet EoY (running sum, net retire)",
        "LUNAR annual BV contribution ($mm/yr)",
        "LUNAR annual hardware value-add ($mm/yr)",
        "LUNAR annual production output ($mm/yr)",
        "LUNAR economic-output proxy ($mm): MEMO ONLY, NOT used in valuation",
        "LUNAR labour units retired this year (cohort lookback)",
        "Labour annual output per unit this year ($mm/yr)",
        "Labour annual output per unit, base year ($mm/yr)",
        "Labour unit base hourly output ($/hr)",
        "Labour unit base hourly output ($/hr; burdened $22/0.7)",
        "Labour unit cost ($/unit)",
        "Labour unit cost ($/unit): declining curve",
        "Labour unit daily working hours",
        "Labour unit mass (kg)",
        "Labour unit operational lifespan on surface (years)",
        "Labour unit productivity factor",
        "Labour unit productivity factor vs human baseline",
        "Labour unit productivity learning rate (%/yr)",
        "Labour unit useful life (yrs)",
        "Launch & Development revenue ($mm)",
        "Launch & Development revenue ($mm/yr)",
        "Launch & Development revenue ($mm/yr): year-row",
        "Launch / facility D&A ($mm)",
        "Launch / vehicle facility CapEx ($mm)",
        "Launch / vehicle facility D&A ($mm)",
        "Launch Dashboard — actual launches flown, by module, per year",
        "Launch IRR slug working-capital % of build",
        "Launch Services revenue ($mm)",
        "Launch capacity allotment: AI-Compute (kg)",
        "Launch capacity allotment: Customer Launch (kg)",
        "Launch capacity allotment: Starlink (kg)",
        "Launch cost ($mm/launch)",
        "Launch cost per sat ($mm)",
        "Launch demand elasticity multiplier cap (x)",
        "Launch demand price elasticity e (extra, on $/kg)",
        "Launch facility share (frac)",
        "Launch insurance % of external rev",
        "Launch insurance ($mm)",
        "Launch other COGS % of external rev",
        "Launch pad build/upgrade cost ($mm per pad)",
        "Launch pad useful life (years)",
        "Launch pads base in service 2025 (Starship-capable)",
        "Launch pads needed (= Starship launches ÷ launches/pad)",
        "Launch services",
        "Launch services cost ($mm)",
        "Launch vehicle calendar life (years)",
        "Launch-capacity deployment ceiling (sats): same-year demand vs start-of-year capacity",
        "Launch-infra capacity installed (launches/yr)",
        "Launch-kg available (= (target + retirements) × dry mass): ODC",
        "Launch-pacing year (apply caps in this year only)",
        "Launch-site infra CapEx ($mm per annual launch of capacity)",
        "Launch-site infrastructure CapEx ($mm)",
        "Launch/vehicle facility CapEx total ($mm)  ◄ launch/vehicle",
        "Launch/vehicle facility D&A total ($mm)  ◄ launch/vehicle",
        "Leftover cash ($mm)",
        "Legacy BB Gbps",
        "Legacy V1 Gbps per sat",
        "Legacy V1 active sats",
        "Legacy V1 active sats end-2025",
        "Legacy V1 base deorbit end year",
        "Legacy V1 base deorbit start year",
        "Legacy V1 sat mass (kg)",
        "Legacy V1.5 Gbps per sat",
        "Legacy V1.5 active sats",
        "Legacy V1.5 active sats end-2025",
        "Legacy V1.5 base deorbit end year",
        "Legacy V1.5 base deorbit start year",
        "Legacy V1.5 sat mass (kg)",
        "Lifetime reuses per booster (year cap)",
        "Lookup form: INDEX/MATCH(..., 1) bracket-find + manual linear interp. NO FORECAST / TREND. Per Memory Snapshot v3 §2.4.",
        "Lunar % payload as labour units",
        "Lunar - Mars",
        "Lunar / Mars",
        "Lunar / Mars (BV×mult)",
        "Lunar / Mars: terminal BV multiplier",
        "Lunar Mars Module D&A ($mm)",
        "Lunar carve-out cash this year ($mm)",
        "Lunar fuel depot multiplier per outbound Starship",
        "Lunar hardware mass landed this year (kg)",
        "Lunar hardware mass per ship (kg)",
        "Lunar labour mass landed this year (kg)",
        "Lunar labour mass per ship (kg)",
        "Lunar labour units landed this year (count)",
        "Lunar labour units per ship (count)",
        "Lunar payload per surface-landed Starship (kg)",
        "Lunar share of Mars/Moon carve-out cash: year-row",
        "Lunar share of carve-out cash (year-row)",
        "Lunar surface missions deployed (count)",
        "Lunar+Mars Net Book Value ($mm)",
        "Lunar+Mars Net Book Value ($mm): SoTP terminal (cumCapEx − cum D&A)",
        "Lunar/Mars BV multiplier",
        "Lunar/Mars carve-out % of prior-year Group FCF",
        "Lunar/Mars carve-out cash ($mm)",
        "Lunar/Mars carve-out floor ($mm/yr)",
        "Lunar/Mars carve-out pre-first-mission-year R&D-only override ($mm/yr)",
        "Lunar/Mars carve-out uses prior-year FCF (0/1)",
        "MARS active labour fleet EoY (running sum, net retire)",
        "MARS annual BV contribution ($mm/yr)",
        "MARS annual hardware value-add ($mm/yr)",
        "MARS annual production output ($mm/yr)",
        "MARS economic-output proxy ($mm): MEMO ONLY, NOT used in valuation",
        "MARS labour units retired this year (cohort lookback)",
        "MW added",
        "MW fleet (EoY, 15y cohort)",
        "MW retirements (15y cohort)",
        "Margin per MW per yr ($mm)",
        "Margin per sat per yr ($mm)",
        "Mars % payload as labour units",
        "Mars carve-out cash this year ($mm)",
        "Mars fuel depot multiplier per outbound Starship",
        "Mars hardware mass landed this year (kg)",
        "Mars hardware mass per ship (kg)",
        "Mars labour mass landed this year (kg)",
        "Mars labour mass per ship (kg)",
        "Mars labour units landed this year (count)",
        "Mars labour units per ship (count)",
        "Mars payload per surface-landed Starship (kg)",
        "Mars share of carve-out cash (year-row)",
        "Mars surface missions deployed (count)",
        "Max Starship build-capacity added per year (ships/yr)",
        "Max Starship launch capacity (kg/yr ceiling): 0 = off",
        "Memo: (retired: carve-out computed on Cash Allocation Engine R24)",
        "Memo: 2025 CapEx reconciliation",
        "Memo: 2025 D&A reconciliation",
        "Memo: 2025 DTC sub-line reconciliation",
        "Memo: 2025 EBIT reconciliation",
        "Memo: 2025 revenue reconciliation",
        "Memo: AI - Compute sub-lines − module Revenue",
        "Memo: AI Apps per-customer Spot IRR (diagnostic: no allocation consumer)",
        "Memo: AI EBITDA tie: Group EBITDA-AI (R54) − module ('AI - Compute' R169+R168); must = 0",
        "Memo: AI kg ration (diagnostic: ODC self-supplies, A7.1)",
        "Memo: AI placeholder strategic CapEx ($mm): engine, TEMP",
        "Memo: AI segment AI Solutions & Infra 2025 ($M)",
        "Memo: AI segment Adj EBITDA 2025 ($M)",
        "Memo: AI segment Advertising 2025 ($M)",
        "Memo: AI segment CapEx 2025 ($M)",
        "Memo: AI segment R&D 2025 ($M)",
        "Memo: AI segment nameplate compute draw EoY 2025 (GW)",
        "Memo: AI segment total revenue 2025 ($M)",
        "Memo: Accumulated depreciation Dec 31 2025 ($M)",
        "Memo: Attributed R&D, Starlink (in Module OpEx; excl. Total R&D)",
        "Memo: Attributed R&D, Starlink (now in Module OpEx; excl. from Total R&D)",
        "Memo: Average $/Gbps BB from curve",
        "Memo: Average $/Gbps DTC from curve",
        "Memo: Avg customer payload size (mt/mission)",
        "Memo: Carve-out reserved vs Module CapEx gap ($mm)",
        "Memo: Connectivity Adj EBITDA margin 2025: calibration target",
        "Memo: Connectivity COGS 2025 ($M)",
        "Memo: Connectivity COGS 2025 ($M): calibration",
        "Memo: Connectivity Consumer revenue 2025 ($M)",
        "Memo: Connectivity E&G incl Mobile revenue 2025 ($M)",
        "Memo: Connectivity R&D 2025 ($M)",
        "Memo: Connectivity R&D 2025 ($M): calibration",
        "Memo: Connectivity SG&A 2025 ($M)",
        "Memo: Connectivity SG&A 2025 ($M): calibration",
        "Memo: Connectivity segment CapEx 2025 ($M)",
        "Memo: Connectivity segment income from ops 2025 ($M): calibration",
        "Memo: Countries served",
        "Memo: Customer A concentration risk (US Gov NASA+DoW % consol)",
        "Memo: Customer Launch sub-lines − module Revenue",
        "Memo: DC chips deployed (ODC R55 + Terr R94)",
        "Memo: Deferred revenue (Dec 31 2025) ($M)",
        "Memo: Demand dampener (price-at-Q, =MIN(1,(demand/supply)^b))",
        "Memo: EBITDA Margin %",
        "Memo: EchoStar spectrum deal total ($M, S-1 audited)",
        "Memo: Engine cash Group FCF ($mm)",
        "Memo: Enterprise churn: qualitative",
        "Memo: F9 available capacity (kg)",
        "Memo: F9 customer (model) vs S-1 customer − Starshield",
        "Memo: F9 customer launches (Customer Launch)",
        "Memo: F9 internal (model) vs S-1 core Starlink + Starshield",
        "Memo: F9 internal launches (Starlink-driven)",
        "Memo: F9 launch capacity (launches/yr)",
        "Memo: F9 price set to $54.8M lands 2025 Launch Services = $2,575.6M (target $2,576M) + Launch & Delivery $1,510M → revenue $4,085.6M ≈ S-1 Space $4,086M.",
        "Memo: Gross Margin %",
        "Memo: Group D&A 2025 variance vs $1,060M",
        "Memo: Group EBITDA 2025 variance vs $8,690M",
        "Memo: Group EV as-of2026 Exit $B",
        "Memo: Group EV as-of2026 Gordon $B",
        "Memo: Group FCF 2025 variance vs $3,670M",
        "Memo: Group Revenue − Group P&L Group Revenue",
        "Memo: Group revenue (claims base) ($mm)",
        "Memo: HQ CapEx (2025 ≈ $53M reference)",
        "Memo: Interface contract: Module OUT canonical labels",
        "Memo: L/M SoTP (BV-based, as-of 2026)",
        "Memo: L/M strategic premium over cash-drain PV",
        "Memo: Loss from operations 2025 ($M): calibration",
        "Memo: Lunar - Mars sub-line − module Revenue",
        "Memo: Lunar surface missions cumulative",
        "Memo: MNO addressable population (millions)",
        "Memo: MNO partner count",
        "Memo: Mars surface missions cumulative",
        "Memo: Mass to orbit: F9 (kg)",
        "Memo: Mass to orbit: Starship (kg)",
        "Memo: ODC cum draws ($mm)",
        "Memo: ODC cum repayments ($mm)",
        "Memo: ODC demand share: RETIRED A8.3 (demand not split; ODC-priority)",
        "Memo: ODC first deployment year (anchor)",
        "Memo: ODC kg-buildable (diagnostic: unused after A7.1)",
        "Memo: ODC→Terr spillover ($mm): A8.3 (consumed by R114)",
        "Memo: Operating cash flow 2025 ($M): calibration",
        "Memo: P&L↔IRR conservation",
        "Memo: P&L↔IRR operating-margin",
        "Memo: PP&E net Dec 31 2025 ($M)",
        "Memo: PV of L/M FCF drain embedded in Group FCF",
        "Memo: R&D dual-track divergence",
        "Memo: Realized $/GPU-hr (base × dampener)",
        "Memo: Space + Connectivity CapEx 2025 ($M)",
        "Memo: Space R&D 2025 ($M): calibration",
        "Memo: Space segment CapEx 2025 ($M)",
        "Memo: Space segment income from ops 2025 ($M): calibration",
        "Memo: SpaceX Launch-Services rev as % of expanded $TAM (coherence check, must be <100%)",
        "Memo: Spectrum licence fee renewal flag (2042)",
        "Memo: Starlink sub-lines − module Revenue",
        "Memo: Starlink+DTC revenue (excl. Starshield)",
        "Memo: Subsequent events check (S-1/A)",
        "Memo: Terr MW demand-implied (pre-cash)",
        "Memo: Terr demand share: RETIRED A8.3 (demand not split)",
        "Memo: Terr share of net demand gap: RETIRED A8.0.1 (superseded by IRR-share demand split)",
        "Memo: Terrestrial AI compute draw (GW): year-row",
        "Memo: Terr→ODC spillover ($mm): A8.3 (consumed by R112)",
        "Memo: Tesla-funded fab CapEx ((1−share)) ($mm)",
        "Memo: Total F9 launches (internal + customer)",
        "Memo: Total Lunar + Mars Accumulated BV ($mm): SoTP terminal input",
        "Memo: Total Lunar+Mars kg landed this year",
        "Memo: Total backlog (Dec 31 2025) ($M)",
        "Memo: Total depreciation 2025 ($M): calibration",
        "Memo: Total mass to orbit (mt)",
        "Memo: Total-demand-vs-supply CHECK",
        "Memo: VB fleet CapEx conservation (=VB R53)",
        "Memo: Vehicle Build FCF ($mm): must = 0 by construction",
        "Memo: avg $/launch (LS)",
        "Memo: best-available launch $/kg index ($mm/kg, readiness-blended)",
        "Memo: booster fleet reconciliation ((cum built − cum retired) − Booster fleet EoY; must = 0)",
        "Memo: carve-out tie (engine − LM receipt, must=0)",
        "Memo: cash deployed by modules ($mm)",
        "Memo: chip-supply check (soft)",
        "Memo: cum active launch vehicles (F9 + Starship)",
        "Memo: cum launch-site infra CapEx ($mm)",
        "Memo: cumulative (Start+ΣIPO+ΣBridge+ΣFCF+Facility net) ($mm)",
        "Memo: cumulative draws ($mm)",
        "Memo: cumulative repayments ($mm)",
        "Memo: expanded commercial launch $TAM ($mm, elastic — baseline row 13 × multiplier)",
        "Memo: expanded government launch $TAM ($mm, elastic — baseline row 14 × multiplier)",
        "Memo: explicit-DCF of Group FCF incl L/M (no TV)",
        "Memo: explicit-DCF of SoTP modules (SL+CL+AI+Corp)",
        "Memo: fleet CapEx conservation (engine − Σ module; must = 0)",
        "Memo: full JV fab CapEx (100%, pre-share) ($mm)",
        "Memo: implied total Starlink subscribers (BB, M) vs S-1 8.9M",
        "Memo: launch cadence (Wright's Law) is driven by total fleet cumulative up-mass (row 76 = Σ row 32 Starship launches × payload) — all flights, internal Starlink + commercial, not customer-launch flights only. Do not repoint.",
        "Memo: launch demand elasticity multiplier (x)",
        "Memo: launch-infra allocable per vehicle ($mm)",
        "Memo: launch/vehicle CapEx (2025 ≈ $593M reference; low today: Starship ships = 0)",
        "Memo: launch/vehicle facility CapEx (from Facilities Build)",
        "Memo: normalization delta (accrual walk − normalized walk) ($mm)",
        "Memo: post-rebuild capacity state (Demand Curves now prices this tab)",
        "Memo: reclassification conservation",
        "Memo: roll-up CapEx: IRR slug basis (fab on D&A) ($mm)",
        "Memo: roll-up blended life L (yrs)",
        "Memo: roll-up capex slug per GPU-hr ($mm)",
        "Memo: roll-up cumulative CapEx ($mm)",
        "Memo: roll-up margin per GPU-hr ($mm)",
        "Memo: satellite-manufacturing CapEx (2025 ≈ $200M reference)",
        "Memo: share sum (must=1)",
        "Memo: ship fleet reconciliation ((cum built − cum retired) − Ship fleet EoY; must = 0)",
        "Memo: total F9 (model) vs S-1 total 171 (132 internal + 38.6 customer)",
        "Memo: total external launches",
        "Memo: total kg demand (kg)",
        "Memo: total launch + facility CapEx",
        "Memo: within-AI share sum (=1)",
        "Memo: Σ Group FCF cumulative (Rule 23 yr-chained)",
        "Memo: Σ module owned launch CapEx (all modules)",
        "Memo: Σ new infrastructure CapEx ex-terminal ($mm)",
        "Midpoint (mean of 3)",
        "Minimum cash buffer ($mm)",
        "Mission ops cost: Lunar ($mm)",
        "Mission ops cost: Lunar (% of Lunar CapEx)",
        "Mission ops cost: Mars ($mm)",
        "Mission ops cost: Mars (% of Mars CapEx)",
        "Model (Gordon) vs Brant",
        "Model (Gordon) vs MS",
        "Model EV as-of 2026: Exit-mult",
        "Model EV as-of 2026: Gordon",
        "Module CapEx",
        "Module CapEx ($mm)",
        "Module CapEx (FCF input) ($mm)",
        "Module CapEx total ($mm)",
        "Module CapEx total ($mm)   ◄ Allocator OUT",
        "Module EBIT",
        "Module EBIT ($mm)",
        "Module EBIT ($mm)   ◄ Allocator OUT",
        "Module EBITDA",
        "Module EBITDA ($mm)",
        "Module EBITDA ($mm)   ◄ Allocator OUT",
        "Module EBITDA Margin %",
        "Module FCF",
        "Module FCF ($mm)",
        "Module FCF ($mm)   ◄ Allocator OUT",
        "Module OpEx",
        "Module OpEx ($mm)",
        "Module OpEx total ($mm)   ◄ Allocator OUT",
        "Module OpEx total (incl. R&D) ($mm)",
        "Module OpEx: AI - Compute",
        "Module OpEx: Customer Launch",
        "Module OpEx: Lunar - Mars",
        "Module OpEx: Starlink",
        "Module Spot IRR   ◄ Allocator OUT",
        "Module Spot IRR (rev-weighted)",
        "Module operating cost: Lunar (% of Lunar CapEx)",
        "Module operating cost: Mars (% of Mars CapEx)",
        "Months elapsed in pacing year (for annualization)",
        "Multiple: AI/Compute (EV/EBITDA at horizon)",
        "Multiple: AI/Compute (EV/Rev at 2050)",
        "Multiple: Customer Launch (EV/EBITDA at horizon)",
        "Multiple: Customer Launch (EV/Rev at 2050)",
        "Multiple: Starlink (EV/EBITDA at horizon)",
        "Multiple: Starlink (EV/Rev at 2050)",
        "NOPAT ($mm)",
        "Net margin per customer (excl CAC) ($)",
        "Net-new customers (M)",
        "Network operations ($mm)",
        "Network ops & G&A (% of revenue)",
        "New Gigabay CapEx this year ($mm)",
        "New Starshield deployment (sats/yr)",
        "New Starship build-capacity added (ships/yr)",
        "New V2 BB deployment (sats/yr)",
        "New V2 DTC deployment (sats/yr)",
        "New V3 BB deployment (sats/yr)",
        "New V3 DTC deployment (sats/yr)",
        "New engine-facility CapEx this year ($mm)",
        "New fab CapEx this year ($mm): 3yr window spread",
        "New fab capacity added (wspm)",
        "New launch-pad CapEx this year ($mm)",
        "New sat-factory CapEx this year ($mm)",
        "New terminal-factory CapEx this year ($mm) × toggle",
        "Next-gen R&D uplift (peak, × extra R&D at gen jump)",
        "Non-thermal base mass (kg): A8.7",
        "ODC CapEx need ($mm): launch-feasible deploy × cost",
        "ODC R&D CAGR",
        "ODC R&D floor pct",
        "ODC R&D start pct",
        "ODC construction facility cap ($mm)",
        "ODC demand-buildable CapEx ($mm)",
        "ODC facility FCF repayment sweep (%)",
        "ODC facility balance EoY ($mm)",
        "ODC facility draw ($mm)",
        "ODC facility draw-window end year",
        "ODC facility interest ($mm)",
        "ODC facility interest rate (annual)",
        "ODC facility repaid-by year",
        "ODC facility repayment ($mm)",
        "ODC insurance pct rev",
        "ODC other COGS pct rev",
        "ODC pool allocation ($mm)",
        "ODC power density (kW/ton): OUTPUT memo (A8.7)",
        "ODC power density ramp-end year",
        "ODC pre-launch R&D ($mm/yr, 2025-27)",
        "ODC sat-factory CapEx ($mm per sat/yr of capacity)",
        "ODC sat-factory capacity installed (sats/yr): EoY ratchet",
        "ODC sat-mfg facility CapEx ($mm)  ◄ infra/Group",
        "ODC sats built: driver (sats/yr)",
        "ODC target fleet (sats, demand-share)",
        "ODC — RETIRED, superseded by the AI/Compute section. Memos below retained.",
        "OPEX (Group-level + module-attributed R&D parameters)",
        "OpEx ($mm)",
        "Orbital DC: allocated cash ($mm) ◄ CAE Level-2",
        "Orbital PUE",
        "Other corporate operating: flat % of group rev",
        "Other launch COGS ($mm)",
        "Other non-thermal mass: bus+structure+compute (kg)",
        "Owned launch-fleet D&A ($mm)",
        "Owned launch-vehicle CapEx ($mm)",
        "PER-LAUNCH AT-COST RATES ($mm): internal transfer pricing source",
        "PUE_base (terrestrial colo)",
        "Paying customers (M)",
        "Payload: booster-only mode (kg-to-LEO)",
        "Payload: fully reusable mode (kg-to-LEO)",
        "Per-ship cost: Lunar ($mm/ship)",
        "Per-ship cost: Mars ($mm/ship)",
        "Placeholder AI/strategic CapEx ($mm): TEMP (retire when AI-Compute loaded)",
        "Placeholder AI/strategic CapEx (% of Group revenue): TEMP",
        "Pool after queue gate ($mm)",
        "Power cost ($/kWh)",
        "Power cost CAGR",
        "Pre-2025 active Starshield installed base (sats)",
        "Pre-IPO bridge loan ($mm)",
        "Productivity multiplier (year-row, anchor-offset)",
        "Queue gate non-module claims total ($mm)",
        "R&D % of revenue",
        "RETIRED (orbital-data-centre ground stations CapEx)",
        "RETIRED (orbital-data-centre ground stations installed)",
        "Radiator area (m²): A8.7",
        "Radiator areal density (kg/m², glide): A8.7",
        "Radiator areal density anchor 2025 (kg/m²)",
        "Radiator areal density mature (kg/m²)",
        "Radiator delta-T (K)",
        "Radiator emissivity (0-1)",
        "Radiator net rejection (W/m²): A8.7",
        "Range (max − min)",
        "Rank key: AI-Compute",
        "Rank key: Customer Launch",
        "Rank key: Starlink",
        "Raptor engines per booster (Super Heavy)",
        "Raptor engines per ship (2nd stage)",
        "Read-only. Direct pulls from module tabs. Each module row is the realized (capped) launch count; total = their sum.",
        "Remaining pool for IRR-weighted allocation ($mm): gated to 0 in the 2025 anchor year; allocation operative 2026 onward",
        "Required fab capacity (wspm)",
        "Required installed compute w/ buffer (GPU-hrs)",
        "Revenue",
        "Revenue   ◄ Allocator OUT",
        "Revenue ($mm)",
        "Revenue per sat ($mm/yr, incl orbital PUE)",
        "Revenue tie",
        "Revenue: AI - Compute",
        "Revenue: AI - Compute — AI Apps (external)",
        "Revenue: AI - Compute — Orbital DC (external)",
        "Revenue: AI - Compute — Terrestrial DC (external)",
        "Revenue: Customer Launch",
        "Revenue: Customer Launch — Launch & Development",
        "Revenue: Customer Launch — Launch Services",
        "Revenue: Lunar - Mars",
        "Revenue: Starlink",
        "Revenue: Starlink — Broadband (BB)",
        "Revenue: Starlink — Direct-to-Cell (DTC)",
        "Revenue: Starlink — Hardware / kit",
        "Revenue: Starlink — Starshield",
        "Roll-up / reconciliation tab — modules own launch CapEx. Books no FCF; aggregates module-owned launch CapEx + fleet.",
        "Roll-up Attributed R&D",
        "Roll-up COGS (consol)",
        "Roll-up D&A",
        "Roll-up Gross Profit",
        "Roll-up Gross margin %",
        "Roll-up Kg demand year N+1",
        "Roll-up Module CapEx",
        "Roll-up Module EBIT",
        "Roll-up Module FCF",
        "Roll-up Module OpEx",
        "Roll-up Owned launch-vehicle CapEx ($mm)",
        "Roll-up Revenue (external, consol)",
        "Roll-up Spot marginal IRR (external, consol)",
        "Roll-up Starship launches per year (ODC-driven)",
        "Running cost (COGS+OpEx) ($mm)",
        "S&M - customer acquisition ($mm)",
        "S-1 2025 SpaceX total CapEx ($mm)",
        "SHIP FLEET ROLL-FORWARD (booster / ship split)",
        "STARLINK",
        "STARSHIP BUILD CapEx SPLIT",
        "Sales & Marketing ($mm)",
        "Sales & Marketing: CAGR (taper)",
        "Sales & Marketing: end-state % (floor)",
        "Sales & Marketing: start % of (Starlink+Starshield+CL ext) rev",
        "Sat cost $/kg (Wright's, floored)",
        "Sat facility capacity-ratio CapEx exponent",
        "Sat factory base capacity 2025 (sats/yr)",
        "Sat factory capacity (sats/yr per increment)",
        "Sat factory cost per capacity increment ($mm)",
        "Sat factory useful life (years)",
        "Sat operational life L (years)",
        "Sat retirements (5y cohort)",
        "Sat solar generation (W)",
        "Sat thermal mass (kg): derived",
        "Sat total cost ($mm/sat)",
        "Sat utilization (frac)",
        "Sat-factory capacity ratio",
        "Sat-mfg facility CapEx total ($mm)  ◄ Starlink",
        "Sat-mfg facility D&A ($mm)  ◄ Starlink",
        "Satellite Dep per kg: base year ($/kg/yr)",
        "Satellite build CapEx ($mm)",
        "Satellite cost floor ($/kg)",
        "Satellite cost per kg: base year ($/kg)",
        "Satellite cost per kg: learning rate",
        "Satellite/unit build CapEx",
        "Sats added (target)",
        "Sats built: Starlink (sats/yr)",
        "Sats deployed (actual)",
        "Sats fundable from cash",
        "Sats fundable from launch kg",
        "Sats per Starship launch",
        "Segment P&L — full Group waterfall with revenue broken to module sub-segments (read-only presentation; ties to Group P&L)",
        "Selling, general & administrative ($mm)",
        "Shared / unattributable R&D ($mm)",
        "Shared / unattributable R&D: corporate",
        "Shared / unattributable R&D: corporate (incl Starship platform R&D)",
        "Shared corporate R&D ($mm/yr): year-row",
        "Shielding $/sat",
        "Ship build CapEx ($mm)",
        "Ship cadence floor (flights/yr, operational)",
        "Ship fleet BoY (units)",
        "Ship fleet EoY (units)",
        "Ship mfg per stack ($mm)",
        "Ship refurb % of manufacturing",
        "Ship-to-booster cadence ratio",
        "Ships built (fleet)",
        "Ships built this year (= Vehicle Build Ships built (fleet), unified)",
        "Ships needed (fleet)",
        "Ships retired (fleet)",
        "SoTP / VALUATION: dual-track terminal · single WACC · EV only",
        "Solar array $/W",
        "Solar array mass (kg): A8.7",
        "Solar specific power (W/kg, glide): A8.7",
        "Solar specific power anchor 2025 (W/kg)",
        "Solar specific power mature (W/kg)",
        "SpaceX commercial market share",
        "SpaceX commercial market share %",
        "SpaceX government market share",
        "SpaceX government market share %",
        "Spectrum licence OpEx ($mm)",
        "Spectrum licence OpEx (% of revenue)",
        "Spectrum licence fee",
        "Spectrum licence fee ($mm)",
        "Spillover weight: AI-Compute",
        "Spillover weight: Customer Launch",
        "Spillover weight: Starlink",
        "Spot IRR",
        "Spot IRR: AI-Compute",
        "Spot IRR: Customer Launch",
        "Spot IRR: ODC (prior yr)",
        "Spot IRR: Starlink",
        "Spot IRR: Terrestrial (prior yr)",
        "Spot marginal IRR",
        "Spread %",
        "Spread (Exit − Gordon)",
        "Starfactory CapEx this year ($mm)",
        "Starfactory D&A ($mm)",
        "Starfactory build cost ($mm)",
        "Starfactory build window (years)",
        "Starlink",
        "Starlink (internal)",
        "Starlink (internal) F9",
        "Starlink BB Revenue from curve ($mm)",
        "Starlink BB capacity input (Gbps)",
        "Starlink DTC Revenue from curve ($mm)",
        "Starlink DTC capacity input (Gbps)",
        "Starlink R&D as % of revenue (frac)",
        "Starlink R&D: CAGR (taper)",
        "Starlink R&D: end-state % (floor)",
        "Starlink R&D: start % of (Starlink+Starshield) rev",
        "Starlink deployment 2025 anchor (sats)",
        "Starlink ground-network CapEx ($mm)",
        "Starlink ground-network CapEx (% of Starlink revenue)",
        "Starlink module allocated cash ($mm/yr): live from Cash Allocation Engine",
        "Starlink module — real cohorts + total-bandwidth revenue + full waterfall + 4-line OpEx + per-sat IRR",
        "Starlink — Broadband (BB)",
        "Starlink — Direct-to-Cell (DTC)",
        "Starlink — Hardware / kit",
        "Starlink — Starshield",
        "Starlink — total",
        "Starshield $/Gbps ($/Gbps-yr)",
        "Starshield $/Gbps ($/Gbps-yr) (working)",
        "Starshield Gbps growth (frac)",
        "Starshield active Gbps (working)",
        "Starshield active Gbps (year-row)",
        "Starshield revenue ($mm)",
        "Starshield sat mass (kg)",
        "Starshield utilization (frac)",
        "Starshield: CapEx slug per sat ($mm)",
        "Starshield: active fleet EoY (sats) (working)",
        "Starshield: margin per sat-yr ($mm)",
        "Starship",
        "Starship $/kg, expendable ship",
        "Starship $/kg, fully expendable",
        "Starship $/kg, fully reusable",
        "Starship 2nd-stage manufacturing cost ($mm/unit, base)",
        "Starship BOOSTER cadence per vehicle in service",
        "Starship F9-inherited experience seed (F9-equiv cum stacks at 2025 entry)",
        "Starship R&D total ($mm/yr): year-row",
        "Starship SHIP cadence per vehicle in service",
        "Starship Spot IRR (competes in the IRR-weighted allocation)",
        "Starship amortized mfg per launch, fully reusable ($mm)",
        "Starship at-cost rate per launch ($mm)",
        "Starship at-cost rate, expendable ship / reusable booster ($mm/launch)",
        "Starship at-cost rate, fully expendable ($mm/launch)",
        "Starship at-cost rate, fully reusable ($mm/launch)",
        "Starship booster cadence for pre-build sizing (flights/yr)",
        "Starship booster refurb cost anchor ($mm/flight, 2024 baseline)",
        "Starship booster refurb per flight ($mm)",
        "Starship booster share of manufacturing cost (% of stack mfg)",
        "Starship build cost ($mm/stack)",
        "Starship build-capacity ceiling (ships/yr)",
        "Starship cadence per vehicle (flights/yr)",
        "Starship commercial launches",
        "Starship commercial-readiness factor",
        "Starship commercial-readiness factor: year-row",
        "Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)",
        "Starship cum-upmass Wright's anchor (kg)",
        "Starship customer launch price ($mm/launch)",
        "Starship customer launch price ($mm/launch): year-row",
        "Starship customer launches per year",
        "Starship facility capacity (ships/yr per Gigabay)",
        "Starship facility cost per Gigabay increment ($mm)",
        "Starship facility useful life (years)",
        "Starship internal launches per year (Starlink-driven)",
        "Starship launches per pad per year",
        "Starship launches per year",
        "Starship launches per year (Lunar/Mars)",
        "Starship launches per year (ODC-driven)",
        "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)",
        "Starship manufacturing cost anchor ($mm/stack, 2024 baseline)",
        "Starship manufacturing cost per stack ($mm)",
        "Starship operational year",
        "Starship ops + fuel cost anchor ($mm/launch, 2024 baseline)",
        "Starship ops + fuel per launch ($mm)",
        "Starship ops/refurb WL learning rate (% reduction per doubling cum stacks)",
        "Starship owned-vehicle D&A ($mm)",
        "Starship owned-vehicle D&A per launch ($mm)      ◄ interface to Starlink",
        "Starship owned-vehicle build CapEx",
        "Starship owned-vehicle build CapEx ($mm)   ◄ Allocator OUT",
        "Starship payload for pre-build sizing (kg)",
        "Starship payload max cap (kg-to-LEO, fully reusable)",
        "Starship payload per launch (kg)",
        "Starship payload ramp 2030 anchor (kg-to-LEO, fully reusable)",
        "Starship payload ramp plateau year",
        "Starship payload, expendable ship (kg)",
        "Starship payload, fully expendable (kg)",
        "Starship payload, fully reusable (kg)",
        "Starship pre-build buffer multiple (x)",
        "Starship pre-build target: planned next-yr upmass (kg)",
        "Starship sats per launch (V3 packing): RETIRED — superseded by mass-derived sats/launch (Starlink R205)",
        "Starship sats per launch (V3, mass-derived)",
        "Starship ship refurb cost anchor ($mm/flight, 2024 baseline)",
        "Starship ship refurb per flight ($mm)",
        "Starship ship reuse life (flights per ship)",
        "Starship target launches (internal + commercial demand)",
        "Starship total capacity (launches/yr)",
        "Starship variable cost per launch ($mm/launch)",
        "Starship vehicle build cost ($mm)",
        "Starship vehicle fleet EoY",
        "Starship vehicle life L (years)",
        "Starship vehicles built (yr)",
        "Starship: CapEx slug per vehicle ($mm)",
        "Starship: margin per vehicle per yr ($mm, ex-D&A)",
        "Starship: revenue per vehicle per yr ($mm)",
        "Starting BoY 2025 subscribers (millions)",
        "Starting cash position EoY 2024 ($mm)",
        "Structure $/sat",
        "Subsystem cost pre-WL ($/sat)",
        "Subsystem cost w/ WL ($/sat)",
        "Subtotal: AI - Compute Revenue ($mm)",
        "Subtotal: Customer Launch Revenue ($mm)",
        "Subtotal: Lunar - Mars Revenue ($mm)",
        "Subtotal: Starlink Revenue ($mm)",
        "TOTAL KG DEMAND",
        "Tax rate (corporate, US federal + state blended)",
        "Taxes ($mm)",
        "Terafab CapEx to fund ($mm)",
        "Terafab R&D % of chip-supply (glide)",
        "Terafab R&D CAGR",
        "Terafab R&D floor pct",
        "Terafab R&D start pct",
        "Terafab capacity per fab phase (wspm/phase)",
        "Terafab chip-supply R&D ($mm) → roll-up R&D",
        "Terafab fab CapEx (blended all-in $/wspm)",
        "Terafab fab construction window (years)",
        "Terafab fab useful life (depreciation, years)",
        "Terafab facility cap ($mm)",
        "Terafab facility draw-window end year",
        "Terafab facility interest rate (annual)",
        "Terafab facility repaid-by year",
        "Terafab good chips per wspm per yr",
        "Terafab production cost frac (chip at-cost, → DC CapEx)",
        "Terafab toggle (1=NVIDIA-parity ON, 0=buy NVIDIA, 0.5=blend)",
        "Terafab: SpaceX cost/capacity share (frac)",
        "Terminal COGS per unit ($)",
        "Terminal FCF averaging window (years pre-2050)",
        "Terminal FCF avg window (yrs, =5)",
        "Terminal facility D&A ($mm) × toggle  ◄ Starlink",
        "Terminal factory CapEx toggle (1=on,0=off)",
        "Terminal factory capacity (kits/yr per increment)",
        "Terminal factory cost per capacity increment ($mm)",
        "Terminal factory useful life (years)",
        "Terminal growth g",
        "Terminal growth rate g (group + most modules)",
        "Terminal kits demanded this year (placeholder: Gbps-growth scaled)",
        "Terminal kits per net subscriber add",
        "Terminal replacement rate (% installed/yr)",
        "Terr demand-buildable CapEx ($mm)",
        "Terr target MW (demand-share)",
        "Terrestrial $/MW build",
        "Terrestrial DC: allocated cash ($mm) ◄ CAE Level-2 [drives R93]",
        "Terrestrial facility cost CAGR",
        "Terrestrial training CapEx ($mm): % × prior-yr AI revenue (A8.5)",
        "Terrestrial training D&A ($mm): cumulative ÷ life, MIN-capped (A8.5)",
        "Terrestrial training carve-out (% of prior-yr AI revenue)",
        "Thermal system $/kg",
        "Top-down sanity ex-chip-fab: (Total − chip-fab) vs S-1 2025 capex",
        "Top-down sanity: Total facility CapEx vs S-1 2025 SpaceX capex $8,000M (must be a fraction)",
        "Total AI-stack tokens (T)",
        "Total BB revenue ($mm)",
        "Total DC compute available (GPU-hrs)",
        "Total DTC revenue ($mm)",
        "Total F9 launches",
        "Total Module OpEx ($mm)",
        "Total R&D ($mm)",
        "Total Revenue ($mm)",
        "Total Starship airframes built (booster + ship)",
        "Total Starship build CapEx ($mm)",
        "Total Starship launches",
        "Total compute demand (GPU-hrs)",
        "Total compute gap (GPU-hrs): A8.3",
        "Total corporate OpEx ($mm)",
        "Total desired launch kg",
        "Total desired sats (pre-cap)",
        "Total desired upmass kg (fleet, current yr)  ◄ Cash Allocation Engine",
        "Total existing compute (GPU-hrs): A8.3",
        "Total facility CapEx ($mm) = sat-mfg + launch/vehicle + terminal + HQ",
        "Total fleet launch CapEx ($mm): independent (engine)",
        "Total inter-module eliminations ($mm)",
        "Total launch capacity (kg)",
        "Total launch capacity: start-of-year stock (kg)",
        "Total launch kg demand year N+1 (fleet)",
        "Total new Starlink deployment (sats/yr)",
        "Total revenue ($mm)",
        "Total sat dry mass (kg): derived",
        "Training carve-out % (= input): A8.5",
        "Two-sided radiator factor",
        "Utilization (%)",
        "V2 BB Gbps",
        "V2 BB Gbps per sat",
        "V2 BB sat mass (kg)",
        "V2 BB share of new deployment (frac)",
        "V2 BB: CapEx slug per sat ($mm)",
        "V2 BB: Spot IRR",
        "V2 BB: margin per sat-yr ($mm)",
        "V2 DTC active sats",
        "V2 DTC active sats end-2025",
        "V2 DTC base deorbit end year",
        "V2 DTC base deorbit start year",
        "V2 DTC effective Gbps",
        "V2 DTC sat mass (kg)",
        "V2 DTC share of new deployment (frac)",
        "V2 DTC: CapEx slug per sat ($mm)",
        "V2 DTC: Spot IRR",
        "V2 DTC: margin per sat-yr ($mm)",
        "V2 Mini BB active sats",
        "V2 Mini BB base deorbit end year",
        "V2 Mini BB base deorbit start year",
        "V2 Mini BB sats end-2025",
        "V2 launch window active (1/0)",
        "V3 BB Gbps",
        "V3 BB Gbps per sat",
        "V3 BB active sats EoY",
        "V3 BB sat mass (kg)",
        "V3 BB share of new deployment (frac)",
        "V3 BB: CapEx slug per sat ($mm)",
        "V3 BB: Spot IRR",
        "V3 BB: margin per sat-yr ($mm)",
        "V3 DTC active sats EoY",
        "V3 DTC effective Gbps",
        "V3 DTC sat mass (kg)",
        "V3 DTC share of new deployment (frac)",
        "V3 DTC: CapEx slug per sat ($mm)",
        "V3 DTC: Spot IRR",
        "V3 DTC: margin per sat-yr ($mm)",
        "V3 Starlink launch trigger year",
        "V3 deployment active (1/0)",
        "VALUATION",
        "VEHICLE PHYSICAL PARAMETERS (F9 + Starship payload + cadence)",
        "Variable launch COGS ($mm)",
        "Variable launch cost: F9 ($mm)",
        "Variable launch cost: Starship ($mm)",
        "Vehicle Build CapEx ($mm)",
        "Vehicle Build at-cost transfer revenue ($mm) — RETIRED (modules own launch CapEx)",
        "Vehicle Build: demand-pulled Starship + F9 launch capacity",
        "WACC (Group)",
        "WACC>g (1=OK; HALT if 0)",
        "WL learning rate: turnaround vs cum upmass doubling",
        "Water-fill residual ($mm)",
        "Working capital per sat ($mm/sat): ΔWC T0",
        "Working capital ΔWC",
        "Working capital ΔWC ($mm)",
        "Working capital ΔWC ($mm)   ◄ Allocator OUT",
        "Wright's Law anchor cum sats",
        "Wright's Law floor pct (of base subsystem cost)",
        "Wright's Law multiplier",
        "YEAR",
        "Year offset",
        "[SUPERSEDED A8.7] ODC power density anchor 2025 (kW/ton)",
        "[SUPERSEDED A8.7] ODC power density target (kW/ton)",
        "[SUPERSEDED A8.7] Sat base mass (non-thermal) (kg)",
        "exp(β·IRR) BB",
        "exp(β·IRR) DTC",
        "exp(β·IRR): AI-Compute",
        "exp(β·IRR): Customer Launch",
        "exp(β·IRR): ODC",
        "exp(β·IRR): Starlink",
        "exp(β·IRR): Terrestrial",
        "g ＼ WACC →",
        "kg-binding flag (1=capacity binds)",
        "less inter-module eliminations",
        "Σ exp(β·IRR)",
        "Σ exp: within-AI",
        "Σ spillover weight",
        "Σ standalone analyst anchors (SL+AI+CL+AIStack+L/M)",
        "Σ-D&A ≤ Σ-CapEx check (1=OK)",
        "⊘ REDUNDANT — AI Apps TAM (M subs)",
        "⊘ REDUNDANT — AI Apps adoption ceiling (% of TAM)",
        "⊘ REDUNDANT — AI Apps adoption steepness k",
        "⊘ REDUNDANT — AI Apps blended ARPU ($/sub/yr)",
        "⊘ REDUNDANT — AI Apps blended ARPU CAGR (/yr)",
        "⊘ REDUNDANT — AI Apps blended tokens per sub (M/sub/yr)",
        "⊘ REDUNDANT — AI Apps subs 2025 seed (M)",
        "⊘ REDUNDANT — AI Apps tokens-per-sub CAGR (/yr)",
        "⊘ REDUNDANT — AI Apps tokens-per-sub growth cap (×)",
        "⊘ REDUNDANT — blended ARPU (superseded by 5-bucket block, rows 224-255)",
        "⊘ REDUNDANT — blended tokens/sub (superseded by 5-bucket block, rows 224-255)",
        "▸ 2026 LAUNCH PACING & CASH RESERVE",
        "▸ ABSORPTIVE-CAPACITY WATER-FILL (top-level, A-refresh V4.102)",
        "▸ AI - COMPUTE OUT CONTRACT",
        "▸ AI - COMPUTE OUT CONTRACT — extended",
        "▸ AI / COMPUTE MODULE",
        "▸ AI APPS: 5-BUCKET DEMAND BUILD (replaces blended R116-118)",
        "▸ AI APPS: per customer-year (sub-line 3, L=3)",
        "▸ AI segment data",
        "▸ AI-COMPUTE SHARED DRIVERS (derived on-tab; no demand curve)",
        "▸ AI: AI Apps",
        "▸ AI: AI Apps (consolidated, A2.2)",
        "▸ AI: AI Apps 5-bucket demand build",
        "▸ AI: AI Apps demand uplift (un-flatten ARPU + tokens/sub)",
        "▸ AI: COMPUTE DEMAND BASIS (A8 endogenisation)",
        "▸ AI: Orbital DC ops cost rates",
        "▸ AI: Orbital DC physical anchors",
        "▸ AI: Orbital DC subsystem unit costs",
        "▸ AI: R&D attribution glides",
        "▸ AI: Terafab JV split + calibration (A4.1)",
        "▸ AI: Terafab chip-fab (→ Facilities Build, A4)",
        "▸ AI: Terafab toggle",
        "▸ AI: Terrestrial DC",
        "▸ AI: chip improvement + lightweighting CAGRs (A8.1)",
        "▸ AI: compute demand curve (A8.3)",
        "▸ AI: exogenous cost CAGRs (CAM port, MC)",
        "▸ AI: external compute demand (A8 endogenisation)",
        "▸ AI: merchant-IaaS supply-share lever",
        "▸ AI: orbital serving S-curve + training carve-out (A8.5)",
        "▸ AI: year-row inputs (Cam G:AF → Group D:AC)",
        "▸ ALLOCATOR IN (cross-tab reads)",
        "▸ ALLOCATOR OUT (canonical labels: Rule 12 sources)",
        "▸ ALLOCATOR: ODC Construction Facility (debt layer)",
        "▸ ALLOCATOR: Terafab Construction Facility (debt layer)",
        "▸ BB/DTC market mix",
        "▸ BLOCK A: ALLOCATOR IN (cross-tab reads)",
        "▸ BLOCK B: LAUNCH DEMAND & FLEET BUILD",
        "▸ BLOCK C: REVENUE (external only)",
        "▸ BLOCK D: COGS → GROSS PROFIT",
        "▸ BLOCK E: MODULE OpEx + R&D → MODULE EBITDA (R&D ABOVE EBITDA, Hard Rule 7)",
        "▸ BLOCK F: EBITDA → EBIT (only D&A below EBITDA)",
        "▸ BLOCK G: CAPEX → MODULE FCF",
        "▸ BLOCK H: PER-VEHICLE IRR ENGINE (v4 canonical, Spot only)",
        "▸ BLOCK I: ALLOCATOR OUT (amended canonical labels)",
        "▸ BLOCK J, CONSERVATION MEMOS (verification only, excl. sums)",
        "▸ BV ENGINE: SoTP / VALUATION TRACK (off-P&L)",
        "▸ Bandwidth flow → superseded by the AI/Compute section; see orbital-compute↔Starlink elimination",
        "▸ CAPACITY-PRIORITY ALLOCATION",
        "▸ CAPEX ($mm)",
        "▸ CAPEX → MODULE FCF",
        "▸ CARVE-OUT CASH RECEIPT (taken off the top, before the IRR allocation)",
        "▸ CARVE-OUT IRR RESPONSE (operative 2030 onward)",
        "▸ CARVE-OUT: LIVE every year",
        "▸ CASH EoY: LIVE every year; 2025 EoY feeds 2026 Cash BoY (the cash spine)",
        "▸ CASH POOL: LIVE every year (2025 = starting cash $11,385M + $20B bridge)",
        "▸ CHECKS (Rule 4/5/15)",
        "▸ CHIP-FAB FACILITY ENGINE (Terafab)",
        "▸ CHIP-FAB INTEGRATION (A5): Terafab R&D + boundary tie",
        "▸ COGS ($mm)",
        "▸ COGS → GROSS PROFIT",
        "▸ COMPARABLES CROSS-CHECK ($B)",
        "▸ CONSERVATION",
        "▸ CONSERVATION (intra-tab; must = 0: Rule 5/21)",
        "▸ CONSERVATION + CALIBRATION",
        "▸ CONSERVATION MEMOS",
        "▸ CONSTELLATION BUILD (real cohorts → total bandwidth)",
        "▸ CORPORATE OpEx ($mm)",
        "▸ CUSTOMER LAUNCH: module = Space segment, 2-stream revenue, R&D above EBITDA",
        "▸ Cash Allocation Engine inputs",
        "▸ Cash pool boundary inputs",
        "▸ Comparables anchors ($B)",
        "▸ Constellation opening balances (Mach33 historical anchors: hard)",
        "▸ Corporate facilities CapEx ($mm/yr)",
        "▸ Corporate historical capital base",
        "▸ Corporate useful lives",
        "▸ Curve evaluators (year-row, read by the Starlink module)",
        "▸ Customer Launch IRR life clamps",
        "▸ D&A ($mm)",
        "▸ DEMAND-DRIVEN FLEET SIZING (forward-demand pull, no circular reference)",
        "▸ DIAGNOSTIC: 2025 vs Q4'25 anchors (narrow-gate, non-halt)",
        "▸ DISCOUNT FACTORS: 1/(1+WACC)^(year−asof); 0 before asof",
        "▸ DUAL-TRACK SUMMARY: Group EV by as-of ($B)",
        "▸ Deorbit parameters",
        "▸ Depreciation parameters",
        "▸ Dual revenue model",
        "▸ EBIT: by segment ($mm)",
        "▸ EBITDA → EBIT (R&D is in Module OpEx above; only D&A below)",
        "▸ EBITDA: by segment ($mm)",
        "▸ EchoStar spectrum reclassified as recurring OpEx licence fee",
        "▸ F9 LAUNCHES FLOWN (count/yr) — legacy, winding down",
        "▸ F9 launch glide path (Customer Launch IN to Vehicle Build)",
        "▸ FACILITIES BASE ANCHORS (2025 standing capacity + sanity denominator)",
        "▸ FACILITIES BUILD: capacity-step facility CapEx",
        "▸ FREE CASH FLOW: by segment ($mm)",
        "▸ Falcon 9 physical + cost parameters",
        "▸ GROSS PROFIT ($mm)",
        "▸ HQ FACILITY (CORPORATE → GROUP)",
        "▸ INPUTS READ FROM ASSUMPTIONS",
        "▸ INTER-MODULE ELIMINATIONS (Rule 21: $0 in current build)",
        "▸ INTERFACE ALIASES (label-fidelity for downstream tabs)",
        "▸ INTERFACE CONTRACT (exposed labels)",
        "▸ INTERNAL LAUNCHES + RETAIL FLEET (working)",
        "▸ IRR-DRIVEN COHORT ALLOCATION: prior-year spot IRR weights per-cohort affordability (broadband vs direct-to-cell)",
        "▸ IRR-weighted allocation parameters",
        "▸ KG-RATIONING GATE",
        "▸ LAUNCH CAPEX ROLL-UP (books no FCF)",
        "▸ LEVEL-2: WITHIN-AI ODC vs TERRESTRIAL SPLIT (A7)",
        "▸ LUNAR MISSION DEPLOYMENT (first-mission-year gated)",
        "▸ LUNAR/MARS BRIDGE & GROUP-FCF RECON (memo, as-of 2026)",
        "▸ LUNAR–MARS REPORTED P&L",
        "▸ Labour unit shared parameters (Optimus-class proxy)",
        "▸ Lunar / Mars share of carve-out cash (derived deployment)",
        "▸ Lunar-specific",
        "▸ Lunar/Mars strategic carve-out (Monte Carlo variable)",
        "▸ MARS MISSION DEPLOYMENT (first-mission-year gated)",
        "▸ MEMO / DIAGNOSTICS",
        "▸ MISSING-CAPEX BUCKETS (prior-year-driven; 2025 = current-year anchor)",
        "▸ MISSING-CAPEX PROGRAMS",
        "▸ MODULE FCF: DCF inputs (direct from Group P&L, $mm)",
        "▸ MODULE OpEx",
        "▸ MODULE OpEx: direct ($mm)",
        "▸ MODULE ROLL-UP (consolidated; external rev only; internal compute transfer eliminated; Terafab off-tab → A4/A5)",
        "▸ MODULE SHARE OF STARSHIP LAUNCHES (%)",
        "▸ MODULE SoTP: EBITDA-MULTIPLE terminal, $mm",
        "▸ MODULE SoTP: EXIT-MULTIPLE terminal, $mm",
        "▸ MODULE SoTP: GORDON (perpetuity-growth) terminal, $mm",
        "▸ Mars-specific",
        "▸ Module-wide parameters",
        "▸ NEW S-1 derived inputs",
        "▸ NEW Starlink rows from S-1 disclosures",
        "▸ ODC CONSTRUCTION FACILITY (debt layer — funds ODC sat rollout)",
        "▸ ORBITAL DC: per compute sat-year (sub-line 1, L=5)",
        "▸ OpEx calibration targets",
        "▸ PER-SAT IRR ENGINE (v4 canonical): per cohort, one cost base",
        "▸ PER-SHIP COST BUILD",
        "▸ Per-module asset life L (canonical IRR formula input)",
        "▸ QUEUE GATE: LIVE every year",
        "▸ R&D ($mm)",
        "▸ R&D attribution rules",
        "▸ R&D: Lunar/Mars ($-profile year-row, pre-revenue)",
        "▸ REVENUE",
        "▸ REVENUE ($mm)",
        "▸ REVENUE — SEGMENT SUB-LINES ($mm)",
        "▸ S-1 NEW CapEx calibration targets",
        "▸ S-1 derived valuation triangulation memos",
        "▸ SATELLITE-MFG FACILITY ENGINE (Redmond)",
        "▸ SEGMENT MIX — % OF GROUP REVENUE",
        "▸ SENSITIVITY: Group EV as-of 2026, GORDON ($B)",
        "▸ SG&A by function (Group-level)",
        "▸ STARFACTORY: initial production facility (base capacity, one-time)",
        "▸ STARLINK MODULE",
        "▸ STARLINK: real cohorts + DTC effective lever",
        "▸ STARSHIP LAUNCHES FLOWN (count/yr)",
        "▸ STARSHIP PRODUCTION FACILITY (Starfactory/Gigabay): capacity + scaling",
        "▸ SUB-SEGMENT MIX — % OF OWN SEGMENT REVENUE",
        "▸ SUBSCRIBERS + HARDWARE",
        "▸ Satellite physical",
        "▸ Shared / unattributable corporate R&D (Group, residual)",
        "▸ SoTP EV/EBITDA multiples (terminal, at horizon)",
        "▸ SoTP TERMINAL MEMO",
        "▸ SoTP multiples (EV/Revenue at 2050)",
        "▸ Starlink R&D attribution rule",
        "▸ Starshield",
        "▸ Starship R&D total ($mm/yr): splits across modules by launch share",
        "▸ Starship cadence (Wright's Law on cum upmass)",
        "▸ Starship time-varying inputs (year-rows)",
        "▸ Starship vehicle physical + cost parameters",
        "▸ Subscribers + ARPU + Terminals (BIG S-1 IMPACTS)",
        "▸ TAXES & NOPAT ($mm)",
        "▸ TERAFAB CONSTRUCTION FACILITY (debt layer)",
        "▸ TERMINAL VALUE @2040 (both methods, $mm)",
        "▸ TERMINALS (Bastrop): toggle-gated",
        "▸ TERRESTRIAL DC: per MW-year (sub-line 2, L=15)",
        "▸ TIE-OUT CHECKS (must = 0 within $1mm)",
        "▸ TOP-LEVEL IRR-WEIGHTED ALLOCATION: allocated cash = 0 in the 2025 anchor year; operative 2026→2050 (shares sum to 1)",
        "▸ TOTAL LAUNCHES, ALL VEHICLES (count/yr)",
        "▸ TRI-TRACK SUMMARY: Group EV by as-of ($B)",
        "▸ Terminal value parameters",
        "▸ VEHICLE BUILD EXPOSURES (added 2026-06-01: resolve VB fleet pulls; canonical uniform labels)",
        "▸ VEHICLE BUILD: Starship fleet Wright's cost + cadence (fleet-level launch learning)",
        "▸ Vehicle build claim (demand-pulled, one-period lag)",
        "▸ WACC + risk premia",
        "▸ WACC component memos (not used in formulas)",
        "▸ Wright's Law parameters",
        "▸ Year-row cost curves",
        "▸ §A8.6: ODC THERMAL RECALIBRATION (kW/ton glide + dynamic TDP)",
        "▸ §IRR allocation soft floor",
    }
)

LABELS_BY_SHEET: Final[dict[str, tuple[str, ...]]] = {
    "AI - Compute": (
        "▸ AI - COMPUTE OUT CONTRACT",
        "Revenue",
        "Module OpEx",
        "Attributed R&D",
        "D&A",
        "Module EBIT",
        "Module CapEx",
        "Module FCF",
        "Kg demand year N+1",
        "Spot marginal IRR",
        "▸ AI-COMPUTE SHARED DRIVERS (derived on-tab; no demand curve)",
        "Chip TDP per chip (W)",
        "Chip FP8 per chip (TFLOPS)",
        "GPU-hr price ($/GPU-hr): base (pre-dampener)",
        "Utilization (%)",
        "Chip cost ASP ($/chip): derived",
        "Sat thermal mass (kg): derived",
        "Total sat dry mass (kg): derived",
        "▸ ORBITAL DC: per compute sat-year (sub-line 1, L=5)",
        "Launch cost ($mm/launch)",
        "Orbital DC: allocated cash ($mm) ◄ CAE Level-2",
        "Launch-kg available (= (target + retirements) × dry mass): ODC",
        "Sats added (target)",
        "Chips per sat",
        "Subsystem cost pre-WL ($/sat)",
        "Sats per Starship launch",
        "Cumulative sats (target, WL)",
        "Wright's Law multiplier",
        "Subsystem cost w/ WL ($/sat)",
        "Chip cost at-cost ($/sat)",
        "Sat total cost ($mm/sat)",
        "Launch cost per sat ($mm)",
        "Sats fundable from cash",
        "Sats fundable from launch kg",
        "Sat retirements (5y cohort)",
        "Sats deployed (actual)",
        "Active sat fleet (EoY)",
        "Chips deployed (count)",
        "Billable H100-eq GPU-hrs/sat",
        "Revenue per sat ($mm/yr, incl orbital PUE)",
        "Fleet gross compute revenue ($mm)",
        "Internal compute share",
        "Launch services cost ($mm)",
        "Fleet energy (GWh/yr)",
        "Gbps demand",
        "Bandwidth cost ($mm)",
        "Ground/network cost ($mm)",
        "R&D % of revenue",
        "Chip purchase internal ($mm)",
        "Kg demand year N (kg)",
        "External revenue ($mm)",
        "COGS ($mm)",
        "Launch services",
        "Bandwidth",
        "Ground / network",
        "OpEx ($mm)",
        "D&A ($mm)",
        "Running cost (COGS+OpEx) ($mm)",
        "Fully-allocated cost ($mm)",
        "Internal transfer revenue ($mm)",
        "Total revenue ($mm)",
        "Gross Profit ($mm)",
        "Attributed R&D ($mm)",
        "EBIT ($mm)",
        "CapEx - sat fleet incl chips ($mm)",
        "Chip purchases (internal transfer) ($mm)",
        "FCF ($mm)",
        "Margin per sat per yr ($mm)",
        "CapEx slug per sat ($mm)",
        "Asset life L: Orbital DC (yrs)",
        "Spot IRR",
        "Starship launches per year (ODC-driven)",
        "Owned launch-vehicle CapEx ($mm)",
        "▸ TERRESTRIAL DC: per MW-year (sub-line 2, L=15)",
        "MW added",
        "GPUs added (count)",
        "Internal share",
        "Power cost ($/kWh)",
        "MW fleet (EoY, 15y cohort)",
        "GPU fleet (EoY, 15y cohort)",
        "Effective compute (H100-eq, vintage-locked)",
        "Billable H100-eq GPU-hrs",
        "Gross compute revenue ($mm)",
        "CapEx - facility + chips ($mm)",
        "Margin per MW per yr ($mm)",
        "CapEx slug per MW ($mm)",
        "Asset life L: Terrestrial DC (yrs)",
        "▸ AI APPS: per customer-year (sub-line 3, L=3)",
        "AI Apps subs (M)",
        "⊘ REDUNDANT — blended ARPU (superseded by 5-bucket block, rows 224-255)",
        "⊘ REDUNDANT — blended tokens/sub (superseded by 5-bucket block, rows 224-255)",
        "AI Apps revenue ($mm)",
        "Paying customers (M)",
        "Net-new customers (M)",
        "S&M - customer acquisition ($mm)",
        "CapEx ($mm)",
        "AI Apps tokens (T)",
        "Total AI-stack tokens (T)",
        "GPU-hrs required (H100-eq)",
        "Total DC compute available (GPU-hrs)",
        "AI Apps served (GPU-hrs, capped)",
        "AI Apps share of DC compute",
        "Demand-vs-supply CHECK (not a cap)",
        "Net margin per customer (excl CAC) ($)",
        "CAC slug per customer ($)",
        "Asset life L: AI Apps (yrs)",
        "Memo: AI Apps per-customer Spot IRR (diagnostic: no allocation consumer)",
        "▸ MODULE ROLL-UP (consolidated; external rev only; internal compute transfer eliminated; Terafab off-tab → A4/A5)",
        "Roll-up Revenue (external, consol)",
        "Roll-up COGS (consol)",
        "Roll-up Gross Profit",
        "Roll-up Gross margin %",
        "Roll-up Module OpEx",
        "Roll-up Attributed R&D",
        "Roll-up D&A",
        "Roll-up Module EBIT",
        "Roll-up Module CapEx",
        "Roll-up Module FCF",
        "Roll-up Kg demand year N+1",
        "Roll-up Spot marginal IRR (external, consol)",
        "Roll-up Starship launches per year (ODC-driven)",
        "Roll-up Owned launch-vehicle CapEx ($mm)",
        "▸ CONSERVATION (intra-tab; must = 0: Rule 5/21)",
        "Compute transfer: DC internal rev − AI Apps COGS (=0)",
        "FCF identity: (EBIT + D&A − CapEx) − FCF (=0)",
        "▸ AI - COMPUTE OUT CONTRACT — extended",
        "COGS",
        "▸ CHIP-FAB INTEGRATION (A5): Terafab R&D + boundary tie",
        "Terafab R&D % of chip-supply (glide)",
        "Terafab chip-supply R&D ($mm) → roll-up R&D",
        "Boundary tie: 'Facilities Build' chips − (ODC R55 + Terr R94)×toggle; must = 0",
        "Memo: roll-up margin per GPU-hr ($mm)",
        "Memo: roll-up cumulative CapEx ($mm)",
        "Memo: roll-up capex slug per GPU-hr ($mm)",
        "Memo: roll-up blended life L (yrs)",
        "Terrestrial DC: allocated cash ($mm) ◄ CAE Level-2 [drives R93]",
        "▸ AI: COMPUTE DEMAND BASIS (A8 endogenisation)",
        "AI compute demand reference (M H100-eq GPU): seed-anchored S-curve (A8.5)",
        "External compute demand (GPU-hrs, H100-eq)",
        "Total compute demand (GPU-hrs)",
        "Required installed compute w/ buffer (GPU-hrs)",
        "Memo: Total-demand-vs-supply CHECK",
        "MW retirements (15y cohort)",
        "GPU retirements (15y cohort)",
        "Memo: Terr share of net demand gap: RETIRED A8.0.1 (superseded by IRR-share demand split)",
        "Memo: Terr MW demand-implied (pre-cash)",
        "Demand-buildable CapEx ($mm)",
        "Memo: ODC demand share: RETIRED A8.3 (demand not split; ODC-priority)",
        "Memo: Terr demand share: RETIRED A8.3 (demand not split)",
        "ODC target fleet (sats, demand-share)",
        "Terr target MW (demand-share)",
        "ODC demand-buildable CapEx ($mm)",
        "Terr demand-buildable CapEx ($mm)",
        "Memo: roll-up CapEx: IRR slug basis (fab on D&A) ($mm)",
        "Memo: Demand dampener (price-at-Q, =MIN(1,(demand/supply)^b))",
        "Memo: Realized $/GPU-hr (base × dampener)",
        "Total existing compute (GPU-hrs): A8.3",
        "Total compute gap (GPU-hrs): A8.3",
        "Training carve-out % (= input): A8.5",
        "Terrestrial training CapEx ($mm): % × prior-yr AI revenue (A8.5)",
        "Terrestrial training D&A ($mm): cumulative ÷ life, MIN-capped (A8.5)",
        "ODC power density (kW/ton): OUTPUT memo (A8.7)",
        "Radiator net rejection (W/m²): A8.7",
        "Radiator area (m²): A8.7",
        "Radiator areal density (kg/m², glide): A8.7",
        "Heat transport (kg/kW, glide): A8.7",
        "Solar specific power (W/kg, glide): A8.7",
        "Solar array mass (kg): A8.7",
        "Non-thermal base mass (kg): A8.7",
        "▸ AI APPS: 5-BUCKET DEMAND BUILD (replaces blended R116-118)",
        "Free: users (M)",
        "Free: ARPU ($/user/yr)",
        "Free: tokens/user (M/yr)",
        "Free: revenue ($mm)",
        "Free: tokens (T)",
        "Individual paid: users (M)",
        "Individual paid: ARPU ($/user/yr)",
        "Individual paid: tokens/user (M/yr)",
        "Individual paid: revenue ($mm)",
        "Individual paid: tokens (T)",
        "Developer/API: users (M)",
        "Developer/API: ARPU ($/acct/yr)",
        "Developer/API: tokens/user (M/yr)",
        "Developer/API: revenue ($mm)",
        "Developer/API: tokens (T)",
        "Enterprise: seats (M)",
        "Enterprise: ARPU ($/seat/yr)",
        "Enterprise: tokens/user (M/yr)",
        "Enterprise: revenue ($mm)",
        "Enterprise: tokens (T)",
        "Agentic coding: users (M)",
        "Agentic coding: ARPU ($/user/yr)",
        "Agentic coding: tokens/user (M/yr)",
        "Agentic coding: revenue ($mm)",
        "Agentic coding: tokens (T)",
        "Ads: monetizable base (M)",
        "Ads: ARPU ($/user/yr)",
        "Ads: revenue ($mm)",
        "AI Apps: paying users (M)",
        "AI Apps: total revenue ($mm)",
        "AI Apps: total tokens (T)",
    ),
    "Assumptions": (
        "GLOBAL",
        "Tax rate (corporate, US federal + state blended)",
        "Demand curve escalator: start rate (annual)",
        "Demand curve escalator: terminal rate (annual)",
        "ALLOCATOR",
        "▸ Cash pool boundary inputs",
        "Starting cash position EoY 2024 ($mm)",
        "IPO injection amount ($mm)",
        "IPO injection year",
        "▸ Lunar/Mars strategic carve-out (Monte Carlo variable)",
        "Lunar/Mars carve-out % of prior-year Group FCF",
        "Lunar/Mars carve-out floor ($mm/yr)",
        "Lunar/Mars carve-out uses prior-year FCF (0/1)",
        "Lunar/Mars carve-out pre-first-mission-year R&D-only override ($mm/yr)",
        "▸ IRR-weighted allocation parameters",
        "Allocation sharpness β (top-level 3-module blend)",
        "▸ Per-module asset life L (canonical IRR formula input)",
        "Asset life L: Customer Launch Starship (years)",
        "Asset life L: Customer Launch F9 (years)",
        "Asset life L: AI/Compute Orbital DC (years)",
        "Asset life L: AI/Compute Terrestrial DC (years)",
        "Asset life L: AI/Compute AI Apps (years)",
        "▸ Customer Launch IRR life clamps",
        "▸ Vehicle build claim (demand-pulled, one-period lag)",
        "CAPACITY (Starship + F9)",
        "▸ Starship vehicle physical + cost parameters",
        "Starship 2nd-stage manufacturing cost ($mm/unit, base)",
        "Ship refurb % of manufacturing",
        "Payload: booster-only mode (kg-to-LEO)",
        "Payload: fully reusable mode (kg-to-LEO)",
        "▸ Starship cadence (Wright's Law on cum upmass)",
        "Base turnaround time per booster (years/flight)",
        "WL learning rate: turnaround vs cum upmass doubling",
        "Cadence ceiling (flights/booster/year)",
        "▸ Starship time-varying inputs (year-rows)",
        "Lifetime reuses per booster (year cap)",
        "▸ Falcon 9 physical + cost parameters",
        "F9 booster (1st stage) mfg cost ($mm/unit)",
        "F9 2nd stage mfg cost ($mm/unit)",
        "F9 fairing cost net of 75% recovery ($mm/flight)",
        "F9 per-launch ops cost ($mm)",
        "F9 booster refurb % of mfg",
        "F9 payload to LEO (kg)",
        "F9 lifetime reuses per booster",
        "F9 Wright's Law mfg learning rate",
        "F9 cadence per booster (flights/year, flat)",
        "F9 base booster build rate (boosters/year, pre-V3-trigger)",
        "V3 Starlink launch trigger year",
        "F9 build-rate decay window (years)",
        "F9 starting fleet at 2025 SoY (boosters)",
        "▸ F9 launch glide path (Customer Launch IN to Vehicle Build)",
        "CUSTOMER LAUNCH",
        "F9 customer launch price ($mm/launch)",
        "Starship customer launch price ($mm/launch): year-row",
        "Commercial launch market size ($mm/year): year-row",
        "Government launch market size ($mm/year): year-row",
        "SpaceX commercial market share %",
        "SpaceX government market share %",
        "Launch insurance % of external rev",
        "Launch other COGS % of external rev",
        "▸ NEW S-1 derived inputs",
        "Memo: Avg customer payload size (mt/mission)",
        "STARLINK",
        "▸ Satellite physical",
        "▸ Wright's Law parameters",
        "Satellite cost per kg: base year ($/kg)",
        "Satellite cost per kg: learning rate",
        "Satellite cost floor ($/kg)",
        "▸ Starshield",
        "▸ Depreciation parameters",
        "Satellite Dep per kg: base year ($/kg/yr)",
        "▸ Constellation opening balances (Mach33 historical anchors: hard)",
        "▸ Deorbit parameters",
        "▸ Subscribers + ARPU + Terminals (BIG S-1 IMPACTS)",
        "Starting BoY 2025 subscribers (millions)",
        "Broadband ARPU ($/sub/mo): year-row",
        "DTC ARPU ($/sub/mo): year-row",
        "Terminal COGS per unit ($)",
        "▸ BB/DTC market mix",
        "▸ Bandwidth flow → superseded by the AI/Compute section; see orbital-compute↔Starlink elimination",
        "▸ NEW Starlink rows from S-1 disclosures",
        "Memo: MNO partner count",
        "Memo: MNO addressable population (millions)",
        "Memo: Countries served",
        "Memo: Enterprise churn: qualitative",
        "Memo: Connectivity Adj EBITDA margin 2025: calibration target",
        "Memo: Connectivity Consumer revenue 2025 ($M)",
        "Memo: Connectivity E&G incl Mobile revenue 2025 ($M)",
        "Memo: Connectivity COGS 2025 ($M)",
        "Memo: Connectivity SG&A 2025 ($M)",
        "Memo: Connectivity R&D 2025 ($M)",
        "▸ Starlink R&D attribution rule",
        "ODC — RETIRED, superseded by the AI/Compute section. Memos below retained.",
        "F_ref: reference compute unit (TFLOPS, H100 FP8)",
        "▸ Dual revenue model",
        "PUE_base (terrestrial colo)",
        "Orbital PUE",
        "Memo: ODC first deployment year (anchor)",
        "Memo: Terrestrial AI compute draw (GW): year-row",
        "AI STACK — RETIRED, superseded by the AI/Compute section. Memos below retained.",
        "▸ AI segment data",
        "Memo: AI segment total revenue 2025 ($M)",
        "Memo: AI segment Advertising 2025 ($M)",
        "Memo: AI segment AI Solutions & Infra 2025 ($M)",
        "Memo: AI segment Adj EBITDA 2025 ($M)",
        "Memo: AI segment R&D 2025 ($M)",
        "Memo: AI segment CapEx 2025 ($M)",
        "Memo: AI segment nameplate compute draw EoY 2025 (GW)",
        "LUNAR / MARS (strategic carve-out: not in the IRR queue)",
        "▸ Module-wide parameters",
        "Capital lifetime: BV straight-line depreciation (years)",
        "Module operating cost: Lunar (% of Lunar CapEx)",
        "Module operating cost: Mars (% of Mars CapEx)",
        "First mission year (Lunar Mars)",
        "▸ Labour unit shared parameters (Optimus-class proxy)",
        "Labour unit mass (kg)",
        "Labour unit base hourly output ($/hr; burdened $22/0.7)",
        "Labour unit daily working hours",
        "Labour unit productivity factor vs human baseline",
        "Labour unit productivity learning rate (%/yr)",
        "Labour unit operational lifespan on surface (years)",
        "▸ Lunar-specific",
        "Lunar fuel depot multiplier per outbound Starship",
        "Lunar payload per surface-landed Starship (kg)",
        "Lunar % payload as labour units",
        "▸ Mars-specific",
        "Mars fuel depot multiplier per outbound Starship",
        "Mars payload per surface-landed Starship (kg)",
        "Mars % payload as labour units",
        "▸ Year-row cost curves",
        "Labour unit cost ($/unit): declining curve",
        "Hardware replacement cost factor ($/kg landed): declining",
        "▸ Lunar / Mars share of carve-out cash (derived deployment)",
        "Lunar share of Mars/Moon carve-out cash: year-row",
        "OPEX (Group-level + module-attributed R&D parameters)",
        "▸ R&D attribution rules",
        "Starlink R&D: start % of (Starlink+Starshield) rev",
        "Starlink R&D: end-state % (floor)",
        "Starlink R&D: CAGR (taper)",
        "Customer Launch R&D: start % of external rev",
        "Customer Launch R&D: end-state % (floor)",
        "Customer Launch R&D: CAGR (taper)",
        "▸ R&D: Lunar/Mars ($-profile year-row, pre-revenue)",
        "▸ Starship R&D total ($mm/yr): splits across modules by launch share",
        "Starship R&D total ($mm/yr): year-row",
        "▸ Shared / unattributable corporate R&D (Group, residual)",
        "Shared corporate R&D ($mm/yr): year-row",
        "▸ SG&A by function (Group-level)",
        "Sales & Marketing: start % of (Starlink+Starshield+CL ext) rev",
        "Sales & Marketing: end-state % (floor)",
        "Sales & Marketing: CAGR (taper)",
        "General & Administrative: start % of group rev",
        "General & Administrative: end-state % (floor)",
        "General & Administrative: CAGR (taper)",
        "Customer Service: flat % of Starlink subscription rev",
        "Other corporate operating: flat % of group rev",
        "▸ OpEx calibration targets",
        "Memo: Space R&D 2025 ($M): calibration",
        "Memo: Connectivity R&D 2025 ($M): calibration",
        "Memo: Connectivity COGS 2025 ($M): calibration",
        "Memo: Connectivity SG&A 2025 ($M): calibration",
        "Memo: Total depreciation 2025 ($M): calibration",
        "Memo: Operating cash flow 2025 ($M): calibration",
        "Memo: Loss from operations 2025 ($M): calibration",
        "Memo: Space segment income from ops 2025 ($M): calibration",
        "Memo: Connectivity segment income from ops 2025 ($M): calibration",
        "CAPEX (corporate + spectrum + module aggregation)",
        "▸ Corporate facilities CapEx ($mm/yr)",
        "▸ Corporate useful lives",
        "▸ Corporate historical capital base",
        "▸ EchoStar spectrum reclassified as recurring OpEx licence fee",
        "Memo: EchoStar spectrum deal total ($M, S-1 audited)",
        "Memo: Spectrum licence fee renewal flag (2042)",
        "▸ S-1 NEW CapEx calibration targets",
        "Memo: Space segment CapEx 2025 ($M)",
        "Memo: Connectivity segment CapEx 2025 ($M)",
        "Memo: Space + Connectivity CapEx 2025 ($M)",
        "Memo: Total backlog (Dec 31 2025) ($M)",
        "Memo: Deferred revenue (Dec 31 2025) ($M)",
        "Memo: PP&E net Dec 31 2025 ($M)",
        "Memo: Accumulated depreciation Dec 31 2025 ($M)",
        "VALUATION",
        "▸ WACC + risk premia",
        "Group WACC",
        "▸ WACC component memos (not used in formulas)",
        "▸ Terminal value parameters",
        "Terminal growth rate g (group + most modules)",
        "Lunar / Mars: terminal BV multiplier",
        "Terminal FCF averaging window (years pre-2050)",
        "▸ Comparables anchors ($B)",
        "Comp anchor: Group EV (Morgan Stanley public)",
        "Comp anchor: Group EV (Brant internal)",
        "Comp anchor: Starlink standalone (Bernstein/JPM)",
        "Comp anchor: AI/Compute standalone (CoreWeave-anchored)",
        "Comp anchor: Customer Launch standalone (Rocket Lab)",
        "Comp anchor: AI Stack standalone",
        "Comp anchor: Lunar / Mars (NASA HLS lifetime)",
        "▸ SoTP multiples (EV/Revenue at 2050)",
        "Multiple: Customer Launch (EV/Rev at 2050)",
        "Multiple: Starlink (EV/Rev at 2050)",
        "Multiple: AI/Compute (EV/Rev at 2050)",
        "▸ S-1 derived valuation triangulation memos",
        "Memo: Customer A concentration risk (US Gov NASA+DoW % consol)",
        "Memo: Subsequent events check (S-1/A)",
        "Memo: Interface contract: Module OUT canonical labels",
        "F9 cadence + at-cost rates + glide path (separate from commercial price)",
        "F9 cadence per booster (flights/year)",
        "F9 at-cost rate per launch ($mm)",
        "Starship at-cost rate per launch ($mm)",
        "F9 launches glide path (per year)",
        "F9 booster economic life (years)",
        "F9 variable cost per launch ($mm/launch)",
        "Starship variable cost per launch ($mm/launch)",
        "▸ STARLINK MODULE",
        "Sat operational life L (years)",
        "Starship operational year",
        "F9 launches V2-Starlink final year",
        "V2 BB sat mass (kg)",
        "V2 DTC sat mass (kg)",
        "V3 BB sat mass (kg)",
        "V3 DTC sat mass (kg)",
        "V2 BB Gbps per sat",
        "V3 BB Gbps per sat",
        "Working capital per sat ($mm/sat): ΔWC T0",
        "Bandwidth/peering cost per Gbps ($mm/Gbps-yr)",
        "Sat utilization (frac)",
        "Starshield $/Gbps ($/Gbps-yr)",
        "Starshield active Gbps (year-row)",
        "Starshield Gbps growth (frac)",
        "Starshield sat mass (kg)",
        "Starlink deployment 2025 anchor (sats)",
        "V2 BB share of new deployment (frac)",
        "V2 DTC share of new deployment (frac)",
        "V3 BB share of new deployment (frac)",
        "V3 DTC share of new deployment (frac)",
        "Pre-2025 active Starshield installed base (sats)",
        "Starshield utilization (frac)",
        "F9 sats per launch (V2 packing)",
        "Starship sats per launch (V3 packing): RETIRED — superseded by mass-derived sats/launch (Starlink R205)",
        "▸ FACILITIES BUILD: capacity-step facility CapEx",
        "Sat factory cost per capacity increment ($mm)",
        "Sat factory capacity (sats/yr per increment)",
        "Sat factory useful life (years)",
        "Sat facility capacity-ratio CapEx exponent",
        "Starship facility cost per Gigabay increment ($mm)",
        "Starship facility capacity (ships/yr per Gigabay)",
        "Starship facility useful life (years)",
        "Launch pad build/upgrade cost ($mm per pad)",
        "Launch pad useful life (years)",
        "Starship launches per pad per year",
        "Engine facility cost per capacity increment ($mm)",
        "Engine facility capacity (engines/yr per increment)",
        "Engine facility useful life (years)",
        "Terminal factory cost per capacity increment ($mm)",
        "Terminal factory capacity (kits/yr per increment)",
        "Terminal factory useful life (years)",
        "Terminal factory CapEx toggle (1=on,0=off)",
        "Ground station build CapEx per station ($mm)",
        "Ground station useful life (years)",
        "Ground stations built per year (placeholder, flat)",
        "HQ facility CapEx (% of revenue)",
        "HQ facility useful life (years)",
        "Ground-network ops COGS (% of revenue)",
        "Asset insurance COGS (% of revenue)",
        "Spectrum licence OpEx (% of revenue)",
        "Starfactory build cost ($mm)",
        "Starfactory build window (years)",
        "▸ STARLINK: real cohorts + DTC effective lever",
        "Effective DTC Gbps per sat (revenue calibration)",
        "Network ops & G&A (% of revenue)",
        "Legacy V1 active sats end-2025",
        "Legacy V1 Gbps per sat",
        "Legacy V1.5 active sats end-2025",
        "Legacy V1.5 Gbps per sat",
        "V2 DTC active sats end-2025",
        "V2 Mini BB sats end-2025",
        "Legacy V1 sat mass (kg)",
        "Legacy V1.5 sat mass (kg)",
        "▸ CUSTOMER LAUNCH: module = Space segment, 2-stream revenue, R&D above EBITDA",
        "Customer Launch module SG&A (% of external rev)",
        "Launch & Development revenue ($mm/yr): year-row",
        "Starship commercial-readiness factor: year-row",
        "BB demand curve level multiplier",
        "DTC demand curve level multiplier",
        "Blended kit sale price ($/kit)",
        "▸ VEHICLE BUILD: Starship fleet Wright's cost + cadence (fleet-level launch learning)",
        "Starship manufacturing cost anchor ($mm/stack, 2024 baseline)",
        "Starship booster share of manufacturing cost (% of stack mfg)",
        "Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)",
        "Starship F9-inherited experience seed (F9-equiv cum stacks at 2025 entry)",
        "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)",
        "Starship ops + fuel cost anchor ($mm/launch, 2024 baseline)",
        "Starship booster refurb cost anchor ($mm/flight, 2024 baseline)",
        "Starship ship refurb cost anchor ($mm/flight, 2024 baseline)",
        "Starship ops/refurb WL learning rate (% reduction per doubling cum stacks)",
        "Starship ship reuse life (flights per ship)",
        "Starship cum-upmass Wright's anchor (kg)",
        "Starship payload ramp 2030 anchor (kg-to-LEO, fully reusable)",
        "Starship payload max cap (kg-to-LEO, fully reusable)",
        "Booster cadence floor (flights/yr, operational)",
        "Ship cadence floor (flights/yr, operational)",
        "Ship-to-booster cadence ratio",
        "Launch vehicle calendar life (years)",
        "Raptor engines per booster (Super Heavy)",
        "Raptor engines per ship (2nd stage)",
        "F9 average realized payload per launch (kg)",
        "▸ Cash Allocation Engine inputs",
        "Placeholder AI/strategic CapEx (% of Group revenue): TEMP",
        "▸ FACILITIES BASE ANCHORS (2025 standing capacity + sanity denominator)",
        "Sat factory base capacity 2025 (sats/yr)",
        "Gigabay base capacity 2025 (ships/yr)",
        "Engine facility base capacity 2025 (engines/yr)",
        "Launch pads base in service 2025 (Starship-capable)",
        "S-1 2025 SpaceX total CapEx ($mm)",
        "Legacy V1 base deorbit start year",
        "Legacy V1 base deorbit end year",
        "Legacy V1.5 base deorbit start year",
        "Legacy V1.5 base deorbit end year",
        "V2 Mini BB base deorbit start year",
        "V2 Mini BB base deorbit end year",
        "V2 DTC base deorbit start year",
        "V2 DTC base deorbit end year",
        "▸ 2026 LAUNCH PACING & CASH RESERVE",
        "Launch-pacing year (apply caps in this year only)",
        "F9 Starlink launches YTD in pacing year (actual)",
        "Months elapsed in pacing year (for annualization)",
        "F9 Starlink launch cap, annualized (launches/yr): derived",
        "Starship pre-build target: planned next-yr upmass (kg)",
        "Starship pre-build buffer multiple (x)",
        "Starship payload for pre-build sizing (kg)",
        "Starship booster cadence for pre-build sizing (flights/yr)",
        "▸ AI / COMPUTE MODULE",
        "Hours per year (AI/Compute utilization)",
        "▸ AI: Orbital DC physical anchors",
        "Compute power per sat (kW)",
        "Sat solar generation (W)",
        "[SUPERSEDED A8.7] Sat base mass (non-thermal) (kg)",
        "Effective Compute Ratio (ratio)",
        "▸ AI: Orbital DC subsystem unit costs",
        "Solar array $/W",
        "Thermal system $/kg",
        "Comms ISL set $/sat",
        "ADCS+avionics $/sat",
        "Structure $/sat",
        "Battery $/sat",
        "Shielding $/sat",
        "Integration & Test $/sat",
        "LR subsystems (learning rate, per doubling)",
        "Wright's Law anchor cum sats",
        "Wright's Law floor pct (of base subsystem cost)",
        "GPU effective-capacity degradation (per yr)",
        "Chip cost basis ($/TFLOPS, gen anchor @2025)",
        "Next-gen R&D uplift (peak, × extra R&D at gen jump)",
        "▸ AI: Orbital DC ops cost rates",
        "Gbps per GWh/yr",
        "BB-share of bandwidth (ratio)",
        "BB pool at-cost $/Gbps/yr",
        "DTC pool at-cost $/Gbps/yr",
        "Ground/network opex pct rev",
        "ODC insurance pct rev",
        "ODC other COGS pct rev",
        "▸ AI: Terrestrial DC",
        "Terrestrial $/MW build",
        "▸ AI: AI Apps",
        "AI Apps CAC ($/customer)",
        "AI Stack insurance pct rev",
        "AI Stack other COGS pct rev",
        "AI Apps GPU-hr per trillion tokens",
        "AI Apps tokens-per-query intensity CAGR",
        "▸ AI: R&D attribution glides",
        "ODC R&D start pct",
        "ODC R&D floor pct",
        "ODC R&D CAGR",
        "ODC pre-launch R&D ($mm/yr, 2025-27)",
        "AI Stack R&D start pct",
        "AI Stack R&D floor pct",
        "AI Stack R&D CAGR",
        "Terafab R&D start pct",
        "Terafab R&D floor pct",
        "Terafab R&D CAGR",
        "▸ AI: Terafab toggle",
        "Terafab toggle (1=NVIDIA-parity ON, 0=buy NVIDIA, 0.5=blend)",
        "▸ AI: Terafab chip-fab (→ Facilities Build, A4)",
        "Terafab fab CapEx (blended all-in $/wspm)",
        "Terafab capacity per fab phase (wspm/phase)",
        "Terafab fab useful life (depreciation, years)",
        "Terafab good chips per wspm per yr",
        "Terafab fab construction window (years)",
        "Terafab production cost frac (chip at-cost, → DC CapEx)",
        "▸ AI: year-row inputs (Cam G:AF → Group D:AC)",
        "GPU-hr price ($/GPU-hr)",
        "Utilization (%)",
        "Power cost ($/kWh)",
        "Allocation sharpness β: Starlink broadband / direct-to-cell sub-split",
        "▸ AI: Terafab JV split + calibration (A4.1)",
        "Terafab: SpaceX cost/capacity share (frac)",
        "▸ AI: AI Apps (consolidated, A2.2)",
        "⊘ REDUNDANT — AI Apps subs 2025 seed (M)",
        "⊘ REDUNDANT — AI Apps TAM (M subs)",
        "⊘ REDUNDANT — AI Apps adoption ceiling (% of TAM)",
        "⊘ REDUNDANT — AI Apps adoption steepness k",
        "⊘ REDUNDANT — AI Apps blended ARPU ($/sub/yr)",
        "⊘ REDUNDANT — AI Apps blended tokens per sub (M/sub/yr)",
        "AI Apps attributed compute capital per sub ($)",
        "Carve-out IRR-response start year",
        "Carve-out IRR-response high-IRR anchor (base % at/above)",
        "Carve-out IRR-response low-IRR anchor (ceiling % at/below)",
        "Carve-out IRR-response ceiling % (max carve-out at low anchor)",
        "▸ AI: exogenous cost CAGRs (CAM port, MC)",
        "GPU-hr price CAGR",
        "Power cost CAGR",
        "Terrestrial facility cost CAGR",
        "Demand curve escalator: taper end (yrs from 2025)",
        "▸ AI: external compute demand (A8 endogenisation)",
        "External compute 2025 seed (M H100-eq GPU)",
        "Compute build headroom buffer (frac)",
        "DTC TAM uplift target: Starlink Mobile premium (×)",
        "DTC TAM uplift ramp-end (yrs from 2025)",
        "▸ AI: chip improvement + lightweighting CAGRs (A8.1)",
        "Chip FP8 density CAGR (post-2030)",
        "Chip TDP CAGR (post-2027, W/chip)",
        "Chip cost-per-TFLOPS decline rate g (per-FLOP, A8.2)",
        "AI: ODC first compute-sat build year",
        "▸ AI: compute demand curve (A8.3)",
        "AI compute demand-curve elasticity b",
        "▸ ALLOCATOR: Terafab Construction Facility (debt layer)",
        "Terafab facility cap ($mm)",
        "Terafab facility interest rate (annual)",
        "Minimum cash buffer ($mm)",
        "FCF repayment sweep (% of excess FCF)",
        "Terafab facility repaid-by year",
        "Terafab facility draw-window end year",
        "BB TAM uplift target: data-intensity / value-per-connection (×)",
        "BB TAM uplift ramp-end (yrs from 2025)",
        "Max Starship build-capacity added per year (ships/yr)",
        "Starship build-capacity ceiling (ships/yr)",
        "▸ AI: orbital serving S-curve + training carve-out (A8.5)",
        "AI orbital compute TAM ceiling (M H100-eq GPU)",
        "AI orbital compute adoption steepness k",
        "Terrestrial training carve-out (% of prior-yr AI revenue)",
        "Allocation sharpness β: AI orbital / terrestrial sub-split",
        "▸ MISSING-CAPEX PROGRAMS",
        "Corporate, IT & HQ CapEx (% of Group revenue)",
        "Launch-site infra CapEx ($mm per annual launch of capacity)",
        "Starlink ground-network CapEx (% of Starlink revenue)",
        "Infrastructure useful life (years)",
        "Terminal kits per net subscriber add",
        "Terminal replacement rate (% installed/yr)",
        "▸ §A8.6: ODC THERMAL RECALIBRATION (kW/ton glide + dynamic TDP)",
        "[SUPERSEDED A8.7] ODC power density anchor 2025 (kW/ton)",
        "[SUPERSEDED A8.7] ODC power density target (kW/ton)",
        "ODC power density ramp-end year",
        "Chip perf-per-watt anchor 2025 (TFLOPS/W)",
        "Chip perf-per-watt CAGR (/yr)",
        "Chip FP8 per chip CAGR (/yr): smooth curve",
        "ODC sat-factory CapEx ($mm per sat/yr of capacity)",
        "Starship payload ramp plateau year",
        "▸ SoTP EV/EBITDA multiples (terminal, at horizon)",
        "Multiple: Starlink (EV/EBITDA at horizon)",
        "Multiple: Customer Launch (EV/EBITDA at horizon)",
        "Multiple: AI/Compute (EV/EBITDA at horizon)",
        "▸ AI: AI Apps demand uplift (un-flatten ARPU + tokens/sub)",
        "⊘ REDUNDANT — AI Apps blended ARPU CAGR (/yr)",
        "⊘ REDUNDANT — AI Apps tokens-per-sub CAGR (/yr)",
        "⊘ REDUNDANT — AI Apps tokens-per-sub growth cap (×)",
        "Launch demand price elasticity e (extra, on $/kg)",
        "Launch demand elasticity multiplier cap (x)",
        "Launch IRR slug working-capital % of build",
        "▸ §IRR allocation soft floor",
        "Allocator min softmax share floor per module (frac)",
        "Chip operating temp (K)",
        "Radiator delta-T (K)",
        "Radiator emissivity (0-1)",
        "Environmental heat load q_env (W/m²)",
        "Two-sided radiator factor",
        "Radiator areal density anchor 2025 (kg/m²)",
        "Radiator areal density mature (kg/m²)",
        "Heat transport anchor 2025 (kg/kW)",
        "Heat transport mature (kg/kW)",
        "Deployable area penalty (kg/m²)",
        "Solar specific power anchor 2025 (W/kg)",
        "Solar specific power mature (W/kg)",
        "Other non-thermal mass: bus+structure+compute (kg)",
        "Max Starship launch capacity (kg/yr ceiling): 0 = off",
        "▸ ALLOCATOR: ODC Construction Facility (debt layer)",
        "ODC construction facility cap ($mm)",
        "ODC facility interest rate (annual)",
        "ODC facility draw-window end year",
        "ODC facility repaid-by year",
        "ODC facility FCF repayment sweep (%)",
        "▸ AI: AI Apps 5-bucket demand build",
        "AIApps Free: users 2025 (M)",
        "AIApps Free: user CAGR (/yr)",
        "AIApps Free: ARPU ($/user/yr)",
        "AIApps Free: ARPU CAGR (/yr)",
        "AIApps Free: tokens/user 2025 (M/yr)",
        "AIApps Free: tokens/user CAGR (/yr)",
        "AIApps Indiv: users 2025 (M)",
        "AIApps Indiv: user CAGR (/yr)",
        "AIApps Indiv: ARPU ($/user/yr)",
        "AIApps Indiv: ARPU CAGR (/yr)",
        "AIApps Indiv: tokens/user 2025 (M/yr)",
        "AIApps Indiv: tokens/user CAGR (/yr)",
        "AIApps API: users 2025 (M)",
        "AIApps API: user CAGR (/yr)",
        "AIApps API: ARPU ($/acct/yr)",
        "AIApps API: ARPU CAGR (/yr)",
        "AIApps API: tokens/user 2025 (M/yr)",
        "AIApps API: tokens/user CAGR (/yr)",
        "AIApps Ent: seats 2025 (M)",
        "AIApps Ent: user CAGR (/yr)",
        "AIApps Ent: ARPU ($/seat/yr)",
        "AIApps Ent: ARPU CAGR (/yr)",
        "AIApps Ent: tokens/user 2025 (M/yr)",
        "AIApps Ent: tokens/user CAGR (/yr)",
        "AIApps Agentic: users 2025 (M)",
        "AIApps Agentic: user CAGR (/yr)",
        "AIApps Agentic: ARPU ($/user/yr)",
        "AIApps Agentic: ARPU CAGR (/yr)",
        "AIApps Agentic: tokens/user 2025 (M/yr)",
        "AIApps Agentic: tokens/user CAGR (/yr)",
        "AIApps Ads: ARPU ($/user/yr)",
        "AIApps Ads: ARPU CAGR (/yr)",
        "▸ AI: merchant-IaaS supply-share lever",
        "AIApps Merchant IaaS demand scale (×)",
    ),
    "Cash Allocation Engine": (
        "▸ CASH POOL: LIVE every year (2025 = starting cash $11,385M + $20B bridge)",
        "Cash BoY ($mm)",
        "IPO injection ($mm)",
        "Pre-IPO bridge loan ($mm)",
        "Cash available for year ($mm)",
        "▸ QUEUE GATE: LIVE every year",
        "Memo: Group revenue (claims base) ($mm)",
        "Corporate SG&A ($mm)",
        "Shared / unattributable R&D ($mm)",
        "Corporate CapEx ($mm)",
        "Spectrum licence fee ($mm)",
        "Taxes ($mm)",
        "Queue gate non-module claims total ($mm)",
        "Pool after queue gate ($mm)",
        "▸ CARVE-OUT: LIVE every year",
        "Lunar/Mars carve-out cash ($mm)",
        "Remaining pool for IRR-weighted allocation ($mm): gated to 0 in the 2025 anchor year; allocation operative 2026 onward",
        "▸ TOP-LEVEL IRR-WEIGHTED ALLOCATION: allocated cash = 0 in the 2025 anchor year; operative 2026→2050 (shares sum to 1)",
        "Spot IRR: Starlink",
        "Spot IRR: Customer Launch",
        "Spot IRR: AI-Compute",
        "exp(β·IRR): Starlink",
        "exp(β·IRR): Customer Launch",
        "exp(β·IRR): AI-Compute",
        "Σ exp(β·IRR)",
        "Allocation share: Starlink",
        "Allocation share: Customer Launch",
        "Allocation share: AI-Compute",
        "Memo: share sum (must=1)",
        "Allocated cash to Starlink ($mm)",
        "Allocated cash to Customer Launch ($mm)",
        "Allocated cash to AI-Compute ($mm)",
        "Memo: cash deployed by modules ($mm)",
        "Leftover cash ($mm)",
        "▸ KG-RATIONING GATE",
        "Memo: total kg demand (kg)",
        "LM kg reserved off-top (kg)",
        "Capacity available after LM (kg)",
        "kg-binding flag (1=capacity binds)",
        "Launch capacity allotment: Starlink (kg)",
        "Launch capacity allotment: Customer Launch (kg)",
        "Launch capacity allotment: AI-Compute (kg)",
        "▸ CASH EoY: LIVE every year; 2025 EoY feeds 2026 Cash BoY (the cash spine)",
        "Group FCF ($mm)",
        "Cash EoY ($mm)",
        "Memo: cumulative (Start+ΣIPO+ΣBridge+ΣFCF+Facility net) ($mm)",
        "▸ CONSERVATION",
        "Memo: carve-out tie (engine − LM receipt, must=0)",
        "Memo: VB fleet CapEx conservation (=VB R53)",
        "▸ CAPACITY-PRIORITY ALLOCATION",
        "Cap: Starlink max deployable ($mm)",
        "Cap: Customer Launch max deployable ($mm)",
        "Cap: AI-Compute max deployable ($mm)",
        "Rank key: Starlink",
        "Rank key: Customer Launch",
        "Rank key: AI-Compute",
        "Higher-rank caps ahead of Starlink ($mm)",
        "Higher-rank caps ahead of Customer Launch ($mm)",
        "Higher-rank caps ahead of AI-Compute ($mm)",
        "Placeholder AI/strategic CapEx ($mm): TEMP (retire when AI-Compute loaded)",
        "▸ LEVEL-2: WITHIN-AI ODC vs TERRESTRIAL SPLIT (A7)",
        "Spot IRR: ODC (prior yr)",
        "Spot IRR: Terrestrial (prior yr)",
        "exp(β·IRR): ODC",
        "exp(β·IRR): Terrestrial",
        "Σ exp: within-AI",
        "Allocation share: orbital (ODC)",
        "Allocation share: terrestrial",
        "Memo: within-AI share sum (=1)",
        "Desired cash → ODC ($mm)",
        "Desired cash → Terrestrial ($mm)",
        "Memo: ODC kg-buildable (diagnostic: unused after A7.1)",
        "Allocated cash → ODC ($mm)",
        "Memo: ODC→Terr spillover ($mm): A8.3 (consumed by R114)",
        "Allocated cash → Terrestrial ($mm)",
        "Memo: AI kg ration (diagnostic: ODC self-supplies, A7.1)",
        "Memo: chip-supply check (soft)",
        "Conservation: Level-2 cash tie: allocated ≤ desired, no creation (≥0 = OK), A8.3",
        "Memo: Terr→ODC spillover ($mm): A8.3 (consumed by R112)",
        "▸ CARVE-OUT IRR RESPONSE (operative 2030 onward)",
        "Carve-out IRR signal: avg prior-yr spot IRR (3 modules)",
        "Carve-out IRR-response ramp [0,1]",
        "Carve-out effective % (IRR-responsive)",
        "Desired launch kg: Starlink",
        "Desired launch kg: Customer Launch",
        "Desired launch kg: AI-Compute",
        "Total desired launch kg",
        "▸ TERAFAB CONSTRUCTION FACILITY (debt layer)",
        "Terafab CapEx to fund ($mm)",
        "Facility draw ($mm)",
        "Facility interest ($mm)",
        "Facility repayment ($mm)",
        "Facility balance EoY ($mm)",
        "Memo: cumulative draws ($mm)",
        "Memo: cumulative repayments ($mm)",
        "Conservation: Σdraw − Σrepay − balance (must = 0)",
        "▸ ABSORPTIVE-CAPACITY WATER-FILL (top-level, A-refresh V4.102)",
        "Desired cash: Starlink ($mm)",
        "Desired cash: Customer Launch ($mm)",
        "Desired cash: AI-Compute ($mm)",
        "Capped: Starlink ($mm)",
        "Capped: Customer Launch ($mm)",
        "Capped: AI-Compute ($mm)",
        "Water-fill residual ($mm)",
        "Headroom: Starlink ($mm)",
        "Headroom: Customer Launch ($mm)",
        "Headroom: AI-Compute ($mm)",
        "Spillover weight: Starlink",
        "Spillover weight: Customer Launch",
        "Spillover weight: AI-Compute",
        "Σ spillover weight",
        "Allocated final: Starlink ($mm)",
        "Allocated final: Customer Launch ($mm)",
        "Allocated final: AI-Compute ($mm)",
        "▸ ODC CONSTRUCTION FACILITY (debt layer — funds ODC sat rollout)",
        "ODC CapEx need ($mm): launch-feasible deploy × cost",
        "ODC pool allocation ($mm)",
        "ODC facility draw ($mm)",
        "ODC facility interest ($mm)",
        "ODC facility repayment ($mm)",
        "ODC facility balance EoY ($mm)",
        "Memo: ODC cum draws ($mm)",
        "Memo: ODC cum repayments ($mm)",
        "Conservation: ODC Σdraw − Σrepay − balance (must = 0)",
    ),
    "Conservation": (
        "CONSERVATION: identity checks",
        "Revenue tie",
        "EBITDA foot",
        "D&A + Lunar-Mars book-value guard",
        "EBIT consistency",
        "Accrual↔cash FCF reconciliation",
        "FCF foot vs NOPAT+D&A−CapEx walk",
        "Cash-flow identity",
        "Elimination conservation (Rule 21)",
        "ALL OK (R108-equivalent)",
        "Memo: Σ Group FCF cumulative (Rule 23 yr-chained)",
        "Memo: normalization delta (accrual walk − normalized walk) ($mm)",
    ),
    "Customer Launch": (
        "Customer Launch module — module = Space segment · 2-stream revenue $4,086M · full waterfall, R&D above EBITDA · separate F9 + Starship D&A · Spot IRR · per-launch D&A interface",
        "YEAR",
        "Year offset",
        "▸ BLOCK A: ALLOCATOR IN (cross-tab reads)",
        "F9 internal launches per year (Starlink-driven)",
        "Starship internal launches per year (Starlink-driven)",
        "F9 customer launch price ($mm/launch)",
        "Starship customer launch price ($mm/launch)",
        "Commercial launch market size ($mm/yr)",
        "Government launch market size ($mm/yr)",
        "SpaceX commercial market share",
        "SpaceX government market share",
        "Launch & Development revenue ($mm/yr)",
        "Starship commercial-readiness factor",
        "F9 at-cost rate per launch ($mm)",
        "Starship at-cost rate per launch ($mm)",
        "F9 booster build cost ($mm)",
        "Starship vehicle build cost ($mm)",
        "F9 cadence per booster (flights/yr)",
        "Starship cadence per vehicle (flights/yr)",
        "F9 vehicle life L (years)",
        "Starship vehicle life L (years)",
        "Group WACC",
        "Customer Launch R&D % (start)",
        "Customer Launch R&D % (floor)",
        "Customer Launch R&D % (CAGR)",
        "Launch / vehicle facility CapEx ($mm)",
        "Launch / vehicle facility D&A ($mm)",
        "▸ BLOCK B: LAUNCH DEMAND & FLEET BUILD",
        "External commercial launch demand (count)",
        "External government launch demand (count)",
        "F9 boosters built (yr)",
        "F9 boosters retired (yr)",
        "F9 booster fleet EoY",
        "F9 total launch capacity (launches/yr)",
        "F9 customer launches (residual)",
        "Starship target launches (internal + commercial demand)",
        "Starship vehicles built (yr)",
        "Starship vehicle fleet EoY",
        "Starship total capacity (launches/yr)",
        "Starship commercial launches",
        "Memo: total external launches",
        "▸ BLOCK C: REVENUE (external only)",
        "Launch Services revenue ($mm)",
        "Launch & Development revenue ($mm)",
        "Revenue   ◄ Allocator OUT",
        "Memo: avg $/launch (LS)",
        "Memo: F9 price set to $54.8M lands 2025 Launch Services = $2,575.6M (target $2,576M) + Launch & Delivery $1,510M → revenue $4,085.6M ≈ S-1 Space $4,086M.",
        "▸ BLOCK D: COGS → GROSS PROFIT",
        "Variable launch cost: F9 ($mm)",
        "Variable launch cost: Starship ($mm)",
        "Launch insurance ($mm)",
        "Other launch COGS ($mm)",
        "COGS total ($mm)   ◄ Allocator OUT",
        "Gross Profit ($mm)   ◄ Allocator OUT",
        "Memo: Gross Margin %",
        "▸ BLOCK E: MODULE OpEx + R&D → MODULE EBITDA (R&D ABOVE EBITDA, Hard Rule 7)",
        "Selling, general & administrative ($mm)",
        "Module OpEx total ($mm)   ◄ Allocator OUT",
        "Attributed R&D ($mm)   ◄ Allocator OUT",
        "Module EBITDA ($mm)   ◄ Allocator OUT",
        "Memo: EBITDA Margin %",
        "▸ BLOCK F: EBITDA → EBIT (only D&A below EBITDA)",
        "F9 owned-vehicle D&A ($mm)",
        "Starship owned-vehicle D&A ($mm)",
        "Launch / facility D&A ($mm)",
        "D&A total ($mm)   ◄ Allocator OUT",
        "Module EBIT ($mm)   ◄ Allocator OUT",
        "▸ BLOCK G: CAPEX → MODULE FCF",
        "F9 owned-vehicle build CapEx ($mm)   ◄ Allocator OUT",
        "Starship owned-vehicle build CapEx ($mm)   ◄ Allocator OUT",
        "Ground/facility CapEx ($mm)   ◄ Allocator OUT",
        "Working capital ΔWC ($mm)   ◄ Allocator OUT",
        "Module CapEx total ($mm)   ◄ Allocator OUT",
        "Module FCF ($mm)   ◄ Allocator OUT",
        "▸ BLOCK H: PER-VEHICLE IRR ENGINE (v4 canonical, Spot only)",
        "F9: revenue per vehicle per yr ($mm)",
        "F9: margin per vehicle per yr ($mm, ex-D&A)",
        "F9: CapEx slug per vehicle ($mm)",
        "F9 Spot IRR (reporting only, excluded from allocation)",
        "Starship: revenue per vehicle per yr ($mm)",
        "Starship: margin per vehicle per yr ($mm, ex-D&A)",
        "Starship: CapEx slug per vehicle ($mm)",
        "Starship Spot IRR (competes in the IRR-weighted allocation)",
        "Module Spot IRR   ◄ Allocator OUT",
        "▸ BLOCK I: ALLOCATOR OUT (amended canonical labels)",
        "Revenue",
        "COGS total",
        "Gross Profit",
        "Module OpEx",
        "Attributed R&D",
        "Module EBITDA",
        "D&A",
        "Module EBIT",
        "F9 owned-vehicle build CapEx",
        "Starship owned-vehicle build CapEx",
        "Ground/facility CapEx",
        "Working capital ΔWC",
        "Module CapEx",
        "Module FCF",
        "Kg demand year N+1",
        "Spot marginal IRR",
        "Capital Deployed (cumulative)",
        "F9 owned-vehicle D&A per launch ($mm)            ◄ interface to Starlink",
        "Starship owned-vehicle D&A per launch ($mm)      ◄ interface to Starlink",
        "▸ BLOCK J, CONSERVATION MEMOS (verification only, excl. sums)",
        "Memo: reclassification conservation",
        "Memo: P&L↔IRR operating-margin",
        "Memo: R&D dual-track divergence",
        "Memo: 2025 revenue reconciliation",
        "Memo: 2025 EBIT reconciliation",
        "Memo: 2025 D&A reconciliation",
        "Memo: 2025 CapEx reconciliation",
        "▸ INTERFACE ALIASES (label-fidelity for downstream tabs)",
        "F9 customer launches per year",
        "Starship customer launches per year",
        "Owned launch-vehicle CapEx ($mm)",
        "Memo: cum launch-site infra CapEx ($mm)",
        "Memo: cum active launch vehicles (F9 + Starship)",
        "Memo: launch-infra allocable per vehicle ($mm)",
        "Memo: best-available launch $/kg index ($mm/kg, readiness-blended)",
        "Memo: launch demand elasticity multiplier (x)",
        "Memo: expanded commercial launch $TAM ($mm, elastic — baseline row 13 × multiplier)",
        "Memo: expanded government launch $TAM ($mm, elastic — baseline row 14 × multiplier)",
        "Memo: SpaceX Launch-Services rev as % of expanded $TAM (coherence check, must be <100%)",
    ),
    "Demand Curves": (
        "Demand Curves: Starlink BB + DTC piecewise-linear lookup",
        "Lookup form: INDEX/MATCH(..., 1) bracket-find + manual linear interp. NO FORECAST / TREND. Per Memory Snapshot v3 §2.4.",
        "DTC DEMAND CURVE (piecewise-linear Q→Revenue lookup)",
        "Constellation Bandwidth (Gbps)",
        "DTC Q breakpoint #1 (Gbps)",
        "DTC Q breakpoint #2 (Gbps)",
        "DTC Q breakpoint #3 (Gbps)",
        "DTC Q breakpoint #4 (Gbps)",
        "DTC Q breakpoint #5 (Gbps)",
        "DTC Q breakpoint #6 (Gbps)",
        "DTC Q breakpoint #7 (Gbps)",
        "DTC Q breakpoint #8 (Gbps)",
        "DTC Q breakpoint #9 (Gbps)",
        "DTC Q breakpoint #10 (Gbps)",
        "DTC Q breakpoint #11 (Gbps)",
        "DTC Q breakpoint #12 (Gbps)",
        "DTC Q breakpoint #13 (Gbps)",
        "DTC Q breakpoint #14 (Gbps)",
        "DTC Q breakpoint #15 (Gbps)",
        "DTC Q breakpoint #16 (Gbps)",
        "DTC Q breakpoint #17 (Gbps)",
        "DTC Q breakpoint #18 (Gbps)",
        "DTC Q breakpoint #19 (Gbps)",
        "DTC Q breakpoint #20 (Gbps)",
        "DTC Q breakpoint #21 (Gbps)",
        "DTC Q breakpoint #22 (Gbps)",
        "DTC Q breakpoint #23 (Gbps)",
        "DTC Q breakpoint #24 (Gbps)",
        "DTC Q breakpoint #25 (Gbps)",
        "DTC Q breakpoint #26 (Gbps)",
        "DTC Q breakpoint #27 (Gbps)",
        "DTC Q breakpoint #28 (Gbps)",
        "DTC Q breakpoint #29 (Gbps)",
        "DTC Q breakpoint #30 (Gbps)",
        "DTC Q breakpoint #31 (Gbps)",
        "DTC Q breakpoint #32 (Gbps)",
        "DTC Q breakpoint #33 (Gbps)",
        "DTC Q breakpoint #34 (Gbps)",
        "DTC Q breakpoint #35 (Gbps)",
        "DTC Q breakpoint #36 (Gbps)",
        "DTC Q breakpoint #37 (Gbps)",
        "DTC Q breakpoint #38 (Gbps)",
        "DTC Q breakpoint #39 (Gbps)",
        "DTC Q breakpoint #40 (Gbps)",
        "DTC Q breakpoint #41 (Gbps)",
        "DTC Q breakpoint #42 (Gbps)",
        "DTC Q breakpoint #43 (Gbps)",
        "DTC Q breakpoint #44 (Gbps)",
        "DTC Q breakpoint #45 (Gbps)",
        "DTC Q breakpoint #46 (Gbps)",
        "DTC Q breakpoint #47 (Gbps)",
        "DTC Q breakpoint #48 (Gbps)",
        "DTC Q breakpoint #49 (Gbps)",
        "DTC Q breakpoint #50 (Gbps)",
        "DTC Q breakpoint #51 (Gbps)",
        "DTC Q breakpoint #52 (Gbps)",
        "DTC Q breakpoint #53 (Gbps)",
        "DTC Q breakpoint #54 (Gbps)",
        "DTC Q breakpoint #55 (Gbps)",
        "DTC Q breakpoint #56 (Gbps)",
        "DTC Q breakpoint #57 (Gbps)",
        "DTC Q breakpoint #58 (Gbps)",
        "DTC Q breakpoint #59 (Gbps)",
        "DTC Q breakpoint #60 (Gbps)",
        "DTC Q breakpoint #61 (Gbps)",
        "BB DEMAND CURVE (piecewise-linear Q→Revenue lookup)",
        "Capacity (Gbps)",
        "BB Q breakpoint #1 (Gbps)",
        "BB Q breakpoint #2 (Gbps)",
        "BB Q breakpoint #3 (Gbps)",
        "BB Q breakpoint #4 (Gbps)",
        "BB Q breakpoint #5 (Gbps)",
        "BB Q breakpoint #6 (Gbps)",
        "BB Q breakpoint #7 (Gbps)",
        "BB Q breakpoint #8 (Gbps)",
        "BB Q breakpoint #9 (Gbps)",
        "BB Q breakpoint #10 (Gbps)",
        "BB Q breakpoint #11 (Gbps)",
        "BB Q breakpoint #12 (Gbps)",
        "BB Q breakpoint #13 (Gbps)",
        "BB Q breakpoint #14 (Gbps)",
        "BB Q breakpoint #15 (Gbps)",
        "BB Q breakpoint #16 (Gbps)",
        "BB Q breakpoint #17 (Gbps)",
        "BB Q breakpoint #18 (Gbps)",
        "BB Q breakpoint #19 (Gbps)",
        "BB Q breakpoint #20 (Gbps)",
        "BB Q breakpoint #21 (Gbps)",
        "BB Q breakpoint #22 (Gbps)",
        "BB Q breakpoint #23 (Gbps)",
        "BB Q breakpoint #24 (Gbps)",
        "BB Q breakpoint #25 (Gbps)",
        "BB Q breakpoint #26 (Gbps)",
        "BB Q breakpoint #27 (Gbps)",
        "BB Q breakpoint #28 (Gbps)",
        "BB Q breakpoint #29 (Gbps)",
        "BB Q breakpoint #30 (Gbps)",
        "BB Q breakpoint #31 (Gbps)",
        "BB Q breakpoint #32 (Gbps)",
        "BB Q breakpoint #33 (Gbps)",
        "BB Q breakpoint #34 (Gbps)",
        "BB Q breakpoint #35 (Gbps)",
        "BB Q breakpoint #36 (Gbps)",
        "BB Q breakpoint #37 (Gbps)",
        "BB Q breakpoint #38 (Gbps)",
        "BB Q breakpoint #39 (Gbps)",
        "BB Q breakpoint #40 (Gbps)",
        "BB Q breakpoint #41 (Gbps)",
        "BB Q breakpoint #42 (Gbps)",
        "BB Q breakpoint #43 (Gbps)",
        "BB Q breakpoint #44 (Gbps)",
        "BB Q breakpoint #45 (Gbps)",
        "BB Q breakpoint #46 (Gbps)",
        "BB Q breakpoint #47 (Gbps)",
        "BB Q breakpoint #48 (Gbps)",
        "BB Q breakpoint #49 (Gbps)",
        "BB Q breakpoint #50 (Gbps)",
        "BB Q breakpoint #51 (Gbps)",
        "BB Q breakpoint #52 (Gbps)",
        "BB Q breakpoint #53 (Gbps)",
        "BB Q breakpoint #54 (Gbps)",
        "BB Q breakpoint #55 (Gbps)",
        "BB Q breakpoint #56 (Gbps)",
        "▸ Curve evaluators (year-row, read by the Starlink module)",
        "Annual TAM shift multiplier",
        "Starlink BB capacity input (Gbps)",
        "Starlink DTC capacity input (Gbps)",
        "Starlink BB Revenue from curve ($mm)",
        "Starlink DTC Revenue from curve ($mm)",
        "Memo: Average $/Gbps BB from curve",
        "Memo: Average $/Gbps DTC from curve",
        "Annual escalator rate (derived, year-row)",
        "DTC TAM uplift multiplier (Starlink Mobile, derived year-row)",
        "BB TAM uplift multiplier (data-intensity, derived year-row)",
    ),
    "Facilities Build": (
        "Facilities Build: capacity-step facility CapEx engine",
        "7 buckets: sat-mfg (Redmond), Starship-vehicle (Gigabay @100/yr), pads, engines, terminals (toggle-OFF), ground stations, HQ→Group. Exposes CapEx + D&A totals by label.",
        "▸ SATELLITE-MFG FACILITY ENGINE (Redmond)",
        "Sats built: Starlink (sats/yr)",
        "Installed sat-factory capacity (sats/yr): EoY ratchet, ≥ current build",
        "Sat-factory capacity ratio",
        "New sat-factory CapEx this year ($mm)",
        "Ground stations built this year",
        "Ground station CapEx this year ($mm)",
        "Sat-mfg facility CapEx total ($mm)  ◄ Starlink",
        "Sat-mfg facility D&A ($mm)  ◄ Starlink",
        "▸ STARSHIP PRODUCTION FACILITY (Starfactory/Gigabay): capacity + scaling",
        "Ships built this year (= Vehicle Build Ships built (fleet), unified)",
        "Installed Starship build capacity (ships/yr): rate-limited ramp",
        "New Starship build-capacity added (ships/yr)",
        "New Gigabay CapEx this year ($mm)",
        "Engines demanded this year (= ships × engines/vehicle)",
        "New engine-facility CapEx this year ($mm)",
        "Launch pads needed (= Starship launches ÷ launches/pad)",
        "New launch-pad CapEx this year ($mm)",
        "Launch/vehicle facility CapEx total ($mm)  ◄ launch/vehicle",
        "Launch/vehicle facility D&A total ($mm)  ◄ launch/vehicle",
        "Installed engine-facility capacity (engines/yr): EoY ratchet, ≥ current demand, memo",
        "Installed launch pads (Starship): cumulative, ≥ base, memo",
        "▸ TERMINALS (Bastrop): toggle-gated",
        "Terminal kits demanded this year (placeholder: Gbps-growth scaled)",
        "New terminal-factory CapEx this year ($mm) × toggle",
        "Terminal facility D&A ($mm) × toggle  ◄ Starlink",
        "Installed terminal-factory capacity (kits/yr): cumulative, memo",
        "▸ HQ FACILITY (CORPORATE → GROUP)",
        "Group revenue base ($mm): placeholder (Starlink rev; swap to Group total in 4.5)",
        "HQ facility CapEx ($mm)  ◄ Group P&L",
        "HQ facility D&A ($mm)  ◄ Group P&L",
        "▸ CONSERVATION + CALIBRATION",
        "Total facility CapEx ($mm) = sat-mfg + launch/vehicle + terminal + HQ",
        "Conservation: max bucket (cum D&A − cum CapEx): must be ≤ 0",
        "Memo: satellite-manufacturing CapEx (2025 ≈ $200M reference)",
        "Memo: launch/vehicle CapEx (2025 ≈ $593M reference; low today: Starship ships = 0)",
        "Memo: HQ CapEx (2025 ≈ $53M reference)",
        "Top-down sanity: Total facility CapEx vs S-1 2025 SpaceX capex $8,000M (must be a fraction)",
        "Top-down sanity ex-chip-fab: (Total − chip-fab) vs S-1 2025 capex",
        "▸ STARFACTORY: initial production facility (base capacity, one-time)",
        "Starfactory CapEx this year ($mm)",
        "Starfactory D&A ($mm)",
        "Boosters built this year (= Vehicle Build Boosters built (fleet))",
        "Total Starship airframes built (booster + ship)",
        "▸ CHIP-FAB FACILITY ENGINE (Terafab)",
        "Chips demanded this year (count)  ◄ AI-Compute",
        "Required fab capacity (wspm)",
        "Installed fab capacity (wspm): EoY ratchet / phase step",
        "New fab capacity added (wspm)",
        "Fab slug cost (online-year, $mm)",
        "New fab CapEx this year ($mm): 3yr window spread",
        "Chip-fab facility CapEx total ($mm)  ◄ AI-Compute",
        "Chip-fab facility D&A total ($mm)  ◄ AI-Compute",
        "Conservation: fab chips − DC chips×toggle; must = 0",
        "Memo: DC chips deployed (ODC R55 + Terr R94)",
        "Memo: full JV fab CapEx (100%, pre-share) ($mm)",
        "Memo: Tesla-funded fab CapEx ((1−share)) ($mm)",
        "▸ MISSING-CAPEX BUCKETS (prior-year-driven; 2025 = current-year anchor)",
        "Corporate, IT & HQ CapEx ($mm)",
        "Launch-infra capacity installed (launches/yr)",
        "Launch-site infrastructure CapEx ($mm)",
        "Starlink ground-network CapEx ($mm)",
        "RETIRED (orbital-data-centre ground stations installed)",
        "RETIRED (orbital-data-centre ground stations CapEx)",
        "Memo: Σ new infrastructure CapEx ex-terminal ($mm)",
        "Corporate & infrastructure CapEx total ($mm)",
        "Corporate & infrastructure D&A total ($mm)",
        "ODC sats built: driver (sats/yr)",
        "ODC sat-factory capacity installed (sats/yr): EoY ratchet",
        "ODC sat-mfg facility CapEx ($mm)  ◄ infra/Group",
    ),
    "Group P&L": (
        "GROUP P&L: segment consolidation",
        "▸ REVENUE ($mm)",
        "Revenue: Starlink",
        "Revenue: Customer Launch",
        "Revenue: AI - Compute",
        "Revenue: Lunar - Mars",
        "less inter-module eliminations",
        "Group Revenue ($mm)",
        "▸ COGS ($mm)",
        "COGS: Starlink",
        "COGS: Customer Launch",
        "COGS: AI - Compute",
        "COGS: Lunar - Mars",
        "Group COGS ($mm)",
        "▸ GROSS PROFIT ($mm)",
        "Gross Profit: Starlink",
        "Gross Profit: Customer Launch",
        "Gross Profit: AI - Compute",
        "Gross Profit: Lunar - Mars",
        "Group Gross Profit ($mm)",
        "▸ MODULE OpEx: direct ($mm)",
        "Module OpEx: Starlink",
        "Module OpEx: Customer Launch",
        "Module OpEx: AI - Compute",
        "Module OpEx: Lunar - Mars",
        "Total Module OpEx ($mm)",
        "▸ R&D ($mm)",
        "Memo: Attributed R&D, Starlink (now in Module OpEx; excl. from Total R&D)",
        "Attributed R&D: Customer Launch (Starship R&D lifted to Shared)",
        "Attributed R&D: AI - Compute",
        "Attributed R&D: Lunar - Mars",
        "Shared / unattributable R&D: corporate (incl Starship platform R&D)",
        "Total R&D ($mm)",
        "▸ CORPORATE OpEx ($mm)",
        "Corporate SG&A",
        "Spectrum licence fee",
        "Total corporate OpEx ($mm)",
        "▸ EBITDA: by segment ($mm)",
        "EBITDA: Starlink",
        "EBITDA: Customer Launch",
        "EBITDA: AI - Compute",
        "EBITDA: Lunar - Mars",
        "EBITDA: Corporate",
        "Group EBITDA ($mm)",
        "▸ D&A ($mm)",
        "D&A: Starlink",
        "D&A: Customer Launch",
        "D&A: AI - Compute",
        "D&A: Lunar - Mars",
        "D&A: Corporate / facilities",
        "Group D&A ($mm)",
        "▸ EBIT: by segment ($mm)",
        "EBIT: Starlink",
        "EBIT: Customer Launch",
        "EBIT: AI - Compute",
        "EBIT: Lunar - Mars",
        "EBIT: Corporate",
        "Group EBIT ($mm)",
        "▸ TAXES & NOPAT ($mm)",
        "Group Taxes ($mm)",
        "NOPAT ($mm)",
        "▸ CAPEX ($mm)",
        "CapEx: Starlink",
        "CapEx: Customer Launch",
        "CapEx: AI - Compute",
        "CapEx: Lunar - Mars",
        "CapEx: Corporate",
        "Group CapEx: accrual ($mm)",
        "▸ FREE CASH FLOW: by segment ($mm)",
        "FCF: Starlink",
        "FCF: Customer Launch (ex-Starship R&D; lifted to corporate)",
        "FCF: AI - Compute",
        "FCF: Lunar - Mars",
        "FCF: less corporate (SG&A+shared R&D+spectrum+taxes+corp CapEx)",
        "Group FCF: accrual walk ($mm)",
        "Memo: AI placeholder strategic CapEx ($mm): engine, TEMP",
        "Memo: Engine cash Group FCF ($mm)",
        "Group FCF: normalized walk (NOPAT+D&A−CapEx) ($mm)",
        "▸ INTER-MODULE ELIMINATIONS (Rule 21: $0 in current build)",
        "Internal launch services: RETIRED by 4.5 inversion",
        "Internal bandwidth eliminated, ODC→Starlink",
        "Internal compute eliminated, ODC→AI",
        "Total inter-module eliminations ($mm)",
        "▸ SoTP TERMINAL MEMO",
        "Lunar+Mars Net Book Value ($mm)",
        "(retired)",
        "▸ DIAGNOSTIC: 2025 vs Q4'25 anchors (narrow-gate, non-halt)",
        "Memo: Group EBITDA 2025 variance vs $8,690M",
        "Memo: Group D&A 2025 variance vs $1,060M",
        "Memo: Group FCF 2025 variance vs $3,670M",
        "Memo: AI EBITDA tie: Group EBITDA-AI (R54) − module ('AI - Compute' R169+R168); must = 0",
    ),
    "Launch Dashboard": (
        "Launch Dashboard — actual launches flown, by module, per year",
        "Read-only. Direct pulls from module tabs. Each module row is the realized (capped) launch count; total = their sum.",
        "▸ STARSHIP LAUNCHES FLOWN (count/yr)",
        "Starlink (internal)",
        "Customer Launch (commercial)",
        "AI-Compute / ODC",
        "Lunar / Mars",
        "Total Starship launches",
        "▸ MODULE SHARE OF STARSHIP LAUNCHES (%)",
        "Starlink",
        "Customer Launch",
        "▸ F9 LAUNCHES FLOWN (count/yr) — legacy, winding down",
        "Starlink (internal) F9",
        "Customer Launch F9",
        "Total F9 launches",
        "▸ TOTAL LAUNCHES, ALL VEHICLES (count/yr)",
        "Starship",
        "F9",
        "Grand total",
    ),
    "Lunar - Mars": (
        "▸ INPUTS READ FROM ASSUMPTIONS",
        "Carve-out % of prior-year Group FCF",
        "Carve-out floor ($mm/yr)",
        "Carve-out pre-2028 R&D-only override ($mm/yr)",
        "First mission year (Lunar Mars)",
        "Capital lifetime: BV straight-line dep (yrs)",
        "Mission ops cost: Lunar (% of Lunar CapEx)",
        "Mission ops cost: Mars (% of Mars CapEx)",
        "Labour unit mass (kg)",
        "Labour unit base hourly output ($/hr)",
        "Labour unit daily working hours",
        "Labour unit productivity factor",
        "Labour unit productivity learning rate (%/yr)",
        "Labour unit useful life (yrs)",
        "Lunar payload per surface-landed Starship (kg)",
        "Lunar % payload as labour units",
        "Mars payload per surface-landed Starship (kg)",
        "Mars % payload as labour units",
        "Labour unit cost ($/unit)",
        "Hardware value-add ($/kg landed)",
        "▸ CARVE-OUT CASH RECEIPT (taken off the top, before the IRR allocation)",
        "Memo: (retired: carve-out computed on Cash Allocation Engine R24)",
        "Carve-out cash receipt ($mm)",
        "▸ PER-SHIP COST BUILD",
        "Lunar labour mass per ship (kg)",
        "Lunar hardware mass per ship (kg)",
        "Lunar labour units per ship (count)",
        "Per-ship cost: Lunar ($mm/ship)",
        "Mars labour mass per ship (kg)",
        "Mars hardware mass per ship (kg)",
        "Mars labour units per ship (count)",
        "Per-ship cost: Mars ($mm/ship)",
        "▸ LUNAR MISSION DEPLOYMENT (first-mission-year gated)",
        "Lunar share of carve-out cash (year-row)",
        "Lunar carve-out cash this year ($mm)",
        "Lunar surface missions deployed (count)",
        "Lunar labour mass landed this year (kg)",
        "Lunar hardware mass landed this year (kg)",
        "Lunar labour units landed this year (count)",
        "▸ MARS MISSION DEPLOYMENT (first-mission-year gated)",
        "Mars share of carve-out cash (year-row)",
        "Mars carve-out cash this year ($mm)",
        "Mars surface missions deployed (count)",
        "Mars labour mass landed this year (kg)",
        "Mars hardware mass landed this year (kg)",
        "Mars labour units landed this year (count)",
        "▸ BV ENGINE: SoTP / VALUATION TRACK (off-P&L)",
        "Labour annual output per unit, base year ($mm/yr)",
        "Productivity multiplier (year-row, anchor-offset)",
        "Labour annual output per unit this year ($mm/yr)",
        "LUNAR labour units retired this year (cohort lookback)",
        "MARS labour units retired this year (cohort lookback)",
        "LUNAR active labour fleet EoY (running sum, net retire)",
        "MARS active labour fleet EoY (running sum, net retire)",
        "LUNAR annual production output ($mm/yr)",
        "MARS annual production output ($mm/yr)",
        "LUNAR annual hardware value-add ($mm/yr)",
        "MARS annual hardware value-add ($mm/yr)",
        "LUNAR annual BV contribution ($mm/yr)",
        "MARS annual BV contribution ($mm/yr)",
        "LUNAR economic-output proxy ($mm): MEMO ONLY, NOT used in valuation",
        "MARS economic-output proxy ($mm): MEMO ONLY, NOT used in valuation",
        "Memo: Total Lunar + Mars Accumulated BV ($mm): SoTP terminal input",
        "▸ LUNAR–MARS REPORTED P&L",
        "Total Revenue ($mm)",
        "Attributed R&D ($mm)",
        "Mission ops cost: Lunar ($mm)",
        "Mission ops cost: Mars ($mm)",
        "Module OpEx ($mm)",
        "Module CapEx ($mm)",
        "Cumulative Module CapEx ($mm)",
        "Lunar Mars Module D&A ($mm)",
        "Cumulative Module D&A ($mm)",
        "Σ-D&A ≤ Σ-CapEx check (1=OK)",
        "Module EBIT ($mm)",
        "Module CapEx (FCF input) ($mm)",
        "Module FCF ($mm)",
        "Module EBITDA Margin %",
        "▸ MEMO / DIAGNOSTICS",
        "Memo: Lunar surface missions cumulative",
        "Memo: Mars surface missions cumulative",
        "Memo: Carve-out reserved vs Module CapEx gap ($mm)",
        "Memo: Total Lunar+Mars kg landed this year",
        "▸ INTERFACE CONTRACT (exposed labels)",
        "Revenue ($mm)",
        "Spot marginal IRR",
        "Kg demand year N+1 (off-the-top reservation)",
        "Lunar+Mars Net Book Value ($mm): SoTP terminal (cumCapEx − cum D&A)",
        "(retired: NBV reported as total on R115; output-BV memo on R76/R77)",
        "▸ VEHICLE BUILD EXPOSURES (added 2026-06-01: resolve VB fleet pulls; canonical uniform labels)",
        "Kg demand year N+1",
        "Starship launches per year (Lunar/Mars)",
    ),
    "Segment P&L": (
        "Segment P&L — full Group waterfall with revenue broken to module sub-segments (read-only presentation; ties to Group P&L)",
        "▸ REVENUE — SEGMENT SUB-LINES ($mm)",
        "Revenue: Starlink — Broadband (BB)",
        "Revenue: Starlink — Direct-to-Cell (DTC)",
        "Revenue: Starlink — Starshield",
        "Revenue: Starlink — Hardware / kit",
        "Subtotal: Starlink Revenue ($mm)",
        "Revenue: Customer Launch — Launch Services",
        "Revenue: Customer Launch — Launch & Development",
        "Subtotal: Customer Launch Revenue ($mm)",
        "Revenue: AI - Compute — Orbital DC (external)",
        "Revenue: AI - Compute — Terrestrial DC (external)",
        "Revenue: AI - Compute — AI Apps (external)",
        "Subtotal: AI - Compute Revenue ($mm)",
        "Revenue: Lunar - Mars",
        "Subtotal: Lunar - Mars Revenue ($mm)",
        "less inter-module eliminations",
        "Group Revenue ($mm)",
        "▸ COGS ($mm)",
        "COGS: Starlink",
        "COGS: Customer Launch",
        "COGS: AI - Compute",
        "COGS: Lunar - Mars",
        "Group COGS ($mm)",
        "▸ GROSS PROFIT ($mm)",
        "Gross Profit: Starlink",
        "Gross Profit: Customer Launch",
        "Gross Profit: AI - Compute",
        "Gross Profit: Lunar - Mars",
        "Group Gross Profit ($mm)",
        "▸ MODULE OpEx: direct ($mm)",
        "Module OpEx: Starlink",
        "Module OpEx: Customer Launch",
        "Module OpEx: AI - Compute",
        "Module OpEx: Lunar - Mars",
        "Total Module OpEx ($mm)",
        "▸ R&D ($mm)",
        "Memo: Attributed R&D, Starlink (in Module OpEx; excl. Total R&D)",
        "Attributed R&D: Customer Launch",
        "Attributed R&D: AI - Compute",
        "Attributed R&D: Lunar - Mars",
        "Shared / unattributable R&D: corporate",
        "Total R&D ($mm)",
        "▸ CORPORATE OpEx ($mm)",
        "Corporate SG&A",
        "Spectrum licence fee",
        "Total corporate OpEx ($mm)",
        "▸ EBITDA: by segment ($mm)",
        "EBITDA: Starlink",
        "EBITDA: Customer Launch",
        "EBITDA: AI - Compute",
        "EBITDA: Lunar - Mars",
        "EBITDA: Corporate",
        "Group EBITDA ($mm)",
        "▸ D&A ($mm)",
        "D&A: Starlink",
        "D&A: Customer Launch",
        "D&A: AI - Compute",
        "D&A: Lunar - Mars",
        "D&A: Corporate / facilities",
        "Group D&A ($mm)",
        "▸ EBIT: by segment ($mm)",
        "EBIT: Starlink",
        "EBIT: Customer Launch",
        "EBIT: AI - Compute",
        "EBIT: Lunar - Mars",
        "EBIT: Corporate",
        "Group EBIT ($mm)",
        "▸ TAXES & NOPAT ($mm)",
        "Group Taxes ($mm)",
        "NOPAT ($mm)",
        "▸ CAPEX ($mm)",
        "CapEx: Starlink",
        "CapEx: Customer Launch",
        "CapEx: AI - Compute",
        "CapEx: Lunar - Mars",
        "CapEx: Corporate",
        "Group CapEx: accrual ($mm)",
        "▸ FREE CASH FLOW: by segment ($mm)",
        "FCF: Starlink",
        "FCF: Customer Launch",
        "FCF: AI - Compute",
        "FCF: Lunar - Mars",
        "FCF: less corporate",
        "Group FCF: accrual walk ($mm)",
        "▸ TIE-OUT CHECKS (must = 0 within $1mm)",
        "Memo: Starlink sub-lines − module Revenue",
        "Memo: Customer Launch sub-lines − module Revenue",
        "Memo: AI - Compute sub-lines − module Revenue",
        "Memo: Lunar - Mars sub-line − module Revenue",
        "Memo: Group Revenue − Group P&L Group Revenue",
        "▸ SUB-SEGMENT MIX — % OF OWN SEGMENT REVENUE",
        "Starlink — Broadband (BB)",
        "Starlink — Direct-to-Cell (DTC)",
        "Starlink — Starshield",
        "Starlink — Hardware / kit",
        "Starlink — total",
        "Customer Launch — Launch Services",
        "Customer Launch — Launch & Development",
        "Customer Launch — total",
        "AI - Compute — Orbital DC (external)",
        "AI - Compute — Terrestrial DC (external)",
        "AI - Compute — AI Apps (external)",
        "AI - Compute — total",
        "▸ SEGMENT MIX — % OF GROUP REVENUE",
        "Starlink",
        "Customer Launch",
        "AI - Compute",
        "Lunar - Mars",
        "Group Revenue — total",
    ),
    "SoTP - Valuation": (
        "SoTP / VALUATION: dual-track terminal · single WACC · EV only",
        "As-of valuation dates →",
        "WACC (Group)",
        "Terminal growth g",
        "Terminal FCF avg window (yrs, =5)",
        "Lunar/Mars BV multiplier",
        "▸ MODULE FCF: DCF inputs (direct from Group P&L, $mm)",
        "FCF: Starlink",
        "FCF: Customer Launch",
        "FCF: AI - Compute",
        "FCF: Corporate (cost centre)",
        "FCF: Group DCF subtotal (SL+CL+AI+Corp; excl L/M)",
        "▸ DISCOUNT FACTORS: 1/(1+WACC)^(year−asof); 0 before asof",
        "DF: as-of 2026",
        "DF: as-of 2030",
        "DF: as-of 2035",
        "DF: as-of 2040",
        "▸ TERMINAL VALUE @2040 (both methods, $mm)",
        "(by module)",
        "Starlink",
        "Customer Launch",
        "AI - Compute",
        "Corporate",
        "▸ MODULE SoTP: GORDON (perpetuity-growth) terminal, $mm",
        "(cols C:F = as-of)",
        "Lunar / Mars (BV×mult)",
        "GROUP EV: Gordon ($mm)",
        "GROUP EV: Gordon ($B)",
        "▸ MODULE SoTP: EXIT-MULTIPLE terminal, $mm",
        "GROUP EV: Exit-mult ($mm)",
        "GROUP EV: Exit-mult ($B)",
        "▸ DUAL-TRACK SUMMARY: Group EV by as-of ($B)",
        "Group EV: Gordon",
        "Group EV: Exit-multiple",
        "Spread (Exit − Gordon)",
        "Spread %",
        "▸ LUNAR/MARS BRIDGE & GROUP-FCF RECON (memo, as-of 2026)",
        "Memo: explicit-DCF of Group FCF incl L/M (no TV)",
        "Memo: explicit-DCF of SoTP modules (SL+CL+AI+Corp)",
        "Memo: PV of L/M FCF drain embedded in Group FCF",
        "Memo: L/M SoTP (BV-based, as-of 2026)",
        "Memo: L/M strategic premium over cash-drain PV",
        "▸ COMPARABLES CROSS-CHECK ($B)",
        "Σ standalone analyst anchors (SL+AI+CL+AIStack+L/M)",
        "Group EV anchor: Morgan Stanley (public)",
        "Group EV anchor: Brant (internal)",
        "Model EV as-of 2026: Gordon",
        "Model EV as-of 2026: Exit-mult",
        "Model (Gordon) vs MS",
        "Model (Gordon) vs Brant",
        "▸ SENSITIVITY: Group EV as-of 2026, GORDON ($B)",
        "Helper: Σ NormTermFCF (SL+CL+AI+Corp) $mm",
        "Helper: L/M BV×mult @2040 (undiscounted) $mm",
        "g ＼ WACC →",
        "▸ CHECKS (Rule 4/5/15)",
        "WACC>g (1=OK; HALT if 0)",
        "DF as-of2026 @2026 = 1.000",
        "DF as-of2040 @2040 = 1.000",
        "Explicit-PV tie (subtotal vs Σ modules) = 0",
        "Flag: rev-module SoTP<0, as-of2026 Gordon (cnt, expect 0)",
        "Flag: rev-module SoTP<0, as-of2026 Exit (cnt, expect 0)",
        "Memo: Group EV as-of2026 Gordon $B",
        "Memo: Group EV as-of2026 Exit $B",
        "▸ MODULE SoTP: EBITDA-MULTIPLE terminal, $mm",
        "GROUP EV: EBITDA-mult ($mm)",
        "GROUP EV: EBITDA-mult ($B)",
        "▸ TRI-TRACK SUMMARY: Group EV by as-of ($B)",
        "Group EV: Gordon (perpetuity-growth)",
        "Group EV: Exit-multiple (revenue)",
        "Group EV: EBITDA-multiple",
        "Range (max − min)",
        "Midpoint (mean of 3)",
        "Flag: rev-module SoTP<0, as-of2026 EBITDA (cnt, expect 0)",
    ),
    "Starlink": (
        "Starlink module — real cohorts + total-bandwidth revenue + full waterfall + 4-line OpEx + per-sat IRR",
        "▸ ALLOCATOR IN (cross-tab reads)",
        "Starlink BB Revenue from curve ($mm)",
        "Starlink DTC Revenue from curve ($mm)",
        "F9 at-cost rate per launch ($mm)",
        "Starship at-cost rate per launch ($mm)",
        "Sat operational life L (years)",
        "Group WACC",
        "Starlink R&D as % of revenue (frac)",
        "Starlink module allocated cash ($mm/yr): live from Cash Allocation Engine",
        "Starlink deployment 2025 anchor (sats)",
        "Sat utilization (frac)",
        "Starship operational year",
        "F9 launches V2-Starlink final year",
        "F9 payload per launch (kg)",
        "Starship payload per launch (kg)",
        "▸ CONSTELLATION BUILD (real cohorts → total bandwidth)",
        "V2 launch window active (1/0)",
        "V3 deployment active (1/0)",
        "Total new Starlink deployment (sats/yr)",
        "New V2 BB deployment (sats/yr)",
        "New V2 DTC deployment (sats/yr)",
        "New V3 BB deployment (sats/yr)",
        "New V3 DTC deployment (sats/yr)",
        "New Starshield deployment (sats/yr)",
        "Blended new-sat CapEx slug ($mm/sat): MEMO ONLY (feeds CAE R88 cap; no longer drives deployment)",
        "Demand-saturation deployment headroom (sats)",
        "BB FLEET (active sats by cohort)",
        "Legacy V1 active sats",
        "Legacy V1.5 active sats",
        "V2 Mini BB active sats",
        "V3 BB active sats EoY",
        "BB BANDWIDTH (Gbps by cohort)",
        "Legacy BB Gbps",
        "V2 BB Gbps",
        "V3 BB Gbps",
        "BB Gbps available for external Starlink revenue",
        "DTC FLEET + BANDWIDTH",
        "V2 DTC active sats",
        "V3 DTC active sats EoY",
        "V2 DTC effective Gbps",
        "V3 DTC effective Gbps",
        "DTC Gbps available for external Starlink revenue",
        "▸ REVENUE",
        "Starshield active Gbps (working)",
        "Starshield $/Gbps ($/Gbps-yr) (working)",
        "Total BB revenue ($mm)",
        "Total DTC revenue ($mm)",
        "Starshield revenue ($mm)",
        "Hardware / kit revenue ($mm)",
        "Revenue",
        "Memo: Starlink+DTC revenue (excl. Starshield)",
        "▸ INTERNAL LAUNCHES + RETAIL FLEET (working)",
        "F9 internal launches per year (Starlink-driven)",
        "Starship internal launches per year (Starlink-driven)",
        "Active retail sats (BB + DTC, EoY)",
        "▸ COGS → GROSS PROFIT",
        "Hardware / kit COGS ($mm)",
        "Ground-network ops COGS ($mm)",
        "Asset insurance COGS ($mm)",
        "Variable launch COGS ($mm)",
        "COGS total ($mm)",
        "Gross Profit ($mm)",
        "Memo: Gross Margin %",
        "▸ MODULE OpEx",
        "Sales & Marketing ($mm)",
        "Customer support & billing ($mm)",
        "Network operations ($mm)",
        "Spectrum licence OpEx ($mm)",
        "Module OpEx total (incl. R&D) ($mm)",
        "Module EBITDA ($mm)",
        "EBITDA Margin % (memo)",
        "▸ EBITDA → EBIT (R&D is in Module OpEx above; only D&A below)",
        "Attributed R&D ($mm): component of Module OpEx total (row 87)",
        "Constellation D&A ($mm)",
        "Owned launch-fleet D&A ($mm)",
        "Launch facility share (frac)",
        "Facility / ground D&A ($mm)",
        "D&A total ($mm)",
        "Module EBIT ($mm)",
        "▸ CAPEX → MODULE FCF",
        "Satellite build CapEx ($mm)",
        "Facility / ground CapEx ($mm)",
        "Owned launch-vehicle CapEx ($mm)",
        "Working capital ΔWC ($mm)",
        "Module CapEx total ($mm)",
        "Module FCF ($mm)",
        "▸ PER-SAT IRR ENGINE (v4 canonical): per cohort, one cost base",
        "Avg $/Gbps BB at Q (price-at-Q)",
        "Avg $/Gbps DTC at Q (price-at-Q)",
        "V2 BB: margin per sat-yr ($mm)",
        "V2 BB: CapEx slug per sat ($mm)",
        "V2 BB: Spot IRR",
        "V2 DTC: margin per sat-yr ($mm)",
        "V2 DTC: CapEx slug per sat ($mm)",
        "V2 DTC: Spot IRR",
        "V3 BB: margin per sat-yr ($mm)",
        "V3 BB: CapEx slug per sat ($mm)",
        "V3 BB: Spot IRR",
        "V3 DTC: margin per sat-yr ($mm)",
        "V3 DTC: CapEx slug per sat ($mm)",
        "V3 DTC: Spot IRR",
        "Starshield: active fleet EoY (sats) (working)",
        "Starshield: margin per sat-yr ($mm)",
        "Starshield: CapEx slug per sat ($mm)",
        "Module Spot IRR (rev-weighted)",
        "Cumulative Starlink sats built (sats)",
        "Sat cost $/kg (Wright's, floored)",
        "▸ ALLOCATOR OUT (canonical labels: Rule 12 sources)",
        "COGS total",
        "Gross Profit",
        "Module OpEx",
        "Module EBITDA",
        "Attributed R&D",
        "D&A",
        "Module EBIT",
        "Satellite/unit build CapEx",
        "Ground/facility CapEx",
        "Working capital ΔWC",
        "Module CapEx",
        "Module FCF",
        "Capital Deployed (cumulative)",
        "Kg demand year N+1",
        "Spot marginal IRR",
        "Blended new-sat mass (kg/sat): share-weighted, regime-gated (acyclic)",
        "Launch-capacity deployment ceiling (sats): same-year demand vs start-of-year capacity",
        "▸ CONSERVATION MEMOS",
        "Memo: reclassification conservation",
        "Memo: P&L↔IRR conservation",
        "Memo: 2025 revenue reconciliation",
        "Memo: 2025 DTC sub-line reconciliation",
        "Memo: post-rebuild capacity state (Demand Curves now prices this tab)",
        "BB active Gbps (V2+V3 combined)",
        "DTC active Gbps (V2+V3 combined)",
        "▸ SUBSCRIBERS + HARDWARE",
        "BB subscribers: revenue-implied level (M)",
        "BB BoY subscribers (M)",
        "BB EoY subscribers (= revenue-implied level, M): stabilised",
        "BB net adds (M)",
        "DTC avg subscribers (implied, M)",
        "Memo: implied total Starlink subscribers (BB, M) vs S-1 8.9M",
        "▸ IRR-DRIVEN COHORT ALLOCATION: prior-year spot IRR weights per-cohort affordability (broadband vs direct-to-cell)",
        "Active-gen BB Spot IRR (prior yr)",
        "Active-gen DTC Spot IRR (prior yr)",
        "exp(β·IRR) BB",
        "exp(β·IRR) DTC",
        "Allocation weight: broadband (V2 era = 1)",
        "Allocation weight: direct-to-cell",
        "Active-gen BB CapEx slug ($mm/sat)",
        "Active-gen DTC CapEx slug ($mm/sat)",
        "Cash → BB ($mm)",
        "Cash → DTC ($mm)",
        "Desired BB sats (pre-cap)",
        "Desired DTC sats (pre-cap)",
        "Total desired sats (pre-cap)",
        "Deployment cap: MIN(demand, launch, pacing) (sats)",
        "Cap scale factor (≤1, pro-rata)",
        "Final BB sats",
        "Final DTC sats",
        "Starship sats per launch (V3, mass-derived)",
    ),
    "Vehicle Build": (
        "Vehicle Build: demand-pulled Starship + F9 launch capacity",
        "Roll-up / reconciliation tab — modules own launch CapEx. Books no FCF; aggregates module-owned launch CapEx + fleet.",
        "VEHICLE PHYSICAL PARAMETERS (F9 + Starship payload + cadence)",
        "F9 payload per launch (kg)",
        "F9 annual cadence per booster in service",
        "Starship payload per launch (kg)",
        "Starship BOOSTER cadence per vehicle in service",
        "Starship SHIP cadence per vehicle in service",
        "PER-LAUNCH AT-COST RATES ($mm): internal transfer pricing source",
        "F9 at-cost rate per launch ($mm)",
        "Starship at-cost rate per launch ($mm)",
        "LAUNCHES PER YEAR (F9 glide path + Starship demand-pulled)",
        "F9 launches per year",
        "Starship launches per year",
        "CAPACITY + CapEx + TRANSFER REVENUE",
        "Total launch capacity (kg)",
        "Vehicle Build CapEx ($mm)",
        "Vehicle Build at-cost transfer revenue ($mm) — RETIRED (modules own launch CapEx)",
        "▸ LAUNCH CAPEX ROLL-UP (books no FCF)",
        "Total fleet launch CapEx ($mm): independent (engine)",
        "Memo: Σ module owned launch CapEx (all modules)",
        "Memo: fleet CapEx conservation (engine − Σ module; must = 0)",
        "FLEET WRIGHT'S COST CURVES + CONFIG LINES",
        "Cum Starship experience units (Wright's-Law cost basis, incl. 2024 baseline + F9-inherited seed; NOT the standing fleet)",
        "Starship manufacturing cost per stack ($mm)",
        "Booster mfg per stack ($mm)",
        "Ship mfg per stack ($mm)",
        "Starship ops + fuel per launch ($mm)",
        "Starship booster refurb per flight ($mm)",
        "Starship ship refurb per flight ($mm)",
        "Starship amortized mfg per launch, fully reusable ($mm)",
        "Starship at-cost rate, fully reusable ($mm/launch)",
        "Starship at-cost rate, expendable ship / reusable booster ($mm/launch)",
        "Starship at-cost rate, fully expendable ($mm/launch)",
        "Starship payload, fully reusable (kg)",
        "Starship payload, expendable ship (kg)",
        "Starship payload, fully expendable (kg)",
        "Starship $/kg, fully reusable",
        "Starship $/kg, expendable ship",
        "Starship $/kg, fully expendable",
        "Starship build cost ($mm/stack)",
        "CUM-UPMASS + FLEET ROLL-FORWARD",
        "Cum Starship upmass (fleet, end-of-year, kg)",
        "Boosters needed (fleet)",
        "Boosters built (fleet)",
        "Booster fleet BoY (units)",
        "Boosters retired (fleet)",
        "Booster fleet EoY (units)",
        "Memo: launch cadence (Wright's Law) is driven by total fleet cumulative up-mass (row 76 = Σ row 32 Starship launches × payload) — all flights, internal Starlink + commercial, not customer-launch flights only. Do not repoint.",
        "F9 boosters built per year",
        "F9 boosters retired per year",
        "F9 fleet BoY (boosters)",
        "F9 fleet EoY (boosters)",
        "F9 launch capacity (launches/yr)",
        "TOTAL KG DEMAND",
        "Total launch kg demand year N+1 (fleet)",
        "Total launch capacity: start-of-year stock (kg)",
        "F9 INTERNAL-VS-CUSTOMER RECONCILIATION (memo)",
        "Memo: F9 internal launches (Starlink-driven)",
        "Memo: F9 customer launches (Customer Launch)",
        "Memo: Total F9 launches (internal + customer)",
        "Memo: F9 launch capacity (launches/yr)",
        "Memo: Mass to orbit: F9 (kg)",
        "Memo: Mass to orbit: Starship (kg)",
        "Memo: Total mass to orbit (mt)",
        "Memo: Vehicle Build FCF ($mm): must = 0 by construction",
        "Memo: F9 internal (model) vs S-1 core Starlink + Starshield",
        "Memo: F9 customer (model) vs S-1 customer − Starshield",
        "Memo: total F9 (model) vs S-1 total 171 (132 internal + 38.6 customer)",
        "SHIP FLEET ROLL-FORWARD (booster / ship split)",
        "Ships needed (fleet)",
        "Ships built (fleet)",
        "Ship fleet BoY (units)",
        "Ships retired (fleet)",
        "Ship fleet EoY (units)",
        "STARSHIP BUILD CapEx SPLIT",
        "Booster build CapEx ($mm)",
        "Ship build CapEx ($mm)",
        "Total Starship build CapEx ($mm)",
        "Memo: launch/vehicle facility CapEx (from Facilities Build)",
        "Memo: total launch + facility CapEx",
        "FLEET PRODUCTION ↔ STANDING-FLEET RECONCILIATION",
        "Cum Starship ships built (cumulative, from 0)",
        "Cum Starship ships retired (cumulative, from 0)",
        "Cum Starship boosters built (cumulative, from 0)",
        "Cum Starship boosters retired (cumulative, from 0)",
        "Memo: ship fleet reconciliation ((cum built − cum retired) − Ship fleet EoY; must = 0)",
        "Memo: booster fleet reconciliation ((cum built − cum retired) − Booster fleet EoY; must = 0)",
        "▸ DEMAND-DRIVEN FLEET SIZING (forward-demand pull, no circular reference)",
        "Total desired upmass kg (fleet, current yr)  ◄ Cash Allocation Engine",
        "Memo: F9 available capacity (kg)",
        "Desired Starship launches (current yr)",
        "Gigabay installed Starship build capacity (ships/yr)  ◄ Assumptions",
    ),
}


def resolve_label(constant_name: str) -> str:
    """Return the Excel label string for a registry constant name."""
    return globals()[constant_name]

from spacex_model.config.canonical_labels_supplement import *  # noqa: E402, F403
