import { LineageEntry } from "../api";

type Props = {
  entry: LineageEntry;
  onClose: () => void;
};

export function LineagePanel({ entry, onClose }: Props) {
  return (
    <aside className="lineage-panel" role="dialog" aria-label="Audit lineage">
      <button type="button" className="close-btn" onClick={onClose} aria-label="Close">
        ×
      </button>
      <h3>{entry.display_name}</h3>
      <dl className="lineage-dl">
        <dt>Function</dt>
        <dd>
          {entry.module_path}::{entry.function}
        </dd>
        <dt>Excel cell</dt>
        <dd>{entry.excel_cell || "—"}</dd>
        <dt>Excel label</dt>
        <dd>{entry.excel_label}</dd>
        <dt>Architecture</dt>
        <dd>{entry.architecture_ref || "—"}</dd>
        <dt>Principle</dt>
        <dd>{entry.principle || "—"}</dd>
        {entry.input_labels.length > 0 && (
          <>
            <dt>Inputs</dt>
            <dd>{entry.input_labels.join(", ")}</dd>
          </>
        )}
      </dl>
    </aside>
  );
}
