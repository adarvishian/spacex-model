import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  fetchHealth,
  fetchRunAuditDashboard,
  fetchScenarios,
  runDeterministic,
} from "../../api";
import type { RunProvenance } from "../../shared/scenario-artifacts";
import {
  canHydrateRunFromArtifact,
  canUsePrecacheRunArtifact,
  getScenarioRunArtifact,
  isInstantPrecacheView,
  preloadScenarioRunArtifacts,
} from "../../shared/scenario-artifacts";
import {
  cacheFromDeterministicRun,
  getCachedRun,
  setCachedRun,
} from "../../shared/query-client";
import type { GridPayload, RunAuditPayload } from "../../shared/types";

function buildOverrides(overrideLabel: string, overrideValue: string): Record<string, number> {
  const overrides: Record<string, number> = {};
  if (overrideValue.trim() && overrideLabel) {
    overrides[overrideLabel] = parseFloat(overrideValue);
  }
  return overrides;
}

export function useAuditRun() {
  const [artifactReady, setArtifactReady] = useState(false);
  const [selectedScenario, setSelectedScenario] = useState("base_case");
  const [overrideLabel, setOverrideLabel] = useState("");
  const [overrideValue, setOverrideValue] = useState("");
  const [runId, setRunId] = useState<string | null>(null);
  const [embeddedGrids, setEmbeddedGrids] = useState<Record<string, GridPayload>>({});
  const [runAuditPayload, setRunAuditPayload] = useState<RunAuditPayload | null>(null);
  const [provenance, setProvenance] = useState<RunProvenance>("fresh");
  const [running, setRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const backgroundRunRef = useRef(false);

  const healthQ = useQuery({ queryKey: ["health"], queryFn: fetchHealth });
  const scenariosQ = useQuery({ queryKey: ["scenarios"], queryFn: fetchScenarios });

  const overrides = useMemo(
    () => buildOverrides(overrideLabel, overrideValue),
    [overrideLabel, overrideValue],
  );

  const artifactSha = getScenarioRunArtifact(selectedScenario)?.git_sha ?? null;

  useEffect(() => {
    let cancelled = false;
    void preloadScenarioRunArtifacts()
      .then(() => {
        if (!cancelled) setArtifactReady(true);
      })
      .catch(() => {
        if (!cancelled) setArtifactReady(true);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const waitingForArtifact =
    isInstantPrecacheView(selectedScenario, overrides) &&
    !artifactReady &&
    !getCachedRun(selectedScenario, overrides);

  const handleRun = useCallback(
    async (opts?: { background?: boolean }) => {
      const background = opts?.background ?? false;
      backgroundRunRef.current = background;

      const cached = getCachedRun(selectedScenario, overrides);
      if (cached) {
        setRunId(cached.run_id);
        setEmbeddedGrids(cached.audit_grids);
        setRunAuditPayload(cached.run_audit);
        setProvenance(cached.source === "precomputed" ? "precomputed" : "cached");
        setRunning(false);
        return;
      }

      if (!background) setRunning(true);
      setError(null);

      try {
        const result = await runDeterministic({
          scenario: selectedScenario,
          overrides,
          use_cache: true,
        });

        let audit: RunAuditPayload | null = runAuditPayload;
        try {
          audit = await fetchRunAuditDashboard(result.run_id, selectedScenario);
        } catch {
          audit = runAuditPayload;
        }

        const grids = result.audit_grids ?? embeddedGrids;
        setRunId(result.run_id);
        if (Object.keys(grids).length > 0) setEmbeddedGrids(grids);
        if (audit) setRunAuditPayload(audit);

        cacheFromDeterministicRun(
          selectedScenario,
          overrides,
          { ...result, audit_grids: grids },
          audit ?? undefined,
        );

        if (!background) setProvenance(result.cached ? "cached" : "fresh");
      } catch (e) {
        if (!background) setError(String(e));
      } finally {
        setRunning(false);
        backgroundRunRef.current = false;
      }
    },
    [embeddedGrids, overrides, runAuditPayload, selectedScenario],
  );

  useEffect(() => {
    if (waitingForArtifact) return;

    const cached = getCachedRun(selectedScenario, overrides);
    if (cached) {
      setRunId(cached.run_id);
      setEmbeddedGrids(cached.audit_grids);
      setRunAuditPayload(cached.run_audit);
      setProvenance(cached.source === "precomputed" ? "precomputed" : "cached");
      return;
    }

    const gitSha = healthQ.data?.git_sha;
    const serverless = Boolean(healthQ.data?.serverless);
    const artifact = getScenarioRunArtifact(selectedScenario);
    if (artifact && canUsePrecacheRunArtifact(selectedScenario, overrides)) {
      setRunId(artifact.run_id);
      setEmbeddedGrids(artifact.audit_grids);
      setRunAuditPayload(artifact.run_audit);
      setProvenance("precomputed");
      setCachedRun(selectedScenario, overrides, {
        run_id: artifact.run_id,
        audit_grids: artifact.audit_grids,
        run_audit: artifact.run_audit,
        cached: true,
        source: "precomputed",
      });
      if (!serverless && canHydrateRunFromArtifact(selectedScenario, overrides, gitSha)) {
        void handleRun({ background: true });
      }
      return;
    }

    if (serverless && isInstantPrecacheView(selectedScenario, overrides)) {
      return;
    }

    setRunId(null);
    setEmbeddedGrids({});
    setRunAuditPayload(null);
    setProvenance("fresh");
    void handleRun();
    // eslint-disable-next-line react-hooks/exhaustive-deps -- overrides use explicit Re-run
  }, [selectedScenario, artifactReady, waitingForArtifact]);

  useEffect(() => {
    const gitSha = healthQ.data?.git_sha;
    if (healthQ.data?.serverless || !gitSha || provenance !== "precomputed") return;
    if (!canHydrateRunFromArtifact(selectedScenario, overrides, gitSha)) {
      setRunId(null);
      setEmbeddedGrids({});
      setRunAuditPayload(null);
      setProvenance("fresh");
      void handleRun();
    }
  }, [healthQ.data?.git_sha, healthQ.data?.serverless, provenance, selectedScenario, overrides, handleRun]);

  return {
    healthQ,
    scenariosQ,
    selectedScenario,
    setSelectedScenario,
    overrideLabel,
    setOverrideLabel,
    overrideValue,
    setOverrideValue,
    overrides,
    runId,
    embeddedGrids,
    runAuditPayload,
    provenance,
    running,
    error,
    setError,
    handleRun,
    waitingForArtifact,
    backgroundRunRef,
    artifactSha,
  };
}
