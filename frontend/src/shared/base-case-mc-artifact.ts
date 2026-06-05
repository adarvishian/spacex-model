import type { BaseCaseMcArtifact } from "./types";

const ARTIFACT_URL = "/data/base_case_mc.json";

let loaded: BaseCaseMcArtifact | null = null;
let inflight: Promise<BaseCaseMcArtifact> | null = null;

export function getBaseCaseMcArtifact(): BaseCaseMcArtifact | null {
  return loaded;
}

export async function loadBaseCaseMcArtifact(): Promise<BaseCaseMcArtifact> {
  if (loaded) return loaded;
  if (!inflight) {
    inflight = fetch(ARTIFACT_URL)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load base case MC artifact (${res.status})`);
        return res.json() as Promise<BaseCaseMcArtifact>;
      })
      .then((data) => {
        loaded = data;
        return data;
      });
  }
  return inflight;
}

export function mcArtifactMatchesGitSha(gitSha: string | null | undefined): boolean {
  if (!loaded) return false;
  if (!gitSha) return true;
  return loaded.git_sha === gitSha;
}

export function canHydrateMcFromArtifact(
  scenario: string,
  overrides: Record<string, number>,
  gitSha: string | null | undefined,
): boolean {
  if (!loaded) return false;
  if (scenario !== "base_case") return false;
  if (Object.keys(overrides).length > 0) return false;
  return mcArtifactMatchesGitSha(gitSha);
}
