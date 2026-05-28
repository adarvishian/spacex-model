import type { Scenario } from "../shared/types";

type Props = {
  scenarios: Scenario[];
  selected: string;
  onSelect: (name: string) => void;
  overrideLabel: string;
  overrideValue: string;
  onOverrideLabel: (v: string) => void;
  onOverrideValue: (v: string) => void;
  onRun: () => void;
  loading: boolean;
};

export function ScenarioSidebar({
  scenarios,
  selected,
  onSelect,
  overrideLabel,
  overrideValue,
  onOverrideLabel,
  onOverrideValue,
  onRun,
  loading,
}: Props) {
  return (
    <div className="scenario-sidebar">
      <h3>Scenario</h3>
      <select
        value={selected}
        onChange={(e) => onSelect(e.target.value)}
        aria-label="Scenario"
      >
        {scenarios.map((s) => (
          <option key={s.name} value={s.name}>
            {s.name.replace("_", " ")}
          </option>
        ))}
      </select>
      <h3>Override label</h3>
      <input
        value={overrideLabel}
        onChange={(e) => onOverrideLabel(e.target.value)}
        placeholder="Canonical label"
        aria-label="Override label"
      />
      <h3>Override value</h3>
      <input
        value={overrideValue}
        onChange={(e) => onOverrideValue(e.target.value)}
        placeholder="e.g. 0.05"
        aria-label="Override value"
      />
      <button type="button" className="run-btn" onClick={onRun} disabled={loading}>
        {loading ? "Running…" : "Re-run"}
      </button>
    </div>
  );
}
