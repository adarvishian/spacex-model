import type { GridDensity, GridPrefs, NumberDisplayFormat } from "../shared/grid-prefs";

type Props = {
  prefs: GridPrefs;
  onPrefsChange: (prefs: GridPrefs) => void;
  onFitColumns: () => void;
  onResetColumns: () => void;
};

const FORMAT_OPTIONS: { id: NumberDisplayFormat; label: string }[] = [
  { id: "mm", label: "$mm" },
  { id: "billions", label: "$B" },
  { id: "raw", label: "Raw" },
];

const DENSITY_OPTIONS: { id: GridDensity; label: string }[] = [
  { id: "comfortable", label: "Comfortable" },
  { id: "compact", label: "Compact" },
];

export function GridToolbar({ prefs, onPrefsChange, onFitColumns, onResetColumns }: Props) {
  const setFormat = (numberFormat: NumberDisplayFormat) => {
    onPrefsChange({ ...prefs, numberFormat });
  };

  const setDensity = (density: GridDensity) => {
    onPrefsChange({ ...prefs, density });
  };

  return (
    <div className="grid-toolbar" data-testid="grid-toolbar" role="toolbar" aria-label="Grid display options">
      <div className="grid-toolbar-group" role="group" aria-label="Number format">
        <span className="grid-toolbar-label">Format</span>
        {FORMAT_OPTIONS.map((opt) => (
          <button
            key={opt.id}
            type="button"
            className="grid-toolbar-btn"
            aria-label={`Show values as ${opt.label}`}
            aria-pressed={prefs.numberFormat === opt.id}
            onClick={() => setFormat(opt.id)}
          >
            {opt.label}
          </button>
        ))}
      </div>

      <div className="grid-toolbar-group" role="group" aria-label="Row density">
        <span className="grid-toolbar-label">Density</span>
        {DENSITY_OPTIONS.map((opt) => (
          <button
            key={opt.id}
            type="button"
            className="grid-toolbar-btn"
            aria-label={`${opt.label} row height`}
            aria-pressed={prefs.density === opt.id}
            onClick={() => setDensity(opt.id)}
          >
            {opt.label}
          </button>
        ))}
      </div>

      <div className="grid-toolbar-group grid-toolbar-actions">
        <button
          type="button"
          className="grid-toolbar-btn"
          aria-label="Fit columns to content"
          onClick={onFitColumns}
        >
          Fit columns
        </button>
        <button
          type="button"
          className="grid-toolbar-btn"
          aria-label="Reset column widths"
          onClick={onResetColumns}
        >
          Reset widths
        </button>
      </div>
    </div>
  );
}
