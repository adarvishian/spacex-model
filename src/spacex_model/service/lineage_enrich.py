"""Extended lineage enrichment for audit derivation panel — FRONTEND_PRD §6.4."""

from __future__ import annotations

from typing import Any

from spacex_model.config.constants import FIRST_YEAR
from spacex_model.engine.label_lookup import lookup_by_label
from spacex_model.engine.pipeline import ModelResult
from spacex_model.io.divergence import tolerance_for
from spacex_model.service.grid import _LABEL_LINEAGE, _infer_unit
from spacex_model.service.lineage import LineageEntry, lookup_lineage
from spacex_model.service.sheets_meta import get_sheet

_FORMULA_EXPRESSIONS: dict[str, str] = {
    "module.starlink.total_revenue": (
        "Total Revenue (Starlink) = Σ over { V2 BB, V2 DTC, V3 BB, V3 DTC, Starshield } of "
        "active_sats(pool, t) × ARPU(pool, t) × months_active(pool, t)"
    ),
    "module.starlink.module_ebitda": "Module EBITDA = Total Revenue − Total COGS",
    "module.starlink.module_fcf": "Module FCF = Module EBITDA − Module CapEx + D&A add-back",
    "module.starlink.module_capex": "Module CapEx = Σ vehicle-pool sat CapEx + facility CapEx (1-yr lag)",
    "module.starlink.blended_irr": "Blended IRR = IRR-weighted blend of per-vehicle pool IRRs",
    "group.group_revenue_net": "Group Revenue = Σ module revenues − inter-module eliminations",
    "group.group_ebitda": "Group EBITDA = Group Gross Profit − Total OpEx",
    "group.group_fcf": "Group FCF = NOPAT + D&A − Total Group CapEx − Mars carve-out",
}

# Static 1-hop graph hints per lineage key (Phase 1 — full graph in Phase 2)
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
) -> tuple[str, str, int, float | None, float | None]:
    """Return (sheet_name, label, year, code_value, xlsx_value)."""
    ingest = result.ingest
    resolved_year = year or FIRST_YEAR

    if sheet and row:
        labels = ingest.value_pass.labels_by_sheet.get(sheet, {})
        label = labels.get(row, key)
        code = lookup_by_label(result, sheet, label, resolved_year)
        xlsx_raw = ingest.value_pass.cached_values.get((sheet, row, resolved_year))
        xlsx = float(xlsx_raw) if isinstance(xlsx_raw, (int, float)) else None
        return sheet, label, resolved_year, code, xlsx

    parsed = _parse_grid_key(key)
    if parsed:
        s, r, y = parsed
        if year is not None:
            y = year
        labels = ingest.value_pass.labels_by_sheet.get(s, {})
        label = labels.get(r, key)
        code = lookup_by_label(result, s, label, y)
        xlsx_raw = ingest.value_pass.cached_values.get((s, r, y))
        xlsx = float(xlsx_raw) if isinstance(xlsx_raw, (int, float)) else None
        return s, label, y, code, xlsx

    # Registry key — find label from reverse map
    for (s, lbl), reg_key in _LABEL_LINEAGE.items():
        if reg_key == key:
            y = year or FIRST_YEAR
            code = lookup_by_label(result, s, lbl, y)
            xlsx_row = next(
                (
                    ri
                    for ri, ln in ingest.value_pass.labels_by_sheet.get(s, {}).items()
                    if ln == lbl
                ),
                None,
            )
            xlsx = None
            if xlsx_row is not None:
                raw = ingest.value_pass.cached_values.get((s, xlsx_row, y))
                xlsx = float(raw) if isinstance(raw, (int, float)) else None
            return s, lbl, y, code, xlsx

    return "", key, resolved_year, None, None


def enrich_lineage(
    key: str,
    result: ModelResult,
    *,
    year: int | None = None,
    sheet: str | None = None,
    row: int | None = None,
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

    sheet_name, label, cell_year, code_val, xlsx_val = _resolve_cell_context(
        key, result, year=year, sheet=sheet, row=row
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
    formula = _FORMULA_EXPRESSIONS.get(
        key,
        f"{base.excel_label} — see Architecture {base.architecture_ref or 'spec'}",
    )

    div_status = "n_a"
    div_delta: float | None = None
    if code_val is not None and xlsx_val is not None:
        tol = tolerance_for(label or base.excel_label, xlsx_val)
        div_delta = code_val - xlsx_val
        div_status = "match" if abs(div_delta) <= tol else "intentional"

    lifecycle = _LIFECYCLE_BY_KEY.get(key, "output")
    section_ref = _section_for_label(sheet_name, label, result)

    resolved_inputs = _build_resolved_inputs(base, result, cell_year)
    upstream = _UPSTREAM_HINTS.get(key, [])
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
            "cell_kind": "derived" if code_val is not None else "stub",
            "unit": unit,
            "formula_expression": formula,
            "resolved_inputs": resolved_inputs,
            "computed_value": code_val,
            "xlsx_cached_value": xlsx_val,
            "divergence_status": div_status,
            "divergence_delta_mm": div_delta,
            "lifecycle_stage": lifecycle,
            "section_ref": section_ref,
            "upstream_keys": [u["key"] for u in upstream],
            "downstream_keys": [d["key"] for d in downstream],
            "upstream": upstream,
            "downstream": downstream,
            "sources": {
                "methodology": {
                    "spec_section": base.architecture_ref or "Architecture spec",
                    "principle": base.principle or "—",
                    "rule": base.principle or "—",
                },
            },
        }
    )
    return payload


def _row_label(sheet_name: str, label: str, result: ModelResult) -> str:
    labels = result.ingest.value_pass.labels_by_sheet.get(sheet_name, {})
    for row_idx, lbl in labels.items():
        if lbl == label:
            return f"R{row_idx}"
    return "—"


def _section_for_label(sheet_name: str, label: str, result: ModelResult) -> str:
    labels = result.ingest.value_pass.labels_by_sheet.get(sheet_name, {})
    current = f"§{sheet_name}"
    for _, lbl in sorted(labels.items()):
        if lbl.startswith("▸"):
            current = lbl.lstrip("▸ ").strip()
        if lbl == label:
            return current
    return current


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
        out.append(
            {
                "label": inp_label,
                "cell_address": f"—",
                "value": val,
                "unit": "dollars_mm",
                "lineage_key": f"grid.resolved.{idx}",
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
