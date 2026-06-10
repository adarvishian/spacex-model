import { useCallback, useEffect, useRef, useState } from "react";
import { moveActiveCell } from "../../audit/grid-navigation";
import type { GridHandle } from "../../audit/Grid";
import { loadGridPrefs, saveGridPrefs, type GridPrefs } from "../../shared/grid-prefs";
import type { ActiveCell, GridPayload } from "../../shared/types";

type Params = {
  sheetSlug: string;
  isRunAudit: boolean;
  gridData: GridPayload | null;
  activeCell: ActiveCell | null;
  openLineage: (cell: ActiveCell) => void;
  jumpToUpstream: () => void;
  setLabelSearchOpen: (open: boolean) => void;
  setDerivationExpanded: React.Dispatch<React.SetStateAction<boolean>>;
};

export function useGridState({
  sheetSlug,
  isRunAudit,
  gridData,
  activeCell,
  openLineage,
  jumpToUpstream,
  setLabelSearchOpen,
  setDerivationExpanded,
}: Params) {
  const [gridPrefs, setGridPrefs] = useState<GridPrefs>(() => loadGridPrefs());
  const gridRef = useRef<GridHandle>(null);

  const onGridPrefsChange = useCallback((prefs: GridPrefs) => {
    setGridPrefs(prefs);
    saveGridPrefs(prefs);
  }, []);

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
  }, [
    isRunAudit,
    gridData,
    activeCell,
    openLineage,
    jumpToUpstream,
    setLabelSearchOpen,
    setDerivationExpanded,
  ]);

  useEffect(() => {
    if (activeCell) gridRef.current?.focusActiveCell(activeCell);
  }, [activeCell, sheetSlug]);

  return { gridRef, gridPrefs, onGridPrefsChange };
}
