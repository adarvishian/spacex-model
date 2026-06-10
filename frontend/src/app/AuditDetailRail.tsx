import { ChangeHistoryList } from "../audit/ChangeHistoryList";
import { DependencyGraph } from "../audit/DependencyGraph";
import { DerivationPanel } from "../audit/DerivationPanel";
import { McAuditPanel } from "../audit/McAuditPanel";
import { RailEmptyState } from "../audit/RailEmptyState";
import { SourcesPanel } from "../audit/SourcesPanel";
import type { McOutputKind } from "../shared/mc-headline";
import type { ActiveCell, GridPayload, LineageEntry } from "../shared/types";

type RailView = "derivation" | "mc";

type Props = {
  activeCell: ActiveCell | null;
  lineage: LineageEntry | null;
  derivationExpanded: boolean;
  railView: RailView;
  setRailView: (view: RailView) => void;
  mcOutputKind: McOutputKind | null;
  selectedScenario: string;
  overrides: Record<string, number>;
  runId: string | null;
  gridData: GridPayload | null;
  onNavigateCell: (opts: {
    sheetSlug: string;
    rowId?: string;
    year?: number;
    lineageKey?: string;
  }) => void;
};

export function AuditDetailRail({
  activeCell,
  lineage,
  derivationExpanded,
  railView,
  setRailView,
  mcOutputKind,
  selectedScenario,
  overrides,
  runId,
  gridData,
  onNavigateCell,
}: Props) {
  if (!activeCell) return <RailEmptyState />;

  return (
    <>
      {mcOutputKind && (
        <div className="rail-view-toggle" data-testid="rail-view-toggle">
          <button
            type="button"
            className={railView === "derivation" ? "active" : ""}
            aria-pressed={railView === "derivation"}
            onClick={() => setRailView("derivation")}
            data-testid="rail-view-derivation"
          >
            Derivation
          </button>
          <button
            type="button"
            className={railView === "mc" ? "active" : ""}
            aria-pressed={railView === "mc"}
            onClick={() => setRailView("mc")}
            data-testid="rail-view-mc"
          >
            Distribution
          </button>
        </div>
      )}
      {railView === "mc" && mcOutputKind ? (
        <McAuditPanel
          outputKind={mcOutputKind}
          label={activeCell.label}
          year={activeCell.year}
          scenario={selectedScenario}
          overrides={overrides}
        />
      ) : (
        <>
          <DerivationPanel entry={lineage} activeCell={activeCell} expanded={derivationExpanded} />
          <DependencyGraph
            lineageKey={activeCell.lineageKey}
            runId={runId}
            year={activeCell.year}
            sheet={gridData?.source_sheet}
            row={activeCell.rowIndex}
            scenario={selectedScenario}
            onNavigateCell={onNavigateCell}
          />
          <div className="sources-history-row">
            <SourcesPanel entry={lineage} />
            <ChangeHistoryList lineageKey={activeCell.lineageKey} year={activeCell.year} />
          </div>
        </>
      )}
    </>
  );
}
