const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

export type Scenario = {
  name: string;
  description: string;
  path: string;
};

export type YearSeries = {
  label: string;
  unit: string;
  years: number[];
  values: number[];
  lineage_key: string;
};

export type LineageEntry = {
  key: string;
  display_name: string;
  module_path: string;
  function: string;
  excel_cell: string;
  excel_label: string;
  architecture_ref: string;
  principle: string;
  input_labels: string[];
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
  module_ev: Record<
    string,
    { display_name: string; ev_2025_b: number; lineage_key: string }
  >;
  override_warnings: { label: string; value: string; message: string }[];
  conservation: { all_ok: boolean };
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(detail || `HTTP ${res.status}`);
  }
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
  return request<Scenario[]>("/scenarios");
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

export function fetchTornado(runId: string, topN = 10) {
  return request<{ run_id: string; tornado: TornadoBar[] }>(
    `/runs/${runId}/tornado?top_n=${topN}`,
  );
}

export function fetchLineage(key: string) {
  return request<LineageEntry>(`/lineage/${encodeURIComponent(key)}`);
}

export function submitMc(body: {
  trials: number;
  include_tornado?: boolean;
  tornado_top?: number;
}) {
  return request<{ job_id: string; status: string }>("/runs/mc", {
    method: "POST",
    body: JSON.stringify({
      scenario: "base_case",
      ...body,
    }),
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
        metrics: Record<
          string,
          { p5: number; p50: number; p95: number; base_case: number | null }
        >;
      };
      tornado?: TornadoBar[];
    };
  }>(`/runs/mc/${jobId}`);
}
