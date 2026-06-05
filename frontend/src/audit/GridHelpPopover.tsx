import { useEffect, useId, useRef, useState } from "react";

const SHORTCUTS = [
  { keys: "↑ ↓ ← →", action: "Move active cell" },
  { keys: "Enter", action: "Expand / collapse derivation" },
  { keys: "⌘ J", action: "Jump to upstream input" },
  { keys: "⌘ K", action: "Search row labels" },
];

export function GridHelpPopover() {
  const [open, setOpen] = useState(false);
  const wrapRef = useRef<HTMLDivElement>(null);
  const popoverId = useId();

  useEffect(() => {
    if (!open) return;
    const onPointerDown = (e: MouseEvent) => {
      if (!wrapRef.current?.contains(e.target as Node)) {
        setOpen(false);
      }
    };
    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("mousedown", onPointerDown);
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("mousedown", onPointerDown);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [open]);

  return (
    <div className="grid-help-wrap" ref={wrapRef}>
      <button
        type="button"
        className="grid-help-btn"
        aria-label="Keyboard shortcuts help"
        aria-expanded={open}
        aria-controls={open ? popoverId : undefined}
        data-testid="grid-help-btn"
        onClick={() => setOpen((v) => !v)}
      >
        ?
      </button>
      {open && (
        <div
          id={popoverId}
          className="grid-help-popover"
          role="dialog"
          aria-label="Keyboard shortcuts"
          data-testid="grid-help-popover"
        >
          <p className="grid-help-title">Keyboard shortcuts</p>
          <ul className="grid-help-list">
            {SHORTCUTS.map((s) => (
              <li key={s.keys}>
                <kbd>{s.keys}</kbd>
                <span>{s.action}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
