import { Scenario } from "../api";

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

const COMMON_OVERRIDES = [
  "TAM inflation rate (annual)",
  "Mars carve-out % of prior-year Group FCF",
  "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)",
];

export function ScenarioPicker({
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
    <div className="panel">
      <h2>Scenario</h2>
      <div className="scenario-list">
        {scenarios.map((s) => (
          <button
            key={s.name}
            type="button"
            className={`scenario-btn ${selected === s.name ? "active" : ""}`}
            onClick={() => onSelect(s.name)}
          >
            {s.name.replace(/_/g, " ")}
            <small>{s.description || "No description"}</small>
          </button>
        ))}
      </div>

      <h2 style={{ marginTop: "1.25rem" }}>Override</h2>
      <select
        value={overrideLabel}
        onChange={(e) => onOverrideLabel(e.target.value)}
        style={{
          width: "100%",
          padding: "0.45rem",
          borderRadius: 6,
          border: "1px solid var(--border)",
          background: "var(--bg)",
          color: "var(--text)",
        }}
      >
        {COMMON_OVERRIDES.map((l) => (
          <option key={l} value={l}>
            {l}
          </option>
        ))}
      </select>
      <div className="override-row">
        <input
          type="number"
          step="any"
          placeholder="Leave empty for scenario default"
          value={overrideValue}
          onChange={(e) => onOverrideValue(e.target.value)}
        />
      </div>

      <button type="button" className="primary-btn" onClick={onRun} disabled={loading}>
        {loading ? "Running…" : "Run scenario"}
      </button>
    </div>
  );
}
