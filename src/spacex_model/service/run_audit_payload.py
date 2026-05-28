"""Run Audit tab payload — FRONTEND_PRD §4.5."""

from __future__ import annotations

from typing import Any

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.engine.label_lookup import lookup_by_label
from spacex_model.engine.pipeline import ModelResult
from spacex_model.io.divergence import build_divergence_report, finalize_triage
from spacex_model.inputs.block_b_anchors import load_block_b_anchors_v1

_ANCHOR_LOOKUP: dict[str, tuple[str, str]] = {
    "Group Revenue 2025": ("Group P&L", "Group Revenue ($mm)"),
    "Group Gross Profit 2025": ("Group P&L", "Group Gross Profit ($mm)"),
    "Group EBITDA 2025": ("Group P&L", "Group EBITDA ($mm)"),
    "Group D&A 2025": ("Group P&L", "Group D&A ($mm)"),
    "Group FCF 2025": ("Group P&L", "Group FCF ($mm)"),
    "Total OpEx 2025": ("Group P&L", "Total OpEx ($mm)"),
    "Total Group CapEx 2025": ("Group P&L", "Total Group CapEx ($mm)"),
    "Mars carve-out 2025": ("Group P&L", "Mars/Moon strategic carve-out ($mm/yr)"),
    "F9 customer launches 2025": ("Customer Launch", "F9 customer launches per year"),
    "Starting cash EoY 2024": ("Group P&L", "Cash BoY ($mm)"),
    "Cash EoY 2025": ("Group P&L", "Cash EoY ($mm)"),
    "Adjusted EBITDA 2025": ("Group P&L", "Adjusted EBITDA ($mm)"),
    "Space segment revenue 2025": ("Customer Launch", "Total Revenue ($mm)"),
    "Connectivity segment revenue 2025": ("Starlink", "Total Revenue ($mm)"),
    "AI segment revenue 2025": ("AI Stack", "Total Revenue ($mm)"),
}


def build_run_audit_payload(result: ModelResult) -> dict[str, Any]:
    """Aggregate solver, conservation, calibration, and divergence data for Run Audit tab."""
    conservation = result.conservation
    solver = result.solver_trace

    r108_rows: list[dict[str, Any]] = []
    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        status = conservation.r108_ok_by_year.get(year, "CHECK")
        residuals = {
            check: conservation.residuals_by_check.get(check, {}).get(year, 0.0)
            for check in ("R99", "R100", "R101", "R102", "R103", "R104", "R105", "R106", "R107", "R110")
            if check in conservation.residuals_by_check
        }
        r108_rows.append(
            {
                "year": year,
                "status": status,
                "ok": status == "OK",
                "max_residual_mm": max((abs(v) for v in residuals.values()), default=0.0),
                "residuals": residuals,
            }
        )

    calibration: list[dict[str, Any]] = []
    for anchor in load_block_b_anchors_v1():
        lookup = _ANCHOR_LOOKUP.get(anchor.name)
        actual: float | None = None
        if lookup:
            sheet, label = lookup
            actual = lookup_by_label(result, sheet, label, FIRST_YEAR)
        within = False
        if actual is not None and anchor.target != 0:
            within = abs(actual - anchor.target) / abs(anchor.target) <= anchor.tolerance
        elif actual is not None:
            within = abs(actual - anchor.target) <= anchor.tolerance
        calibration.append(
            {
                "name": anchor.name,
                "target": anchor.target,
                "tolerance_pct": anchor.tolerance,
                "actual": actual,
                "within_tolerance": within,
                "delta": (actual - anchor.target) if actual is not None else None,
            }
        )

    div_report = finalize_triage(build_divergence_report(result), result)
    top50 = div_report.top_divergences(50)

    from spacex_model.service.sheets_meta import sheet_for_name

    divergences = []
    for e in top50:
        meta = sheet_for_name(e.sheet)
        divergences.append(
            {
                "sheet": e.sheet,
                "sheet_slug": meta.slug if meta else e.sheet.lower().replace(" ", "_"),
                "row": e.row,
                "row_id": f"R{e.row}",
                "label": e.label,
                "year": e.year,
                "xlsx_value": e.xlsx_value,
                "code_value": e.code_value,
                "delta": e.delta,
                "triage": e.triage.value,
                "triage_note": e.triage_note,
            }
        )

    return {
        "run_id": result.run_id,
        "solver": {
            "iterations": solver.iterations,
            "converged": solver.converged,
            "max_residual": solver.max_residual,
        },
        "conservation": {
            "all_ok": conservation.all_ok,
            "r108_by_year": r108_rows,
        },
        "calibration_anchors": calibration,
        "divergence_summary": {
            "matching_count": div_report.matching_count,
            "diverging_count": div_report.diverging_count,
            "mapped_count": div_report.mapped_count,
            "total_compared": len(div_report.entries),
        },
        "divergences": divergences,
    }
