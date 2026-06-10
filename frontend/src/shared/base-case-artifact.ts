/** Back-compat re-exports — use scenario-artifacts.ts for multi-scenario precache. */
export type {
  RunProvenance,
  ScenarioRunArtifact as BaseCaseArtifact,
} from "./scenario-artifacts";

export {
  PRECACHE_SCENARIOS,
  artifactShaMatchesDeploy as artifactMatchesGitSha,
  canHydrateRunFromArtifact as canHydrateFromArtifact,
  getScenarioRunArtifact as getBaseCaseArtifact,
  loadScenarioRunArtifact as loadBaseCaseArtifact,
  preloadScenarioRunArtifacts,
  runCacheKey,
} from "./scenario-artifacts";
