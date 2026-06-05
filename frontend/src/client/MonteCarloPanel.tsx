import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { fetchHealth, fetchMcJob, submitMc } from "../api";
import {
  canHydrateMcFromArtifact,
  loadBaseCaseMcArtifact,
} from "../shared/base-case-mc-artifact";
import { formatBillions } from "../shared/format";
import { TornadoChart } from "../shared/TornadoChart";
import type { McAggregationPayload, McJobResult, TornadoBar } from "../shared/types";
import { EvDistributionChart } from "./EvDistributionChart";
import { FcfFanChart } from "./FcfFanChart";

const DEFAULT_TRIALS = 2000;
const SERVERLESS_MAX_TRIALS = 200;

type McSource = "precache" | "live";

type Props = {
  scenario: string;
  overrides: Record<string, number>;
};

function cvarReadout(cvar: number, p50: number): string {
  if (!Number.isFinite(cvar) || !Number.isFinite(p50)) return "";
  const gap = p50 - cvar;
  if (gap <= 0) return "Tail risk is limited relative to the median outcome.";
  return `In the worst 5% of trials, Group EV averages ${formatBillions(cvar)} — about ${formatBillions(gap)} below the median.`;
}

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

export function MonteCarloPanel({ scenario, overrides }: Props) {
  const [searchParams, setSearchParams] = useSearchParams();
  const [aggregation, setAggregation] = useState<McAggregationPayload | null>(null);
  const [tornado, setTornado] = useState<TornadoBar[]>([]);
  const [jobId, setJobId] = useState<string | null>(null);
  const [source, setSource] = useState<McSource | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [progress, setProgress] = useState<{ done: number; total: number } | null>(null);
  const [etaSec, setEtaSec] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [trials, setTrials] = useState(DEFAULT_TRIALS);
  const [serverless, setServerless] = useState(false);
  const [gitSha, setGitSha] = useState<string | null>(null);
  const [artifactReady, setArtifactReady] = useState(false);
  const pollStart = useRef<number | null>(null);

  const isInstantBase =
    scenario === "base_case" && Object.keys(overrides).length === 0;

  const maxTrials = serverless ? SERVERLESS_MAX_TRIALS : DEFAULT_TRIALS;

  useEffect(() => {
    fetchHealth()
      .then((h) => {
        setGitSha(h.git_sha);
        setServerless(Boolean(h.serverless));
        if (h.serverless) setTrials(Math.min(DEFAULT_TRIALS, SERVERLESS_MAX_TRIALS));
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
    void loadBaseCaseMcArtifact().then((artifact) => {
      applyAggregation(artifact.aggregation, "precache", artifact.job_id);
    });
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

  const provenance = useMemo(() => {
    if (!visibleAggregation) return null;
    const status = visibleAggregation.convergence_status;
    const statusLabel =
      status === "converged"
        ? "complete"
        : status === "partial"
          ? "partial"
          : status === "failed"
            ? "incomplete"
            : status;
    return {
      n_trials: visibleAggregation.n_trials,
      n_converged: visibleAggregation.n_converged,
      base_seed: visibleAggregation.base_seed,
      statusLabel,
    };
  }, [visibleAggregation]);

  const showProgress =
    status === "submitting" ||
    status === "queued" ||
    status === "running" ||
    status === "loading";

  return (
    <section className="client-mc panel" aria-label="Monte Carlo" data-testid="mc-panel">
      <div className="client-mc-header">
        <h2>Monte Carlo</h2>
        {source === "precache" && (
          <span className="audit-badge mc-badge-precache" data-testid="mc-provenance">
            precomputed
          </span>
        )}
        {source === "live" && jobId && (
          <span className="audit-badge" data-testid="mc-provenance">
            run {jobId.slice(0, 8)}
          </span>
        )}
      </div>

      <p className="muted client-mc-intro">
        {isInstantBase
          ? "Base-case distribution loads instantly from precomputed trials. Re-run when you change scenario or inputs."
          : "Run a Monte Carlo study for this scenario to see the Group EV distribution and sensitivity drivers."}
      </p>

      <div className="client-mc-controls">
        <label className="client-mc-trials">
          Trials
          <input
            type="number"
            min={50}
            max={maxTrials}
            step={50}
            value={Math.min(trials, maxTrials)}
            onChange={(e) => setTrials(Number(e.target.value) || DEFAULT_TRIALS)}
            data-testid="mc-trials-input"
          />
        </label>
        <button
          type="button"
          className="secondary-btn"
          onClick={() => void runMc()}
          disabled={showProgress}
          data-testid="mc-run-btn"
        >
          Run Monte Carlo
        </button>
      </div>

      {showProgress && (
        <div className="mc-progress" data-testid="mc-progress" role="status">
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

      {visibleAggregation && evMetrics && histogram && (
        <>
          <h3>Group EV distribution</h3>
          <EvDistributionChart histogram={histogram} metrics={evMetrics} />
          <p className="mc-cvar-readout" data-testid="mc-cvar-readout">
            {cvarReadout(evMetrics.cvar_5, evMetrics.p50)}
          </p>

          {fan && (
            <>
              <h3>Group FCF uncertainty</h3>
              <FcfFanChart fan={fan} />
            </>
          )}

          {tornado.length > 0 && (
            <>
              <h3>What drives this</h3>
              <TornadoChart bars={tornado} />
            </>
          )}

          {provenance && (
            <p className="mc-provenance-line muted" data-testid="mc-provenance-detail">
              {provenance.n_converged.toLocaleString()} of {provenance.n_trials.toLocaleString()}{" "}
              trials · seed {provenance.base_seed} · {provenance.statusLabel}
            </p>
          )}
        </>
      )}

      {!visibleAggregation && !showProgress && !error && !isInstantBase && (
        <p className="muted">Click Run Monte Carlo to generate a distribution for this scenario.</p>
      )}
    </section>
  );
}
