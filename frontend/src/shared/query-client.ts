import { QueryClient } from "@tanstack/react-query";
import type { DeterministicRun, GridPayload, RunAuditPayload } from "./types";
import { runCacheKey } from "./base-case-artifact";

export type CachedRunResult = {
  run_id: string;
  audit_grids: Record<string, GridPayload>;
  run_audit: RunAuditPayload;
  cached: boolean;
  source?: "precomputed" | "live";
};

export const DETERMINISTIC_RUN_QUERY = "deterministic-run";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      retry: 1,
    },
  },
});

export function getCachedRun(
  scenario: string,
  overrides: Record<string, number>,
): CachedRunResult | undefined {
  return queryClient.getQueryData<CachedRunResult>([
    DETERMINISTIC_RUN_QUERY,
    runCacheKey(scenario, overrides),
  ]);
}

export function setCachedRun(
  scenario: string,
  overrides: Record<string, number>,
  result: CachedRunResult,
): void {
  queryClient.setQueryData([DETERMINISTIC_RUN_QUERY, runCacheKey(scenario, overrides)], result);
}

export function cacheFromDeterministicRun(
  scenario: string,
  overrides: Record<string, number>,
  result: DeterministicRun & { audit_grids?: Record<string, GridPayload> },
  runAudit?: RunAuditPayload,
): CachedRunResult {
  const cached: CachedRunResult = {
    run_id: result.run_id,
    audit_grids: result.audit_grids ?? {},
    run_audit: runAudit ?? ({} as RunAuditPayload),
    cached: result.cached,
    source: "live",
  };
  setCachedRun(scenario, overrides, cached);
  return cached;
}
