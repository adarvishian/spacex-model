"""Diagnostic snapshot store for xlsx value-pass (R0: V4.113 JSON snapshot)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS, LAST_YEAR
from spacex_model.io.excel_ingest import IngestResult


def _serialize_value(value: Any) -> Any:
    if isinstance(value, float):
        return value
    if isinstance(value, (int, str, bool)) or value is None:
        return value
    return str(value)


def ingest_to_snapshot_dict(ingest: IngestResult) -> dict[str, Any]:
    """Full diagnostic snapshot metadata for divergence triage."""
    labels_by_sheet = ingest.value_pass.labels_by_sheet
    label_rows: dict[str, dict[str, int]] = {}
    duplicate_labels: list[str] = []
    for sheet, labels in labels_by_sheet.items():
        sheet_map: dict[str, int] = {}
        for row_idx, label in labels.items():
            if label in sheet_map and sheet_map[label] != row_idx:
                duplicate_labels.append(f"{sheet}: duplicate label {label!r}")
            sheet_map[label] = row_idx
        label_rows[sheet] = sheet_map

    year_coverage: dict[int, int] = {}
    for (_sheet, _row, year), value in ingest.value_pass.cached_values.items():
        if isinstance(year, int) and FIRST_YEAR <= year <= LAST_YEAR and value is not None:
            year_coverage[year] = year_coverage.get(year, 0) + 1

    return {
        "workbook": str(ingest.workbook_path),
        "workbook_version": ingest.workbook_path.name,
        "horizon": {
            "first_year": FIRST_YEAR,
            "last_year": LAST_YEAR,
            "years": HORIZON_YEARS,
        },
        "sheet_names": ingest.formula_pass.sheet_names,
        "label_count_by_sheet": {s: len(lbls) for s, lbls in labels_by_sheet.items()},
        "label_rows": label_rows,
        "duplicate_labels": duplicate_labels,
        "assumption_rows": len(ingest.value_pass.assumptions_rows),
        "formula_cells": len(ingest.formula_pass.formulas),
        "cached_value_count": len(ingest.value_pass.cached_values),
        "year_value_coverage": {str(y): year_coverage.get(y, 0) for y in range(FIRST_YEAR, LAST_YEAR + 1)},
        "warnings": ingest.value_pass.warnings,
        "demand_curves": {
            "bb_breakpoints": len(ingest.demand_curves.bb_breakpoints) if ingest.demand_curves else 0,
            "dtc_breakpoints": len(ingest.demand_curves.dtc_breakpoints) if ingest.demand_curves else 0,
        },
        "sample_assumptions": [
            {
                "label": r.label,
                "base_case": _serialize_value(r.base_case),
                "y2025": _serialize_value(r.year_values.get(2025)),
            }
            for r in ingest.value_pass.assumptions_rows[:8]
        ],
    }


def write_diagnostic_snapshot(ingest: IngestResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ingest_to_snapshot_dict(ingest), indent=2), encoding="utf-8")
