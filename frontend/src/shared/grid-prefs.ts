export type NumberDisplayFormat = "mm" | "billions" | "raw";
export type GridDensity = "comfortable" | "compact";

export type GridPrefs = {
  numberFormat: NumberDisplayFormat;
  density: GridDensity;
};

const STORAGE_KEY = "audit-grid-prefs";

const DEFAULT_PREFS: GridPrefs = {
  numberFormat: "mm",
  density: "compact",
};

export function loadGridPrefs(): GridPrefs {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { ...DEFAULT_PREFS };
    const parsed = JSON.parse(raw) as Partial<GridPrefs>;
    return {
      numberFormat:
        parsed.numberFormat === "billions" || parsed.numberFormat === "raw"
          ? parsed.numberFormat
          : "mm",
      density: parsed.density === "comfortable" ? "comfortable" : "compact",
    };
  } catch {
    return { ...DEFAULT_PREFS };
  }
}

export function saveGridPrefs(prefs: GridPrefs): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
}
