import type { RunProvenance } from "./scenario-artifacts";
import {
  clientWorkbookLabel,
  formatDataAsOf,
  freshnessLabel,
  provenanceLabel,
  resolveArtifactFreshness,
  type ArtifactFreshness,
} from "./provenance";

type Props = {
  mode: "audit" | "client";
  workbookName?: string | null;
  workbookMtime?: number | null;
  runProvenance?: RunProvenance;
  artifactSha?: string | null;
  apiGitSha?: string | null;
  buildSha?: string | null;
};

export function ModelProvenanceChip({
  mode,
  workbookName,
  workbookMtime,
  runProvenance,
  artifactSha,
  apiGitSha,
  buildSha,
}: Props) {
  const dataAsOf = formatDataAsOf(workbookMtime);
  const freshness: ArtifactFreshness | null = artifactSha
    ? resolveArtifactFreshness(artifactSha, apiGitSha)
    : null;

  const workbookLabel =
    mode === "client" ? clientWorkbookLabel(workbookName) : workbookName?.replace(/\.xlsx$/i, "");

  return (
    <div className="model-provenance-chip" data-testid="model-provenance-chip">
      {dataAsOf && (
        <span className="model-provenance-item" data-testid="model-data-as-of">
          Data as of {dataAsOf}
        </span>
      )}
      {workbookLabel && mode === "audit" && (
        <span className="model-provenance-item muted" data-testid="model-workbook-name">
          {workbookLabel}
        </span>
      )}
      {runProvenance && (
        <span
          className={`run-provenance provenance-${runProvenance}`}
          data-testid="run-provenance"
        >
          {provenanceLabel(runProvenance)}
        </span>
      )}
      {freshness && runProvenance === "precomputed" && (
        <span
          className={`artifact-freshness freshness-${freshness}`}
          data-testid="artifact-freshness"
        >
          {freshnessLabel(freshness)}
        </span>
      )}
      {mode === "audit" && buildSha && (
        <span className="model-provenance-item" data-testid="model-build-sha">
          build <code>{buildSha}</code>
        </span>
      )}
    </div>
  );
}
