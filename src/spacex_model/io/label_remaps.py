"""Versioned label remap tables for workbook migrations (Theme A / Milestone 2)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from spacex_model.config.settings import get_repo_root
from spacex_model.engine.label_lookup import normalize_label

_UNIT_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\$mm/yr", re.I), "mm_usd_per_yr"),
    (re.compile(r"\$mm", re.I), "mm_usd"),
    (re.compile(r"\$/mo", re.I), "usd_per_mo"),
    (re.compile(r"\$/kg", re.I), "usd_per_kg"),
    (re.compile(r"\$/kit", re.I), "usd_per_kit"),
    (re.compile(r"\$/gbps", re.I), "usd_per_gbps"),
    (re.compile(r"\(%\)", re.I), "pct"),
    (re.compile(r"\(frac\)", re.I), "frac"),
    (re.compile(r"\(ratio\)", re.I), "ratio"),
    (re.compile(r"\(kg\)", re.I), "kg"),
    (re.compile(r"\(gbps\)", re.I), "gbps"),
    (re.compile(r"\(count\)", re.I), "count"),
    (re.compile(r"\(years?\)", re.I), "years"),
    (re.compile(r"\(gpu\)", re.I), "gpu"),
    (re.compile(r"cagr", re.I), "cagr"),
    (re.compile(r" pct\b", re.I), "pct"),
]


def parse_unit_hints(label: str) -> list[str]:
    """Extract coarse unit hints from label text for compatibility checks."""
    hints: list[str] = []
    for pattern, hint in _UNIT_PATTERNS:
        if pattern.search(label):
            hints.append(hint)
    return hints or ["unknown"]


def unit_hints_compatible(old_label: str, new_label: str) -> bool:
    """True when unit hints overlap or either side is unknown-only."""
    old_hints = set(parse_unit_hints(old_label))
    new_hints = set(parse_unit_hints(new_label))
    if old_hints == {"unknown"} or new_hints == {"unknown"}:
        return True
    return bool(old_hints & new_hints)


@dataclass
class RemapEntry:
    old_label: str
    new_label: str
    status: str = "proposed"
    old_unit_hints: list[str] = field(default_factory=list)
    new_unit_hints: list[str] = field(default_factory=list)
    reason: str = ""


@dataclass
class RemapTable:
    from_workbook: str
    to_workbook: str
    entries: list[RemapEntry]
    generated: str = ""
    source_script: str = ""
    applied_in_code: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "from_workbook": self.from_workbook,
            "to_workbook": self.to_workbook,
            "generated": self.generated,
            "source_script": self.source_script,
            "applied_in_code": self.applied_in_code,
            "label_remaps": [
                {
                    "old_label": e.old_label,
                    "new_label": e.new_label,
                    "status": e.status,
                    "old_unit_hints": e.old_unit_hints or parse_unit_hints(e.old_label),
                    "new_unit_hints": e.new_unit_hints or parse_unit_hints(e.new_label),
                    "reason": e.reason,
                }
                for e in self.entries
            ],
        }


def remaps_dir() -> Path:
    return get_repo_root() / "data" / "label_remaps"


def list_remap_files() -> list[Path]:
    root = remaps_dir()
    if not root.is_dir():
        return []
    return sorted(root.glob("*.json"))


def load_remap_table(path: Path | None = None) -> RemapTable | None:
    """Load a remap table; default loads all tables merged oldest-first."""
    if path is not None:
        return _load_one(path)
    files = list_remap_files()
    if not files:
        return None
    merged: list[RemapEntry] = []
    from_wb = ""
    to_wb = ""
    for file in files:
        table = _load_one(file)
        if table is None:
            continue
        from_wb = from_wb or table.from_workbook
        to_wb = table.to_workbook
        merged.extend(table.entries)
    if not merged:
        return None
    return RemapTable(from_workbook=from_wb, to_workbook=to_wb, entries=merged)


def _load_one(path: Path) -> RemapTable | None:
    if not path.is_file():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    entries = [
        RemapEntry(
            old_label=str(item["old_label"]),
            new_label=str(item["new_label"]),
            status=str(item.get("status", "proposed")),
            old_unit_hints=list(
                item.get("old_unit_hints") or parse_unit_hints(str(item["old_label"]))
            ),
            new_unit_hints=list(
                item.get("new_unit_hints") or parse_unit_hints(str(item["new_label"]))
            ),
            reason=str(item.get("reason", "")),
        )
        for item in raw.get("label_remaps", [])
    ]
    return RemapTable(
        from_workbook=str(raw.get("from_workbook", "")),
        to_workbook=str(raw.get("to_workbook", "")),
        entries=entries,
        generated=str(raw.get("generated", "")),
        source_script=str(raw.get("source_script", "")),
        applied_in_code=bool(raw.get("applied_in_code", False)),
    )


def build_remap_index(table: RemapTable | None) -> dict[str, str]:
    """Map normalized new label -> old label (last wins on collision)."""
    if table is None:
        return {}
    out: dict[str, str] = {}
    for entry in table.entries:
        out[normalize_label(entry.new_label)] = entry.old_label
    return out


def build_old_to_new_index(table: RemapTable | None) -> dict[str, str]:
    """Map normalized old label -> normalized new label."""
    if table is None:
        return {}
    out: dict[str, str] = {}
    for entry in table.entries:
        out[normalize_label(entry.old_label)] = normalize_label(entry.new_label)
    return out


def build_old_label_keys(table: RemapTable | None) -> set[str]:
    if table is None:
        return set()
    return {normalize_label(e.old_label) for e in table.entries}


def validate_remap_table(table: RemapTable, *, allow_flagged: bool = True) -> list[str]:
    """Return blocking errors for unit-incompatible or unannotated many-to-one remaps."""
    errors: list[str] = []
    new_targets: dict[str, list[str]] = {}
    for entry in table.entries:
        key = normalize_label(entry.new_label)
        new_targets.setdefault(key, []).append(entry.old_label)
        if entry.status == "flagged" and allow_flagged:
            continue
        if not unit_hints_compatible(entry.old_label, entry.new_label):
            errors.append(
                f"Unit-incompatible remap ({entry.status}): "
                f"{entry.old_label!r} -> {entry.new_label!r}"
            )
    for new_label, olds in new_targets.items():
        if len(olds) > 1:
            flagged = all(
                e.status in ("flagged", "fixed")
                for e in table.entries
                if normalize_label(e.new_label) == new_label
            )
            if not flagged and not allow_flagged:
                errors.append(f"Many-to-one remap to {new_label!r}: {olds}")
            elif not flagged:
                errors.append(
                    f"Many-to-one remap to {new_label!r} requires status flagged: {olds}"
                )
    return errors


def write_remap_table(table: RemapTable, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(table.to_dict(), indent=2) + "\n", encoding="utf-8")
