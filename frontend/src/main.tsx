import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import ModeRouter from "./app/ModeRouter";
import { queryClient } from "./shared/query-client";
import "./styles/tokens.css";
import "./styles/grid.css";
import "./styles.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <ModeRouter />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
);
