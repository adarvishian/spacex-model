import { Link } from "react-router-dom";
import { Navigate, Route, Routes } from "react-router-dom";
import AuditApp from "./AuditApp";
import ClientApp from "./ClientApp";
import LegacyApp from "../App";

export default function ModeRouter() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/audit/starlink" replace />} />
      <Route path="/audit" element={<Navigate to="/audit/starlink" replace />} />
      <Route path="/audit/:sheetSlug" element={<AuditApp />} />
      <Route path="/client/*" element={<ClientApp />} />
      <Route path="/explorer" element={<LegacyApp />} />
      <Route path="*" element={<Navigate to="/audit/starlink" replace />} />
    </Routes>
  );
}

export function ModeSwitchLink({ to, children }: { to: "/audit" | "/client"; children: React.ReactNode }) {
  return (
    <Link to={to} className="mode-switch">
      {children}
    </Link>
  );
}
