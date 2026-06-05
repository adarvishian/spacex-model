import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { ChangeHistoryList } from "../audit/ChangeHistoryList";
import { DependencyGraph } from "../audit/DependencyGraph";
import { DerivationPanel } from "../audit/DerivationPanel";
import { Grid, GridSkeleton, type GridHandle } from "../audit/Grid";
import { GridHelpPopover } from "../audit/GridHelpPopover";
import { GridToolbar } from "../audit/GridToolbar";
import { LabelSearchPalette, type LabelSearchHit } from "../audit/LabelSearchPalette";
import { RailEmptyState } from "../audit/RailEmptyState";
import { moveActiveCell } from "../audit/grid-navigation";
import { RunAuditTab } from "../audit/RunAuditTab";
import { ScenarioSidebar } from "../audit/ScenarioSidebar";
import { SheetTabs } from "../audit/SheetTabs";
import { SourcesPanel } from "../audit/SourcesPanel";
import { parseCellAddress, sheetSlugFromName } from "../shared/cell-ref";
import {
  canHydrateFromArtifact,
  getBaseCaseArtifact,
  loadBaseCaseArtifact,
  type RunProvenance,
} from "../shared/base-case-artifact";
import {
  cacheFromDeterministicRun,
  getCachedRun,
  setCachedRun,
} from "../shared/query-client";
import {
  fetchHealth,
  fetchLineage,
  fetchRunAuditDashboard,
  fetchScenarios,
  fetchSheetGrid,
  fetchSheets,
  runDeterministic,
} from "../api";
import { loadGridPrefs, saveGridPrefs, type GridPrefs } from "../shared/grid-prefs";
import type { ActiveCell, GridPayload, LineageEntry, RunAuditPayload } from "../shared/types";

const RUN_AUDIT_SLUG = "run_audit";

function buildOverrides(overrideLabel: string, overrideValue: string): Record<string, number> {
  const overrides: Record<string, number> = {};
  if (overrideValue.trim() && overrideLabel) {
    overrides[overrideLabel] = parseFloat(overrideValue);
  }
  return overrides;
}

export default function AuditApp() {
  const { sheetSlug = "starlink" } = useParams<{ sheetSlug: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const isRunAudit = sheetSlug === RUN_AUDIT_SLUG;

  const [artifactReady, setArtifactReady] = useState(Boolean(getBaseCaseArtifact()));
  const [selectedScenario, setSelectedScenario] = useState("base_case");
  const [overrideLabel, setOverrideLabel] = useState("");
  const [overrideValue, setOverrideValue] = useState("");
  const [runId, setRunId] = useState<string | null>(null);
  const [embeddedGrids, setEmbeddedGrids] = useState<Record<string, GridPayload>>({});
  const [runAuditPayload, setRunAuditPayload] = useState<RunAuditPayload | null>(null);
  const [provenance, setProvenance] = useState<RunProvenance>("fresh");
  const [activeCell, setActiveCell] = useState<ActiveCell | null>(null);
  const [lineage, setLineage] = useState<LineageEntry | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);
  const [derivationExpanded, setDerivationExpanded] = useState(false);
  const [labelSearchOpen, setLabelSearchOpen] = useState(false);
  const [gridPrefs, setGridPrefs] = useState<GridPrefs>(() => loadGridPrefs());
  const gridRef = useRef<GridHandle>(null);
  const backgroundRunRef = useRef(false);

  const healthQ = useQuery({ queryKey: ["health"], queryFn: fetchHealth });
  const scenariosQ = useQuery({ queryKey: ["scenarios"], queryFn: fetchScenarios });
  const sheetsQ = useQuery({ queryKey: ["sheets"], queryFn: fetchSheets });

  const overrides = useMemo(
    () => buildOverrides(overrideLabel, overrideValue),
    [overrideLabel, overrideValue],
  );

  useEffect(() => {
    let cancelled = false;
    void loadBaseCaseArtifact()
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

  const waitingForArtifact =
    selectedScenario === "base_case" &&
    Object.keys(overrides).length === 0 &&
    !artifactReady &&
    !getCachedRun(selectedScenario, overrides);

  const showRunProgress =
    (running || waitingForArtifact) && !gridData && !isRunAudit;
  const showGridSkeleton = (running || waitingForArtifact) && !gridData && !isRunAudit;

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

      if (!background) {
        setRunning(true);
      }
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
        if (Object.keys(grids).length > 0) {
          setEmbeddedGrids(grids);
        }
        if (audit) {
          setRunAuditPayload(audit);
        }

        cacheFromDeterministicRun(
          selectedScenario,
          overrides,
          { ...result, audit_grids: grids },
          audit ?? undefined,
        );

        if (!background) {
          setProvenance(result.cached ? "cached" : "fresh");
        }
      } catch (e) {
        if (!background) {
          setError(String(e));
        }
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
    const artifact = getBaseCaseArtifact();
    if (artifact && canHydrateFromArtifact(selectedScenario, overrides, gitSha)) {
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
      void handleRun({ background: true });
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
    if (!gitSha || provenance !== "precomputed") return;
    if (!canHydrateFromArtifact(selectedScenario, overrides, gitSha)) {
      setRunId(null);
      setEmbeddedGrids({});
      setRunAuditPayload(null);
      setProvenance("fresh");
      void handleRun();
    }
  }, [healthQ.data?.git_sha, provenance, selectedScenario, overrides, handleRun]);

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
      displayValue: row.year_values[yearIndex] ?? null,
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

  const onGridPrefsChange = useCallback((prefs: GridPrefs) => {
    setGridPrefs(prefs);
    saveGridPrefs(prefs);
  }, []);

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
          <span className={`run-provenance provenance-${provenance}`} data-testid="run-provenance">
            {provenance}
          </span>
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
            onRun={() => void handleRun()}
            loading={running && !backgroundRunRef.current}
          />
        </aside>

        <div className="audit-center">
          {isRunAudit ? (
            <RunAuditTab
              runId={runId}
              scenario={selectedScenario}
              auditPayload={runAuditPayload}
              loading={running && !runAuditPayload}
              onNavigateDivergence={({ sheetSlug: slug, rowId, year }) =>
                navigateToCell({ sheetSlug: slug, rowId, year })
              }
            />
          ) : (
            <div className="audit-grid-panel">
              <div className="grid-title-bar" data-testid="grid-title-bar">
                <div className="grid-title-left">
                  <strong>{activeSheetMeta?.display_name ?? sheetSlug}</strong>
                  {gridData && (
                    <span className="grid-dims">
                      {gridData.rows.length} rows × {gridData.years.length} year-columns
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
              {gridData && (
                <GridToolbar
                  prefs={gridPrefs}
                  onPrefsChange={onGridPrefsChange}
                  onFitColumns={() => gridRef.current?.fitColumns()}
                  onResetColumns={() => gridRef.current?.resetColumns()}
                />
              )}
              {showRunProgress && (
                <div className="audit-run-status" data-testid="audit-run-status">
                  <span className="skeleton-pulse" aria-hidden="true" />
                  {waitingForArtifact
                    ? "Loading base case…"
                    : `Running ${selectedScenario.replace("_", " ")} — solver converging, ~40 s on first run`}
                </div>
              )}
              {showGridSkeleton && <GridSkeleton />}
              {gridData && (
                <Grid
                  ref={gridRef}
                  payload={gridData}
                  activeCell={activeCell}
                  onCellSelect={openLineage}
                  numberFormat={gridPrefs.numberFormat}
                  density={gridPrefs.density}
                />
              )}
            </div>
          )}
        </div>

        {!isRunAudit && (
          <aside className="audit-detail-rail" aria-label="Cell detail panel">
            {!activeCell ? (
              <RailEmptyState />
            ) : (
              <>
                <DerivationPanel
                  entry={lineage}
                  activeCell={activeCell}
                  expanded={derivationExpanded}
                />
                <DependencyGraph
                  lineageKey={activeCell.lineageKey}
                  runId={runId}
                  year={activeCell.year}
                  sheet={gridData?.source_sheet}
                  row={activeCell.rowIndex}
                  scenario={selectedScenario}
                  onNavigateCell={({ sheetSlug: slug, rowId, year, lineageKey }) => {
                    navigateToCell({ sheetSlug: slug, rowId, year, lineageKey });
                  }}
                />
                <div className="sources-history-row">
                  <SourcesPanel entry={lineage} />
                  <ChangeHistoryList lineageKey={activeCell.lineageKey} />
                </div>
              </>
            )}
          </aside>
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
