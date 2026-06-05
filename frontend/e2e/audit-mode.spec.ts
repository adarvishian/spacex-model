import { test, expect, type Page } from "@playwright/test";
import { DATA_SHEET_SLUGS, installMockApi } from "./mock-api";

async function assertNoNumericTruncation(page: Page, sheetSlug: string) {
  const issues = await page.evaluate(() => {
    const cells = Array.from(
      document.querySelectorAll(".audit-grid-wrap .ag-cell.num-cell"),
    ) as HTMLElement[];
    return cells
      .filter((cell) => {
        const text = cell.textContent ?? "";
        if (text.includes("…")) return true;
        return cell.scrollWidth > cell.clientWidth + 2;
      })
      .map((cell) => cell.textContent?.trim() ?? "(empty)");
  });
  expect(issues, `truncated numeric cells on ${sheetSlug}`).toEqual([]);
}

/** Deep-linked audit URL — row/col match precomputed base_case artifact. */
const DEEP_ROW = "R11";
const DEEP_COL = "2030";

/** FRONTEND_PRD A1 — deep-linked audit URL opens grid and cell detail rail. */
test("A1: audit URL loads grid, derivation, and sources", async ({ page }) => {
  await installMockApi(page);
  await page.goto(`/audit/starlink?row=${DEEP_ROW}&col=${DEEP_COL}`);

  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });
  await expect(page.getByTestId("derivation-panel")).toContainText(/BB Revenue|2030/i, {
    timeout: 20_000,
  });
  await expect(page.getByLabel("Cell detail panel")).toBeVisible();
  await expect(page.getByLabel("Sources panel")).toBeVisible();
});

/** FRONTEND_PRD A9 — keyboard navigation and shortcuts. */
test("A9: arrow keys move active cell; Enter expands derivation", async ({ page }) => {
  await installMockApi(page);
  await page.goto(`/audit/starlink?row=${DEEP_ROW}&col=${DEEP_COL}`);
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const grid = page.getByTestId("audit-grid");
  await grid.focus();
  await page.keyboard.press("ArrowDown");
  await expect(page.getByTestId("derivation-panel")).toContainText(/DTC Revenue/i, {
    timeout: 10_000,
  });

  await page.keyboard.press("Enter");
  await expect(page.locator(".derivation-panel.expanded")).toBeVisible();
});

test("A9: Cmd+K opens label search palette", async ({ page, browserName }) => {
  test.skip(browserName !== "chromium", "metaKey shortcuts");
  await installMockApi(page);
  await page.goto("/audit/starlink");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  await page.keyboard.press("Meta+k");
  await expect(page.getByTestId("label-search-input")).toBeVisible();
  await page.getByTestId("label-search-input").fill("Revenue");
  await expect(page.locator(".label-search-results button").first()).toBeVisible();
});

/** FRONTEND_PRD A8 — cold load budget (mocked API, generous CI ceiling). */
test("A8: audit starlink route loads within budget", async ({ page }) => {
  await installMockApi(page);
  const start = Date.now();
  await page.goto(`/audit/starlink?row=${DEEP_ROW}&col=${DEEP_COL}`);
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });
  await expect(page.getByTestId("derivation-panel")).toContainText(/2030|Revenue/i, {
    timeout: 10_000,
  });
  const elapsed = Date.now() - start;
  const maxMs = Number(process.env.E2E_LOAD_MAX_MS ?? 8000);
  expect(elapsed).toBeLessThan(maxMs);
});

/** FRONTEND_UX_PRD A4 — base case paints from precomputed artifact before solver response. */
test("A4: base case grid visible before runDeterministic response", async ({ page }) => {
  await installMockApi(page);

  let deterministicResolved = false;
  await page.route("**/api/runs/deterministic", async (route) => {
    if (route.request().method() !== "POST") {
      return route.continue();
    }
    await new Promise((r) => setTimeout(r, 60_000));
    deterministicResolved = true;
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        run_id: "e2e_delayed",
        scenario: "base_case",
        cached: true,
        solver: { iterations: 42, converged: true, max_residual: 0.001 },
        override_warnings: [],
      }),
    });
  });

  page.on("response", (response) => {
    if (
      response.url().includes("/runs/deterministic") &&
      response.request().method() === "POST"
    ) {
      deterministicResolved = true;
    }
  });

  await page.goto("/audit/starlink");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 3_000 });
  await expect(page.locator(".ag-cell").first()).toBeVisible();
  expect(deterministicResolved).toBe(false);
  await expect(page.getByTestId("run-provenance")).toHaveText("precomputed");
});

/** FRONTEND_UX_PRD A4 — non-base scenario shows skeleton + status, not a blank pane. */
test("A4: non-base scenario shows progress skeleton", async ({ page }) => {
  await installMockApi(page);

  await page.route("**/api/runs/deterministic", async (route) => {
    if (route.request().method() !== "POST") {
      return route.continue();
    }
    const body = route.request().postDataJSON() as { scenario?: string } | undefined;
    if (body?.scenario === "bear") {
      await new Promise((r) => setTimeout(r, 5_000));
      return route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          run_id: "e2e_bear_run",
          scenario: "bear",
          cached: false,
          solver: { iterations: 42, converged: true, max_residual: 0.001 },
          override_warnings: [],
        }),
      });
    }
    return route.continue();
  });

  await page.goto("/audit/starlink");
  await page.getByLabel("Scenario").selectOption("bear");
  await expect(page.getByTestId("audit-run-status")).toBeVisible({ timeout: 3_000 });
  await expect(page.getByTestId("audit-grid-skeleton")).toBeVisible();
});

/** FRONTEND_UX_PRD F7 — Run Audit reuses precomputed payload without blocking. */
test("A4: run audit tab shows precomputed audit without skeleton", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/run_audit");
  await expect(page.getByTestId("run-audit-skeleton")).not.toBeVisible({ timeout: 3_000 });
  await expect(page.locator(".run-audit-tab")).toContainText(/Solver convergence/i);
  await expect(page.getByTestId("run-provenance")).toHaveText("precomputed");
});

/** FRONTEND_UX_PRD A1 — no numeric truncation across all 13 data sheets (F1). */
test("A1 UX: numeric cells fit without ellipsis on all data sheets", async ({ page }) => {
  await installMockApi(page);

  for (const slug of DATA_SHEET_SLUGS) {
    await page.goto(`/audit/${slug}`);
    await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 8_000 });
    await expect(page.locator(".audit-grid-wrap .ag-cell.num-cell").first()).toBeVisible({
      timeout: 8_000,
    });
    await assertNoNumericTruncation(page, slug);
  }
});

/** FRONTEND_UX_PRD A1 — binary flag rows render 1/0, never % (F4). */
test("A1 UX: flag rows render 1/0 not percent", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const r28 = page.locator('.ag-row[row-id="R28"] .ag-cell.num-cell').first();
  const r29 = page.locator('.ag-row[row-id="R29"] .ag-cell.num-cell').first();
  await expect(r28).toHaveText("1");
  await expect(r29).toHaveText("0");
  await expect(r28).not.toContainText("%");
});

/** FRONTEND_UX_PRD A1 — $mm rows must not render as % (F4). */
test("A1 UX: group P&L OpEx row renders dollars not percent", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/group_pnl");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const r34 = page.locator('.ag-row[row-id="R34"] .ag-cell.num-cell').first();
  await expect(r34).not.toContainText("%");
  await expect(r34).toHaveText(/\d+/);
});

/** FRONTEND_UX_PRD A1 — label tooltip and derivation strip show full label (F5). */
test("A1 UX: full label in tooltip and derivation strip", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink?row=R11&col=2026");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const labelCell = page.locator('.ag-row[row-id="R11"] .label-cell').first();
  const title = await labelCell.getAttribute("title");
  expect(title).toMatch(/Starlink BB Revenue from curve/i);

  await expect(page.getByTestId("derivation-panel")).toContainText(
    /Starlink BB Revenue from curve/i,
  );
});

/** FRONTEND_UX_PRD A2 — stub cells show Planned state, never "= $mm" (F2). */
test("A2 UX: stub cell shows Planned state not empty computed", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink?row=R11&col=2030");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const panel = page.getByTestId("derivation-panel");
  await expect(panel).toContainText(/Planned/i, { timeout: 10_000 });
  await expect(panel).not.toContainText(/not yet ported to a traced derivation/i);
  await expect(panel).not.toContainText("= $mm");
  await expect(page.getByTestId("derivation-stub-state")).toBeVisible();
  await expect(page.getByTestId("depgraph-empty")).toBeVisible();
  await expect(page.locator(".depgraph-canvas")).not.toBeVisible();
});

/** Lineage Trust L1 — derived numeric cells never show the stub Planned copy. */
test("L1: derived cell does not show Planned stub state", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/group_pnl?row=R14&col=2026");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const panel = page.getByTestId("derivation-panel");
  await expect(panel).toContainText(/Group Revenue/i, { timeout: 10_000 });
  await expect(page.getByTestId("derivation-stub-state")).not.toBeVisible();
  await expect(panel).not.toContainText(/Planned —/i);
  await expect(page.getByTestId("derivation-computed")).toBeVisible();
});

/** FRONTEND_UX_PRD A2 — derived cells show formula and resolved inputs (F2). */
test("A2 UX: derived cell shows formula and resolved inputs", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/group_pnl?row=R14&col=2026");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const panel = page.getByTestId("derivation-panel");
  await expect(panel).toContainText(/Group Revenue/i, { timeout: 10_000 });
  await expect(page.getByTestId("derivation-formula")).toContainText(/Σ module revenues/i);
  await expect(page.getByTestId("derivation-computed")).toBeVisible();
  await expect(page.getByTestId("derivation-computed")).not.toContainText("= $mm");

  const inputRows = page.locator('[data-testid="derivation-inputs"] tbody tr');
  await expect(inputRows).toHaveCount(2);
  await expect(page.locator(".depgraph-canvas")).toBeVisible();
  await expect(page.getByTestId("depgraph-empty")).not.toBeVisible();
});

/** Lineage Trust Sprint 3 — derived formula is an expression; Sources has no code paths (L2/L4). */
test("L2/L4: derived cell shows real formula and clean sources panel", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/group_pnl?row=R14&col=2026");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const formula = page.getByTestId("derivation-formula");
  await expect(formula).toContainText(/Σ module revenues/i);
  await expect(formula).not.toContainText(/see Architecture/i);

  const sources = page.getByLabel("Sources panel");
  await expect(sources).toBeVisible();
  await expect(sources).toContainText(/Architecture & Methodology/i);
  await expect(sources).toContainText(/§9\.2/);
  await expect(sources).not.toContainText(/spacex_model\./i);
  await expect(sources).not.toContainText(/module calc\./i);
  await expect(sources.getByText("Principle", { exact: true })).toBeVisible();
  await expect(sources.getByText("Rule", { exact: true })).toBeVisible();
  await expect(sources).toContainText(/Rule 9/i);
});

/** Lineage Trust Sprint 4 — change history shows before→after effect from ingest diff (L3). */
test("L3: change history renders effect_on_cell before and after", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/group_pnl?row=R14&col=2030");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const history = page.getByLabel("Change history");
  await expect(history).toBeVisible();
  await expect(history).toContainText(/Effect:/i);
  await expect(history).toContainText(/12,000/);
  await expect(history).toContainText(/12,100/);
  await expect(history).toContainText(/\+100/);
  await expect(history).toContainText(/VALUE/i);
});

/** FRONTEND_UX_PRD A3 — grid value matches derivation displayed value (F6). */
test("A3 UX: derivation displayed value matches grid cell", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink?row=R11&col=2030");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const gridCell = page.locator('.ag-row[row-id="R11"] .ag-cell[col-id="y_2030"]');
  await expect(gridCell).toBeVisible();
  const gridText = ((await gridCell.textContent()) ?? "").trim();

  await expect(page.getByTestId("derivation-displayed-value")).toContainText(gridText, {
    timeout: 10_000,
  });
});

/** FRONTEND_UX_PRD A5 — calibration uses PASS/FAIL with glyph; no ambiguous CHECK (F11). */
test("A5 UX: calibration verdicts use PASS/FAIL not CHECK", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/run_audit");
  await expect(page.locator(".run-audit-tab")).toContainText(/2025 calibration anchors/i, {
    timeout: 5_000,
  });

  const table = page.locator(".run-audit-table").first();
  await expect(table).toBeVisible();
  await expect(table).not.toContainText("CHECK");

  const statusCells = table.locator("tbody tr td:last-child");
  const count = await statusCells.count();
  expect(count).toBeGreaterThan(0);

  for (let i = 0; i < count; i++) {
    const text = ((await statusCells.nth(i).textContent()) ?? "").trim();
    expect(text).toMatch(/^(✓ PASS|✗ FAIL)$/);
  }

  await expect(table.locator("thead")).toContainText("Δ% vs tol");
});

/** FRONTEND_UX_PRD A6 — single token source enforced by CI check (script smoke). */
test("A6 UX: design token lint passes", async () => {
  const { execSync } = await import("node:child_process");
  const { dirname, join } = await import("node:path");
  const { fileURLToPath } = await import("node:url");
  const frontendRoot = join(dirname(fileURLToPath(import.meta.url)), "..");
  expect(() =>
    execSync("npm run check:tokens", { cwd: frontendRoot, stdio: "pipe" }),
  ).not.toThrow();
});

/** FRONTEND_UX_PRD A8 — grid toolbar toggles format and density; persists in localStorage (F14). */
test("A8 UX: grid toolbar format and density persist across reload", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink");
  await expect(page.getByTestId("grid-toolbar")).toBeVisible({ timeout: 5_000 });

  await page.getByRole("button", { name: "Show values as $B" }).click();
  await page.getByRole("button", { name: "Comfortable row height" }).click();

  const prefs = await page.evaluate(() => localStorage.getItem("audit-grid-prefs"));
  expect(prefs).toContain("billions");
  expect(prefs).toContain("comfortable");

  await page.reload();
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  await expect(page.getByRole("button", { name: "Show values as $B" })).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await expect(page.getByRole("button", { name: "Comfortable row height" })).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  await expect(page.getByTestId("audit-grid")).toHaveAttribute("data-density", "comfortable");
});

/** FRONTEND_UX_PRD A8 — format toggle re-renders numeric cells (F14). */
test("A8 UX: billions format renders compact dollar values", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/group_pnl");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  await page.getByRole("button", { name: "Show values as $B" }).click();
  const cell = page.locator('.ag-row[row-id="R14"] .ag-cell.num-cell').first();
  await expect(cell).toContainText(/\$[\d.]+B/);
});

/** FRONTEND_UX_PRD A9 — single rail empty state when no cell selected (F9). */
test("A9 UX: rail shows one empty state without cell selection", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  await expect(page.getByTestId("rail-empty-state")).toBeVisible();
  await expect(page.getByTestId("derivation-panel")).not.toBeVisible();
  await expect(page.getByText("Select a cell to view sources")).not.toBeVisible();
  await expect(page.getByText("Select a cell to view change history")).not.toBeVisible();

  const emptyHints = await page.locator(".panel-hint").count();
  expect(emptyHints).toBe(0);
});

/** FRONTEND_UX_PRD A9 — title bar single row at 1280px; shortcuts behind ? popover (F10). */
test("A9 UX: title bar does not wrap at 1280px; help popover shows shortcuts", async ({
  page,
}) => {
  await installMockApi(page);
  await page.setViewportSize({ width: 1280, height: 900 });
  await page.goto("/audit/starlink");
  await expect(page.getByTestId("grid-title-bar")).toBeVisible({ timeout: 5_000 });

  const height = await page.getByTestId("grid-title-bar").evaluate((el) => el.clientHeight);
  expect(height).toBeLessThan(48);

  await expect(page.locator(".grid-shortcuts-hint")).not.toBeVisible();
  await page.getByTestId("grid-help-btn").click();
  await expect(page.getByTestId("grid-help-popover")).toBeVisible();
  await expect(page.getByTestId("grid-help-popover")).toContainText(/Move active cell/i);
  await expect(page.getByTestId("grid-help-popover")).toContainText(/Search row labels/i);
});

/** Lineage Trust Sprint 7 — MC panel from headline module FCF cell (R-M1.9). */
test("MC3: audit MC panel opens from module FCF with distribution and provenance", async ({
  page,
}) => {
  await installMockApi(page);
  await page.goto("/audit/starlink?row=R106&col=2026");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  await expect(page.getByTestId("rail-view-toggle")).toBeVisible();
  await page.getByTestId("rail-view-mc").click();

  const panel = page.getByTestId("audit-mc-panel");
  await expect(panel).toBeVisible();
  await expect(page.getByTestId("audit-mc-progress")).toHaveCount(0);
  await expect(page.getByTestId("mc-ev-distribution")).toBeVisible({ timeout: 5_000 });
  await expect(page.getByTestId("mc-percentile-table")).toBeVisible();
  await expect(page.getByTestId("tornado-chart")).toBeVisible();
  await expect(page.getByTestId("audit-mc-provenance-detail")).toContainText(/2,000/);
  await expect(page.getByTestId("audit-mc-provenance-detail")).toContainText(/Seed:\s*42/i);
  await expect(page.getByTestId("audit-mc-provenance-detail")).toContainText(/Convergence:\s*converged/i);
  await expect(page.getByTestId("mc-p5")).toHaveText("$220B");
  await expect(page.getByTestId("mc-p50")).toHaveText("$278B");
  await expect(page.getByTestId("mc-p95")).toHaveText("$340B");

  await page.getByTestId("rail-view-derivation").click();
  await expect(page.getByTestId("derivation-panel")).toBeVisible();
  await expect(page.getByTestId("audit-mc-panel")).not.toBeVisible();
});

/** Lineage Trust Sprint 7 — deep-linked MC run reproduces identical aggregates (R-M1.8). */
test("MC4: audit MC run id deep-link reproduces percentiles", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink?row=R106&col=2026&mc=precache");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  await expect(page.getByTestId("audit-mc-panel")).toBeVisible({ timeout: 5_000 });
  await expect(page.getByTestId("mc-ev-distribution")).toBeVisible({ timeout: 5_000 });
  await expect(page.getByTestId("mc-p5")).toHaveText("$220B");
  await expect(page.getByTestId("mc-p50")).toHaveText("$278B");
  await expect(page.getByTestId("mc-p95")).toHaveText("$340B");
  await expect(page.getByTestId("audit-mc-provenance")).toContainText(/precomputed/i);
});

/** FRONTEND_UX_PRD A1 — implausible pct values show raw + warning (F4 guard). */
test("A1 UX: implausible pct magnitudes show warning not silent percent", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/allocator");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const r25 = page.locator('.ag-row[row-id="R25"] .ag-cell.num-cell').nth(1);
  await expect(r25).toContainText("⚠");
  await expect(r25).not.toContainText("%");
});
