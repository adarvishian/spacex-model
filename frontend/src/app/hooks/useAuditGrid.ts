import { useQuery } from "@tanstack/react-query";
import { useMemo } from "react";
import { fetchSheetGrid, fetchSheets } from "../../api";
import type { GridPayload } from "../../shared/types";

type Params = {
  sheetSlug: string;
  isRunAudit: boolean;
  runId: string | null;
  selectedScenario: string;
  embeddedGrids: Record<string, GridPayload>;
  running: boolean;
  waitingForArtifact: boolean;
};

export function useAuditGrid({
  sheetSlug,
  isRunAudit,
  runId,
  selectedScenario,
  embeddedGrids,
  running,
  waitingForArtifact,
}: Params) {
  const sheetsQ = useQuery({ queryKey: ["sheets"], queryFn: fetchSheets });

  const gridQ = useQuery({
    queryKey: ["grid", runId, sheetSlug, selectedScenario],
    queryFn: () => fetchSheetGrid(runId!, sheetSlug, selectedScenario),
    enabled: Boolean(runId) && !isRunAudit && !embeddedGrids[sheetSlug],
  });

  const gridData = isRunAudit
    ? null
    : running && !embeddedGrids[sheetSlug]
      ? null
      : embeddedGrids[sheetSlug] ?? gridQ.data ?? null;

  const showRunProgress = (running || waitingForArtifact) && !gridData && !isRunAudit;
  const showGridSkeleton = (running || waitingForArtifact) && !gridData && !isRunAudit;

  const activeSheetMeta = useMemo(
    () => sheetsQ.data?.find((s) => s.slug === sheetSlug),
    [sheetsQ.data, sheetSlug],
  );

  return {
    sheetsQ,
    gridData,
    showRunProgress,
    showGridSkeleton,
    activeSheetMeta,
  };
}
