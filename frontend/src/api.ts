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

export type TornadoBar = {
  label: string;
  low_ev: number;
  high_ev: number;
  base_ev: number;
  delta: number;
};

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

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!res.ok) throw new Error(await res.text() || `HTTP ${res.status}`);
  return res.json() as Promise<T>;
}

export function fetchHealth() {
  return request<{
    status: string;
    git_sha: string | null;
    serverless?: boolean;
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
  overrides: Record<string, number>;
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

export function fetchTornado(runId: string, topN = 10) {
  return request<{ run_id: string; tornado: TornadoBar[] }>(
    `/runs/${runId}/tornado?top_n=${topN}`,
  );
}

export function submitMc(body: {
  trials: number;
  include_tornado?: boolean;
  tornado_top?: number;
}) {
  return request<{ job_id: string; status: string }>("/runs/mc", {
    method: "POST",
    body: JSON.stringify({ scenario: "base_case", ...body }),
  });
}

export function fetchMcJob(jobId: string) {
  return request<{
    job_id: string;
    status: string;
    progress?: { trials_done: number; trials: number };
    error?: string;
    result?: {
      aggregation: {
        metrics: Record<string, { p5: number; p50: number; p95: number; base_case: number | null }>;
      };
      tornado?: TornadoBar[];
    };
  }>(`/runs/mc/${jobId}`);
}
