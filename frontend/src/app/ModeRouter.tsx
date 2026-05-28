import { lazy, Suspense } from "react";
import { Link } from "react-router-dom";
import { Navigate, Route, Routes } from "react-router-dom";

const AuditApp = lazy(() => import("./AuditApp"));
const ClientApp = lazy(() => import("./ClientApp"));
const LegacyApp = lazy(() => import("../App"));

function RouteFallback() {
  return <p className="audit-loading">Loading…</p>;
}

export default function ModeRouter() {
  return (
    <Suspense fallback={<RouteFallback />}>
      <Routes>
        <Route path="/" element={<Navigate to="/audit/starlink" replace />} />
        <Route path="/audit" element={<Navigate to="/audit/starlink" replace />} />
        <Route path="/audit/:sheetSlug" element={<AuditApp />} />
        <Route path="/client/*" element={<ClientApp />} />
        <Route path="/explorer" element={<LegacyApp />} />
        <Route path="*" element={<Navigate to="/audit/starlink" replace />} />
      </Routes>
    </Suspense>
  );
}

export function ModeSwitchLink({
  to,
  children,
}: {
  to: "/audit" | "/client";
  children: React.ReactNode;
}) {
  return (
    <Link to={to} className="mode-switch">
      {children}
    </Link>
  );
}
