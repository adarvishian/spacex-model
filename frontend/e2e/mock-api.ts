import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import type { Page } from "@playwright/test";

const GRID_UNITS = [
  "dollars_mm",
  "pct",
  "ratio",
  "count",
  "kg_to_leo",
  "gbps",
  "flag",
  "boolean",
] as const;

const ARTIFACT_PATH = join(
  dirname(fileURLToPath(import.meta.url)),
  "../public/data/base_case_run.json",
);

type GridRow = {
  row_id: string;
  label: string;
  unit: string;
  [key: string]: unknown;
};

type GridPayload = {
  sheet: string;
  source_sheet: string;
  years: number[];
  rows: GridRow[];
};

type BaseCaseArtifact = {
  git_sha: string;
  run_id: string;
  audit_grids: Record<string, GridPayload>;
  run_audit: Record<string, unknown>;
};

const RAW_ARTIFACT = JSON.parse(readFileSync(ARTIFACT_PATH, "utf-8")) as BaseCaseArtifact;

/** §8 API ask — corrected unit metadata for e2e (production consumes payload as-is). */
const UNIT_PATCHES: Record<string, Record<string, string>> = {
  starlink: { R28: "flag", R29: "flag" },
  group_pnl: { R34: "dollars_mm" },
};

function patchGridUnits(grid: GridPayload): GridPayload {
  const patches = UNIT_PATCHES[grid.sheet];
  if (!patches) return grid;
  return {
    ...grid,
    rows: grid.rows.map((row) => {
      const unit = patches[row.row_id];
      return unit ? { ...row, unit } : row;
    }),
  };
}

function patchArtifact(artifact: BaseCaseArtifact): BaseCaseArtifact {
  const audit_grids: Record<string, GridPayload> = {};
  for (const [slug, grid] of Object.entries(artifact.audit_grids)) {
    audit_grids[slug] = patchGridUnits(grid);
  }
  return { ...artifact, audit_grids };
}

const ARTIFACT = patchArtifact(RAW_ARTIFACT);

/** 13 data sheets per FRONTEND_UX_PRD A1 — excludes run_audit. */
export const DATA_SHEET_SLUGS = [
  "assumptions",
  "demand_curves",
  "allocator",
  "launch_capacity",
  "customer_launch",
  "starlink",
  "starlink_capacity",
  "ai_stack",
  "lunar_mars",
  "opex",
  "capex",
  "group_pnl",
  "valuation",
] as const;

export const MOCK_SHEETS = [
  {
    slug: "assumptions",
    display_name: "Assumptions",
    source_sheet: "Assumptions",
    row_count: 525,
    col_count: 36,
    lifecycle_stage: "input",
    enabled: true,
  },
  {
    slug: "demand_curves",
    display_name: "Demand Curves",
    source_sheet: "Demand Curves",
    row_count: 134,
    col_count: 36,
    lifecycle_stage: "demand",
    enabled: true,
  },
  {
    slug: "allocator",
    display_name: "Allocator",
    source_sheet: "Cash Allocation Engine",
    row_count: 124,
    col_count: 31,
    lifecycle_stage: "allocation",
    enabled: true,
  },
  {
    slug: "launch_capacity",
    display_name: "Launch Capacity",
    source_sheet: "Vehicle Build",
    row_count: 93,
    col_count: 31,
    lifecycle_stage: "allocation",
    enabled: true,
  },
  {
    slug: "customer_launch",
    display_name: "Customer Launch",
    source_sheet: "Customer Launch",
    row_count: 125,
    col_count: 31,
    lifecycle_stage: "output",
    enabled: true,
  },
  {
    slug: "starlink",
    display_name: "Starlink",
    source_sheet: "Starlink",
    row_count: 166,
    col_count: 29,
    lifecycle_stage: "output",
    enabled: true,
  },
  {
    slug: "starlink_capacity",
    display_name: "Starlink Capacity",
    source_sheet: "Starlink",
    row_count: 35,
    col_count: 29,
    lifecycle_stage: "output",
    enabled: true,
  },
  {
    slug: "ai_stack",
    display_name: "AI Stack",
    source_sheet: "AI - Compute",
    row_count: 230,
    col_count: 29,
    lifecycle_stage: "output",
    enabled: true,
  },
  {
    slug: "lunar_mars",
    display_name: "Lunar Mars",
    source_sheet: "Lunar - Mars",
    row_count: 98,
    col_count: 32,
    lifecycle_stage: "output",
    enabled: true,
  },
  {
    slug: "opex",
    display_name: "OpEx",
    source_sheet: "Group P&L",
    row_count: 19,
    col_count: 29,
    lifecycle_stage: "pnl",
    enabled: true,
  },
  {
    slug: "capex",
    display_name: "CapEx",
    source_sheet: "Group P&L",
    row_count: 7,
    col_count: 29,
    lifecycle_stage: "pnl",
    enabled: true,
  },
  {
    slug: "group_pnl",
    display_name: "Group P&L",
    source_sheet: "Group P&L",
    row_count: 92,
    col_count: 56,
    lifecycle_stage: "pnl",
    enabled: true,
  },
  {
    slug: "valuation",
    display_name: "Valuation",
    source_sheet: "SoTP - Valuation",
    row_count: 89,
    col_count: 29,
    lifecycle_stage: "valuation",
    enabled: true,
  },
  {
    slug: "run_audit",
    display_name: "Run Audit",
    source_sheet: "Run Audit",
    row_count: 0,
    col_count: 0,
    lifecycle_stage: "conservation",
    enabled: true,
    is_run_audit: true,
  },
];

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
    starlink: ARTIFACT.audit_grids.starlink,
  },
};

/** Stub cell — matches production contract: grid value present, traced value null (F2). */
const MOCK_STUB_LINEAGE = {
  key: "grid.starlink.R11.2030",
  display_name: "Starlink BB Revenue from curve ($mm)",
  module_path: "calc.starlink.module",
  function: "compute_revenue",
  excel_cell: "R11",
  excel_label: "Starlink BB Revenue from curve ($mm)",
  architecture_ref: "§8.4",
  principle: "Principle 8",
  input_labels: [],
  cell_address: { sheet: "Starlink", row: "R11", column: "2030", year: 2030 },
  cell_kind: "stub",
  unit: "dollars_mm",
  formula_expression:
    "Starlink BB Revenue from curve ($mm) — see Architecture §8 Starlink module",
  resolved_inputs: [],
  computed_value: null,
  xlsx_cached_value: null,
  divergence_status: "n_a",
  lifecycle_stage: "output",
  section_ref: "§8 — Starlink module",
  upstream: [],
  downstream: [],
  sources: {
    methodology: {
      spec_section: "§8",
      principle: "Principle 8",
      rule: "Stub — not yet ported",
      module: "calc.starlink.module",
    },
  },
};

/** Derived cell with traced formula + inputs (F2 acceptance sample). */
const MOCK_DERIVED_LINEAGE = {
  key: "group.group_revenue_net",
  display_name: "Group Revenue ($mm)",
  module_path: "calc.group_pnl",
  function: "compute_group_revenue",
  excel_cell: "R14",
  excel_label: "Group Revenue ($mm)",
  architecture_ref: "§9.2",
  principle: "Principle 9",
  input_labels: ["Starlink module revenue", "Customer Launch revenue"],
  cell_address: { sheet: "Group P&L", row: "R14", column: "2026", year: 2026 },
  cell_kind: "derived",
  unit: "dollars_mm",
  formula_expression: "Group Revenue = Σ module revenues − inter-module eliminations",
  resolved_inputs: [
    {
      label: "Starlink module revenue",
      cell_address: "Starlink!R88:2026",
      value: 4200,
      unit: "dollars_mm",
      lineage_key: "starlink.module_revenue.2026",
    },
    {
      label: "Customer Launch revenue",
      cell_address: "Customer Launch!R81:2026",
      value: 3100,
      unit: "dollars_mm",
      lineage_key: "customer_launch.revenue.2026",
    },
  ],
  computed_value: 18116,
  xlsx_cached_value: 18116,
  divergence_status: "match",
  lifecycle_stage: "pnl",
  section_ref: "§9.2 — Group roll-up",
  upstream: [
    { key: "starlink.module_revenue.2026", label: "Starlink!R88 · Module revenue" },
    { key: "customer_launch.revenue.2026", label: "Customer Launch!R81 · Revenue" },
  ],
  downstream: [],
  sources: {
    methodology: {
      spec_section: "§9.2",
      principle: "Principle 9",
      rule: "Rule 31",
      module: "calc.group_pnl.compute_group_revenue",
    },
  },
};

const MOCK_GRAPH_DERIVED = {
  root_key: "group.group_revenue_net",
  depth: 2,
  nodes: [
    {
      id: "group.group_revenue_net",
      type: "auditCell",
      position: { x: 280, y: 40 },
      data: {
        key: "group.group_revenue_net",
        label: "Group Revenue",
        subtitle: "Group P&L!R14 · 2026",
        sheet: "Group P&L",
        row: "R14",
        year: 2026,
        active: true,
      },
    },
    {
      id: "starlink.module_revenue.2026",
      type: "auditCell",
      position: { x: 0, y: 0 },
      data: {
        key: "starlink.module_revenue.2026",
        label: "Starlink module revenue",
        subtitle: "Starlink!R88 · 2026",
        sheet: "Starlink",
        row: "R88",
        year: 2026,
        active: false,
      },
    },
    {
      id: "customer_launch.revenue.2026",
      type: "auditCell",
      position: { x: 0, y: 80 },
      data: {
        key: "customer_launch.revenue.2026",
        label: "Customer Launch revenue",
        subtitle: "Customer Launch!R81 · 2026",
        sheet: "Customer Launch",
        row: "R81",
        year: 2026,
        active: false,
      },
    },
  ],
  edges: [
    {
      id: "e-starlink-group",
      source: "starlink.module_revenue.2026",
      target: "group.group_revenue_net",
    },
    {
      id: "e-cl-group",
      source: "customer_launch.revenue.2026",
      target: "group.group_revenue_net",
    },
  ],
};

/** Assert every row unit in patched artifact is in the allowed enum. */
export function assertArtifactUnitCoverage(): void {
  const allowed = new Set<string>(GRID_UNITS);
  for (const [slug, grid] of Object.entries(ARTIFACT.audit_grids)) {
    for (const row of grid.rows) {
      if (!allowed.has(row.unit)) {
        throw new Error(`Unknown unit "${row.unit}" on ${slug} ${row.row_id}`);
      }
    }
  }
}

export async function installMockApi(page: Page) {
  assertArtifactUnitCoverage();

  await page.route("**/data/base_case_run.json", async (route) => {
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(ARTIFACT),
    });
  });

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
      return json({ status: "ok", git_sha: ARTIFACT.git_sha });
    }
    if (path === "/scenarios") {
      return json([
        { name: "base_case", description: "Base", path: "scenarios/base_case.yaml" },
        { name: "bear", description: "Bear", path: "scenarios/bear.yaml" },
      ]);
    }
    if (path === "/sheets") {
      return json(MOCK_SHEETS);
    }
    if (path.startsWith("/sheets/") && path.endsWith("/grid")) {
      const slug = path.split("/")[2] ?? "starlink";
      const grid = ARTIFACT.audit_grids[slug];
      return json(grid ?? MOCK_RUN.audit_grids.starlink);
    }
    if (path === "/runs/deterministic" && route.request().method() === "POST") {
      const body = route.request().postDataJSON() as { scenario?: string } | undefined;
      return json({
        ...MOCK_RUN,
        scenario: body?.scenario ?? "base_case",
        run_id: body?.scenario === "bear" ? "e2e_bear_run" : MOCK_RUN.run_id,
      });
    }
    if (path.match(/^\/runs\/[^/]+\/audit-dashboard/)) {
      return json(ARTIFACT.run_audit);
    }
    if (path.startsWith("/lineage/") && !path.includes("/history") && !path.includes("/graph")) {
      const key = decodeURIComponent(path.split("/lineage/")[1]?.split("/")[0] ?? "");
      if (key === "group.group_revenue_net" || key.includes("group_revenue")) {
        return json({ ...MOCK_DERIVED_LINEAGE, key });
      }
      if (key.includes("R12") || key.includes("DTC")) {
        return json({
          ...MOCK_STUB_LINEAGE,
          key,
          display_name: "Starlink DTC Revenue from curve ($mm)",
          excel_label: "Starlink DTC Revenue from curve ($mm)",
          excel_cell: "R12",
          cell_address: { sheet: "Starlink", row: "R12", column: "2030", year: 2030 },
        });
      }
      return json({ ...MOCK_STUB_LINEAGE, key });
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
      const key = decodeURIComponent(path.split("/lineage/")[1]?.split("/")[0] ?? "");
      if (key === "group.group_revenue_net" || key.includes("group_revenue")) {
        return json(MOCK_GRAPH_DERIVED);
      }
      return json({ root_key: key, depth: 2, nodes: [], edges: [] });
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
