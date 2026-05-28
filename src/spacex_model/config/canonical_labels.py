"""Canonical label registry — append-only per PRD §2.4 / Rule 10.

Extracted from: SpaceX Model V2.16.xlsx
Regenerate via: python scripts/extract_canonical_labels.py
"""

from __future__ import annotations

from typing import Final

# fmt: off

ADCS_AVIONICS_COST_PER_SAT_PRE_WL: Final[str] = "ADCS + avionics cost per sat ($, pre-WL)"
ADCS_AVIONICS_FLAT_COST: Final[str] = "ADCS + avionics flat cost ($)"
AI_STACK_BLENDED_IRR: Final[str] = "AI Stack Blended IRR"
AI_STACK_FORWARD_IRR_Y_2: Final[str] = "AI Stack Forward IRR (Y+2)"
AI_STACK_MODULE_CAPEX_MM: Final[str] = "AI Stack Module CapEx ($mm)"
AI_STACK_R_D_PROFILE_MM_PRE_REVENUE_FLOOR: Final[str] = "AI Stack R&D $-profile ($mm, pre-revenue floor)"
AI_STACK_R_D_PROFILE_MM_YR_YEAR_ROW: Final[str] = "AI Stack R&D $-profile ($mm/yr) — year-row"
AI_STACK_R_D_MM_MAX_PROFILE_REV: Final[str] = "AI Stack R&D ($mm) — MAX($-profile, % × rev)"
AI_STACK_R_D_BASE_AI_STACK_REV_MM: Final[str] = "AI Stack R&D base — AI Stack rev ($mm)"
AI_STACK_R_D_OF_AI_STACK_REV_BOUNDED_CAGR: Final[str] = "AI Stack R&D — % of AI Stack rev (bounded-CAGR)"
AI_STACK_R_D_CAGR_TAPER: Final[str] = "AI Stack R&D — CAGR (taper)"
AI_STACK_R_D_END_STATE_FLOOR: Final[str] = "AI Stack R&D — end-state % (floor)"
AI_STACK_R_D_START_OF_AI_STACK_REV: Final[str] = "AI Stack R&D — start % of AI Stack rev"
AI_STACK_SPOT_IRR: Final[str] = "AI Stack Spot IRR"
AI_STACK_CASH_ALLOCATION: Final[str] = "AI Stack cash allocation"
AI_STACK_CASH_DEMAND_MM: Final[str] = "AI Stack cash demand ($mm)"
AI_STACK_INSURANCE_OF_REVENUE: Final[str] = "AI Stack insurance % of revenue"
AI_STACK_KG_ALLOCATION: Final[str] = "AI Stack kg allocation"
AI_STACK_KG_DEMAND_KG_TO_LEO: Final[str] = "AI Stack kg demand (kg-to-LEO)"
AI_STACK_KG_PROPOSED_ALLOCATION: Final[str] = "AI Stack kg proposed allocation"
AI_STACK_KG_WEIGHT: Final[str] = "AI Stack kg weight"
AI_STACK_OTHER_COGS_OF_REVENUE: Final[str] = "AI Stack other COGS % of revenue"
AI_STACK_PROPOSED_ALLOCATION_MM: Final[str] = "AI Stack proposed allocation ($mm)"
AI_STACK_WEIGHT: Final[str] = "AI Stack weight"
ALL_OK_BOOLEAN: Final[str] = "ALL OK boolean"
ACTIVE_V2_BB_SATS: Final[str] = "Active V2 BB sats"
ACTIVE_V2_DTC_SATS: Final[str] = "Active V2 DTC sats"
ACTIVE_V3_BB_SATS: Final[str] = "Active V3 BB sats"
ACTIVE_V3_DTC_SATS: Final[str] = "Active V3 DTC sats"
ACTIVE_SAT_FLEET_EOY_YEAR_CHAINED_RULE_23_EXCEPTION: Final[str] = "Active sat fleet EoY (year-chained, Rule 23 exception)"
ADJUSTED_COREWEAVE_BASELINE_YEAR_ROW_B_GW_IT_YR: Final[str] = "Adjusted CoreWeave baseline year-row ($B/GW_IT/yr)"
ANCHOR_YEAR_FOR_ODC_WRIGHT_S_LAW: Final[str] = "Anchor year for ODC Wright’s Law"
ANCHOR_YEAR_FOR_CUM_UPMASS_WRIGHT_S_LAW: Final[str] = "Anchor year for cum-upmass Wright's Law"
ANNUAL_GPU_HR_PRICE_DEFLATION_RATE: Final[str] = "Annual GPU-hr price deflation rate"
ANNUAL_TAM_SHIFT_MULTIPLIER: Final[str] = "Annual TAM shift multiplier"
ANNUAL_BANDWIDTH_SERVICES_COST_MM_YR: Final[str] = "Annual bandwidth services cost ($mm/yr)"
ANNUAL_GROUND_OPS_COST_MM_YR: Final[str] = "Annual ground ops cost ($mm/yr)"
ANNUAL_INSURANCE_COST_MM_YR: Final[str] = "Annual insurance cost ($mm/yr)"
ANNUAL_LAUNCH_SERVICES_COST_MM_YR: Final[str] = "Annual launch services cost ($mm/yr)"
ANNUAL_OTHER_COGS_MM_YR: Final[str] = "Annual other COGS ($mm/yr)"
ANNUAL_SAT_D_A_MM_YR: Final[str] = "Annual sat D&A ($mm/yr)"
ANNUAL_SPECTRUM_AMORTIZATION_MM: Final[str] = "Annual spectrum amortization ($mm)"
AVAILABLE_CASH_FOR_IRR_QUEUE_MM: Final[str] = "Available cash for IRR queue ($mm)"
BANDWIDTH_CLAIM_SERVICES_COST_PAID_TO_STARLINK_AT_FULLY_ALLOCATED_AT_COST_RATE: Final[str] = "BANDWIDTH CLAIM & SERVICES COST (paid to Starlink at fully-allocated at-cost rate)"
BB_GBPS_GBPS_YR: Final[str] = "BB $/Gbps ($/Gbps/yr)"
BB_ARPU_MO_YEAR_ROW_FROM_ASSUMPTIONS: Final[str] = "BB ARPU ($/mo, year-row from Assumptions)"
BB_DEMAND_CURVE_PIECEWISE_LINEAR_Q_REVENUE_LOOKUP: Final[str] = "BB DEMAND CURVE (piecewise-linear Q→Revenue lookup)"
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
BB_REVENUE_MM: Final[str] = "BB Revenue ($mm)"
BB_MARKET_SHARE_STARLINK_REVENUE_MIX: Final[str] = "BB market share % (Starlink revenue mix)"
BB_POOL_AT_COST_RATE_GBPS_YR: Final[str] = "BB pool at-cost rate ($/Gbps/yr)"
BB_POOL_AT_COST_RATE_GBPS_YR_READ_FROM_STARLINK_CAPACITY: Final[str] = "BB pool at-cost rate ($/Gbps/yr) — read from Starlink Capacity"
BB_POOL_COST_BASIS_MM_YR: Final[str] = "BB pool cost basis ($mm/yr)"
BB_SUBSCRIBERS_MILLIONS_DERIVED_BB_REVENUE_ARPU_12: Final[str] = "BB subscribers (millions, derived = BB Revenue / (ARPU × 12))"
BB_SHARE_OF_ODC_BANDWIDTH_CLAIM: Final[str] = "BB-share of ODC bandwidth claim"
BLENDED_COST_STACK_CALIBRATION: Final[str] = "BLENDED COST STACK + CALIBRATION"
BV_ENGINE_INPUTS_ARCHITECTURE_11_4_LABOUR_UNITS_HARDWARE: Final[str] = "BV ENGINE INPUTS (Architecture §11.4 — labour units + hardware)"
BV_ENGINE_OUTPUT_ARCHITECTURE_11_4: Final[str] = "BV ENGINE OUTPUT (Architecture §11.4)"
BANDWIDTH_REMOVED_PER_DEORBITED_V2_MINI_BB_SAT_GBPS: Final[str] = "Bandwidth Removed per Deorbited V2 Mini BB Sat (Gbps)"
BANDWIDTH_REMOVED_PER_DEORBITED_V2_MINI_DTC_SAT_GBPS: Final[str] = "Bandwidth Removed per Deorbited V2 Mini DTC Sat (Gbps)"
BANDWIDTH_REMOVED_PER_DEORBITED_V3_BB_SAT_GBPS: Final[str] = "Bandwidth Removed per Deorbited V3 BB Sat (Gbps)"
BANDWIDTH_REMOVED_PER_DEORBITED_V3_DTC_SAT_GBPS: Final[str] = "Bandwidth Removed per Deorbited V3 DTC Sat (Gbps)"
BANDWIDTH_ELIMINATION_CONSERVATION: Final[str] = "Bandwidth elimination conservation"
BANDWIDTH_SERVICES_COST_MM: Final[str] = "Bandwidth services cost ($mm)"
BASE_TURNAROUND_TIME_PER_BOOSTER_YEARS_FLIGHT: Final[str] = "Base turnaround time per booster (years/flight)"
BATTERY_COST_PER_SAT_PRE_WL: Final[str] = "Battery cost per sat ($, pre-WL)"
BATTERY_FLAT_COST: Final[str] = "Battery flat cost ($)"
BLENDED_KG: Final[str] = "Blended $/kg"
BLENDED_IRR: Final[str] = "Blended IRR"
BOOSTER_FLEET_BEGINNING_OF_YEAR_UNITS: Final[str] = "Booster fleet beginning-of-year (units)"
BOOSTER_FLEET_END_OF_YEAR_UNITS: Final[str] = "Booster fleet end-of-year (units)"
BOOSTER_ONLY_LAUNCHES_PER_YEAR_COUNT: Final[str] = "Booster-only launches per year (count)"
BOOSTERS_BUILT_PER_YEAR_UNITS: Final[str] = "Boosters built per year (units)"
BOOSTERS_RETIRED_PER_YEAR_UNITS: Final[str] = "Boosters retired per year (units)"
BROADBAND_ARPU_SUB_MO_YEAR_ROW: Final[str] = "Broadband ARPU ($/sub/mo, year-row)"
CAPEX_MODULE_CAPEX_AGGREGATION_CORPORATE_CAPEX_SPECTRUM_CAPEX_CORPORATE_D_A_SPRINT_8_FILLS: Final[str] = "CAPEX -- module CapEx aggregation + corporate CapEx + spectrum CapEx + corporate D&A. Sprint 8 fills."
CARVE_OUT_CASH_INFLOW_ARCHITECTURE_11_1_READ_FROM_ALLOCATOR_3: Final[str] = "CARVE-OUT CASH INFLOW (Architecture §11.1 — read from Allocator §3)"
CENTRAL_ALLOCATOR_OUTPUTS: Final[str] = "CENTRAL ALLOCATOR OUTPUTS"
COGS_BANDWIDTH_SERVICES_COST_MM: Final[str] = "COGS — Bandwidth services cost ($mm)"
COGS_CONSTELLATION_D_A_MM: Final[str] = "COGS — Constellation D&A ($mm)"
COGS_GROUND_OPS_MM: Final[str] = "COGS — Ground ops ($mm)"
COGS_INSURANCE_MM: Final[str] = "COGS — Insurance ($mm)"
COGS_LAUNCH_SERVICES_COST_MM: Final[str] = "COGS — Launch services cost ($mm)"
COGS_OTHER_COGS_MM: Final[str] = "COGS — Other COGS ($mm)"
CUSTOMER_LAUNCH_MODULE_BODY: Final[str] = "CUSTOMER LAUNCH — MODULE BODY"
CADENCE_CEILING_FLIGHTS_BOOSTER_YEAR: Final[str] = "Cadence ceiling (flights/booster/year)"
CAPEX_LAG_YEARS: Final[str] = "CapEx Lag (years)"
CAPEX_CHECK: Final[str] = "CapEx check"
CAPACITY_GBPS: Final[str] = "Capacity (Gbps)"
CAPACITY_DEMAND_KG_TO_LEO: Final[str] = "Capacity Demand (kg-to-LEO)"
CAPACITY_AVAILABLE_FOR_IRR_QUEUE_KG_TO_LEO: Final[str] = "Capacity available for IRR queue (kg-to-LEO)"
CAPACITY_GAP_KG_TO_LEO: Final[str] = "Capacity gap (kg-to-LEO)"
CAPITAL_ALLOCATION_MM: Final[str] = "Capital Allocation ($mm)"
CAPITAL_DEPLOYED_MM: Final[str] = "Capital deployed ($mm)"
CAPITAL_DEPLOYED_MM_DIAGNOSTIC: Final[str] = "Capital deployed ($mm) — diagnostic"
CAPITAL_LIFETIME_BOOK_VALUE_STRAIGHT_LINE_DEP_YRS: Final[str] = "Capital lifetime — book value straight-line dep (yrs)"
CAPITAL_LIFETIME_BOOK_VALUE_STRAIGHT_LINE_DEPRECIATION_YEARS: Final[str] = "Capital lifetime — book value straight-line depreciation (years)"
CASH_BOY_MM: Final[str] = "Cash BoY ($mm)"
CASH_DEMAND_YEAR_ROW_PUBLISHED_MM_MASKED_BY_BLENDED_IRR_0: Final[str] = "Cash demand year-row published ($mm) — masked by Blended IRR > 0"
CASH_FLOW_IDENTITY_CHECK_MM_STARTING_IPO_FCF_CASH_EOY: Final[str] = "Cash flow identity check ($mm — Starting + ΣIPO + ΣFCF − Cash EoY)"
CHIP_FP8_PER_CHIP_TFLOPS_YEAR_ROW: Final[str] = "Chip FP8 per chip (TFLOPS) — year-row"
CHIP_FP8_PERFORMANCE_PER_CHIP_TFLOPS_YEAR_ROW: Final[str] = "Chip FP8 performance per chip (TFLOPS) — year-row"
CHIP_TDP_PER_CHIP_W_YEAR_ROW: Final[str] = "Chip TDP per chip (W) — year-row"
CHIP_COST_PER_CHIP_YEAR_ROW: Final[str] = "Chip cost per chip ($) — year-row"
CHIP_COST_PER_SAT_YEAR_ROW: Final[str] = "Chip cost per sat ($) — year-row"
CHIP_MASS_PER_CHIP_KG_YEAR_ROW: Final[str] = "Chip mass per chip (kg) — year-row"
CHIPS_PER_SAT: Final[str] = "Chips per sat"
COMMERCIAL_LAUNCH_MARKET_SIZE_MM_YEAR_YEAR_ROW: Final[str] = "Commercial launch market size ($mm/year) — year-row"
COMMS_ISL_SET_COST_PER_SAT_PRE_WL: Final[str] = "Comms (ISL set) cost per sat ($, pre-WL)"
COMMS_ISL_SET_FLAT_COST: Final[str] = "Comms (ISL set) flat cost ($)"
COMP_ANCHOR_AI_STACK_STANDALONE: Final[str] = "Comp anchor — AI Stack standalone"
COMP_ANCHOR_CUSTOMER_LAUNCH_STANDALONE_ROCKET_LAB: Final[str] = "Comp anchor — Customer Launch standalone (Rocket Lab)"
COMP_ANCHOR_GROUP_EV_BRANT_INTERNAL: Final[str] = "Comp anchor — Group EV (Brant internal)"
COMP_ANCHOR_GROUP_EV_MORGAN_STANLEY_PUBLIC: Final[str] = "Comp anchor — Group EV (Morgan Stanley public)"
COMP_ANCHOR_LUNAR_MARS_NASA_HLS_LIFETIME: Final[str] = "Comp anchor — Lunar / Mars (NASA HLS lifetime)"
COMP_ANCHOR_ODC_STANDALONE_COREWEAVE_ANCHORED: Final[str] = "Comp anchor — ODC standalone (CoreWeave-anchored)"
COMP_ANCHOR_STARLINK_STANDALONE_BERNSTEIN_JPM: Final[str] = "Comp anchor — Starlink standalone (Bernstein/JPM)"
COMPUTE_ELIMINATION_CONSERVATION: Final[str] = "Compute elimination conservation"
COMPUTE_POWER_PER_SAT_KW: Final[str] = "Compute power per sat (kW)"
CONSTELLATION_BANDWIDTH_GBPS: Final[str] = "Constellation Bandwidth (Gbps)"
CONSTELLATION_D_A_MM: Final[str] = "Constellation D&A ($mm)"
COREWEAVE_BASELINE_B_GW_IT_YR_2026_ANCHOR: Final[str] = "CoreWeave baseline ($B/GW_IT/yr, 2026 anchor)"
COREWEAVE_BASELINE_ANCHOR_B_GW_IT_YR_2026: Final[str] = "CoreWeave baseline anchor ($B/GW_IT/yr, 2026)"
CORPORATE_CAPEX_CLAIM_MM: Final[str] = "Corporate CapEx claim ($mm)"
CORPORATE_IT_CAPEX_MM: Final[str] = "Corporate IT CapEx ($mm)"
CORPORATE_IT_CAPEX_MM_YR_FLAT: Final[str] = "Corporate IT CapEx ($mm/yr, flat)"
CORPORATE_IT_USEFUL_LIFE_YEARS: Final[str] = "Corporate IT useful life (years)"
CORPORATE_HISTORICAL_CAPITAL_BASE_MM: Final[str] = "Corporate historical capital base ($mm)"
COST_OF_DEBT_MEMO: Final[str] = "Cost of debt (memo)"
COST_OF_EQUITY_MEMO: Final[str] = "Cost of equity (memo)"
CREDENCE_ON_MODEL_A_PR_A: Final[str] = "Credence on Model A (Pr(A))"
CUM_ODC_SATS_AT_WL_ANCHOR_YEAR: Final[str] = "Cum ODC sats at WL anchor year"
CUM_ODC_SATS_DEPLOYED_RUNNING_SUM_RULE_23_EXCEPTION_INTENTIONAL: Final[str] = "Cum ODC sats deployed (running sum) — Rule 23 exception, intentional"
CUM_STARSHIP_STACKS_MANUFACTURED_END_OF_YEAR_UNITS: Final[str] = "Cum Starship stacks manufactured (end-of-year, units)"
CUM_UPMASS_TO_DATE_KG: Final[str] = "Cum upmass to date (kg)"
CUMULATIVE_GEN_ENG_CAPEX_MM: Final[str] = "Cumulative Gen eng CapEx ($mm)"
CUMULATIVE_HQ_CAPEX_MM: Final[str] = "Cumulative HQ CapEx ($mm)"
CUMULATIVE_IT_CAPEX_MM: Final[str] = "Cumulative IT CapEx ($mm)"
CUMULATIVE_OTHER_CAPEX_MM: Final[str] = "Cumulative Other CapEx ($mm)"
CUMULATIVE_SATS_AT_BASE_YEAR_END_2024: Final[str] = "Cumulative sats at base year (end-2024)"
CUMULATIVE_SPECTRUM_INTANGIBLE_MM: Final[str] = "Cumulative spectrum intangible ($mm)"
CURSOR_AVG_SUBSCRIPTION_PRICE_SEAT_MO: Final[str] = "Cursor avg subscription price ($/seat/mo)"
CURSOR_ENTERPRISE_API_REV_PER_SEAT_YEAR: Final[str] = "Cursor enterprise API rev per seat ($/year)"
CURSOR_PAID_SEATS_MILLIONS_YEAR_ROW: Final[str] = "Cursor paid seats (millions) — year-row"
CUSTOMER_LAUNCH_BLENDED_IRR: Final[str] = "Customer Launch Blended IRR"
CUSTOMER_LAUNCH_FORWARD_IRR_Y_2: Final[str] = "Customer Launch Forward IRR (Y+2)"
CUSTOMER_LAUNCH_MODULE_CAPEX_MM: Final[str] = "Customer Launch Module CapEx ($mm)"
CUSTOMER_LAUNCH_R_D_MM: Final[str] = "Customer Launch R&D ($mm)"
CUSTOMER_LAUNCH_R_D_BASE_CUSTOMER_LAUNCH_EXTERNAL_REV_MM: Final[str] = "Customer Launch R&D base — Customer Launch external rev ($mm)"
CUSTOMER_LAUNCH_R_D_OF_EXTERNAL_REV: Final[str] = "Customer Launch R&D — % of external rev"
CUSTOMER_LAUNCH_R_D_CAGR_TAPER: Final[str] = "Customer Launch R&D — CAGR (taper)"
CUSTOMER_LAUNCH_R_D_END_STATE_FLOOR: Final[str] = "Customer Launch R&D — end-state % (floor)"
CUSTOMER_LAUNCH_R_D_START_OF_EXTERNAL_REV: Final[str] = "Customer Launch R&D — start % of external rev"
CUSTOMER_LAUNCH_SPOT_IRR: Final[str] = "Customer Launch Spot IRR"
CUSTOMER_LAUNCH_CASH_ALLOCATION: Final[str] = "Customer Launch cash allocation"
CUSTOMER_LAUNCH_CASH_DEMAND_MM: Final[str] = "Customer Launch cash demand ($mm)"
CUSTOMER_LAUNCH_CASH_DEMAND_LARGE_DEFAULT_MM: Final[str] = "Customer Launch cash demand large default ($mm)"
CUSTOMER_LAUNCH_REVENUE_TRAJECTORY_STUB_MM: Final[str] = "Customer Launch revenue trajectory stub ($mm)"
CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_KG_DEMAND_STUB_KG: Final[str] = (
    "Customer Launch external Starship kg demand stub (kg)"
)
CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_LAUNCHES_STUB: Final[str] = (
    "Customer Launch external Starship launches stub"
)
CUSTOMER_LAUNCH_DEPRECIATION_USEFUL_LIFE_YEARS: Final[str] = "Customer Launch depreciation useful life (years)"
CUSTOMER_LAUNCH_FORWARD_KG_DEMAND_AT_T_LEAD: Final[str] = "Customer Launch forward kg demand at T+lead"
CUSTOMER_LAUNCH_GROUND_OPS_MM: Final[str] = "Customer Launch ground ops ($mm)"
CUSTOMER_LAUNCH_INSURANCE_MM: Final[str] = "Customer Launch insurance ($mm)"
CUSTOMER_LAUNCH_INTERNAL_TRANSFER_REVENUE_MM: Final[str] = "Customer Launch internal transfer revenue ($mm)"
CUSTOMER_LAUNCH_KG_ALLOCATION: Final[str] = "Customer Launch kg allocation"
CUSTOMER_LAUNCH_KG_DEMAND_KG_TO_LEO: Final[str] = "Customer Launch kg demand (kg-to-LEO)"
CUSTOMER_LAUNCH_KG_PROPOSED_ALLOCATION: Final[str] = "Customer Launch kg proposed allocation"
CUSTOMER_LAUNCH_KG_WEIGHT: Final[str] = "Customer Launch kg weight"
CUSTOMER_LAUNCH_OTHER_COGS_MM: Final[str] = "Customer Launch other COGS ($mm)"
CUSTOMER_LAUNCH_PROPOSED_ALLOCATION_MM: Final[str] = "Customer Launch proposed allocation ($mm)"
CUSTOMER_LAUNCH_WEIGHT: Final[str] = "Customer Launch weight"
CUSTOMER_SERVICE_MM_2_STARLINK_SUBSCRIPTION_REV: Final[str] = "Customer Service ($mm) — 2% × Starlink subscription rev"
CUSTOMER_SERVICE_FLAT_OF_STARLINK_SUBSCRIPTION_REV: Final[str] = "Customer Service — flat % of Starlink subscription rev"
D_A_CHECK: Final[str] = "D&A check"
DEPLOYMENT_FLEET_RAMP_CASH_KG_DEMAND_PUBLISH: Final[str] = "DEPLOYMENT, FLEET RAMP, CASH/KG DEMAND PUBLISH"
DTC_GBPS_GBPS_YR: Final[str] = "DTC $/Gbps ($/Gbps/yr)"
DTC_ARPU_MO_YEAR_ROW_FROM_ASSUMPTIONS: Final[str] = "DTC ARPU ($/mo, year-row from Assumptions)"
DTC_ARPU_SUB_MO_YEAR_ROW: Final[str] = "DTC ARPU ($/sub/mo, year-row)"
DTC_DEMAND_CURVE_PIECEWISE_LINEAR_Q_REVENUE_LOOKUP: Final[str] = "DTC DEMAND CURVE (piecewise-linear Q→Revenue lookup)"
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
DTC_REVENUE_MM: Final[str] = "DTC Revenue ($mm)"
DTC_MARKET_SHARE_STARLINK_REVENUE_MIX: Final[str] = "DTC market share % (Starlink revenue mix)"
DTC_POOL_AT_COST_RATE_GBPS_YR: Final[str] = "DTC pool at-cost rate ($/Gbps/yr)"
DTC_POOL_AT_COST_RATE_GBPS_YR_READ_FROM_STARLINK_CAPACITY: Final[str] = "DTC pool at-cost rate ($/Gbps/yr) — read from Starlink Capacity"
DTC_POOL_COST_BASIS_MM_YR: Final[str] = "DTC pool cost basis ($mm/yr)"
DTC_SUBSCRIBERS_MILLIONS_DERIVED_DTC_REVENUE_ARPU_12: Final[str] = "DTC subscribers (millions, derived = DTC Revenue / (ARPU × 12))"
DUAL_REVENUE_MODEL_PR_A_MODEL_A_PR_B_MODEL_B_ARCHITECTURE_9_2: Final[str] = "DUAL REVENUE MODEL (Pr(A) × Model A + Pr(B) × Model B; Architecture §9.2)"
DEMAND_CURVES: Final[str] = "Demand Curves"
EBIT_CONSISTENCY: Final[str] = "EBIT consistency"
EBITDA_CHECK: Final[str] = "EBITDA check"
ECHOSTAR_MID_BAND_CAPEX_MM: Final[str] = "EchoStar mid-band CapEx ($mm)"
ECHOSTAR_MID_BAND_CAPEX_MM_YEAR_ROW: Final[str] = "EchoStar mid-band CapEx ($mm) — year-row"
EFFECTIVE_COMPUTE_RATIO_ECR: Final[str] = "Effective Compute Ratio (ECR)"
EXTERNAL_COMPUTE_REVENUE_MM_YR: Final[str] = "External compute revenue ($mm/yr)"
EXTERNAL_COMPUTE_SHARE_TO_CUSTOMERS_YEAR_ROW: Final[str] = "External compute share to customers % — year-row"
F9_2ND_STAGE_MFG_COST_MM_UNIT: Final[str] = "F9 2nd stage mfg cost ($mm/unit)"
F9_ANNUAL_CAPACITY_KG_TO_LEO: Final[str] = "F9 Annual Capacity (kg-to-LEO)"
F9_D_A_SHARE_MM: Final[str] = "F9 D&A share ($mm)"
F9_D_A_SHARE_PER_LAUNCH_MM_READ_FROM_LAUNCH_CAPACITY: Final[str] = "F9 D&A share per launch ($mm) — read from Launch Capacity"
F9_FORWARD_IRR_Y_2_PER_LAUNCH_MARGINAL_IRR_YEAR_T_2_CASHFLOW: Final[str] = "F9 Forward IRR (Y+2) — per-launch marginal IRR, year T+2 cashflow"
F9_IRR_CASHFLOW_STREAM_PERIOD_COUNT_N_CLAMPED_AT_R23_MAX: Final[str] = "F9 IRR cashflow stream period count N (clamped at R23 MAX)"
F9_SPOT_IRR_PER_LAUNCH_MARGINAL_IRR_CURRENT_YEAR_EXTERNAL_CUSTOMER_ECONOMICS: Final[str] = "F9 Spot IRR (per-launch marginal IRR, current year — external customer economics)"
F9_V2_BB_LAUNCHES_INTERNAL: Final[str] = "F9 V2 BB launches (internal)"
F9_V2_DTC_LAUNCHES_INTERNAL: Final[str] = "F9 V2 DTC launches (internal)"
F9_WL_LEARNING_RATE: Final[str] = "F9 WL learning rate"
F9_WRIGHT_S_LAW_MFG_LEARNING_RATE: Final[str] = "F9 Wright's Law mfg learning rate"
F9_AT_COST_RATE_MM_LAUNCH: Final[str] = "F9 at-cost rate ($mm/launch)"
F9_AT_COST_RATE_MM_LAUNCH_READ_FROM_LAUNCH_CAPACITY: Final[str] = "F9 at-cost rate ($mm/launch) — read from Launch Capacity"
F9_BASE_BOOSTER_BUILD_RATE_BOOSTERS_YEAR_PRE_V3_TRIGGER: Final[str] = "F9 base booster build rate (boosters/year, pre-V3-trigger)"
F9_BOOSTER_1ST_STAGE_MFG_COST_MM_UNIT: Final[str] = "F9 booster (1st stage) mfg cost ($mm/unit)"
F9_BOOSTER_D_A_SHARE_PER_LAUNCH_MM: Final[str] = "F9 booster D&A share per launch ($mm)"
F9_BOOSTER_REFURB_OF_MFG: Final[str] = "F9 booster refurb % of mfg"
F9_BUILD_RATE_DECAY_WINDOW_YEARS: Final[str] = "F9 build-rate decay window (years)"
F9_CADENCE_PER_BOOSTER_FLIGHTS_YEAR_FLAT: Final[str] = "F9 cadence per booster (flights/year, flat)"
F9_CADENCE_UTILIZATION_PER_BOOSTER_MEMO_DERIVED: Final[str] = "F9 cadence-utilization per booster (memo, derived)"
F9_CUSTOMER_LAUNCH_INSURANCE_OTHER_COGS_MM_LAUNCH: Final[str] = "F9 customer launch insurance + other COGS ($mm/launch)"
F9_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH: Final[str] = "F9 customer launch price ($mm/launch)"
F9_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH_2025_ANCHOR: Final[str] = "F9 customer launch price ($mm/launch) — 2025 anchor"
F9_CUSTOMER_LAUNCHES_PER_YEAR: Final[str] = "F9 customer launches per year"
F9_CUSTOMER_REVENUE_MM: Final[str] = "F9 customer revenue ($mm)"
F9_FAIRING_COST_NET_OF_75_RECOVERY_MM_FLIGHT: Final[str] = "F9 fairing cost net of 75% recovery ($mm/flight)"
F9_FLEET_BEGINNING_OF_YEAR_BOOSTERS: Final[str] = "F9 fleet beginning-of-year (boosters)"
F9_FLEET_END_OF_YEAR_BOOSTERS: Final[str] = "F9 fleet end-of-year (boosters)"
F9_INTERNAL_LAUNCHES_BB_DTC: Final[str] = "F9 internal launches (BB + DTC)"
F9_LAUNCHES_PER_YEAR: Final[str] = "F9 launches per year"
F9_BOOSTER_ACCOUNTING_DEPRECIATION_CAP_FLIGHTS: Final[str] = (
    "F9 booster accounting depreciation cap (flights)"
)
F9_LIFETIME_REUSES_PER_BOOSTER: Final[str] = "F9 lifetime reuses per booster"
F9_LIFETIME_REUSES_PER_BOOSTER_READ_FROM_ASSUMPTIONS: Final[str] = "F9 lifetime reuses per booster — read from Assumptions"
IMPAIRMENT_CHARGES_MM_YEAR_ROW: Final[str] = "Impairment charges ($mm/yr) — year-row"
LAUNCH_SERVICES_REVENUE_SHARE_YEAR_ROW: Final[str] = (
    "Launch Services revenue share of external CL rev — year-row"
)
F9_MANUFACTURED_PER_YEAR_UNITS_V3_TRIGGER_AWARE_DECAY_NOTE_D61_E61_HISTORICAL_ANCHORS_PRESERVED_SPRINT_11_DECISION_A_FULL_IF_BIFURCATED_FORM_DEFERRED_TO_SPRINT_12: Final[str] = "F9 manufactured per year (units) — V3-trigger-aware decay note: D61/E61 historical anchors preserved (Sprint 11 Decision A; full IF-bifurcated form deferred to Sprint 12)"
F9_PAYLOAD_TO_LEO_KG: Final[str] = "F9 payload to LEO (kg)"
F9_PER_LAUNCH_BLENDED_IRR_EXTERNAL_CUSTOMER_ECONOMICS: Final[str] = "F9 per-launch Blended IRR (external customer economics)"
F9_PER_LAUNCH_ANNUAL_MARGIN_MM_YR_CADENCE_PER_LAUNCH_MARGIN: Final[str] = "F9 per-launch annual margin ($mm/yr — cadence × per-launch margin)"
F9_PER_LAUNCH_COST_SLUG_MM_T_0_CAPEX: Final[str] = "F9 per-launch cost slug ($mm — t=0 capex)"
F9_PER_LAUNCH_OPS_COST_MM: Final[str] = "F9 per-launch ops cost ($mm)"
F9_RETIRED_PER_YEAR_BOOSTERS: Final[str] = "F9 retired per year (boosters)"
F9_RETIREMENT_RATE_OF_LAUNCHES_YEAR: Final[str] = "F9 retirement rate (% of launches/year)"
F9_STARTING_FLEET_AT_2025_SOY_BOOSTERS: Final[str] = "F9 starting fleet at 2025 SoY (boosters)"
F9_VARIABLE_COST_MM: Final[str] = "F9 variable cost ($mm)"
F9_VARIABLE_COST_PER_LAUNCH_MM: Final[str] = "F9 variable cost per launch ($mm)"
F9_VARIABLE_COST_PER_LAUNCH_MM_READ_FROM_LAUNCH_CAPACITY: Final[str] = "F9 variable cost per launch ($mm) — read from Launch Capacity"
FALCON_9_VEHICLE_SUPPLY: Final[str] = "FALCON 9 — VEHICLE SUPPLY"
FCF_CHECK: Final[str] = "FCF check"
F_REF_REFERENCE_COMPUTE_UNIT_TFLOPS_H100_FP8_DENSE: Final[str] = "F_ref — reference compute unit (TFLOPS, H100 FP8 dense)"
F_REF_REFERENCE_COMPUTE_UNIT_TFLOPS_H100_FP8: Final[str] = "F_ref — reference compute unit (TFLOPS, H100 FP8)"
FACILITY_CAPEX_PER_SATELLITE_BASE_YEAR: Final[str] = "Facility CapEx per satellite — base year ($)"
FACILITY_CAPEX_LEARNING_RATE: Final[str] = "Facility CapEx — learning rate"
FACILITY_D_A_SAT_MANUFACTURING_GROUND_STATIONS_MM_YR_FLAT: Final[str] = "Facility D&A — sat manufacturing + ground stations ($mm/yr, flat)"
FIRST_MISSION_YEAR_LUNAR_MARS: Final[str] = "First mission year (Lunar Mars)"
FLEET_ODC_COMPUTE_ENERGY_DELIVERED_GWH_YR: Final[str] = "Fleet ODC compute energy delivered (GWh/yr)"
FLEET_PFLOPS_FP8: Final[str] = "Fleet PFLOPS (FP8)"
FLEET_ANNUAL_PFLOP_HRS_DELIVERED_UTIL_ADJUSTED: Final[str] = "Fleet annual PFLOP-hrs delivered (util-adjusted)"
FLEET_COMPUTE_POWER_GW: Final[str] = "Fleet compute power (GW)"
FLEET_EXTERNAL_COMPUTE_REVENUE_MM_YR: Final[str] = "Fleet external compute revenue ($mm/yr)"
FORWARD_IRR_Y_2: Final[str] = "Forward IRR (Y+2)"
FORWARD_IRR_LOOK_AHEAD_HORIZON_YEARS: Final[str] = "Forward IRR look-ahead horizon (years)"
FORWARD_IRR_WEIGHT_W_BLENDED_1_W_SPOT_W_FORWARD: Final[str] = "Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)"
FORWARD_AGGREGATE_KG_DEMAND: Final[str] = "Forward aggregate kg demand"
FORWARD_AGGREGATE_KG_DEMAND_GROWTH_CAP_CURRENT_CAPACITY: Final[str] = "Forward aggregate kg demand growth cap (× current capacity)"
FULLY_REUSABLE_LAUNCHES_PER_YEAR_COUNT: Final[str] = "Fully-reusable launches per year (count)"
G_A_MM: Final[str] = "G&A ($mm)"
G_A_BASE_GROUP_P_L_NET_LOCK_D_2026_05_22: Final[str] = "G&A base — Group P&L net (Lock d 2026-05-22)"
G_A_OF_GROUP_REV_BOUNDED_CAGR_DRIFT_TOWARD_CEILING: Final[str] = "G&A — % of group rev (bounded-CAGR, drift toward ceiling)"
GNI_PER_CAPITA_GROWTH_RATE_ANNUAL: Final[str] = "GNI per capita growth rate (annual)"
GROUP_FCF_MM: Final[str] = "GROUP FCF ($mm)"
GROUP_P_L_CONSOLIDATED_REVENUE_EBITDA_D_A_EBIT_TAXES_NOPAT_CAPEX_FCF_INTER_MODULE_ELIMINATIONS_CONSERVATION_BLOCK_SPRINT_9_FILLS_THE_P_L_WALK_ABOVE_ROW_99: Final[str] = "GROUP P&L -- consolidated Revenue / EBITDA / D&A / EBIT / Taxes / NOPAT / CapEx / FCF + inter-module eliminations + conservation block. Sprint 9 fills the P&L walk above row 99."
GROUP_REVENUE_NET_OF_ELIMS_MM: Final[str] = "GROUP REVENUE NET OF ELIMS ($mm)"
GBPS_PER_GWH_YR_ODC_COMPUTE_ENERGY_CONVERSION_FACTOR: Final[str] = "Gbps per GWh/yr ODC compute energy conversion factor"
GBPS_PER_GWH_YR_OF_ODC_COMPUTE_ENERGY: Final[str] = "Gbps per GWh/yr of ODC compute energy"
GEN_ENG_D_A_MM: Final[str] = "Gen eng D&A ($mm)"
GENERAL_ADMINISTRATIVE_CAGR_DRIFT: Final[str] = "General & Administrative — CAGR (drift)"
GENERAL_ADMINISTRATIVE_END_STATE_CEILING: Final[str] = "General & Administrative — end-state % (ceiling)"
GENERAL_ADMINISTRATIVE_START_OF_GROUP_REV: Final[str] = "General & Administrative — start % of group rev"
GENERAL_ENGINEERING_FACILITIES_CAPEX_MM: Final[str] = "General engineering facilities CapEx ($mm)"
GENERAL_ENGINEERING_FACILITIES_CAPEX_MM_YR_FLAT: Final[str] = "General engineering facilities CapEx ($mm/yr, flat)"
GENERAL_ENGINEERING_FACILITIES_LIFE_YEARS: Final[str] = "General engineering facilities life (years)"
GOVERNMENT_LAUNCH_MARKET_SIZE_MM_YEAR_YEAR_ROW: Final[str] = "Government launch market size ($mm/year) — year-row"
GROK_CONSUMER_ARPU_USER_YEAR: Final[str] = "Grok consumer ARPU ($/user/year)"
GROK_CONSUMER_PAID_SUBS_MILLIONS_YEAR_ROW: Final[str] = "Grok consumer paid subs (millions) — year-row"
GROK_ENTERPRISE_API_PRICE_MTOKEN_YEAR_ROW: Final[str] = "Grok enterprise API price ($/Mtoken) — year-row"
GROK_ENTERPRISE_API_TOKEN_VOLUME_T_TOKENS_YEAR_YEAR_ROW: Final[str] = "Grok enterprise API token volume (T tokens/year) — year-row"
GROSS_PROFIT_MM: Final[str] = "Gross Profit ($mm)"
GROUND_OPS_COST_MM: Final[str] = "Ground ops cost ($mm)"
GROUND_STATION_NETWORK_OPEX_OF_REVENUE: Final[str] = "Ground station / network opex % of revenue"
GROUP_COGS_NET_OF_ELIMS_MM: Final[str] = "Group COGS (net of elims) ($mm)"
GROUP_D_A_MM: Final[str] = "Group D&A ($mm)"
GROUP_EBIT_MM: Final[str] = "Group EBIT ($mm)"
GROUP_EBITDA_MM: Final[str] = "Group EBITDA ($mm)"
GROUP_GROSS_PROFIT_MM: Final[str] = "Group Gross Profit ($mm)"
GROUP_WACC: Final[str] = "Group WACC"
HQ_D_A_MM: Final[str] = "HQ D&A ($mm)"
HQ_BUILDINGS_CAPEX_MM: Final[str] = "HQ buildings CapEx ($mm)"
HQ_BUILDINGS_CAPEX_MM_YR_FLAT: Final[str] = "HQ buildings CapEx ($mm/yr, flat)"
HQ_BUILDINGS_USEFUL_LIFE_YEARS: Final[str] = "HQ buildings useful life (years)"
HARDWARE_KG_LANDED_YEAR_ROW: Final[str] = "Hardware $/kg landed (year-row)"
HARDWARE_REPLACEMENT_COST_FACTOR_KG_LANDED_DECLINING: Final[str] = "Hardware replacement cost factor ($/kg landed) — declining"
INPUTS_FROM_CENTRAL_ALLOCATOR: Final[str] = "INPUTS FROM CENTRAL ALLOCATOR"
IPO_INJECTION_AMOUNT_MM: Final[str] = "IPO injection amount ($mm)"
IPO_INJECTION_THIS_YEAR_MM: Final[str] = "IPO injection this year ($mm)"
IPO_INJECTION_YEAR: Final[str] = "IPO injection year"
PRE_IPO_BRIDGE_DRAWDOWN_YEAR: Final[str] = "Pre-IPO bridge year of drawdown"
PRE_IPO_DEBT_FACILITY_MM: Final[str] = "Pre-IPO debt facility ($mm)"
RESTRUCTURING_CHARGES_MM_YEAR_ROW: Final[str] = "Restructuring charges ($mm/yr) — year-row"
SHARE_BASED_COMPENSATION_MM_YEAR_ROW: Final[str] = "Share-based compensation ($mm/yr) — year-row"
IT_D_A_MM: Final[str] = "IT D&A ($mm)"
INFLATION_RATE_PER_YEAR: Final[str] = "Inflation rate (% per year)"
INSURANCE_MM: Final[str] = "Insurance ($mm)"
INTEGRATION_TEST_COST_PER_SAT_PRE_WL: Final[str] = "Integration & Test cost per sat ($, pre-WL)"
INTEGRATION_TEST_FLAT_COST: Final[str] = "Integration & Test flat cost ($)"
INTERNAL_BANDWIDTH_ELIMINATED_MM: Final[str] = "Internal bandwidth eliminated ($mm)"
INTERNAL_COMPUTE_PFLOP_HRS_DELIVERED_TO_AI_STACK: Final[str] = "Internal compute PFLOP-hrs delivered to AI Stack"
INTERNAL_COMPUTE_ELIMINATED_MM: Final[str] = "Internal compute eliminated ($mm)"
INTERNAL_COMPUTE_SHARE_TO_AI_STACK_YEAR_ROW: Final[str] = "Internal compute share to AI Stack % — year-row"
INTERNAL_LAUNCH_SERVICES_ELIMINATED_MM: Final[str] = "Internal launch services eliminated ($mm)"
INTERNAL_TRANSFER_REVENUE_AT_COST_COMPUTE_MM: Final[str] = "Internal transfer revenue (at-cost compute) ($mm)"
INTERNAL_TRANSFER_REVENUE_AT_COST_COMPUTE_MM_YR: Final[str] = "Internal transfer revenue (at-cost compute) ($mm/yr)"
KG_RESERVATION_OFF_THE_TOP_ARCHITECTURE_11_3_6_4: Final[str] = "KG RESERVATION OFF-THE-TOP (Architecture §11.3 + §6.4)"
KG_DEMAND_YEAR_ROW_PUBLISHED_KG_MASKED_BY_BLENDED_IRR_0: Final[str] = "Kg demand year-row published (kg) — masked by Blended IRR > 0"
LAUNCH_SERVICES_PAID_TO_LAUNCH_CAPACITY_AT_FULLY_ALLOCATED_AT_COST_RATE: Final[str] = "LAUNCH SERVICES (paid to Launch Capacity at fully-allocated at-cost rate)"
LR_CHIPS_PER_DOUBLING: Final[str] = "LR — chips (per doubling)"
LR_SUBSYSTEMS_PER_DOUBLING: Final[str] = "LR — subsystems (per doubling)"
LUNAR_MARS_P_L_ARCHITECTURE_11_5: Final[str] = "LUNAR MARS P&L (Architecture §11.5)"
LUNAR_MISSION_DEPLOYMENT_ARCHITECTURE_11_2: Final[str] = "LUNAR MISSION DEPLOYMENT (Architecture §11.2)"
LUNAR_ACCUMULATED_BOOK_VALUE_YEAR: Final[str] = "LUNAR accumulated book value (year)"
LUNAR_ACTIVE_LABOUR_FLEET_EOY_RUNNING_SUM_NET_RETIREMENTS: Final[str] = "LUNAR active labour fleet EoY (running sum, net retirements)"
LUNAR_ANNUAL_BV_CONTRIBUTION_MM_YR: Final[str] = "LUNAR annual BV contribution ($mm/yr)"
LUNAR_ANNUAL_HARDWARE_VALUE_ADD_MM_YR: Final[str] = "LUNAR annual hardware value add ($mm/yr)"
LUNAR_ANNUAL_PRODUCTION_OUTPUT_MM_YR: Final[str] = "LUNAR annual production output ($mm/yr)"
LUNAR_LABOUR_UNITS_LANDED_COUNT_THIS_YEAR: Final[str] = "LUNAR labour units landed (count this year)"
LUNAR_LABOUR_UNITS_RETIRED_THIS_YEAR_COHORT_LOOKBACK: Final[str] = "LUNAR labour units retired this year (cohort lookback)"
LABOUR_ANNUAL_OUTPUT_PER_UNIT_BASE_YEAR_MM_YR: Final[str] = "Labour annual output per unit base year ($mm/yr)"
LABOUR_ANNUAL_OUTPUT_PER_UNIT_THIS_YEAR_MM_YR: Final[str] = "Labour annual output per unit this year ($mm/yr)"
LABOUR_UNIT_BASE_HOURLY_OUTPUT_HR: Final[str] = "Labour unit base hourly output ($/hr)"
LABOUR_UNIT_BASE_HOURLY_OUTPUT_HR_BURDENED_22_0_7: Final[str] = "Labour unit base hourly output ($/hr; burdened $22/0.7)"
LABOUR_UNIT_COST_UNIT_DECLINING_CURVE: Final[str] = "Labour unit cost ($/unit) — declining curve"
LABOUR_UNIT_DAILY_WORKING_HOURS: Final[str] = "Labour unit daily working hours"
LABOUR_UNIT_MASS_KG: Final[str] = "Labour unit mass (kg)"
LABOUR_UNIT_OPERATIONAL_LIFESPAN_ON_SURFACE_YEARS: Final[str] = "Labour unit operational lifespan on surface (years)"
LABOUR_UNIT_PRODUCTIVITY_FACTOR: Final[str] = "Labour unit productivity factor"
LABOUR_UNIT_PRODUCTIVITY_FACTOR_VS_HUMAN_BASELINE: Final[str] = "Labour unit productivity factor vs human baseline"
LABOUR_UNIT_PRODUCTIVITY_LEARNING_RATE_YR: Final[str] = "Labour unit productivity learning rate (%/yr)"
LABOUR_UNIT_USEFUL_LIFE_YRS: Final[str] = "Labour unit useful life (yrs)"
LAUNCH_INSURANCE_OF_EXTERNAL_REVENUE: Final[str] = "Launch insurance % of external revenue"
LAUNCH_OTHER_COGS_OF_EXTERNAL_REVENUE: Final[str] = "Launch other COGS % of external revenue"
LAUNCH_SERVICES_COST_MM_INTERNAL_AT_COST_FROM_CUSTOMER_LAUNCH: Final[str] = "Launch services cost ($mm) — internal at-cost from Customer Launch"
LAUNCH_SERVICES_COST_PER_SAT_MM: Final[str] = "Launch services cost per sat ($mm)"
LAUNCH_SERVICES_ELIMINATION_CONSERVATION: Final[str] = "Launch services elimination conservation"
LAUNCHES_PER_STARSHIP_VEHICLE_PER_YEAR_CADENCE_VARIANT_BLEND_USED_FOR_SIZING: Final[str] = "Launches per Starship vehicle per year (cadence × variant blend, used for sizing)"
LAUNCHES_PER_STARSHIP_VEHICLE_PER_YEAR_CADENCE: Final[str] = "Launches per Starship vehicle per year (cadence)"
LEGACY_V1_V1_5_ACTIVE_BANDWIDTH_GBPS_YEAR_ROW_RUNOFF: Final[str] = "Legacy V1/V1.5 Active Bandwidth (Gbps, year-row runoff)"
LEGACY_V1_V1_5_BANDWIDTH_END_2025_GBPS: Final[str] = "Legacy V1/V1.5 Bandwidth — end-2025 (Gbps)"
LEGACY_V1_V1_5_D_A_BASELINE_MM_2025_ANCHOR: Final[str] = "Legacy V1/V1.5 D&A baseline ($mm, 2025 anchor)"
LEGACY_V1_V1_5_D_A_USEFUL_LIFE_YRS: Final[str] = "Legacy V1/V1.5 D&A useful life (yrs)"
LEVERAGE_E_V_MEMO: Final[str] = "Leverage E/V (memo)"
LIFETIME_REUSES_PER_BOOSTER_YEAR_CAP: Final[str] = "Lifetime reuses per booster (year cap)"
LIFETIME_REUSES_PER_SHIP_CAP: Final[str] = "Lifetime reuses per ship (cap)"
LUNAR_PAYLOAD_AS_LABOUR_UNITS: Final[str] = "Lunar % payload as labour units"
LUNAR_MARS_TERMINAL_BV_MULTIPLIER: Final[str] = "Lunar / Mars — terminal BV multiplier"
LUNAR_ACCUMULATED_BOOK_VALUE_MM: Final[str] = "Lunar Accumulated Book Value ($mm)"
LUNAR_MARS_BLENDED_IRR_HARDCODED_0_PER_ARCHITECTURE_11_6: Final[str] = "Lunar Mars Blended IRR (hardcoded 0 per Architecture §11.6)"
LUNAR_MARS_MODULE_CAPEX_MM: Final[str] = "Lunar Mars Module CapEx ($mm)"
LUNAR_MARS_MODULE_D_A_MM: Final[str] = "Lunar Mars Module D&A ($mm)"
LUNAR_MARS_CASH_ALLOCATION: Final[str] = "Lunar Mars cash allocation"
LUNAR_MARS_FORWARD_KG_DEMAND_AT_T_LEAD: Final[str] = "Lunar Mars forward kg demand at T+lead"
LUNAR_MARS_KG_ALLOCATION: Final[str] = "Lunar Mars kg allocation"
LUNAR_MARS_KG_RESERVED_OFF_THE_TOP: Final[str] = "Lunar Mars kg reserved (off-the-top)"
LUNAR_MARS_TOTAL_KG_RESERVED_OFF_TOP_KG_TO_LEO: Final[str] = "Lunar Mars total kg reserved off-top (kg-to-LEO)"
LUNAR_CASH_ALLOCATION_MM: Final[str] = "Lunar cash allocation ($mm)"
LUNAR_DEPOT_MULTIPLIER: Final[str] = "Lunar depot multiplier (×)"
LUNAR_FUEL_DEPOT_MULTIPLIER_PER_OUTBOUND_STARSHIP: Final[str] = "Lunar fuel depot multiplier per outbound Starship"
LUNAR_HARDWARE_MASS_LANDED_KG: Final[str] = "Lunar hardware mass landed (kg)"
LUNAR_LABOUR_MASS_LANDED_KG: Final[str] = "Lunar labour mass landed (kg)"
LUNAR_LABOUR_SHARE_OF_SURFACE_PAYLOAD_YEAR_ROW: Final[str] = "Lunar labour share of surface payload — year-row"
LUNAR_LABOUR_SHARE_THIS_YEAR: Final[str] = "Lunar labour share this year (%)"
LUNAR_PAYLOAD_PER_SURFACE_SHIP_KG: Final[str] = "Lunar payload per surface ship (kg)"
LUNAR_PAYLOAD_PER_SURFACE_LANDED_STARSHIP_KG: Final[str] = "Lunar payload per surface-landed Starship (kg)"
LUNAR_PAYLOAD_VALUE_MM_SHIP: Final[str] = "Lunar payload value ($mm/ship)"
LUNAR_SHARE_OF_MARS_MOON_CARVE_OUT_CASH_YEAR_ROW: Final[str] = "Lunar share of Mars/Moon carve-out cash — year-row"
LUNAR_SHARE_OF_CARVE_OUT_YEAR_ROW: Final[str] = "Lunar share of carve-out (% — year-row)"
LUNAR_SURFACE_MISSIONS_DEPLOYED_COUNT: Final[str] = "Lunar surface missions deployed (count)"
LUNAR_SURFACE_PAYLOAD_MASS_KG_LANDED: Final[str] = "Lunar surface payload mass (kg landed)"
LUNAR_TOTAL_LAUNCHES_LEO_PAYLOAD_KG: Final[str] = "Lunar total launches × LEO payload (kg)"
LUNAR_TOTAL_VEHICLE_LAUNCHES_COUNT: Final[str] = "Lunar total vehicle launches (count)"
MARS_MISSION_DEPLOYMENT_ARCHITECTURE_11_2: Final[str] = "MARS MISSION DEPLOYMENT (Architecture §11.2)"
MARS_ACCUMULATED_BOOK_VALUE_YEAR: Final[str] = "MARS accumulated book value (year)"
MARS_ACTIVE_LABOUR_FLEET_EOY_RUNNING_SUM_NET_RETIREMENTS: Final[str] = "MARS active labour fleet EoY (running sum, net retirements)"
MARS_ANNUAL_BV_CONTRIBUTION_MM_YR: Final[str] = "MARS annual BV contribution ($mm/yr)"
MARS_ANNUAL_HARDWARE_VALUE_ADD_MM_YR: Final[str] = "MARS annual hardware value add ($mm/yr)"
MARS_ANNUAL_PRODUCTION_OUTPUT_MM_YR: Final[str] = "MARS annual production output ($mm/yr)"
MARS_LABOUR_UNITS_LANDED_COUNT_THIS_YEAR: Final[str] = "MARS labour units landed (count this year)"
MARS_LABOUR_UNITS_RETIRED_THIS_YEAR_COHORT_LOOKBACK: Final[str] = "MARS labour units retired this year (cohort lookback)"
MEMO_DIAGNOSTICS: Final[str] = "MEMO: DIAGNOSTICS"
MFW_IRR_AI_STACK_ECONOMIC_LIFE_N_YEARS: Final[str] = "MFW-IRR — AI Stack economic life N (years)"
MFW_IRR_CUSTOMER_LAUNCH_ECONOMIC_LIFE_CLAMP_MAX_YEARS: Final[str] = "MFW-IRR — Customer Launch economic life clamp MAX (years)"
MFW_IRR_CUSTOMER_LAUNCH_ECONOMIC_LIFE_CLAMP_MIN_YEARS: Final[str] = "MFW-IRR — Customer Launch economic life clamp MIN (years)"
MFW_IRR_ODC_ECONOMIC_LIFE_N_YEARS: Final[str] = "MFW-IRR — ODC economic life N (years)"
MFW_IRR_STARLINK_ECONOMIC_LIFE_N_YEARS: Final[str] = "MFW-IRR — Starlink economic life N (years)"
MODULE_P_L: Final[str] = "MODULE P&L"
MANUFACTURING_LEARNING_RATE_PER_DOUBLING_OF_CUM_UNITS: Final[str] = "Manufacturing learning rate (per doubling of cum units)"
MARS_PAYLOAD_AS_LABOUR_UNITS: Final[str] = "Mars % payload as labour units"
MARS_ACCUMULATED_BOOK_VALUE_MM: Final[str] = "Mars Accumulated Book Value ($mm)"
MARS_CARVE_OUT_OF_PRIOR_YEAR_GROUP_FCF: Final[str] = "Mars carve-out % of prior-year Group FCF"
MARS_CARVE_OUT_OF_PRIOR_YEAR_GROUP_FCF_INPUT: Final[str] = "Mars carve-out % of prior-year Group FCF (input)"
MARS_CARVE_OUT_FLOOR_MM_YR: Final[str] = "Mars carve-out floor ($mm/yr)"
MARS_CARVE_OUT_FLOOR_MM_YR_INPUT: Final[str] = "Mars carve-out floor ($mm/yr) (input)"
MARS_CARVE_OUT_USES_PRIOR_YEAR_FCF_0_1: Final[str] = "Mars carve-out uses prior-year FCF (0/1)"
MARS_CASH_ALLOCATION_MM: Final[str] = "Mars cash allocation ($mm)"
MARS_DEPOT_MULTIPLIER: Final[str] = "Mars depot multiplier (×)"
MARS_FUEL_DEPOT_MULTIPLIER_PER_OUTBOUND_STARSHIP: Final[str] = "Mars fuel depot multiplier per outbound Starship"
MARS_HARDWARE_MASS_LANDED_KG: Final[str] = "Mars hardware mass landed (kg)"
MARS_LABOUR_MASS_LANDED_KG: Final[str] = "Mars labour mass landed (kg)"
MARS_LABOUR_SHARE_OF_SURFACE_PAYLOAD_YEAR_ROW: Final[str] = "Mars labour share of surface payload — year-row"
MARS_LABOUR_SHARE_THIS_YEAR: Final[str] = "Mars labour share this year (%)"
MARS_PAYLOAD_PER_SURFACE_SHIP_KG: Final[str] = "Mars payload per surface ship (kg)"
MARS_PAYLOAD_PER_SURFACE_LANDED_STARSHIP_KG: Final[str] = "Mars payload per surface-landed Starship (kg)"
MARS_PAYLOAD_VALUE_MM_SHIP: Final[str] = "Mars payload value ($mm/ship)"
MARS_SHARE_OF_CARVE_OUT_YEAR_ROW: Final[str] = "Mars share of carve-out (% — year-row)"
MARS_SHARE_OF_CARVE_OUT_CASH_YEAR_ROW: Final[str] = "Mars share of carve-out cash — year-row"
MARS_SURFACE_MISSIONS_DEPLOYED_COUNT: Final[str] = "Mars surface missions deployed (count)"
MARS_SURFACE_PAYLOAD_MASS_KG_LANDED: Final[str] = "Mars surface payload mass (kg landed)"
MARS_TOTAL_LAUNCHES_LEO_PAYLOAD_KG: Final[str] = "Mars total launches × LEO payload (kg)"
MARS_TOTAL_VEHICLE_LAUNCHES_COUNT: Final[str] = "Mars total vehicle launches (count)"
MARS_MOON_R_D_MM_YR_YEAR_ROW: Final[str] = "Mars/Moon R&D ($mm/yr) — year-row"
MARS_MOON_CARVE_OUT_CLAIM_MM: Final[str] = "Mars/Moon carve-out claim ($mm)"
MARS_MOON_STRATEGIC_CARVE_OUT_MM: Final[str] = "Mars/Moon strategic carve-out ($mm)"
MARS_MOON_STRATEGIC_CARVE_OUT_MM_YR: Final[str] = "Mars/Moon strategic carve-out ($mm/yr)"
MAX_ANNUAL_PRODUCTION_GROWTH_RATE_MULTIPLIER: Final[str] = "Max annual production growth rate (multiplier)"
MEMO_2025_CALIBRATION_PASS_CHECK: Final[str] = "Memo: 2025 calibration PASS/CHECK"
MEMO_2025_CALIBRATION_ANCHORS_READ_ONLY_DIAGNOSTICS: Final[str] = "Memo: 2025 calibration anchors (read-only diagnostics)"
MEMO_2025_CALIBRATION_STATUS: Final[str] = "Memo: 2025 calibration status"
MEMO_AVERAGE_GBPS_BB_FROM_CURVE_BB_REVENUE_BB_GBPS_1E6: Final[str] = "Memo: Average $/Gbps BB from curve (= BB Revenue / BB Gbps × 1e6)"
MEMO_AVERAGE_GBPS_DTC_FROM_CURVE_DTC_REVENUE_DTC_GBPS_1E6: Final[str] = "Memo: Average $/Gbps DTC from curve (= DTC Revenue / DTC Gbps × 1e6)"
MEMO_BV_DECAY_LUNAR_MM_YR_VALUATION_INPUT_ONLY_NOT_IN_GROUP_D_A: Final[str] = "Memo: BV decay — Lunar ($mm/yr) — Valuation input only, NOT in Group D&A"
MEMO_BV_DECAY_MARS_MM_YR_VALUATION_INPUT_ONLY_NOT_IN_GROUP_D_A: Final[str] = "Memo: BV decay — Mars ($mm/yr) — Valuation input only, NOT in Group D&A"
MEMO_CARVE_OUT_VS_MODULE_CAPEX_GAP_MM: Final[str] = "Memo: Carve-out vs Module CapEx gap ($mm)"
MEMO_CORPORATE_D_A_MM: Final[str] = "Memo: Corporate D&A ($mm)"
MEMO_CUM_V3_BB_SATS_LAUNCHED_RUNNING_SUM_RULE_23_EXCEPTION_YEAR_CHAINED: Final[str] = "Memo: Cum V3 BB sats launched (running sum) — Rule 23 exception, year-chained"
MEMO_CUSTOMER_LAUNCH_MODULE_D_A_IN_COGS_MM: Final[str] = "Memo: Customer Launch Module D&A in COGS ($mm)"
MEMO_CUSTOMER_LAUNCH_EXTERNAL_REVENUE_MM: Final[str] = "Memo: Customer Launch external revenue ($mm)"
MEMO_F9_CUSTOMER_LAUNCHES_2025: Final[str] = "Memo: F9 customer launches 2025"
MEMO_F9_CUSTOMER_REVENUE_2025_TARGET_4_290M_5: Final[str] = "Memo: F9 customer revenue 2025 (target $4,290M ±5%)"
MEMO_FACILITY_D_A_SAT_MANUFACTURING_GROUND_STATIONS_MM: Final[str] = "Memo: Facility D&A — sat manufacturing + ground stations ($mm)"
MEMO_GROUP_D_A_2025_DELTA: Final[str] = "Memo: Group D&A 2025 delta (%)"
MEMO_GROUP_D_A_2025_TARGET_MM_REVISED: Final[str] = "Memo: Group D&A 2025 target ($mm) — REVISED"
MEMO_GROUP_EBITDA_2025_DELTA: Final[str] = "Memo: Group EBITDA 2025 delta (%)"
MEMO_GROUP_EBITDA_2025_TARGET_MM_REVISED: Final[str] = "Memo: Group EBITDA 2025 target ($mm) — REVISED"
MEMO_GROUP_FCF_2025_DELTA: Final[str] = "Memo: Group FCF 2025 delta (%)"
MEMO_GROUP_FCF_2025_TARGET_MM_REVISED: Final[str] = "Memo: Group FCF 2025 target ($mm) — REVISED"
MEMO_GROUP_GROSS_PROFIT_2025_DELTA: Final[str] = "Memo: Group Gross Profit 2025 delta (%)"
MEMO_GROUP_GROSS_PROFIT_2025_TARGET_MM_REVISED: Final[str] = "Memo: Group Gross Profit 2025 target ($mm) — REVISED"
MEMO_GROUP_REVENUE_2025_DELTA: Final[str] = "Memo: Group Revenue 2025 delta (%)"
MEMO_GROUP_REVENUE_2025_TARGET_MM_REVISED: Final[str] = "Memo: Group Revenue 2025 target ($mm) — revised"
MEMO_GROUP_REVENUE_SPRINT_8_PRE_AGGREGATION_SUM_OF_5_MODULE_R201S: Final[str] = "Memo: Group revenue (Sprint 8 pre-aggregation; sum of 5 module R201s)"
MEMO_LEGACY_V1_V1_5_D_A_MM: Final[str] = "Memo: Legacy V1/V1.5 D&A ($mm)"
MEMO_LUNAR_LABOUR_ANNUAL_OUTPUT_MM_YR: Final[str] = "Memo: Lunar labour annual output ($mm/yr)"
MEMO_LUNAR_SURFACE_MISSIONS_CUMULATIVE: Final[str] = "Memo: Lunar surface missions cumulative"
MEMO_MARS_LABOUR_ANNUAL_OUTPUT_MM_YR: Final[str] = "Memo: Mars labour annual output ($mm/yr)"
MEMO_MARS_SURFACE_MISSIONS_CUMULATIVE: Final[str] = "Memo: Mars surface missions cumulative"
MEMO_ODC_SAT_D_A_IN_COGS_MM: Final[str] = "Memo: ODC sat D&A in COGS ($mm)"
MEMO_Q4_25_GROUP_EBITDA_ORIGINAL_TARGET_MM_ARCHAEOLOGY: Final[str] = "Memo: Q4'25 Group EBITDA original target ($mm) — archaeology"
MEMO_Q4_25_GROUP_FCF_ORIGINAL_TARGET_MM_ARCHAEOLOGY: Final[str] = "Memo: Q4'25 Group FCF original target ($mm) — archaeology"
MEMO_SPECTRUM_AMORT_MM: Final[str] = "Memo: Spectrum amort ($mm)"
MEMO_SPRINT_8_GROUP_D_A_CONTRIBUTION_CORPORATE_D_A_SPECTRUM_AMORT: Final[str] = "Memo: Sprint 8 Group D&A contribution (Corporate D&A + Spectrum amort)"
MEMO_STARLINK_CONSTELLATION_D_A_IN_STARLINK_COGS_MM: Final[str] = "Memo: Starlink Constellation D&A in Starlink COGS ($mm)"
MEMO_STARSHIP_AT_COST_RATE_SHIP_EXPENDED_MODE_MOON_MARS_MM_LAUNCH: Final[str] = "Memo: Starship at-cost rate, ship-expended mode (Moon/Mars, $mm/launch)"
MEMO_STARSHIP_CUSTOMER_REVENUE_2025_TARGET_0_EXACT: Final[str] = "Memo: Starship customer revenue 2025 (target $0 exact)"
MEMO_TOTAL_GROUP_CAPEX_2025_READ_FROM_CAPEX_TAB: Final[str] = "Memo: Total Group CapEx 2025 (read from CapEx tab)"
MEMO_TOTAL_LUNAR_MARS_VEHICLE_LAUNCHES_THIS_YEAR: Final[str] = "Memo: Total Lunar + Mars vehicle launches this year"
MEMO_TOTAL_OPEX_2025_READ_FROM_OPEX_TAB: Final[str] = "Memo: Total OpEx 2025 (read from OpEx tab)"
MEMO_TOTAL_OPEX_2025_CALIBRATION_ANCHOR_MM: Final[str] = "Memo: Total OpEx 2025 calibration anchor ($mm)"
MEMO_TOTAL_OPEX_2025_CALIBRATION_DELTA: Final[str] = "Memo: Total OpEx 2025 calibration delta (%)"
MEMO_TOTAL_R_D_2025_CALIBRATION_ANCHOR_MM: Final[str] = "Memo: Total R&D 2025 calibration anchor ($mm)"
MEMO_TOTAL_ACTIVE_STARLINK_SATS_EXCL_LEGACY_V1_V1_5: Final[str] = "Memo: Total active Starlink sats (excl legacy V1/V1.5)"
MEMO_TOTAL_CARVE_OUT_RESERVED_THIS_YEAR_MM: Final[str] = "Memo: Total carve-out reserved this year ($mm)"
MEMO_V2_BB_BLENDED_IRR: Final[str] = "Memo: V2 BB Blended IRR"
MEMO_V2_BB_FORWARD_IRR_Y_2: Final[str] = "Memo: V2 BB Forward IRR (Y+2)"
MEMO_V2_BB_SPOT_IRR: Final[str] = "Memo: V2 BB Spot IRR"
MEMO_V2_BB_PER_SAT_COST_MM_SAT_SAT_UNIT_COST_FACILITY_PER_SAT: Final[str] = "Memo: V2 BB per-sat cost ($mm/sat) — sat unit cost + facility per sat"
MEMO_V2_BB_PER_SAT_NET_MARGINAL_REVENUE_PER_YEAR_MM_SAT_YR: Final[str] = "Memo: V2 BB per-sat net marginal revenue per year ($mm/sat/yr)"
MEMO_V2_DTC_BLENDED_IRR: Final[str] = "Memo: V2 DTC Blended IRR"
MEMO_V2_DTC_FORWARD_IRR_Y_2: Final[str] = "Memo: V2 DTC Forward IRR (Y+2)"
MEMO_V2_DTC_SPOT_IRR: Final[str] = "Memo: V2 DTC Spot IRR"
MEMO_V2_DTC_PER_SAT_COST_MM_SAT: Final[str] = "Memo: V2 DTC per-sat cost ($mm/sat)"
MEMO_V2_DTC_PER_SAT_NET_MARGINAL_REVENUE_PER_YEAR_MM_SAT_YR: Final[str] = "Memo: V2 DTC per-sat net marginal revenue per year ($mm/sat/yr)"
MEMO_V3_BB_BLENDED_IRR: Final[str] = "Memo: V3 BB Blended IRR"
MEMO_V3_BB_FORWARD_IRR_Y_2: Final[str] = "Memo: V3 BB Forward IRR (Y+2)"
MEMO_V3_BB_SPOT_IRR: Final[str] = "Memo: V3 BB Spot IRR"
MEMO_V3_BB_PER_SAT_COST_MM_SAT: Final[str] = "Memo: V3 BB per-sat cost ($mm/sat)"
MEMO_V3_BB_PER_SAT_NET_MARGINAL_REVENUE_PER_YEAR_MM_SAT_YR: Final[str] = "Memo: V3 BB per-sat net marginal revenue per year ($mm/sat/yr)"
MEMO_V3_DTC_BLENDED_IRR: Final[str] = "Memo: V3 DTC Blended IRR"
MEMO_V3_DTC_FORWARD_IRR_Y_2: Final[str] = "Memo: V3 DTC Forward IRR (Y+2)"
MEMO_V3_DTC_SPOT_IRR: Final[str] = "Memo: V3 DTC Spot IRR"
MEMO_V3_DTC_PER_SAT_COST_MM_SAT: Final[str] = "Memo: V3 DTC per-sat cost ($mm/sat)"
MEMO_V3_DTC_PER_SAT_NET_MARGINAL_REVENUE_PER_YEAR_MM_SAT_YR: Final[str] = "Memo: V3 DTC per-sat net marginal revenue per year ($mm/sat/yr)"
MEMO_MODULE_D_A_IN_COGS_MM: Final[str] = "Memo: Σ Module D&A in COGS ($mm)"
MEMO_MODULE_FCF_RECONCILIATION_RESIDUAL_MM: Final[str] = "Memo: Σ Module FCF reconciliation residual ($mm)"
MISSION_OPS_COST_LUNAR_MM: Final[str] = "Mission ops cost — Lunar ($mm)"
MISSION_OPS_COST_MARS_MM: Final[str] = "Mission ops cost — Mars ($mm)"
MODULE_CAPEX_MM: Final[str] = "Module CapEx ($mm)"
MODULE_CAPEX_MM_RESTATED: Final[str] = "Module CapEx ($mm) — restated"
MODULE_D_A_MM_INFORMATIONAL_ALSO_IN_COGS_ROWS_86_88: Final[str] = "Module D&A ($mm) — informational (also in COGS rows 86 + 88)"
MODULE_D_A_ADD_BACK_MM: Final[str] = "Module D&A add-back ($mm)"
MODULE_EBITDA_MM: Final[str] = "Module EBITDA ($mm)"
MODULE_EBITDA_MARGIN: Final[str] = "Module EBITDA Margin %"
MODULE_FCF_MM: Final[str] = "Module FCF ($mm)"
MODULE_OPERATING_COST_LUNAR_OF_LUNAR_CAPEX: Final[str] = "Module operating cost — Lunar (% of Lunar CapEx)"
MODULE_OPERATING_COST_MARS_OF_MARS_CAPEX: Final[str] = "Module operating cost — Mars (% of Mars CapEx)"
MULTIPLE_AI_STACK_EV_REV_AT_2050: Final[str] = "Multiple — AI Stack (EV/Rev at 2050)"
MULTIPLE_CUSTOMER_LAUNCH_EV_REV_AT_2050: Final[str] = "Multiple — Customer Launch (EV/Rev at 2050)"
MULTIPLE_LUNAR_MARS_ANCHOR_STUB_B: Final[str] = "Multiple — Lunar / Mars (anchor stub, $B)"
MULTIPLE_ODC_EV_REV_AT_2050: Final[str] = "Multiple — ODC (EV/Rev at 2050)"
MULTIPLE_STARLINK_EV_REV_AT_2050: Final[str] = "Multiple — Starlink (EV/Rev at 2050)"
NOPAT_MM: Final[str] = "NOPAT ($mm)"
ODC_BB_GBPS_DEMAND: Final[str] = "ODC BB Gbps demand"
ODC_BB_BANDWIDTH_COST_MM_YR: Final[str] = "ODC BB bandwidth cost ($mm/yr)"
ODC_BLENDED_IRR: Final[str] = "ODC Blended IRR"
ODC_DTC_GBPS_DEMAND: Final[str] = "ODC DTC Gbps demand"
ODC_DTC_BANDWIDTH_COST_MM_YR: Final[str] = "ODC DTC bandwidth cost ($mm/yr)"
ODC_FULLY_ALLOCATED_COST_AT_COST_COMPUTE_RATE_ARCHITECTURE_7_3: Final[str] = "ODC FULLY-ALLOCATED COST + AT-COST COMPUTE RATE (Architecture §7.3)"
ODC_FORWARD_IRR_Y_2: Final[str] = "ODC Forward IRR (Y+2)"
ODC_MODULE_CAPEX_MM: Final[str] = "ODC Module CapEx ($mm)"
ODC_R_D_PROFILE_MM_PRE_REVENUE_FLOOR: Final[str] = "ODC R&D $-profile ($mm, pre-revenue floor)"
ODC_R_D_PROFILE_MM_YR_YEAR_ROW: Final[str] = "ODC R&D $-profile ($mm/yr) — year-row"
ODC_R_D_MM_MAX_PROFILE_REV: Final[str] = "ODC R&D ($mm) — MAX($-profile, % × rev)"
ODC_R_D_BASE_ODC_REV_MM: Final[str] = "ODC R&D base — ODC rev ($mm)"
ODC_R_D_OF_ODC_REV_BOUNDED_CAGR: Final[str] = "ODC R&D — % of ODC rev (bounded-CAGR)"
ODC_R_D_CAGR_TAPER: Final[str] = "ODC R&D — CAGR (taper)"
ODC_R_D_END_STATE_FLOOR: Final[str] = "ODC R&D — end-state % (floor)"
ODC_R_D_START_OF_ODC_REV: Final[str] = "ODC R&D — start % of ODC rev"
ODC_SAT_PHYSICAL_COST_STACK: Final[str] = "ODC SAT PHYSICAL & COST STACK"
ODC_SPOT_IRR: Final[str] = "ODC Spot IRR"
ODC_STARSHIP_KG_DEMAND: Final[str] = "ODC Starship kg demand"
ODC_STARSHIP_LAUNCHES_INTERNAL: Final[str] = "ODC Starship launches (internal)"
ODC_AT_COST_COMPUTE_RATE_PFLOP_HR: Final[str] = "ODC at-cost compute rate ($/PFLOP-hr)"
ODC_CASH_ALLOCATION: Final[str] = "ODC cash allocation"
ODC_CASH_DEMAND_MM: Final[str] = "ODC cash demand ($mm)"
ODC_CASH_DEMAND_LARGE_DEFAULT_MM: Final[str] = "ODC cash demand large default ($mm)"
ODC_CASH_DEMAND_LARGE_DEFAULT_MM_ASSUMPTIONS_READ: Final[str] = "ODC cash demand large default ($mm) — Assumptions read"
ODC_EXTERNAL_COMPUTE_SHARE_TO_CUSTOMERS_YEAR_ROW: Final[str] = "ODC external compute share to customers % — year-row"
ODC_FLEET_DESIGN_LIFE_YEARS: Final[str] = "ODC fleet design life (years)"
ODC_FORWARD_KG_DEMAND_AT_T_LEAD: Final[str] = "ODC forward kg demand at T+lead"
ODC_INSURANCE_OF_REVENUE: Final[str] = "ODC insurance % of revenue"
ODC_INTERNAL_COMPUTE_SHARE_TO_AI_STACK_YEAR_ROW: Final[str] = "ODC internal compute share to AI Stack % — year-row"
ODC_KG_ALLOCATION: Final[str] = "ODC kg allocation"
ODC_KG_DEMAND_KG_TO_LEO: Final[str] = "ODC kg demand (kg-to-LEO)"
ODC_KG_DEMAND_LARGE_DEFAULT_KG: Final[str] = "ODC kg demand large default (kg)"
ODC_KG_DEMAND_LARGE_DEFAULT_KG_ASSUMPTIONS_READ: Final[str] = "ODC kg demand large default (kg) — Assumptions read"
ODC_KG_PROPOSED_ALLOCATION: Final[str] = "ODC kg proposed allocation"
ODC_KG_WEIGHT: Final[str] = "ODC kg weight"
ODC_OTHER_COGS_OF_REVENUE: Final[str] = "ODC other COGS % of revenue"
ODC_PROPOSED_ALLOCATION_MM: Final[str] = "ODC proposed allocation ($mm)"
ODC_WEIGHT: Final[str] = "ODC weight"
OPEX_CORPORATE_OPERATING_COSTS_R_D_BY_MODULE_SG_A_BY_FUNCTION_SPRINT_8_FILLS: Final[str] = "OPEX -- corporate operating costs (R&D by module + SG&A by function). Sprint 8 fills."
OPEX_CLAIM_MM: Final[str] = "OpEx claim ($mm)"
ORBITAL_PUE: Final[str] = "Orbital PUE"
OTHER_COGS_MM: Final[str] = "Other COGS ($mm)"
OTHER_D_A_MM: Final[str] = "Other D&A ($mm)"
OTHER_CORPORATE_CAPEX_MM: Final[str] = "Other corporate CapEx ($mm)"
OTHER_CORPORATE_CAPEX_MM_YR_FLAT: Final[str] = "Other corporate CapEx ($mm/yr, flat)"
OTHER_CORPORATE_OPERATING_MM_1_GROUP_P_L_NET_LOCK_D_2026_05_22: Final[str] = "Other corporate operating ($mm) — 1% × Group P&L net (Lock d 2026-05-22)"
OTHER_CORPORATE_OPERATING_FLAT_OF_GROUP_REV: Final[str] = "Other corporate operating — flat % of group rev"
OTHER_CORPORATE_USEFUL_LIFE_YEARS: Final[str] = "Other corporate useful life (years)"
PER_SAT_MARGINAL_IRR_ENGINE_ARCHITECTURE_9_4_READS_EXTERNAL_REVENUE_ONLY_PER_7_3: Final[str] = "PER-SAT MARGINAL IRR ENGINE (Architecture §9.4, reads external revenue only per §7.3)"
PER_SHIP_COST_BUILD_ARCHITECTURE_11_2: Final[str] = "PER-SHIP COST BUILD (Architecture §11.2)"
PUE_UPLIFT_ORBITAL_ADVANTAGE_PUE_BASE_PUE_ORBITAL: Final[str] = "PUE uplift (orbital advantage = PUE_base / PUE_orbital)"
PUE_BASE_TERRESTRIAL_COLO: Final[str] = "PUE_base (terrestrial colo)"
PAYLOAD_BOOSTER_ONLY_MODE_KG_TO_LEO: Final[str] = "Payload — booster-only mode (kg-to-LEO)"
PAYLOAD_FULLY_REUSABLE_MODE_KG_TO_LEO: Final[str] = "Payload — fully reusable mode (kg-to-LEO)"
PER_LAUNCH_UPMASS_KG: Final[str] = "Per-launch upmass (kg)"
PER_LAUNCH_UPMASS_KG_FROM_LAUNCH_CAPACITY: Final[str] = "Per-launch upmass (kg) — from Launch Capacity"
PER_SAT_BB_GBPS_DEMAND: Final[str] = "Per-sat BB Gbps demand"
PER_SAT_DTC_GBPS_DEMAND: Final[str] = "Per-sat DTC Gbps demand"
PER_SAT_EXPECTED_REVENUE_MM_YR_PR_A_WEIGHTED: Final[str] = "Per-sat Expected Revenue ($mm/yr) — Pr-A-weighted"
PER_SAT_MODEL_A_REVENUE_MM_YR_ENERGY_ANCHORED: Final[str] = "Per-sat Model A revenue ($mm/yr) — energy-anchored"
PER_SAT_MODEL_B_REVENUE_MM_YR_ANCHORED: Final[str] = "Per-sat Model B revenue ($mm/yr) — η-anchored"
PER_SAT_BANDWIDTH_COST_MM_YR: Final[str] = "Per-sat bandwidth cost ($mm/yr)"
PER_SAT_BILLABLE_H100_EQUIV_GPU_HRS_YR: Final[str] = "Per-sat billable H100-equiv GPU-hrs/yr"
PER_SAT_EXTERNAL_COMPUTE_REVENUE_MM_YR_AT_MARKET: Final[str] = "Per-sat external compute revenue ($mm/yr) — at market"
PER_SAT_GROUND_OPS_COST_MM_YR: Final[str] = "Per-sat ground ops cost ($mm/yr)"
PER_SAT_INSURANCE_COST_MM_YR: Final[str] = "Per-sat insurance cost ($mm/yr)"
PER_SAT_NET_MARGINAL_REVENUE_MM_YR: Final[str] = "Per-sat net marginal revenue ($mm/yr)"
PER_SAT_OTHER_COGS_MM_YR: Final[str] = "Per-sat other COGS ($mm/yr)"
PER_SAT_UPFRONT_COST_MM_SAT_HARDWARE_LAUNCH_SERVICES_PER_SAT: Final[str] = "Per-sat upfront cost ($mm) — sat hardware + launch services per sat"
PER_SHIP_COST_LUNAR_MM: Final[str] = "Per-ship cost — Lunar ($mm)"
PER_SHIP_COST_MARS_MM: Final[str] = "Per-ship cost — Mars ($mm)"
PR_A_ARCHITECTURE_9_2: Final[str] = "Pr(A) (Architecture §9.2)"
PRICE_PER_H100_EQUIV_GPU_HR_YEAR_ROW: Final[str] = "Price per H100-equiv GPU-hr ($) — year-row"
PRIOR_YEAR_GROUP_FCF_READ_MM: Final[str] = "Prior-year Group FCF read ($mm)"
PRIOR_YEAR_GROUP_FCF_READ_MM_YR: Final[str] = "Prior-year Group FCF read ($mm/yr)"
PRODUCTIVITY_MULTIPLIER_YEAR_ROW_ANCHOR_AND_OFFSET: Final[str] = "Productivity multiplier (year-row, anchor-and-offset)"
PROJECTED_CAPACITY_AT_T_LEAD_KG_TO_LEO: Final[str] = "Projected capacity at T+lead (kg-to-LEO)"
R_D_MOON_MARS_MM_YR_YEAR_ROW: Final[str] = "R&D — Moon/Mars ($mm/yr) — year-row"
REAL_GNI_GROWTH_RATE_PER_YEAR: Final[str] = "Real GNI growth rate (% per year)"
REQUIRED_LAUNCHES_COUNT: Final[str] = "Required launches (count)"
REQUIRED_VEHICLES_COUNT: Final[str] = "Required vehicles (count)"
REVENUE_CHECK: Final[str] = "Revenue check"
RISK_PREMIUM_AI_STACK: Final[str] = "Risk premium — AI Stack"
RISK_PREMIUM_CUSTOMER_LAUNCH: Final[str] = "Risk premium — Customer Launch"
RISK_PREMIUM_LUNAR_MARS: Final[str] = "Risk premium — Lunar / Mars"
RISK_PREMIUM_ODC: Final[str] = "Risk premium — ODC"
RISK_PREMIUM_STARLINK_OVER_GROUP_WACC: Final[str] = "Risk premium — Starlink (over group WACC)"
S_M_MM: Final[str] = "S&M ($mm)"
S_M_BASE_STARLINK_STARSHIELD_CUSTOMER_LAUNCH_EXT_AI_STACK_REV_MM: Final[str] = "S&M base — Starlink + Starshield + Customer Launch ext + AI Stack rev ($mm)"
S_M_OF_BASE_BOUNDED_CAGR: Final[str] = "S&M — % of base (bounded-CAGR)"
STARLINK_CAPACITY_AGGREGATES_CONSTELLATION_BB_DTC_POOLS_ALLOCATES_INTERNAL_BANDWIDTH_CLAIM_TO_ODC_COMPUTES_AVAILABLE_BANDWIDTH_FOR_EXTERNAL_STARLINK_REVENUE_SPRINT_4_FILLS: Final[str] = "STARLINK CAPACITY -- aggregates constellation BB + DTC pools, allocates internal bandwidth claim to ODC, computes available bandwidth for external Starlink revenue. Sprint 4 fills."
STARLINK_CAPACITY_SUPPLY_SIDE_BANDWIDTH_AGGREGATION_INTERNAL_CLAIM_TO_ODC: Final[str] = "STARLINK CAPACITY — supply-side bandwidth aggregation + internal claim to ODC"
STARSHIP_VEHICLE_SUPPLY: Final[str] = "STARSHIP — VEHICLE SUPPLY"
SALES_MARKETING_CAGR_TAPER: Final[str] = "Sales & Marketing — CAGR (taper)"
SALES_MARKETING_END_STATE_FLOOR: Final[str] = "Sales & Marketing — end-state % (floor)"
SALES_MARKETING_START_OF_STARLINK_STARSHIELD_CUSTOMER_LAUNCH_EXT_REV: Final[str] = "Sales & Marketing — start % of (Starlink+Starshield+Customer Launch ext) rev"
SAT_PFLOPS_FP8_PER_SAT_PER_YEAR_COMPUTED: Final[str] = "Sat PFLOPS (FP8, per sat per year computed)"
SAT_CHIP_MASS_KG: Final[str] = "Sat chip mass (kg)"
SAT_RETIREMENTS_YEAR_ROW_N_YEAR_COHORT_LINEAR: Final[str] = "Sat retirements (year-row, N-year cohort linear)"
SAT_SOLAR_GENERATION_W: Final[str] = "Sat solar generation (W)"
SAT_SOLAR_GENERATION_W_FOR_W_SUBSYSTEM_COST: Final[str] = "Sat solar generation (W, for $/W subsystem cost)"
SAT_SUBSYSTEM_COST_PRE_WL: Final[str] = "Sat subsystem cost (pre-WL, $)"
SAT_SUBSYSTEM_COST_WITH_WL_YEAR_ROW: Final[str] = "Sat subsystem cost (with WL, $) — year-row"
SAT_THERMAL_MASS_KG: Final[str] = "Sat thermal mass (kg)"
SAT_TOTAL_COST_YEAR_ROW: Final[str] = "Sat total cost ($, year-row)"
SAT_TOTAL_COST_MM_YEAR_ROW: Final[str] = "Sat total cost ($mm, year-row)"
SATELLITE_DEP_PER_KG_ANNUAL_DECAY_RATE: Final[str] = "Satellite Dep per kg — annual decay rate"
SATELLITE_DEP_PER_KG_BASE_YEAR_KG_YR: Final[str] = "Satellite Dep per kg — base year ($/kg/yr)"
SATELLITE_COST_FLOOR_KG: Final[str] = "Satellite cost floor ($/kg)"
SATELLITE_COST_PER_KG_BASE_YEAR_KG: Final[str] = "Satellite cost per kg — base year ($/kg)"
SATELLITE_COST_PER_KG_LEARNING_RATE: Final[str] = "Satellite cost per kg — learning rate"
SATELLITE_USEFUL_LIFE_V2_DTC_YEARS: Final[str] = "Satellite useful life — V2 Mini DTC (years)"
SATELLITE_USEFUL_LIFE_V2_MINI_YEARS: Final[str] = "Satellite useful life — V2 Mini (years)"
SATELLITE_USEFUL_LIFE_V3_DTC_YEARS: Final[str] = "Satellite useful life — V3 DTC (years)"
SATELLITE_USEFUL_LIFE_V3_YEARS: Final[str] = "Satellite useful life — V3 (years)"
STARSHIP_PRECOMMERCIAL_RD_MM_YEAR_ROW: Final[str] = (
    "Starship pre-commercialization R&D ($mm/yr) — year-row"
)
STARSHIELD_S1_GOV_CONNECTIVITY_SCOPE_FACTOR: Final[str] = (
    "Starshield S-1 Government Connectivity scope factor"
)
SATS_DEPLOYABLE_FROM_CASH_ALLOCATION: Final[str] = "Sats deployable from cash allocation"
SATS_DEPLOYABLE_FROM_KG_ALLOCATION: Final[str] = "Sats deployable from kg allocation"
SATS_DEPLOYED_ACTUAL: Final[str] = "Sats deployed (actual)"
SATS_PER_F9_LAUNCH_V2_BB: Final[str] = "Sats per F9 launch — V2 BB"
SATS_PER_F9_LAUNCH_V2_DTC: Final[str] = "Sats per F9 launch — V2 DTC"
SATS_PER_STARSHIP_LAUNCH_COMPUTE_CONFIG: Final[str] = "Sats per Starship launch (Compute config)"
SATS_PER_STARSHIP_LAUNCH_V3_BB: Final[str] = "Sats per Starship launch — V3 BB"
SATS_PER_STARSHIP_LAUNCH_V3_DTC: Final[str] = "Sats per Starship launch — V3 DTC"
SHIELDING_COST_PER_SAT_PRE_WL: Final[str] = "Shielding cost per sat ($, pre-WL)"
SHIELDING_FLAT_COST: Final[str] = "Shielding flat cost ($)"
SIGMOID_IRR_BLEND_EXPONENT_K: Final[str] = "Sigmoid IRR-blend exponent k"
SOLAR_ARRAY_COST_PER_SAT_PRE_WL: Final[str] = "Solar array cost per sat ($, pre-WL)"
SOLAR_ARRAY_UNIT_COST_W: Final[str] = "Solar array unit cost ($/W)"
SOLAR_GENERATION_PER_SAT_KW_GEN_REQUIREMENT: Final[str] = "Solar generation per sat (kW, gen requirement)"
SPACEX_COMMERCIAL_MARKET_SHARE_YEAR_ROW: Final[str] = "SpaceX commercial market share % — year-row"
SPACEX_GOVERNMENT_MARKET_SHARE_YEAR_ROW: Final[str] = "SpaceX government market share % — year-row"
SPECTRUM_CAPEX_CLAIM_MM: Final[str] = "Spectrum CapEx claim ($mm)"
SPECTRUM_AMORTIZATION_BB_ONLY_MM: Final[str] = "Spectrum amortization (BB-only) ($mm)"
SPECTRUM_USEFUL_LIFE_YEARS: Final[str] = "Spectrum useful life (years)"
SPOT_IRR: Final[str] = "Spot IRR"
STARLINK_BB_REVENUE_FROM_CURVE_MM: Final[str] = "Starlink BB Revenue from curve ($mm)"
STARLINK_BB_CAPACITY_INPUT_GBPS: Final[str] = "Starlink BB capacity input (Gbps)"
STARLINK_BLENDED_IRR: Final[str] = "Starlink Blended IRR"
STARLINK_DTC_REVENUE_FROM_CURVE_MM: Final[str] = "Starlink DTC Revenue from curve ($mm)"
STARLINK_DTC_CAPACITY_INPUT_GBPS: Final[str] = "Starlink DTC capacity input (Gbps)"
STARLINK_FORWARD_IRR_Y_2: Final[str] = "Starlink Forward IRR (Y+2)"
STARLINK_MODULE_CAPEX_MM: Final[str] = "Starlink Module CapEx ($mm)"
STARLINK_R_D_MM: Final[str] = "Starlink R&D ($mm)"
STARLINK_R_D_BASE_STARLINK_STARSHIELD_REV_MM: Final[str] = "Starlink R&D base — Starlink + Starshield rev ($mm)"
STARLINK_R_D_OF_STARLINK_STARSHIELD_REV: Final[str] = "Starlink R&D — % of (Starlink + Starshield) rev"
STARLINK_R_D_CAGR_TAPER: Final[str] = "Starlink R&D — CAGR (taper)"
STARLINK_R_D_END_STATE_FLOOR: Final[str] = "Starlink R&D — end-state % (floor)"
STARLINK_R_D_START_OF_STARLINK_STARSHIELD_REV: Final[str] = "Starlink R&D — start % of (Starlink + Starshield) rev"
STARLINK_SPOT_IRR: Final[str] = "Starlink Spot IRR"
STARLINK_V2_BB_BLENDED_IRR: Final[str] = "Starlink V2 BB Blended IRR"
STARLINK_V2_BB_CASH_ALLOCATION: Final[str] = "Starlink V2 BB cash allocation"
STARLINK_V2_BB_CASH_ALLOCATION_MM: Final[str] = "Starlink V2 BB cash allocation ($mm)"
STARLINK_V2_BB_CASH_DEMAND_MM: Final[str] = "Starlink V2 BB cash demand ($mm)"
STARLINK_V2_BB_PROPOSED_ALLOCATION_MM: Final[str] = "Starlink V2 BB proposed allocation ($mm)"
STARLINK_V2_BB_WEIGHT: Final[str] = "Starlink V2 BB weight"
STARLINK_V2_DTC_BLENDED_IRR: Final[str] = "Starlink V2 DTC Blended IRR"
STARLINK_V2_DTC_CASH_ALLOCATION: Final[str] = "Starlink V2 DTC cash allocation"
STARLINK_V2_DTC_CASH_ALLOCATION_MM: Final[str] = "Starlink V2 DTC cash allocation ($mm)"
STARLINK_V2_DTC_CASH_DEMAND_MM: Final[str] = "Starlink V2 DTC cash demand ($mm)"
STARLINK_V2_DTC_PROPOSED_ALLOCATION_MM: Final[str] = "Starlink V2 DTC proposed allocation ($mm)"
STARLINK_V2_DTC_WEIGHT: Final[str] = "Starlink V2 DTC weight"
STARLINK_V3_BB_BLENDED_IRR: Final[str] = "Starlink V3 BB Blended IRR"
STARLINK_V3_BB_CASH_ALLOCATION: Final[str] = "Starlink V3 BB cash allocation"
STARLINK_V3_BB_CASH_ALLOCATION_MM: Final[str] = "Starlink V3 BB cash allocation ($mm)"
STARLINK_V3_BB_CASH_DEMAND_MM: Final[str] = "Starlink V3 BB cash demand ($mm)"
STARLINK_V3_BB_KG_ALLOCATION: Final[str] = "Starlink V3 BB kg allocation"
STARLINK_V3_BB_KG_ALLOCATION_KG_TO_LEO: Final[str] = "Starlink V3 BB kg allocation (kg-to-LEO)"
STARLINK_V3_BB_KG_DEMAND_KG_TO_LEO: Final[str] = "Starlink V3 BB kg demand (kg-to-LEO)"
STARLINK_V3_BB_KG_PROPOSED_ALLOCATION: Final[str] = "Starlink V3 BB kg proposed allocation"
STARLINK_V3_BB_KG_WEIGHT: Final[str] = "Starlink V3 BB kg weight"
STARLINK_V3_BB_PROPOSED_ALLOCATION_MM: Final[str] = "Starlink V3 BB proposed allocation ($mm)"
STARLINK_V3_BB_WEIGHT: Final[str] = "Starlink V3 BB weight"
STARLINK_V3_DTC_BLENDED_IRR: Final[str] = "Starlink V3 DTC Blended IRR"
STARLINK_V3_DTC_CASH_ALLOCATION: Final[str] = "Starlink V3 DTC cash allocation"
STARLINK_V3_DTC_CASH_ALLOCATION_MM: Final[str] = "Starlink V3 DTC cash allocation ($mm)"
STARLINK_V3_DTC_CASH_DEMAND_MM: Final[str] = "Starlink V3 DTC cash demand ($mm)"
STARLINK_V3_DTC_KG_ALLOCATION: Final[str] = "Starlink V3 DTC kg allocation"
STARLINK_V3_DTC_KG_ALLOCATION_KG_TO_LEO: Final[str] = "Starlink V3 DTC kg allocation (kg-to-LEO)"
STARLINK_V3_DTC_KG_DEMAND_KG_TO_LEO: Final[str] = "Starlink V3 DTC kg demand (kg-to-LEO)"
STARLINK_V3_DTC_KG_PROPOSED_ALLOCATION: Final[str] = "Starlink V3 DTC kg proposed allocation"
STARLINK_V3_DTC_KG_WEIGHT: Final[str] = "Starlink V3 DTC kg weight"
STARLINK_V3_DTC_PROPOSED_ALLOCATION_MM: Final[str] = "Starlink V3 DTC proposed allocation ($mm)"
STARLINK_V3_DTC_WEIGHT: Final[str] = "Starlink V3 DTC weight"
STARLINK_CASH_ALLOCATION: Final[str] = "Starlink cash allocation"
STARLINK_CASH_ASK_YEAR_ROW_MM_LARGE_DEFAULT: Final[str] = "Starlink cash ask year-row ($mm, large default)"
STARLINK_FORWARD_KG_DEMAND_AT_T_LEAD: Final[str] = "Starlink forward kg demand at T+lead"
STARLINK_GROUND_OPS_OF_REVENUE: Final[str] = "Starlink ground ops % of revenue"
STARLINK_INSURANCE_OF_REVENUE: Final[str] = "Starlink insurance % of revenue"
STARLINK_INTERNAL_BANDWIDTH_REVENUE_MM: Final[str] = "Starlink internal bandwidth revenue ($mm)"
STARLINK_KG_ALLOCATION: Final[str] = "Starlink kg allocation"
STARLINK_KG_ASK_YEAR_ROW_LARGE_DEFAULT_EXCEEDS_PLAUSIBLE_CAPACITY: Final[str] = "Starlink kg ask year-row (large default, exceeds plausible capacity)"
STARLINK_OTHER_COGS_OF_REVENUE: Final[str] = "Starlink other COGS % of revenue"
STARLINK_EXIT_REVENUE_MULTIPLE: Final[str] = "Starlink — exit revenue multiple"
STARSHIELD_GBPS_GBPS_YR: Final[str] = "Starshield $/Gbps ($/Gbps/yr)"
STARSHIELD_RESERVED_DECAY_RATE: Final[str] = "Starshield Reserved % — decay rate"
STARSHIELD_RESERVED_FLOOR: Final[str] = "Starshield Reserved % — floor"
STARSHIELD_RESERVED_START: Final[str] = "Starshield Reserved % — start"
STARSHIELD_REV_PER_GBPS_BASE_YEAR_GBPS: Final[str] = "Starshield Rev per Gbps — base year ($/Gbps)"
STARSHIELD_REV_PER_GBPS_DECAY_RATE: Final[str] = "Starshield Rev per Gbps — decay rate"
STARSHIELD_RESERVED: Final[str] = "Starshield reserved %"
STARSHIELD_RESERVED_GBPS: Final[str] = "Starshield reserved Gbps"
STARSHIELD_REVENUE_MM: Final[str] = "Starshield revenue ($mm)"
STARSHIP_2ND_STAGE_MANUFACTURING_COST_MM_UNIT: Final[str] = "Starship 2nd-stage manufacturing cost ($mm/unit)"
STARSHIP_2ND_STAGE_MANUFACTURING_COST_MM_UNIT_BASE: Final[str] = "Starship 2nd-stage manufacturing cost ($mm/unit, base)"
STARSHIP_CAPACITY_ALLOCATION_KG_TO_LEO: Final[str] = "Starship Capacity Allocation (kg-to-LEO)"
STARSHIP_D_A_SHARE_MM: Final[str] = "Starship D&A share ($mm)"
STARSHIP_D_A_SHARE_PER_LAUNCH_MM_READ_FROM_LAUNCH_CAPACITY: Final[str] = "Starship D&A share per launch ($mm) — read from Launch Capacity"
STARSHIP_D_A_SHARE_PER_LAUNCH_FULLY_REUSABLE_MODE_MM: Final[str] = "Starship D&A share per launch, fully reusable mode ($mm)"
STARSHIP_D_A_USEFUL_LIFE_MEMO_ADD_BACK_FOR_LAUNCH_STANDALONE_DCF: Final[str] = "Starship D&A useful life — memo add-back for Launch standalone DCF"
STARSHIP_FORWARD_IRR_Y_2: Final[str] = "Starship Forward IRR (Y+2)"
STARSHIP_IRR_CASHFLOW_STREAM_PERIOD_COUNT_N_CLAMPED_AT_R23_MAX_YEAR_ROW: Final[str] = "Starship IRR cashflow stream period count N (clamped at R23 MAX, year-row)"
STARSHIP_LEO_PAYLOAD_PER_LAUNCH_KG: Final[str] = "Starship LEO payload per launch (kg)"
STARSHIP_LEO_PAYLOAD_PER_LAUNCH_COMPUTE_CONFIG_KG: Final[str] = "Starship LEO payload per launch — Compute config (kg)"
STARSHIP_SPOT_IRR: Final[str] = "Starship Spot IRR"
STARSHIP_TOTAL_ANNUAL_CAPACITY_KG_TO_LEO_FROM_LAUNCH_CAPACITY: Final[str] = "Starship Total Annual Capacity (kg-to-LEO) — from Launch Capacity"
STARSHIP_V3_BB_LAUNCHES_INTERNAL: Final[str] = "Starship V3 BB launches (internal)"
STARSHIP_V3_DTC_LAUNCHES_INTERNAL: Final[str] = "Starship V3 DTC launches (internal)"
STARSHIP_AT_COST_RATE_MM_LAUNCH: Final[str] = "Starship at-cost rate ($mm/launch)"
STARSHIP_AT_COST_RATE_MM_LAUNCH_READ_FROM_LAUNCH_CAPACITY: Final[str] = "Starship at-cost rate ($mm/launch) — read from Launch Capacity"
STARSHIP_BOOSTER_SHARE_OF_MANUFACTURING_COST_OF_STACK_MFG: Final[str] = "Starship booster share of manufacturing cost (% of stack mfg)"
STARSHIP_CAPACITY_AVAILABLE_FOR_CUSTOMER_LAUNCHES_KG: Final[str] = "Starship capacity available for customer launches (kg)"
STARSHIP_COST_WL_ANCHOR_CUM_UNITS_CUM_STACKS_AT_END_2024_BASELINE: Final[str] = "Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)"
STARSHIP_CUSTOMER_LAUNCH_INSURANCE_OTHER_COGS_MM_LAUNCH: Final[str] = "Starship customer launch insurance + other COGS ($mm/launch)"
STARSHIP_CUSTOMER_LAUNCH_MARGIN_MULTIPLIER_YEAR_ROW: Final[str] = "Starship customer launch margin multiplier (year-row)"
STARSHIP_CUSTOMER_LAUNCH_MARGIN_2027_ANCHOR_MULTIPLIER_ON_AT_COST_RATE: Final[str] = "Starship customer launch margin — 2027 anchor (multiplier on at-cost rate)"
STARSHIP_CUSTOMER_LAUNCH_MARGIN_2050_TERMINAL_MULTIPLIER_ON_AT_COST_RATE_FLOOR: Final[str] = "Starship customer launch margin — 2050 terminal (multiplier on at-cost rate, floor)"
STARSHIP_CUSTOMER_LAUNCH_MARGIN_CAGR_CHANGE_YR_FROM_2027_ANCHOR: Final[str] = "Starship customer launch margin — CAGR (% change/yr from 2027 anchor)"
STARSHIP_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH: Final[str] = "Starship customer launch price ($mm/launch)"
STARSHIP_CUSTOMER_LAUNCH_PRICE_MM_LAUNCH_YEAR_ROW: Final[str] = "Starship customer launch price ($mm/launch) — year-row"
STARSHIP_CUSTOMER_LAUNCHES_PER_YEAR: Final[str] = "Starship customer launches per year"
STARSHIP_CUSTOMER_REVENUE_MM: Final[str] = "Starship customer revenue ($mm)"
STARSHIP_INTERNAL_KG_DEMAND_POST_STARLINK_ODC_AI_STACK: Final[str] = "Starship internal kg demand (post-Starlink + ODC + AI Stack)"
STARSHIP_INTERNAL_LAUNCHES_V3_BB_V3_DTC_ODC_AI_STACK: Final[str] = "Starship internal launches (V3 BB + V3 DTC + ODC + AI Stack)"
STARSHIP_LIFETIME_REUSES_PER_BOOSTER_YEAR_ROW_FROM_LAUNCH_CAPACITY_R21: Final[str] = "Starship lifetime reuses per booster — year-row from Launch Capacity R21"
STARSHIP_MANUFACTURING_WL_LEARNING_RATE_REDUCTION_PER_DOUBLING_CUM_STACKS: Final[str] = "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)"
STARSHIP_MANUFACTURING_COST_MM_STACK_THIS_YEAR: Final[str] = "Starship manufacturing cost ($mm/stack, this year)"
STARSHIP_MANUFACTURING_COST_ANCHOR_MM_STACK_2024_BASELINE: Final[str] = "Starship manufacturing cost anchor ($mm/stack, 2024 baseline)"
STARSHIP_OPS_FUEL_REFURB_WL_LEARNING_RATE_REDUCTION_PER_DOUBLING_CUM_STACKS: Final[str] = "Starship ops + fuel + refurb WL learning rate (% reduction per doubling cum stacks)"
STARSHIP_OPS_FUEL_REFURB_COST_ANCHOR_MM_LAUNCH_2024_BASELINE: Final[str] = "Starship ops + fuel + refurb cost anchor ($mm/launch, 2024 baseline)"
STARSHIP_OPS_FUEL_REFURB_COST_PER_LAUNCH_MM_READ_FROM_LAUNCH_CAPACITY: Final[str] = "Starship ops + fuel + refurb cost per launch ($mm) — read from Launch Capacity"
STARSHIP_OPS_FUEL_REFURB_COST_PER_LAUNCH_MM_THIS_YEAR: Final[str] = "Starship ops + fuel + refurb cost per launch ($mm, this year)"
STARSHIP_PAYLOAD_2025_BASELINE_KG_TO_LEO_FULLY_REUSABLE_MODE: Final[str] = "Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)"
STARSHIP_PAYLOAD_2030_ANCHOR_KG_TO_LEO_FULLY_REUSABLE_MODE: Final[str] = "Starship payload — 2030 anchor (kg-to-LEO, fully reusable mode)"
STARSHIP_PAYLOAD_BOOSTER_ONLY_MODE_DELTA_KG_ADDITIVE_TO_FULLY_REUSABLE_PAYLOAD: Final[str] = "Starship payload — booster-only mode delta (kg, additive to fully-reusable payload)"
STARSHIP_PAYLOAD_MAX_CAP_KG_TO_LEO: Final[str] = "Starship payload — max cap (kg-to-LEO)"
STARSHIP_PER_LAUNCH_BLENDED_IRR_EXTERNAL_CUSTOMER_ECONOMICS: Final[str] = "Starship per-launch Blended IRR (external customer economics)"
STARSHIP_PER_LAUNCH_ANNUAL_MARGIN_MM_YR_CADENCE_PER_LAUNCH_MARGIN: Final[str] = "Starship per-launch annual margin ($mm/yr — cadence × per-launch margin)"
STARSHIP_PER_LAUNCH_COST_SLUG_MM_YEAR_ROW_OF_MANUFACTURING_COST_FROM_LAUNCH_CAPACITY_R37: Final[str] = "Starship per-launch cost slug ($mm — year-row of manufacturing cost from Launch Capacity R37)"
STARSHIP_VARIABLE_COST_MM: Final[str] = "Starship variable cost ($mm)"
STARSHIP_VEHICLE_COST_AMORTIZED_MM_SHIP: Final[str] = "Starship vehicle cost amortized ($mm/ship)"
STARTING_BOY_2025_SUBSCRIBERS_MILLIONS: Final[str] = "Starting BoY 2025 subscribers (millions)"
STARTING_CASH_POSITION_EOY_2024_MM: Final[str] = "Starting cash position EoY 2024 ($mm)"
STEADY_STATE_UTILIZATION: Final[str] = "Steady-state utilization"
STEADY_STATE_UTILIZATION_FOR_MODEL_A_UTIL_ADJUSTMENT_RATIO: Final[str] = "Steady-state utilization (for Model A util-adjustment ratio)"
STRUCTURE_COST_PER_SAT_PRE_WL: Final[str] = "Structure cost per sat ($, pre-WL)"
STRUCTURE_FLAT_COST: Final[str] = "Structure flat cost ($)"
SUBSIDY_MIX_OF_NET_ADDS_SUBSIDIZED: Final[str] = "Subsidy mix (% of net adds subsidized)"
SUPER_HEAVY_MANUFACTURING_COST_MM_UNIT: Final[str] = "Super Heavy manufacturing cost ($mm/unit)"
SUPER_HEAVY_MANUFACTURING_COST_MM_UNIT_BASE_YEAR: Final[str] = "Super Heavy manufacturing cost ($mm/unit, base year)"
TAM_INFLATION_RATE_ANNUAL: Final[str] = "TAM inflation rate (annual)"
TAX_RATE_CORPORATE_US_FEDERAL_STATE_BLENDED: Final[str] = "Tax rate (corporate, US federal + state blended)"
TAXES_MM: Final[str] = "Taxes ($mm)"
TAXES_CLAIM_MM: Final[str] = "Taxes claim ($mm)"
TERMINAL_COGS_MM: Final[str] = "Terminal COGS ($mm)"
TERMINAL_COGS_PER_UNIT: Final[str] = "Terminal COGS per unit ($)"
TERMINAL_FCF_AVERAGING_WINDOW_YEARS_PRE_2050: Final[str] = "Terminal FCF averaging window (years pre-2050)"
TERMINAL_GROWTH_RATE_G_GROUP_MOST_MODULES: Final[str] = "Terminal growth rate g (group + most modules)"
TERMINAL_HARDWARE_REVENUE_MM: Final[str] = "Terminal hardware revenue ($mm)"
TERMINAL_RETAIL_PRICE_NON_SUBSIDIZED: Final[str] = "Terminal retail price ($, non-subsidized)"
TERMINAL_RETAIL_PRICE_SUBSIDIZED: Final[str] = "Terminal retail price ($, subsidized)"
TERRESTRIAL_PRICE_DEFLATION_YR: Final[str] = "Terrestrial price deflation %/yr"
TERRESTRIAL_PRICE_DEFLATION_YR_MODEL_A_BASELINE_YEAR_ROW_DRIVER: Final[str] = "Terrestrial price deflation %/yr (Model A baseline year-row driver)"
THERMAL_SYSTEM_COST_PER_SAT_PRE_WL: Final[str] = "Thermal system cost per sat ($, pre-WL)"
THERMAL_SYSTEM_UNIT_COST_KG: Final[str] = "Thermal system unit cost ($/kg)"
TOTAL_ANNUAL_CAPACITY_KG_TO_LEO: Final[str] = "Total Annual Capacity (kg-to-LEO)"
TOTAL_COGS_MM: Final[str] = "Total COGS ($mm)"
TOTAL_CAPITAL_AVAILABLE_MM: Final[str] = "Total Capital Available ($mm)"
TOTAL_CORPORATE_CAPEX_MM: Final[str] = "Total Corporate CapEx ($mm)"
TOTAL_CORPORATE_D_A_MM: Final[str] = "Total Corporate D&A ($mm)"
TOTAL_D_A_ADD_BACK_MM: Final[str] = "Total D&A add-back ($mm)"
TOTAL_GROUP_CAPEX_MM: Final[str] = "Total Group CapEx ($mm)"
TOTAL_LUNAR_MARS_ACCUMULATED_BV_MM: Final[str] = "Total Lunar + Mars accumulated BV ($mm)"
TOTAL_MARS_MOON_STRATEGIC_CARVE_OUT_MM_YR: Final[str] = "Total Mars/Moon strategic carve-out ($mm/yr)"
TOTAL_MODULE_CAPEX_MM: Final[str] = "Total Module CapEx ($mm)"
TOTAL_ODC_GBPS_DEMAND: Final[str] = "Total ODC Gbps demand"
TOTAL_OPEX_MM: Final[str] = "Total OpEx ($mm)"
TOTAL_R_D_MM: Final[str] = "Total R&D ($mm)"
TOTAL_REVENUE_MM: Final[str] = "Total Revenue ($mm)"
TOTAL_SG_A_MM: Final[str] = "Total SG&A ($mm)"
TOTAL_STARSHIP_CAPACITY_KG_TO_LEO: Final[str] = "Total Starship capacity (kg-to-LEO)"
TOTAL_STARSHIP_LAUNCHES_PER_YEAR: Final[str] = "Total Starship launches per year"
TOTAL_ACTIVE_BB_GBPS: Final[str] = "Total active BB Gbps"
TOTAL_ACTIVE_BB_GBPS_STARLINK_STARSHIELD_LEGACY: Final[str] = "Total active BB Gbps (Starlink + Starshield + legacy)"
TOTAL_ACTIVE_DTC_GBPS: Final[str] = "Total active DTC Gbps"
TOTAL_CUSTOMER_LAUNCH_MARKET_LAUNCHES_YR: Final[str] = "Total customer launch market (launches/yr)"
TOTAL_CUSTOMER_LAUNCH_MARKET_LAUNCHES_YR_2025_ANCHOR: Final[str] = "Total customer launch market (launches/yr) — 2025 anchor"
TOTAL_CUSTOMER_LAUNCH_MARKET_CAGR_GROWTH_YR: Final[str] = "Total customer launch market CAGR (% growth/yr)"
TOTAL_FULLY_ALLOCATED_ODC_COST_MM_YR: Final[str] = "Total fully-allocated ODC cost ($mm/yr)"
TOTAL_LAUNCH_CAPEX_PER_YEAR_MM_VARIABLE_AMORTIZED_D_A: Final[str] = "Total launch CapEx per year ($mm) — variable + amortized D&A"
TOTAL_LAUNCHES_PER_YEAR_ALL_VEHICLES: Final[str] = "Total launches per year (all vehicles)"
TOTAL_SAT_DRY_MASS_KG: Final[str] = "Total sat dry mass (kg)"
TOTAL_UPMASS_PER_YEAR_KG: Final[str] = "Total upmass per year (kg)"
UTILIZATION_FLEET_RAMP_YEAR_ROW: Final[str] = "Utilization % (fleet ramp) — year-row"
V2_BB_GBPS_PER_SAT: Final[str] = "V2 BB Gbps per sat"
V2_BB_FACILITY_CAPEX_MM: Final[str] = "V2 BB facility CapEx ($mm)"
V2_BB_FACILITY_CAPEX_PER_SAT_MM_SAT: Final[str] = "V2 BB facility CapEx per sat ($mm/sat)"
V2_BB_HISTORICAL_RETIREMENT: Final[str] = "V2 BB historical retirement"
V2_BB_LAUNCH_COHORT_RETIREMENT: Final[str] = "V2 BB launch-cohort retirement"
V2_BB_LAUNCHES_PER_YEAR: Final[str] = "V2 BB launches per year"
V2_BB_SAT_CAPEX_MM: Final[str] = "V2 BB sat CapEx ($mm)"
V2_BB_SAT_UNIT_COST_MM_SAT: Final[str] = "V2 BB sat unit cost ($mm/sat)"
V2_DTC_GBPS_PER_SAT: Final[str] = "V2 DTC Gbps per sat"
V2_DTC_FACILITY_CAPEX_MM: Final[str] = "V2 DTC facility CapEx ($mm)"
V2_DTC_FACILITY_CAPEX_PER_SAT_MM_SAT: Final[str] = "V2 DTC facility CapEx per sat ($mm/sat)"
V2_DTC_HISTORICAL_RETIREMENT: Final[str] = "V2 DTC historical retirement"
V2_DTC_LAUNCH_COHORT_RETIREMENT: Final[str] = "V2 DTC launch-cohort retirement"
V2_DTC_LAUNCHES_PER_YEAR: Final[str] = "V2 DTC launches per year"
V2_DTC_PERMANENT_CAP_FLAG_RETIRED_2026_05_26_REPLACED_BY_V2_PHASE_OUT_YEAR_R350_PER_20_6_ARCHITECTURE_AMENDMENTS: Final[str] = "V2 DTC permanent cap flag — RETIRED 2026-05-26 (replaced by V2 phase-out year R350 per §20.6 Architecture amendments)"
V2_DTC_SAT_CAPEX_MM: Final[str] = "V2 DTC sat CapEx ($mm)"
V2_DTC_SAT_UNIT_COST_MM_SAT: Final[str] = "V2 DTC sat unit cost ($mm/sat)"
V2_MINI_BB_ACTIVE_SATS_END_2025: Final[str] = "V2 Mini BB Active Sats — end-2025"
V2_MINI_BB_BANDWIDTH_END_2025_GBPS: Final[str] = "V2 Mini BB Bandwidth — end-2025 (Gbps)"
V2_MINI_BB_DEORBIT_LAG_YEARS: Final[str] = "V2 Mini BB Deorbit Lag (years)"
V2_MINI_BB_SATS_LAUNCHED_2025: Final[str] = "V2 Mini BB Sats Launched 2025"
V2_MINI_BB_HISTORICAL_BASELINE_SOY_2025: Final[str] = "V2 Mini BB historical baseline (SoY 2025)"
V2_MINI_BANDWIDTH_PER_SAT_BB_GBPS: Final[str] = "V2 Mini Bandwidth per Sat — BB (Gbps)"
V2_MINI_BANDWIDTH_PER_SAT_DTC_GBPS: Final[str] = "V2 Mini Bandwidth per Sat — DTC (Gbps)"
V2_MINI_DTC_ACTIVE_SATS_END_2025: Final[str] = "V2 Mini DTC Active Sats — end-2025"
V2_MINI_DTC_BANDWIDTH_END_2025_GBPS: Final[str] = "V2 Mini DTC Bandwidth — end-2025 (Gbps)"
V2_MINI_DTC_DEORBIT_LAG_YEARS: Final[str] = "V2 Mini DTC Deorbit Lag (years)"
V2_MINI_DTC_SATS_LAUNCHED_2025: Final[str] = "V2 Mini DTC Sats Launched 2025"
V2_MINI_DTC_HISTORICAL_BASELINE_SOY_2025: Final[str] = "V2 Mini DTC historical baseline (SoY 2025)"
V2_MINI_MASS_KG: Final[str] = "V2 Mini Mass (kg)"
V2_MINI_COST_FLOOR_KG: Final[str] = "V2 Mini cost floor ($/kg)"
V2_MINI_COST_PER_KG_BASE_YEAR_KG: Final[str] = "V2 Mini cost per kg — base year ($/kg)"
V2_MINI_COST_PER_KG_LEARNING_RATE: Final[str] = "V2 Mini cost per kg — learning rate"
V2_PHASE_OUT_YEAR_NO_V2_BB_V2_DTC_LAUNCHES_FROM_THIS_YEAR: Final[str] = "V2 phase-out year (no V2 BB / V2 DTC launches from this year)"
V2_V3_RATCHET_FLAG_RETIRED_2026_05_26_REPLACED_BY_V2_PHASE_OUT_R350_V3_TRIGGER_LC_R56_GATES_PER_20_6_ARCHITECTURE_AMENDMENTS: Final[str] = "V2/V3 ratchet flag — RETIRED 2026-05-26 (replaced by V2 phase-out R350 + V3 trigger LC R56 gates per §20.6 Architecture amendments)"
V3_BB_BANDWIDTH_PER_SAT_BASE_YEAR_GBPS: Final[str] = "V3 BB Bandwidth per Sat — base year (Gbps)"
V3_BB_DEORBIT_LAG_YEARS: Final[str] = "V3 BB Deorbit Lag (years)"
V3_BB_GBPS_PER_SAT: Final[str] = "V3 BB Gbps per sat"
V3_BB_SATS_LAUNCHED_2025: Final[str] = "V3 BB Sats Launched 2025"
V3_BB_STARSHIP_KG_DEMAND: Final[str] = "V3 BB Starship kg demand"
V3_BB_WRIGHT_S_LAW_ANCHOR_CUM_SATS: Final[str] = "V3 BB Wright’s Law anchor — cum sats"
V3_BB_BANDWIDTH_PER_SAT_WRIGHT_S_LAW_LEARNING_RATE_PER_DOUBLING: Final[str] = "V3 BB bandwidth-per-sat Wright’s Law learning rate (per doubling)"
V3_BB_FACILITY_CAPEX_MM: Final[str] = "V3 BB facility CapEx ($mm)"
V3_BB_FACILITY_CAPEX_PER_SAT_MM_SAT: Final[str] = "V3 BB facility CapEx per sat ($mm/sat)"
V3_BB_FIRST_LAUNCH_YEAR: Final[str] = "V3 BB first launch year"
V3_BB_LAUNCH_COHORT_RETIREMENT: Final[str] = "V3 BB launch-cohort retirement"
V3_BB_LAUNCHES_PER_YEAR: Final[str] = "V3 BB launches per year"
V3_BB_LAUNCHES_PER_YEAR_STUB_TRAJECTORY: Final[str] = "V3 BB launches per year stub trajectory"
V3_BB_SAT_CAPEX_MM: Final[str] = "V3 BB sat CapEx ($mm)"
V3_BB_SAT_UNIT_COST_MM_SAT: Final[str] = "V3 BB sat unit cost ($mm/sat)"
V3_DTC_BANDWIDTH_PER_SAT_GBPS: Final[str] = "V3 DTC Bandwidth per Sat (Gbps)"
V3_DTC_DEORBIT_LAG_YEARS: Final[str] = "V3 DTC Deorbit Lag (years)"
V3_DTC_GBPS_PER_SAT: Final[str] = "V3 DTC Gbps per sat"
V3_DTC_SATS_LAUNCHED_2025: Final[str] = "V3 DTC Sats Launched 2025"
V3_DTC_STARSHIP_KG_DEMAND: Final[str] = "V3 DTC Starship kg demand"
V3_DTC_FACILITY_CAPEX_MM: Final[str] = "V3 DTC facility CapEx ($mm)"
V3_DTC_FACILITY_CAPEX_PER_SAT_MM_SAT: Final[str] = "V3 DTC facility CapEx per sat ($mm/sat)"
V3_DTC_FIRST_LAUNCH_YEAR: Final[str] = "V3 DTC first launch year"
V3_DTC_LAUNCH_COHORT_RETIREMENT: Final[str] = "V3 DTC launch-cohort retirement"
V3_DTC_LAUNCHES_PER_YEAR: Final[str] = "V3 DTC launches per year"
V3_DTC_LAUNCHES_PER_YEAR_STUB_TRAJECTORY: Final[str] = "V3 DTC launches per year stub trajectory"
V3_DTC_SAT_CAPEX_MM: Final[str] = "V3 DTC sat CapEx ($mm)"
V3_DTC_SAT_UNIT_COST_MM_SAT: Final[str] = "V3 DTC sat unit cost ($mm/sat)"
V3_MASS_KG: Final[str] = "V3 Mass (kg)"
V3_STARLINK_LAUNCH_TRIGGER_YEAR: Final[str] = "V3 Starlink launch trigger year"
V3_BANDWIDTH_CAP_GBPS: Final[str] = "V3 bandwidth cap (Gbps)"
V3_BANDWIDTH_PER_SAT_LEARNING_RATE: Final[str] = "V3 bandwidth per sat — learning rate"
VALUATION_DCF_OFF_GROUP_FCF_SUM_OF_PARTS_PER_MODULE_MULTIPLES_CROSS_CHECK_COMPARABLES_SENSITIVITY_SPRINT_11_FILLS: Final[str] = "VALUATION -- DCF off Group FCF + Sum-of-parts per module + Multiples cross-check + Comparables + Sensitivity. Sprint 11 fills."
VARIANT_MIX_FULLY_REUSABLE: Final[str] = "Variant mix (% fully reusable)"
VEHICLE_BUILD_CLAIM_MM: Final[str] = "Vehicle build claim ($mm)"
VEHICLE_BUILD_CLAIM_TOGGLE_0_LEGACY_MODE_1_FORWARD_DEMAND_SIZED_NON_MODULE_CLAIM: Final[str] = "Vehicle build claim toggle (0=legacy mode, 1=forward-demand-sized non-module claim)"
VEHICLE_BUILD_LEAD_TIME_YEARS: Final[str] = "Vehicle build lead time (years)"
VEHICLE_MASKED_DEMAND_LARGE_DEFAULT_SATS_EFFECTIVELY_UNCAPPED: Final[str] = "Vehicle masked-demand large default (sats; effectively uncapped)"
WL_LEARNING_RATE_TURNAROUND_VS_CUM_UPMASS_DOUBLING: Final[str] = "WL learning rate — turnaround vs cum upmass doubling"
WANTED_SATS_DEPLOYED_UNCAPPED_CASH_DERIVED: Final[str] = "Wanted sats deployed (uncapped, cash-derived)"
WORKLOAD_MIX_INFERENCE: Final[str] = "Workload mix — % inference"
WRIGHT_S_LAW_MULTIPLIER_ON_SUBSYSTEMS_YEAR_ROW: Final[str] = "Wright's Law multiplier on subsystems (year-row)"
YEAR_N_NON_MODULE_CLAIMS_MM: Final[str] = "Year-N non-module claims ($mm)"
MODULE_COGS_GROSS_PRE_ELIM_MM: Final[str] = "Σ Module COGS (gross, pre-elim) ($mm)"
MODULE_REVENUE_GROSS_PRE_ELIM_MM: Final[str] = "Σ Module revenue (gross, pre-elim) ($mm)"
CASH_WEIGHTS_DENOMINATOR_FOR_SHARES: Final[str] = "Σ cash weights (denominator for shares)"
KG_WEIGHTS_DENOMINATOR_FOR_SHARES: Final[str] = "Σ kg weights (denominator for shares)"
AI_STACK_IN_QUEUE_MODULE: Final[str] = "▸ AI Stack (in-queue module)"
AI_STACK_KG_SUB_BLOCK_TERRESTRIAL_KG_DEMAND_STRUCTURALLY_0: Final[str] = "▸ AI Stack kg sub-block (terrestrial — kg demand structurally 0)"
AI_STACK_OPERATING_PARAMETERS: Final[str] = "▸ AI Stack operating parameters"
ANNUAL_TAM_GROWTH_INFLATION_REAL_GNI_COMPONENTS: Final[str] = "▸ Annual TAM growth — inflation + real GNI components"
AT_COST_TRANSFER_RATES_GBPS_YR_FOR_SPRINT_5_ODC_STARLINK_INTERNAL_BANDWIDTH_REVENUE: Final[str] = "▸ At-cost transfer rates ($/Gbps/yr; for Sprint 5 ODC + Starlink internal bandwidth revenue)"
AVAILABLE_BANDWIDTH_FOR_EXTERNAL_STARLINK_REVENUE: Final[str] = "▸ Available bandwidth for external Starlink revenue"
BB_DTC_MARKET_MIX_SPEC_09: Final[str] = "▸ BB/DTC market mix (Spec 09)"
BANDWIDTH_FLOW_TO_ODC_SPEC_04_PLACEHOLDERS: Final[str] = "▸ Bandwidth flow to ODC (Spec 04 PLACEHOLDERS)"
CAPEX_FCF: Final[str] = "▸ CAPEX + FCF"
COGS_CONSTELLATION_D_A_GROUND_OPS_SPECTRUM_AMORT_BB_ONLY_TERMINAL_COGS_INSURANCE_OTHER: Final[str] = "▸ COGS (Constellation D&A, Ground ops, Spectrum amort BB-only, Terminal COGS, Insurance, Other)"
COST_OF_GOODS_SOLD_MM: Final[str] = "▸ COST OF GOODS SOLD ($mm)"
CASH_POOL_BOUNDARY_INPUTS: Final[str] = "▸ Cash pool boundary inputs"
CHIP_ROADMAP_YEAR_ROWS_H100_AI5_DOJO_3: Final[str] = "▸ Chip roadmap (year-rows, H100 → AI5 → Dojo-3)"
CHIP_ROADMAP_READS_YEAR_ROWS: Final[str] = "▸ Chip roadmap reads (year-rows)"
COMPARABLES_ANCHORS_B: Final[str] = "▸ Comparables anchors ($B)"
CONSTELLATION_OPENING_BALANCES_MACH33_HISTORICAL_ANCHORS_HARD: Final[str] = "▸ Constellation opening balances (Mach33 historical anchors — hard)"
CORPORATE_FACILITIES_CAPEX_MM_YR: Final[str] = "▸ Corporate facilities CapEx ($mm/yr)"
CORPORATE_HISTORICAL_CAPITAL_BASE: Final[str] = "▸ Corporate historical capital base"
CORPORATE_USEFUL_LIVES: Final[str] = "▸ Corporate useful lives"
CURSOR_ORCHESTRATION: Final[str] = "▸ Cursor (orchestration)"
CURVE_EVALUATORS_YEAR_ROW_READ_BY_STARLINK_MODULE: Final[str] = "▸ Curve evaluators (year-row, read by Starlink module)"
CUSTOMER_LAUNCH_IN_QUEUE_MODULE: Final[str] = "▸ Customer Launch (in-queue module)"
CUSTOMER_LAUNCH_KG_SUB_BLOCK_EXTERNAL_STARSHIP_DEMAND: Final[str] = "▸ Customer Launch kg sub-block (external Starship demand)"
DEMAND_MECHANIC_TOTAL_MARKET_F9_VS_STARSHIP_SPLIT_VIA_IRR_CAPACITY: Final[str] = "▸ Demand mechanic (total market + F9 vs Starship split via IRR + capacity)"
DEORBIT_PARAMETERS: Final[str] = "▸ Deorbit parameters"
DEPRECIATION_PARAMETERS: Final[str] = "▸ Depreciation parameters"
DUAL_REVENUE_MODEL_SPRINT_3_5: Final[str] = "▸ Dual revenue model (Sprint 3.5)"
ECHOSTAR_SPECTRUM_SPEC_03_5: Final[str] = "▸ EchoStar spectrum (Spec 03 §5)"
EXTERNAL_REVENUE_BANDWIDTH_DRIVEN_AVAILABLE_GBPS_GBPS_SUBS_DERIVED: Final[str] = "▸ External revenue (bandwidth-driven: Available Gbps × $/Gbps; subs derived)"
F9_CAPACITY_AT_COST_TRANSFER_RATE: Final[str] = "▸ F9 capacity + at-cost transfer rate"
F9_CUSTOMER_LAUNCHES_ECONOMICS: Final[str] = "▸ F9 customer launches — economics"
F9_SUPPLY_MECHANIC_PRE_V3_TRIGGER_ANCHORS_POST_TRIGGER_DECAY: Final[str] = "▸ F9 supply mechanic (pre-V3-trigger anchors + post-trigger decay)"
FALCON_9_PHYSICAL_COST_PARAMETERS: Final[str] = "▸ Falcon 9 physical + cost parameters"
GROK_CONSUMER_X_PREMIUM_GROK_PREMIUM: Final[str] = "▸ Grok consumer (X Premium / Grok Premium)"
GROK_ENTERPRISE_API: Final[str] = "▸ Grok enterprise (API)"
IRR_ENGINE_SIGMOID_BLEND_PARAMETERS: Final[str] = "▸ IRR engine + sigmoid blend parameters"
INTERNAL_BANDWIDTH_REVENUE_STARLINK_ODC_4_STEP_PATTERN_PER_ARCHITECTURE_7_2: Final[str] = "▸ Internal bandwidth revenue (Starlink → ODC, 4-step pattern per Architecture §7.2)"
INTERNAL_CLAIM_BY_ODC_SPRINT_5_PLACEHOLDERS: Final[str] = "▸ Internal claim by ODC (Sprint 5 placeholders)"
INTERNAL_TRANSFER_REVENUE_LAUNCH_SERVICES_TO_SPRINT_4_5_6_CONSUMERS: Final[str] = "▸ Internal transfer revenue (launch services to Sprint 4/5/6 consumers)"
LABOUR_UNIT_SHARED_PARAMETERS_OPTIMUS_CLASS_PROXY: Final[str] = "▸ Labour unit shared parameters (Optimus-class proxy)"
LUNAR_MARS_SHARE_OF_CARVE_OUT_CASH_DERIVED_DEPLOYMENT: Final[str] = "▸ Lunar / Mars share of carve-out cash (derived deployment)"
LUNAR_SPECIFIC: Final[str] = "▸ Lunar-specific"
MARS_SPECIFIC: Final[str] = "▸ Mars-specific"
MEMO_2025_CALIBRATION_ANCHORS_DIAGNOSTIC_CHECKS: Final[str] = "▸ Memo: 2025 calibration anchors + diagnostic checks"
MODULE_P_L_VENDING_MACHINE_REVENUE_COGS_EBITDA_CAPEX_FCF: Final[str] = "▸ Module P&L (vending-machine: Revenue → COGS → EBITDA → CapEx → FCF)"
MODULE_P_L_VENDING_MACHINE_REVENUE_COGS_MODULE_EBITDA_CAPEX_FCF: Final[str] = "▸ Module P&L (vending-machine: Revenue → COGS → Module EBITDA → CapEx → FCF)"
MODULE_WIDE_PARAMETERS: Final[str] = "▸ Module-wide parameters"
MOON_MARS_STRATEGIC_CARVE_OUT_VLAD_CONFIRMED_MC_VARIABLE: Final[str] = "▸ Moon/Mars strategic carve-out (Vlad-confirmed MC-variable)"
ODC_IN_QUEUE_MODULE: Final[str] = "▸ ODC (in-queue module)"
ODC_INTERNAL_VS_EXTERNAL_COMPUTE_SPLIT_NEW_PER_VLAD_S_FRAMING: Final[str] = "▸ ODC internal vs external compute split (NEW per Vlad's framing)"
ODC_KG_SUB_BLOCK: Final[str] = "▸ ODC kg sub-block"
PER_LAUNCH_MARGINAL_IRR_ENGINES_F9_STARSHIP_EXTERNAL_CUSTOMER_ONLY: Final[str] = "▸ Per-launch marginal IRR engines (F9 + Starship, external customer only)"
PER_VEHICLE_CAPEX_SAT_UNIT_COST_VIA_WRIGHT_S_LAW_FACILITY_CAPEX_WITH_1_YR_LAG: Final[str] = "▸ Per-vehicle CapEx (sat unit cost via Wright's Law + facility CapEx with 1-yr lag)"
PHYSICAL_COST_PARAMETERS_FROM_ASSUMPTIONS_3: Final[str] = "▸ Physical + cost parameters (from Assumptions §3)"
POOL_COST_BASIS_MM_YR_READS_STARLINK_TAB_COGS_COMPONENTS: Final[str] = "▸ Pool cost basis ($mm/yr; reads Starlink tab COGS components)"
R_D_BY_MODULE_START_END_CAGR_TAPER_PER_SPEC_03_2_2: Final[str] = "▸ R&D by module (start% / end% / CAGR taper per Spec 03 §2.2)"
R_D_MOON_MARS_PROFILE_YEAR_ROW_PRE_REVENUE: Final[str] = "▸ R&D — Moon/Mars ($-profile year-row, pre-revenue)"
REVENUE_PARAMETERS: Final[str] = "▸ Revenue parameters"
SG_A_BY_FUNCTION: Final[str] = "▸ SG&A by function"
SATELLITE_SUBSYSTEM_ANCHORS_V2_COMPUTE_CONFIG: Final[str] = "▸ Satellite & subsystem anchors (V2 Compute config)"
SATELLITE_PHYSICAL: Final[str] = "▸ Satellite physical"
SOTP_MULTIPLES_EV_REVENUE_AT_2050: Final[str] = "▸ SoTP multiples (EV/Revenue at 2050)"
STARLINK_V2_BB: Final[str] = "▸ Starlink V2 BB"
STARLINK_V2_DTC: Final[str] = "▸ Starlink V2 DTC"
STARLINK_V3_BB: Final[str] = "▸ Starlink V3 BB"
STARLINK_V3_BB_KG_SUB_BLOCK: Final[str] = "▸ Starlink V3 BB kg sub-block"
STARLINK_V3_DTC: Final[str] = "▸ Starlink V3 DTC"
STARLINK_V3_DTC_KG_SUB_BLOCK: Final[str] = "▸ Starlink V3 DTC kg sub-block"
STARLINK_LARGE_DEFAULT_CASH_KG_ASKS_SPEC_09: Final[str] = "▸ Starlink large-default cash + kg asks (Spec 09)"
STARSHIELD_VLAD_CORRECTED_FROM_Q4_25: Final[str] = "▸ Starshield (Vlad-corrected from Q4'25)"
STARSHIELD_REVENUE_Q4_25_MECHANIC_RESERVED_GBPS_GBPS_WITH_DECAY: Final[str] = "▸ Starshield revenue (Q4'25 mechanic — reserved Gbps × $/Gbps with decay)"
STARSHIP_AT_COST_TRANSFER_RATE_ARCHITECTURE_7_1: Final[str] = "▸ Starship at-cost transfer rate (Architecture §7.1)"
STARSHIP_CADENCE_WRIGHT_S_LAW_ON_CUM_UPMASS: Final[str] = "▸ Starship cadence (Wright's Law on cum upmass)"
STARSHIP_CUSTOMER_LAUNCHES_ECONOMICS: Final[str] = "▸ Starship customer launches — economics"
STARSHIP_TIME_VARYING_INPUTS_YEAR_ROWS: Final[str] = "▸ Starship time-varying inputs (year-rows)"
STARSHIP_VEHICLE_PHYSICAL_COST_PARAMETERS: Final[str] = "▸ Starship vehicle physical + cost parameters"
SUBSCRIBERS_ARPU_TERMINALS: Final[str] = "▸ Subscribers + ARPU + Terminals"
SUBSYSTEM_UNIT_COSTS_PER_SAT_FLAT_UNLESS_NOTED: Final[str] = "▸ Subsystem unit costs (per-sat, flat unless noted)"
SUBSYSTEM_UNIT_COSTS_WRIGHT_S_LAW: Final[str] = "▸ Subsystem unit costs + Wright's Law"
TERMINAL_VALUE_PARAMETERS: Final[str] = "▸ Terminal value parameters"
TOTAL_ACTIVE_GBPS_BB_DTC_FROM_STARLINK_TAB_ACTIVE_SAT_FLEET: Final[str] = "▸ Total active Gbps (BB + DTC, from Starlink tab active sat fleet)"
VARIANT_MIX_BOOSTER_LIFETIME_REUSES_YEAR_ROWS_FROM_ASSUMPTIONS_3: Final[str] = "▸ Variant mix + booster lifetime reuses (year-rows from Assumptions §3)"
VEHICLE_BUILD_CLAIM_SPEC_09_ARCHITECTURE: Final[str] = "▸ Vehicle build claim (Spec 09 architecture)"
VEHICLE_DEPLOYMENT_V2_BB_V2_DTC_V3_BB_V3_DTC_LAUNCHES_FLEET_RATCHET_RETIREMENT: Final[str] = "▸ Vehicle deployment (V2 BB, V2 DTC, V3 BB, V3 DTC — launches, fleet, ratchet, retirement)"
WACC_RISK_PREMIA: Final[str] = "▸ WACC + risk premia"
WACC_COMPONENT_MEMOS_NOT_USED_IN_FORMULAS: Final[str] = "▸ WACC component memos (not used in formulas)"
WRIGHT_S_LAW_LEARNING_RATES: Final[str] = "▸ Wright's Law learning rates"
WRIGHT_S_LAW_PARAMETERS: Final[str] = "▸ Wright's Law parameters"
YEAR_ROW_COST_CURVES: Final[str] = "▸ Year-row cost curves"

# fmt: on

CANONICAL_LABELS: Final[frozenset[str]] = frozenset(
    {
        "ADCS + avionics cost per sat ($, pre-WL)",
        "ADCS + avionics flat cost ($)",
        "AI Stack Blended IRR",
        "AI Stack Forward IRR (Y+2)",
        "AI Stack Module CapEx ($mm)",
        "AI Stack R&D $-profile ($mm, pre-revenue floor)",
        "AI Stack R&D $-profile ($mm/yr) — year-row",
        "AI Stack R&D ($mm) — MAX($-profile, % × rev)",
        "AI Stack R&D base — AI Stack rev ($mm)",
        "AI Stack R&D — % of AI Stack rev (bounded-CAGR)",
        "AI Stack R&D — CAGR (taper)",
        "AI Stack R&D — end-state % (floor)",
        "AI Stack R&D — start % of AI Stack rev",
        "AI Stack Spot IRR",
        "AI Stack cash allocation",
        "AI Stack cash demand ($mm)",
        "AI Stack insurance % of revenue",
        "AI Stack kg allocation",
        "AI Stack kg demand (kg-to-LEO)",
        "AI Stack kg proposed allocation",
        "AI Stack kg weight",
        "AI Stack other COGS % of revenue",
        "AI Stack proposed allocation ($mm)",
        "AI Stack weight",
        "ALL OK boolean",
        "Active V2 BB sats",
        "Active V2 DTC sats",
        "Active V3 BB sats",
        "Active V3 DTC sats",
        "Active sat fleet EoY (year-chained, Rule 23 exception)",
        "Adjusted CoreWeave baseline year-row ($B/GW_IT/yr)",
        "Anchor year for ODC Wright’s Law",
        "Anchor year for cum-upmass Wright's Law",
        "Annual GPU-hr price deflation rate",
        "Annual TAM shift multiplier",
        "Annual bandwidth services cost ($mm/yr)",
        "Annual ground ops cost ($mm/yr)",
        "Annual insurance cost ($mm/yr)",
        "Annual launch services cost ($mm/yr)",
        "Annual other COGS ($mm/yr)",
        "Annual sat D&A ($mm/yr)",
        "Annual spectrum amortization ($mm)",
        "Available cash for IRR queue ($mm)",
        "BANDWIDTH CLAIM & SERVICES COST (paid to Starlink at fully-allocated at-cost rate)",
        "BB $/Gbps ($/Gbps/yr)",
        "BB ARPU ($/mo, year-row from Assumptions)",
        "BB DEMAND CURVE (piecewise-linear Q→Revenue lookup)",
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
        "BB Revenue ($mm)",
        "BB market share % (Starlink revenue mix)",
        "BB pool at-cost rate ($/Gbps/yr)",
        "BB pool at-cost rate ($/Gbps/yr) — read from Starlink Capacity",
        "BB pool cost basis ($mm/yr)",
        "BB subscribers (millions, derived = BB Revenue / (ARPU × 12))",
        "BB-share of ODC bandwidth claim",
        "BLENDED COST STACK + CALIBRATION",
        "BV ENGINE INPUTS (Architecture §11.4 — labour units + hardware)",
        "BV ENGINE OUTPUT (Architecture §11.4)",
        "Bandwidth Removed per Deorbited V2 Mini BB Sat (Gbps)",
        "Bandwidth Removed per Deorbited V2 Mini DTC Sat (Gbps)",
        "Bandwidth Removed per Deorbited V3 BB Sat (Gbps)",
        "Bandwidth Removed per Deorbited V3 DTC Sat (Gbps)",
        "Bandwidth elimination conservation",
        "Bandwidth services cost ($mm)",
        "Base turnaround time per booster (years/flight)",
        "Battery cost per sat ($, pre-WL)",
        "Battery flat cost ($)",
        "Blended $/kg",
        "Blended IRR",
        "Booster fleet beginning-of-year (units)",
        "Booster fleet end-of-year (units)",
        "Booster-only launches per year (count)",
        "Boosters built per year (units)",
        "Boosters retired per year (units)",
        "Broadband ARPU ($/sub/mo, year-row)",
        "CAPEX -- module CapEx aggregation + corporate CapEx + spectrum CapEx + corporate D&A. Sprint 8 fills.",
        "CARVE-OUT CASH INFLOW (Architecture §11.1 — read from Allocator §3)",
        "CENTRAL ALLOCATOR OUTPUTS",
        "COGS — Bandwidth services cost ($mm)",
        "COGS — Constellation D&A ($mm)",
        "COGS — Ground ops ($mm)",
        "COGS — Insurance ($mm)",
        "COGS — Launch services cost ($mm)",
        "COGS — Other COGS ($mm)",
        "CUSTOMER LAUNCH — MODULE BODY",
        "Cadence ceiling (flights/booster/year)",
        "CapEx Lag (years)",
        "CapEx check",
        "Capacity (Gbps)",
        "Capacity Demand (kg-to-LEO)",
        "Capacity available for IRR queue (kg-to-LEO)",
        "Capacity gap (kg-to-LEO)",
        "Capital Allocation ($mm)",
        "Capital deployed ($mm)",
        "Capital deployed ($mm) — diagnostic",
        "Capital lifetime — book value straight-line dep (yrs)",
        "Capital lifetime — book value straight-line depreciation (years)",
        "Cash BoY ($mm)",
        "Cash demand year-row published ($mm) — masked by Blended IRR > 0",
        "Cash flow identity check ($mm — Starting + ΣIPO + ΣFCF − Cash EoY)",
        "Chip FP8 per chip (TFLOPS) — year-row",
        "Chip FP8 performance per chip (TFLOPS) — year-row",
        "Chip TDP per chip (W) — year-row",
        "Chip cost per chip ($) — year-row",
        "Chip cost per sat ($) — year-row",
        "Chip mass per chip (kg) — year-row",
        "Chips per sat",
        "Commercial launch market size ($mm/year) — year-row",
        "Comms (ISL set) cost per sat ($, pre-WL)",
        "Comms (ISL set) flat cost ($)",
        "Comp anchor — AI Stack standalone",
        "Comp anchor — Customer Launch standalone (Rocket Lab)",
        "Comp anchor — Group EV (Brant internal)",
        "Comp anchor — Group EV (Morgan Stanley public)",
        "Comp anchor — Lunar / Mars (NASA HLS lifetime)",
        "Comp anchor — ODC standalone (CoreWeave-anchored)",
        "Comp anchor — Starlink standalone (Bernstein/JPM)",
        "Compute elimination conservation",
        "Compute power per sat (kW)",
        "Constellation Bandwidth (Gbps)",
        "Constellation D&A ($mm)",
        "CoreWeave baseline ($B/GW_IT/yr, 2026 anchor)",
        "CoreWeave baseline anchor ($B/GW_IT/yr, 2026)",
        "Corporate CapEx claim ($mm)",
        "Corporate IT CapEx ($mm)",
        "Corporate IT CapEx ($mm/yr, flat)",
        "Corporate IT useful life (years)",
        "Corporate historical capital base ($mm)",
        "Cost of debt (memo)",
        "Cost of equity (memo)",
        "Credence on Model A (Pr(A))",
        "Cum ODC sats at WL anchor year",
        "Cum ODC sats deployed (running sum) — Rule 23 exception, intentional",
        "Cum Starship stacks manufactured (end-of-year, units)",
        "Cum upmass to date (kg)",
        "Cumulative Gen eng CapEx ($mm)",
        "Cumulative HQ CapEx ($mm)",
        "Cumulative IT CapEx ($mm)",
        "Cumulative Other CapEx ($mm)",
        "Cumulative sats at base year (end-2024)",
        "Cumulative spectrum intangible ($mm)",
        "Cursor avg subscription price ($/seat/mo)",
        "Cursor enterprise API rev per seat ($/year)",
        "Cursor paid seats (millions) — year-row",
        "Customer Launch Blended IRR",
        "Customer Launch Forward IRR (Y+2)",
        "Customer Launch Module CapEx ($mm)",
        "Customer Launch R&D ($mm)",
        "Customer Launch R&D base — Customer Launch external rev ($mm)",
        "Customer Launch R&D — % of external rev",
        "Customer Launch R&D — CAGR (taper)",
        "Customer Launch R&D — end-state % (floor)",
        "Customer Launch R&D — start % of external rev",
        "Customer Launch Spot IRR",
        "Customer Launch cash allocation",
        "Customer Launch cash demand ($mm)",
        "Customer Launch cash demand large default ($mm)",
        "Customer Launch revenue trajectory stub ($mm)",
        "Customer Launch external Starship kg demand stub (kg)",
        "Customer Launch external Starship launches stub",
        "Customer Launch depreciation useful life (years)",
        "Customer Launch forward kg demand at T+lead",
        "Customer Launch ground ops ($mm)",
        "Customer Launch insurance ($mm)",
        "Customer Launch internal transfer revenue ($mm)",
        "Customer Launch kg allocation",
        "Customer Launch kg demand (kg-to-LEO)",
        "Customer Launch kg proposed allocation",
        "Customer Launch kg weight",
        "Customer Launch other COGS ($mm)",
        "Customer Launch proposed allocation ($mm)",
        "Customer Launch weight",
        "Customer Service ($mm) — 2% × Starlink subscription rev",
        "Customer Service — flat % of Starlink subscription rev",
        "D&A check",
        "DEPLOYMENT, FLEET RAMP, CASH/KG DEMAND PUBLISH",
        "DTC $/Gbps ($/Gbps/yr)",
        "DTC ARPU ($/mo, year-row from Assumptions)",
        "DTC ARPU ($/sub/mo, year-row)",
        "DTC DEMAND CURVE (piecewise-linear Q→Revenue lookup)",
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
        "DTC Revenue ($mm)",
        "DTC market share % (Starlink revenue mix)",
        "DTC pool at-cost rate ($/Gbps/yr)",
        "DTC pool at-cost rate ($/Gbps/yr) — read from Starlink Capacity",
        "DTC pool cost basis ($mm/yr)",
        "DTC subscribers (millions, derived = DTC Revenue / (ARPU × 12))",
        "DUAL REVENUE MODEL (Pr(A) × Model A + Pr(B) × Model B; Architecture §9.2)",
        "Demand Curves",
        "EBIT consistency",
        "EBITDA check",
        "EchoStar mid-band CapEx ($mm)",
        "EchoStar mid-band CapEx ($mm) — year-row",
        "Effective Compute Ratio (ECR)",
        "External compute revenue ($mm/yr)",
        "External compute share to customers % — year-row",
        "F9 2nd stage mfg cost ($mm/unit)",
        "F9 Annual Capacity (kg-to-LEO)",
        "F9 D&A share ($mm)",
        "F9 D&A share per launch ($mm) — read from Launch Capacity",
        "F9 Forward IRR (Y+2) — per-launch marginal IRR, year T+2 cashflow",
        "F9 IRR cashflow stream period count N (clamped at R23 MAX)",
        "F9 Spot IRR (per-launch marginal IRR, current year — external customer economics)",
        "F9 V2 BB launches (internal)",
        "F9 V2 DTC launches (internal)",
        "F9 WL learning rate",
        "F9 Wright's Law mfg learning rate",
        "F9 at-cost rate ($mm/launch)",
        "F9 at-cost rate ($mm/launch) — read from Launch Capacity",
        "F9 base booster build rate (boosters/year, pre-V3-trigger)",
        "F9 booster (1st stage) mfg cost ($mm/unit)",
        "F9 booster D&A share per launch ($mm)",
        "F9 booster refurb % of mfg",
        "F9 build-rate decay window (years)",
        "F9 cadence per booster (flights/year, flat)",
        "F9 cadence-utilization per booster (memo, derived)",
        "F9 customer launch insurance + other COGS ($mm/launch)",
        "F9 customer launch price ($mm/launch)",
        "F9 customer launch price ($mm/launch) — 2025 anchor",
        "F9 customer launches per year",
        "F9 customer revenue ($mm)",
        "F9 fairing cost net of 75% recovery ($mm/flight)",
        "F9 fleet beginning-of-year (boosters)",
        "F9 fleet end-of-year (boosters)",
        "F9 internal launches (BB + DTC)",
        "F9 launches per year",
        "F9 lifetime reuses per booster",
        "F9 lifetime reuses per booster — read from Assumptions",
        "F9 manufactured per year (units) — V3-trigger-aware decay note: D61/E61 historical anchors preserved (Sprint 11 Decision A; full IF-bifurcated form deferred to Sprint 12)",
        "F9 payload to LEO (kg)",
        "F9 per-launch Blended IRR (external customer economics)",
        "F9 per-launch annual margin ($mm/yr — cadence × per-launch margin)",
        "F9 per-launch cost slug ($mm — t=0 capex)",
        "F9 per-launch ops cost ($mm)",
        "F9 retired per year (boosters)",
        "F9 retirement rate (% of launches/year)",
        "F9 starting fleet at 2025 SoY (boosters)",
        "F9 variable cost ($mm)",
        "F9 variable cost per launch ($mm)",
        "F9 variable cost per launch ($mm) — read from Launch Capacity",
        "FALCON 9 — VEHICLE SUPPLY",
        "FCF check",
        "F_ref — reference compute unit (TFLOPS, H100 FP8 dense)",
        "F_ref — reference compute unit (TFLOPS, H100 FP8)",
        "Facility CapEx per satellite — base year ($)",
        "Facility CapEx — learning rate",
        "Facility D&A — sat manufacturing + ground stations ($mm/yr, flat)",
        "First mission year (Lunar Mars)",
        "Fleet ODC compute energy delivered (GWh/yr)",
        "Fleet PFLOPS (FP8)",
        "Fleet annual PFLOP-hrs delivered (util-adjusted)",
        "Fleet compute power (GW)",
        "Fleet external compute revenue ($mm/yr)",
        "Forward IRR (Y+2)",
        "Forward IRR look-ahead horizon (years)",
        "Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)",
        "Forward aggregate kg demand",
        "Forward aggregate kg demand growth cap (× current capacity)",
        "Fully-reusable launches per year (count)",
        "G&A ($mm)",
        "G&A base — Group P&L net (Lock d 2026-05-22)",
        "G&A — % of group rev (bounded-CAGR, drift toward ceiling)",
        "GNI per capita growth rate (annual)",
        "GROUP FCF ($mm)",
        "GROUP P&L -- consolidated Revenue / EBITDA / D&A / EBIT / Taxes / NOPAT / CapEx / FCF + inter-module eliminations + conservation block. Sprint 9 fills the P&L walk above row 99.",
        "GROUP REVENUE NET OF ELIMS ($mm)",
        "Gbps per GWh/yr ODC compute energy conversion factor",
        "Gbps per GWh/yr of ODC compute energy",
        "Gen eng D&A ($mm)",
        "General & Administrative — CAGR (drift)",
        "General & Administrative — end-state % (ceiling)",
        "General & Administrative — start % of group rev",
        "General engineering facilities CapEx ($mm)",
        "General engineering facilities CapEx ($mm/yr, flat)",
        "General engineering facilities life (years)",
        "Government launch market size ($mm/year) — year-row",
        "Grok consumer ARPU ($/user/year)",
        "Grok consumer paid subs (millions) — year-row",
        "Grok enterprise API price ($/Mtoken) — year-row",
        "Grok enterprise API token volume (T tokens/year) — year-row",
        "Gross Profit ($mm)",
        "Ground ops cost ($mm)",
        "Ground station / network opex % of revenue",
        "Group COGS (net of elims) ($mm)",
        "Group D&A ($mm)",
        "Group EBIT ($mm)",
        "Group EBITDA ($mm)",
        "Group Gross Profit ($mm)",
        "Group WACC",
        "HQ D&A ($mm)",
        "HQ buildings CapEx ($mm)",
        "HQ buildings CapEx ($mm/yr, flat)",
        "HQ buildings useful life (years)",
        "Hardware $/kg landed (year-row)",
        "Hardware replacement cost factor ($/kg landed) — declining",
        "INPUTS FROM CENTRAL ALLOCATOR",
        "IPO injection amount ($mm)",
        "IPO injection this year ($mm)",
        "IPO injection year",
        "Pre-IPO debt facility ($mm)",
        "IT D&A ($mm)",
        "Inflation rate (% per year)",
        "Insurance ($mm)",
        "Integration & Test cost per sat ($, pre-WL)",
        "Integration & Test flat cost ($)",
        "Internal bandwidth eliminated ($mm)",
        "Internal compute PFLOP-hrs delivered to AI Stack",
        "Internal compute eliminated ($mm)",
        "Internal compute share to AI Stack % — year-row",
        "Internal launch services eliminated ($mm)",
        "Internal transfer revenue (at-cost compute) ($mm)",
        "Internal transfer revenue (at-cost compute) ($mm/yr)",
        "KG RESERVATION OFF-THE-TOP (Architecture §11.3 + §6.4)",
        "Kg demand year-row published (kg) — masked by Blended IRR > 0",
        "LAUNCH SERVICES (paid to Launch Capacity at fully-allocated at-cost rate)",
        "LR — chips (per doubling)",
        "LR — subsystems (per doubling)",
        "LUNAR MARS P&L (Architecture §11.5)",
        "LUNAR MISSION DEPLOYMENT (Architecture §11.2)",
        "LUNAR accumulated book value (year)",
        "LUNAR active labour fleet EoY (running sum, net retirements)",
        "LUNAR annual BV contribution ($mm/yr)",
        "LUNAR annual hardware value add ($mm/yr)",
        "LUNAR annual production output ($mm/yr)",
        "LUNAR labour units landed (count this year)",
        "LUNAR labour units retired this year (cohort lookback)",
        "Labour annual output per unit base year ($mm/yr)",
        "Labour annual output per unit this year ($mm/yr)",
        "Labour unit base hourly output ($/hr)",
        "Labour unit base hourly output ($/hr; burdened $22/0.7)",
        "Labour unit cost ($/unit) — declining curve",
        "Labour unit daily working hours",
        "Labour unit mass (kg)",
        "Labour unit operational lifespan on surface (years)",
        "Labour unit productivity factor",
        "Labour unit productivity factor vs human baseline",
        "Labour unit productivity learning rate (%/yr)",
        "Labour unit useful life (yrs)",
        "Launch insurance % of external revenue",
        "Launch other COGS % of external revenue",
        "Launch services cost ($mm) — internal at-cost from Customer Launch",
        "Launch services cost per sat ($mm)",
        "Launch services elimination conservation",
        "Launches per Starship vehicle per year (cadence × variant blend, used for sizing)",
        "Launches per Starship vehicle per year (cadence)",
        "Legacy V1/V1.5 Active Bandwidth (Gbps, year-row runoff)",
        "Legacy V1/V1.5 Bandwidth — end-2025 (Gbps)",
        "Legacy V1/V1.5 D&A baseline ($mm, 2025 anchor)",
        "Legacy V1/V1.5 D&A useful life (yrs)",
        "Leverage E/V (memo)",
        "Lifetime reuses per booster (year cap)",
        "Lifetime reuses per ship (cap)",
        "Lunar % payload as labour units",
        "Lunar / Mars — terminal BV multiplier",
        "Lunar Accumulated Book Value ($mm)",
        "Lunar Mars Blended IRR (hardcoded 0 per Architecture §11.6)",
        "Lunar Mars Module CapEx ($mm)",
        "Lunar Mars Module D&A ($mm)",
        "Lunar Mars cash allocation",
        "Lunar Mars forward kg demand at T+lead",
        "Lunar Mars kg allocation",
        "Lunar Mars kg reserved (off-the-top)",
        "Lunar Mars total kg reserved off-top (kg-to-LEO)",
        "Lunar cash allocation ($mm)",
        "Lunar depot multiplier (×)",
        "Lunar fuel depot multiplier per outbound Starship",
        "Lunar hardware mass landed (kg)",
        "Lunar labour mass landed (kg)",
        "Lunar labour share of surface payload — year-row",
        "Lunar labour share this year (%)",
        "Lunar payload per surface ship (kg)",
        "Lunar payload per surface-landed Starship (kg)",
        "Lunar payload value ($mm/ship)",
        "Lunar share of Mars/Moon carve-out cash — year-row",
        "Lunar share of carve-out (% — year-row)",
        "Lunar surface missions deployed (count)",
        "Lunar surface payload mass (kg landed)",
        "Lunar total launches × LEO payload (kg)",
        "Lunar total vehicle launches (count)",
        "MARS MISSION DEPLOYMENT (Architecture §11.2)",
        "MARS accumulated book value (year)",
        "MARS active labour fleet EoY (running sum, net retirements)",
        "MARS annual BV contribution ($mm/yr)",
        "MARS annual hardware value add ($mm/yr)",
        "MARS annual production output ($mm/yr)",
        "MARS labour units landed (count this year)",
        "MARS labour units retired this year (cohort lookback)",
        "MEMO: DIAGNOSTICS",
        "MFW-IRR — AI Stack economic life N (years)",
        "MFW-IRR — Customer Launch economic life clamp MAX (years)",
        "MFW-IRR — Customer Launch economic life clamp MIN (years)",
        "MFW-IRR — ODC economic life N (years)",
        "MFW-IRR — Starlink economic life N (years)",
        "MODULE P&L",
        "Manufacturing learning rate (per doubling of cum units)",
        "Mars % payload as labour units",
        "Mars Accumulated Book Value ($mm)",
        "Mars carve-out % of prior-year Group FCF",
        "Mars carve-out % of prior-year Group FCF (input)",
        "Mars carve-out floor ($mm/yr)",
        "Mars carve-out floor ($mm/yr) (input)",
        "Mars carve-out uses prior-year FCF (0/1)",
        "Mars cash allocation ($mm)",
        "Mars depot multiplier (×)",
        "Mars fuel depot multiplier per outbound Starship",
        "Mars hardware mass landed (kg)",
        "Mars labour mass landed (kg)",
        "Mars labour share of surface payload — year-row",
        "Mars labour share this year (%)",
        "Mars payload per surface ship (kg)",
        "Mars payload per surface-landed Starship (kg)",
        "Mars payload value ($mm/ship)",
        "Mars share of carve-out (% — year-row)",
        "Mars share of carve-out cash — year-row",
        "Mars surface missions deployed (count)",
        "Mars surface payload mass (kg landed)",
        "Mars total launches × LEO payload (kg)",
        "Mars total vehicle launches (count)",
        "Mars/Moon R&D ($mm/yr) — year-row",
        "Mars/Moon carve-out claim ($mm)",
        "Mars/Moon strategic carve-out ($mm)",
        "Mars/Moon strategic carve-out ($mm/yr)",
        "Max annual production growth rate (multiplier)",
        "Memo: 2025 calibration PASS/CHECK",
        "Memo: 2025 calibration anchors (read-only diagnostics)",
        "Memo: 2025 calibration status",
        "Memo: Average $/Gbps BB from curve (= BB Revenue / BB Gbps × 1e6)",
        "Memo: Average $/Gbps DTC from curve (= DTC Revenue / DTC Gbps × 1e6)",
        "Memo: BV decay — Lunar ($mm/yr) — Valuation input only, NOT in Group D&A",
        "Memo: BV decay — Mars ($mm/yr) — Valuation input only, NOT in Group D&A",
        "Memo: Carve-out vs Module CapEx gap ($mm)",
        "Memo: Corporate D&A ($mm)",
        "Memo: Cum V3 BB sats launched (running sum) — Rule 23 exception, year-chained",
        "Memo: Customer Launch Module D&A in COGS ($mm)",
        "Memo: Customer Launch external revenue ($mm)",
        "Memo: F9 customer launches 2025",
        "Memo: F9 customer revenue 2025 (target $4,290M ±5%)",
        "Memo: Facility D&A — sat manufacturing + ground stations ($mm)",
        "Memo: Group D&A 2025 delta (%)",
        "Memo: Group D&A 2025 target ($mm) — REVISED",
        "Memo: Group EBITDA 2025 delta (%)",
        "Memo: Group EBITDA 2025 target ($mm) — REVISED",
        "Memo: Group FCF 2025 delta (%)",
        "Memo: Group FCF 2025 target ($mm) — REVISED",
        "Memo: Group Gross Profit 2025 delta (%)",
        "Memo: Group Gross Profit 2025 target ($mm) — REVISED",
        "Memo: Group Revenue 2025 delta (%)",
        "Memo: Group Revenue 2025 target ($mm) — revised",
        "Memo: Group revenue (Sprint 8 pre-aggregation; sum of 5 module R201s)",
        "Memo: Legacy V1/V1.5 D&A ($mm)",
        "Memo: Lunar labour annual output ($mm/yr)",
        "Memo: Lunar surface missions cumulative",
        "Memo: Mars labour annual output ($mm/yr)",
        "Memo: Mars surface missions cumulative",
        "Memo: ODC sat D&A in COGS ($mm)",
        "Memo: Q4'25 Group EBITDA original target ($mm) — archaeology",
        "Memo: Q4'25 Group FCF original target ($mm) — archaeology",
        "Memo: Spectrum amort ($mm)",
        "Memo: Sprint 8 Group D&A contribution (Corporate D&A + Spectrum amort)",
        "Memo: Starlink Constellation D&A in Starlink COGS ($mm)",
        "Memo: Starship at-cost rate, ship-expended mode (Moon/Mars, $mm/launch)",
        "Memo: Starship customer revenue 2025 (target $0 exact)",
        "Memo: Total Group CapEx 2025 (read from CapEx tab)",
        "Memo: Total Lunar + Mars vehicle launches this year",
        "Memo: Total OpEx 2025 (read from OpEx tab)",
        "Memo: Total OpEx 2025 calibration anchor ($mm)",
        "Memo: Total OpEx 2025 calibration delta (%)",
        "Memo: Total R&D 2025 calibration anchor ($mm)",
        "Memo: Total active Starlink sats (excl legacy V1/V1.5)",
        "Memo: Total carve-out reserved this year ($mm)",
        "Memo: V2 BB Blended IRR",
        "Memo: V2 BB Forward IRR (Y+2)",
        "Memo: V2 BB Spot IRR",
        "Memo: V2 BB per-sat cost ($mm/sat) — sat unit cost + facility per sat",
        "Memo: V2 BB per-sat net marginal revenue per year ($mm/sat/yr)",
        "Memo: V2 DTC Blended IRR",
        "Memo: V2 DTC Forward IRR (Y+2)",
        "Memo: V2 DTC Spot IRR",
        "Memo: V2 DTC per-sat cost ($mm/sat)",
        "Memo: V2 DTC per-sat net marginal revenue per year ($mm/sat/yr)",
        "Memo: V3 BB Blended IRR",
        "Memo: V3 BB Forward IRR (Y+2)",
        "Memo: V3 BB Spot IRR",
        "Memo: V3 BB per-sat cost ($mm/sat)",
        "Memo: V3 BB per-sat net marginal revenue per year ($mm/sat/yr)",
        "Memo: V3 DTC Blended IRR",
        "Memo: V3 DTC Forward IRR (Y+2)",
        "Memo: V3 DTC Spot IRR",
        "Memo: V3 DTC per-sat cost ($mm/sat)",
        "Memo: V3 DTC per-sat net marginal revenue per year ($mm/sat/yr)",
        "Memo: Σ Module D&A in COGS ($mm)",
        "Memo: Σ Module FCF reconciliation residual ($mm)",
        "Mission ops cost — Lunar ($mm)",
        "Mission ops cost — Mars ($mm)",
        "Module CapEx ($mm)",
        "Module CapEx ($mm) — restated",
        "Module D&A ($mm) — informational (also in COGS rows 86 + 88)",
        "Module D&A add-back ($mm)",
        "Module EBITDA ($mm)",
        "Module EBITDA Margin %",
        "Module FCF ($mm)",
        "Module operating cost — Lunar (% of Lunar CapEx)",
        "Module operating cost — Mars (% of Mars CapEx)",
        "Multiple — AI Stack (EV/Rev at 2050)",
        "Multiple — Customer Launch (EV/Rev at 2050)",
        "Multiple — Lunar / Mars (anchor stub, $B)",
        "Multiple — ODC (EV/Rev at 2050)",
        "Multiple — Starlink (EV/Rev at 2050)",
        "NOPAT ($mm)",
        "ODC BB Gbps demand",
        "ODC BB bandwidth cost ($mm/yr)",
        "ODC Blended IRR",
        "ODC DTC Gbps demand",
        "ODC DTC bandwidth cost ($mm/yr)",
        "ODC FULLY-ALLOCATED COST + AT-COST COMPUTE RATE (Architecture §7.3)",
        "ODC Forward IRR (Y+2)",
        "ODC Module CapEx ($mm)",
        "ODC R&D $-profile ($mm, pre-revenue floor)",
        "ODC R&D $-profile ($mm/yr) — year-row",
        "ODC R&D ($mm) — MAX($-profile, % × rev)",
        "ODC R&D base — ODC rev ($mm)",
        "ODC R&D — % of ODC rev (bounded-CAGR)",
        "ODC R&D — CAGR (taper)",
        "ODC R&D — end-state % (floor)",
        "ODC R&D — start % of ODC rev",
        "ODC SAT PHYSICAL & COST STACK",
        "ODC Spot IRR",
        "ODC Starship kg demand",
        "ODC Starship launches (internal)",
        "ODC at-cost compute rate ($/PFLOP-hr)",
        "ODC cash allocation",
        "ODC cash demand ($mm)",
        "ODC cash demand large default ($mm)",
        "ODC cash demand large default ($mm) — Assumptions read",
        "ODC external compute share to customers % — year-row",
        "ODC fleet design life (years)",
        "ODC forward kg demand at T+lead",
        "ODC insurance % of revenue",
        "ODC internal compute share to AI Stack % — year-row",
        "ODC kg allocation",
        "ODC kg demand (kg-to-LEO)",
        "ODC kg demand large default (kg)",
        "ODC kg demand large default (kg) — Assumptions read",
        "ODC kg proposed allocation",
        "ODC kg weight",
        "ODC other COGS % of revenue",
        "ODC proposed allocation ($mm)",
        "ODC weight",
        "OPEX -- corporate operating costs (R&D by module + SG&A by function). Sprint 8 fills.",
        "OpEx claim ($mm)",
        "Orbital PUE",
        "Other COGS ($mm)",
        "Other D&A ($mm)",
        "Other corporate CapEx ($mm)",
        "Other corporate CapEx ($mm/yr, flat)",
        "Other corporate operating ($mm) — 1% × Group P&L net (Lock d 2026-05-22)",
        "Other corporate operating — flat % of group rev",
        "Other corporate useful life (years)",
        "PER-SAT MARGINAL IRR ENGINE (Architecture §9.4, reads external revenue only per §7.3)",
        "PER-SHIP COST BUILD (Architecture §11.2)",
        "PUE uplift (orbital advantage = PUE_base / PUE_orbital)",
        "PUE_base (terrestrial colo)",
        "Payload — booster-only mode (kg-to-LEO)",
        "Payload — fully reusable mode (kg-to-LEO)",
        "Per-launch upmass (kg)",
        "Per-launch upmass (kg) — from Launch Capacity",
        "Per-sat BB Gbps demand",
        "Per-sat DTC Gbps demand",
        "Per-sat Expected Revenue ($mm/yr) — Pr-A-weighted",
        "Per-sat Model A revenue ($mm/yr) — energy-anchored",
        "Per-sat Model B revenue ($mm/yr) — η-anchored",
        "Per-sat bandwidth cost ($mm/yr)",
        "Per-sat billable H100-equiv GPU-hrs/yr",
        "Per-sat external compute revenue ($mm/yr) — at market",
        "Per-sat ground ops cost ($mm/yr)",
        "Per-sat insurance cost ($mm/yr)",
        "Per-sat net marginal revenue ($mm/yr)",
        "Per-sat other COGS ($mm/yr)",
        "Per-sat upfront cost ($mm) — sat hardware + launch services per sat",
        "Per-ship cost — Lunar ($mm)",
        "Per-ship cost — Mars ($mm)",
        "Pr(A) (Architecture §9.2)",
        "Price per H100-equiv GPU-hr ($) — year-row",
        "Prior-year Group FCF read ($mm)",
        "Prior-year Group FCF read ($mm/yr)",
        "Productivity multiplier (year-row, anchor-and-offset)",
        "Projected capacity at T+lead (kg-to-LEO)",
        "R&D — Moon/Mars ($mm/yr) — year-row",
        "Real GNI growth rate (% per year)",
        "Required launches (count)",
        "Required vehicles (count)",
        "Revenue check",
        "Risk premium — AI Stack",
        "Risk premium — Customer Launch",
        "Risk premium — Lunar / Mars",
        "Risk premium — ODC",
        "Risk premium — Starlink (over group WACC)",
        "S&M ($mm)",
        "S&M base — Starlink + Starshield + Customer Launch ext + AI Stack rev ($mm)",
        "S&M — % of base (bounded-CAGR)",
        "STARLINK CAPACITY -- aggregates constellation BB + DTC pools, allocates internal bandwidth claim to ODC, computes available bandwidth for external Starlink revenue. Sprint 4 fills.",
        "STARLINK CAPACITY — supply-side bandwidth aggregation + internal claim to ODC",
        "STARSHIP — VEHICLE SUPPLY",
        "Sales & Marketing — CAGR (taper)",
        "Sales & Marketing — end-state % (floor)",
        "Sales & Marketing — start % of (Starlink+Starshield+Customer Launch ext) rev",
        "Sat PFLOPS (FP8, per sat per year computed)",
        "Sat chip mass (kg)",
        "Sat retirements (year-row, N-year cohort linear)",
        "Sat solar generation (W)",
        "Sat solar generation (W, for $/W subsystem cost)",
        "Sat subsystem cost (pre-WL, $)",
        "Sat subsystem cost (with WL, $) — year-row",
        "Sat thermal mass (kg)",
        "Sat total cost ($, year-row)",
        "Sat total cost ($mm, year-row)",
        "Satellite Dep per kg — annual decay rate",
        "Satellite Dep per kg — base year ($/kg/yr)",
        "Satellite cost floor ($/kg)",
        "Satellite cost per kg — base year ($/kg)",
        "Satellite cost per kg — learning rate",
        "Satellite useful life — V2 Mini (years)",
        "Satellite useful life — V3 (years)",
        "Sats deployable from cash allocation",
        "Sats deployable from kg allocation",
        "Sats deployed (actual)",
        "Sats per F9 launch — V2 BB",
        "Sats per F9 launch — V2 DTC",
        "Sats per Starship launch (Compute config)",
        "Sats per Starship launch — V3 BB",
        "Sats per Starship launch — V3 DTC",
        "Shielding cost per sat ($, pre-WL)",
        "Shielding flat cost ($)",
        "Sigmoid IRR-blend exponent k",
        "Solar array cost per sat ($, pre-WL)",
        "Solar array unit cost ($/W)",
        "Solar generation per sat (kW, gen requirement)",
        "SpaceX commercial market share % — year-row",
        "SpaceX government market share % — year-row",
        "Spectrum CapEx claim ($mm)",
        "Spectrum amortization (BB-only) ($mm)",
        "Spectrum useful life (years)",
        "Spot IRR",
        "Starlink BB Revenue from curve ($mm)",
        "Starlink BB capacity input (Gbps)",
        "Starlink Blended IRR",
        "Starlink DTC Revenue from curve ($mm)",
        "Starlink DTC capacity input (Gbps)",
        "Starlink Forward IRR (Y+2)",
        "Starlink Module CapEx ($mm)",
        "Starlink R&D ($mm)",
        "Starlink R&D base — Starlink + Starshield rev ($mm)",
        "Starlink R&D — % of (Starlink + Starshield) rev",
        "Starlink R&D — CAGR (taper)",
        "Starlink R&D — end-state % (floor)",
        "Starlink R&D — start % of (Starlink + Starshield) rev",
        "Starlink Spot IRR",
        "Starlink V2 BB Blended IRR",
        "Starlink V2 BB cash allocation",
        "Starlink V2 BB cash allocation ($mm)",
        "Starlink V2 BB cash demand ($mm)",
        "Starlink V2 BB proposed allocation ($mm)",
        "Starlink V2 BB weight",
        "Starlink V2 DTC Blended IRR",
        "Starlink V2 DTC cash allocation",
        "Starlink V2 DTC cash allocation ($mm)",
        "Starlink V2 DTC cash demand ($mm)",
        "Starlink V2 DTC proposed allocation ($mm)",
        "Starlink V2 DTC weight",
        "Starlink V3 BB Blended IRR",
        "Starlink V3 BB cash allocation",
        "Starlink V3 BB cash allocation ($mm)",
        "Starlink V3 BB cash demand ($mm)",
        "Starlink V3 BB kg allocation",
        "Starlink V3 BB kg allocation (kg-to-LEO)",
        "Starlink V3 BB kg demand (kg-to-LEO)",
        "Starlink V3 BB kg proposed allocation",
        "Starlink V3 BB kg weight",
        "Starlink V3 BB proposed allocation ($mm)",
        "Starlink V3 BB weight",
        "Starlink V3 DTC Blended IRR",
        "Starlink V3 DTC cash allocation",
        "Starlink V3 DTC cash allocation ($mm)",
        "Starlink V3 DTC cash demand ($mm)",
        "Starlink V3 DTC kg allocation",
        "Starlink V3 DTC kg allocation (kg-to-LEO)",
        "Starlink V3 DTC kg demand (kg-to-LEO)",
        "Starlink V3 DTC kg proposed allocation",
        "Starlink V3 DTC kg weight",
        "Starlink V3 DTC proposed allocation ($mm)",
        "Starlink V3 DTC weight",
        "Starlink cash allocation",
        "Starlink cash ask year-row ($mm, large default)",
        "Starlink forward kg demand at T+lead",
        "Starlink ground ops % of revenue",
        "Starlink insurance % of revenue",
        "Starlink internal bandwidth revenue ($mm)",
        "Starlink kg allocation",
        "Starlink kg ask year-row (large default, exceeds plausible capacity)",
        "Starlink other COGS % of revenue",
        "Starlink — exit revenue multiple",
        "Starshield $/Gbps ($/Gbps/yr)",
        "Starshield Reserved % — decay rate",
        "Starshield Reserved % — floor",
        "Starshield Reserved % — start",
        "Starshield Rev per Gbps — base year ($/Gbps)",
        "Starshield Rev per Gbps — decay rate",
        "Starshield reserved %",
        "Starshield reserved Gbps",
        "Starshield revenue ($mm)",
        "Starship 2nd-stage manufacturing cost ($mm/unit)",
        "Starship 2nd-stage manufacturing cost ($mm/unit, base)",
        "Starship Capacity Allocation (kg-to-LEO)",
        "Starship D&A share ($mm)",
        "Starship D&A share per launch ($mm) — read from Launch Capacity",
        "Starship D&A share per launch, fully reusable mode ($mm)",
        "Starship D&A useful life — memo add-back for Launch standalone DCF",
        "Starship Forward IRR (Y+2)",
        "Starship IRR cashflow stream period count N (clamped at R23 MAX, year-row)",
        "Starship LEO payload per launch (kg)",
        "Starship LEO payload per launch — Compute config (kg)",
        "Starship Spot IRR",
        "Starship Total Annual Capacity (kg-to-LEO) — from Launch Capacity",
        "Starship V3 BB launches (internal)",
        "Starship V3 DTC launches (internal)",
        "Starship at-cost rate ($mm/launch)",
        "Starship at-cost rate ($mm/launch) — read from Launch Capacity",
        "Starship booster share of manufacturing cost (% of stack mfg)",
        "Starship capacity available for customer launches (kg)",
        "Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)",
        "Starship customer launch insurance + other COGS ($mm/launch)",
        "Starship customer launch margin multiplier (year-row)",
        "Starship customer launch margin — 2027 anchor (multiplier on at-cost rate)",
        "Starship customer launch margin — 2050 terminal (multiplier on at-cost rate, floor)",
        "Starship customer launch margin — CAGR (% change/yr from 2027 anchor)",
        "Starship customer launch price ($mm/launch)",
        "Starship customer launch price ($mm/launch) — year-row",
        "Starship customer launches per year",
        "Starship customer revenue ($mm)",
        "Starship internal kg demand (post-Starlink + ODC + AI Stack)",
        "Starship internal launches (V3 BB + V3 DTC + ODC + AI Stack)",
        "Starship lifetime reuses per booster — year-row from Launch Capacity R21",
        "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)",
        "Starship manufacturing cost ($mm/stack, this year)",
        "Starship manufacturing cost anchor ($mm/stack, 2024 baseline)",
        "Starship ops + fuel + refurb WL learning rate (% reduction per doubling cum stacks)",
        "Starship ops + fuel + refurb cost anchor ($mm/launch, 2024 baseline)",
        "Starship ops + fuel + refurb cost per launch ($mm) — read from Launch Capacity",
        "Starship ops + fuel + refurb cost per launch ($mm, this year)",
        "Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)",
        "Starship payload — 2030 anchor (kg-to-LEO, fully reusable mode)",
        "Starship payload — booster-only mode delta (kg, additive to fully-reusable payload)",
        "Starship payload — max cap (kg-to-LEO)",
        "Starship per-launch Blended IRR (external customer economics)",
        "Starship per-launch annual margin ($mm/yr — cadence × per-launch margin)",
        "Starship per-launch cost slug ($mm — year-row of manufacturing cost from Launch Capacity R37)",
        "Starship variable cost ($mm)",
        "Starship vehicle cost amortized ($mm/ship)",
        "Starting BoY 2025 subscribers (millions)",
        "Starting cash position EoY 2024 ($mm)",
        "Steady-state utilization",
        "Steady-state utilization (for Model A util-adjustment ratio)",
        "Structure cost per sat ($, pre-WL)",
        "Structure flat cost ($)",
        "Subsidy mix (% of net adds subsidized)",
        "Super Heavy manufacturing cost ($mm/unit)",
        "Super Heavy manufacturing cost ($mm/unit, base year)",
        "TAM inflation rate (annual)",
        "Tax rate (corporate, US federal + state blended)",
        "Taxes ($mm)",
        "Taxes claim ($mm)",
        "Terminal COGS ($mm)",
        "Terminal COGS per unit ($)",
        "Terminal FCF averaging window (years pre-2050)",
        "Terminal growth rate g (group + most modules)",
        "Terminal hardware revenue ($mm)",
        "Terminal retail price ($, non-subsidized)",
        "Terminal retail price ($, subsidized)",
        "Terrestrial price deflation %/yr",
        "Terrestrial price deflation %/yr (Model A baseline year-row driver)",
        "Thermal system cost per sat ($, pre-WL)",
        "Thermal system unit cost ($/kg)",
        "Total Annual Capacity (kg-to-LEO)",
        "Total COGS ($mm)",
        "Total Capital Available ($mm)",
        "Total Corporate CapEx ($mm)",
        "Total Corporate D&A ($mm)",
        "Total D&A add-back ($mm)",
        "Total Group CapEx ($mm)",
        "Total Lunar + Mars accumulated BV ($mm)",
        "Total Mars/Moon strategic carve-out ($mm/yr)",
        "Total Module CapEx ($mm)",
        "Total ODC Gbps demand",
        "Total OpEx ($mm)",
        "Total R&D ($mm)",
        "Total Revenue ($mm)",
        "Total SG&A ($mm)",
        "Total Starship capacity (kg-to-LEO)",
        "Total Starship launches per year",
        "Total active BB Gbps",
        "Total active BB Gbps (Starlink + Starshield + legacy)",
        "Total active DTC Gbps",
        "Total customer launch market (launches/yr)",
        "Total customer launch market (launches/yr) — 2025 anchor",
        "Total customer launch market CAGR (% growth/yr)",
        "Total fully-allocated ODC cost ($mm/yr)",
        "Total launch CapEx per year ($mm) — variable + amortized D&A",
        "Total launches per year (all vehicles)",
        "Total sat dry mass (kg)",
        "Total upmass per year (kg)",
        "Utilization % (fleet ramp) — year-row",
        "V2 BB Gbps per sat",
        "V2 BB facility CapEx ($mm)",
        "V2 BB facility CapEx per sat ($mm/sat)",
        "V2 BB historical retirement",
        "V2 BB launch-cohort retirement",
        "V2 BB launches per year",
        "V2 BB sat CapEx ($mm)",
        "V2 BB sat unit cost ($mm/sat)",
        "V2 DTC Gbps per sat",
        "V2 DTC facility CapEx ($mm)",
        "V2 DTC facility CapEx per sat ($mm/sat)",
        "V2 DTC historical retirement",
        "V2 DTC launch-cohort retirement",
        "V2 DTC launches per year",
        "V2 DTC permanent cap flag — RETIRED 2026-05-26 (replaced by V2 phase-out year R350 per §20.6 Architecture amendments)",
        "V2 DTC sat CapEx ($mm)",
        "V2 DTC sat unit cost ($mm/sat)",
        "V2 Mini BB Active Sats — end-2025",
        "V2 Mini BB Bandwidth — end-2025 (Gbps)",
        "V2 Mini BB Deorbit Lag (years)",
        "V2 Mini BB Sats Launched 2025",
        "V2 Mini BB historical baseline (SoY 2025)",
        "V2 Mini Bandwidth per Sat — BB (Gbps)",
        "V2 Mini Bandwidth per Sat — DTC (Gbps)",
        "V2 Mini DTC Active Sats — end-2025",
        "V2 Mini DTC Bandwidth — end-2025 (Gbps)",
        "V2 Mini DTC Deorbit Lag (years)",
        "V2 Mini DTC Sats Launched 2025",
        "V2 Mini DTC historical baseline (SoY 2025)",
        "V2 Mini Mass (kg)",
        "V2 Mini cost floor ($/kg)",
        "V2 Mini cost per kg — base year ($/kg)",
        "V2 Mini cost per kg — learning rate",
        "V2 phase-out year (no V2 BB / V2 DTC launches from this year)",
        "V2/V3 ratchet flag — RETIRED 2026-05-26 (replaced by V2 phase-out R350 + V3 trigger LC R56 gates per §20.6 Architecture amendments)",
        "V3 BB Bandwidth per Sat — base year (Gbps)",
        "V3 BB Deorbit Lag (years)",
        "V3 BB Gbps per sat",
        "V3 BB Sats Launched 2025",
        "V3 BB Starship kg demand",
        "V3 BB Wright’s Law anchor — cum sats",
        "V3 BB bandwidth-per-sat Wright’s Law learning rate (per doubling)",
        "V3 BB facility CapEx ($mm)",
        "V3 BB facility CapEx per sat ($mm/sat)",
        "V3 BB first launch year",
        "V3 BB launch-cohort retirement",
        "V3 BB launches per year",
        "V3 BB launches per year stub trajectory",
        "V3 BB sat CapEx ($mm)",
        "V3 BB sat unit cost ($mm/sat)",
        "V3 DTC Bandwidth per Sat (Gbps)",
        "V3 DTC Deorbit Lag (years)",
        "V3 DTC Gbps per sat",
        "V3 DTC Sats Launched 2025",
        "V3 DTC Starship kg demand",
        "V3 DTC facility CapEx ($mm)",
        "V3 DTC facility CapEx per sat ($mm/sat)",
        "V3 DTC first launch year",
        "V3 DTC launch-cohort retirement",
        "V3 DTC launches per year",
        "V3 DTC launches per year stub trajectory",
        "V3 DTC sat CapEx ($mm)",
        "V3 DTC sat unit cost ($mm/sat)",
        "V3 Mass (kg)",
        "V3 Starlink launch trigger year",
        "V3 bandwidth cap (Gbps)",
        "V3 bandwidth per sat — learning rate",
        "VALUATION -- DCF off Group FCF + Sum-of-parts per module + Multiples cross-check + Comparables + Sensitivity. Sprint 11 fills.",
        "Variant mix (% fully reusable)",
        "Vehicle build claim ($mm)",
        "Vehicle build claim toggle (0=legacy mode, 1=forward-demand-sized non-module claim)",
        "Vehicle build lead time (years)",
        "Vehicle masked-demand large default (sats; effectively uncapped)",
        "WL learning rate — turnaround vs cum upmass doubling",
        "Wanted sats deployed (uncapped, cash-derived)",
        "Workload mix — % inference",
        "Wright's Law multiplier on subsystems (year-row)",
        "Year-N non-module claims ($mm)",
        "Σ Module COGS (gross, pre-elim) ($mm)",
        "Σ Module revenue (gross, pre-elim) ($mm)",
        "Σ cash weights (denominator for shares)",
        "Σ kg weights (denominator for shares)",
        "▸ AI Stack (in-queue module)",
        "▸ AI Stack kg sub-block (terrestrial — kg demand structurally 0)",
        "▸ AI Stack operating parameters",
        "▸ Annual TAM growth — inflation + real GNI components",
        "▸ At-cost transfer rates ($/Gbps/yr; for Sprint 5 ODC + Starlink internal bandwidth revenue)",
        "▸ Available bandwidth for external Starlink revenue",
        "▸ BB/DTC market mix (Spec 09)",
        "▸ Bandwidth flow to ODC (Spec 04 PLACEHOLDERS)",
        "▸ CAPEX + FCF",
        "▸ COGS (Constellation D&A, Ground ops, Spectrum amort BB-only, Terminal COGS, Insurance, Other)",
        "▸ COST OF GOODS SOLD ($mm)",
        "▸ Cash pool boundary inputs",
        "▸ Chip roadmap (year-rows, H100 → AI5 → Dojo-3)",
        "▸ Chip roadmap reads (year-rows)",
        "▸ Comparables anchors ($B)",
        "▸ Constellation opening balances (Mach33 historical anchors — hard)",
        "▸ Corporate facilities CapEx ($mm/yr)",
        "▸ Corporate historical capital base",
        "▸ Corporate useful lives",
        "▸ Cursor (orchestration)",
        "▸ Curve evaluators (year-row, read by Starlink module)",
        "▸ Customer Launch (in-queue module)",
        "▸ Customer Launch kg sub-block (external Starship demand)",
        "▸ Demand mechanic (total market + F9 vs Starship split via IRR + capacity)",
        "▸ Deorbit parameters",
        "▸ Depreciation parameters",
        "▸ Dual revenue model (Sprint 3.5)",
        "▸ EchoStar spectrum (Spec 03 §5)",
        "▸ External revenue (bandwidth-driven: Available Gbps × $/Gbps; subs derived)",
        "▸ F9 capacity + at-cost transfer rate",
        "▸ F9 customer launches — economics",
        "▸ F9 supply mechanic (pre-V3-trigger anchors + post-trigger decay)",
        "▸ Falcon 9 physical + cost parameters",
        "▸ Grok consumer (X Premium / Grok Premium)",
        "▸ Grok enterprise (API)",
        "▸ IRR engine + sigmoid blend parameters",
        "▸ Internal bandwidth revenue (Starlink → ODC, 4-step pattern per Architecture §7.2)",
        "▸ Internal claim by ODC (Sprint 5 placeholders)",
        "▸ Internal transfer revenue (launch services to Sprint 4/5/6 consumers)",
        "▸ Labour unit shared parameters (Optimus-class proxy)",
        "▸ Lunar / Mars share of carve-out cash (derived deployment)",
        "▸ Lunar-specific",
        "▸ Mars-specific",
        "▸ Memo: 2025 calibration anchors + diagnostic checks",
        "▸ Module P&L (vending-machine: Revenue → COGS → EBITDA → CapEx → FCF)",
        "▸ Module P&L (vending-machine: Revenue → COGS → Module EBITDA → CapEx → FCF)",
        "▸ Module-wide parameters",
        "▸ Moon/Mars strategic carve-out (Vlad-confirmed MC-variable)",
        "▸ ODC (in-queue module)",
        "▸ ODC internal vs external compute split (NEW per Vlad's framing)",
        "▸ ODC kg sub-block",
        "▸ Per-launch marginal IRR engines (F9 + Starship, external customer only)",
        "▸ Per-vehicle CapEx (sat unit cost via Wright's Law + facility CapEx with 1-yr lag)",
        "▸ Physical + cost parameters (from Assumptions §3)",
        "▸ Pool cost basis ($mm/yr; reads Starlink tab COGS components)",
        "▸ R&D by module (start% / end% / CAGR taper per Spec 03 §2.2)",
        "▸ R&D — Moon/Mars ($-profile year-row, pre-revenue)",
        "▸ Revenue parameters",
        "▸ SG&A by function",
        "▸ Satellite & subsystem anchors (V2 Compute config)",
        "▸ Satellite physical",
        "▸ SoTP multiples (EV/Revenue at 2050)",
        "▸ Starlink V2 BB",
        "▸ Starlink V2 DTC",
        "▸ Starlink V3 BB",
        "▸ Starlink V3 BB kg sub-block",
        "▸ Starlink V3 DTC",
        "▸ Starlink V3 DTC kg sub-block",
        "▸ Starlink large-default cash + kg asks (Spec 09)",
        "▸ Starshield (Vlad-corrected from Q4'25)",
        "▸ Starshield revenue (Q4'25 mechanic — reserved Gbps × $/Gbps with decay)",
        "▸ Starship at-cost transfer rate (Architecture §7.1)",
        "▸ Starship cadence (Wright's Law on cum upmass)",
        "▸ Starship customer launches — economics",
        "▸ Starship time-varying inputs (year-rows)",
        "▸ Starship vehicle physical + cost parameters",
        "▸ Subscribers + ARPU + Terminals",
        "▸ Subsystem unit costs (per-sat, flat unless noted)",
        "▸ Subsystem unit costs + Wright's Law",
        "▸ Terminal value parameters",
        "▸ Total active Gbps (BB + DTC, from Starlink tab active sat fleet)",
        "▸ Variant mix + booster lifetime reuses (year-rows from Assumptions §3)",
        "▸ Vehicle build claim (Spec 09 architecture)",
        "▸ Vehicle deployment (V2 BB, V2 DTC, V3 BB, V3 DTC — launches, fleet, ratchet, retirement)",
        "▸ WACC + risk premia",
        "▸ WACC component memos (not used in formulas)",
        "▸ Wright's Law learning rates",
        "▸ Wright's Law parameters",
        "▸ Year-row cost curves",
    }
)

LABELS_BY_SHEET: Final[dict[str, tuple[str, ...]]] = {
    "AI Stack": (
        "INPUTS FROM CENTRAL ALLOCATOR",
        "Capital Allocation ($mm)",
        "Starship Capacity Allocation (kg-to-LEO)",
        "Total Capital Available ($mm)",
        "CENTRAL ALLOCATOR OUTPUTS",
        "Total Revenue ($mm)",
        "Module EBITDA ($mm)",
        "Module EBITDA Margin %",
        "Module FCF ($mm)",
        "Module CapEx ($mm)",
        "Capital deployed ($mm)",
        "Spot IRR",
        "Forward IRR (Y+2)",
        "Blended IRR",
        "Capacity Demand (kg-to-LEO)",
    ),
    "Allocator": (
        "Starting cash position EoY 2024 ($mm)",
        "IPO injection this year ($mm)",
        "Prior-year Group FCF read ($mm)",
        "Cash BoY ($mm)",
        "OpEx claim ($mm)",
        "Corporate CapEx claim ($mm)",
        "Spectrum CapEx claim ($mm)",
        "Taxes claim ($mm)",
        "Mars/Moon carve-out claim ($mm)",
        "Vehicle build claim ($mm)",
        "Year-N non-module claims ($mm)",
        "Available cash for IRR queue ($mm)",
        "Mars carve-out % of prior-year Group FCF (input)",
        "Mars carve-out floor ($mm/yr) (input)",
        "Prior-year Group FCF read ($mm/yr)",
        "Mars/Moon strategic carve-out ($mm/yr)",
        "Lunar share of carve-out (% — year-row)",
        "Mars share of carve-out (% — year-row)",
        "▸ Customer Launch (in-queue module)",
        "Customer Launch Blended IRR",
        "Customer Launch cash demand ($mm)",
        "Customer Launch cash demand large default ($mm)",
        "Customer Launch revenue trajectory stub ($mm)",
        "Customer Launch external Starship kg demand stub (kg)",
        "Customer Launch external Starship launches stub",
        "Customer Launch weight",
        "Customer Launch proposed allocation ($mm)",
        "▸ Starlink V2 BB",
        "Starlink V2 BB Blended IRR",
        "Starlink V2 BB cash demand ($mm)",
        "Starlink V2 BB weight",
        "Starlink V2 BB proposed allocation ($mm)",
        "▸ Starlink V2 DTC",
        "Starlink V2 DTC Blended IRR",
        "Starlink V2 DTC cash demand ($mm)",
        "Starlink V2 DTC weight",
        "Starlink V2 DTC proposed allocation ($mm)",
        "▸ Starlink V3 BB",
        "Starlink V3 BB Blended IRR",
        "Starlink V3 BB cash demand ($mm)",
        "Starlink V3 BB weight",
        "Starlink V3 BB proposed allocation ($mm)",
        "▸ Starlink V3 DTC",
        "Starlink V3 DTC Blended IRR",
        "Starlink V3 DTC cash demand ($mm)",
        "Starlink V3 DTC weight",
        "Starlink V3 DTC proposed allocation ($mm)",
        "▸ ODC (in-queue module)",
        "ODC Blended IRR",
        "ODC cash demand ($mm)",
        "ODC weight",
        "ODC proposed allocation ($mm)",
        "▸ AI Stack (in-queue module)",
        "AI Stack Blended IRR",
        "AI Stack cash demand ($mm)",
        "AI Stack weight",
        "AI Stack proposed allocation ($mm)",
        "Σ cash weights (denominator for shares)",
        "Customer Launch cash allocation",
        "Starlink cash allocation",
        "ODC cash allocation",
        "AI Stack cash allocation",
        "Lunar Mars cash allocation",
        "Starlink V2 BB cash allocation",
        "Starlink V2 DTC cash allocation",
        "Starlink V3 BB cash allocation",
        "Starlink V3 DTC cash allocation",
        "Total Starship capacity (kg-to-LEO)",
        "Lunar Mars kg reserved (off-the-top)",
        "Capacity available for IRR queue (kg-to-LEO)",
        "▸ Customer Launch kg sub-block (external Starship demand)",
        "Customer Launch kg demand (kg-to-LEO)",
        "Customer Launch kg weight",
        "Customer Launch kg proposed allocation",
        "▸ Starlink V3 BB kg sub-block",
        "Starlink V3 BB kg demand (kg-to-LEO)",
        "Starlink V3 BB kg weight",
        "Starlink V3 BB kg proposed allocation",
        "▸ Starlink V3 DTC kg sub-block",
        "Starlink V3 DTC kg demand (kg-to-LEO)",
        "Starlink V3 DTC kg weight",
        "Starlink V3 DTC kg proposed allocation",
        "▸ ODC kg sub-block",
        "ODC kg demand (kg-to-LEO)",
        "ODC kg weight",
        "ODC kg proposed allocation",
        "▸ AI Stack kg sub-block (terrestrial — kg demand structurally 0)",
        "AI Stack kg demand (kg-to-LEO)",
        "AI Stack kg weight",
        "AI Stack kg proposed allocation",
        "Σ kg weights (denominator for shares)",
        "Customer Launch kg allocation",
        "Starlink V3 BB kg allocation",
        "Starlink V3 DTC kg allocation",
        "Starlink kg allocation",
        "ODC kg allocation",
        "AI Stack kg allocation",
        "Lunar Mars kg allocation",
        "Vehicle build lead time (years)",
        "Starlink forward kg demand at T+lead",
        "ODC forward kg demand at T+lead",
        "Customer Launch forward kg demand at T+lead",
        "Lunar Mars forward kg demand at T+lead",
        "Forward aggregate kg demand",
        "Projected capacity at T+lead (kg-to-LEO)",
        "Capacity gap (kg-to-LEO)",
        "Required launches (count)",
        "Required vehicles (count)",
        "Customer Launch Spot IRR",
        "Customer Launch Forward IRR (Y+2)",
        "Starlink Spot IRR",
        "Starlink Forward IRR (Y+2)",
        "Starlink Blended IRR",
        "ODC Spot IRR",
        "ODC Forward IRR (Y+2)",
        "AI Stack Spot IRR",
        "AI Stack Forward IRR (Y+2)",
        "Lunar Mars Blended IRR (hardcoded 0 per Architecture §11.6)",
    ),
    "Assumptions": (
        "Tax rate (corporate, US federal + state blended)",
        "TAM inflation rate (annual)",
        "GNI per capita growth rate (annual)",
        "▸ Cash pool boundary inputs",
        "Starting cash position EoY 2024 ($mm)",
        "IPO injection amount ($mm)",
        "IPO injection year",
        "Pre-IPO debt facility ($mm)",
        "▸ Moon/Mars strategic carve-out (Vlad-confirmed MC-variable)",
        "Mars carve-out % of prior-year Group FCF",
        "Mars carve-out floor ($mm/yr)",
        "Mars carve-out uses prior-year FCF (0/1)",
        "▸ IRR engine + sigmoid blend parameters",
        "Sigmoid IRR-blend exponent k",
        "Forward IRR weight w (Blended = (1-w)·Spot + w·Forward)",
        "Forward IRR look-ahead horizon (years)",
        "MFW-IRR — Starlink economic life N (years)",
        "MFW-IRR — ODC economic life N (years)",
        "MFW-IRR — AI Stack economic life N (years)",
        "MFW-IRR — Customer Launch economic life clamp MIN (years)",
        "MFW-IRR — Customer Launch economic life clamp MAX (years)",
        "▸ Vehicle build claim (Spec 09 architecture)",
        "Vehicle build claim toggle (0=legacy mode, 1=forward-demand-sized non-module claim)",
        "Vehicle build lead time (years)",
        "Launches per Starship vehicle per year (cadence × variant blend, used for sizing)",
        "Vehicle masked-demand large default (sats; effectively uncapped)",
        "Forward aggregate kg demand growth cap (× current capacity)",
        "▸ Starship vehicle physical + cost parameters",
        "Super Heavy manufacturing cost ($mm/unit, base year)",
        "Starship 2nd-stage manufacturing cost ($mm/unit, base)",
        "Payload — booster-only mode (kg-to-LEO)",
        "Payload — fully reusable mode (kg-to-LEO)",
        "Lifetime reuses per ship (cap)",
        "Manufacturing learning rate (per doubling of cum units)",
        "▸ Starship cadence (Wright's Law on cum upmass)",
        "Base turnaround time per booster (years/flight)",
        "WL learning rate — turnaround vs cum upmass doubling",
        "Anchor year for cum-upmass Wright's Law",
        "Cadence ceiling (flights/booster/year)",
        "Max annual production growth rate (multiplier)",
        "▸ Starship time-varying inputs (year-rows)",
        "Variant mix (% fully reusable)",
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
        "F9 customer launch price ($mm/launch) — 2025 anchor",
        "Starship customer launch price ($mm/launch) — year-row",
        "Commercial launch market size ($mm/year) — year-row",
        "Government launch market size ($mm/year) — year-row",
        "SpaceX commercial market share % — year-row",
        "SpaceX government market share % — year-row",
        "Launch insurance % of external revenue",
        "Launch other COGS % of external revenue",
        "Customer Launch depreciation useful life (years)",
        "▸ Satellite physical",
        "V2 Mini Mass (kg)",
        "V3 Mass (kg)",
        "V2 Mini Bandwidth per Sat — BB (Gbps)",
        "V2 Mini Bandwidth per Sat — DTC (Gbps)",
        "V3 BB Bandwidth per Sat — base year (Gbps)",
        "V3 DTC Bandwidth per Sat (Gbps)",
        "Satellite useful life — V2 Mini (years)",
        "Satellite useful life — V3 (years)",
        "CapEx Lag (years)",
        "▸ Wright's Law parameters",
        "Satellite cost per kg — base year ($/kg)",
        "Satellite cost per kg — learning rate",
        "V3 bandwidth per sat — learning rate",
        "Cumulative sats at base year (end-2024)",
        "Satellite cost floor ($/kg)",
        "V3 bandwidth cap (Gbps)",
        "V2 Mini cost per kg — base year ($/kg)",
        "V2 Mini cost per kg — learning rate",
        "V2 Mini cost floor ($/kg)",
        "▸ Starshield (Vlad-corrected from Q4'25)",
        "Starshield Reserved % — start",
        "Starshield Reserved % — floor",
        "Starshield Reserved % — decay rate",
        "Starshield Rev per Gbps — base year ($/Gbps)",
        "Starshield Rev per Gbps — decay rate",
        "▸ Depreciation parameters",
        "Satellite Dep per kg — base year ($/kg/yr)",
        "Satellite Dep per kg — annual decay rate",
        "Facility CapEx per satellite — base year ($)",
        "Facility CapEx — learning rate",
        "▸ Constellation opening balances (Mach33 historical anchors — hard)",
        "V2 Mini BB Active Sats — end-2025",
        "V2 Mini DTC Active Sats — end-2025",
        "V2 Mini BB Bandwidth — end-2025 (Gbps)",
        "V2 Mini DTC Bandwidth — end-2025 (Gbps)",
        "Legacy V1/V1.5 Bandwidth — end-2025 (Gbps)",
        "V2 Mini BB Sats Launched 2025",
        "V2 Mini DTC Sats Launched 2025",
        "V3 BB Sats Launched 2025",
        "V3 DTC Sats Launched 2025",
        "Legacy V1/V1.5 Active Bandwidth (Gbps, year-row runoff)",
        "V2 Mini BB historical baseline (SoY 2025)",
        "V2 Mini DTC historical baseline (SoY 2025)",
        "▸ Deorbit parameters",
        "V2 Mini BB Deorbit Lag (years)",
        "V3 BB Deorbit Lag (years)",
        "V2 Mini DTC Deorbit Lag (years)",
        "V3 DTC Deorbit Lag (years)",
        "Bandwidth Removed per Deorbited V2 Mini BB Sat (Gbps)",
        "Bandwidth Removed per Deorbited V2 Mini DTC Sat (Gbps)",
        "Bandwidth Removed per Deorbited V3 BB Sat (Gbps)",
        "Bandwidth Removed per Deorbited V3 DTC Sat (Gbps)",
        "▸ Subscribers + ARPU + Terminals",
        "Starting BoY 2025 subscribers (millions)",
        "Broadband ARPU ($/sub/mo, year-row)",
        "DTC ARPU ($/sub/mo, year-row)",
        "Subsidy mix (% of net adds subsidized)",
        "Terminal retail price ($, non-subsidized)",
        "Terminal retail price ($, subsidized)",
        "Terminal COGS per unit ($)",
        "▸ BB/DTC market mix (Spec 09)",
        "BB market share % (Starlink revenue mix)",
        "DTC market share % (Starlink revenue mix)",
        "▸ Bandwidth flow to ODC (Spec 04 PLACEHOLDERS)",
        "Gbps per GWh/yr of ODC compute energy",
        "BB-share of ODC bandwidth claim",
        "▸ Starlink large-default cash + kg asks (Spec 09)",
        "Starlink kg ask year-row (large default, exceeds plausible capacity)",
        "Starlink cash ask year-row ($mm, large default)",
        "▸ Satellite & subsystem anchors (V2 Compute config)",
        "Compute power per sat (kW)",
        "Solar generation per sat (kW, gen requirement)",
        "Total sat dry mass (kg)",
        "F_ref — reference compute unit (TFLOPS, H100 FP8 dense)",
        "Effective Compute Ratio (ECR)",
        "Workload mix — % inference",
        "ODC fleet design life (years)",
        "Sat solar generation (W, for $/W subsystem cost)",
        "Sat thermal mass (kg)",
        "▸ Subsystem unit costs (per-sat, flat unless noted)",
        "Solar array unit cost ($/W)",
        "Thermal system unit cost ($/kg)",
        "Comms (ISL set) flat cost ($)",
        "ADCS + avionics flat cost ($)",
        "Structure flat cost ($)",
        "Battery flat cost ($)",
        "Shielding flat cost ($)",
        "Integration & Test flat cost ($)",
        "▸ Wright's Law learning rates",
        "LR — chips (per doubling)",
        "LR — subsystems (per doubling)",
        "Anchor year for ODC Wright’s Law",
        "▸ Revenue parameters",
        "Annual GPU-hr price deflation rate",
        "Ground station / network opex % of revenue",
        "ODC insurance % of revenue",
        "ODC other COGS % of revenue",
        "▸ Chip roadmap (year-rows, H100 → AI5 → Dojo-3)",
        "Chip TDP per chip (W) — year-row",
        "Chip FP8 performance per chip (TFLOPS) — year-row",
        "Chip mass per chip (kg) — year-row",
        "Chip cost per chip ($) — year-row",
        "Price per H100-equiv GPU-hr ($) — year-row",
        "Utilization % (fleet ramp) — year-row",
        "▸ Dual revenue model (Sprint 3.5)",
        "Credence on Model A (Pr(A))",
        "CoreWeave baseline anchor ($B/GW_IT/yr, 2026)",
        "PUE_base (terrestrial colo)",
        "Orbital PUE",
        "Terrestrial price deflation %/yr (Model A baseline year-row driver)",
        "Steady-state utilization (for Model A util-adjustment ratio)",
        "▸ ODC internal vs external compute split (NEW per Vlad's framing)",
        "ODC internal compute share to AI Stack % — year-row",
        "ODC external compute share to customers % — year-row",
        "▸ Cursor (orchestration)",
        "Cursor paid seats (millions) — year-row",
        "Cursor avg subscription price ($/seat/mo)",
        "Cursor enterprise API rev per seat ($/year)",
        "▸ Grok consumer (X Premium / Grok Premium)",
        "Grok consumer paid subs (millions) — year-row",
        "Grok consumer ARPU ($/user/year)",
        "▸ Grok enterprise (API)",
        "Grok enterprise API token volume (T tokens/year) — year-row",
        "Grok enterprise API price ($/Mtoken) — year-row",
        "▸ AI Stack operating parameters",
        "AI Stack insurance % of revenue",
        "AI Stack other COGS % of revenue",
        "▸ Module-wide parameters",
        "Capital lifetime — book value straight-line depreciation (years)",
        "Module operating cost — Lunar (% of Lunar CapEx)",
        "Module operating cost — Mars (% of Mars CapEx)",
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
        "Labour unit cost ($/unit) — declining curve",
        "Hardware replacement cost factor ($/kg landed) — declining",
        "▸ Lunar / Mars share of carve-out cash (derived deployment)",
        "Lunar share of Mars/Moon carve-out cash — year-row",
        "Mars share of carve-out cash — year-row",
        "▸ R&D by module (start% / end% / CAGR taper per Spec 03 §2.2)",
        "Starlink R&D — start % of (Starlink + Starshield) rev",
        "Starlink R&D — end-state % (floor)",
        "Starlink R&D — CAGR (taper)",
        "Customer Launch R&D — start % of external rev",
        "Customer Launch R&D — end-state % (floor)",
        "Customer Launch R&D — CAGR (taper)",
        "ODC R&D — start % of ODC rev",
        "ODC R&D — end-state % (floor)",
        "ODC R&D — CAGR (taper)",
        "AI Stack R&D — start % of AI Stack rev",
        "AI Stack R&D — end-state % (floor)",
        "AI Stack R&D — CAGR (taper)",
        "▸ R&D — Moon/Mars ($-profile year-row, pre-revenue)",
        "R&D — Moon/Mars ($mm/yr) — year-row",
        "▸ SG&A by function",
        "Sales & Marketing — start % of (Starlink+Starshield+Customer Launch ext) rev",
        "Sales & Marketing — end-state % (floor)",
        "Sales & Marketing — CAGR (taper)",
        "General & Administrative — start % of group rev",
        "General & Administrative — end-state % (ceiling)",
        "General & Administrative — CAGR (drift)",
        "Customer Service — flat % of Starlink subscription rev",
        "Other corporate operating — flat % of group rev",
        "▸ Corporate facilities CapEx ($mm/yr)",
        "HQ buildings CapEx ($mm/yr, flat)",
        "Corporate IT CapEx ($mm/yr, flat)",
        "General engineering facilities CapEx ($mm/yr, flat)",
        "Other corporate CapEx ($mm/yr, flat)",
        "▸ Corporate useful lives",
        "HQ buildings useful life (years)",
        "Corporate IT useful life (years)",
        "General engineering facilities life (years)",
        "Other corporate useful life (years)",
        "▸ Corporate historical capital base",
        "Corporate historical capital base ($mm)",
        "▸ EchoStar spectrum (Spec 03 §5)",
        "EchoStar mid-band CapEx ($mm) — year-row",
        "Spectrum useful life (years)",
        "▸ WACC + risk premia",
        "Group WACC",
        "Risk premium — Starlink (over group WACC)",
        "Risk premium — Customer Launch",
        "Risk premium — ODC",
        "Risk premium — AI Stack",
        "Risk premium — Lunar / Mars",
        "▸ WACC component memos (not used in formulas)",
        "Cost of equity (memo)",
        "Cost of debt (memo)",
        "Leverage E/V (memo)",
        "▸ Terminal value parameters",
        "Terminal growth rate g (group + most modules)",
        "Starlink — exit revenue multiple",
        "Lunar / Mars — terminal BV multiplier",
        "Starship D&A useful life — memo add-back for Launch standalone DCF",
        "Terminal FCF averaging window (years pre-2050)",
        "▸ Comparables anchors ($B)",
        "Comp anchor — Group EV (Morgan Stanley public)",
        "Comp anchor — Group EV (Brant internal)",
        "Comp anchor — Starlink standalone (Bernstein/JPM)",
        "Comp anchor — ODC standalone (CoreWeave-anchored)",
        "Comp anchor — Customer Launch standalone (Rocket Lab)",
        "Comp anchor — AI Stack standalone",
        "Comp anchor — Lunar / Mars (NASA HLS lifetime)",
        "▸ SoTP multiples (EV/Revenue at 2050)",
        "Multiple — Customer Launch (EV/Rev at 2050)",
        "Multiple — Starlink (EV/Rev at 2050)",
        "Multiple — ODC (EV/Rev at 2050)",
        "Multiple — AI Stack (EV/Rev at 2050)",
        "Multiple — Lunar / Mars (anchor stub, $B)",
        "F9 retirement rate (% of launches/year)",
        "Starship manufacturing cost anchor ($mm/stack, 2024 baseline)",
        "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)",
        "Starship cost WL anchor cum units (= cum stacks at end-2024 baseline)",
        "Starship ops + fuel + refurb cost anchor ($mm/launch, 2024 baseline)",
        "Starship ops + fuel + refurb WL learning rate (% reduction per doubling cum stacks)",
        "Starship booster share of manufacturing cost (% of stack mfg)",
        "Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)",
        "Starship payload — 2030 anchor (kg-to-LEO, fully reusable mode)",
        "Starship payload — max cap (kg-to-LEO)",
        "Starship payload — booster-only mode delta (kg, additive to fully-reusable payload)",
        "Total customer launch market (launches/yr) — 2025 anchor",
        "Total customer launch market CAGR (% growth/yr)",
        "Starship customer launch margin — 2027 anchor (multiplier on at-cost rate)",
        "Starship customer launch margin — 2050 terminal (multiplier on at-cost rate, floor)",
        "V3 BB first launch year",
        "V3 DTC first launch year",
        "V2 DTC permanent cap flag — RETIRED 2026-05-26 (replaced by V2 phase-out year R350 per §20.6 Architecture amendments)",
        "Starlink ground ops % of revenue",
        "Starlink insurance % of revenue",
        "Starlink other COGS % of revenue",
        "V3 BB launches per year stub trajectory",
        "V3 DTC launches per year stub trajectory",
        "Sats per F9 launch — V2 BB",
        "Sats per F9 launch — V2 DTC",
        "Sats per Starship launch — V3 BB",
        "Sats per Starship launch — V3 DTC",
        "ODC cash demand large default ($mm)",
        "ODC kg demand large default (kg)",
        "Legacy V1/V1.5 D&A baseline ($mm, 2025 anchor)",
        "Legacy V1/V1.5 D&A useful life (yrs)",
        "Facility D&A — sat manufacturing + ground stations ($mm/yr, flat)",
        "V3 BB Wright’s Law anchor — cum sats",
        "V3 BB bandwidth-per-sat Wright’s Law learning rate (per doubling)",
        "Starship LEO payload per launch — Compute config (kg)",
        "Lunar labour share of surface payload — year-row",
        "Mars labour share of surface payload — year-row",
        "First mission year (Lunar Mars)",
        "Starship customer launch margin — CAGR (% change/yr from 2027 anchor)",
        "ODC R&D $-profile ($mm/yr) — year-row",
        "AI Stack R&D $-profile ($mm/yr) — year-row",
        "▸ Annual TAM growth — inflation + real GNI components",
        "Inflation rate (% per year)",
        "Real GNI growth rate (% per year)",
        "V2 phase-out year (no V2 BB / V2 DTC launches from this year)",
    ),
    "CapEx": (
        "CAPEX -- module CapEx aggregation + corporate CapEx + spectrum CapEx + corporate D&A. Sprint 8 fills.",
        "Customer Launch Module CapEx ($mm)",
        "Starlink Module CapEx ($mm)",
        "ODC Module CapEx ($mm)",
        "AI Stack Module CapEx ($mm)",
        "Lunar Mars Module CapEx ($mm)",
        "Total Module CapEx ($mm)",
        "HQ buildings CapEx ($mm)",
        "Corporate IT CapEx ($mm)",
        "General engineering facilities CapEx ($mm)",
        "Other corporate CapEx ($mm)",
        "Total Corporate CapEx ($mm)",
        "Cumulative HQ CapEx ($mm)",
        "Cumulative IT CapEx ($mm)",
        "Cumulative Gen eng CapEx ($mm)",
        "Cumulative Other CapEx ($mm)",
        "HQ D&A ($mm)",
        "IT D&A ($mm)",
        "Gen eng D&A ($mm)",
        "Other D&A ($mm)",
        "Total Corporate D&A ($mm)",
        "EchoStar mid-band CapEx ($mm)",
        "Cumulative spectrum intangible ($mm)",
        "Annual spectrum amortization ($mm)",
        "Vehicle build claim ($mm)",
        "Total Group CapEx ($mm)",
        "Memo: Sprint 8 Group D&A contribution (Corporate D&A + Spectrum amort)",
    ),
    "Customer Launch": (
        "INPUTS FROM CENTRAL ALLOCATOR",
        "Capital Allocation ($mm)",
        "Starship Capacity Allocation (kg-to-LEO)",
        "Total Capital Available ($mm)",
        "CUSTOMER LAUNCH — MODULE BODY",
        "▸ Demand mechanic (total market + F9 vs Starship split via IRR + capacity)",
        "Total customer launch market (launches/yr)",
        "Starship customer launch margin multiplier (year-row)",
        "F9 customer launch price ($mm/launch)",
        "Starship customer launch price ($mm/launch)",
        "Starship Total Annual Capacity (kg-to-LEO) — from Launch Capacity",
        "Per-launch upmass (kg) — from Launch Capacity",
        "Starship internal kg demand (post-Starlink + ODC + AI Stack)",
        "Starship capacity available for customer launches (kg)",
        "Starship customer launches per year",
        "F9 customer launches per year",
        "▸ F9 customer launches — economics",
        "F9 customer revenue ($mm)",
        "F9 variable cost per launch ($mm) — read from Launch Capacity",
        "F9 D&A share per launch ($mm) — read from Launch Capacity",
        "F9 at-cost rate ($mm/launch) — read from Launch Capacity",
        "F9 customer launch insurance + other COGS ($mm/launch)",
        "▸ Starship customer launches — economics",
        "Starship customer revenue ($mm)",
        "Starship ops + fuel + refurb cost per launch ($mm) — read from Launch Capacity",
        "Starship D&A share per launch ($mm) — read from Launch Capacity",
        "Starship at-cost rate ($mm/launch) — read from Launch Capacity",
        "Starship customer launch insurance + other COGS ($mm/launch)",
        "▸ Internal transfer revenue (launch services to Sprint 4/5/6 consumers)",
        "F9 internal launches (BB + DTC)",
        "Starship internal launches (V3 BB + V3 DTC + ODC + AI Stack)",
        "Customer Launch internal transfer revenue ($mm)",
        "▸ Module P&L (vending-machine: Revenue → COGS → Module EBITDA → CapEx → FCF)",
        "Total Revenue ($mm)",
        "▸ COST OF GOODS SOLD ($mm)",
        "F9 variable cost ($mm)",
        "F9 D&A share ($mm)",
        "Starship variable cost ($mm)",
        "Starship D&A share ($mm)",
        "Customer Launch ground ops ($mm)",
        "Customer Launch insurance ($mm)",
        "Customer Launch other COGS ($mm)",
        "Total COGS ($mm)",
        "Gross Profit ($mm)",
        "Module EBITDA ($mm)",
        "Module EBITDA Margin %",
        "▸ CAPEX + FCF",
        "Module CapEx ($mm)",
        "Module D&A ($mm) — informational (also in COGS rows 86 + 88)",
        "Module FCF ($mm)",
        "Capital deployed ($mm)",
        "▸ Per-launch marginal IRR engines (F9 + Starship, external customer only)",
        "F9 lifetime reuses per booster — read from Assumptions",
        "F9 IRR cashflow stream period count N (clamped at R23 MAX)",
        "Starship lifetime reuses per booster — year-row from Launch Capacity R21",
        "Starship IRR cashflow stream period count N (clamped at R23 MAX, year-row)",
        "F9 per-launch cost slug ($mm — t=0 capex)",
        "F9 per-launch annual margin ($mm/yr — cadence × per-launch margin)",
        "F9 Spot IRR (per-launch marginal IRR, current year — external customer economics)",
        "F9 Forward IRR (Y+2) — per-launch marginal IRR, year T+2 cashflow",
        "F9 per-launch Blended IRR (external customer economics)",
        "Starship per-launch cost slug ($mm — year-row of manufacturing cost from Launch Capacity R37)",
        "Starship per-launch annual margin ($mm/yr — cadence × per-launch margin)",
        "Starship Spot IRR",
        "Starship Forward IRR (Y+2)",
        "Starship per-launch Blended IRR (external customer economics)",
        "▸ Memo: 2025 calibration anchors + diagnostic checks",
        "Memo: F9 customer launches 2025",
        "Memo: F9 customer revenue 2025 (target $4,290M ±5%)",
        "Memo: Starship customer revenue 2025 (target $0 exact)",
        "Memo: 2025 calibration PASS/CHECK",
        "CENTRAL ALLOCATOR OUTPUTS",
        "Spot IRR",
        "Forward IRR (Y+2)",
        "Blended IRR",
        "Capacity Demand (kg-to-LEO)",
    ),
    "Demand Curves": (
        "Demand Curves",
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
        "▸ Curve evaluators (year-row, read by Starlink module)",
        "Annual TAM shift multiplier",
        "Starlink BB capacity input (Gbps)",
        "Starlink DTC capacity input (Gbps)",
        "Starlink BB Revenue from curve ($mm)",
        "Starlink DTC Revenue from curve ($mm)",
    ),
    "Group P&L": (
        "GROUP P&L -- consolidated Revenue / EBITDA / D&A / EBIT / Taxes / NOPAT / CapEx / FCF + inter-module eliminations + conservation block. Sprint 9 fills the P&L walk above row 99.",
        "Σ Module revenue (gross, pre-elim) ($mm)",
        "GROUP REVENUE NET OF ELIMS ($mm)",
        "Σ Module COGS (gross, pre-elim) ($mm)",
        "Group COGS (net of elims) ($mm)",
        "Group Gross Profit ($mm)",
        "Total OpEx ($mm)",
        "Memo: Starlink Constellation D&A in Starlink COGS ($mm)",
        "Memo: Customer Launch Module D&A in COGS ($mm)",
        "Memo: ODC sat D&A in COGS ($mm)",
        "Group EBITDA ($mm)",
        "Group D&A ($mm)",
        "Group EBIT ($mm)",
        "Taxes ($mm)",
        "NOPAT ($mm)",
        "Memo: Σ Module D&A in COGS ($mm)",
        "Memo: Corporate D&A ($mm)",
        "Memo: Spectrum amort ($mm)",
        "Total D&A add-back ($mm)",
        "Internal launch services eliminated ($mm)",
        "Internal bandwidth eliminated ($mm)",
        "Internal compute eliminated ($mm)",
        "Total Group CapEx ($mm)",
        "Mars/Moon strategic carve-out ($mm)",
        "GROUP FCF ($mm)",
        "Revenue check",
        "EBITDA check",
        "CapEx check",
        "FCF check",
        "D&A check",
        "EBIT consistency",
        "Launch services elimination conservation",
        "Bandwidth elimination conservation",
        "Compute elimination conservation",
        "ALL OK boolean",
        "Cash flow identity check ($mm — Starting + ΣIPO + ΣFCF − Cash EoY)",
        "Memo: Σ Module FCF reconciliation residual ($mm)",
        "Memo: Group Revenue 2025 target ($mm) — revised",
        "Memo: Group Revenue 2025 delta (%)",
        "Memo: Group Gross Profit 2025 target ($mm) — REVISED",
        "Memo: Group Gross Profit 2025 delta (%)",
        "Memo: Group EBITDA 2025 target ($mm) — REVISED",
        "Memo: Group EBITDA 2025 delta (%)",
        "Memo: Group D&A 2025 target ($mm) — REVISED",
        "Memo: Group D&A 2025 delta (%)",
        "Memo: Group FCF 2025 target ($mm) — REVISED",
        "Memo: Group FCF 2025 delta (%)",
        "Memo: Q4'25 Group EBITDA original target ($mm) — archaeology",
        "Memo: Q4'25 Group FCF original target ($mm) — archaeology",
        "Memo: Total OpEx 2025 (read from OpEx tab)",
        "Memo: Total Group CapEx 2025 (read from CapEx tab)",
    ),
    "Launch Capacity": (
        "STARSHIP — VEHICLE SUPPLY",
        "▸ Physical + cost parameters (from Assumptions §3)",
        "Super Heavy manufacturing cost ($mm/unit)",
        "Starship 2nd-stage manufacturing cost ($mm/unit)",
        "Payload — booster-only mode (kg-to-LEO)",
        "Payload — fully reusable mode (kg-to-LEO)",
        "Lifetime reuses per ship (cap)",
        "Manufacturing learning rate (per doubling of cum units)",
        "Cadence ceiling (flights/booster/year)",
        "WL learning rate — turnaround vs cum upmass doubling",
        "Anchor year for cum-upmass Wright's Law",
        "▸ Variant mix + booster lifetime reuses (year-rows from Assumptions §3)",
        "Variant mix (% fully reusable)",
        "Lifetime reuses per booster (year cap)",
        "Launches per Starship vehicle per year (cadence)",
        "Booster fleet beginning-of-year (units)",
        "Boosters built per year (units)",
        "Boosters retired per year (units)",
        "Booster fleet end-of-year (units)",
        "Cum upmass to date (kg)",
        "Per-launch upmass (kg)",
        "Cum Starship stacks manufactured (end-of-year, units)",
        "Booster-only launches per year (count)",
        "Fully-reusable launches per year (count)",
        "Total Starship launches per year",
        "Total Annual Capacity (kg-to-LEO)",
        "▸ Starship at-cost transfer rate (Architecture §7.1)",
        "Starship manufacturing cost ($mm/stack, this year)",
        "Starship ops + fuel + refurb cost per launch ($mm, this year)",
        "Starship D&A share per launch, fully reusable mode ($mm)",
        "Starship at-cost rate ($mm/launch)",
        "Memo: Starship at-cost rate, ship-expended mode (Moon/Mars, $mm/launch)",
        "FALCON 9 — VEHICLE SUPPLY",
        "F9 booster (1st stage) mfg cost ($mm/unit)",
        "F9 2nd stage mfg cost ($mm/unit)",
        "F9 fairing cost net of 75% recovery ($mm/flight)",
        "F9 per-launch ops cost ($mm)",
        "F9 booster refurb % of mfg",
        "F9 payload to LEO (kg)",
        "F9 lifetime reuses per booster",
        "F9 cadence per booster (flights/year, flat)",
        "F9 WL learning rate",
        "▸ F9 supply mechanic (pre-V3-trigger anchors + post-trigger decay)",
        "F9 base booster build rate (boosters/year, pre-V3-trigger)",
        "V3 Starlink launch trigger year",
        "F9 build-rate decay window (years)",
        "F9 starting fleet at 2025 SoY (boosters)",
        "F9 fleet beginning-of-year (boosters)",
        "F9 manufactured per year (units) — V3-trigger-aware decay note: D61/E61 historical anchors preserved (Sprint 11 Decision A; full IF-bifurcated form deferred to Sprint 12)",
        "F9 retired per year (boosters)",
        "F9 fleet end-of-year (boosters)",
        "F9 launches per year",
        "F9 cadence-utilization per booster (memo, derived)",
        "▸ F9 capacity + at-cost transfer rate",
        "F9 Annual Capacity (kg-to-LEO)",
        "F9 variable cost per launch ($mm)",
        "F9 booster D&A share per launch ($mm)",
        "F9 at-cost rate ($mm/launch)",
        "BLENDED COST STACK + CALIBRATION",
        "Total launches per year (all vehicles)",
        "Total upmass per year (kg)",
        "Total launch CapEx per year ($mm) — variable + amortized D&A",
        "Blended $/kg",
        "Memo: 2025 calibration anchors (read-only diagnostics)",
        "Memo: 2025 calibration status",
    ),
    "Lunar Mars": (
        "INPUTS FROM CENTRAL ALLOCATOR",
        "Capital Allocation ($mm)",
        "Starship Capacity Allocation (kg-to-LEO)",
        "Total Capital Available ($mm)",
        "CARVE-OUT CASH INFLOW (Architecture §11.1 — read from Allocator §3)",
        "Total Mars/Moon strategic carve-out ($mm/yr)",
        "Lunar share of carve-out (% — year-row)",
        "Mars share of carve-out (% — year-row)",
        "Lunar cash allocation ($mm)",
        "Mars cash allocation ($mm)",
        "PER-SHIP COST BUILD (Architecture §11.2)",
        "Starship vehicle cost amortized ($mm/ship)",
        "Lunar depot multiplier (×)",
        "Mars depot multiplier (×)",
        "Lunar payload per surface ship (kg)",
        "Mars payload per surface ship (kg)",
        "Hardware $/kg landed (year-row)",
        "Lunar payload value ($mm/ship)",
        "Mars payload value ($mm/ship)",
        "Per-ship cost — Lunar ($mm)",
        "Per-ship cost — Mars ($mm)",
        "LUNAR MISSION DEPLOYMENT (Architecture §11.2)",
        "Lunar surface missions deployed (count)",
        "Lunar total vehicle launches (count)",
        "Lunar surface payload mass (kg landed)",
        "Lunar labour share this year (%)",
        "Lunar labour mass landed (kg)",
        "Lunar hardware mass landed (kg)",
        "MARS MISSION DEPLOYMENT (Architecture §11.2)",
        "Mars surface missions deployed (count)",
        "Mars total vehicle launches (count)",
        "Mars surface payload mass (kg landed)",
        "Mars labour share this year (%)",
        "Mars labour mass landed (kg)",
        "Mars hardware mass landed (kg)",
        "KG RESERVATION OFF-THE-TOP (Architecture §11.3 + §6.4)",
        "Starship LEO payload per launch (kg)",
        "Lunar total launches × LEO payload (kg)",
        "Mars total launches × LEO payload (kg)",
        "Lunar Mars total kg reserved off-top (kg-to-LEO)",
        "BV ENGINE INPUTS (Architecture §11.4 — labour units + hardware)",
        "Labour unit mass (kg)",
        "Labour unit useful life (yrs)",
        "Labour unit base hourly output ($/hr)",
        "Labour unit daily working hours",
        "Labour unit productivity factor",
        "Labour unit productivity learning rate (%/yr)",
        "Labour annual output per unit base year ($mm/yr)",
        "Productivity multiplier (year-row, anchor-and-offset)",
        "Labour annual output per unit this year ($mm/yr)",
        "LUNAR labour units landed (count this year)",
        "MARS labour units landed (count this year)",
        "LUNAR labour units retired this year (cohort lookback)",
        "MARS labour units retired this year (cohort lookback)",
        "LUNAR active labour fleet EoY (running sum, net retirements)",
        "MARS active labour fleet EoY (running sum, net retirements)",
        "BV ENGINE OUTPUT (Architecture §11.4)",
        "Capital lifetime — book value straight-line dep (yrs)",
        "LUNAR annual production output ($mm/yr)",
        "MARS annual production output ($mm/yr)",
        "LUNAR annual hardware value add ($mm/yr)",
        "MARS annual hardware value add ($mm/yr)",
        "LUNAR annual BV contribution ($mm/yr)",
        "MARS annual BV contribution ($mm/yr)",
        "LUNAR accumulated book value (year)",
        "MARS accumulated book value (year)",
        "Total Lunar + Mars accumulated BV ($mm)",
        "LUNAR MARS P&L (Architecture §11.5)",
        "Total Revenue ($mm)",
        "Mission ops cost — Lunar ($mm)",
        "Mission ops cost — Mars ($mm)",
        "Memo: BV decay — Lunar ($mm/yr) — Valuation input only, NOT in Group D&A",
        "Memo: BV decay — Mars ($mm/yr) — Valuation input only, NOT in Group D&A",
        "Total COGS ($mm)",
        "Lunar Mars Module D&A ($mm)",
        "Gross Profit ($mm)",
        "Module EBITDA ($mm)",
        "Module EBITDA Margin %",
        "Module CapEx ($mm)",
        "Capital deployed ($mm)",
        "Module D&A add-back ($mm)",
        "Module FCF ($mm)",
        "MEMO: DIAGNOSTICS",
        "Memo: Total carve-out reserved this year ($mm)",
        "Memo: Carve-out vs Module CapEx gap ($mm)",
        "Memo: Lunar surface missions cumulative",
        "Memo: Mars surface missions cumulative",
        "Memo: Total Lunar + Mars vehicle launches this year",
        "Memo: Lunar labour annual output ($mm/yr)",
        "Memo: Mars labour annual output ($mm/yr)",
        "CENTRAL ALLOCATOR OUTPUTS",
        "Spot IRR",
        "Forward IRR (Y+2)",
        "Blended IRR",
        "Capacity Demand (kg-to-LEO)",
        "Lunar Accumulated Book Value ($mm)",
        "Mars Accumulated Book Value ($mm)",
    ),
    "ODC": (
        "INPUTS FROM CENTRAL ALLOCATOR",
        "Capital Allocation ($mm)",
        "Starship Capacity Allocation (kg-to-LEO)",
        "Total Capital Available ($mm)",
        "ODC SAT PHYSICAL & COST STACK",
        "Compute power per sat (kW)",
        "Total sat dry mass (kg)",
        "Sat solar generation (W)",
        "Sat thermal mass (kg)",
        "F_ref — reference compute unit (TFLOPS, H100 FP8)",
        "Effective Compute Ratio (ECR)",
        "ODC fleet design life (years)",
        "▸ Chip roadmap reads (year-rows)",
        "Chip TDP per chip (W) — year-row",
        "Chip FP8 per chip (TFLOPS) — year-row",
        "Chip mass per chip (kg) — year-row",
        "Chip cost per chip ($) — year-row",
        "Price per H100-equiv GPU-hr ($) — year-row",
        "Utilization % (fleet ramp) — year-row",
        "Chips per sat",
        "Sat PFLOPS (FP8, per sat per year computed)",
        "Sat chip mass (kg)",
        "▸ Subsystem unit costs + Wright's Law",
        "Solar array cost per sat ($, pre-WL)",
        "Thermal system cost per sat ($, pre-WL)",
        "Comms (ISL set) cost per sat ($, pre-WL)",
        "ADCS + avionics cost per sat ($, pre-WL)",
        "Structure cost per sat ($, pre-WL)",
        "Battery cost per sat ($, pre-WL)",
        "Shielding cost per sat ($, pre-WL)",
        "Integration & Test cost per sat ($, pre-WL)",
        "Sat subsystem cost (pre-WL, $)",
        "Cum ODC sats deployed (running sum) — Rule 23 exception, intentional",
        "Wright's Law multiplier on subsystems (year-row)",
        "Cum ODC sats at WL anchor year",
        "Sat subsystem cost (with WL, $) — year-row",
        "Chip cost per sat ($) — year-row",
        "Sat total cost ($, year-row)",
        "Sat total cost ($mm, year-row)",
        "LAUNCH SERVICES (paid to Launch Capacity at fully-allocated at-cost rate)",
        "Sats per Starship launch (Compute config)",
        "Starship at-cost rate ($mm/launch) — read from Launch Capacity",
        "Launch services cost per sat ($mm)",
        "ODC Starship launches (internal)",
        "ODC Starship kg demand",
        "DEPLOYMENT, FLEET RAMP, CASH/KG DEMAND PUBLISH",
        "ODC cash demand large default ($mm) — Assumptions read",
        "ODC kg demand large default (kg) — Assumptions read",
        "Cash demand year-row published ($mm) — masked by Blended IRR > 0",
        "Kg demand year-row published (kg) — masked by Blended IRR > 0",
        "Wanted sats deployed (uncapped, cash-derived)",
        "Sats deployable from cash allocation",
        "Sats deployable from kg allocation",
        "Sats deployed (actual)",
        "Sat retirements (year-row, N-year cohort linear)",
        "Active sat fleet EoY (year-chained, Rule 23 exception)",
        "Fleet PFLOPS (FP8)",
        "Fleet compute power (GW)",
        "Fleet annual PFLOP-hrs delivered (util-adjusted)",
        "BANDWIDTH CLAIM & SERVICES COST (paid to Starlink at fully-allocated at-cost rate)",
        "Gbps per GWh/yr ODC compute energy conversion factor",
        "BB-share of ODC bandwidth claim",
        "Fleet ODC compute energy delivered (GWh/yr)",
        "Total ODC Gbps demand",
        "ODC BB Gbps demand",
        "ODC DTC Gbps demand",
        "BB pool at-cost rate ($/Gbps/yr) — read from Starlink Capacity",
        "DTC pool at-cost rate ($/Gbps/yr) — read from Starlink Capacity",
        "ODC BB bandwidth cost ($mm/yr)",
        "ODC DTC bandwidth cost ($mm/yr)",
        "Bandwidth services cost ($mm)",
        "DUAL REVENUE MODEL (Pr(A) × Model A + Pr(B) × Model B; Architecture §9.2)",
        "CoreWeave baseline ($B/GW_IT/yr, 2026 anchor)",
        "Terrestrial price deflation %/yr",
        "Adjusted CoreWeave baseline year-row ($B/GW_IT/yr)",
        "PUE uplift (orbital advantage = PUE_base / PUE_orbital)",
        "Steady-state utilization",
        "Per-sat Model A revenue ($mm/yr) — energy-anchored",
        "Per-sat billable H100-equiv GPU-hrs/yr",
        "Per-sat Model B revenue ($mm/yr) — η-anchored",
        "Pr(A) (Architecture §9.2)",
        "Per-sat Expected Revenue ($mm/yr) — Pr-A-weighted",
        "Internal compute share to AI Stack % — year-row",
        "External compute share to customers % — year-row",
        "Per-sat external compute revenue ($mm/yr) — at market",
        "Fleet external compute revenue ($mm/yr)",
        "ODC FULLY-ALLOCATED COST + AT-COST COMPUTE RATE (Architecture §7.3)",
        "Annual sat D&A ($mm/yr)",
        "Annual launch services cost ($mm/yr)",
        "Annual bandwidth services cost ($mm/yr)",
        "Annual insurance cost ($mm/yr)",
        "Annual other COGS ($mm/yr)",
        "Annual ground ops cost ($mm/yr)",
        "Total fully-allocated ODC cost ($mm/yr)",
        "ODC at-cost compute rate ($/PFLOP-hr)",
        "Internal compute PFLOP-hrs delivered to AI Stack",
        "Internal transfer revenue (at-cost compute) ($mm)",
        "MODULE P&L",
        "External compute revenue ($mm/yr)",
        "Internal transfer revenue (at-cost compute) ($mm/yr)",
        "Total Revenue ($mm)",
        "COGS — Constellation D&A ($mm)",
        "COGS — Launch services cost ($mm)",
        "COGS — Bandwidth services cost ($mm)",
        "COGS — Ground ops ($mm)",
        "COGS — Insurance ($mm)",
        "COGS — Other COGS ($mm)",
        "Total COGS ($mm)",
        "Gross Profit ($mm)",
        "Module EBITDA ($mm)",
        "Module EBITDA Margin %",
        "Module CapEx ($mm)",
        "Capital deployed ($mm) — diagnostic",
        "Module FCF ($mm)",
        "PER-SAT MARGINAL IRR ENGINE (Architecture §9.4, reads external revenue only per §7.3)",
        "Per-sat upfront cost ($mm) — sat hardware + launch services per sat",
        "Per-sat ground ops cost ($mm/yr)",
        "Per-sat insurance cost ($mm/yr)",
        "Per-sat other COGS ($mm/yr)",
        "Per-sat bandwidth cost ($mm/yr)",
        "Per-sat BB Gbps demand",
        "Per-sat DTC Gbps demand",
        "Per-sat net marginal revenue ($mm/yr)",
        "Spot IRR",
        "Forward IRR (Y+2)",
        "Blended IRR",
        "CENTRAL ALLOCATOR OUTPUTS",
        "Capital deployed ($mm)",
        "Capacity Demand (kg-to-LEO)",
    ),
    "OpEx": (
        "OPEX -- corporate operating costs (R&D by module + SG&A by function). Sprint 8 fills.",
        "Starlink R&D — % of (Starlink + Starshield) rev",
        "Starlink R&D base — Starlink + Starshield rev ($mm)",
        "Starlink R&D ($mm)",
        "Customer Launch R&D — % of external rev",
        "Customer Launch R&D base — Customer Launch external rev ($mm)",
        "Customer Launch R&D ($mm)",
        "ODC R&D — % of ODC rev (bounded-CAGR)",
        "ODC R&D base — ODC rev ($mm)",
        "ODC R&D $-profile ($mm, pre-revenue floor)",
        "ODC R&D ($mm) — MAX($-profile, % × rev)",
        "AI Stack R&D — % of AI Stack rev (bounded-CAGR)",
        "AI Stack R&D base — AI Stack rev ($mm)",
        "AI Stack R&D $-profile ($mm, pre-revenue floor)",
        "AI Stack R&D ($mm) — MAX($-profile, % × rev)",
        "Mars/Moon R&D ($mm/yr) — year-row",
        "Total R&D ($mm)",
        "S&M — % of base (bounded-CAGR)",
        "S&M base — Starlink + Starshield + Customer Launch ext + AI Stack rev ($mm)",
        "S&M ($mm)",
        "G&A — % of group rev (bounded-CAGR, drift toward ceiling)",
        "G&A base — Group P&L net (Lock d 2026-05-22)",
        "G&A ($mm)",
        "Customer Service ($mm) — 2% × Starlink subscription rev",
        "Other corporate operating ($mm) — 1% × Group P&L net (Lock d 2026-05-22)",
        "Total SG&A ($mm)",
        "Total OpEx ($mm)",
        "Memo: Customer Launch external revenue ($mm)",
        "Memo: Group revenue (Sprint 8 pre-aggregation; sum of 5 module R201s)",
        "Memo: Total R&D 2025 calibration anchor ($mm)",
        "Memo: Total OpEx 2025 calibration anchor ($mm)",
        "Memo: Total OpEx 2025 calibration delta (%)",
    ),
    "Starlink": (
        "INPUTS FROM CENTRAL ALLOCATOR",
        "Starlink V2 BB cash allocation ($mm)",
        "Starlink V2 DTC cash allocation ($mm)",
        "Starlink V3 BB cash allocation ($mm)",
        "Starlink V3 DTC cash allocation ($mm)",
        "Starlink V3 BB kg allocation (kg-to-LEO)",
        "Starlink V3 DTC kg allocation (kg-to-LEO)",
        "Total Capital Available ($mm)",
        "V2 BB Gbps per sat",
        "V2 DTC Gbps per sat",
        "V3 BB Gbps per sat",
        "V3 DTC Gbps per sat",
        "▸ Vehicle deployment (V2 BB, V2 DTC, V3 BB, V3 DTC — launches, fleet, ratchet, retirement)",
        "V2 BB launches per year",
        "V2 DTC launches per year",
        "V3 BB launches per year",
        "V3 DTC launches per year",
        "V2/V3 ratchet flag — RETIRED 2026-05-26 (replaced by V2 phase-out R350 + V3 trigger LC R56 gates per §20.6 Architecture amendments)",
        "F9 V2 BB launches (internal)",
        "F9 V2 DTC launches (internal)",
        "Starship V3 BB launches (internal)",
        "Starship V3 DTC launches (internal)",
        "V3 BB Starship kg demand",
        "V3 DTC Starship kg demand",
        "V2 BB historical retirement",
        "V2 DTC historical retirement",
        "V2 BB launch-cohort retirement",
        "V2 DTC launch-cohort retirement",
        "V3 BB launch-cohort retirement",
        "V3 DTC launch-cohort retirement",
        "Active V2 BB sats",
        "Active V2 DTC sats",
        "Active V3 BB sats",
        "Active V3 DTC sats",
        "Memo: Total active Starlink sats (excl legacy V1/V1.5)",
        "▸ Per-vehicle CapEx (sat unit cost via Wright's Law + facility CapEx with 1-yr lag)",
        "V2 BB sat unit cost ($mm/sat)",
        "V2 DTC sat unit cost ($mm/sat)",
        "V3 BB sat unit cost ($mm/sat)",
        "V3 DTC sat unit cost ($mm/sat)",
        "V2 BB facility CapEx per sat ($mm/sat)",
        "V2 DTC facility CapEx per sat ($mm/sat)",
        "V3 BB facility CapEx per sat ($mm/sat)",
        "V3 DTC facility CapEx per sat ($mm/sat)",
        "V2 BB sat CapEx ($mm)",
        "V2 BB facility CapEx ($mm)",
        "V2 DTC sat CapEx ($mm)",
        "V2 DTC facility CapEx ($mm)",
        "V3 BB sat CapEx ($mm)",
        "V3 BB facility CapEx ($mm)",
        "V3 DTC sat CapEx ($mm)",
        "V3 DTC facility CapEx ($mm)",
        "Module CapEx ($mm)",
        "Capital deployed ($mm)",
        "▸ Starshield revenue (Q4'25 mechanic — reserved Gbps × $/Gbps with decay)",
        "Total active BB Gbps (Starlink + Starshield + legacy)",
        "Starshield reserved %",
        "Starshield reserved Gbps",
        "Starshield $/Gbps ($/Gbps/yr)",
        "Starshield revenue ($mm)",
        "▸ External revenue (bandwidth-driven: Available Gbps × $/Gbps; subs derived)",
        "BB Gbps available for external Starlink revenue",
        "BB $/Gbps ($/Gbps/yr)",
        "BB Revenue ($mm)",
        "BB ARPU ($/mo, year-row from Assumptions)",
        "BB subscribers (millions, derived = BB Revenue / (ARPU × 12))",
        "DTC Gbps available for external Starlink revenue",
        "DTC $/Gbps ($/Gbps/yr)",
        "DTC ARPU ($/mo, year-row from Assumptions)",
        "DTC Revenue ($mm)",
        "DTC subscribers (millions, derived = DTC Revenue / (ARPU × 12))",
        "Terminal hardware revenue ($mm)",
        "▸ Internal bandwidth revenue (Starlink → ODC, 4-step pattern per Architecture §7.2)",
        "Starlink internal bandwidth revenue ($mm)",
        "▸ COGS (Constellation D&A, Ground ops, Spectrum amort BB-only, Terminal COGS, Insurance, Other)",
        "Constellation D&A ($mm)",
        "Launch services cost ($mm) — internal at-cost from Customer Launch",
        "Ground ops cost ($mm)",
        "Spectrum amortization (BB-only) ($mm)",
        "Terminal COGS ($mm)",
        "Insurance ($mm)",
        "Other COGS ($mm)",
        "Total COGS ($mm)",
        "▸ Module P&L (vending-machine: Revenue → COGS → EBITDA → CapEx → FCF)",
        "Total Revenue ($mm)",
        "Module EBITDA ($mm)",
        "Module EBITDA Margin %",
        "Module CapEx ($mm) — restated",
        "Module FCF ($mm)",
        "CENTRAL ALLOCATOR OUTPUTS",
        "Spot IRR",
        "Forward IRR (Y+2)",
        "Blended IRR",
        "Capacity Demand (kg-to-LEO)",
        "Memo: V2 BB per-sat cost ($mm/sat) — sat unit cost + facility per sat",
        "Memo: V2 BB per-sat net marginal revenue per year ($mm/sat/yr)",
        "Memo: V2 BB Spot IRR",
        "Memo: V2 BB Forward IRR (Y+2)",
        "Memo: V2 BB Blended IRR",
        "Memo: V2 DTC per-sat cost ($mm/sat)",
        "Memo: V2 DTC per-sat net marginal revenue per year ($mm/sat/yr)",
        "Memo: V2 DTC Spot IRR",
        "Memo: V2 DTC Forward IRR (Y+2)",
        "Memo: V2 DTC Blended IRR",
        "Memo: V3 BB per-sat cost ($mm/sat)",
        "Memo: V3 BB per-sat net marginal revenue per year ($mm/sat/yr)",
        "Memo: V3 BB Spot IRR",
        "Memo: V3 BB Forward IRR (Y+2)",
        "Memo: V3 BB Blended IRR",
        "Memo: V3 DTC per-sat cost ($mm/sat)",
        "Memo: V3 DTC per-sat net marginal revenue per year ($mm/sat/yr)",
        "Memo: V3 DTC Spot IRR",
        "Memo: V3 DTC Forward IRR (Y+2)",
        "Memo: V3 DTC Blended IRR",
        "Memo: Average $/Gbps BB from curve (= BB Revenue / BB Gbps × 1e6)",
        "Memo: Average $/Gbps DTC from curve (= DTC Revenue / DTC Gbps × 1e6)",
        "Memo: Legacy V1/V1.5 D&A ($mm)",
        "Memo: Facility D&A — sat manufacturing + ground stations ($mm)",
        "Memo: Cum V3 BB sats launched (running sum) — Rule 23 exception, year-chained",
    ),
    "Starlink Capacity": (
        "STARLINK CAPACITY -- aggregates constellation BB + DTC pools, allocates internal bandwidth claim to ODC, computes available bandwidth for external Starlink revenue. Sprint 4 fills.",
        "STARLINK CAPACITY — supply-side bandwidth aggregation + internal claim to ODC",
        "▸ Total active Gbps (BB + DTC, from Starlink tab active sat fleet)",
        "Total active BB Gbps",
        "Total active DTC Gbps",
        "▸ Internal claim by ODC (Sprint 5 placeholders)",
        "ODC BB Gbps demand",
        "ODC DTC Gbps demand",
        "▸ Available bandwidth for external Starlink revenue",
        "BB Gbps available for external Starlink revenue",
        "DTC Gbps available for external Starlink revenue",
        "▸ Pool cost basis ($mm/yr; reads Starlink tab COGS components)",
        "BB pool cost basis ($mm/yr)",
        "DTC pool cost basis ($mm/yr)",
        "▸ At-cost transfer rates ($/Gbps/yr; for Sprint 5 ODC + Starlink internal bandwidth revenue)",
        "BB pool at-cost rate ($/Gbps/yr)",
        "DTC pool at-cost rate ($/Gbps/yr)",
    ),
    "Valuation": (
        "VALUATION -- DCF off Group FCF + Sum-of-parts per module + Multiples cross-check + Comparables + Sensitivity. Sprint 11 fills.",
    ),
}


def resolve_label(constant_name: str) -> str:
    """Return the Excel label string for a registry constant name."""
    return globals()[constant_name]
