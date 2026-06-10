export type {
  Scenario,
  LineageEntry,
  GridPayload,
  SheetMeta,
  ActiveCell,
} from "./shared/types";

export type YearSeries = {
  label: string;
  unit: string;
  years: number[];
  values: number[];
  lineage_key: string;
};

export type {
  TornadoBar,
  McMetricSummary,
  McHistogram,
  McFcfFan,
  McAggregationPayload,
  McJobResult,
  McJobStatus,
  BaseCaseMcArtifact,
} from "./shared/types";

export type DeterministicRun = {
  run_id: string;
  scenario: string;
  cached: boolean;
  audit: Record<string, unknown>;
  solver: { iterations: number; converged: boolean; max_residual: number };
  valuation: {
    group_ev_2025_b: number;
    group_wacc: number;
    terminal_growth: number;
    lineage_key: string;
  };
  group: Record<string, YearSeries>;
  modules: Record<
    string,
    {
      display_name: string;
      total_revenue: YearSeries;
      module_fcf: YearSeries;
      module_ebitda: YearSeries;
      blended_irr: YearSeries;
    }
  >;
  module_ev: Record<string, { display_name: string; ev_2025_b: number; lineage_key: string }>;
  override_warnings: { label: string; value: string; message: string }[];
  conservation: { all_ok: boolean };
  audit_grids?: Record<string, import("./shared/types").GridPayload>;
};

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";
const API_KEY = import.meta.env.VITE_API_KEY as string | undefined;

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (API_KEY) headers["X-API-Key"] = API_KEY;
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { ...headers, ...init?.headers },
  });
  if (!res.ok) throw new Error(await res.text() || `HTTP ${res.status}`);
  return res.json() as Promise<T>;
}

export function fetchHealth() {
  return request<{
    status: string;
    git_sha: string | null;
    serverless?: boolean;
    custom_mc_enabled?: boolean;
    precached_scenarios?: string[];
    precache_mc_trials?: number;
  }>("/health");
}

export function fetchScenarios() {
  return request<import("./shared/types").Scenario[]>("/scenarios");
}

export function fetchSheets() {
  return request<import("./shared/types").SheetMeta[]>("/sheets");
}

export function fetchSheetGrid(runId: string, sheetSlug: string, scenario?: string) {
  const params = new URLSearchParams({ run_id: runId });
  if (scenario) params.set("scenario", scenario);
  return request<import("./shared/types").GridPayload>(
    `/sheets/${sheetSlug}/grid?${params.toString()}`,
  );
}

export function runDeterministic(body: {
  scenario: string;
  overrides?: Record<string, number>;
  client_overrides?: Record<string, number>;
  use_cache?: boolean;
}) {
  return request<DeterministicRun>("/runs/deterministic", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function fetchLineage(
  key: string,
  opts?: { runId?: string; year?: number; sheet?: string; row?: number; scenario?: string },
) {
  const params = new URLSearchParams();
  if (opts?.runId) params.set("run_id", opts.runId);
  if (opts?.year != null) params.set("year", String(opts.year));
  if (opts?.sheet) params.set("sheet", opts.sheet);
  if (opts?.row != null) params.set("row", String(opts.row));
  if (opts?.scenario) params.set("scenario", opts.scenario);
  const qs = params.toString();
  return request<import("./shared/types").LineageEntry>(
    `/lineage/${encodeURIComponent(key)}${qs ? `?${qs}` : ""}`,
  );
}

export function fetchLineageHistory(key: string, opts?: { limit?: number; year?: number }) {
  const params = new URLSearchParams();
  if (opts?.limit != null) params.set("limit", String(opts.limit));
  if (opts?.year != null) params.set("year", String(opts.year));
  const qs = params.toString();
  return request<{ key: string; entries: import("./shared/types").ChangeHistoryEntry[]; total: number }>(
    `/lineage/${encodeURIComponent(key)}/history${qs ? `?${qs}` : ""}`,
  );
}

export function fetchLineageGraph(
  key: string,
  opts: {
    runId: string;
    depth?: number;
    year?: number;
    sheet?: string;
    row?: number;
    scenario?: string;
  },
) {
  const params = new URLSearchParams({ run_id: opts.runId });
  if (opts.depth != null) params.set("depth", String(opts.depth));
  if (opts.year != null) params.set("year", String(opts.year));
  if (opts.sheet) params.set("sheet", opts.sheet);
  if (opts.row != null) params.set("row", String(opts.row));
  if (opts.scenario) params.set("scenario", opts.scenario);
  return request<import("./shared/types").LineageGraphPayload>(
    `/lineage/${encodeURIComponent(key)}/graph?${params.toString()}`,
  );
}

export function fetchRunAuditDashboard(runId: string, scenario?: string) {
  const params = new URLSearchParams();
  if (scenario) params.set("scenario", scenario);
  const qs = params.toString();
  return request<import("./shared/types").RunAuditPayload>(
    `/runs/${encodeURIComponent(runId)}/audit-dashboard${qs ? `?${qs}` : ""}`,
  );
}

export function fetchTornado(runId: string, topN = 10) {
  return request<{ run_id: string; tornado: import("./shared/types").TornadoBar[] }>(
    `/runs/${runId}/tornado?top_n=${topN}`,
  );
}

export function submitMc(body: {
  trials: number;
  scenario?: string;
  base_seed?: number;
  include_tornado?: boolean;
  tornado_top?: number;
}) {
  return request<{ job_id: string; status: string; execution?: string }>("/runs/mc", {
    method: "POST",
    body: JSON.stringify({ scenario: "base_case", ...body }),
  });
}

export type CalibrationStatus = {
  calibrated: boolean;
  pending_count: number;
  enforced_count: number;
  total_count: number;
  pending_anchors: string[];
};

export function fetchClientCalibrationStatus() {
  return request<CalibrationStatus>("/client/calibration-status");
}

export function fetchClientScenarios() {
  return request<import("./shared/types").ClientScenarioCard[]>("/client/scenarios");
}

export function fetchClientInputWhitelist() {
  return request<import("./shared/types").ClientInputSpec[]>("/client/inputs/whitelist");
}

export function validateClientShare(body: {
  scenario: string;
  overrides: Record<string, number>;
}) {
  return request<{
    ok: boolean;
    scenario: string;
    share_token: string;
    canonical_overrides: Record<string, unknown>;
  }>("/client/validate-share", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export function decodeClientShare(token: string) {
  return request<{
    scenario: string;
    overrides: Record<string, number>;
    canonical_overrides: Record<string, unknown>;
  }>(`/client/decode-share?s=${encodeURIComponent(token)}`);
}

export async function downloadScenarioXlsx(body: {
  run_id?: string;
  scenario: string;
  overrides?: Record<string, number>;
  public_base_url?: string;
}) {
  const res = await fetch(`${API_BASE}/exports/scenario.xlsx`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(await res.text() || `HTTP ${res.status}`);
  return res.blob();
}

export async function downloadScenarioPackXlsx(publicBaseUrl?: string) {
  const res = await fetch(`${API_BASE}/exports/scenario_pack.xlsx`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      scenarios: ["base_case", "bear", "bull"],
      public_base_url: publicBaseUrl ?? "",
    }),
  });
  if (!res.ok) throw new Error(await res.text() || `HTTP ${res.status}`);
  return res.blob();
}

export function methodologyDownloadUrl() {
  return `${API_BASE}/client/methodology`;
}

export function fetchMcJob(jobId: string) {
  return request<import("./shared/types").McJobStatus>(`/runs/mc/${jobId}`);
}

export function fetchMcDistribution(jobId: string) {
  return request<{
    job_id: string;
    scenario?: string;
    n_trials: number;
    n_converged: number;
    base_seed: number;
    convergence_status: string;
    group_ev_histogram?: import("./shared/types").McHistogram;
    group_fcf_fan?: import("./shared/types").McFcfFan;
    metrics: Record<string, import("./shared/types").McMetricSummary>;
    convergence_trace?: Record<string, number[]>;
  }>(`/runs/mc/${jobId}/distribution`);
}
