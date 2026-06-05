import type { NumberDisplayFormat } from "./grid-prefs";

/** Units the grid payload may supply — render exactly as given, never infer. */
export const GRID_UNITS = [
  "dollars_mm",
  "pct",
  "ratio",
  "count",
  "kg_to_leo",
  "gbps",
  "flag",
  "boolean",
] as const;

export type GridUnit = (typeof GRID_UNITS)[number];

/** Values above this displayed % are implausible for ratio/pct rows (e.g. $mm mis-tagged). */
const IMPLAUSIBLE_PCT_THRESHOLD = 150;

function localeNumber(v: number, maxFractionDigits = 0): string {
  return v.toLocaleString(undefined, { maximumFractionDigits: maxFractionDigits });
}

function isFlagUnit(unit: string): boolean {
  return unit === "flag" || unit === "boolean";
}

function formatFlag(v: number): string {
  if (v === 0) return "0";
  if (v === 1) return "1";
  return String(Math.round(v));
}

function pctDisplayValue(v: number): number {
  return Math.abs(v) <= 1 ? v * 100 : v;
}

function isImplausiblePct(v: number): boolean {
  const abs = Math.abs(v);
  const asPct = abs <= 1 ? abs * 100 : abs;
  return asPct > IMPLAUSIBLE_PCT_THRESHOLD;
}

function formatPctOrRatio(v: number): string {
  if (isImplausiblePct(v)) {
    return `${localeNumber(v)} ⚠`;
  }
  return `${pctDisplayValue(v).toFixed(1)}%`;
}

export function formatBillions(v: number | null | undefined): string {
  if (v == null || Number.isNaN(v)) return "—";
  return `$${v.toFixed(0)}B`;
}

export function formatMm(v: number | null | undefined): string {
  if (v == null || Number.isNaN(v)) return "—";
  const abs = Math.abs(v);
  if (abs >= 1000) return `$${(v / 1000).toFixed(1)}B`;
  return `$${v.toFixed(0)}M`;
}

export function formatCount(v: number | null | undefined): string {
  if (v == null || Number.isNaN(v)) return "—";
  return localeNumber(v);
}

export function formatPct(v: number | null | undefined): string {
  if (v == null || Number.isNaN(v)) return "—";
  return formatPctOrRatio(v);
}

export function formatCellValue(v: number | null | undefined, unit: string): string {
  if (v == null || Number.isNaN(v)) return "";
  if (isFlagUnit(unit)) return formatFlag(v);
  switch (unit) {
    case "pct":
    case "ratio":
      return formatPctOrRatio(v);
    case "count":
    case "kg_to_leo":
    case "gbps":
      return localeNumber(v);
    default:
      return formatMm(v).replace("$", "").replace("M", "").replace("B", "B");
  }
}

function formatDollarsMm(
  v: number,
  displayFormat: NumberDisplayFormat = "mm",
): string {
  switch (displayFormat) {
    case "billions": {
      const abs = Math.abs(v);
      if (abs >= 1000) return `$${(v / 1000).toFixed(1)}B`;
      if (abs >= 1) return `$${v.toFixed(0)}M`;
      return `$${v.toFixed(2)}M`;
    }
    case "raw":
      return localeNumber(v);
    default:
      return localeNumber(v);
  }
}

export function formatGridNumber(
  v: number | null | undefined,
  unit: string,
  displayFormat: NumberDisplayFormat = "mm",
): string {
  if (v == null || Number.isNaN(v)) return "";
  if (isFlagUnit(unit)) return formatFlag(v);
  if (unit === "pct" || unit === "ratio") return formatPctOrRatio(v);
  if (unit === "count" || unit === "kg_to_leo" || unit === "gbps") {
    return localeNumber(v);
  }
  if (unit === "dollars_mm") return formatDollarsMm(v, displayFormat);
  return localeNumber(v);
}

/** Unit suffix for derivation panel display (never infer unit from value). */
export function formatUnitLabel(unit: string): string {
  if (unit === "dollars_mm") return "$mm";
  return unit;
}

/** Formatted grid value with unit suffix for derivation header (F6). */
export function formatValueWithUnit(v: number | null | undefined, unit: string): string {
  if (v == null || Number.isNaN(v)) return "—";
  const num = formatGridNumber(v, unit);
  if (!num) return "—";
  if (unit === "dollars_mm") return `${num} $mm`;
  return num;
}

export function isStubLineage(
  entry: { cell_kind?: string },
  cellKind?: string,
): boolean {
  return entry.cell_kind === "stub" || cellKind === "stub";
}
