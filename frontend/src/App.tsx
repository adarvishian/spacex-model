import { Navigate } from "react-router-dom";

/** Legacy explorer shell — redirects to Audit Mode (R-M1.11). */
export default function App() {
  return <Navigate to="/audit/starlink" replace />;
}
