import { useEffect, useMemo, useRef, useState } from "react";
import type { GridPayload, SheetMeta } from "../shared/types";

export type LabelSearchHit = {
  sheetSlug: string;
  sheetName: string;
  rowId: string;
  label: string;
  year: number;
  lineageKey: string;
};

type Props = {
  open: boolean;
  onClose: () => void;
  sheets: SheetMeta[];
  activeSheetSlug: string;
  gridPayload: GridPayload | null;
  gridCache: Record<string, GridPayload>;
  onSelect: (hit: LabelSearchHit) => void;
};

function hitsFromGrid(
  slug: string,
  sheetName: string,
  payload: GridPayload,
  query: string,
): LabelSearchHit[] {
  const q = query.trim().toLowerCase();
  if (!q) return [];
  const out: LabelSearchHit[] = [];
  for (const row of payload.rows) {
    if (row.is_header) continue;
    if (!row.label.toLowerCase().includes(q) && !row.row_id.toLowerCase().includes(q)) {
      continue;
    }
    const year = payload.years[0];
    const idx = 0;
    out.push({
      sheetSlug: slug,
      sheetName,
      rowId: row.row_id,
      label: row.label,
      year,
      lineageKey: row.lineage_keys[idx],
    });
    if (out.length >= 40) break;
  }
  return out;
}

export function LabelSearchPalette({
  open,
  onClose,
  sheets,
  activeSheetSlug,
  gridPayload,
  gridCache,
  onSelect,
}: Props) {
  const [query, setQuery] = useState("");
  const [highlight, setHighlight] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const results = useMemo(() => {
    const q = query.trim();
    if (!q) return [];

    const merged: LabelSearchHit[] = [];
    const seen = new Set<string>();

    const addPayload = (slug: string, payload: GridPayload) => {
      const meta = sheets.find((s) => s.slug === slug);
      const name = meta?.display_name ?? payload.source_sheet;
      for (const hit of hitsFromGrid(slug, name, payload, q)) {
        const key = `${hit.sheetSlug}:${hit.rowId}`;
        if (seen.has(key)) continue;
        seen.add(key);
        merged.push(hit);
      }
    };

    if (gridPayload) addPayload(activeSheetSlug, gridPayload);
    for (const [slug, payload] of Object.entries(gridCache)) {
      if (slug === activeSheetSlug) continue;
      addPayload(slug, payload);
    }

    return merged.slice(0, 25);
  }, [query, gridPayload, gridCache, activeSheetSlug, sheets]);

  useEffect(() => {
    if (open) {
      setQuery("");
      setHighlight(0);
      requestAnimationFrame(() => inputRef.current?.focus());
    }
  }, [open]);

  useEffect(() => {
    setHighlight(0);
  }, [query]);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        onClose();
      }
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setHighlight((h) => Math.min(h + 1, Math.max(0, results.length - 1)));
      }
      if (e.key === "ArrowUp") {
        e.preventDefault();
        setHighlight((h) => Math.max(h - 1, 0));
      }
      if (e.key === "Enter" && results[highlight]) {
        e.preventDefault();
        onSelect(results[highlight]);
        onClose();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, results, highlight, onClose, onSelect]);

  if (!open) return null;

  return (
    <div
      className="label-search-overlay"
      role="dialog"
      aria-modal="true"
      aria-label="Search labels across sheets"
      onClick={onClose}
    >
      <div className="label-search-panel" onClick={(e) => e.stopPropagation()}>
        <input
          ref={inputRef}
          type="search"
          className="label-search-input"
          placeholder="Search row labels (Cmd+K)…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          aria-label="Label search query"
          data-testid="label-search-input"
        />
        <ul className="label-search-results" role="listbox">
          {results.length === 0 && query && (
            <li className="label-search-empty muted">No matching labels in loaded sheets.</li>
          )}
          {results.map((hit, i) => (
            <li key={`${hit.sheetSlug}-${hit.rowId}`}>
              <button
                type="button"
                role="option"
                aria-selected={i === highlight}
                className={i === highlight ? "active" : ""}
                onMouseEnter={() => setHighlight(i)}
                onClick={() => {
                  onSelect(hit);
                  onClose();
                }}
              >
                <span className="label-search-sheet">{hit.sheetName}</span>
                <span className="label-search-row">{hit.rowId}</span>
                <span className="label-search-label">{hit.label}</span>
              </button>
            </li>
          ))}
        </ul>
        <p className="label-search-hint muted">
          ↑↓ navigate · Enter open · Esc close · Searches current sheet and cached tabs
        </p>
      </div>
    </div>
  );
}
