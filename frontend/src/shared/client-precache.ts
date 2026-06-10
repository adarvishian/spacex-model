import type { ClientRunSummary, DeterministicRun } from "./types";
import type { ScenarioRunArtifact } from "./scenario-artifacts";
import { hasClientRunPayload } from "./scenario-artifacts";

export function clientSummaryFromDeterministic(run: DeterministicRun): ClientRunSummary {
  const groupFcf = run.group?.group_fcf as { years?: number[]; values?: number[] } | undefined;
  return {
    run_id: run.run_id,
    scenario: run.scenario,
    valuation: run.valuation,
    module_ev: (run.module_ev ?? {}) as ClientRunSummary["module_ev"],
    group: {
      group_fcf: {
        years: groupFcf?.years ?? [],
        values: groupFcf?.values ?? [],
      },
    },
    modules: (run.modules ?? {}) as ClientRunSummary["modules"],
    override_warnings: run.override_warnings ?? [],
  };
}

export function clientSummaryFromArtifact(artifact: ScenarioRunArtifact): ClientRunSummary | null {
  if (!hasClientRunPayload(artifact.deterministic)) return null;
  return clientSummaryFromDeterministic(artifact.deterministic);
}
