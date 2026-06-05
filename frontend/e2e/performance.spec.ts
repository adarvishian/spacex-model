import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const DEEP_ROW = "R11";
const DEEP_COL = "2030";

/** FRONTEND_UX_PRD A7 — performance suite includes axe gate on audit shell. */
test("audit shell passes axe with no serious violations", async ({ page }) => {
  const { installMockApi } = await import("./mock-api");
  await installMockApi(page);
  await page.goto(`/audit/starlink?row=${DEEP_ROW}&col=${DEEP_COL}`);
  await page.getByTestId("audit-grid").waitFor({ timeout: 5_000 });

  const results = await new AxeBuilder({ page }).include(".audit-app").analyze();
  const serious = results.violations.filter(
    (v) => v.impact === "critical" || v.impact === "serious",
  );
  expect(serious).toEqual([]);
});

/** FRONTEND_PRD §8.3 — cell detail rail updates quickly after keyboard cell move. */
test("cell detail rail updates quickly after keyboard cell move", async ({ page }) => {
  const { installMockApi } = await import("./mock-api");
  await installMockApi(page);
  await page.goto(`/audit/starlink?row=${DEEP_ROW}&col=${DEEP_COL}`);
  await page.getByTestId("audit-grid").waitFor({ timeout: 5_000 });
  await expect(page.getByTestId("derivation-panel")).toContainText(/BB Revenue/i);

  const t0 = Date.now();
  await page.keyboard.press("ArrowDown");
  await expect(page.getByTestId("derivation-panel")).toContainText(/DTC Revenue/i, {
    timeout: 5_000,
  });
  await expect(page.getByLabel("Sources panel")).toBeVisible();
  const elapsed = Date.now() - t0;
  expect(elapsed).toBeLessThan(800);
});
