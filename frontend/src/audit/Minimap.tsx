import { LIFECYCLE_STAGES, SHEET_GRAPH, SHEET_GROUPS } from "../data/sheet_graph";
import type { ActiveCell, LineageEntry } from "../shared/types";

type Props = {
  activeSheetSlug: string;
  lineage: LineageEntry | null;
  activeCell: ActiveCell | null;
  onNavigateSheet: (slug: string) => void;
  onNavigateCell?: (node: { key: string; label: string }) => void;
};

export function Minimap({
  activeSheetSlug,
  lineage,
  activeCell,
  onNavigateSheet,
  onNavigateCell,
}: Props) {
  const lifecycle = lineage?.lifecycle_stage ?? "output";
  const sectionRef =
    lineage?.section_ref ??
    (activeCell ? `${activeSheetSlug} · ${activeCell.label}` : "—");

  const upstream = lineage?.upstream ?? [];
  const downstream = lineage?.downstream ?? [];

  return (
    <section className="minimap minimap-below-grid" aria-label="Model minimap">
      <div className="minimap-meta">
        <div className="lifecycle-block">
          <h3>Lifecycle stage</h3>
          <div className="lifecycle-stages">
            {LIFECYCLE_STAGES.map((stage) => (
              <span
                key={stage.id}
                className={`stage ${lifecycle === stage.id ? "active" : ""}`}
              >
                {stage.label}
              </span>
            ))}
          </div>
        </div>

        <div className="section-ref-block">
          <span className="lbl">Section in sheet</span>
          {sectionRef}
        </div>
      </div>

      <div className="minimap-neighbors">
        <div className="neighbor-block">
          <h3>Upstream (1-hop)</h3>
          {upstream.length === 0 && <p className="muted">Select a cell to see upstream cells.</p>}
          {upstream.map((n) => (
            <button
              key={n.key}
              type="button"
              className="neighbor-row neighbor-btn"
              onClick={() => onNavigateCell?.(n)}
            >
              <span className="arrow">←</span> {n.label}
            </button>
          ))}
        </div>

        <div className="neighbor-block">
          <h3>Downstream (1-hop)</h3>
          {downstream.length === 0 && (
            <p className="muted">Select a cell to see downstream cells.</p>
          )}
          {downstream.map((n) => (
            <button
              key={n.key}
              type="button"
              className="neighbor-row neighbor-btn"
              onClick={() => onNavigateCell?.(n)}
            >
              <span className="arrow">→</span> {n.label}
            </button>
          ))}
        </div>
      </div>

      <div className="minimap-map">
        <h2>Model Map</h2>
        <div className="map-grid">
          {SHEET_GROUPS.map((group) => {
            const nodes = SHEET_GRAPH.filter((n) => n.group === group.id);
            return (
              <div key={group.id} className="map-group-block">
                <div className="map-group">{group.title}</div>
                <div className="map-group-cells">
                  {nodes.map((node) => {
                    const isActive = node.slug === activeSheetSlug;
                    const feeds =
                      !isActive &&
                      upstream.some((u) =>
                        u.label.toLowerCase().includes(node.label.toLowerCase()),
                      );
                    const depends =
                      !isActive &&
                      downstream.some((d) =>
                        d.label.toLowerCase().includes(node.label.toLowerCase()),
                      );
                    return (
                      <button
                        key={node.slug}
                        type="button"
                        className={`map-cell ${isActive ? "active" : ""} ${feeds ? "feeds" : ""} ${depends ? "depends" : ""}`}
                        onClick={() => onNavigateSheet(node.slug)}
                        aria-label={`${node.label} sheet`}
                        aria-current={isActive ? "true" : undefined}
                      >
                        <span className="dot" />
                        {node.label}
                      </button>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
