#!/usr/bin/env python3
"""Audit stub-cell misclassification baseline — PRD Lineage Trust §10 Sprint 0 (L1.1).

Walks every grid-renderable audit sheet, calls lineage enrichment per cell that
displays a finite number, and partitions stub classifications into:
  (a) placeholder-tab cells (AI Stack, Valuation per context.md §2.4)
  (b) computed-but-unresolved (grid shows a number; lineage says stub)

Usage (from repo root):
    python scripts/audit_stub_cells.py
"""

from __future__ import annotations

import math
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = REPO_ROOT / "docs" / "stub_audit_2026-06-05.md"

# Placeholder audit views — genuine stubs per context.md §2.4.
PLACEHOLDER_SLUGS = frozenset({"ai_stack", "valuation"})


def _finite_number(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def _collect_stub_cells(
    result: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, int]]:
    from spacex_model.service.grid import build_grid_payload
    from spacex_model.service.lineage_enrich import enrich_lineage
    from spacex_model.service.sheets_meta import SHEETS

    bucket_a: list[dict[str, Any]] = []
    bucket_b: list[dict[str, Any]] = []
    stats: Counter[str] = Counter()

    for meta in SHEETS:
        if meta.slug == "run_audit":
            continue

        grid = build_grid_payload(meta, result)
        stats["sheets_walked"] += 1

        for row in grid["rows"]:
            if row.get("is_header"):
                continue

            label = row["label"]
            row_index = row["row_index"]

            for year_idx, year in enumerate(grid["years"]):
                display = row["year_values"][year_idx]
                if not _finite_number(display):
                    continue

                stats["cells_with_display_value"] += 1
                lineage_key = row["lineage_keys"][year_idx]

                enriched = enrich_lineage(
                    lineage_key,
                    result,
                    year=year,
                    sheet=meta.source_sheet,
                    row=row_index,
                    sheet_slug=meta.slug,
                )

                if enriched.get("cell_kind") != "stub":
                    stats["derived_or_input"] += 1
                    continue

                stats["stub_classified"] += 1
                entry = {
                    "sheet_slug": meta.slug,
                    "source_sheet": meta.source_sheet,
                    "row": row_index,
                    "label": label,
                    "year": year,
                    "lineage_key": lineage_key,
                    "grid_value": float(display),
                    "computed_value": enriched.get("computed_value"),
                    "grid_cell_kind": row["cell_kinds"][year_idx],
                }

                if meta.slug in PLACEHOLDER_SLUGS:
                    bucket_a.append(entry)
                    stats["bucket_a"] += 1
                else:
                    bucket_b.append(entry)
                    stats["bucket_b"] += 1

    return bucket_a, bucket_b, dict(stats)


def _format_entries(entries: list[dict[str, Any]], *, limit: int = 50) -> list[str]:
    lines: list[str] = []
    for i, e in enumerate(entries[:limit]):
        lines.append(
            f"| {i + 1} | `{e['sheet_slug']}` | R{e['row']} | {e['year']} | "
            f"`{e['lineage_key']}` | {e['grid_value']:,.4g} | {e['label'][:60]} |"
        )
    if len(entries) > limit:
        lines.append(f"\n*…and {len(entries) - limit} more (truncated).*")
    return lines


def _write_report(
    bucket_a: list[dict[str, Any]],
    bucket_b: list[dict[str, Any]],
    stats: dict[str, int],
    outputs_hash: str,
) -> None:
    by_sheet_b = Counter(e["sheet_slug"] for e in bucket_b)
    by_sheet_a = Counter(e["sheet_slug"] for e in bucket_a)

    lines = [
        "# Stub-cell audit baseline",
        "",
        f"**Generated:** {date.today().isoformat()}",
        "**Script:** `scripts/audit_stub_cells.py`",
        "**PRD:** `docs/PRD_Lineage_Trust_and_Monte_Carlo_2026-06-05.md` §10 Sprint 0 (L1.1)",
        f"**Model outputs hash:** `{outputs_hash}`",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|--------|------:|",
        f"| Grid-renderable sheets walked | {stats.get('sheets_walked', 0)} |",
        f"| Cells with finite display value | {stats.get('cells_with_display_value', 0)} |",
        f"| Classified derived/input (non-stub) | {stats.get('derived_or_input', 0)} |",
        f"| Classified stub (total) | {stats.get('stub_classified', 0)} |",
        f"| **Bucket (a)** — placeholder tabs (AI Stack, Valuation) | **{len(bucket_a)}** |",
        f"| **Bucket (b)** — computed-but-unresolved (the bug) | **{len(bucket_b)}** |",
        "",
        "## Interpretation",
        "",
        "- **Bucket (a):** Genuine stubs on placeholder audit views (`ai_stack`, `valuation`).",
        (
            "- **Bucket (b):** Grid renders a number but `enrich_lineage` returns "
            "`cell_kind == \"stub\"` because `_resolve_cell_context` failed to resolve "
            "`computed_value` (4-sheet resolver, exact-label match, accessor gaps — PRD §2.2)."
        ),
        "- Sprint 1 target: bucket (b) == 0.",
        "",
        "## Bucket (b) breakdown by sheet",
        "",
        "| Sheet slug | Count |",
        "|------------|------:|",
    ]
    for slug, count in sorted(by_sheet_b.items(), key=lambda x: -x[1]):
        lines.append(f"| `{slug}` | {count} |")
    if not by_sheet_b:
        lines.append("| *(none)* | 0 |")

    lines.extend(
        [
            "",
            "## Bucket (a) breakdown by sheet",
            "",
            "| Sheet slug | Count |",
            "|------------|------:|",
        ]
    )
    for slug, count in sorted(by_sheet_a.items(), key=lambda x: -x[1]):
        lines.append(f"| `{slug}` | {count} |")
    if not by_sheet_a:
        lines.append("| *(none)* | 0 |")

    lines.extend(
        [
            "",
            "## Bucket (b) sample (first 50)",
            "",
            "| # | Sheet | Row | Year | Lineage key | Grid value | Label |",
            "|---|-------|-----|------|-------------|------------|-------|",
            *_format_entries(bucket_b),
            "",
            "## Bucket (a) sample (first 20)",
            "",
            "| # | Sheet | Row | Year | Lineage key | Grid value | Label |",
            "|---|-------|-----|------|-------------|------------|-------|",
            *_format_entries(bucket_a, limit=20),
            "",
        ]
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    sys.path.insert(0, str(REPO_ROOT / "src"))

    from spacex_model.config.settings import get_settings
    from spacex_model.engine.pipeline import run_base_case

    workbook = get_settings().workbook_path
    if not workbook.exists():
        print(f"ERROR: workbook not found: {workbook}", file=sys.stderr)
        return 1

    print(f"Running base case ({workbook.name})…")
    result = run_base_case(workbook, write_outputs=False)
    outputs_hash = result.audit["outputs_hash"]

    bucket_a, bucket_b, stats = _collect_stub_cells(result)
    _write_report(bucket_a, bucket_b, stats, outputs_hash)

    print(f"Wrote {REPORT_PATH}")
    print(f"  cells with display value: {stats.get('cells_with_display_value', 0)}")
    print(f"  bucket (a) placeholder stubs: {len(bucket_a)}")
    print(f"  bucket (b) computed-but-unresolved: {len(bucket_b)}")
    print(f"  outputs_hash: {outputs_hash}")

    if len(bucket_b) > 0:
        print(
            f"WARNING: bucket (b) is {len(bucket_b)} — Sprint 1 target is 0.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
