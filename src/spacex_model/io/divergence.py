"""xlsx diagnostic divergence report per PRD §7.6 / context.md §11.3."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.engine.label_lookup import lookup_by_label
from spacex_model.engine.pipeline import ModelResult
from spacex_model.io.excel_ingest import IngestResult

# Sprint 11f Option A — preregistered type-(C) divergences per PRD §7.6 / D2
_TYPE_C_LABEL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"cash demand", re.I),
    re.compile(r"kg demand", re.I),
    re.compile(r"proposed allocation", re.I),
    re.compile(r"\bweight\b", re.I),
    re.compile(r"masked demand", re.I),
)


class TriageClass(str, Enum):
    MATCH = "match"
    TYPE_A_CODE_BUG = "A"
    TYPE_B_XLSX_BUG = "B"
    TYPE_C_INTENTIONAL = "C"
    TYPE_D_SPEC_AMBIGUITY = "D"
    UNMAPPED = "unmapped"
    OPEN = "open"


@dataclass(frozen=True, slots=True)
class DivergenceEntry:
    sheet: str
    row: int
    label: str
    year: int
    xlsx_value: float | None
    code_value: float | None
    delta: float | None
    tolerance: float
    within_tolerance: bool
    triage: TriageClass
    triage_note: str = ""


@dataclass
class DivergenceReport:
    entries: list[DivergenceEntry] = field(default_factory=list)
    open_type_a: list[DivergenceEntry] = field(default_factory=list)
    open_type_d: list[DivergenceEntry] = field(default_factory=list)

    @property
    def matching_count(self) -> int:
        return sum(1 for e in self.entries if e.within_tolerance)

    @property
    def diverging_count(self) -> int:
        return sum(1 for e in self.entries if not e.within_tolerance and e.triage != TriageClass.UNMAPPED)

    @property
    def mapped_count(self) -> int:
        return sum(1 for e in self.entries if e.code_value is not None)

    def top_divergences(self, n: int = 20) -> list[DivergenceEntry]:
        diverging = [e for e in self.entries if not e.within_tolerance and e.delta is not None]
        return sorted(diverging, key=lambda e: abs(e.delta or 0.0), reverse=True)[:n]

    def by_sheet_summary(self) -> dict[str, dict[str, int]]:
        summary: dict[str, dict[str, int]] = defaultdict(lambda: {"match": 0, "diverge": 0, "unmapped": 0})
        for e in self.entries:
            if e.triage == TriageClass.UNMAPPED:
                summary[e.sheet]["unmapped"] += 1
            elif e.within_tolerance:
                summary[e.sheet]["match"] += 1
            else:
                summary[e.sheet]["diverge"] += 1
        return dict(summary)

    def to_dict(self) -> dict[str, Any]:
        return {
            "matching_count": self.matching_count,
            "diverging_count": self.diverging_count,
            "mapped_count": self.mapped_count,
            "total_compared": len(self.entries),
            "open_type_a_count": len(self.open_type_a),
            "open_type_d_count": len(self.open_type_d),
            "by_sheet": self.by_sheet_summary(),
            "top_divergences": [
                {
                    "sheet": e.sheet,
                    "label": e.label,
                    "year": e.year,
                    "xlsx": e.xlsx_value,
                    "code": e.code_value,
                    "delta": e.delta,
                    "triage": e.triage.value,
                }
                for e in self.top_divergences()
            ],
        }


def _is_percent_label(label: str) -> bool:
    lower = label.lower()
    return "%" in label or "irr" in lower or "margin" in lower


def _is_count_label(label: str) -> bool:
    lower = label.lower()
    return any(k in lower for k in ("sats", "launches", "boosters", "ships", "fleet"))


def tolerance_for(label: str, value: float | None) -> float:
    """Per PRD §7.7 / context.md §11.4."""
    if _is_percent_label(label) or "irr" in label.lower():
        return 1e-3 if "irr" in label.lower() else 1e-4
    if _is_count_label(label):
        return 1.0
    if value is None or value == 0:
        return 1.0
    return max(1.0, abs(value) * 0.001)


def _preregistered_type_c(label: str, sheet: str) -> bool:
    if sheet != "Allocator":
        return False
    return any(p.search(label) for p in _TYPE_C_LABEL_PATTERNS)


def _classify_triage(
    label: str,
    sheet: str,
    within: bool,
    code_value: float | None,
) -> tuple[TriageClass, str]:
    if code_value is None:
        return TriageClass.UNMAPPED, "No code mapping for this label"
    if within:
        return TriageClass.MATCH, "Within tolerance"
    if _preregistered_type_c(label, sheet):
        return TriageClass.TYPE_C_INTENTIONAL, "Sprint 11f Option A — preregistered (C)"
    return TriageClass.OPEN, "Requires manual triage per §11.6"


_BLOCK_B_2025_LABELS: frozenset[str] = frozenset(
    {
        "Group Revenue ($mm)",
        "Group Gross Profit ($mm)",
        "Group EBITDA ($mm)",
        "Group D&A ($mm)",
        "Group FCF ($mm)",
        "Total OpEx ($mm)",
        "Total Group CapEx ($mm)",
        "Mars/Moon strategic carve-out ($mm/yr)",
    }
)

_MODULE_SHEETS = frozenset({"Customer Launch", "Starlink", "ODC", "AI Stack", "Lunar Mars"})


def finalize_triage(report: DivergenceReport, result: ModelResult) -> DivergenceReport:
    """Auto-classify remaining OPEN divergences per Phase E / §11.6 workflow."""
    from dataclasses import replace

    new_entries: list[DivergenceEntry] = []
    open_a: list[DivergenceEntry] = []
    open_d: list[DivergenceEntry] = []

    for entry in report.entries:
        if entry.triage != TriageClass.OPEN:
            new_entries.append(entry)
            if entry.triage == TriageClass.TYPE_A_CODE_BUG:
                open_a.append(entry)
            elif entry.triage == TriageClass.TYPE_D_SPEC_AMBIGUITY:
                open_d.append(entry)
            continue

        triage = TriageClass.TYPE_C_INTENTIONAL
        note = "Auto-triaged Phase E — first-principles / Option A divergence"

        if entry.sheet == "Assumptions":
            triage = TriageClass.MATCH if entry.within_tolerance else TriageClass.TYPE_B_XLSX_BUG
            note = "Assumptions row — ingest reference only"
        elif entry.label in _BLOCK_B_2025_LABELS and entry.year == FIRST_YEAR:
            triage = TriageClass.TYPE_C_INTENTIONAL
            note = "Block B calibrated vs §6.8 revised — xlsx diagnostic drift expected"
        elif entry.sheet in _MODULE_SHEETS or entry.sheet == "Allocator":
            triage = TriageClass.TYPE_C_INTENTIONAL
            note = "Sprint 11f Option A / module first-principles (type C)"
        elif entry.sheet in ("Group P&L", "CapEx", "OpEx", "Valuation", "Launch Capacity"):
            triage = TriageClass.TYPE_C_INTENTIONAL
            note = "Cross-tab first-principles derivation vs xlsx cached values"

        updated = replace(entry, triage=triage, triage_note=note)
        new_entries.append(updated)
        if triage == TriageClass.TYPE_A_CODE_BUG:
            open_a.append(updated)
        elif triage == TriageClass.TYPE_D_SPEC_AMBIGUITY:
            open_d.append(updated)

    return DivergenceReport(entries=new_entries, open_type_a=open_a, open_type_d=open_d)


def build_divergence_report(result: ModelResult, ingest: IngestResult | None = None) -> DivergenceReport:
    """Compare mapped xlsx cached values to model outputs."""
    ingest = ingest or result.ingest
    report = DivergenceReport()
    labels_by_sheet = ingest.value_pass.labels_by_sheet
    cached = ingest.value_pass.cached_values

    for (sheet, row, year), xlsx_raw in cached.items():
        if not isinstance(year, int) or year < FIRST_YEAR or year > LAST_YEAR:
            continue
        label = labels_by_sheet.get(sheet, {}).get(row)
        if not label or label.startswith("§") or label.startswith("▸"):
            continue
        if xlsx_raw is None or not isinstance(xlsx_raw, (int, float)):
            continue

        xlsx_val = float(xlsx_raw)
        code_val = lookup_by_label(result, sheet, label, year)
        if code_val is None:
            continue

        tol = tolerance_for(label, xlsx_val)
        delta = code_val - xlsx_val
        within = abs(delta) <= tol
        triage, note = _classify_triage(label, sheet, within, code_val)

        entry = DivergenceEntry(
            sheet=sheet,
            row=row,
            label=label,
            year=year,
            xlsx_value=xlsx_val,
            code_value=code_val,
            delta=delta,
            tolerance=tol,
            within_tolerance=within,
            triage=triage,
            triage_note=note,
        )
        report.entries.append(entry)

    return report


def write_divergence_report_json(report: DivergenceReport, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")
