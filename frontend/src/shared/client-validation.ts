import type { ClientInputSpec } from "./types";

/** Server override_warnings use canonical labels — map to client ids (F8). */
const CANONICAL_TO_ID: Record<string, string> = {
  "Mars carve-out % of prior-year Group FCF": "mars_pct",
  "Blended $/kg": "starship_dollars_per_kg_2030",
  "Credence on Model A (Pr(A))": "odc_prob_a",
  "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)":
    "wrights_law_learning_rate",
  "DTC ARPU ($/sub/mo, year-row)": "starlink_dtc_arpu_2030",
  "TAM inflation rate (annual)": "tam_inflation_rate",
};

/** MC P10/P90 envelopes for client-side caveat (FRONTEND_PRD §7.2, A6). */
const TYPICAL_ENVELOPE: Partial<Record<string, { p10: number; p90: number }>> = {
  mars_pct: { p10: 0.02, p90: 0.12 },
};

export function validateCustomValues(
  inputs: ClientInputSpec[],
  values: Record<string, number>,
): { errors: Record<string, string>; warnings: Record<string, string> } {
  const errors: Record<string, string> = {};
  const warnings: Record<string, string> = {};
  for (const inp of inputs) {
    const v = values[inp.id];
    if (v == null || Number.isNaN(v)) {
      errors[inp.id] = "Enter a value";
      continue;
    }
    if (v < inp.min || v > inp.max) {
      errors[inp.id] = `Must be between ${inp.min} and ${inp.max}`;
      continue;
    }
    const envelope = TYPICAL_ENVELOPE[inp.id];
    if (envelope && (v < envelope.p10 || v > envelope.p90)) {
      warnings[inp.id] =
        v > envelope.p90
          ? "Above typical range (above P90)"
          : "Below typical range (below P10)";
    }
  }
  return { errors, warnings };
}

export function warningsFromApi(
  apiWarnings: { label: string; message: string }[],
): Record<string, string> {
  const out: Record<string, string> = {};
  for (const w of apiWarnings) {
    const id = CANONICAL_TO_ID[w.label];
    if (id) {
      out[id] = w.message.includes("P90") || w.message.includes("P10")
        ? `Outside typical range (${w.message})`
        : w.message;
    }
  }
  return out;
}

export function defaultCustomValues(inputs: ClientInputSpec[]): Record<string, number> {
  const v: Record<string, number> = {};
  inputs.forEach((i) => {
    v[i.id] = i.default;
  });
  return v;
}
