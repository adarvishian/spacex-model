export function RailEmptyState() {
  return (
    <section
      className="rail-empty-state"
      data-testid="rail-empty-state"
      aria-label="Cell detail panel"
    >
      <div className="rail-empty-icon" aria-hidden="true">
        ⊞
      </div>
      <h2 className="rail-empty-title">Select a cell</h2>
      <p className="rail-empty-desc">
        Click any grid cell to inspect its formula, traced inputs, dependency graph, sources,
        and change history.
      </p>
      <ul className="rail-empty-features">
        <li>Formula &amp; computed value</li>
        <li>Resolved inputs &amp; dependency graph</li>
        <li>Sources &amp; change history</li>
      </ul>
    </section>
  );
}
