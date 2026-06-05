import {
  AllCommunityModule,
  CellClickedEvent,
  CellClassParams,
  ColDef,
  FirstDataRenderedEvent,
  GridApi,
  ModuleRegistry,
} from "ag-grid-community";
import { AgGridReact } from "ag-grid-react";
import { forwardRef, useCallback, useEffect, useImperativeHandle, useMemo, useRef } from "react";
import type { GridDensity, NumberDisplayFormat } from "../shared/grid-prefs";
import type { ActiveCell, GridPayload } from "../shared/types";
import { formatGridNumber } from "../shared/format";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

ModuleRegistry.registerModules([AllCommunityModule]);

const YEAR_COL_MIN_WIDTH = 64;
const LABEL_COL_MIN_WIDTH = 280;
const LABEL_COL_MAX_WIDTH = 420;

export type GridHandle = {
  focusActiveCell: (cell: ActiveCell) => void;
  fitColumns: () => void;
  resetColumns: () => void;
};

type Props = {
  payload: GridPayload;
  activeCell: ActiveCell | null;
  onCellSelect: (cell: ActiveCell) => void;
  numberFormat?: NumberDisplayFormat;
  density?: GridDensity;
};

export function GridSkeleton({ rows = 14 }: { rows?: number }) {
  return (
    <div className="audit-grid-skeleton" data-testid="audit-grid-skeleton" aria-hidden="true">
      <div className="skeleton-header" />
      {Array.from({ length: rows }, (_, i) => (
        <div key={i} className="skeleton-row" />
      ))}
    </div>
  );
}

type GridRowData = Record<string, string | number | null | boolean>;

function fitYearColumns(api: GridApi<GridRowData>, years: number[]) {
  const colIds = years.map((y) => `y_${y}`);
  api.autoSizeColumns(colIds, false);
  const widths = colIds.map((id) => {
    const col = api.getColumn(id);
    const w = col?.getActualWidth() ?? YEAR_COL_MIN_WIDTH;
    return { key: id, newWidth: Math.max(w, YEAR_COL_MIN_WIDTH) };
  });
  api.setColumnWidths(widths);
}

function fitLabelColumn(api: GridApi<GridRowData>) {
  api.autoSizeColumns(["label"], false);
  const col = api.getColumn("label");
  const w = col?.getActualWidth() ?? LABEL_COL_MIN_WIDTH;
  const clamped = Math.min(Math.max(w, LABEL_COL_MIN_WIDTH), LABEL_COL_MAX_WIDTH);
  api.setColumnWidths([{ key: "label", newWidth: clamped }]);
}

const ROW_HEIGHT: Record<GridDensity, number> = {
  comfortable: 36,
  compact: 28,
};

export const Grid = forwardRef<GridHandle, Props>(function Grid(
  { payload, activeCell, onCellSelect, numberFormat = "mm", density = "compact" },
  ref,
) {
  const gridRef = useRef<AgGridReact<GridRowData>>(null);
  const apiRef = useRef<GridApi<GridRowData> | null>(null);

  const rowData = useMemo(() => {
    return payload.rows
      .filter((r) => !r.is_header)
      .map((row) => {
        const record: GridRowData = {
          row_id: row.row_id,
          row_index: row.row_index,
          label: row.label,
          unit: row.unit,
          _is_header: row.is_header,
        };
        payload.years.forEach((year, idx) => {
          record[`y_${year}`] = row.year_values[idx];
          record[`kind_${year}`] = row.cell_kinds[idx];
          record[`div_${year}`] = row.divergence_flags[idx];
          record[`key_${year}`] = row.lineage_keys[idx];
        });
        return record;
      });
  }, [payload]);

  const columnDefs = useMemo<ColDef<GridRowData>[]>(() => {
    const yearCols: ColDef<GridRowData>[] = payload.years.map((year) => ({
      colId: `y_${year}`,
      field: `y_${year}`,
      headerName: String(year),
      minWidth: YEAR_COL_MIN_WIDTH,
      type: "numericColumn",
      cellClass: (p: CellClassParams<GridRowData>) => {
        const classes = ["num-cell"];
        const kind = p.data?.[`kind_${year}`];
        const div = p.data?.[`div_${year}`];
        if (kind === "input") classes.push("input-cell");
        else classes.push("derived-cell");
        if (div === "drift" || div === "intentional") classes.push("divergence-cell");
        if (
          activeCell &&
          p.data?.row_id === activeCell.rowId &&
          year === activeCell.year
        ) {
          classes.push("active-cell");
        }
        return classes;
      },
      valueFormatter: (p) =>
        formatGridNumber(p.value as number | null, String(p.data?.unit ?? ""), numberFormat),
    }));

    return [
      {
        field: "row_id",
        headerName: "#",
        pinned: "left",
        width: 44,
        suppressSizeToFit: true,
        cellClass: "row-id-cell",
      },
      {
        field: "label",
        headerName: "Label",
        pinned: "left",
        minWidth: LABEL_COL_MIN_WIDTH,
        maxWidth: LABEL_COL_MAX_WIDTH,
        wrapText: true,
        autoHeight: true,
        tooltipField: "label",
        cellClass: "label-cell",
      },
      ...yearCols,
    ];
  }, [payload.years, activeCell, numberFormat]);

  const fitColumns = useCallback(() => {
    const api = apiRef.current;
    if (!api) return;
    fitYearColumns(api, payload.years);
    fitLabelColumn(api);
  }, [payload.years]);

  useImperativeHandle(ref, () => ({
    focusActiveCell(cell: ActiveCell) {
      const api = apiRef.current;
      if (!api) return;
      const rowIdx = rowData.findIndex((r) => r.row_id === cell.rowId);
      if (rowIdx < 0) return;
      api.ensureIndexVisible(rowIdx, "middle");
      const colId = `y_${cell.year}`;
      api.setFocusedCell(rowIdx, colId);
    },
    fitColumns: () => fitColumns(),
    resetColumns: () => fitColumns(),
  }));

  useEffect(() => {
    fitColumns();
  }, [fitColumns, payload.sheet, rowData, numberFormat]);

  useEffect(() => {
    if (activeCell) {
      const api = apiRef.current;
      if (!api) return;
      const rowIdx = rowData.findIndex((r) => r.row_id === activeCell.rowId);
      if (rowIdx >= 0) {
        api.ensureIndexVisible(rowIdx, "middle");
      }
    }
  }, [activeCell, rowData]);

  const onFirstDataRendered = useCallback(
    (_event: FirstDataRenderedEvent<GridRowData>) => {
      fitColumns();
    },
    [fitColumns],
  );

  const onCellClicked = (event: CellClickedEvent<GridRowData>) => {
    const field = event.colDef.field;
    if (!field?.startsWith("y_") || !event.data) return;
    const year = parseInt(field.slice(2), 10);
    const yearIndex = payload.years.indexOf(year);
    if (yearIndex < 0) return;
    onCellSelect({
      rowId: String(event.data.row_id),
      rowIndex: Number(event.data.row_index),
      label: String(event.data.label),
      year,
      yearIndex,
      lineageKey: String(event.data[`key_${year}`]),
      unit: String(event.data.unit),
      cellKind: event.data[`kind_${year}`] as ActiveCell["cellKind"],
      displayValue: (event.data[`y_${year}`] as number | null) ?? null,
    });
  };

  const rowHeight = ROW_HEIGHT[density];

  return (
    <div
      className={`audit-grid-wrap ag-theme-alpine-dark density-${density}`}
      data-testid="audit-grid"
      data-density={density}
      tabIndex={0}
      role="region"
      aria-label={`${payload.source_sheet} audit grid`}
      aria-describedby="grid-cell-legend"
    >
      <AgGridReact
        ref={gridRef}
        rowData={rowData}
        columnDefs={columnDefs}
        defaultColDef={{ sortable: false, filter: false, resizable: true }}
        onGridReady={(e) => {
          apiRef.current = e.api;
          fitColumns();
        }}
        onFirstDataRendered={onFirstDataRendered}
        onCellClicked={onCellClicked}
        suppressCellFocus={false}
        enableBrowserTooltips
        enableCellTextSelection
        getRowId={(p) => String(p.data.row_id)}
        getRowHeight={() => rowHeight}
        headerHeight={32}
        animateRows={false}
      />
    </div>
  );
});
