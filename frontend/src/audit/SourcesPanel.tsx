import type { LineageEntry } from "../shared/types";

type Props = {
  entry: LineageEntry | null;
};

export function SourcesPanel({ entry }: Props) {
  if (!entry?.sources) {
    return (
      <section className="sources-panel empty" aria-label="Sources panel">
        <p className="panel-hint">Select a cell to view sources.</p>
      </section>
    );
  }

  const { methodology, input_provenance, calibration_anchor } = entry.sources;

  return (
    <section className="sources-panel" aria-label="Sources panel">
      <p className="group-title">Sources for this cell</p>

      <div className="source-row">
        <span className="source-lbl">Methodology</span>
        Architecture &amp; Methodology spec <strong>{methodology.spec_section}</strong>
        {methodology.module && (
          <>
            {" "}
            · module <code>{methodology.module}</code>
          </>
        )}
      </div>

      {input_provenance && (
        <div className="source-row">
          <span className="source-lbl">Input provenance</span>
          {input_provenance.source} — {input_provenance.reference}
          {input_provenance.url && (
            <>
              {" "}
              ·{" "}
              <a href={`/${input_provenance.url}`} target="_blank" rel="noreferrer">
                DEV_LOG ↗
              </a>
            </>
          )}
        </div>
      )}

      {calibration_anchor && (
        <div className="source-row">
          <span className="source-lbl">Calibration anchor</span>
          2025 target {calibration_anchor.target.toLocaleString()} ±{" "}
          {(calibration_anchor.tolerance_pct * 100).toFixed(0)}% — {calibration_anchor.basis}
        </div>
      )}

      <div className="source-row">
        <span className="source-lbl">Principle / Rule</span>
        {methodology.principle}
        {methodology.rule !== methodology.principle && (
          <>
            {" "}
            · {methodology.rule}
          </>
        )}
      </div>
    </section>
  );
}
