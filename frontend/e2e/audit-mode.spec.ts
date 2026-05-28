import { test, expect } from "@playwright/test";
import { installMockApi } from "./mock-api";

/** FRONTEND_PRD A1 — deep-linked audit URL opens grid and cell detail rail. */
test("A1: audit URL loads grid, derivation, and sources", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink?row=R8&col=2030");

  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 45_000 });
  await expect(page.getByTestId("derivation-panel")).toContainText(/Total Revenue|2030/i, {
    timeout: 20_000,
  });
  await expect(page.getByLabel("Cell detail panel")).toBeVisible();
  await expect(page.getByLabel("Sources panel")).toContainText(/§8.4/i);
});

/** FRONTEND_PRD A9 — keyboard navigation and shortcuts. */
test("A9: arrow keys move active cell; Enter expands derivation", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink?row=R8&col=2030");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 45_000 });

  const grid = page.getByTestId("audit-grid");
  await grid.focus();
  await page.keyboard.press("ArrowDown");
  await expect(page.getByTestId("derivation-panel")).toContainText(/Gross Profit/i, {
    timeout: 10_000,
  });

  await page.keyboard.press("Enter");
  await expect(page.locator(".derivation-panel.expanded")).toBeVisible();
});

test("A9: Cmd+K opens label search palette", async ({ page, browserName }) => {
  test.skip(browserName !== "chromium", "metaKey shortcuts");
  await installMockApi(page);
  await page.goto("/audit/starlink");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 45_000 });

  await page.keyboard.press("Meta+k");
  await expect(page.getByTestId("label-search-input")).toBeVisible();
  await page.getByTestId("label-search-input").fill("Revenue");
  await expect(page.locator(".label-search-results button").first()).toBeVisible();
});

/** FRONTEND_PRD A8 — cold load budget (mocked API, generous CI ceiling). */
test("A8: audit starlink route loads within budget", async ({ page }) => {
  await installMockApi(page);
  const start = Date.now();
  await page.goto("/audit/starlink?row=R8&col=2030");
  await expect(page.getByTestId("derivation-panel")).toContainText(/2030|Revenue/i, {
    timeout: 45_000,
  });
  const elapsed = Date.now() - start;
  const maxMs = Number(process.env.E2E_LOAD_MAX_MS ?? 8000);
  expect(elapsed).toBeLessThan(maxMs);
});
