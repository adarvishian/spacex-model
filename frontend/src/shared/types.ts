export type Scenario = {
  name: string;
  description: string;
  path: string;
};

export type SheetMeta = {
  slug: string;
  display_name: string;
  source_sheet: string;
  row_count: number;
  col_count: number;
  lifecycle_stage: LifecycleStage;
  enabled: boolean;
};

export type LifecycleStage =
  | "input"
  | "demand"
  | "allocation"
  | "output"
  | "pnl"
  | "conservation"
  | "valuation";

export type CellKind = "input" | "derived" | "anchor" | "stub";
export type DivergenceStatus = "match" | "drift" | "intentional" | "n_a";

export type GridRow = {
  row_id: string;
  row_index: number;
  label: string;
  section_ref: string;
  unit: string;
  base_case_value: number | null;
  year_values: (number | null)[];
  cell_kinds: CellKind[];
  divergence_flags: DivergenceStatus[];
  lineage_keys: string[];
  is_header: boolean;
};

export type GridPayload = {
  sheet: string;
  source_sheet: string;
  years: number[];
  rows: GridRow[];
};

export type ResolvedInput = {
  label: string;
  cell_address: string;
  value: number | null;
  unit: string;
  lineage_key: string;
};

export type LineageEntry = {
  key: string;
  display_name: string;
  module_path: string;
  function: string;
  excel_cell: string;
  excel_label: string;
  architecture_ref: string;
  principle: string;
  input_labels: string[];
  cell_address?: {
    sheet: string;
    row: string;
    column: string;
    year?: number;
  };
  cell_kind?: CellKind;
  unit?: string;
  formula_expression?: string;
  resolved_inputs?: ResolvedInput[];
  computed_value?: number | null;
  xlsx_cached_value?: number | null;
  divergence_status?: DivergenceStatus;
  divergence_delta_mm?: number | null;
  lifecycle_stage?: LifecycleStage;
  section_ref?: string;
  upstream_keys?: string[];
  downstream_keys?: string[];
  upstream?: Array<{ key: string; label: string }>;
  downstream?: Array<{ key: string; label: string }>;
  sources?: {
    input_provenance?: { source: string; reference: string; url?: string };
    methodology: { spec_section: string; principle: string; rule: string };
    calibration_anchor?: { target: number; tolerance_pct: number; basis: string };
  };
};

export type DeterministicRun = {
  run_id: string;
  scenario: string;
  cached: boolean;
  audit?: Record<string, unknown>;
  solver: { iterations: number; converged: boolean; max_residual: number };
  valuation: {
    group_ev_2025_b: number;
    lineage_key: string;
    group_wacc?: number;
    terminal_growth?: number;
  };
  group?: Record<string, unknown>;
  modules?: Record<string, unknown>;
  module_ev?: Record<string, unknown>;
  override_warnings: { label: string; value: string; message: string }[];
  conservation?: { all_ok: boolean };
};

export type ActiveCell = {
  rowId: string;
  rowIndex: number;
  label: string;
  year: number;
  yearIndex: number;
  lineageKey: string;
  unit: string;
  cellKind: CellKind;
};
