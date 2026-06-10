#!/usr/bin/env python3
"""Remove default= kwargs from assumption_scalar() calls under calc/ and engine/."""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [
    ROOT / "src/spacex_model/calc",
    ROOT / "src/spacex_model/engine",
]


def _call_name(node: ast.Call) -> str | None:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def strip_file(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    spans: list[tuple[int, int, int]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or _call_name(node) != "assumption_scalar":
            continue
        for kw in node.keywords:
            if kw.arg != "default":
                continue
            start = kw.col_offset
            end = kw.end_col_offset
            line = kw.lineno - 1
            line_text = source.splitlines()[line]
            if start > 0 and line_text[start - 1] == ",":
                start -= 1
            spans.append((line, start, end))

    if not spans:
        return False

    lines = source.splitlines(keepends=True)
    for line_idx, start, end in sorted(spans, key=lambda t: (t[0], -t[1])):
        line = lines[line_idx]
        newline = line[:start] + line[end:]
        lines[line_idx] = newline

    path.write_text("".join(lines), encoding="utf-8")
    return True


def main() -> int:
    changed = 0
    for base in TARGET_DIRS:
        for path in sorted(base.rglob("*.py")):
            if strip_file(path):
                print(path.relative_to(ROOT))
                changed += 1
    print(f"Updated {changed} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
