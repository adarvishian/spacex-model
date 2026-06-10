import { useCallback, useEffect, useMemo, useState } from "react";
import type { NavigateFunction } from "react-router-dom";
import type { SetURLSearchParams } from "react-router-dom";
import { fetchLineage } from "../../api";
import type { LabelSearchHit } from "../../audit/LabelSearchPalette";
import { parseCellAddress, sheetSlugFromName } from "../../shared/cell-ref";
import { resolveMcOutputKind } from "../../shared/mc-headline";
import type { ActiveCell, GridPayload, LineageEntry } from "../../shared/types";

type RailView = "derivation" | "mc";

type Params = {
  runId: string | null;
  selectedScenario: string;
  gridData: GridPayload | null | undefined;
  searchParams: URLSearchParams;
  setSearchParams: SetURLSearchParams;
  navigate: NavigateFunction;
  setError: (msg: string | null) => void;
  isRunAudit: boolean;
};

export function useDerivationPanel({
  runId,
  selectedScenario,
  gridData,
  searchParams,
  setSearchParams,
  navigate,
  setError,
  isRunAudit,
}: Params) {
  const [activeCell, setActiveCell] = useState<ActiveCell | null>(null);
  const [lineage, setLineage] = useState<LineageEntry | null>(null);
  const [derivationExpanded, setDerivationExpanded] = useState(false);
  const [railView, setRailView] = useState<RailView>("derivation");

  const urlRow = searchParams.get("row");
  const urlCol = searchParams.get("col");
  const urlMc = searchParams.get("mc");

  const mcOutputKind = useMemo(() => {
    if (!activeCell) return null;
    return resolveMcOutputKind(activeCell.lineageKey, activeCell.label);
  }, [activeCell]);

  const openLineage = useCallback(
    async (cell: ActiveCell) => {
      if (!runId) return;
      const params = new URLSearchParams(searchParams);
      params.set("row", cell.rowId);
      params.set("col", String(cell.year));
      setSearchParams(params, { replace: true });
      setActiveCell(cell);
      setRailView("derivation");
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
    [runId, searchParams, setSearchParams, gridData?.source_sheet, selectedScenario, setError],
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
    if (urlMc && activeCell && mcOutputKind) setRailView("mc");
  }, [urlMc, activeCell, mcOutputKind]);

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
  }, [gridData, urlRow, urlCol, openLineage, isRunAudit]);

  return {
    activeCell,
    lineage,
    derivationExpanded,
    setDerivationExpanded,
    railView,
    setRailView,
    mcOutputKind,
    openLineage,
    navigateToCell,
    jumpToUpstream,
    onLabelSearchSelect,
  };
}
