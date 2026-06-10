import type { RunProvenance } from "./scenario-artifacts";
import { artifactShaMatchesDeploy, resolveDeploySha } from "./scenario-artifacts";

export type ArtifactFreshness = "matched" | "stale" | "unknown";

export function resolveArtifactFreshness(
  artifactSha: string | undefined,
  apiGitSha?: string | null,
): ArtifactFreshness {
  if (!artifactSha) return "unknown";
  if (artifactShaMatchesDeploy(artifactSha, apiGitSha)) return "matched";
  const deploy = resolveDeploySha();
  if (deploy || apiGitSha) return "stale";
  return "unknown";
}

export function formatDataAsOf(mtimeUnix?: number | null): string | null {
  if (mtimeUnix == null || !Number.isFinite(mtimeUnix)) return null;
  return new Date(mtimeUnix * 1000).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

/** Client-safe workbook label — no version numbers (context.md §3.11). */
export function clientWorkbookLabel(workbookName?: string | null): string | null {
  if (!workbookName) return null;
  const base = workbookName.replace(/\.xlsx$/i, "").trim();
  const stripped = base
    .replace(/^SpaceX\s+/i, "")
    .replace(/\s*V[\d.]+$/i, "")
    .trim();
  return stripped || "valuation model";
}

export function provenanceLabel(provenance: RunProvenance): string {
  switch (provenance) {
    case "precomputed":
      return "precomputed";
    case "cached":
      return "cached";
    case "fresh":
      return "live";
  }
}

export function freshnessLabel(freshness: ArtifactFreshness): string {
  switch (freshness) {
    case "matched":
      return "current";
    case "stale":
      return "stale";
    case "unknown":
      return "freshness unknown";
  }
}
