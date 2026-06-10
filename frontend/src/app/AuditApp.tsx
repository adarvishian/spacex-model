import { useState } from "react";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";
import { Grid, GridSkeleton } from "../audit/Grid";
import { GridHelpPopover } from "../audit/GridHelpPopover";
import { GridToolbar } from "../audit/GridToolbar";
import { LabelSearchPalette } from "../audit/LabelSearchPalette";
import { RunAuditTab } from "../audit/RunAuditTab";
import { ScenarioSidebar } from "../audit/ScenarioSidebar";
import { SheetTabs } from "../audit/SheetTabs";
import { AuditAppHeader } from "./AuditAppHeader";
import { AuditDetailRail } from "./AuditDetailRail";
import { useAuditGrid } from "./hooks/useAuditGrid";
import { useAuditRun } from "./hooks/useAuditRun";
import { useDerivationPanel } from "./hooks/useDerivationPanel";
import { useGridState } from "./hooks/useGridState";

const RUN_AUDIT_SLUG = "run_audit";

export default function AuditApp() {
  const { sheetSlug = "starlink" } = useParams<{ sheetSlug: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  const isRunAudit = sheetSlug === RUN_AUDIT_SLUG;

  const run = useAuditRun();
  const gridView = useAuditGrid({
    sheetSlug,
    isRunAudit,
    runId: run.runId,
    selectedScenario: run.selectedScenario,
    embeddedGrids: run.embeddedGrids,
    running: run.running,
    waitingForArtifact: run.waitingForArtifact,
  });

  const [labelSearchOpen, setLabelSearchOpen] = useState(false);

  const derivation = useDerivationPanel({
    runId: run.runId,
    selectedScenario: run.selectedScenario,
    gridData: gridView.gridData,
    searchParams,
    setSearchParams,
    navigate,
    setError: run.setError,
    isRunAudit,
  });

  const grid = useGridState({
    sheetSlug,
    isRunAudit,
    gridData: gridView.gridData,
    activeCell: derivation.activeCell,
    openLineage: derivation.openLineage,
    jumpToUpstream: derivation.jumpToUpstream,
    setLabelSearchOpen,
    setDerivationExpanded: derivation.setDerivationExpanded,
  });

  const onSheetChange = (slug: string) => {
    navigate(`/audit/${slug}${searchParams.toString() ? `?${searchParams.toString()}` : ""}`);
  };

  return (
    <div className="audit-app">
      <AuditAppHeader
        selectedScenario={run.selectedScenario}
        runId={run.runId}
        provenance={run.provenance}
        workbookName={run.healthQ.data?.workbook_name}
        workbookMtime={run.healthQ.data?.workbook_mtime}
        artifactSha={run.artifactSha}
        apiGitSha={run.healthQ.data?.git_sha}
      />

      {run.error && <div className="audit-alert error">{run.error}</div>}

      <div className="audit-body">
        <aside className="audit-tabs-col">
          <SheetTabs
            sheets={gridView.sheetsQ.data ?? []}
            activeSlug={sheetSlug}
            onSelect={onSheetChange}
          />
          <ScenarioSidebar
            scenarios={run.scenariosQ.data ?? []}
            selected={run.selectedScenario}
            onSelect={run.setSelectedScenario}
            overrideLabel={run.overrideLabel}
            overrideValue={run.overrideValue}
            onOverrideLabel={run.setOverrideLabel}
            onOverrideValue={run.setOverrideValue}
            onRun={() => void run.handleRun()}
            loading={run.running && !run.backgroundRunRef.current}
          />
        </aside>

        <div className="audit-center">
          {isRunAudit ? (
            <RunAuditTab
              runId={run.runId}
              scenario={run.selectedScenario}
              auditPayload={run.runAuditPayload}
              loading={run.running && !run.runAuditPayload}
              onNavigateDivergence={({ sheetSlug: slug, rowId, year }) =>
                derivation.navigateToCell({ sheetSlug: slug, rowId, year })
              }
            />
          ) : (
            <div className="audit-grid-panel">
              <div className="grid-title-bar" data-testid="grid-title-bar">
                <div className="grid-title-left">
                  <strong>{gridView.activeSheetMeta?.display_name ?? sheetSlug}</strong>
                  {gridView.gridData && (
                    <span className="grid-dims">
                      {gridView.gridData.rows.length} rows × {gridView.gridData.years.length}{" "}
                      year-columns
                    </span>
                  )}
                </div>
                <div className="grid-title-right">
                  <div className="grid-legend" id="grid-cell-legend" aria-label="Cell type legend">
                    <span>
                      <i className="sw input" aria-hidden="true" />
                      <span className="legend-glyph" aria-hidden="true">
                        I
                      </span>{" "}
                      Input
                    </span>
                    <span>
                      <i className="sw derived" aria-hidden="true" />
                      <span className="legend-glyph" aria-hidden="true">
                        D
                      </span>{" "}
                      Derived
                    </span>
                    <span>
                      <i className="sw divergence" aria-hidden="true" />
                      <span className="legend-glyph" aria-hidden="true">
                        ▲
                      </span>{" "}
                      Divergence
                    </span>
                  </div>
                  <GridHelpPopover />
                </div>
              </div>
              {gridView.gridData && (
                <GridToolbar
                  prefs={grid.gridPrefs}
                  onPrefsChange={grid.onGridPrefsChange}
                  onFitColumns={() => grid.gridRef.current?.fitColumns()}
                  onResetColumns={() => grid.gridRef.current?.resetColumns()}
                />
              )}
              {gridView.showRunProgress && (
                <div className="audit-run-status" data-testid="audit-run-status">
                  <span className="skeleton-pulse" aria-hidden="true" />
                  {run.waitingForArtifact
                    ? "Loading base case…"
                    : `Running ${run.selectedScenario.replace("_", " ")} — solver converging, ~40 s on first run`}
                </div>
              )}
              {gridView.showGridSkeleton && <GridSkeleton />}
              {gridView.gridData && (
                <Grid
                  ref={grid.gridRef}
                  payload={gridView.gridData}
                  activeCell={derivation.activeCell}
                  onCellSelect={derivation.openLineage}
                  numberFormat={grid.gridPrefs.numberFormat}
                  density={grid.gridPrefs.density}
                />
              )}
            </div>
          )}
        </div>

        {!isRunAudit && (
          <aside className="audit-detail-rail" aria-label="Cell detail panel">
            <AuditDetailRail
              activeCell={derivation.activeCell}
              lineage={derivation.lineage}
              derivationExpanded={derivation.derivationExpanded}
              railView={derivation.railView}
              setRailView={derivation.setRailView}
              mcOutputKind={derivation.mcOutputKind}
              selectedScenario={run.selectedScenario}
              overrides={run.overrides}
              runId={run.runId}
              gridData={gridView.gridData}
              onNavigateCell={derivation.navigateToCell}
            />
          </aside>
        )}
      </div>

      <LabelSearchPalette
        open={labelSearchOpen}
        onClose={() => setLabelSearchOpen(false)}
        sheets={gridView.sheetsQ.data ?? []}
        activeSheetSlug={sheetSlug}
        gridPayload={gridView.gridData}
        gridCache={run.embeddedGrids}
        onSelect={derivation.onLabelSearchSelect}
      />
    </div>
  );
}
