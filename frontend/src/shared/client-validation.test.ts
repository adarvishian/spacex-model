import { describe, expect, it } from "vitest";
import {
  defaultCustomValues,
  validateCustomValues,
  warningsFromApi,
} from "./client-validation";
import type { ClientInputSpec } from "./types";

const inputs: ClientInputSpec[] = [
  { id: "mars_pct", plain_label: "Mars %", min: 0, max: 0.2, default: 0.05 },
  { id: "tam_inflation_rate", plain_label: "TAM inflation", min: 0, max: 0.1, default: 0.025 },
];

describe("validateCustomValues", () => {
  it("flags out-of-range and missing values", () => {
    const result = validateCustomValues(inputs, { mars_pct: 0.5 });
    expect(result.errors.mars_pct).toContain("between");
  });

  it("warns when outside MC envelope", () => {
    const result = validateCustomValues(inputs, { mars_pct: 0.15, tam_inflation_rate: 0.025 });
    expect(result.warnings.mars_pct).toContain("P90");
  });
});

describe("warningsFromApi", () => {
  it("maps canonical labels to client ids", () => {
    const out = warningsFromApi([
      { label: "Mars carve-out % of prior-year Group FCF", message: "above P90" },
    ]);
    expect(out.mars_pct).toContain("P90");
  });
});

describe("defaultCustomValues", () => {
  it("seeds defaults from input specs", () => {
    expect(defaultCustomValues(inputs)).toEqual({
      mars_pct: 0.05,
      tam_inflation_rate: 0.025,
    });
  });
});
