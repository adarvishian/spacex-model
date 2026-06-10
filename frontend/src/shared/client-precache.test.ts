import { describe, expect, it } from "vitest";
import { clientSummaryFromArtifact } from "./client-precache";
import type { ScenarioRunArtifact } from "./scenario-artifacts";

describe("client precache", () => {
  it("builds client summary from full deterministic payload", () => {
    const artifact = {
      git_sha: "abc1234",
      scenario: "base_case",
      run_id: "run1",
      audit_grids: {},
      run_audit: {} as ScenarioRunArtifact["run_audit"],
      deterministic: {
        run_id: "run1",
        scenario: "base_case",
        cached: false,
        solver: { iterations: 1, converged: true, max_residual: 0 },
        valuation: { group_ev_2025_b: 278, lineage_key: "valuation.group_ev" },
        module_ev: { starlink: { display_name: "Starlink", ev_2025_b: 164 } },
        group: { group_fcf: { years: [2025], values: [1000] } },
        modules: {
          starlink: {
            display_name: "Starlink",
            total_revenue: { values: [1] },
            blended_irr: { values: [0.2] },
          },
        },
        override_warnings: [],
      },
    } as ScenarioRunArtifact;

    const summary = clientSummaryFromArtifact(artifact);
    expect(summary?.valuation.group_ev_2025_b).toBe(278);
    expect(summary?.module_ev.starlink.ev_2025_b).toBe(164);
  });

  it("returns null for legacy partial deterministic payloads", () => {
    const artifact = {
      git_sha: "abc1234",
      scenario: "base_case",
      run_id: "run1",
      audit_grids: {},
      run_audit: {} as ScenarioRunArtifact["run_audit"],
      deterministic: {
        run_id: "run1",
        scenario: "base_case",
        cached: false,
        solver: { iterations: 1, converged: true, max_residual: 0 },
        valuation: { group_ev_2025_b: 278, lineage_key: "x" },
        override_warnings: [],
      },
    } as ScenarioRunArtifact;

    expect(clientSummaryFromArtifact(artifact)).toBeNull();
  });
});
