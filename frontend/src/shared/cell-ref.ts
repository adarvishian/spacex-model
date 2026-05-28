/** Parse Excel-style cell references for cross-sheet navigation (FRONTEND_PRD §4.2). */

export type ParsedCellRef = {
  sheetName: string;
  rowId: string;
  year?: number;
};

export function parseCellAddress(address: string): ParsedCellRef | null {
  const trimmed = address.trim();
  if (!trimmed || trimmed === "—") return null;

  const bang = trimmed.indexOf("!");
  if (bang < 0) {
    return { sheetName: trimmed, rowId: "" };
  }

  const sheetName = trimmed.slice(0, bang).trim();
  let rest = trimmed.slice(bang + 1).trim();
  let year: number | undefined;

  const colon = rest.indexOf(":");
  if (colon >= 0) {
    const colPart = rest.slice(colon + 1).trim();
    rest = rest.slice(0, colon).trim();
    const y = parseInt(colPart, 10);
    if (!Number.isNaN(y) && y >= 2025 && y <= 2050) year = y;
  }

  const rowMatch = rest.match(/R\d+/i);
  const rowId = rowMatch ? rowMatch[0].toUpperCase() : rest;

  return { sheetName, rowId, year };
}

export function sheetSlugFromName(sheet?: string): string {
  if (!sheet) return "starlink";
  const map: Record<string, string> = {
    Assumptions: "assumptions",
    Allocator: "allocator",
    "Launch Capacity": "launch_capacity",
    "Customer Launch": "customer_launch",
    Starlink: "starlink",
    "Starlink Capacity": "starlink_capacity",
    ODC: "odc",
    "AI Stack": "ai_stack",
    "Lunar Mars": "lunar_mars",
    "Group P&L": "group_pnl",
    OpEx: "opex",
    CapEx: "capex",
    Valuation: "valuation",
    "Demand Curves": "demand_curves",
  };
  return map[sheet] ?? sheet.toLowerCase().replace(/&/g, "").replace(/\s+/g, "_").replace(/_+/g, "_");
}
