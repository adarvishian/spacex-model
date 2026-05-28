import type {
  DeterministicRun,
  GridPayload,
  LineageEntry,
  Scenario,
  SheetMeta,
} from "./types";

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

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
  return request<{ status: string; git_sha: string | null; serverless?: boolean }>("/health");
}

export function fetchScenarios() {
  return request<Scenario[]>("/scenarios");
}

export function fetchSheets() {
  return request<SheetMeta[]>("/sheets");
}

export function fetchSheetGrid(runId: string, sheetSlug: string) {
  return request<GridPayload>(`/sheets/${sheetSlug}/grid?run_id=${encodeURIComponent(runId)}`);
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
  opts?: { runId?: string; year?: number; sheet?: string; row?: number },
) {
  const params = new URLSearchParams();
  if (opts?.runId) params.set("run_id", opts.runId);
  if (opts?.year != null) params.set("year", String(opts.year));
  if (opts?.sheet) params.set("sheet", opts.sheet);
  if (opts?.row != null) params.set("row", String(opts.row));
  const qs = params.toString();
  return request<LineageEntry>(`/lineage/${encodeURIComponent(key)}${qs ? `?${qs}` : ""}`);
}

export type { Scenario, SheetMeta, GridPayload, LineageEntry, DeterministicRun };
