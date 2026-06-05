import type { ActiveCell, LineageEntry } from "../shared/types";
import {
  formatGridNumber,
  formatUnitLabel,
  formatValueWithUnit,
  isStubLineage,
} from "../shared/format";

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

function stubSpecRef(entry: LineageEntry): string {
  return (
    entry.stub_spec_section ??
    entry.section_ref ??
    entry.architecture_ref ??
    "architecture spec"
  );
}

export function DerivationPanel({ entry, activeCell, expanded = false }: Props) {
  if (!entry || !activeCell) {
    return null;
  }

  const pill = statusPill(entry);
  const addr = entry.cell_address;
  const addressStr = addr
    ? `${addr.sheet}!${addr.row} · column ${addr.year ?? activeCell.year}`
    : `${activeCell.label} · ${activeCell.year}`;

  const unit = entry.unit ?? activeCell.unit;
  const unitLabel = formatUnitLabel(unit);
  const isStub = isStubLineage(entry, activeCell.cellKind);
  const displayedValue = formatValueWithUnit(activeCell.displayValue, unit);
  const tracedValue =
    entry.computed_value != null ? formatValueWithUnit(entry.computed_value, unit) : null;
  const hasResolvedInputs = (entry.resolved_inputs ?? []).length > 0;

  return (
    <section
      className={`derivation-panel ${isStub ? "stub" : "derived"} ${expanded ? "expanded" : ""}`}
      aria-label="Derivation panel"
      tabIndex={0}
      data-testid="derivation-panel"
    >
      <div className="derivation-addr">
        <p className="derivation-label" title={activeCell.label}>
          {activeCell.label}
        </p>
        <code>{addressStr}</code>
        <span className="addr-meta">
          type:{" "}
          <strong className={isStub ? "cell-kind-stub" : "cell-kind-derived"}>
            {entry.cell_kind ?? activeCell.cellKind} (year-row)
          </strong>
        </span>
        <span className="addr-meta">
          unit: <strong>{unitLabel}</strong>
        </span>
        <span className="addr-spacer" />
        <span className={pill.className}>{pill.text}</span>
      </div>

      <div className="derivation-value-row" data-testid="derivation-displayed-value">
        <span className="panel-title">Displayed value (grid)</span>
        <span className="derivation-displayed-value">{displayedValue}</span>
        {!isStub && tracedValue && tracedValue !== displayedValue && (
          <span className="derivation-traced-note muted">
            Traced value differs: {tracedValue}
          </span>
        )}
      </div>

      <div className="derivation-columns">
        <div>
          <p className="panel-title">Formula</p>
          <div className="formula-box" data-testid="derivation-formula">
            {entry.formula_expression ?? entry.display_name}
          </div>

          {isStub ? (
            <>
              <p className="panel-title">Computed (traced)</p>
              <div className="stub-state" data-testid="derivation-stub-state">
                <p>
                  <strong>Planned</strong> — {stubSpecRef(entry)}
                </p>
              </div>
            </>
          ) : (
            <>
              <p className="panel-title">Computed (traced)</p>
              <div className="formula-box computed traced" data-testid="derivation-computed">
                = {formatGridNumber(entry.computed_value ?? null, unit)}
                {unit === "dollars_mm" ? " $mm" : ""}
              </div>
            </>
          )}
        </div>

        <div>
          <p className="panel-title">Resolved inputs (depth 1)</p>
          <table className="inputs-table" data-testid="derivation-inputs">
            <thead>
              <tr>
                <th>Input</th>
                <th>Source cell</th>
                <th>Value</th>
              </tr>
            </thead>
            <tbody>
              {!hasResolvedInputs && (
                <tr>
                  <td colSpan={3} className="muted">
                    {isStub
                      ? "No resolved inputs — stub cell has no traced upstream."
                      : "No resolved inputs for this cell."}
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
