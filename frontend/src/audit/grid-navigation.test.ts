import { describe, expect, it } from "vitest";
import { cellAt, dataRows, moveActiveCell } from "./grid-navigation";
import type { ActiveCell, GridPayload } from "../shared/types";

const payload: GridPayload = {
  sheet: "starlink",
  source_sheet: "Starlink",
  years: [2025, 2026],
  rows: [
    {
      row_id: "hdr",
      row_index: 0,
      label: "Header",
      section_ref: "",
      unit: "",
      base_case_value: null,
      is_header: true,
      lineage_keys: ["", ""],
      cell_kinds: ["stub", "stub"],
      divergence_flags: ["match", "match"],
      year_values: [null, null],
    },
    {
      row_id: "R1",
      row_index: 1,
      label: "Revenue",
      section_ref: "",
      unit: "$mm",
      base_case_value: 100,
      is_header: false,
      lineage_keys: ["a", "b"],
      cell_kinds: ["derived", "derived"],
      divergence_flags: ["match", "match"],
      year_values: [100, 110],
    },
    {
      row_id: "R2",
      row_index: 2,
      label: "FCF",
      section_ref: "",
      unit: "$mm",
      base_case_value: 10,
      is_header: false,
      lineage_keys: ["c", "d"],
      cell_kinds: ["derived", "derived"],
      divergence_flags: ["match", "match"],
      year_values: [10, 12],
    },
  ],
};

const active: ActiveCell = {
  rowId: "R1",
  rowIndex: 1,
  label: "Revenue",
  year: 2025,
  yearIndex: 0,
  lineageKey: "a",
  unit: "$mm",
  cellKind: "derived",
  displayValue: 100,
};

describe("grid navigation", () => {
  it("filters data rows", () => {
    expect(dataRows(payload)).toHaveLength(2);
  });

  it("resolves cellAt", () => {
    const cell = cellAt(payload, "R2", 2026);
    expect(cell?.displayValue).toBe(12);
    expect(cell?.lineageKey).toBe("d");
  });

  it("moves across years and rows", () => {
    expect(moveActiveCell(payload, active, "right")?.year).toBe(2026);
    expect(moveActiveCell(payload, active, "down")?.rowId).toBe("R2");
    expect(moveActiveCell(payload, active, "up")).toBeNull();
  });
});
