"""Diagnostic snapshot store for xlsx value-pass (Phase A: JSON; parquet in Phase E)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from spacex_model.io.excel_ingest import IngestResult


def _serialize_value(value: Any) -> Any:
    if isinstance(value, float):
        return value
    if isinstance(value, (int, str, bool)) or value is None:
        return value
    return str(value)


def ingest_to_snapshot_dict(ingest: IngestResult) -> dict[str, Any]:
    return {
        "workbook": str(ingest.workbook_path),
        "assumption_rows": len(ingest.value_pass.assumptions_rows),
        "formula_cells": len(ingest.formula_pass.formulas),
        "cached_value_count": len(ingest.value_pass.cached_values),
        "warnings": ingest.value_pass.warnings,
        "sample_assumptions": [
            {
                "label": r.label,
                "base_case": _serialize_value(r.base_case),
                "y2025": _serialize_value(r.year_values.get(2025)),
            }
            for r in ingest.value_pass.assumptions_rows[:5]
        ],
    }


def write_diagnostic_snapshot(ingest: IngestResult, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ingest_to_snapshot_dict(ingest), indent=2), encoding="utf-8")
