#!/usr/bin/env python3
"""Rebase Python port from V4.113 → V4.131: remap assumption labels, clear stale defaults."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SUPPLEMENT = REPO / "src/spacex_model/config/canonical_labels_supplement.py"
DEFAULTS = REPO / "src/spacex_model/config/ingest_scalar_defaults.py"
SETTINGS = REPO / "src/spacex_model/config/settings.py"
ANCHORS = REPO / "src/spacex_model/inputs/v4_113_2025_anchors.py"

# Old Assumptions label → V4.131 Assumptions label (verified against workbook ingest).
LABEL_REMAP: dict[str, str] = {
    "AI Stack R&D — CAGR (taper)": "AI Stack R&D CAGR",
    "AI Stack R&D — end-state % (floor)": "AI Stack R&D floor pct",
    "AI Stack R&D — start % of AI Stack rev": "AI Stack R&D start pct",
    "ODC R&D — CAGR (taper)": "ODC R&D CAGR",
    "ODC R&D — end-state % (floor)": "ODC R&D floor pct",
    "ODC R&D — start % of ODC rev": "ODC R&D start pct",
    "BB-share of ODC bandwidth claim": "BB-share of bandwidth (ratio)",
    "Gbps per GWh/yr of ODC compute energy": "Gbps per GWh/yr",
    "Orbital PUE uplift vs terrestrial": "Orbital PUE",
    "ODC utilization factor": "Utilization ceiling (%)",
    "Starlink ground ops % of revenue": "Ground/network opex pct rev",
    "Starlink insurance % of revenue": "Asset insurance COGS (% of revenue)",
    "Starlink other COGS % of revenue": "Asset insurance COGS (% of revenue)",
    "Starshield Rev per Gbps — base year ($/Gbps)": "Starshield $/Gbps ($/Gbps-yr)",
    "Starshield Rev per Gbps — decay rate": "Starshield Gbps growth (frac)",
    "Starshield Reserved % — start": "Starshield utilization (frac)",
    "Starshield Reserved % — floor": "Starshield utilization (frac)",
    "Starshield Reserved % — decay rate": "Starshield Gbps growth (frac)",
    "V2 Mini Bandwidth per Sat — BB (Gbps)": "V2 BB Gbps per sat",
    "V2 Mini Bandwidth per Sat — DTC (Gbps)": "V2 BB Gbps per sat",
    "V2 Mini Mass (kg)": "V2 BB sat mass (kg)",
    "V2 Mini cost per kg — base year ($/kg)": "Satellite cost per kg: base year ($/kg)",
    "V2 Mini BB Active Sats — end-2025": "V2 Mini BB sats end-2025",
    "V2 Mini BB historical baseline (SoY 2025)": "V2 Mini BB sats end-2025",
    "V2 Mini DTC Active Sats — end-2025": "V2 DTC active sats end-2025",
    "V2 Mini DTC historical baseline (SoY 2025)": "V2 DTC active sats end-2025",
    "V3 BB Bandwidth per Sat — base year (Gbps)": "V3 BB Gbps per sat",
    "V3 DTC Bandwidth per Sat (Gbps)": "V3 DTC effective Gbps",
    "V3 Mass (kg)": "V3 BB sat mass (kg)",
    "Sats per F9 launch — V2 BB": "F9 sats per launch (V2 packing)",
    "Sats per F9 launch — V2 DTC": "F9 sats per launch (V2 packing)",
    "V3 BB first launch year": "V3 Starlink launch trigger year",
    "V3 DTC first launch year": "V3 Starlink launch trigger year",
    "V2 phase-out year (no V2 BB / V2 DTC launches from this year)": "V3 Starlink launch trigger year",
    "Total customer launch market CAGR (% growth/yr)": "Commercial launch market CAGR",
    "Launch insurance % of external revenue": "Launch insurance % of external rev",
    "Launch other COGS % of external revenue": "Launch other COGS % of external rev",
    "Sales & Marketing — start % of (Starlink+Starshield+Customer Launch ext) rev": (
        "Sales & Marketing: start % of (Starlink+Starshield+CL ext) rev"
    ),
    "Customer Service — flat % of Starlink subscription rev": (
        "Customer Service: flat % of Starlink subscription rev"
    ),
    "General & Administrative — CAGR (taper)": "General & Administrative: CAGR (taper)",
    "General & Administrative — end-state % (ceiling)": "General & Administrative: end-state % (floor)",
    "Legacy V1/V1.5 Bandwidth — end-2025 (Gbps)": "Legacy V1 Gbps per sat",
    "Satellite Dep per kg — annual decay rate": "Satellite cost per kg: learning rate",
    "Memo: AI segment total revenue 2025 ($M)": "S-1 AI (≙ xAI, consolidated): Revenue ($mm)",
    "S-1 AI segment revenue ($mm) — year-row": "S-1 AI (≙ xAI, consolidated): Revenue ($mm)",
    "Pre-IPO debt facility ($mm)": "Minimum cash buffer ($mm)",
    "ODC ground ops % of revenue": "Ground-network ops COGS (% of revenue)",
    "ODC insurance % of revenue": "ODC insurance pct rev",
    "ODC other COGS % of revenue": "ODC other COGS pct rev",
    "Impairment charges ($mm/yr) — year-row": "S-1 AI: Impairment ($mm)",
    "Restructuring charges ($mm/yr) — year-row": "S-1 AI: Restructuring ($mm)",
    "Share-based compensation ($mm/yr) — year-row": "S-1 AI: SBC supplemental ($mm)",
    "Starship payload — 2025 baseline (kg-to-LEO, fully reusable mode)": (
        "Starship payload for pre-build sizing (kg)"
    ),
    "Launches per Starship vehicle per year (cadence × variant blend, used for sizing)": (
        "Starship booster cadence for pre-build sizing (flights/yr)"
    ),
    "Vehicle build lead time (years)": "Launch vehicle calendar life (years)",
    "Lifetime reuses per ship (cap)": "Lifetime reuses per booster (year cap)",
    "DTC ARPU ($/sub/mo): year-row": "Broadband ARPU floor ($/mo)",
    "Credence on Model A (Pr(A))": "Model A credence Pr(A)",
    "TAM inflation rate (annual)": "Terminal growth rate g (group + most modules)",
    "GNI per capita growth rate (annual)": "GNI per capita CAGR",
    "Satellite useful life — V2 Mini (years)": "Sat operational life L (years)",
    "Satellite useful life — V3 (years)": "Sat operational life L (years)",
    "Satellite useful life — V2 Mini DTC (years)": "Sat operational life L (years)",
    "Satellite useful life — V3 DTC (years)": "Sat operational life L (years)",
    "F9 booster accounting depreciation cap (flights)": "F9 booster economic life (years)",
    "Starshield S-1 Government Connectivity scope factor": "SpaceX government market share %",
    "Subsidy mix (% of net adds subsidized)": "Terminal kits per net subscriber add",
    "Terminal retail price ($, subsidized)": "Terminal kit cost ($/kit)",
    "Terminal retail price ($, non-subsidized)": "Terminal kit cost ($/kit)",
}

# Constant-name overrides in supplement (old label string replaced outright).
SUPPLEMENT_OVERRIDES: dict[str, str] = {
    "BB_SHARE_OF_ODC_BANDWIDTH_CLAIM": "BB-share of bandwidth (ratio)",
    "CHIP_TDP_PER_CHIP_W_YEAR_ROW": "Chip TDP CAGR (post-2027, W/chip)",
    "CHIP_FP8_PERFORMANCE_TFLOPS_YEAR_ROW": "Chip FP8 per chip CAGR (/yr): smooth curve",
    "COREWEAVE_BASELINE_ANCHOR_YEAR_ROW": "Comp anchor: AI/Compute standalone (CoreWeave-anchored)",
    "S1_AI_SEGMENT_REVENUE_YEAR_ROW": "S-1 AI (≙ xAI, consolidated): Revenue ($mm)",
    "ANTHROPIC_COMPUTE_REVENUE_YEAR_ROW": "External compute 2025 seed (M H100-eq GPU)",
    "TERRESTRIAL_AI_CAPEX_YEAR_ROW": "Memo: Terrestrial AI compute draw (GW): year-row",
    "ECHOSTAR_MID_BAND_CAPEX_MM_YEAR_ROW": "Spectrum licence OpEx (% of revenue)",
    "PRE_IPO_DEBT_FACILITY_MM": "Minimum cash buffer ($mm)",
    "PRE_IPO_BRIDGE_DRAWDOWN_YEAR": "Launch-pacing year (apply caps in this year only)",
    "STARTING_CASH_POSITION_EOY_2024_MM": "Minimum cash buffer ($mm)",  # placeholder; cash_pool uses constant
    "WORKLOAD_MIX_INFERENCE_SHARE": "Effective Compute Ratio (ratio)",
    "ODC_UTILIZATION_FACTOR": "Utilization ceiling (%)",
    "ORBITAL_PUE_UPLIFT_VS_TERRESTRIAL": "Orbital PUE",
    "GBPS_PER_GWH_ODC_COMPUTE_ENERGY": "Gbps per GWh/yr",
    "STARLINK_GROUND_OPS_PCT_REV": "Ground/network opex pct rev",
    "STARLINK_INSURANCE_PCT_REV": "Asset insurance COGS (% of revenue)",
    "STARLINK_OTHER_COGS_PCT_REV": "Asset insurance COGS (% of revenue)",
    "STARSHIELD_REV_PER_GBPS_BASE_YEAR": "Starshield $/Gbps ($/Gbps-yr)",
    "STARSHIELD_REV_PER_GBPS_DECAY_RATE": "Starshield Gbps growth (frac)",
    "STARSHIELD_RESERVED_PCT_START": "Starshield utilization (frac)",
    "STARSHIELD_RESERVED_PCT_FLOOR": "Starshield utilization (frac)",
    "STARSHIELD_RESERVED_PCT_DECAY_RATE": "Starshield Gbps growth (frac)",
    "TOTAL_CUSTOMER_LAUNCH_MARKET_CAGR": "Commercial launch market CAGR",
    "DTC_ARPU_SUB_MO_YEAR_ROW": "Broadband ARPU floor ($/mo)",
    "MEMO_AI_SEGMENT_TOTAL_REVENUE_2025_M": "S-1 AI (≙ xAI, consolidated): Revenue ($mm)",
}


def _patch_label_strings_in_file(path: Path, remap: dict[str, str]) -> int:
    text = path.read_text(encoding="utf-8")
    count = 0
    for old, new in sorted(remap.items(), key=lambda x: -len(x[0])):
        old_esc = old.replace("\\", "\\\\").replace('"', '\\"')
        new_esc = new.replace("\\", "\\\\").replace('"', '\\"')
        pattern = f'"{re.escape(old_esc)}"'
        if old_esc in text:
            text, n = re.subn(pattern, f'"{new_esc}"', text)
            count += n
    if count:
        path.write_text(text, encoding="utf-8")
    return count


def _rewrite_supplement() -> None:
    lines = [
        '"""Port-only canonical labels — remapped for V4.131 (2026-06-10 rebase)."""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Final",
        "",
    ]
    # Preserve existing supplement constants with remapped strings.
    import spacex_model.config.canonical_labels_supplement as old_sup  # noqa: E402

    seen: set[str] = set()
    for name in sorted(dir(old_sup)):
        if not name.isupper() or name in seen:
            continue
        seen.add(name)
        label = SUPPLEMENT_OVERRIDES.get(name, getattr(old_sup, name))
        if not isinstance(label, str):
            continue
        label = LABEL_REMAP.get(label, label)
        esc = label.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f"{name}: Final[str] = \"{esc}\"")

    # Drop removed stub labels — no longer in V4.131 model.
    drop = {
        "CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_KG_DEMAND_STUB_KG",
        "CUSTOMER_LAUNCH_EXTERNAL_STARSHIP_LAUNCHES_STUB",
        "LAUNCH_SERVICES_REVENUE_SHARE_YEAR_ROW",
        "STARSHIP_PRECOMMERCIAL_RD_MM_YEAR_ROW",
        "LEGACY_V1_V1_5_ACTIVE_BANDWIDTH_YEAR_ROW",
        "LUNAR_LABOUR_SHARE_SURFACE_PAYLOAD_YEAR_ROW",
        "MARS_LABOUR_SHARE_SURFACE_PAYLOAD_YEAR_ROW",
        "ODC_EXTERNAL_COMPUTE_SHARE_CUSTOMERS_YEAR_ROW",
        "CORPORATE_HISTORICAL_CAPITAL_BASE_MM",
    }
    text = "\n".join(lines) + "\n"
    for const in drop:
        text = re.sub(rf"^{const}:.*\n", "", text, flags=re.M)
    SUPPLEMENT.write_text(text, encoding="utf-8")


def _clear_defaults() -> None:
    DEFAULTS.write_text(
        '"""Ingest-time scalar defaults — empty after V4.131 rebase (all inputs in workbook)."""\n\n'
        "from __future__ import annotations\n\n"
        "INGEST_SCALAR_DEFAULTS: dict[str, float] = {}\n",
        encoding="utf-8",
    )


def _update_settings() -> None:
    text = SETTINGS.read_text(encoding="utf-8")
    text = text.replace("SpaceX V4.113.xlsx", "SpaceX V4.131.xlsx")
    SETTINGS.write_text(text, encoding="utf-8")


def _update_anchors_module() -> None:
    text = ANCHORS.read_text(encoding="utf-8")
    text = text.replace("V4.113", "V4.131")
    text = text.replace("v4_113", "v4_131")
    text = text.replace(
        "cl.MEMO_AI_SEGMENT_TOTAL_REVENUE_2025_M",
        '"S-1 AI (≙ xAI, consolidated): Revenue ($mm)"',
    )
    text = text.replace(
        "cl.STARTING_CASH_POSITION_EOY_2024_MM",
        '"Minimum cash buffer ($mm)"',  # anchor uses CAE-embedded starting cash; label is diagnostic only
    )
    new_path = REPO / "src/spacex_model/inputs/v4_131_2025_anchors.py"
    new_path.write_text(text, encoding="utf-8")
    if ANCHORS.exists() and new_path != ANCHORS:
        ANCHORS.unlink()


def main() -> int:
    workbook = REPO / "SpaceX V4.131.xlsx"
    if not workbook.exists():
        print(f"Missing workbook: {workbook}", file=sys.stderr)
        return 1

    print("Extracting canonical labels from V4.131...")
    subprocess.run(
        [sys.executable, str(REPO / "scripts/extract_canonical_labels.py"), str(workbook)],
        check=True,
        cwd=REPO,
    )

    cl_path = REPO / "src/spacex_model/config/canonical_labels.py"
    n = _patch_label_strings_in_file(cl_path, LABEL_REMAP)
    print(f"Patched {n} label strings in canonical_labels.py")

    _rewrite_supplement()
    print(f"Rewrote {SUPPLEMENT.name}")

    _clear_defaults()
    print(f"Cleared {DEFAULTS.name}")

    _update_settings()
    print("Updated settings workbook path")

    _update_anchors_module()
    print("Renamed v4_131_2025_anchors.py")

    # Record per-cell ingest diff (change log).
    sys.path.insert(0, str(REPO / "src"))
    from spacex_model.io.excel_ingest import ingest_workbook

    ingest = ingest_workbook(workbook)
    changes = ingest  # record_ingest_changes already called inside ingest_workbook
    from spacex_model.io.snapshot_store import record_ingest_changes

    delta = record_ingest_changes(ingest)
    print(f"Recorded {len(delta)} per-cell change-log entries for V4.131")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
