"""Structural drift analysis and remap proposal for workbook rebases."""

from __future__ import annotations

import difflib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from spacex_model.engine.label_lookup import normalize_label
from spacex_model.io.excel_ingest import run_value_pass
from spacex_model.io.label_remaps import (
    RemapEntry,
    RemapTable,
    parse_unit_hints,
    unit_hints_compatible,
    validate_remap_table,
    write_remap_table,
)


@dataclass
class LabelLocation:
    sheet: str
    row: int
    label: str


@dataclass
class DriftReport:
    from_workbook: str
    to_workbook: str
    exact_matches: list[tuple[LabelLocation, LabelLocation]] = field(
        default_factory=list
    )
    moved: list[tuple[LabelLocation, LabelLocation]] = field(default_factory=list)
    removed: list[LabelLocation] = field(default_factory=list)
    added: list[LabelLocation] = field(default_factory=list)
    fuzzy_candidates: list[tuple[LabelLocation, LabelLocation, float]] = field(
        default_factory=list
    )

    def to_dict(self) -> dict[str, Any]:
        def loc(d: LabelLocation) -> dict[str, Any]:
            return {"sheet": d.sheet, "row": d.row, "label": d.label}

        return {
            "from_workbook": self.from_workbook,
            "to_workbook": self.to_workbook,
            "exact_matches": [
                {"old": loc(o), "new": loc(n)} for o, n in self.exact_matches
            ],
            "moved": [{"old": loc(o), "new": loc(n)} for o, n in self.moved],
            "removed": [loc(r) for r in self.removed],
            "added": [loc(a) for a in self.added],
            "fuzzy_candidates": [
                {
                    "old": loc(o),
                    "new": loc(n),
                    "score": round(score, 3),
                }
                for o, n, score in self.fuzzy_candidates
            ],
        }


def _labels_by_sheet(workbook: Path) -> dict[str, dict[int, str]]:
    return run_value_pass(workbook).labels_by_sheet


def _flatten(labels: dict[str, dict[int, str]]) -> dict[tuple[str, str], LabelLocation]:
    """Key: (sheet, exact label) -> location (first row wins)."""
    out: dict[tuple[str, str], LabelLocation] = {}
    for sheet, rows in labels.items():
        if sheet == "Claude Log":
            continue
        for row, label in rows.items():
            if label.startswith("§") or label.startswith("▸") or label.isupper():
                continue
            key = (sheet, label)
            if key not in out:
                out[key] = LabelLocation(sheet=sheet, row=row, label=label)
    return out


def _token_ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, normalize_label(a), normalize_label(b)).ratio()


def compute_drift(from_workbook: Path, to_workbook: Path) -> DriftReport:
    """Compare label sets between two workbook versions."""
    old_labels = _flatten(_labels_by_sheet(from_workbook))
    new_labels = _flatten(_labels_by_sheet(to_workbook))

    report = DriftReport(
        from_workbook=from_workbook.name,
        to_workbook=to_workbook.name,
    )
    matched_new: set[tuple[str, str]] = set()

    for key, old_loc in old_labels.items():
        if key in new_labels:
            new_loc = new_labels[key]
            matched_new.add(key)
            if old_loc.row != new_loc.row or old_loc.sheet != new_loc.sheet:
                report.moved.append((old_loc, new_loc))
            else:
                report.exact_matches.append((old_loc, new_loc))

    for key, old_loc in old_labels.items():
        if key not in new_labels:
            report.removed.append(old_loc)

    for key, new_loc in new_labels.items():
        if key not in old_labels:
            report.added.append(new_loc)

    # Fuzzy: unmatched removed × added within same sheet
    removed_by_sheet: dict[str, list[LabelLocation]] = {}
    for loc in report.removed:
        removed_by_sheet.setdefault(loc.sheet, []).append(loc)
    added_by_sheet: dict[str, list[LabelLocation]] = {}
    for loc in report.added:
        added_by_sheet.setdefault(loc.sheet, []).append(loc)

    for sheet in set(removed_by_sheet) & set(added_by_sheet):
        for old_loc in removed_by_sheet[sheet]:
            for new_loc in added_by_sheet[sheet]:
                score = _token_ratio(old_loc.label, new_loc.label)
                if score >= 0.55:
                    report.fuzzy_candidates.append((old_loc, new_loc, score))

    report.fuzzy_candidates.sort(key=lambda t: t[2], reverse=True)
    return report


def propose_remap(
    drift: DriftReport,
    *,
    fuzzy_threshold: float = 0.72,
) -> RemapTable:
    """Build a proposed remap table from a drift report."""
    entries: list[RemapEntry] = []
    used_new: set[str] = set()

    for old_loc, new_loc in drift.moved:
        entries.append(
            RemapEntry(
                old_label=old_loc.label,
                new_label=new_loc.label,
                status="faithful",
                old_unit_hints=parse_unit_hints(old_loc.label),
                new_unit_hints=parse_unit_hints(new_loc.label),
                reason="Label moved row/sheet but text unchanged",
            )
        )
        used_new.add(new_loc.label)

    matched_fuzzy_old: set[str] = set()
    for old_loc, new_loc, score in drift.fuzzy_candidates:
        if old_loc.label in matched_fuzzy_old or new_loc.label in used_new:
            continue
        if score < fuzzy_threshold:
            continue
        compatible = unit_hints_compatible(old_loc.label, new_loc.label)
        status = "faithful" if compatible else "flagged"
        reason = "Fuzzy label match"
        if not compatible:
            reason = "Fuzzy match with incompatible unit hints — needs owner sign-off"
        entries.append(
            RemapEntry(
                old_label=old_loc.label,
                new_label=new_loc.label,
                status=status,
                old_unit_hints=parse_unit_hints(old_loc.label),
                new_unit_hints=parse_unit_hints(new_loc.label),
                reason=reason,
            )
        )
        matched_fuzzy_old.add(old_loc.label)
        used_new.add(new_loc.label)

    return RemapTable(
        from_workbook=drift.from_workbook,
        to_workbook=drift.to_workbook,
        entries=entries,
        generated=datetime.now(UTC).date().isoformat(),
        source_script="spacex-model rebase propose",
        applied_in_code=False,
    )


def apply_remap_strings(
    remap: RemapTable,
    *,
    target_paths: list[Path] | None = None,
    supplement_path: Path | None = None,
) -> int:
    """Patch label strings in Python source files from a remap table (registry apply)."""
    from spacex_model.config.settings import get_repo_root

    repo = get_repo_root()
    if target_paths is None:
        target_paths = [
            repo / "src" / "spacex_model" / "config" / "canonical_labels.py",
            repo / "src" / "spacex_model" / "config" / "canonical_labels_supplement.py",
            repo / "src" / "spacex_model" / "inputs",
            repo / "src" / "spacex_model" / "calc",
        ]
    remap_dict = {e.old_label: e.new_label for e in remap.entries}
    count = 0
    files: list[Path] = []
    for base in target_paths:
        if base.is_file() and base.suffix == ".py":
            files.append(base)
        elif base.is_dir():
            files.extend(sorted(base.rglob("*.py")))
    for path in files:
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in sorted(remap_dict.items(), key=lambda x: -len(x[0])):
            needle = f'"{old}"'
            if needle in text:
                text = text.replace(needle, f'"{new}"')
        if text != original:
            path.write_text(text, encoding="utf-8")
            count += 1
    return count


def write_drift_report(drift: DriftReport, path: Path) -> None:
    import json

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(drift.to_dict(), indent=2) + "\n", encoding="utf-8")


def validate_or_raise(table: RemapTable) -> None:
    errors = validate_remap_table(table, allow_flagged=True)
    blocking = [
        e
        for e in errors
        if "requires status flagged" not in e and "Many-to-one" not in e
    ]
    if blocking:
        msg = "Remap validation failed:\n" + "\n".join(f"  - {e}" for e in blocking)
        raise ValueError(msg)


__all__ = [
    "DriftReport",
    "compute_drift",
    "propose_remap",
    "apply_remap_strings",
    "write_drift_report",
    "write_remap_table",
    "validate_or_raise",
]
