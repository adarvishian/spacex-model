"""Load xlsx cached-value cell index for divergence parametrization — PRD §7.6."""

from __future__ import annotations

from pathlib import Path

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.config.settings import get_settings
from spacex_model.io.excel_ingest import IngestResult, ingest_workbook


def load_xlsx_cached_cells_v216(
    workbook_path: Path | None = None,
    *,
    ingest: IngestResult | None = None,
) -> list[tuple[str, int, int]]:
    """Return (sheet, row, year) tuples for mapped cached numeric cells."""
    if ingest is None:
        path = workbook_path or get_settings().workbook_path
        ingest = ingest_workbook(path)

    labels_by_sheet = ingest.value_pass.labels_by_sheet
    cells: list[tuple[str, int, int]] = []
    for (sheet, row, year), value in ingest.value_pass.cached_values.items():
        if not isinstance(year, int) or year < FIRST_YEAR or year > LAST_YEAR:
            continue
        label = labels_by_sheet.get(sheet, {}).get(row)
        if not label or label.startswith("§") or label.startswith("▸"):
            continue
        if value is None or not isinstance(value, (int, float)):
            continue
        cells.append((sheet, row, year))
    return sorted(cells)
