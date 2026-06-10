import { describe, expect, it } from "vitest";
import { parseCellAddress, sheetSlugFromName } from "./cell-ref";

describe("parseCellAddress", () => {
  it("returns null for empty or dash addresses", () => {
    expect(parseCellAddress("")).toBeNull();
    expect(parseCellAddress("—")).toBeNull();
  });

  it("parses sheet-only references", () => {
    expect(parseCellAddress("Starlink")).toEqual({
      sheetName: "Starlink",
      rowId: "",
    });
  });

  it("parses sheet, row, and year", () => {
    expect(parseCellAddress("Starlink!R42:2030")).toEqual({
      sheetName: "Starlink",
      rowId: "R42",
      year: 2030,
    });
  });
});

describe("sheetSlugFromName", () => {
  it("maps known sheets and slugifies unknown", () => {
    expect(sheetSlugFromName("Group P&L")).toBe("group_pnl");
    expect(sheetSlugFromName("Custom Tab")).toBe("custom_tab");
  });
});
