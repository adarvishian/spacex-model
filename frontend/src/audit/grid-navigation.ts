import type { ActiveCell, GridPayload } from "../shared/types";

export function dataRows(payload: GridPayload) {
  return payload.rows.filter((r) => !r.is_header);
}

export function cellAt(
  payload: GridPayload,
  rowId: string,
  year: number,
): ActiveCell | null {
  const row = payload.rows.find((r) => r.row_id === rowId && !r.is_header);
  if (!row) return null;
  const yearIndex = payload.years.indexOf(year);
  if (yearIndex < 0) return null;
  return {
    rowId: row.row_id,
    rowIndex: row.row_index,
    label: row.label,
    year,
    yearIndex,
    lineageKey: row.lineage_keys[yearIndex],
    unit: row.unit,
    cellKind: row.cell_kinds[yearIndex],
  };
}

export function moveActiveCell(
  payload: GridPayload,
  active: ActiveCell,
  direction: "up" | "down" | "left" | "right",
): ActiveCell | null {
  const rows = dataRows(payload);
  const rowIdx = rows.findIndex((r) => r.row_id === active.rowId);
  if (rowIdx < 0) return null;

  if (direction === "left" || direction === "right") {
    const nextYearIdx =
      direction === "left"
        ? Math.max(0, active.yearIndex - 1)
        : Math.min(payload.years.length - 1, active.yearIndex + 1);
    if (nextYearIdx === active.yearIndex) return null;
    const year = payload.years[nextYearIdx];
    return cellAt(payload, active.rowId, year);
  }

  const nextRowIdx = direction === "up" ? rowIdx - 1 : rowIdx + 1;
  if (nextRowIdx < 0 || nextRowIdx >= rows.length) return null;
  const row = rows[nextRowIdx];
  return cellAt(payload, row.row_id, active.year);
}
