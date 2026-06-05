import { useQuery } from "@tanstack/react-query";
import { fetchRunAuditDashboard } from "../api";
import { formatGridNumber } from "../shared/format";
import type { RunAuditPayload } from "../shared/types";

type Props = {
  runId: string | null;
  scenario?: string;
  auditPayload?: RunAuditPayload | null;
  loading?: boolean;
  onNavigateDivergence?: (opts: {
    sheetSlug: string;
    rowId: string;
    year: number;
  }) => void;
};

function formatDeltaPct(delta: number | null, target: number): string {
  if (delta == null || target === 0) return "—";
  const pct = (Math.abs(delta) / Math.abs(target)) * 100;
  return `${pct.toFixed(1)}%`;
}

function CalibrationVerdict({ withinTolerance }: { withinTolerance: boolean }) {
  return (
    <span
      className={withinTolerance ? "conserv-ok" : "conserv-fail"}
      aria-label={withinTolerance ? "Pass" : "Fail"}
    >
      {withinTolerance ? "✓ PASS" : "✗ FAIL"}
    </span>
  );
}

function RunAuditSkeleton() {
  return (
    <div className="run-audit-tab run-audit-skeleton" data-testid="run-audit-skeleton">
      <div className="audit-run-status">
        <span className="skeleton-pulse" aria-hidden="true" />
        Loading run audit — solver may still be running (~40 s on first run)
      </div>
      <div className="skeleton-block" />
      <div className="skeleton-block" />
      <div className="skeleton-block" />
    </div>
  );
}

export function RunAuditTab({
  runId,
  scenario,
  auditPayload,
  loading = false,
  onNavigateDivergence,
}: Props) {
  const needsFetch = Boolean(runId) && auditPayload == null;
  const auditQ = useQuery({
    queryKey: ["run-audit", runId, scenario],
    queryFn: () => fetchRunAuditDashboard(runId!, scenario),
    enabled: needsFetch,
  });

  if (!runId && !auditPayload) {
    return (
      <div className="run-audit-tab">
        <p className="muted">Run a scenario to view audit results.</p>
      </div>
    );
  }

  if (loading && !auditPayload) {
    return <RunAuditSkeleton />;
  }

  if (needsFetch && auditQ.isLoading) {
    return <RunAuditSkeleton />;
  }

  const data = auditPayload ?? auditQ.data;
  if (!data) {
    return (
      <div className="run-audit-tab">
        <p className="audit-alert error">Failed to load audit dashboard.</p>
      </div>
    );
  }

  const failYears = data.conservation.r108_by_year.filter((r) => !r.ok);

  return (
    <div className="run-audit-tab" tabIndex={0} aria-label="Run audit dashboard">
      <div className="run-audit-section">
        <h3>Solver convergence</h3>
        <div className="run-audit-metrics">
          <span>
            Iterations: <strong>{data.solver.iterations}</strong>
          </span>
          <span className={data.solver.converged ? "conserv-ok" : "conserv-fail"}>
            {data.solver.converged ? "Converged" : "Did not converge"}
          </span>
          <span>
            Max residual: <strong>{data.solver.max_residual.toExponential(2)}</strong>
          </span>
        </div>
      </div>

      <div className="run-audit-section">
        <h3>
          Conservation R99–R108{" "}
          <span className={data.conservation.all_ok ? "pill match" : "pill intentional"}>
            {data.conservation.all_ok ? "ALL OK" : `${failYears.length} FAIL year${failYears.length === 1 ? "" : "s"}`}
          </span>
        </h3>
        <div className="conservation-grid">
          {data.conservation.r108_by_year.map((row) => (
            <span
              key={row.year}
              className={`conservation-year ${row.ok ? "ok" : "fail"}`}
              title={`Max residual ${row.max_residual_mm.toFixed(2)} mm`}
            >
              {row.year}
            </span>
          ))}
        </div>
      </div>

      <div className="run-audit-section">
        <h3>2025 calibration anchors</h3>
        <table className="run-audit-table">
          <thead>
            <tr>
              <th>Anchor</th>
              <th>Target</th>
              <th>Actual</th>
              <th>Δ</th>
              <th>Δ% vs tol</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.calibration_anchors.map((a) => (
              <tr key={a.name}>
                <td>{a.name}</td>
                <td className="num">{a.target.toLocaleString()}</td>
                <td className="num">
                  {a.actual != null ? a.actual.toLocaleString(undefined, { maximumFractionDigits: 1 }) : "—"}
                </td>
                <td className="num">
                  {a.delta != null ? a.delta.toLocaleString(undefined, { maximumFractionDigits: 1 }) : "—"}
                </td>
                <td className="num" title={`Tolerance ±${(a.tolerance_pct * 100).toFixed(0)}%`}>
                  {formatDeltaPct(a.delta, a.target)}
                </td>
                <td>
                  <CalibrationVerdict withinTolerance={a.within_tolerance} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="run-audit-section">
        <h3>
          Divergence triage (top {data.divergences.length}){" "}
          <span className="muted">
            {data.divergence_summary.diverging_count} diverging /{" "}
            {data.divergence_summary.total_compared} compared
          </span>
        </h3>
        <table className="run-audit-table divergence-table">
          <thead>
            <tr>
              <th>Cell</th>
              <th>Year</th>
              <th>xlsx</th>
              <th>code</th>
              <th>Δ</th>
              <th>Triage</th>
            </tr>
          </thead>
          <tbody>
            {data.divergences.map((d, i) => (
              <tr
                key={`${d.sheet}-${d.row_id}-${d.year}-${i}`}
                className="divergence-row-clickable"
                onClick={() =>
                  onNavigateDivergence?.({
                    sheetSlug: d.sheet_slug,
                    rowId: d.row_id,
                    year: d.year,
                  })
                }
              >
                <td>
                  {d.sheet}!{d.row_id} · {d.label.slice(0, 40)}
                </td>
                <td>{d.year}</td>
                <td className="num">{formatGridNumber(d.xlsx_value, "dollars_mm")}</td>
                <td className="num">{formatGridNumber(d.code_value, "dollars_mm")}</td>
                <td className="num">{formatGridNumber(d.delta, "dollars_mm")}</td>
                <td title={d.triage_note}>{d.triage}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
