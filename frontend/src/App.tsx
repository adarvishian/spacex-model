import { useCallback, useEffect, useState } from "react";
import {
  DeterministicRun,
  LineageEntry,
  TornadoBar,
  fetchHealth,
  fetchLineage,
  fetchScenarios,
  fetchTornado,
  runDeterministic,
  submitMc,
  fetchMcJob,
  Scenario,
} from "./api";
import { FcfTable } from "./components/FcfTable";
import { LineagePanel } from "./components/LineagePanel";
import { ScenarioPicker } from "./components/ScenarioPicker";
import { TornadoChart } from "./components/TornadoChart";

type Tab = "deterministic" | "mc";

function formatBillions(v: number): string {
  return `$${v.toFixed(1)}B`;
}

function formatMm(v: number): string {
  if (Math.abs(v) >= 1000) return `$${(v / 1000).toFixed(1)}B`;
  return `$${v.toFixed(0)}M`;
}

export default function App() {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selectedScenario, setSelectedScenario] = useState("base_case");
  const [overrideLabel, setOverrideLabel] = useState("TAM inflation rate (annual)");
  const [overrideValue, setOverrideValue] = useState("");
  const [run, setRun] = useState<DeterministicRun | null>(null);
  const [tornado, setTornado] = useState<TornadoBar[]>([]);
  const [lineage, setLineage] = useState<LineageEntry | null>(null);
  const [loading, setLoading] = useState(false);
  const [tornadoLoading, setTornadoLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [gitSha, setGitSha] = useState<string | null>(null);
  const [tab, setTab] = useState<Tab>("deterministic");
  const [mcJobId, setMcJobId] = useState<string | null>(null);
  const [mcStatus, setMcStatus] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth()
      .then((h) => setGitSha(h.git_sha))
      .catch(() => undefined);
    fetchScenarios()
      .then(setScenarios)
      .catch((e) => setError(String(e)));
  }, []);

  const openLineage = useCallback(async (key: string) => {
    try {
      const entry = await fetchLineage(key);
      setLineage(entry);
    } catch (e) {
      setError(String(e));
    }
  }, []);

  const handleRun = async () => {
    setLoading(true);
    setError(null);
    setTornado([]);
    try {
      const overrides: Record<string, number> = {};
      if (overrideValue.trim()) {
        overrides[overrideLabel] = parseFloat(overrideValue);
      }
      const result = await runDeterministic({
        scenario: selectedScenario,
        overrides,
        use_cache: true,
      });
      setRun(result);
      setTornadoLoading(true);
      const tornadoRes = await fetchTornado(result.run_id, 10);
      setTornado(tornadoRes.tornado);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
      setTornadoLoading(false);
    }
  };

  const handleMc = async () => {
    setError(null);
    setMcStatus("submitting");
    try {
      const { job_id } = await submitMc({ trials: 200, include_tornado: true, tornado_top: 10 });
      setMcJobId(job_id);
      setMcStatus("queued");
      const poll = async () => {
        const job = await fetchMcJob(job_id);
        setMcStatus(job.status);
        if (job.status === "completed" && job.result?.tornado) {
          setTornado(job.result.tornado);
        }
        if (job.status === "queued" || job.status === "running") {
          setTimeout(poll, 2000);
        } else if (job.status === "failed") {
          setError(job.error ?? "MC job failed");
        }
      };
      setTimeout(poll, 1500);
    } catch (e) {
      setError(String(e));
      setMcStatus(null);
    }
  };

  return (
    <div className="app-shell">
      <header>
        <div>
          <h1>Mach33 SpaceX Valuation Model</h1>
          <p>Scenario explorer · audit-grade lineage · Base Case</p>
        </div>
        <div className="badge">
          {run?.cached ? "Cached result" : "Live run"}
          {gitSha ? ` · build ${gitSha}` : ""}
        </div>
      </header>

      {error && <div className="alert error">{error}</div>}

      <div className="layout">
        <aside className="stack">
          <ScenarioPicker
            scenarios={scenarios}
            selected={selectedScenario}
            onSelect={setSelectedScenario}
            overrideLabel={overrideLabel}
            overrideValue={overrideValue}
            onOverrideLabel={setOverrideLabel}
            onOverrideValue={setOverrideValue}
            onRun={handleRun}
            loading={loading}
          />
          <div className="panel">
            <h2>Monte Carlo</h2>
            <p style={{ fontSize: "0.85rem", color: "var(--muted)", margin: "0 0 0.75rem" }}>
              Quick 200-trial study with tornado (dev preview).
            </p>
            <button className="secondary-btn" onClick={handleMc} disabled={!!mcStatus && mcStatus === "running"}>
              Run MC preview
            </button>
            {mcJobId && (
              <p style={{ fontSize: "0.8rem", color: "var(--muted)", marginTop: "0.5rem" }}>
                Job {mcJobId}: {mcStatus}
              </p>
            )}
          </div>
        </aside>

        <main className="stack">
          <div className="tabs">
            <button
              className={`tab ${tab === "deterministic" ? "active" : ""}`}
              onClick={() => setTab("deterministic")}
            >
              Deterministic
            </button>
            <button
              className={`tab ${tab === "mc" ? "active" : ""}`}
              onClick={() => setTab("mc")}
            >
              Sensitivity
            </button>
          </div>

          {run?.override_warnings?.length ? (
            <div className="alert warn">
              {run.override_warnings.map((w) => (
                <div key={w.label}>
                  {w.label}: {w.message}
                </div>
              ))}
            </div>
          ) : null}

          {run && tab === "deterministic" && (
            <>
              <div className="panel">
                <h2>Group &amp; Module EV (2025)</h2>
                <div className="metrics-grid">
                  <button
                    type="button"
                    className="metric-card"
                    onClick={() => openLineage(run.valuation.lineage_key)}
                  >
                    <div className="label">Group EV</div>
                    <div className="value">{formatBillions(run.valuation.group_ev_2025_b)}</div>
                  </button>
                  {Object.entries(run.module_ev).map(([key, mod]) => (
                    <button
                      key={key}
                      type="button"
                      className="metric-card"
                      onClick={() => openLineage(mod.lineage_key)}
                    >
                      <div className="label">{mod.display_name}</div>
                      <div className="value">{formatBillions(mod.ev_2025_b)}</div>
                    </button>
                  ))}
                </div>
                <p style={{ fontSize: "0.78rem", color: "var(--muted)", margin: 0 }}>
                  Click any metric for audit lineage. Run {run.run_id} ·{" "}
                  {run.solver.converged ? "converged" : "not converged"} in{" "}
                  {run.solver.iterations} iterations.
                </p>
              </div>

              <div className="panel">
                <h2>Group FCF ($mm)</h2>
                <FcfTable
                  rows={[
                    { label: "Group FCF", series: run.group.group_fcf, lineageKey: "group.group_fcf" },
                    { label: "Group EBITDA", series: run.group.group_ebitda, lineageKey: "group.group_ebitda" },
                    { label: "Group Revenue", series: run.group.group_revenue_net, lineageKey: "group.group_revenue_net" },
                  ]}
                  onCellClick={openLineage}
                  formatValue={formatMm}
                />
              </div>

              <div className="panel">
                <h2>Per-Module FCF ($mm)</h2>
                <FcfTable
                  rows={Object.entries(run.modules).map(([key, mod]) => ({
                    label: mod.display_name,
                    series: mod.module_fcf,
                    lineageKey: `module.${key}.module_fcf`,
                  }))}
                  onCellClick={openLineage}
                  formatValue={formatMm}
                />
              </div>
            </>
          )}

          {(tab === "mc" || tornado.length > 0) && (
            <div className="panel">
              <h2>Tornado — Δ Group EV (±1σ)</h2>
              {tornadoLoading && <p style={{ color: "var(--muted)" }}>Computing sensitivity…</p>}
              {!tornadoLoading && tornado.length === 0 && (
                <p style={{ color: "var(--muted)" }}>Run a scenario to generate tornado bars.</p>
              )}
              {tornado.length > 0 && <TornadoChart bars={tornado} />}
            </div>
          )}
        </main>
      </div>

      {lineage && <LineagePanel entry={lineage} onClose={() => setLineage(null)} />}
    </div>
  );
}
