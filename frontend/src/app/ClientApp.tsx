import { Link } from "react-router-dom";

export default function ClientApp() {
  return (
    <div className="client-stub">
      <header className="audit-header">
        <div className="audit-header-left">
          <h1>Mach33 · SpaceX Valuation</h1>
          <span className="audit-badge">CLIENT MODE</span>
        </div>
        <Link to="/audit/starlink" className="mode-switch">
          Switch to Audit →
        </Link>
      </header>
      <main className="client-stub-body">
        <p>Client Mode ships in Phase 3. Use Audit Mode to explore the Starlink grid.</p>
        <Link to="/audit/starlink">Open Audit Mode</Link>
      </main>
    </div>
  );
}
