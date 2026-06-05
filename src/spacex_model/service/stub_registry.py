"""Explicit registry of true stub cells — PRD Lineage Trust L1.4.

Only cells listed here (or on placeholder audit views) render as planned stubs.
Lookup failure must never imply stub.
"""

from __future__ import annotations

import re

from spacex_model.service.sheets_meta import SHEETS

# Placeholder audit views per context.md §2.4 — AI Stack, Valuation.
PLACEHOLDER_SLUGS: frozenset[str] = frozenset({"ai_stack", "valuation"})

_STUB_SPEC_BY_SLUG: dict[str, str] = {
    "ai_stack": "§7 AI Stack",
    "valuation": "§11 Valuation",
}

_SECTION_HEADER = re.compile(r"^(§|▸)")


def _is_section_header(label: str) -> bool:
    return bool(_SECTION_HEADER.match(label.strip())) or label.strip().isupper()


def stub_spec_section(
    *,
    sheet_slug: str | None = None,
    label: str | None = None,
    architecture_ref: str | None = None,
    section_ref: str | None = None,
) -> str:
    """Human-readable spec pointer for a planned stub panel."""
    if sheet_slug and sheet_slug in _STUB_SPEC_BY_SLUG:
        return _STUB_SPEC_BY_SLUG[sheet_slug]
    if section_ref:
        return section_ref
    if architecture_ref:
        return architecture_ref
    if label and _is_section_header(label):
        return label.lstrip("▸ ").strip()
    return "architecture spec"


def is_registered_stub(
    *,
    sheet_slug: str | None = None,
    source_sheet: str | None = None,
    row: int | None = None,
    label: str | None = None,
    lineage_key: str | None = None,
) -> bool:
    """Return True iff the cell is a genuine stub (placeholder tab or section banner)."""
    del row, lineage_key  # reserved for future row-level registry entries

    if label and _is_section_header(label):
        return True

    if sheet_slug and sheet_slug in PLACEHOLDER_SLUGS:
        return True

    if source_sheet:
        for meta in SHEETS:
            if meta.slug in PLACEHOLDER_SLUGS and meta.source_sheet == source_sheet:
                if sheet_slug is None or sheet_slug == meta.slug:
                    return True

    return False


def slug_for_sheet_row(source_sheet: str, row: int) -> str | None:
    """Resolve audit slug for a workbook row (handles row-range slices)."""
    matches = [m for m in SHEETS if m.source_sheet == source_sheet and m.slug != "run_audit"]
    if not matches:
        return None
    for meta in matches:
        if meta.row_range is not None:
            lo, hi = meta.row_range
            if lo <= row <= hi:
                return meta.slug
    for meta in matches:
        if meta.row_range is None:
            return meta.slug
    return matches[0].slug
