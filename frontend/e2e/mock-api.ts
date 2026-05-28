import type { Page } from "@playwright/test";

const MOCK_RUN = {
  run_id: "e2e_run_1",
  scenario: "base_case",
  cached: true,
  solver: { iterations: 42, converged: true, max_residual: 0.001 },
  valuation: { group_ev_2025_b: 278, lineage_key: "valuation.group_ev" },
  module_ev: {
    customer_launch: { display_name: "Customer Launch", ev_2025_b: 42 },
    starlink: { display_name: "Starlink", ev_2025_b: 164 },
  },
  group: {
    group_fcf: {
      years: [2025, 2026, 2030],
      values: [1000, 1200, 1500],
    },
  },
  modules: {
    starlink: {
      display_name: "Starlink",
      total_revenue: { values: [7852, 9140, 22640] },
      blended_irr: { values: [0.22, 0.23, 0.27], unit: "pct" },
    },
  },
  override_warnings: [],
  conservation: { all_ok: true },
  audit_grids: {
    starlink: {
      sheet: "starlink",
      source_sheet: "Starlink",
      years: [2025, 2026, 2030],
      rows: [
        {
          row_id: "R8",
          row_index: 8,
          label: "Total Revenue ($mm)",
          section_ref: "§8.4",
          unit: "dollars_mm",
          base_case_value: null,
          year_values: [7852, 9140, 22640],
          cell_kinds: ["derived", "derived", "derived"],
          divergence_flags: ["match", "match", "match"],
          lineage_keys: ["starlink.rev.2025", "starlink.rev.2026", "starlink.rev.2030"],
          is_header: false,
        },
        {
          row_id: "R10",
          row_index: 10,
          label: "Gross Profit ($mm)",
          section_ref: "§8.4",
          unit: "dollars_mm",
          base_case_value: null,
          year_values: [4672, 5430, 13460],
          cell_kinds: ["derived", "derived", "derived"],
          divergence_flags: ["match", "match", "intentional"],
          lineage_keys: ["starlink.gp.2025", "starlink.gp.2026", "starlink.gp.2030"],
          is_header: false,
        },
      ],
    },
  },
};

const MOCK_LINEAGE = {
  key: "starlink.rev.2030",
  display_name: "Total Revenue",
  module_path: "calc.starlink.module",
  function: "compute_revenue",
  excel_cell: "R8",
  excel_label: "Total Revenue",
  architecture_ref: "§8.4",
  principle: "Principle 8",
  input_labels: ["V2 BB active sats"],
  cell_address: { sheet: "Starlink", row: "R8", column: "2030", year: 2030 },
  cell_kind: "derived",
  unit: "dollars_mm",
  formula_expression: "Total Revenue = Σ pool revenues",
  resolved_inputs: [
    {
      label: "V2 BB active sats",
      cell_address: "Starlink!R5:2030",
      value: 10200,
      unit: "count",
      lineage_key: "starlink.r5.2030",
    },
  ],
  computed_value: 22640,
  xlsx_cached_value: 22640,
  divergence_status: "match",
  lifecycle_stage: "output",
  section_ref: "§8.4 — Bandwidth-driven revenue",
  upstream: [{ key: "starlink.r5.2030", label: "Starlink!R5 · V2 BB sats" }],
  downstream: [{ key: "group.rev.2030", label: "Group P&L!R8 · Group Revenue" }],
  sources: {
    methodology: {
      spec_section: "§8.4",
      principle: "Principle 8",
      rule: "Rule 23",
      module: "calc.starlink.module.compute_revenue",
    },
  },
};

export async function installMockApi(page: Page) {
  await page.route("**/api/**", async (route) => {
    const url = new URL(route.request().url());
    const path = url.pathname.replace(/^\/api/, "");

    const json = (body: unknown, status = 200) =>
      route.fulfill({
        status,
        contentType: "application/json",
        body: JSON.stringify(body),
      });

    if (path === "/health") {
      return json({ status: "ok", git_sha: "e2e0000" });
    }
    if (path === "/scenarios") {
      return json([
        { name: "base_case", description: "Base", path: "scenarios/base_case.yaml" },
      ]);
    }
    if (path === "/sheets") {
      return json([
        {
          slug: "starlink",
          display_name: "Starlink",
          source_sheet: "Starlink",
          row_count: 235,
          col_count: 29,
          lifecycle_stage: "output",
          enabled: true,
        },
        {
          slug: "group_pnl",
          display_name: "Group P&L",
          source_sheet: "Group P&L",
          row_count: 125,
          col_count: 56,
          lifecycle_stage: "pnl",
          enabled: true,
        },
      ]);
    }
    if (path.startsWith("/sheets/") && path.endsWith("/grid")) {
      return json(MOCK_RUN.audit_grids.starlink);
    }
    if (path === "/runs/deterministic" && route.request().method() === "POST") {
      return json(MOCK_RUN);
    }
    if (path.startsWith("/lineage/") && !path.includes("/history") && !path.includes("/graph")) {
      const key = decodeURIComponent(path.split("/lineage/")[1]?.split("/")[0] ?? "");
      if (key.includes("gp")) {
        return json({
          ...MOCK_LINEAGE,
          key,
          display_name: "Gross Profit ($mm)",
          excel_label: "Gross Profit",
          formula_expression: "Gross Profit = Revenue − COGS",
          computed_value: 13460,
          cell_address: { sheet: "Starlink", row: "R10", column: "2030", year: 2030 },
        });
      }
      return json(MOCK_LINEAGE);
    }
    if (path.includes("/history")) {
      return json({
        entries: [
          {
            date: "2026-05-26",
            commit_sha: "a1b2c3d",
            title: "Sprint 11e merged",
            change_kind: "formula",
            dev_log_anchor: "docs/DEV_LOG.md#sprint-11e-merge",
          },
        ],
      });
    }
    if (path.includes("/graph")) {
      return json({ root_key: "starlink.rev.2030", depth: 2, nodes: [], edges: [] });
    }
    if (path === "/client/scenarios") {
      return json([
        {
          id: "base_case",
          name: "Base Case",
          description: "Base",
          key_inputs: [],
          group_ev_2025_b: 278,
        },
      ]);
    }
    if (path === "/client/inputs/whitelist") {
      return json([
        {
          id: "mars_pct",
          plain_label: "Share of group FCF dedicated to Mars",
          min: 0,
          max: 0.2,
          default: 0.05,
        },
      ]);
    }
    if (path === "/client/decode-share") {
      const token = url.searchParams.get("s") ?? "";
      try {
        const pad = "=".repeat((4 - (token.length % 4)) % 4);
        const b64 = token.replace(/-/g, "+").replace(/_/g, "/") + pad;
        const data = JSON.parse(Buffer.from(b64, "base64").toString("utf-8")) as {
          scenario?: string;
          overrides?: Record<string, number>;
        };
        return json({
          scenario: data.scenario ?? "base_case",
          overrides: data.overrides ?? {},
          canonical_overrides: {},
        });
      } catch {
        return json({ detail: "invalid" }, 400);
      }
    }
    if (path === "/client/validate-share" && route.request().method() === "POST") {
      const body = route.request().postDataJSON() as {
        scenario?: string;
        overrides?: Record<string, number>;
      };
      return json({
        ok: true,
        scenario: body?.scenario ?? "base_case",
        share_token: "mock",
        canonical_overrides: {},
      });
    }

    return route.continue();
  });
}
