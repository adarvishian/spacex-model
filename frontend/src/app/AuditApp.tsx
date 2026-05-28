import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ChangeHistoryList } from "../audit/ChangeHistoryList";
import { DependencyGraph } from "../audit/DependencyGraph";
import { DerivationPanel } from "../audit/DerivationPanel";
import { Grid, type GridHandle } from "../audit/Grid";
import { LabelSearchPalette, type LabelSearchHit } from "../audit/LabelSearchPalette";
import { moveActiveCell } from "../audit/grid-navigation";
import { Minimap } from "../audit/Minimap";
import { RunAuditTab } from "../audit/RunAuditTab";
import { ScenarioSidebar } from "../audit/ScenarioSidebar";
import { SheetTabs } from "../audit/SheetTabs";
import { SourcesPanel } from "../audit/SourcesPanel";
import { parseCellAddress, sheetSlugFromName } from "../shared/cell-ref";
import {
  fetchHealth,
  fetchLineage,
  fetchScenarios,
  fetchSheetGrid,
  fetchSheets,
  runDeterministic,
} from "../api";
import type { ActiveCell, GridPayload, LineageEntry } from "../shared/types";

const RUN_AUDIT_SLUG = "run_audit";

export default function AuditApp() {
  const { sheetSlug = "starlink" } = useParams<{ sheetSlug: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const isRunAudit = sheetSlug === RUN_AUDIT_SLUG;

  const [selectedScenario, setSelectedScenario] = useState("base_case");
  const [overrideLabel, setOverrideLabel] = useState("");
  const [overrideValue, setOverrideValue] = useState("");
  const [runId, setRunId] = useState<string | null>(null);
  const [embeddedGrids, setEmbeddedGrids] = useState<Record<string, GridPayload>>({});
  const [activeCell, setActiveCell] = useState<ActiveCell | null>(null);
  const [lineage, setLineage] = useState<LineageEntry | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [derivationExpanded, setDerivationExpanded] = useState(false);
  const [labelSearchOpen, setLabelSearchOpen] = useState(false);
  const gridRef = useRef<GridHandle>(null);

  const healthQ = useQuery({ queryKey: ["health"], queryFn: fetchHealth });
  const scenariosQ = useQuery({ queryKey: ["scenarios"], queryFn: fetchScenarios });
  const sheetsQ = useQuery({ queryKey: ["sheets"], queryFn: fetchSheets });

  const gridQ = useQuery({
    queryKey: ["grid", runId, sheetSlug, selectedScenario],
    queryFn: () => fetchSheetGrid(runId!, sheetSlug, selectedScenario),
    enabled: Boolean(runId) && !isRunAudit && !embeddedGrids[sheetSlug],
  });

  const gridData = isRunAudit
    ? null
    : embeddedGrids[sheetSlug] ?? gridQ.data ?? null;

  const handleRun = useCallback(async () => {
    setRunning(true);
    setError(null);
    try {
      const overrides: Record<string, number> = {};
      if (overrideValue.trim() && overrideLabel) {
        overrides[overrideLabel] = parseFloat(overrideValue);
      }
      const result = await runDeterministic({
        scenario: selectedScenario,
        overrides,
        use_cache: true,
      });
      setRunId(result.run_id);
      if (result.audit_grids) {
        setEmbeddedGrids(result.audit_grids);
      }
    } catch (e) {
      setError(String(e));
    } finally {
      setRunning(false);
    }
  }, [overrideLabel, overrideValue, selectedScenario]);

  useEffect(() => {
    if (!runId && !running) {
      void handleRun();
    }
  }, [runId, running, handleRun]);

  const openLineage = useCallback(
    async (cell: ActiveCell) => {
      if (!runId) return;
      const params = new URLSearchParams(searchParams);
      params.set("row", cell.rowId);
      params.set("col", String(cell.year));
      setSearchParams(params, { replace: true });
      setActiveCell(cell);
      try {
        const entry = await fetchLineage(cell.lineageKey, {
          runId,
          year: cell.year,
          sheet: gridData?.source_sheet,
          row: cell.rowIndex,
          scenario: selectedScenario,
        });
        setLineage(entry);
      } catch (e) {
        setError(String(e));
      }
    },
    [runId, searchParams, setSearchParams, gridData?.source_sheet, selectedScenario],
  );

  const navigateToCell = useCallback(
    (opts: { sheetSlug: string; rowId?: string; year?: number; lineageKey?: string }) => {
      const params = new URLSearchParams();
      if (opts.rowId) params.set("row", opts.rowId);
      if (opts.year != null) params.set("col", String(opts.year));
      const qs = params.toString();
      navigate(`/audit/${opts.sheetSlug}${qs ? `?${qs}` : ""}`);
      setLineage(null);
      setActiveCell(null);
    },
    [navigate],
  );

  const urlRow = searchParams.get("row");
  const urlCol = searchParams.get("col");

  useEffect(() => {
    if (!gridData || !urlRow || !urlCol || isRunAudit) return;
    const year = parseInt(urlCol, 10);
    const row = gridData.rows.find((r) => r.row_id === urlRow);
    if (!row || row.is_header) return;
    const yearIndex = gridData.years.indexOf(year);
    if (yearIndex < 0) return;
    const cell: ActiveCell = {
      rowId: row.row_id,
      rowIndex: row.row_index,
      label: row.label,
      year,
      yearIndex,
      lineageKey: row.lineage_keys[yearIndex],
      unit: row.unit,
      cellKind: row.cell_kinds[yearIndex],
    };
    void openLineage(cell);
  }, [gridData, urlRow, urlCol, openLineage, isRunAudit, sheetSlug]);

  const activeSheetMeta = useMemo(
    () => sheetsQ.data?.find((s) => s.slug === sheetSlug),
    [sheetsQ.data, sheetSlug],
  );

  const onSheetChange = (slug: string) => {
    navigate(`/audit/${slug}${searchParams.toString() ? `?${searchParams.toString()}` : ""}`);
  };

  const jumpToUpstream = useCallback(() => {
    const first = lineage?.resolved_inputs?.[0];
    if (!first?.cell_address) return;
    const parsed = parseCellAddress(first.cell_address);
    if (!parsed?.rowId) return;
    navigateToCell({
      sheetSlug: sheetSlugFromName(parsed.sheetName),
      rowId: parsed.rowId,
      year: parsed.year ?? activeCell?.year,
      lineageKey: first.lineage_key,
    });
  }, [lineage, activeCell, navigateToCell]);

  const onLabelSearchSelect = useCallback(
    (hit: LabelSearchHit) => {
      navigateToCell({
        sheetSlug: hit.sheetSlug,
        rowId: hit.rowId,
        year: hit.year,
        lineageKey: hit.lineageKey,
      });
    },
    [navigateToCell],
  );

  useEffect(() => {
    if (isRunAudit || !gridData) return;

    const onKeyDown = (e: KeyboardEvent) => {
      const mod = e.metaKey || e.ctrlKey;
      if (mod && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setLabelSearchOpen(true);
        return;
      }
      if (mod && e.key.toLowerCase() === "j") {
        e.preventDefault();
        jumpToUpstream();
        return;
      }

      const tag = (e.target as HTMLElement)?.tagName;
      if (tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT") return;

      if (e.key === "Enter" && activeCell) {
        e.preventDefault();
        setDerivationExpanded((v) => !v);
        return;
      }

      if (!activeCell) return;
      const dir =
        e.key === "ArrowUp"
          ? "up"
          : e.key === "ArrowDown"
            ? "down"
            : e.key === "ArrowLeft"
              ? "left"
              : e.key === "ArrowRight"
                ? "right"
                : null;
      if (!dir) return;
      e.preventDefault();
      const next = moveActiveCell(gridData, activeCell, dir);
      if (next) {
        void openLineage(next);
        gridRef.current?.focusActiveCell(next);
      }
    };

    window.addEventListener("keydown", onKeyDown, true);
    return () => window.removeEventListener("keydown", onKeyDown, true);
  }, [isRunAudit, gridData, activeCell, openLineage, jumpToUpstream]);

  useEffect(() => {
    if (activeCell) {
      gridRef.current?.focusActiveCell(activeCell);
    }
  }, [activeCell, sheetSlug]);

  return (
    <div className="audit-app">
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
          {healthQ.data?.git_sha && (
            <span>
              build: <code>{healthQ.data.git_sha}</code>
            </span>
          )}
          <Link to="/client" className="mode-switch">
            Switch to Client Mode →
          </Link>
        </div>
      </header>

      {error && <div className="audit-alert error">{error}</div>}

      <div className="audit-body">
        <aside className="audit-tabs-col">
          <SheetTabs
            sheets={sheetsQ.data ?? []}
            activeSlug={sheetSlug}
            onSelect={onSheetChange}
          />
          <ScenarioSidebar
            scenarios={scenariosQ.data ?? []}
            selected={selectedScenario}
            onSelect={setSelectedScenario}
            overrideLabel={overrideLabel}
            overrideValue={overrideValue}
            onOverrideLabel={setOverrideLabel}
            onOverrideValue={setOverrideValue}
            onRun={handleRun}
            loading={running}
          />
        </aside>

        <div className="audit-center">
          {isRunAudit ? (
            <RunAuditTab
              runId={runId}
              scenario={selectedScenario}
              onNavigateDivergence={({ sheetSlug: slug, rowId, year }) =>
                navigateToCell({ sheetSlug: slug, rowId, year })
              }
            />
          ) : (
            <>
              <div className="audit-grid-panel">
                <div className="grid-title-bar">
                  <span>
                    <strong>{activeSheetMeta?.display_name ?? sheetSlug}</strong>
                    {gridData && (
                      <>
                        {" "}
                        · {gridData.rows.length} rows × {gridData.years.length} year-columns
                      </>
                    )}
                  </span>
                  <div className="grid-legend">
                    <span className="grid-shortcuts-hint" aria-label="Keyboard shortcuts">
                      ↑↓←→ cell · Enter expand · ⌘J upstream · ⌘K search
                    </span>
                    <span>
                      <i className="sw input" /> Input
                    </span>
                    <span>
                      <i className="sw derived" /> Derived
                    </span>
                    <span>
                      <i className="sw divergence" /> Divergence
                    </span>
                  </div>
                </div>
                {gridQ.isLoading && !gridData && (
                  <p className="audit-loading">Loading grid…</p>
                )}
                {gridData && (
                  <Grid
                    ref={gridRef}
                    payload={gridData}
                    activeCell={activeCell}
                    onCellSelect={openLineage}
                  />
                )}
              </div>
              <DerivationPanel
                entry={lineage}
                activeCell={activeCell}
                expanded={derivationExpanded}
              />
              <DependencyGraph
                lineageKey={activeCell?.lineageKey ?? null}
                runId={runId}
                year={activeCell?.year}
                sheet={gridData?.source_sheet}
                row={activeCell?.rowIndex}
                scenario={selectedScenario}
                onNavigateCell={({ sheetSlug: slug, rowId, year, lineageKey }) => {
                  navigateToCell({ sheetSlug: slug, rowId, year, lineageKey });
                }}
              />
              <div className="sources-history-row">
                <SourcesPanel entry={lineage} />
                <ChangeHistoryList lineageKey={activeCell?.lineageKey ?? null} />
              </div>
            </>
          )}
        </div>

        {!isRunAudit && (
          <Minimap
            activeSheetSlug={sheetSlug}
            lineage={lineage}
            activeCell={activeCell}
            onNavigateSheet={onSheetChange}
            onNavigateCell={(n) => {
              const slug = sheetSlugFromName(n.label.split("!")[0]);
              navigateToCell({ sheetSlug: slug, lineageKey: n.key });
            }}
          />
        )}
      </div>

      <LabelSearchPalette
        open={labelSearchOpen}
        onClose={() => setLabelSearchOpen(false)}
        sheets={sheetsQ.data ?? []}
        activeSheetSlug={sheetSlug}
        gridPayload={gridData}
        gridCache={embeddedGrids}
        onSelect={onLabelSearchSelect}
      />
    </div>
  );
}
