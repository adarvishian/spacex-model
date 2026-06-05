import type { DeterministicRun, GridPayload, RunAuditPayload } from "./types";

export type RunProvenance = "precomputed" | "cached" | "fresh";

export type BaseCaseArtifact = {
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

const ARTIFACT_URL = "/data/base_case_run.json";

let loaded: BaseCaseArtifact | null = null;
let inflight: Promise<BaseCaseArtifact> | null = null;

export function getBaseCaseArtifact(): BaseCaseArtifact | null {
  return loaded;
}

export async function loadBaseCaseArtifact(): Promise<BaseCaseArtifact> {
  if (loaded) return loaded;
  if (!inflight) {
    inflight = fetch(ARTIFACT_URL)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load base case artifact (${res.status})`);
        return res.json() as Promise<BaseCaseArtifact>;
      })
      .then((data) => {
        loaded = data;
        return data;
      });
  }
  return inflight;
}

export function artifactMatchesGitSha(gitSha: string | null | undefined): boolean {
  if (!loaded) return false;
  if (!gitSha) return true;
  return loaded.git_sha === gitSha;
}

export function canHydrateFromArtifact(
  scenario: string,
  overrides: Record<string, number>,
  gitSha: string | null | undefined,
): boolean {
  if (!loaded) return false;
  if (scenario !== "base_case") return false;
  if (Object.keys(overrides).length > 0) return false;
  return artifactMatchesGitSha(gitSha);
}

export function runCacheKey(scenario: string, overrides: Record<string, number>): string {
  const sorted = Object.keys(overrides)
    .sort()
    .map((k) => `${k}=${overrides[k]}`)
    .join("|");
  return `${scenario}::${sorted}`;
}
