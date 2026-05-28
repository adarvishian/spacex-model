"""Audit grid payload builder — FRONTEND_PRD §8.2."""

from __future__ import annotations

import re
from typing import Any

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.engine.label_lookup import lookup_by_label
from spacex_model.engine.pipeline import ModelResult
from spacex_model.io.divergence import tolerance_for
from spacex_model.service.sheets_meta import SheetMeta, sheet_for_name

_YEARS = list(range(FIRST_YEAR, LAST_YEAR + 1))

# Known label → v0 lineage registry key
_LABEL_LINEAGE: dict[tuple[str, str], str] = {
    ("Starlink", "Total Revenue ($mm)"): "module.starlink.total_revenue",
    ("Starlink", "Module EBITDA ($mm)"): "module.starlink.module_ebitda",
    ("Starlink", "Module FCF ($mm)"): "module.starlink.module_fcf",
    ("Starlink", "Module CapEx ($mm)"): "module.starlink.module_capex",
    ("Starlink", "Module CapEx ($mm) — restated"): "module.starlink.module_capex",
    ("Starlink", "Blended IRR"): "module.starlink.blended_irr",
    ("Customer Launch", "Total Revenue ($mm)"): "module.customer_launch.total_revenue",
    ("Customer Launch", "Module FCF ($mm)"): "module.customer_launch.module_fcf",
    ("ODC", "Total Revenue ($mm)"): "module.odc.total_revenue",
    ("ODC", "Module FCF ($mm)"): "module.odc.module_fcf",
    ("AI Stack", "Total Revenue ($mm)"): "module.ai_stack.total_revenue",
    ("AI Stack", "Module FCF ($mm)"): "module.ai_stack.module_fcf",
    ("Lunar Mars", "Total Revenue ($mm)"): "module.lunar_mars.total_revenue",
    ("Lunar Mars", "Module FCF ($mm)"): "module.lunar_mars.module_fcf",
    ("Group P&L", "Group Revenue ($mm)"): "group.group_revenue_net",
    ("Group P&L", "Group EBITDA ($mm)"): "group.group_ebitda",
    ("Group P&L", "Group FCF ($mm)"): "group.group_fcf",
}

_INPUT_LABEL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"from Assumptions", re.I),
    re.compile(r"cash allocation \(\$mm\)$", re.I),
    re.compile(r"kg allocation", re.I),
    re.compile(r"Gbps per sat", re.I),
    re.compile(r"reserved %", re.I),
)


def _row_id(row_idx: int) -> str:
    return f"R{row_idx}"


def _infer_unit(label: str) -> str:
    lower = label.lower()
    if "irr" in lower or "%" in label or "margin" in lower:
        return "pct"
    if "kg" in lower and "allocation" in lower:
        return "kg_to_leo"
    if "gbps" in lower:
        return "gbps"
    if any(k in lower for k in ("sats", "launches", "boosters", "ships", "fleet", "subscribers")):
        return "count"
    if "$mm" in label or "($mm" in label or "revenue" in lower or "capex" in lower or "cogs" in lower:
        return "dollars_mm"
    return "ratio"


def _is_section_header(label: str) -> bool:
    return label.startswith("§") or label.startswith("▸") or label.isupper()


def _cell_kind(sheet: str, label: str, code_val: float | None) -> str:
    if _is_section_header(label):
        return "stub"
    if sheet == "Assumptions":
        return "input"
    if any(p.search(label) for p in _INPUT_LABEL_PATTERNS):
        return "input"
    if code_val is not None:
        return "derived"
    return "stub"


def _divergence_status(
    label: str,
    xlsx_val: float | None,
    code_val: float | None,
) -> tuple[str, float | None]:
    if code_val is None or xlsx_val is None:
        return "n_a", None
    tol = tolerance_for(label, xlsx_val)
    delta = code_val - xlsx_val
    if abs(delta) <= tol:
        return "match", delta
    # Phase 1: treat out-of-tolerance mapped cells as intentional (Sprint 11f Option A)
    return "intentional", delta


def _lineage_key(sheet: str, label: str, row_idx: int, year: int) -> str:
    mapped = _LABEL_LINEAGE.get((sheet, label))
    if mapped:
        return mapped
    slug = sheet_for_name(sheet)
    slug_part = slug.slug if slug else sheet.lower().replace(" ", "_")
    return f"grid.{slug_part}.{_row_id(row_idx)}.{year}"


def _section_ref(current_section: str, label: str) -> str:
    if _is_section_header(label):
        return label.lstrip("▸ ").strip()
    return current_section


def build_grid_payload(meta: SheetMeta, result: ModelResult) -> dict[str, Any]:
    """Build GridPayload for one sheet from a pipeline result."""
    sheet = meta.source_sheet
    ingest = result.ingest
    labels_map = ingest.value_pass.labels_by_sheet.get(sheet, {})
    cached = ingest.value_pass.cached_values

    rows: list[dict[str, Any]] = []
    current_section = f"§{meta.display_name} module"

    for row_idx in sorted(labels_map.keys()):
        label = labels_map[row_idx]
        if _is_section_header(label):
            current_section = _section_ref(current_section, label)

        year_values: list[float | None] = []
        cell_kinds: list[str] = []
        divergence_flags: list[str] = []
        lineage_keys: list[str] = []

        base_scalar = cached.get((sheet, row_idx, 2))
        if isinstance(base_scalar, (int, float)) and not _is_section_header(label):
            base_case_value: float | None = float(base_scalar)
        else:
            base_case_value = None

        for year in _YEARS:
            xlsx_raw = cached.get((sheet, row_idx, year))
            xlsx_val = float(xlsx_raw) if isinstance(xlsx_raw, (int, float)) else None
            code_val = None if _is_section_header(label) else lookup_by_label(result, sheet, label, year)
            display = code_val if code_val is not None else xlsx_val

            kind = _cell_kind(sheet, label, code_val)
            div_status, _ = _divergence_status(label, xlsx_val, code_val)

            year_values.append(display)
            cell_kinds.append(kind)
            divergence_flags.append(div_status)
            lineage_keys.append(_lineage_key(sheet, label, row_idx, year))

        rows.append(
            {
                "row_id": _row_id(row_idx),
                "row_index": row_idx,
                "label": label,
                "section_ref": current_section if not _is_section_header(label) else "",
                "unit": _infer_unit(label),
                "base_case_value": base_case_value,
                "year_values": year_values,
                "cell_kinds": cell_kinds,
                "divergence_flags": divergence_flags,
                "lineage_keys": lineage_keys,
                "is_header": _is_section_header(label),
            }
        )

    return {
        "sheet": meta.slug,
        "source_sheet": sheet,
        "years": _YEARS,
        "rows": rows,
    }
