import type { DeterministicRun, GridPayload, RunAuditPayload } from "./types";
import type { BaseCaseMcArtifact } from "./types";

export const PRECACHE_SCENARIOS = ["base_case", "bear", "bull", "mars_share"] as const;
export type PrecachedScenario = (typeof PRECACHE_SCENARIOS)[number];

export type RunProvenance = "precomputed" | "cached" | "fresh";

export type ScenarioRunArtifact = {
  git_sha: string;
  scenario: string;
  run_id: string;
  audit_grids: Record<string, GridPayload>;
  run_audit: RunAuditPayload;
  deterministic: Pick<
    DeterministicRun,
    "run_id" | "scenario" | "cached" | "solver" | "conservation"
  >;
};

const runCache = new Map<string, ScenarioRunArtifact>();
const runInflight = new Map<string, Promise<ScenarioRunArtifact>>();
const mcCache = new Map<string, BaseCaseMcArtifact>();
const mcInflight = new Map<string, Promise<BaseCaseMcArtifact>>();

export function isPrecachedScenario(scenario: string): boolean {
  return (PRECACHE_SCENARIOS as readonly string[]).includes(scenario);
}

export function runArtifactUrl(scenario: string): string {
  return `/data/${scenario}_run.json`;
}

export function mcArtifactUrl(scenario: string): string {
  return `/data/${scenario}_mc.json`;
}

export function resolveDeploySha(): string | null {
  const raw = import.meta.env.VITE_DEPLOY_SHA;
  if (!raw) return null;
  return raw.length > 7 ? raw.slice(0, 7) : raw;
}

export function artifactShaMatchesDeploy(
  artifactSha: string,
  apiGitSha?: string | null,
): boolean {
  const deploy = resolveDeploySha();
  if (deploy) return artifactSha === deploy || artifactSha.startsWith(deploy);
  if (apiGitSha) return artifactSha === apiGitSha;
  return false;
}

export function getScenarioRunArtifact(scenario: string): ScenarioRunArtifact | null {
  return runCache.get(scenario) ?? null;
}

export async function loadScenarioRunArtifact(scenario: string): Promise<ScenarioRunArtifact> {
  const cached = runCache.get(scenario);
  if (cached) return cached;
  let inflight = runInflight.get(scenario);
  if (!inflight) {
    inflight = fetch(runArtifactUrl(scenario))
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load ${scenario} run artifact (${res.status})`);
        return res.json() as Promise<ScenarioRunArtifact>;
      })
      .then((data) => {
        runCache.set(scenario, data);
        return data;
      });
    runInflight.set(scenario, inflight);
  }
  return inflight;
}

export async function preloadScenarioRunArtifacts(): Promise<void> {
  await Promise.all(PRECACHE_SCENARIOS.map((s) => loadScenarioRunArtifact(s).catch(() => undefined)));
}

export function getScenarioMcArtifact(scenario: string): BaseCaseMcArtifact | null {
  return mcCache.get(scenario) ?? null;
}

export async function loadScenarioMcArtifact(scenario: string): Promise<BaseCaseMcArtifact> {
  const cached = mcCache.get(scenario);
  if (cached) return cached;
  let inflight = mcInflight.get(scenario);
  if (!inflight) {
    inflight = fetch(mcArtifactUrl(scenario))
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load ${scenario} MC artifact (${res.status})`);
        return res.json() as Promise<BaseCaseMcArtifact>;
      })
      .then((data) => {
        mcCache.set(scenario, data);
        return data;
      });
    mcInflight.set(scenario, inflight);
  }
  return inflight;
}

export async function preloadScenarioMcArtifacts(): Promise<void> {
  await Promise.all(PRECACHE_SCENARIOS.map((s) => loadScenarioMcArtifact(s).catch(() => undefined)));
}

export function canHydrateRunFromArtifact(
  scenario: string,
  overrides: Record<string, number>,
  apiGitSha?: string | null,
): boolean {
  if (!isPrecachedScenario(scenario)) return false;
  if (Object.keys(overrides).length > 0) return false;
  const loaded = runCache.get(scenario);
  if (!loaded) return false;
  return artifactShaMatchesDeploy(loaded.git_sha, apiGitSha);
}

export function canHydrateMcFromArtifact(
  scenario: string,
  overrides: Record<string, number>,
  apiGitSha?: string | null,
): boolean {
  if (!isPrecachedScenario(scenario)) return false;
  if (Object.keys(overrides).length > 0) return false;
  const loaded = mcCache.get(scenario);
  if (!loaded) return false;
  return artifactShaMatchesDeploy(loaded.git_sha, apiGitSha);
}

export function isInstantPrecacheView(
  scenario: string,
  overrides: Record<string, number>,
): boolean {
  return isPrecachedScenario(scenario) && Object.keys(overrides).length === 0;
}

export function runCacheKey(scenario: string, overrides: Record<string, number>): string {
  const sorted = Object.keys(overrides)
    .sort()
    .map((k) => `${k}=${overrides[k]}`)
    .join("|");
  return `${scenario}::${sorted}`;
}
