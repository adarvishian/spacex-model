"""Extended lineage enrichment for audit derivation panel — FRONTEND_PRD §6.4."""

from __future__ import annotations

import logging
import re
from typing import Any

from spacex_model.config.constants import FIRST_YEAR
from spacex_model.engine.label_lookup import (
    find_label_row,
    labels_match,
    lookup_by_label,
    normalize_label,
)
from spacex_model.engine.pipeline import ModelResult
from spacex_model.inputs.s1_2025_anchors import S1_INGEST_ANCHORS_2025
from spacex_model.inputs.v4_131_2025_anchors import AnchorSpec
from spacex_model.io.divergence import tolerance_for
from spacex_model.service.grid import (
    _INPUT_LABEL_PATTERNS,
    _LABEL_LINEAGE,
    _infer_unit,
    resolve_cell_values,
)
from spacex_model.service.lineage import LineageEntry, lookup_lineage
from spacex_model.service.methodology_registry import lookup_methodology
from spacex_model.service.sheets_meta import SHEETS, get_sheet, sheet_for_name
from spacex_model.service.stub_registry import (
    is_registered_stub,
    slug_for_sheet_row,
    stub_spec_section,
)

_log = logging.getLogger(__name__)

_UPSTREAM_HINTS: dict[str, list[dict[str, str]]] = {
    "module.starlink.total_revenue": [
        {"key": "grid.starlink.R5", "label": "Starlink!R5 · V2 BB active sats"},
        {"key": "grid.assumptions.R142", "label": "Assumptions · V2 BB ARPU"},
        {"key": "grid.starlink.R26", "label": "Starlink!R26 · Starshield revenue"},
    ],
    "module.starlink.module_ebitda": [
        {"key": "module.starlink.total_revenue", "label": "Starlink Total Revenue"},
        {"key": "grid.starlink.R9", "label": "Starlink!R9 · Total COGS"},
    ],
}

_DOWNSTREAM_HINTS: dict[str, list[dict[str, str]]] = {
    "module.starlink.total_revenue": [
        {"key": "group.group_revenue_net", "label": "Group P&L · Group Revenue"},
        {"key": "grid.starlink_capacity.D12", "label": "Starlink Cap · Gbps capacity"},
        {"key": "valuation.implied_ev_2025", "label": "Valuation · Starlink SoTP"},
    ],
    "module.starlink.module_ebitda": [
        {"key": "module.starlink.module_fcf", "label": "Starlink Module FCF"},
    ],
}

_LIFECYCLE_BY_KEY: dict[str, str] = {
    "module.starlink.total_revenue": "output",
    "module.starlink.module_ebitda": "pnl",
    "module.starlink.module_fcf": "pnl",
    "module.starlink.module_capex": "output",
    "module.starlink.blended_irr": "output",
    "group.group_revenue_net": "pnl",
    "group.group_ebitda": "pnl",
    "group.group_fcf": "conservation",
}


def _default_inputs(key: str) -> tuple[str, ...]:
    defaults: dict[str, tuple[str, ...]] = {
        "module.starlink.total_revenue": (
            "V2 BB active sats",
            "V2 BB ARPU",
            "Starshield revenue",
        ),
        "module.starlink.module_ebitda": ("Total Revenue ($mm)", "Total COGS ($mm)"),
        "module.starlink.module_fcf": ("Module EBITDA ($mm)", "Module CapEx ($mm)"),
    }
    return defaults.get(key, ())


def _is_input_label(label: str) -> bool:
    return any(p.search(label) for p in _INPUT_LABEL_PATTERNS)


def _grid_key(sheet: str, row: int, year: int) -> str:
    slug = sheet_for_name(sheet)
    slug_part = slug.slug if slug else sheet.lower().replace(" ", "_")
    return f"grid.{slug_part}.R{row}.{year}"


def _find_label_row(sheet: str, label: str, result: ModelResult) -> int | None:
    labels = result.ingest.value_pass.labels_by_sheet.get(sheet, {})
    return find_label_row(labels, label)


def _resolve_label_to_grid_key(label: str, year: int, result: ModelResult) -> tuple[str, str] | None:
    """Return (lineage_key, display_label) for a canonical label on any grid sheet."""
    ingest = result.ingest
    for meta in SHEETS:
        if meta.slug == "run_audit":
            continue
        sheet = meta.source_sheet
        labels = ingest.value_pass.labels_by_sheet.get(sheet, {})
        for row_idx, lbl in labels.items():
            if meta.row_range is not None:
                lo, hi = meta.row_range
                if row_idx < lo or row_idx > hi:
                    continue
            if not labels_match(lbl, label):
                continue
            return (
                f"grid.{meta.slug}.R{row_idx}.{year}",
                f"{sheet}!R{row_idx} · {lbl}",
            )
    return None


def _classify_cell_kind(
    *,
    sheet_slug: str | None,
    source_sheet: str,
    label: str,
    display_val: float | None,
    lineage_key: str,
) -> str:
    if is_registered_stub(
        sheet_slug=sheet_slug,
        source_sheet=source_sheet,
        label=label,
        lineage_key=lineage_key,
    ):
        return "stub"
    if source_sheet == "Assumptions" or _is_input_label(label):
        return "input"
    if display_val is not None:
        return "derived"
    return "stub"


def _lookup_upstream_for_key(
    key: str,
    result: ModelResult,
    *,
    sheet_name: str,
    label: str,
    year: int,
) -> list[dict[str, str]]:
    upstream = _UPSTREAM_HINTS.get(key, [])
    if upstream:
        return upstream

    reg_key = _LABEL_LINEAGE.get((sheet_name, label))
    if reg_key:
        upstream = _UPSTREAM_HINTS.get(reg_key, [])
        if upstream:
            return upstream

    if sheet_name != "Assumptions" and _is_input_label(label):
        row = _find_label_row("Assumptions", label, result)
        if row is not None:
            return [
                {
                    "key": _grid_key("Assumptions", row, year),
                    "label": f"Assumptions!R{row} · {label}",
                }
            ]

    return []


def _parse_grid_key(key: str) -> tuple[str, int, int] | None:
    """Parse grid.{slug}.R{row}.{year} synthetic keys."""
    parts = key.split(".")
    if len(parts) < 4 or parts[0] != "grid":
        return None
    row_part = parts[2]
    if not row_part.startswith("R"):
        return None
    try:
        row = int(row_part[1:])
        year = int(parts[3])
    except ValueError:
        return None
    slug = parts[1]
    sheet_meta = get_sheet(slug)
    if sheet_meta is None:
        return None
    return sheet_meta.source_sheet, row, year


def _resolve_cell_context(
    key: str,
    result: ModelResult,
    *,
    year: int | None = None,
    sheet: str | None = None,
    row: int | None = None,
) -> tuple[str, str, int, float | None, float | None, float | None, str | None]:
    """Return (sheet, label, year, code_value, xlsx_value, display_value, sheet_slug)."""
    ingest = result.ingest
    resolved_year = year or FIRST_YEAR
    sheet_slug: str | None = None

    if sheet and row:
        labels = ingest.value_pass.labels_by_sheet.get(sheet, {})
        label = labels.get(row, key)
        sheet_slug = slug_for_sheet_row(sheet, row)
        code, xlsx, display = resolve_cell_values(result, sheet, label, row, resolved_year)
        return sheet, label, resolved_year, code, xlsx, display, sheet_slug

    parsed = _parse_grid_key(key)
    if parsed:
        s, r, y = parsed
        if year is not None:
            y = year
        labels = ingest.value_pass.labels_by_sheet.get(s, {})
        label = labels.get(r, key)
        slug = key.split(".")[1] if key.startswith("grid.") else ""
        meta = get_sheet(slug)
        sheet_slug = meta.slug if meta else slug_for_sheet_row(s, r)
        code, xlsx, display = resolve_cell_values(result, s, label, r, y)
        return s, label, y, code, xlsx, display, sheet_slug

    # Registry key — find label from reverse map
    for (s, lbl), reg_key in _LABEL_LINEAGE.items():
        if reg_key == key:
            y = year or FIRST_YEAR
            xlsx_row = _find_label_row(s, lbl, result)
            code, xlsx, display = (
                (None, None, None)
                if xlsx_row is None
                else resolve_cell_values(result, s, lbl, xlsx_row, y)
            )
            if code is None and xlsx_row is not None:
                code = lookup_by_label(result, s, lbl, y)
                if code is not None and display is None:
                    display = code
            sheet_slug = slug_for_sheet_row(s, xlsx_row) if xlsx_row is not None else None
            return s, lbl, y, code, xlsx, display, sheet_slug

    return "", key, resolved_year, None, None, None, sheet_slug


def enrich_lineage(
    key: str,
    result: ModelResult,
    *,
    year: int | None = None,
    sheet: str | None = None,
    row: int | None = None,
    sheet_slug: str | None = None,
) -> dict[str, Any]:
    """Return extended LineageEntry payload per FRONTEND_PRD §6.4."""
    base = lookup_lineage(key)
    if base is None:
        for (s, lbl), reg_key in _LABEL_LINEAGE.items():
            if reg_key == key:
                base = LineageEntry(
                    key=key,
                    display_name=lbl,
                    module_path=f"spacex_model.calc.{s.lower().replace(' ', '_')}",
                    function="compute_allocator_out",
                    excel_cell=f"{s}!—",
                    excel_label=lbl,
                    architecture_ref="§8 Starlink module" if s == "Starlink" else "§3 vending-machine framing",
                    principle="7 (Module EBITDA = Gross Profit)" if "Revenue" in lbl else "8 (module FCF pre-tax, pre-corp)",
                    input_labels=_default_inputs(key),
                )
                break

    sheet_name, label, cell_year, code_val, xlsx_val, display_val, inferred_slug = (
        _resolve_cell_context(key, result, year=year, sheet=sheet, row=row)
    )
    if sheet_slug is None:
        sheet_slug = inferred_slug
    if sheet_slug is None and key.startswith("grid."):
        meta = get_sheet(key.split(".")[1])
        if meta is not None:
            sheet_slug = meta.slug

    if display_val is None and not is_registered_stub(
        sheet_slug=sheet_slug,
        source_sheet=sheet_name,
        label=label,
        lineage_key=key,
    ):
        _log.warning(
            "lineage resolver: no display value for non-stub cell %s (%s!%s · %s)",
            key,
            sheet_name,
            row,
            label,
        )

    if base is None and key.startswith("grid."):
        base = LineageEntry(
            key=key,
            display_name=label,
            module_path="spacex_model.engine.label_lookup",
            function="lookup_by_label",
            excel_cell=f"{sheet_name}!{_row_label(sheet_name, label, result)}",
            excel_label=label,
            architecture_ref="§8 Starlink module" if sheet_name == "Starlink" else "",
            principle="",
            input_labels=(),
        )
    elif base is None:
        raise KeyError(key)

    unit = _infer_unit(label if label else base.excel_label)

    div_status = "n_a"
    div_delta: float | None = None
    if code_val is not None and xlsx_val is not None:
        tol = tolerance_for(label or base.excel_label, xlsx_val)
        div_delta = code_val - xlsx_val
        div_status = "match" if abs(div_delta) <= tol else "intentional"

    cell_kind = _classify_cell_kind(
        sheet_slug=sheet_slug,
        source_sheet=sheet_name,
        label=label,
        display_val=display_val,
        lineage_key=key,
    )
    stub_section = (
        stub_spec_section(
            sheet_slug=sheet_slug,
            label=label,
            architecture_ref=base.architecture_ref,
            section_ref=_section_for_label(sheet_name, label, result),
        )
        if cell_kind == "stub"
        else None
    )

    lifecycle = _LIFECYCLE_BY_KEY.get(key, "output")
    section_ref = _section_for_label(sheet_name, label, result)

    formula = _resolve_formula(
        key=key,
        base=base,
        cell_kind=cell_kind,
        stub_section=stub_section,
        sheet_name=sheet_name,
        label=label,
        architecture_section=_architecture_section_for_methodology(base, sheet_name),
    )

    resolved_inputs = _build_resolved_inputs(base, result, cell_year)
    upstream = _lookup_upstream_for_key(
        key,
        result,
        sheet_name=sheet_name,
        label=label,
        year=cell_year,
    )
    if not upstream and resolved_inputs:
        upstream = [
            {
                "key": ri["lineage_key"],
                "label": ri.get("cell_address") or ri["label"],
            }
            for ri in resolved_inputs
            if ri.get("lineage_key") and not str(ri["lineage_key"]).startswith("grid.resolved")
        ]
    downstream = _DOWNSTREAM_HINTS.get(key, [])

    payload = base.to_dict()
    payload.update(
        {
            "cell_address": {
                "sheet": sheet_name or base.excel_cell.split("!")[0] if "!" in base.excel_cell else "",
                "row": _row_label(sheet_name, label, result),
                "column": str(cell_year),
                "year": cell_year,
            },
            "cell_kind": cell_kind,
            "stub_spec_section": stub_section,
            "unit": unit,
            "formula_expression": formula,
            "resolved_inputs": resolved_inputs,
            "computed_value": display_val,
            "xlsx_cached_value": xlsx_val,
            "divergence_status": div_status,
            "divergence_delta_mm": div_delta,
            "lifecycle_stage": lifecycle,
            "section_ref": section_ref,
            "upstream_keys": [u["key"] for u in upstream],
            "downstream_keys": [d["key"] for d in downstream],
            "upstream": upstream,
            "downstream": downstream,
            "sources": _build_sources(
                base,
                sheet_name,
                label,
                code_val,
                xlsx_val,
                cell_year,
                key=key,
                architecture_section=_architecture_section_for_methodology(base, sheet_name),
                cell_kind=cell_kind,
            ),
        }
    )
    return payload


def _architecture_section_for_methodology(base: LineageEntry, sheet_name: str) -> str:
    """Map a cell to an Architecture § section — not the Excel row-group banner."""
    ref = base.architecture_ref or ""
    token = re.search(r"§\d+(?:\.\d+)?", ref)
    if token:
        return token.group(0)
    sheet_defaults: dict[str, str] = {
        "Assumptions": "§3",
        "Launch Capacity": "§6",
        "Customer Launch": "§8",
        "Starlink": "§8",
        "Starlink Capacity": "§8",
        "AI - Compute": "§8",
        "ODC": "§8",
        "Lunar - Mars": "§8",
        "Cash Allocation Engine": "§6",
        "OpEx": "§15",
        "CapEx": "§15",
        "Group P&L": "§15",
        "Demand Curves": "§8",
    }
    return sheet_defaults.get(sheet_name, "§3")


def _resolve_formula(
    *,
    key: str,
    base: LineageEntry,
    cell_kind: str,
    stub_section: str | None,
    sheet_name: str,
    label: str,
    architecture_section: str,
) -> str:
    """Formula from methodology registry; Architecture placeholder only for stubs."""
    if cell_kind == "stub":
        section = stub_section or base.architecture_ref or "spec"
        return f"{base.excel_label} — see Architecture {section}"

    if cell_kind == "input":
        return f"{label or base.excel_label} — exogenous input"

    rec = lookup_methodology(
        key,
        sheet=sheet_name or None,
        label=label or base.excel_label,
        section_ref=architecture_section,
    )
    if rec and rec.formula_expression.strip():
        return rec.formula_expression

    arch = architecture_section or base.architecture_ref or "§3"
    return f"{base.excel_label} = computed per {arch}"


def _match_ingest_anchor(label: str) -> AnchorSpec | None:
    norm = normalize_label(label)
    for anchor in S1_INGEST_ANCHORS_2025:
        if anchor.assumptions_label and labels_match(anchor.assumptions_label, label):
            return anchor
        if labels_match(anchor.name, label) or normalize_label(anchor.name) == norm:
            return anchor
    return None


def _row_label(sheet_name: str, label: str, result: ModelResult) -> str:
    labels = result.ingest.value_pass.labels_by_sheet.get(sheet_name, {})
    for row_idx, lbl in labels.items():
        if labels_match(lbl, label):
            return f"R{row_idx}"
    return "—"


def _section_for_label(sheet_name: str, label: str, result: ModelResult) -> str:
    labels = result.ingest.value_pass.labels_by_sheet.get(sheet_name, {})
    current = f"§{sheet_name}"
    for _, lbl in sorted(labels.items()):
        if lbl.startswith("▸"):
            current = lbl.lstrip("▸ ").strip()
        if labels_match(lbl, label):
            return current
    return current


def _build_sources(
    base: LineageEntry,
    sheet_name: str,
    label: str,
    code_val: float | None,
    xlsx_val: float | None,
    year: int,
    *,
    key: str,
    architecture_section: str,
    cell_kind: str,
) -> dict[str, Any]:
    rec = lookup_methodology(
        key,
        sheet=sheet_name or None,
        label=label or base.excel_label,
        section_ref=architecture_section,
    )
    if rec:
        methodology: dict[str, str] = {
            "spec_section": rec.architecture_section,
            "method_statement": rec.method_statement,
            "principle": rec.principle,
            "rule": rec.rule,
        }
    elif cell_kind == "stub":
        section = base.architecture_ref or architecture_section or "spec"
        methodology = {
            "spec_section": section,
            "method_statement": f"Planned implementation per Architecture {section}",
            "principle": base.principle or "—",
            "rule": "Not yet implemented — placeholder tab",
        }
    else:
        arch = architecture_section or base.architecture_ref or "§3"
        methodology = {
            "spec_section": arch,
            "method_statement": f"Computed per Architecture {arch}",
            "principle": base.principle or "8 (vending-machine module framing)",
            "rule": "Rule 1 — One concept per write; every formula traces to its source cell",
        }

    sources: dict[str, Any] = {"methodology": methodology}

    anchor = _match_ingest_anchor(label)
    is_input = cell_kind == "input" or sheet_name == "Assumptions" or _is_input_label(label)

    if is_input:
        if anchor:
            tol = (
                f"±{anchor.tolerance_pct:.0%}"
                if anchor.tolerance_pct > 0
                else "exact"
            )
            sources["input_provenance"] = {
                "source": "S-1 disclosure / V4.113 ingest anchor",
                "reference": f"{anchor.name} — target {anchor.target:,.2f} ({tol})",
            }
        elif sheet_name == "Assumptions" or base.key.startswith("grid.assumptions"):
            sources["input_provenance"] = {
                "source": "Assumptions sheet",
                "reference": "Exogenous model input (not derived from other tabs)",
            }
        elif _is_input_label(label):
            sources["input_provenance"] = {
                "source": "Assumptions cross-reference",
                "reference": "Input row sourced from Assumptions tab",
            }

    if year == 2025 and anchor and code_val is not None:
        sources["calibration_anchor"] = {
            "target": anchor.target,
            "tolerance_pct": anchor.tolerance_pct,
            "basis": f"S-1 ingest anchor · code lands {code_val:,.2f}",
        }
    elif year == 2025 and code_val is not None and xlsx_val is not None:
        sources["calibration_anchor"] = {
            "target": xlsx_val,
            "tolerance_pct": 0.05,
            "basis": f"2025 xlsx cached · code lands {code_val:,.0f}",
        }

    return sources


def _build_resolved_inputs(
    base: LineageEntry,
    result: ModelResult,
    year: int,
) -> list[dict[str, Any]]:
    """Build depth-1 resolved inputs from lineage input_labels."""
    out: list[dict[str, Any]] = []
    for idx, inp_label in enumerate(base.input_labels):
        val = lookup_by_label(result, "Starlink", inp_label, year)
        if val is None and "Revenue" in inp_label:
            val = lookup_by_label(result, "Starlink", "Total Revenue ($mm)", year)
        resolved = _resolve_label_to_grid_key(inp_label, year, result)
        if resolved:
            lineage_key, cell_address = resolved
            unit = _infer_unit(inp_label)
        else:
            lineage_key = f"grid.resolved.{idx}"
            cell_address = "—"
            unit = "dollars_mm"
        out.append(
            {
                "label": inp_label,
                "cell_address": cell_address,
                "value": val,
                "unit": unit,
                "lineage_key": lineage_key,
            }
        )
    if not out and base.key == "module.starlink.total_revenue":
        pools = result.vehicle_pools
        if pools is not None:
            v2_sats = float(pools.v2_bb.active_fleet.at(year))
            out.append(
                {
                    "label": "V2 BB active sats",
                    "cell_address": "Starlink!R5",
                    "value": v2_sats,
                    "unit": "count",
                    "lineage_key": "grid.starlink.R5",
                }
            )
        rev = lookup_by_label(result, "Starlink", "Starshield revenue ($mm)", year)
        if rev is not None:
            out.append(
                {
                    "label": "Starshield revenue",
                    "cell_address": "Starlink!R26",
                    "value": rev,
                    "unit": "dollars_mm",
                    "lineage_key": "grid.starlink.R26",
                }
            )
    return out
