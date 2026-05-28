export function formatMm(v: number | null | undefined): string {
  if (v == null || Number.isNaN(v)) return "—";
  const abs = Math.abs(v);
  if (abs >= 1000) return `$${(v / 1000).toFixed(1)}B`;
  return `$${v.toFixed(0)}M`;
}

export function formatCount(v: number | null | undefined): string {
  if (v == null || Number.isNaN(v)) return "—";
  return v.toLocaleString(undefined, { maximumFractionDigits: 0 });
}

export function formatPct(v: number | null | undefined): string {
  if (v == null || Number.isNaN(v)) return "—";
  const pct = Math.abs(v) <= 1 ? v * 100 : v;
  return `${pct.toFixed(1)}%`;
}

export function formatCellValue(v: number | null | undefined, unit: string): string {
  if (v == null || Number.isNaN(v)) return "";
  switch (unit) {
    case "pct":
    case "ratio":
      return formatPct(v);
    case "count":
      return formatCount(v);
    case "kg_to_leo":
      return formatCount(v);
    case "gbps":
      return formatCount(v);
    default:
      return formatMm(v).replace("$", "").replace("M", "").replace("B", "B");
  }
}

export function formatGridNumber(v: number | null | undefined, unit: string): string {
  if (v == null || Number.isNaN(v)) return "";
  if (unit === "pct" || unit === "ratio") {
    const pct = Math.abs(v) <= 1 ? v * 100 : v;
    return `${pct.toFixed(1)}%`;
  }
  if (unit === "count" || unit === "kg_to_leo" || unit === "gbps") {
    return v.toLocaleString(undefined, { maximumFractionDigits: 0 });
  }
  return v.toLocaleString(undefined, { maximumFractionDigits: 0 });
}
