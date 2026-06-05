"""Read cached xlsx values by canonical label — diagnostic / gate tests."""

from __future__ import annotations

import numpy as np

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.domain.year_vector import YearVector
from spacex_model.io.excel_ingest import IngestResult


def _row_for_label(ingest: IngestResult, sheet: str, label: str) -> int | None:
    labels = ingest.value_pass.labels_by_sheet.get(sheet, {})
    for row, text in labels.items():
        if text == label:
            return row
    return None


def label_year_value(ingest: IngestResult, sheet: str, label: str, year: int) -> float | None:
    """Return cached numeric value for (sheet, label, year) or None."""
    row = _row_for_label(ingest, sheet, label)
    if row is None:
        return None
    raw = ingest.value_pass.cached_values.get((sheet, row, year))
    if raw is None or not isinstance(raw, (int, float)):
        return None
    return float(raw)


def label_year_vector(ingest: IngestResult, sheet: str, label: str) -> YearVector:
    """Build horizon YearVector from cached xlsx values (0.0 if missing)."""
    row = _row_for_label(ingest, sheet, label)
    if row is None:
        return YearVector.zeros()
    vals = np.zeros(HORIZON_YEARS, dtype=np.float64)
    for t in range(HORIZON_YEARS):
        year = FIRST_YEAR + t
        raw = ingest.value_pass.cached_values.get((sheet, row, year))
        if isinstance(raw, (int, float)):
            vals[t] = float(raw)
    return YearVector(vals)
