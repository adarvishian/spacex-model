import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { installMockApi } from "./mock-api";

const DEEP_ROW = "R11";
const DEEP_COL = "2030";

function seriousViolations(
  results: Awaited<ReturnType<AxeBuilder["analyze"]>>,
) {
  return results.violations.filter((v) => v.impact === "critical" || v.impact === "serious");
}

/** FRONTEND_UX_PRD A7 — axe reports no critical/serious violations on audit surfaces. */
test("A7 UX: audit grid and rail pass axe", async ({ page }) => {
  await installMockApi(page);
  await page.goto(`/audit/starlink?row=${DEEP_ROW}&col=${DEEP_COL}`);
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });
  await expect(page.getByTestId("derivation-panel")).toBeVisible({ timeout: 10_000 });

  const results = await new AxeBuilder({ page })
    .include(".audit-grid-panel")
    .include(".audit-detail-rail")
    .analyze();

  expect(seriousViolations(results)).toEqual([]);
});

/** FRONTEND_UX_PRD A7 — Run Audit tab passes axe. */
test("A7 UX: run audit tab passes axe", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/run_audit");
  await expect(page.locator(".run-audit-tab")).toContainText(/Solver convergence/i, {
    timeout: 5_000,
  });

  const results = await new AxeBuilder({ page }).include(".run-audit-tab").analyze();
  expect(seriousViolations(results)).toEqual([]);
});

/** FRONTEND_UX_PRD A7 — keyboard-only core loop: select cell, read derivation, open Run Audit. */
test("A7 UX: keyboard walkthrough completes core loop", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/audit/starlink");
  await expect(page.getByTestId("audit-grid")).toBeVisible({ timeout: 5_000 });

  const firstNumCell = page.locator(".audit-grid-wrap .ag-cell.num-cell").first();
  await firstNumCell.click();
  await expect(page.getByTestId("derivation-panel")).toBeVisible({ timeout: 10_000 });

  const grid = page.getByTestId("audit-grid");
  await grid.focus();
  await page.keyboard.press("ArrowRight");
  await expect(page.getByTestId("derivation-panel")).toBeVisible();

  await page.keyboard.press("Tab");
  const focused = await page.evaluate(() => document.activeElement?.className ?? "");
  expect(focused.length).toBeGreaterThan(0);

  await page.goto("/audit/run_audit");
  await expect(page.locator(".run-audit-tab")).toContainText(/2025 calibration anchors/i, {
    timeout: 5_000,
  });
  await page.locator(".run-audit-tab").focus();
  await expect(page.locator(".run-audit-tab")).toBeFocused();
});
