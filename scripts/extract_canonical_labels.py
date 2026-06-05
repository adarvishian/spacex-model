#!/usr/bin/env python3
"""Extract column-A canonical labels from the canonical workbook into canonical_labels.py.

Merges V2.16 code-referenced constants not yet present in V4.113 (retired in R1+).
"""

from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

import openpyxl

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKBOOK = REPO_ROOT / "SpaceX V4.113.xlsx"
OUTPUT_PATH = REPO_ROOT / "src" / "spacex_model" / "config" / "canonical_labels.py"
SKIP_SHEETS = frozenset({"Claude Log"})


def label_to_constant_name(label: str) -> str:
    """Convert Excel column-A label to a valid Python identifier."""
    name = label.upper()
    name = re.sub(r"[^A-Z0-9]+", "_", name)
    name = re.sub(r"_+", "_", name).strip("_")
    if name and name[0].isdigit():
        name = f"L_{name}"
    if not name:
        name = "UNNAMED"
    return name


def extract_labels(workbook_path: Path) -> dict[str, list[str]]:
    wb = openpyxl.load_workbook(workbook_path, read_only=True, data_only=True)
    by_sheet: dict[str, list[str]] = {}
    for sheet_name in wb.sheetnames:
        if sheet_name in SKIP_SHEETS:
            continue
        ws = wb[sheet_name]
        labels: list[str] = []
        seen: set[str] = set()
        scan_rows = max(ws.max_row, 400)
        for row in ws.iter_rows(min_row=1, max_row=scan_rows, min_col=1, max_col=1):
            value = row[0].value
            if not value or not isinstance(value, str):
                continue
            text = value.strip()
            if len(text) < 2 or text.startswith("§"):
                continue
            if text not in seen:
                seen.add(text)
                labels.append(text)
        by_sheet[sheet_name] = labels
    wb.close()
    return by_sheet


def _code_referenced_constants() -> set[str]:
    """Constant names referenced as cl.<NAME> under src/spacex_model."""
    src_root = REPO_ROOT / "src" / "spacex_model"
    refs: set[str] = set()
    for path in src_root.rglob("*.py"):
        if path.name == "canonical_labels.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id == "cl"
            ):
                refs.add(node.attr)
    return refs


def _load_v216_constants() -> dict[str, str]:
    """Load constant -> label map from committed V2.16 registry (git HEAD)."""
    try:
        raw = subprocess.run(
            ["git", "show", "HEAD:src/spacex_model/config/canonical_labels.py"],
            check=True,
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}
    mapping: dict[str, str] = {}
    for line in raw.splitlines():
        m = re.match(r'^([A-Z][A-Z0-9_]*): Final\[str\] = "(.*)"$', line)
        if m:
            mapping[m.group(1)] = m.group(2).replace('\\"', '"').replace("\\\\", "\\")
    return mapping


def _legacy_constants_for_merge(
    workbook_labels: set[str],
    used_names: dict[str, str],
) -> list[tuple[str, str]]:
    """V2.16 constants still referenced by code but absent from V4.113 workbook."""
    refs = _code_referenced_constants()
    v216 = _load_v216_constants()
    legacy: list[tuple[str, str]] = []
    for const, label in sorted(v216.items()):
        if const not in refs:
            continue
        if label in workbook_labels:
            continue
        if const in used_names:
            continue
        legacy.append((const, label))
        used_names[const] = label
    return legacy


def render_module(by_sheet: dict[str, list[str]], workbook_path: Path) -> str:
    all_labels: list[str] = []
    for labels in by_sheet.values():
        all_labels.extend(labels)
    unique_sorted = sorted(set(all_labels))

    lines = [
        '"""Canonical label registry — append-only per PRD §2.4 / Rule 10.',
        "",
        f"Extracted from: {workbook_path.name}",
        "Regenerate via: python scripts/extract_canonical_labels.py",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Final",
        "",
        "# fmt: off",
        "",
    ]

    used_names: dict[str, str] = {}
    workbook_label_set = set(unique_sorted)
    for label in unique_sorted:
        const = label_to_constant_name(label)
        base = const
        n = 2
        while const in used_names and used_names[const] != label:
            const = f"{base}_{n}"
            n += 1
        used_names[const] = label
        escaped = label.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'{const}: Final[str] = "{escaped}"')

    legacy = _legacy_constants_for_merge(workbook_label_set, used_names)
    if legacy:
        lines.append("")
        lines.append("# V2.16 code-referenced labels — supersede in R1 module re-base")
        for const, label in legacy:
            escaped = label.replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'{const}: Final[str] = "{escaped}"')

    lines.extend(
        [
            "",
            "# fmt: on",
            "",
            "CANONICAL_LABELS: Final[frozenset[str]] = frozenset(",
            "    {",
        ]
    )
    for label in unique_sorted:
        escaped = label.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'        "{escaped}",')
    lines.extend(["    }", ")", "", "LABELS_BY_SHEET: Final[dict[str, tuple[str, ...]]] = {"])
    for sheet, labels in sorted(by_sheet.items()):
        sheet_key = sheet.replace("'", "\\'")
        lines.append(f'    "{sheet_key}": (')
        for label in labels:
            escaped = label.replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'        "{escaped}",')
        lines.append("    ),")
    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def resolve_label(constant_name: str) -> str:")
    lines.append('    """Return the Excel label string for a registry constant name."""')
    lines.append("    return globals()[constant_name]")
    lines.append("")
    lines.append("from spacex_model.config.canonical_labels_supplement import *  # noqa: E402, F403")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    workbook = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_WORKBOOK
    if not workbook.exists():
        print(f"Workbook not found: {workbook}", file=sys.stderr)
        return 1
    by_sheet = extract_labels(workbook)
    total = sum(len(v) for v in by_sheet.values())
    all_wb_labels = {label for labels in by_sheet.values() for label in labels}
    legacy_n = len(_legacy_constants_for_merge(all_wb_labels, {}))
    print(f"Extracted {total} labels across {len(by_sheet)} sheets")
    if legacy_n:
        print(f"Merged {legacy_n} V2.16 code-referenced legacy constants")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(render_module(by_sheet, workbook), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
