import { test, expect } from "@playwright/test";
import { installMockApi } from "./mock-api";
import { encodeShareState } from "../src/shared/share-link";

const FORBIDDEN_IN_CLIENT = [
  "lineage_key",
  "V2.16",
  "xlsx_cached",
  "divergence",
  "converged",
  "git_sha",
  "formula_expression",
  "module_path",
  "!R",
];

/** FRONTEND_PRD A5 — Client Mode must not leak audit machinery. */
test("A5: client DOM excludes forbidden audit tokens", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/client");
  await expect(page.getByTestId("client-app")).toBeVisible({ timeout: 30_000 });
  await expect(page.getByRole("heading", { name: /SpaceX Valuation/i })).toBeVisible();

  const text = await page.locator(".client-app").innerText();
  const html = await page.locator(".client-app").innerHTML();
  const blob = `${text}\n${html}`.toLowerCase();

  for (const token of FORBIDDEN_IN_CLIENT) {
    expect(blob, `forbidden token: ${token}`).not.toContain(token.toLowerCase());
  }
});

/** FRONTEND_PRD A6 — custom builder range validation. */
test("A6: custom mars_pct validation", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/client");
  await page.getByText("Custom…").click();
  await expect(page.getByTestId("custom-input-mars_pct")).toBeVisible();

  const mars = page.getByTestId("custom-input-mars_pct");

  await mars.fill("0.25");
  await mars.blur();
  await expect(page.locator(".client-field-error")).toContainText(/between 0 and 0.2/i);

  await mars.fill("0.18");
  await mars.blur();
  await expect(page.locator(".client-field-warn")).toContainText(/above P90/i);

  await mars.fill("0.07");
  await mars.blur();
  await expect(page.locator(".client-field-error")).toHaveCount(0);
  await expect(page.locator(".client-field-warn")).toHaveCount(0);
});

/** Sprint 6 — base-case MC distribution renders instantly from precache. */
test("MC1: base case shows distribution without wait", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/client");
  await expect(page.getByTestId("client-app")).toBeVisible({ timeout: 30_000 });
  await expect(page.getByTestId("mc-panel")).toBeVisible();
  await expect(page.getByTestId("mc-ev-distribution")).toBeVisible({ timeout: 5_000 });
  await expect(page.getByTestId("mc-progress")).toHaveCount(0);
  await expect(page.getByTestId("mc-provenance")).toContainText(/precomputed/i);
  await expect(page.getByTestId("mc-p5")).toHaveText("$220B");
  await expect(page.getByTestId("mc-p50")).toHaveText("$278B");
  await expect(page.getByTestId("mc-p95")).toHaveText("$340B");
  await expect(page.getByTestId("mc-fcf-fan")).toBeVisible();
});

/** Milestone 3.2 — bear scenario loads instantly from precache (no custom MC). */
test("MC2: bear scenario MC loads from precache without run button", async ({ page }) => {
  await installMockApi(page);
  await page.goto("/client");
  await expect(page.getByTestId("client-app")).toBeVisible({ timeout: 30_000 });
  await page.locator('.client-scenario-card:has(input[value="bear"])').click();
  await expect(page.getByTestId("mc-ev-distribution")).toBeVisible({ timeout: 5_000 });
  await expect(page.getByTestId("mc-progress")).toHaveCount(0);
  await expect(page.getByTestId("mc-run-btn")).toHaveCount(0);
  await expect(page.getByTestId("mc-provenance")).toContainText(/precomputed/i);
  await expect(page.getByTestId("mc-p5")).toHaveText("$220B");
  await expect(page.getByTestId("mc-p50")).toHaveText("$278B");
  await expect(page.getByTestId("mc-p95")).toHaveText("$340B");
});

/** FRONTEND_PRD A10 — share link round-trip. */
test("A10: share link restores custom overrides", async ({ page }) => {
  await installMockApi(page);
  const token = encodeShareState("base_case", { mars_pct: 0.09 });
  await page.goto(`/client?s=${encodeURIComponent(token)}`);
  await expect(page.getByTestId("client-app")).toBeVisible({ timeout: 30_000 });
  await expect(page.getByTestId("custom-input-mars_pct")).toHaveValue("0.09");
});
