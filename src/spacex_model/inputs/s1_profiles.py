"""S-1 disclosed value profiles (SpaceX Form S-1 filed 2026-05-20).

Used as code defaults when V2.16 Assumptions rows are missing or pre-audit.
See SpaceX_Modeler_S1_Adherence_Audit_2026-05-28.docx §7.2 P0 + §7.3 P1 backlog.
"""

from __future__ import annotations

import numpy as np

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS

# P1-1 — MDA §6.5: $20B bridge executed March 2026
BRIDGE_DRAWDOWN_YEAR = 2026


def year_profile(pairs: list[tuple[int, float]], *, fill: float = 0.0) -> np.ndarray:
    """Build length-26 vector from (year, value) anchors; forward-fill between knots."""
    vec = np.full(HORIZON_YEARS, fill, dtype=np.float64)
    knots = sorted(pairs, key=lambda x: x[0])
    for year, value in knots:
        idx = year - FIRST_YEAR
        if 0 <= idx < HORIZON_YEARS:
            vec[idx] = value
    last = fill
    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        for y, v in knots:
            if y == year:
                last = v
                break
        vec[t] = last
    return vec


def broadband_arpu_sub_mo() -> np.ndarray:
    """MD&A §7.2 — S-1 Starlink blended ARPU direction; BB row R127."""
    return year_profile(
        [
            (2025, 81.0),
            (2026, 70.0),
            (2027, 65.0),
            (2028, 65.0),
            (2029, 70.0),
            (2030, 75.0),
        ],
        fill=75.0,
    )


def echostar_spectrum_capex_mm() -> np.ndarray:
    """MD&A ~line 5145 — close Nov 30, 2027; $19.6B total consideration."""
    vec = np.zeros(HORIZON_YEARS, dtype=np.float64)
    vec[2027 - FIRST_YEAR] = 19_600.0
    return vec


def f9_customer_launches_per_year() -> np.ndarray:
    """MD&A ~line 920 — audited 43 in 2025; P1-12 plateau/decline per §9.8."""
    return year_profile(
        [
            (2025, 43.0),
            (2026, 40.0),
            (2027, 38.0),
            (2028, 35.0),
            (2029, 32.0),
            (2030, 30.0),
            (2035, 25.0),
            (2040, 20.0),
            (2050, 15.0),
        ],
        fill=15.0,
    )


def s1_ai_segment_revenue_mm() -> np.ndarray:
    """S-1 AI segment (xAI / X legacy) — MDA §1.5; 2025 audited $3,201mm."""
    return year_profile(
        [
            (2025, 3_201.0),
            (2026, 3_200.0),
            (2027, 3_250.0),
            (2028, 3_300.0),
            (2029, 3_350.0),
            (2030, 3_400.0),
        ],
        fill=3_400.0,
    )


def anthropic_compute_revenue_mm() -> np.ndarray:
    """Anthropic Cloud Services Agreement — PS ~line 1300 ($1.25B/mo from May 2026)."""
    vec = np.zeros(HORIZON_YEARS, dtype=np.float64)
    vec[2026 - FIRST_YEAR] = 9_000.0
    vec[2027 - FIRST_YEAR] = 15_000.0
    vec[2028 - FIRST_YEAR] = 15_000.0
    vec[2029 - FIRST_YEAR] = 5_000.0
    return vec


def terrestrial_ai_capex_mm() -> np.ndarray:
    """COLOSSUS / COLOSSUS II terrestrial data-center CapEx — MDA §5.4."""
    return year_profile(
        [
            (2025, 12_727.0),
            (2026, 30_000.0),
            (2027, 20_000.0),
            (2028, 12_000.0),
            (2029, 8_000.0),
            (2030, 5_000.0),
        ],
        fill=3_000.0,
    )


def starship_precommercial_rd_mm() -> np.ndarray:
    """Starship R&D expensed pre-commercialization — MDA §9 / §11.6 (P1-4)."""
    return year_profile(
        [
            (2025, 3_004.0),
            (2026, 2_000.0),
            (2027, 1_000.0),
            (2028, 500.0),
        ],
        fill=500.0,
    )


def starship_customer_launches_per_year() -> np.ndarray:
    """Starship customer launches — PS ~line 720; 2H 2026 commercial start (P1-5)."""
    return year_profile(
        [
            (2025, 0.0),
            (2026, 3.0),
            (2027, 8.0),
            (2028, 15.0),
            (2029, 25.0),
            (2030, 35.0),
        ],
        fill=50.0,
    )


def starship_customer_launch_price_mm() -> np.ndarray:
    """First commercial Starship flights — loss-leader at ~$75mm/launch (P1-5)."""
    return year_profile(
        [
            (2026, 75.0),
            (2027, 80.0),
            (2028, 90.0),
            (2029, 100.0),
            (2030, 110.0),
        ],
        fill=150.0,
    )


def launch_services_revenue_share() -> np.ndarray:
    """Space segment L&D vs Launch Services split — MDA §1.3 (P1-11)."""
    return year_profile([(2025, 0.63), (2026, 0.63), (2027, 0.62)], fill=0.60)


def share_based_compensation_mm() -> np.ndarray:
    """S-1 audited SBC — FIN_STMTS (P1-7 Adj EBITDA add-back)."""
    return year_profile([(2025, 1_947.0), (2026, 2_000.0)], fill=2_000.0)


def restructuring_charges_mm() -> np.ndarray:
    """S-1 restructuring — FIN_STMTS (P1-7)."""
    return year_profile([(2025, 487.0), (2026, 400.0)], fill=200.0)


def impairment_charges_mm() -> np.ndarray:
    """S-1 impairment — FIN_STMTS (P1-7)."""
    return year_profile([(2025, 38.0), (2026, 30.0)], fill=20.0)


def starshield_gov_connectivity_scope_factor() -> float:
    """P1-10: scale Starshield to S-1 Government Connectivity (~$1.75B vs port ~$2.52B)."""
    return 1_750.0 / 2_520.0


# P1-8 — audited multi-year reference anchors (FIN_STMTS_IDX)
S1_AUDITED_GROUP_REVENUE_MM: dict[int, float] = {
    2023: 10_387.0,
    2024: 14_015.0,
    2025: 18_674.0,
}

S1_AUDITED_SPACE_REVENUE_MM: dict[int, float] = {
    2023: 3_557.0,
    2024: 3_796.0,
    2025: 4_086.0,
}

S1_AUDITED_CONNECTIVITY_REVENUE_MM: dict[int, float] = {
    2023: 3_869.0,
    2024: 7_599.0,
    2025: 11_387.0,
}

S1_AUDITED_AI_REVENUE_MM: dict[int, float] = {
    2023: 2_961.0,
    2024: 2_620.0,
    2025: 3_201.0,
}

S1_AUDITED_GROUP_CAPEX_MM: dict[int, float] = {
    2023: 4_500.0,  # approximate from segment roll-up
    2024: 8_500.0,
    2025: 20_737.0,
}

S1_AUDITED_ADJ_EBITDA_MM: dict[int, float] = {
    2023: 3_821.0,
    2024: 5_350.0,
    2025: 6_584.0,
}

# P1-9 — Q1 2026 sanity anchors (FIN_STMTS_NOTES_2)
S1_Q1_2026_REVENUE_MM = 4_694.0
S1_Q1_2026_OCF_MM = 1_047.0
S1_Q1_2026_CAPEX_MM = 10_107.0
