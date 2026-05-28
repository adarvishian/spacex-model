import { useMemo } from "react";
import type { ClientInputSpec } from "../shared/types";

export type CustomValues = Record<string, number>;

type Props = {
  inputs: ClientInputSpec[];
  values: CustomValues;
  onChange: (id: string, value: number) => void;
  fieldErrors: Record<string, string>;
  fieldWarnings: Record<string, string>;
  onRun: () => void;
  onReset: () => void;
  running: boolean;
  visible: boolean;
};

export function CustomBuilder({
  inputs,
  values,
  onChange,
  fieldErrors,
  fieldWarnings,
  onRun,
  onReset,
  running,
  visible,
}: Props) {
  const defaults = useMemo(() => {
    const d: CustomValues = {};
    inputs.forEach((i) => {
      d[i.id] = i.default;
    });
    return d;
  }, [inputs]);

  if (!visible) return null;

  return (
    <section className="client-custom panel" aria-label="Custom scenario builder">
      <h2>Custom scenario</h2>
      <div className="client-custom-grid">
        {inputs.map((inp) => (
          <label key={inp.id} className="client-custom-field">
            <span>{inp.plain_label}</span>
            <input
              type="number"
              step="any"
              min={inp.min}
              max={inp.max}
              value={values[inp.id] ?? defaults[inp.id]}
              onChange={(e) => onChange(inp.id, parseFloat(e.target.value))}
              aria-invalid={Boolean(fieldErrors[inp.id])}
            />
            {fieldErrors[inp.id] && (
              <span className="client-field-error" role="alert">
                {fieldErrors[inp.id]}
              </span>
            )}
            {fieldWarnings[inp.id] && !fieldErrors[inp.id] && (
              <span className="client-field-warn">{fieldWarnings[inp.id]}</span>
            )}
          </label>
        ))}
      </div>
      <div className="client-custom-actions">
        <button type="button" className="run-btn" onClick={onRun} disabled={running}>
          {running ? "Running…" : "Run scenario"}
        </button>
        <button type="button" className="btn-secondary" onClick={onReset} disabled={running}>
          Reset
        </button>
      </div>
    </section>
  );
}
