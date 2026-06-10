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

/** Sprint 6 — instant base-case MC distribution (matches e2e percentile assertions). */
export const MOCK_MC_AGGREGATION = {
  n_trials: 5000,
  n_converged: 4988,
  base_seed: 42,
  convergence_status: "converged",
  metrics: {
    group_ev_2025_b: {
      metric: "group_ev_2025_b",
      p5: 220,
      p10: 235,
      p25: 255,
      p50: 278,
      p75: 302,
      p90: 318,
      p95: 340,
      mean: 279,
      std: 42,
      cvar_5: 205,
      base_case: 278,
    },
  },
  group_ev_histogram: {
    metric: "group_ev_2025_b",
    n_bins: 10,
    bin_edges: [180, 196, 212, 228, 244, 260, 276, 292, 308, 324, 360],
    counts: [12, 45, 120, 280, 420, 510, 380, 150, 55, 16],
  },
  group_fcf_fan: {
    years: [2025, 2026, 2027, 2028, 2029, 2030, 2035, 2040],
    p5: [800, 850, 900, 950, 1000, 1050, 1400, 1800],
    p25: [950, 1000, 1050, 1100, 1150, 1200, 1600, 2100],
    p50: [1100, 1150, 1200, 1250, 1300, 1350, 1850, 2400],
    p75: [1250, 1300, 1350, 1400, 1450, 1500, 2100, 2700],
    p95: [1400, 1450, 1500, 1550, 1600, 1650, 2350, 3000],
    base_case: [1000, 1200, 1300, 1400, 1450, 1500, 2000, 2600],
  },
};

const MOCK_MC_TORNADO = [
  {
    label: "TAM inflation rate",
    low_ev: 240,
    high_ev: 310,
    base_ev: 278,
    delta: 35,
  },
  {
    label: "Starlink ARPU",
    low_ev: 250,
    high_ev: 300,
    base_ev: 278,
    delta: 25,
  },
];

export const MOCK_MC_ARTIFACT = {
  git_sha: ARTIFACT.git_sha,
  scenario: "base_case",
  job_id: "precache",
  run_id: "e2e_mc_precache",
  trials: 5000,
  base_seed: 42,
  trials_completed: 5000,
  trials_converged: 4988,
  n_trials: 5000,
  n_converged: 4988,
  convergence_status: "converged",
  aggregation: MOCK_MC_AGGREGATION,
  tornado: MOCK_MC_TORNADO,
};

const mcJobPolls = new Map<string, number>();

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
  stub_spec_section: "§8.4",
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
      spec_section: "§8.4",
      method_statement: "Planned implementation per Architecture §8.4",
      principle: "Principle 8",
      rule: "Not yet implemented — placeholder tab",
    },
  },
};

/** Headline module FCF — Audit MC panel (Sprint 7). */
const MOCK_MODULE_FCF_LINEAGE = {
  key: "module.starlink.module_fcf",
  display_name: "Module FCF ($mm)",
  module_path: "calc.starlink.module",
  function: "compute_module_fcf",
  excel_cell: "R106",
  excel_label: "Module FCF ($mm)",
  architecture_ref: "§8.4",
  principle: "Principle 8",
  input_labels: ["Module EBITDA", "Module CapEx"],
  cell_address: { sheet: "Starlink", row: "R106", column: "2026", year: 2026 },
  cell_kind: "derived",
  unit: "dollars_mm",
  formula_expression: "Module FCF = Module EBITDA − Module CapEx + D&A add-back",
  resolved_inputs: [
    {
      label: "Module EBITDA",
      cell_address: "Starlink!R102:2026",
      value: 2100,
      unit: "dollars_mm",
      lineage_key: "module.starlink.module_ebitda",
    },
  ],
  computed_value: 1372.86,
  xlsx_cached_value: 1372.86,
  divergence_status: "match",
  lifecycle_stage: "pnl",
  section_ref: "§8 — Starlink module",
  upstream: [],
  downstream: [],
  sources: {
    methodology: {
      spec_section: "§8.4",
      method_statement: "Module EBITDA − CapEx + D&A add-back (pre-tax, pre-corp)",
      principle: "Principle 8",
      rule: "Rule 8 — Module FCF excludes taxes, SG&A, and corporate overhead",
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
      method_statement: "Σ module gross revenues minus inter-module elimination rows",
      principle: "Principle 9",
      rule: "Rule 9 — Internal transfers eliminate only at Group P&L",
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

  await page.route("**/data/*_run.json", async (route) => {
    const url = route.request().url();
    const scenario = url.match(/\/([^/]+)_run\.json/)?.[1] ?? "base_case";
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({ ...ARTIFACT, scenario }),
    });
  });

  await page.route("**/data/*_mc.json", async (route) => {
    const url = route.request().url();
    const scenario = url.match(/\/([^/]+)_mc\.json/)?.[1] ?? "base_case";
    return route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        ...MOCK_MC_ARTIFACT,
        scenario,
        aggregation: MOCK_MC_AGGREGATION,
        tornado: MOCK_MC_TORNADO,
      }),
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
      return json({
        status: "ok",
        git_sha: ARTIFACT.git_sha,
        workbook_name: "SpaceX V4.131.xlsx",
        workbook_mtime: 1_718_000_000,
        serverless: true,
        custom_mc_enabled: false,
        precached_scenarios: ["base_case", "bear", "bull", "mars_share"],
        precache_mc_trials: 5000,
      });
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
      if (key === "module.starlink.module_fcf" || key.includes("module_fcf")) {
        return json({ ...MOCK_MODULE_FCF_LINEAGE, key });
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
        key: "group.group_revenue_net",
        total: 2,
        entries: [
          {
            date: "2026-06-05",
            commit_sha: "V4.114-synthetic.xlsx",
            title: "Value updated — V4.114-synthetic.xlsx 2030",
            change_kind: "value",
            effect_on_cell: { before: 12000, after: 12100, delta: 100 },
          },
          {
            date: "2026-06-04",
            commit_sha: "V4.113.xlsx",
            title: "First ingest — V4.113.xlsx 2030",
            change_kind: "initial",
            effect_on_cell: { before: null, after: 12000, delta: null },
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
        {
          id: "bear",
          name: "Bear",
          description: "Bear",
          key_inputs: [],
          group_ev_2025_b: 210,
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
    if (path === "/runs/mc" && route.request().method() === "POST") {
      const body = route.request().postDataJSON() as { trials?: number; scenario?: string };
      const jobId = `e2e_mc_${body?.scenario ?? "base_case"}_${Date.now()}`;
      mcJobPolls.set(jobId, 0);
      return json({ job_id: jobId, status: "queued" });
    }
    if (path.match(/^\/runs\/mc\/[^/]+\/distribution$/)) {
      const jobId = path.split("/")[3] ?? "unknown";
      return json({
        job_id: jobId,
        scenario: "bear",
        n_trials: 2000,
        n_converged: 1990,
        base_seed: 42,
        convergence_status: "converged",
        group_ev_histogram: MOCK_MC_AGGREGATION.group_ev_histogram,
        group_fcf_fan: MOCK_MC_AGGREGATION.group_fcf_fan,
        metrics: MOCK_MC_AGGREGATION.metrics,
      });
    }
    if (path.match(/^\/runs\/mc\/[^/]+$/) && route.request().method() === "GET") {
      const jobId = path.split("/")[3] ?? "unknown";
      if (jobId === "precache") {
        return json({
          job_id: jobId,
          status: "completed",
          result: {
            scenario: "base_case",
            n_trials: MOCK_MC_ARTIFACT.n_trials,
            n_converged: MOCK_MC_ARTIFACT.n_converged,
            base_seed: MOCK_MC_ARTIFACT.base_seed,
            convergence_status: MOCK_MC_ARTIFACT.convergence_status,
            aggregation: MOCK_MC_AGGREGATION,
            tornado: MOCK_MC_TORNADO,
          },
        });
      }
      const polls = (mcJobPolls.get(jobId) ?? 0) + 1;
      mcJobPolls.set(jobId, polls);
      const total = 2000;
      const done = polls < 2 ? 400 : total;
      if (done < total) {
        return json({
          job_id: jobId,
          status: "running",
          progress: { trials_done: done, trials: total },
        });
      }
      return json({
        job_id: jobId,
        status: "completed",
        result: {
          scenario: "bear",
          n_trials: total,
          n_converged: 1990,
          base_seed: 42,
          convergence_status: "converged",
          aggregation: MOCK_MC_AGGREGATION,
          tornado: MOCK_MC_TORNADO,
        },
      });
    }

    return route.continue();
  });
}
