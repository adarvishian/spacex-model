import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { EvDistributionChart } from "../client/EvDistributionChart";
import { FcfFanChart } from "../client/FcfFanChart";
import { fetchHealth, fetchMcJob, submitMc } from "../api";
import {
  canHydrateMcFromArtifact,
  loadBaseCaseMcArtifact,
} from "../shared/base-case-mc-artifact";
import { formatBillions, formatGridNumber } from "../shared/format";
import type { McOutputKind } from "../shared/mc-headline";
import { TornadoChart } from "../shared/TornadoChart";
import type { McAggregationPayload, McJobResult, McMetricSummary, TornadoBar } from "../shared/types";

const AUDIT_DEFAULT_TRIALS = 5000;
const SERVERLESS_MAX_TRIALS = 200;

type McSource = "precache" | "live";

type Props = {
  outputKind: McOutputKind;
  label: string;
  year: number;
  scenario: string;
  overrides: Record<string, number>;
};

function aggregationFromJob(result: McJobResult): McAggregationPayload {
  const agg = result.aggregation;
  return {
    ...agg,
    n_trials: result.n_trials ?? agg.n_trials,
    n_converged: result.n_converged ?? agg.n_converged,
    base_seed: result.base_seed ?? agg.base_seed,
    convergence_status: result.convergence_status ?? agg.convergence_status,
  };
}

function cvarReadout(cvar: number, p50: number): string {
  if (!Number.isFinite(cvar) || !Number.isFinite(p50)) return "";
  const gap = p50 - cvar;
  if (gap <= 0) return "Tail risk is limited relative to the median outcome.";
  return `In the worst 5% of trials, Group EV averages ${formatBillions(cvar)} — about ${formatBillions(gap)} below the median.`;
}

function PercentileTable({ metrics }: { metrics: McMetricSummary }) {
  const rows: Array<{ label: string; value: number }> = [
    { label: "P5", value: metrics.p5 },
    { label: "P10", value: metrics.p10 },
    { label: "P25", value: metrics.p25 },
    { label: "P50", value: metrics.p50 },
    { label: "P75", value: metrics.p75 },
    { label: "P90", value: metrics.p90 },
    { label: "P95", value: metrics.p95 },
    { label: "Mean", value: metrics.mean },
    { label: "CVaR (5%)", value: metrics.cvar_5 },
  ];

  return (
    <table className="mc-percentile-table" data-testid="mc-percentile-table">
      <thead>
        <tr>
          <th>Percentile</th>
          <th>Group EV ($B)</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.label}>
            <td>{row.label}</td>
            <td className="num">{formatBillions(row.value)}</td>
          </tr>
        ))}
        {metrics.base_case != null && (
          <tr className="base-case-row">
            <td>Base case</td>
            <td className="num">{formatBillions(metrics.base_case)}</td>
          </tr>
        )}
      </tbody>
    </table>
  );
}

export function McAuditPanel({ outputKind, label, year, scenario, overrides }: Props) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [aggregation, setAggregation] = useState<McAggregationPayload | null>(null);
  const [tornado, setTornado] = useState<TornadoBar[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [source, setSource] = useState<McSource | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [progress, setProgress] = useState<{ done: number; total: number } | null>(null);
  const [etaSec, setEtaSec] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [trials, setTrials] = useState(AUDIT_DEFAULT_TRIALS);
  const [serverless, setServerless] = useState(false);
  const [gitSha, setGitSha] = useState<string | null>(null);
  const [artifactReady, setArtifactReady] = useState(false);
  const pollStart = useRef<number | null>(null);

  const isInstantBase =
    scenario === "base_case" && Object.keys(overrides).length === 0;

  const maxTrials = serverless ? SERVERLESS_MAX_TRIALS : AUDIT_DEFAULT_TRIALS;

  useEffect(() => {
    fetchHealth()
      .then((h) => {
        setGitSha(h.git_sha);
        setServerless(Boolean(h.serverless));
        if (h.serverless) setTrials(Math.min(AUDIT_DEFAULT_TRIALS, SERVERLESS_MAX_TRIALS));
      })
      .catch(() => undefined);
  }, []);

  useEffect(() => {
    let cancelled = false;
    loadBaseCaseMcArtifact()
      .then(() => {
        if (!cancelled) setArtifactReady(true);
      })
      .catch(() => {
        if (!cancelled) setArtifactReady(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const applyAggregation = useCallback(
    (agg: McAggregationPayload, src: McSource, id: string | null, bars: TornadoBar[] = []) => {
      setAggregation(agg);
      setSource(src);
      setJobId(id);
      setTornado(bars);
      setStatus("completed");
      setProgress(null);
      setEtaSec(null);
    },
    [],
  );

  useEffect(() => {
    if (!artifactReady || !isInstantBase) return;
    if (!canHydrateMcFromArtifact(scenario, overrides, gitSha)) return;
    void (async () => {
      const artifact = await loadBaseCaseMcArtifact();
      try {
        const job = await fetchMcJob(artifact.job_id);
        if (job.status === "completed" && job.result) {
          applyAggregation(
            aggregationFromJob(job.result),
            "precache",
            artifact.job_id,
            job.result.tornado ?? artifact.tornado ?? [],
          );
          return;
        }
      } catch {
        /* fall back to static artifact */
      }
      applyAggregation(
        artifact.aggregation,
        "precache",
        artifact.job_id,
        artifact.tornado ?? [],
      );
    })();
  }, [artifactReady, isInstantBase, scenario, overrides, gitSha, applyAggregation]);

  useEffect(() => {
    if (isInstantBase) return;
    setAggregation(null);
    setTornado([]);
    setSource(null);
    setJobId(null);
    setStatus(null);
    setProgress(null);
  }, [scenario, overrides, isInstantBase]);

  const pollJob = useCallback(
    async (id: string) => {
      const job = await fetchMcJob(id);
      setStatus(job.status);
      if (job.progress) {
        setProgress({ done: job.progress.trials_done, total: job.progress.trials });
        if (pollStart.current && job.progress.trials_done > 0) {
          const elapsed = (Date.now() - pollStart.current) / 1000;
          const rate = job.progress.trials_done / elapsed;
          const remaining = job.progress.trials - job.progress.trials_done;
          setEtaSec(rate > 0 ? Math.ceil(remaining / rate) : null);
        }
      }
      if (job.status === "completed" && job.result) {
        applyAggregation(
          aggregationFromJob(job.result),
          "live",
          id,
          job.result.tornado ?? [],
        );
        return;
      }
      if (job.status === "failed") {
        setError(job.error ?? "Monte Carlo run failed");
        setProgress(null);
        return;
      }
      if (job.status === "queued" || job.status === "running") {
        setTimeout(() => void pollJob(id), serverless ? 800 : 1500);
      }
    },
    [applyAggregation, serverless],
  );

  const runMc = useCallback(async () => {
    setError(null);
    setStatus("submitting");
    setProgress(null);
    setEtaSec(null);
    pollStart.current = Date.now();
    try {
      const { job_id } = await submitMc({
        trials: Math.min(trials, maxTrials),
        scenario,
        base_seed: 42,
        include_tornado: true,
        tornado_top: 10,
      });
      setJobId(job_id);
      const params = new URLSearchParams(searchParams);
      params.set("mc", job_id);
      setSearchParams(params, { replace: true });
      setStatus("queued");
      await pollJob(job_id);
    } catch (e) {
      setError(String(e));
      setStatus(null);
    }
  }, [trials, maxTrials, scenario, pollJob, searchParams, setSearchParams]);

  useEffect(() => {
    const mcParam = searchParams.get("mc");
    if (!mcParam || aggregation) return;
    setJobId(mcParam);
    setStatus("loading");
    void fetchMcJob(mcParam)
      .then((job) => {
        if (job.status === "completed" && job.result) {
          applyAggregation(
            aggregationFromJob(job.result),
            "live",
            mcParam,
            job.result.tornado ?? [],
          );
        } else if (job.status === "queued" || job.status === "running") {
          pollStart.current = Date.now();
          void pollJob(mcParam);
        }
      })
      .catch((e) => setError(String(e)));
  }, [searchParams.get("mc")]);

  const visibleAggregation = useMemo(() => {
    if (!aggregation) return null;
    if (source === "precache" && !isInstantBase) return null;
    return aggregation;
  }, [aggregation, source, isInstantBase]);

  const evMetrics = visibleAggregation?.metrics?.group_ev_2025_b;
  const histogram = visibleAggregation?.group_ev_histogram;
  const fan = visibleAggregation?.group_fcf_fan;

  const yearFanIndex = fan?.years.indexOf(year) ?? -1;
  const yearFanSlice =
    yearFanIndex >= 0 && fan
      ? {
          p5: fan.p5[yearFanIndex],
          p25: fan.p25[yearFanIndex],
          p50: fan.p50[yearFanIndex],
          p75: fan.p75[yearFanIndex],
          p95: fan.p95[yearFanIndex],
          base: fan.base_case[yearFanIndex],
        }
      : null;

  const showProgress =
    status === "submitting" ||
    status === "queued" ||
    status === "running" ||
    status === "loading";

  const outputCaption =
    outputKind === "group_ev"
      ? "Stochastic distribution of Group EV (2025)"
      : outputKind === "group_fcf"
        ? `Stochastic distribution of Group FCF — ${year}`
        : `Sensitivity context for ${label} — trial drivers affect Group EV`;

  return (
    <section
      className="audit-mc panel"
      aria-label="Monte Carlo distribution"
      data-testid="audit-mc-panel"
    >
      <div className="audit-mc-header">
        <h2>Monte Carlo</h2>
        {source === "precache" && (
          <span className="audit-badge mc-badge-precache" data-testid="audit-mc-provenance">
            precomputed
          </span>
        )}
        {source === "live" && jobId && (
          <span className="audit-badge" data-testid="audit-mc-provenance">
            run {jobId.slice(0, 8)}
          </span>
        )}
      </div>

      <p className="muted audit-mc-intro">{outputCaption}</p>

      <div className="audit-mc-controls">
        <label className="audit-mc-trials">
          Trials
          <input
            type="number"
            min={50}
            max={maxTrials}
            step={50}
            value={Math.min(trials, maxTrials)}
            onChange={(e) => setTrials(Number(e.target.value) || AUDIT_DEFAULT_TRIALS)}
            data-testid="audit-mc-trials-input"
          />
        </label>
        <button
          type="button"
          className="secondary-btn"
          onClick={() => void runMc()}
          disabled={showProgress}
          data-testid="audit-mc-run-btn"
        >
          Run Monte Carlo
        </button>
      </div>

      {showProgress && (
        <div className="mc-progress" data-testid="audit-mc-progress" role="status">
          <p>
            Running {scenario} Monte Carlo
            {progress
              ? ` — ${progress.done.toLocaleString()} / ${progress.total.toLocaleString()} trials`
              : " — starting…"}
            {etaSec != null && etaSec > 0 ? ` · ~${etaSec}s remaining` : ""}
          </p>
          {progress && (
            <div className="mc-progress-bar" aria-hidden>
              <div
                className="mc-progress-fill"
                style={{ width: `${(progress.done / progress.total) * 100}%` }}
              />
            </div>
          )}
        </div>
      )}

      {error && <p className="audit-alert error">{error}</p>}

      {visibleAggregation && evMetrics && (
        <>
          {(outputKind === "group_ev" || outputKind === "module_fcf") && histogram && (
            <>
              <h3>Group EV distribution</h3>
              <EvDistributionChart histogram={histogram} metrics={evMetrics} />
              <p className="mc-cvar-readout" data-testid="audit-mc-cvar-readout">
                {cvarReadout(evMetrics.cvar_5, evMetrics.p50)}
              </p>
            </>
          )}

          <h3>Percentile table</h3>
          <PercentileTable metrics={evMetrics} />

          {outputKind === "group_fcf" && yearFanSlice && (
            <div className="audit-mc-year-band" data-testid="audit-mc-year-band">
              <h3>Group FCF band — {year}</h3>
              <dl className="audit-mc-year-stats">
                <div>
                  <dt>P5</dt>
                  <dd>{formatGridNumber(yearFanSlice.p5, "dollars_mm")} $mm</dd>
                </div>
                <div>
                  <dt>P50</dt>
                  <dd>{formatGridNumber(yearFanSlice.p50, "dollars_mm")} $mm</dd>
                </div>
                <div>
                  <dt>P95</dt>
                  <dd>{formatGridNumber(yearFanSlice.p95, "dollars_mm")} $mm</dd>
                </div>
                {yearFanSlice.base != null && (
                  <div>
                    <dt>Base case</dt>
                    <dd>{formatGridNumber(yearFanSlice.base, "dollars_mm")} $mm</dd>
                  </div>
                )}
              </dl>
            </div>
          )}

          {fan && (outputKind === "group_fcf" || outputKind === "group_ev") && (
            <>
              <h3>Group FCF uncertainty</h3>
              <FcfFanChart fan={fan} />
            </>
          )}

          {tornado.length > 0 && (
            <>
              <h3>Sensitivity</h3>
              <TornadoChart bars={tornado} />
            </>
          )}

          <div className="audit-mc-provenance" data-testid="audit-mc-provenance-detail">
            <p>
              <strong>Trials:</strong> {visibleAggregation.n_converged.toLocaleString()} converged
              of {visibleAggregation.n_trials.toLocaleString()}
            </p>
            <p>
              <strong>Seed:</strong> {visibleAggregation.base_seed}
            </p>
            <p>
              <strong>Convergence:</strong> {visibleAggregation.convergence_status}
            </p>
          </div>
        </>
      )}

      {!visibleAggregation && !showProgress && !error && !isInstantBase && (
        <p className="muted">Click Run Monte Carlo to generate a distribution for this scenario.</p>
      )}
    </section>
  );
}
