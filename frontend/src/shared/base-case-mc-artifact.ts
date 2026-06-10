/** Back-compat re-exports — use scenario-artifacts.ts for multi-scenario precache. */
export {
  artifactShaMatchesDeploy as mcArtifactMatchesGitSha,
  canHydrateMcFromArtifact,
  getScenarioMcArtifact as getBaseCaseMcArtifact,
  loadScenarioMcArtifact as loadBaseCaseMcArtifact,
  preloadScenarioMcArtifacts,
} from "./scenario-artifacts";
