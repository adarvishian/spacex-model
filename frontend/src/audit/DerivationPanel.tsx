import type { ActiveCell, LineageEntry } from "../shared/types";
import { formatGridNumber } from "../shared/format";

type Props = {
  entry: LineageEntry | null;
  activeCell: ActiveCell | null;
  expanded?: boolean;
};

function statusPill(entry: LineageEntry): { className: string; text: string } {
  const code = entry.computed_value;
  const xlsx = entry.xlsx_cached_value;
  const status = entry.divergence_status ?? "n_a";

  if (status === "match" && code != null && xlsx != null) {
    return {
      className: "pill match",
      text: `code ${formatGridNumber(code, entry.unit ?? "")} = xlsx ${formatGridNumber(xlsx, entry.unit ?? "")} · match`,
    };
  }
  if (status === "intentional" && entry.divergence_delta_mm != null) {
    return {
      className: "pill intentional",
      text: `intentional divergence Δ ${formatGridNumber(entry.divergence_delta_mm, "dollars_mm")} mm · §11.6`,
    };
  }
  if (status === "drift" && entry.divergence_delta_mm != null) {
    return {
      className: "pill intentional",
      text: `drift Δ ${formatGridNumber(entry.divergence_delta_mm, "dollars_mm")} mm`,
    };
  }
  return { className: "pill match", text: "—" };
}

export function DerivationPanel({ entry, activeCell, expanded = false }: Props) {
  if (!entry || !activeCell) {
    return (
      <section
        className="derivation-panel empty"
        aria-label="Derivation panel"
        tabIndex={0}
        data-testid="derivation-panel"
      >
        <p className="panel-hint">Click a grid cell to inspect its derivation.</p>
      </section>
    );
  }

  const pill = statusPill(entry);
  const addr = entry.cell_address;
  const addressStr = addr
    ? `${addr.sheet}!${addr.row} · column ${addr.year ?? activeCell.year}`
    : `${activeCell.label} · ${activeCell.year}`;

  return (
    <section
      className={`derivation-panel ${expanded ? "expanded" : ""}`}
      aria-label="Derivation panel"
      tabIndex={0}
      data-testid="derivation-panel"
    >
      <div className="derivation-addr">
        <code>{addressStr}</code>
        <span className="addr-meta">
          type: <strong>{entry.cell_kind ?? activeCell.cellKind} (year-row)</strong>
        </span>
        <span className="addr-meta">
          unit: <strong>{entry.unit === "dollars_mm" ? "$mm" : entry.unit ?? activeCell.unit}</strong>
        </span>
        <span className="addr-spacer" />
        <span className={pill.className}>{pill.text}</span>
      </div>

      <div className="derivation-columns">
        <div>
          <p className="panel-title">Formula</p>
          <div className="formula-box">{entry.formula_expression ?? entry.display_name}</div>
          <p className="panel-title">Computed</p>
          <div className="formula-box computed">
            = {formatGridNumber(entry.computed_value ?? null, entry.unit ?? "dollars_mm")}
            {entry.unit === "dollars_mm" ? " $mm" : ""}
          </div>
        </div>

        <div>
          <p className="panel-title">Resolved inputs (depth 1)</p>
          <table className="inputs-table">
            <thead>
              <tr>
                <th>Input</th>
                <th>Source cell</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {(entry.resolved_inputs ?? []).length === 0 && (
                <tr>
                  <td colSpan={3} className="muted">
                    No resolved inputs for this cell.
                  </td>
                </tr>
              )}
              {(entry.resolved_inputs ?? []).map((inp) => (
                <tr key={inp.lineage_key + inp.label}>
                  <td>{inp.label}</td>
                  <td>
                    <code>{inp.cell_address}</code>
                  </td>
                  <td className="num">{formatGridNumber(inp.value, inp.unit)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
