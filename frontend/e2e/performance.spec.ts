import { test, expect } from "@playwright/test";

/** FRONTEND_PRD §8.3 — cell detail rail updates quickly after keyboard cell move. */
test("cell detail rail updates quickly after keyboard cell move", async ({ page }) => {
  const { installMockApi } = await import("./mock-api");
  await installMockApi(page);
  await page.goto("/audit/starlink?row=R8&col=2030");
  await page.getByTestId("audit-grid").waitFor({ timeout: 45_000 });
  await expect(page.getByTestId("derivation-panel")).toContainText(/Total Revenue/i);

  const t0 = Date.now();
  await page.keyboard.press("ArrowDown");
  await expect(page.getByTestId("derivation-panel")).toContainText(/Gross Profit/i, {
    timeout: 5_000,
  });
  await expect(page.getByLabel("Sources panel")).toBeVisible();
  const elapsed = Date.now() - t0;
  expect(elapsed).toBeLessThan(800);
});
