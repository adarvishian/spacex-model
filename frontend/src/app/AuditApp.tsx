import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { DerivationPanel } from "../audit/DerivationPanel";
import { Grid } from "../audit/Grid";
import { Minimap } from "../audit/Minimap";
import { ScenarioSidebar } from "../audit/ScenarioSidebar";
import { SheetTabs } from "../audit/SheetTabs";
import {
  fetchHealth,
  fetchLineage,
  fetchScenarios,
  fetchSheetGrid,
  fetchSheets,
  runDeterministic,
} from "../api";
import type { ActiveCell, GridPayload, LineageEntry } from "../shared/types";

const ENABLED_SHEETS = new Set(["starlink"]);

export default function AuditApp() {
  const { sheetSlug = "starlink" } = useParams<{ sheetSlug: string }>();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  const [selectedScenario, setSelectedScenario] = useState("base_case");
  const [overrideLabel, setOverrideLabel] = useState("");
  const [overrideValue, setOverrideValue] = useState("");
  const [runId, setRunId] = useState<string | null>(null);
  const [embeddedGrid, setEmbeddedGrid] = useState<GridPayload | null>(null);
  const [activeCell, setActiveCell] = useState<ActiveCell | null>(null);
  const [lineage, setLineage] = useState<LineageEntry | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);

  const healthQ = useQuery({ queryKey: ["health"], queryFn: fetchHealth });
  const scenariosQ = useQuery({ queryKey: ["scenarios"], queryFn: fetchScenarios });
  const sheetsQ = useQuery({ queryKey: ["sheets"], queryFn: fetchSheets });

  const gridQ = useQuery({
    queryKey: ["grid", runId, sheetSlug, selectedScenario],
    queryFn: () => fetchSheetGrid(runId!, sheetSlug, selectedScenario),
    enabled: Boolean(runId) && ENABLED_SHEETS.has(sheetSlug) && !embeddedGrid,
  });

  const gridData =
    embeddedGrid && sheetSlug === embeddedGrid.sheet ? embeddedGrid : gridQ.data ?? null;

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
      setEmbeddedGrid(result.audit_grids?.starlink ?? null);
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
      setActiveCell(cell);
      const params = new URLSearchParams(searchParams);
      params.set("row", cell.rowId);
      params.set("col", String(cell.year));
      setSearchParams(params, { replace: true });
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

  const urlRow = searchParams.get("row");
  const urlCol = searchParams.get("col");

  useEffect(() => {
    if (!gridData || !urlRow || !urlCol) return;
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
    if (
      activeCell?.rowId === cell.rowId &&
      activeCell?.year === cell.year &&
      lineage
    ) {
      return;
    }
    void openLineage(cell);
  }, [gridData, urlRow, urlCol, openLineage, activeCell, lineage]);

  const activeSheetMeta = useMemo(
    () => sheetsQ.data?.find((s) => s.slug === sheetSlug),
    [sheetsQ.data, sheetSlug],
  );

  const onSheetChange = (slug: string) => {
    if (!ENABLED_SHEETS.has(slug)) return;
    navigate(`/audit/${slug}${searchParams.toString() ? `?${searchParams.toString()}` : ""}`);
  };

  const sheetDisabled = !ENABLED_SHEETS.has(sheetSlug);

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
            enabledSlugs={ENABLED_SHEETS}
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
          {sheetDisabled ? (
            <div className="audit-placeholder">
              <p>
                <strong>{activeSheetMeta?.display_name ?? sheetSlug}</strong> ships in Phase 2.
              </p>
              <button type="button" onClick={() => navigate("/audit/starlink")}>
                Open Starlink sheet
              </button>
            </div>
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
                {gridQ.isLoading && !gridData && <p className="audit-loading">Loading grid…</p>}
                {gridData && (
                  <Grid
                    payload={gridData}
                    activeCell={activeCell}
                    onCellSelect={openLineage}
                  />
                )}
              </div>
              <DerivationPanel entry={lineage} activeCell={activeCell} />
            </>
          )}
        </div>

        <Minimap
          activeSheetSlug={sheetSlug}
          lineage={lineage}
          activeCell={activeCell}
          onNavigateSheet={onSheetChange}
        />
      </div>
    </div>
  );
}
