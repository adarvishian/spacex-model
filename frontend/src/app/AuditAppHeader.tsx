import { Link } from "react-router-dom";
import { ModelProvenanceChip } from "../shared/ModelProvenanceChip";
import type { RunProvenance } from "../shared/scenario-artifacts";

type Props = {
  selectedScenario: string;
  runId: string | null;
  provenance: RunProvenance;
  workbookName?: string | null;
  workbookMtime?: number | null;
  artifactSha?: string | null;
  apiGitSha?: string | null;
};

export function AuditAppHeader({
  selectedScenario,
  runId,
  provenance,
  workbookName,
  workbookMtime,
  artifactSha,
  apiGitSha,
}: Props) {
  return (
    <header className="audit-header">
      <div className="audit-header-left">
        <h1>Mach33 SpaceX Valuation Model</h1>
        <span className="audit-badge">AUDIT MODE</span>
      </div>
      <div className="audit-header-meta">
        <span>
          scenario: <strong>{selectedScenario.replace("_", " ")}</strong>
        </span>
        {runId && (
          <span>
            run: <code>{runId}</code>
          </span>
        )}
        <ModelProvenanceChip
          mode="audit"
          workbookName={workbookName}
          workbookMtime={workbookMtime}
          runProvenance={provenance}
          artifactSha={artifactSha}
          apiGitSha={apiGitSha}
          buildSha={apiGitSha}
        />
        <Link to="/client" className="mode-switch">
          Switch to Client Mode →
        </Link>
      </div>
    </header>
  );
}
