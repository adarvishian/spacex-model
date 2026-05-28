import {
  AllCommunityModule,
  CellClickedEvent,
  CellClassParams,
  ColDef,
  ModuleRegistry,
} from "ag-grid-community";
import { AgGridReact } from "ag-grid-react";
import { useMemo, useRef } from "react";
import type { ActiveCell, GridPayload } from "../shared/types";
import { formatGridNumber } from "../shared/format";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

ModuleRegistry.registerModules([AllCommunityModule]);

type Props = {
  payload: GridPayload;
  activeCell: ActiveCell | null;
  onCellSelect: (cell: ActiveCell) => void;
};

type GridRowData = Record<string, string | number | null | boolean>;

export function Grid({ payload, activeCell, onCellSelect }: Props) {
  const gridRef = useRef<AgGridReact<GridRowData>>(null);

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
      field: `y_${year}`,
      headerName: String(year),
      width: 72,
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
      valueFormatter: (p) => formatGridNumber(p.value as number | null, String(p.data?.unit ?? "")),
    }));

    return [
      {
        field: "row_id",
        headerName: "#",
        pinned: "left",
        width: 44,
        cellClass: "row-id-cell",
      },
      {
        field: "label",
        headerName: "Label",
        pinned: "left",
        width: 260,
        cellClass: "label-cell",
      },
      ...yearCols,
    ];
  }, [payload.years, activeCell]);

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
    });
  };

  return (
    <div className="audit-grid-wrap ag-theme-alpine-dark">
      <AgGridReact
        ref={gridRef}
        rowData={rowData}
        columnDefs={columnDefs}
        defaultColDef={{ sortable: false, filter: false, resizable: true }}
        onCellClicked={onCellClicked}
        suppressCellFocus={false}
        rowSelection={{ mode: "singleRow", checkboxes: false }}
        getRowId={(p) => String(p.data.row_id)}
        headerHeight={32}
        rowHeight={28}
        animateRows={false}
      />
    </div>
  );
}
