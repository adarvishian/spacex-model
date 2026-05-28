# Frontend PRD — Mach33 SpaceX Valuation Model

**Document version:** 1.0
**Date:** 2026-05-28
**Author:** Dr. Marcus Hale (port lead)
**Status:** Draft for review. Companion to `PRD.md` (v1) and `context.md` §5.4.

**Companion documents (read order):**

1. `role.md` — operating persona.
2. `context.md` — living project context; §5.4 defines the original web UI scope this PRD expands.
3. `PRD.md` §17 — backlog list this PRD operationalizes.
4. `docs/model_translation_log.csv` — the lineage index the Audit Tab reads from.
5. `docs/DEV_LOG.md` — append-only change log; this PRD's Sources panel surfaces entries here.
6. `frontend/src/App.tsx`, `frontend/src/api.ts` — v0 baseline this PRD extends.

---

## §1 — Purpose & Scope

### §1.1 Purpose

The v0 frontend (`frontend/src/App.tsx`) ships the minimum surface area context.md §5.4 specified: scenario picker, EV/FCF panels, tornado, a click-to-open lineage drawer. It is sufficient for engineering-internal validation but not for the two real audiences:

- **Internal model auditors** (Vlad, Dr. Hale, future model-risk reviewers) need to verify every cell — its derivation, inputs, history of change, and where it sits in the larger model graph — with the fluency of operating in Excel.
- **Clients** need a clean, opinionated view that hides model machinery and lets them export defensible scenario tables to xlsx.

This PRD specifies the v1.5 frontend that serves both audiences from a single codebase with a hard mode switch.

### §1.2 In scope

- **Audit Mode** (internal):
  - Excel-style grid tab per source sheet (Assumptions, Allocator, Customer Launch, Starlink, etc.) with year columns 2025–2050.
  - Cell click → derivation panel showing the formula, resolved inputs, intermediate values, and a flow diagram of upstream dependencies.
  - Right-rail **Minimap** showing where the active cell sits in the 15-sheet model, updating on cell click and tab change.
  - **Sources & Change History** panel per cell: input provenance (S-1 ref, Q4'25 anchor, MC range), why-this-value entries from `DEV_LOG.md`, and timestamps for assumption / formula / output deltas.
- **Client Mode** (external):
  - Curated scenario picker (Base / Bear / Bull / Custom).
  - Headline outputs (Group EV, per-module EV, FCF) with plain-language captions.
  - Custom-scenario builder gated to a vetted subset of MC-variable inputs.
  - One-click xlsx download of the active scenario's results.
- Hard mode switch (URL-routed `/audit` vs `/client`); the mode is also an auth boundary in production.

### §1.3 Out of scope (defer to v2)

- Cell **editing** in the Audit grid (read-only; overrides happen via the scenario sidebar).
- Multi-user collaboration / comments / annotations.
- Mobile / tablet layouts (desktop ≥ 1440px target).
- Real-time co-watching of MC progress.
- Historical model-version comparison views (one canonical model per context.md §3.11).
- Saved client workspaces beyond URL-shareable scenario state.

### §1.4 Success criteria

1. An auditor can verify any one of the ~10,900 derived values by clicking exactly one cell and reading the derivation panel — no source-code lookup required.
2. The Minimap correctly indicates the active cell's tab, section, and one of seven canonical lifecycle stages (Input → Demand → Allocation → Output → P&L → Conservation → Valuation) within 100 ms of any cell click.
3. Every cell exposes at least one **Source** entry (input provenance or `DEV_LOG.md` reference) and a complete **Change History** since the first commit that produced its current value.
4. A client with no model context can run a custom scenario and download its xlsx in under 3 minutes, with no error states that require engineering intervention.
5. The Audit grid renders a 26-column × ~350-row sheet at ≥ 55 fps on a 2022 MacBook Pro.

---

## §2 — Personas & Top User Journeys

### §2.1 Personas

**P1 — Vlad (Principal, sign-off).** Reviews calibration runs weekly. Lives in the Audit Tab. Lands on a flagged cell from a reconciliation report, expects the derivation panel and Sources to answer "why does 2050 Group FCF land at −$90B" without leaving the page.

**P2 — Dr. Hale (Port lead / model-risk reviewer).** Spends most time in Audit Mode triaging xlsx-vs-code divergences (`context.md §11.6`). Needs to compare a single cell to its V2.16 cached value, see the chain of upstream cells, and link directly to the spec section.

**P3 — Future model-risk auditor (institutional).** Doesn't know the codebase. Must reach numerical sign-off using only the UI + the architecture spec. Treats the Audit Tab the way they treat an Excel workbook in a model review — they want familiar muscle memory (click cell, see formula bar, follow precedents).

**P4 — Institutional client (read-only).** Lands in Client Mode. Selects a scenario, optionally adjusts 3–5 vetted inputs (Mars share, Starship $/kg learning, ODC Pr(A)), downloads xlsx. Never sees a formula.

**P5 — Mach33 client-success lead.** Walks clients through Client Mode in screenshare. Needs the experience to be self-explanatory; needs a "share link" that captures the client's custom scenario state.

### §2.2 Top user journeys

| # | Persona | Journey | Primary surface |
|---|---|---|---|
| J1 | Vlad | "Why is Group FCF 2027 = $X?" | Audit Tab → Group P&L sheet → click cell → derivation + minimap |
| J2 | Dr. Hale | Triage Block C divergence on Customer Launch IRR 2030 | Audit Tab → CL sheet → click → derivation → Sources (DEV_LOG entry on Block C accepted) |
| J3 | Auditor | Verify R108 conservation holds 2025–2050 | Audit Tab → Group P&L → R108 row, scan + click any failing year |
| J4 | Client | Run a bullish Starship learning scenario | Client Mode → Bull preset → adjust Starship $/kg → download xlsx |
| J5 | Client-success lead | Send client a saved custom scenario | Client Mode → Configure → "Copy share link" |

---

## §3 — Information Architecture

### §3.1 Mode switch

```
/audit    → Audit Mode shell (sheet tabs + grid + derivation + minimap + sources)
/client   → Client Mode shell (scenario picker + headline panels + xlsx export)
/         → redirects based on the auth profile's `role` claim (auditor → /audit, client → /client)
```

The two modes share the same FastAPI backend (`/api/...`). Client Mode calls a strict subset; Audit Mode calls everything plus the new endpoints in §6.

### §3.2 Audit Mode layout (desktop, ≥ 1440px)

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ Header: Mach33 SpaceX Model · scenario [Base ▾] · run id · build sha · [Switch mode] │
├──────────────────┬───────────────────────────────────────────┬──────────────────────┤
│  SHEET TABS      │                                           │  MINIMAP             │
│  ───────────     │            EXCEL-STYLE GRID               │  ───────────────     │
│  • Assumptions   │  ┌────┬─────────┬──────┬──────┬──────┐    │  ┌────────────────┐  │
│  • Allocator     │  │    │ Label   │ 2025 │ 2026 │ ...  │    │  │   Sheet map    │  │
│  • Launch Cap.   │  ├────┼─────────┼──────┼──────┼──────┤    │  │  (15 cells)    │  │
│  • Customer Lnch │  │ R8 │ Revenue │ 14.6 │ 18.2 │ ...  │    │  │  ▣ active sheet│  │
│  • Starlink   ←  │  │ R9 │ COGS    │  5.9 │  7.3 │ ...  │    │  └────────────────┘  │
│  • Starlink Cap. │  │R10 │ GP      │  8.7 │ 10.9*│ ...  │    │                      │
│  • ODC           │  └────┴─────────┴──────┴──────┴──────┘    │  Lifecycle stage:    │
│  • AI Stack      │                  ▲ active cell             │   Input · Demand     │
│  • Lunar Mars    │  ┌─────────────────────────────────────┐   │   Alloc · Output     │
│  • Group P&L     │  │  DERIVATION PANEL (active cell)     │   │   P&L · Conserv.     │
│  • OpEx          │  │  Formula:  GP = Revenue − COGS      │   │   ▣ Valuation        │
│  • CapEx         │  │  Inputs:  Revenue 2025 = 14,650     │   │                      │
│  • Valuation     │  │           COGS    2025 =  5,960     │   │  Section in sheet:   │
│  • Demand Curves │  │  Result:  8,690                     │   │  §6.3 Sigmoid cash   │
│  • Run Audit     │  │  Cached xlsx: 8,690 ✓ match        │   │                      │
│                  │  │  [Show dependency graph ▾]          │   │  Upstream sheets:    │
│  Scenario:       │  └─────────────────────────────────────┘   │   ◯ Allocator        │
│  [Base Case  ▾]  │                                            │   ◯ Launch Capacity  │
│  Overrides: 0    │  ┌─────────────────────────────────────┐   │  Downstream sheets:  │
│  [Re-run]        │  │  SOURCES & CHANGE HISTORY           │   │   ◯ Group P&L        │
│                  │  │  Spec ref: Architecture §15.2 R100  │   │   ◯ Valuation        │
│                  │  │  Module:   calc.group_pnl.compute_  │   │                      │
│                  │  │            group_ebitda             │   │                      │
│                  │  │  Inputs:   • Customer Launch rev    │   │                      │
│                  │  │              (S-1 P&L, p. F-12)     │   │                      │
│                  │  │            • Starlink BB rev        │   │                      │
│                  │  │              (Q4'25 anchor)         │   │                      │
│                  │  │  Last change: 2026-05-26 (Sprint    │   │                      │
│                  │  │  11e) — see DEV_LOG entry           │   │                      │
│                  │  └─────────────────────────────────────┘   │                      │
└──────────────────┴───────────────────────────────────────────┴──────────────────────┘
```

### §3.3 Client Mode layout

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  Mach33 · SpaceX Valuation                                       [Switch to Audit]   │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   Scenario:  ◉ Base   ◯ Bear   ◯ Bull   ◯ Custom…                                   │
│                                                                                      │
│   ┌─────────── HEADLINE ──────────────────────────────────────────────────────┐      │
│   │  Group Equity Value (2025):   $278 B                                      │      │
│   │  Sum-of-parts (per module):   bar chart                                   │      │
│   │  Group FCF profile:           sparkline 2025 → 2050                       │      │
│   └──────────────────────────────────────────────────────────────────────────┘      │
│                                                                                      │
│   ┌─── Per-module summary ───┐   ┌─── Custom scenario builder ────────────────┐     │
│   │  Customer Launch    $42B │   │  Mars carve-out share         [ 0.05  ▾]  │     │
│   │  Starlink         $164B  │   │  Starship $/kg (2030 anchor)  [ 1,200 ]   │     │
│   │  ODC                 $0  │   │  ODC Pr(A) dual revenue       [ 0.40  ▾]  │     │
│   │  AI Stack            $0  │   │  Wright's Law learning rate   [ 0.22  ▾]  │     │
│   │  Lunar Mars          $8B │   │  …                                        │     │
│   └──────────────────────────┘   │  [Run scenario]   [Reset]                 │     │
│                                  └────────────────────────────────────────────┘     │
│                                                                                      │
│   ┌──────────── Downloads ─────────────────────────────────────────────────┐         │
│   │  ⬇  Active scenario (xlsx)                                             │         │
│   │  ⬇  Scenario pack — Base + Bear + Bull (xlsx)                          │         │
│   │  ⬇  Methodology one-pager (pdf)                                        │         │
│   └────────────────────────────────────────────────────────────────────────┘         │
│                                                                                      │
│   "Share this scenario:  https://…/?s=eyJtYXJzX3Bj…"                                │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## §4 — Audit Tab Specification

### §4.1 Sheet tabs

One tab per source sheet in the Excel inventory (`context.md §2.2`):

| Tab | Source sheet | Cell count (cap) |
|---|---|---:|
| Assumptions | Assumptions | 350 rows × 36 cols |
| Allocator | Allocator | 171 × 31 |
| Launch Capacity | Launch Capacity | 80 × 29 |
| Customer Launch | Customer Launch | 210 × 31 |
| Starlink | Starlink | 235 × 29 |
| Starlink Capacity | Starlink Capacity | 50 × 29 |
| ODC | ODC | 210 × 29 |
| AI Stack | AI Stack | 210 × 29 |
| Lunar Mars | Lunar Mars | 212 × 32 |
| Group P&L | Group P&L | 125 × 56 |
| OpEx | OpEx | 60 × 29 |
| CapEx | CapEx | 47 × 29 |
| Valuation | Valuation | 6 × 29 |
| Demand Curves | Demand Curves | 145 × 36 |
| Run Audit | derived from `audit_log.py` | dynamic |

Tabs render eagerly for visited sheets, lazily for unvisited. The active tab key is reflected in the URL: `/audit/starlink?row=R8&col=2026`.

### §4.2 Grid component

**Library choice:** `ag-grid-community` v32 or `glide-data-grid`. Both handle 26 × 350 with no virtualization regression and support custom cell renderers, sticky headers, and keyboard nav. Decision logged in §11.

**Columns:** A (label), B (Base Case scalar), C (notes/source), D–AC (years 2025–2050). Frozen left columns A–C and frozen header row.

**Cell renderer:**
- Numeric cells: right-aligned, scaled per row unit (`$mm`, `%`, `count`).
- Cells that are inputs (from Assumptions): light blue background.
- Cells that are derived: white background.
- Cells that diverge from V2.16 cached value beyond §11.6 tolerance: amber border (`#F59E0B`).
- Cells with an open Sprint backlog item: orange dot in the top-right.
- The active cell: 2-px Mach33 indigo outline (`#4F46E5`).

**Selection model:** single cell selection (no ranges in v1; ranges in v2).

**Keyboard:** arrow keys move selection; `Enter` opens the derivation panel in expanded view; `Cmd-J` jumps to the upstream cell (first input listed); `Cmd-K` opens a label-search palette across all sheets.

### §4.3 Derivation panel

Anchored below the grid (resizable horizontal split, default 40% grid / 30% derivation / 30% sources). Contents per active cell:

1. **Address strip:** `Starlink!R10:E (2026)` · type: `derived (year-row)` · unit: `$mm`.
2. **Formula expression:** rendered from the lineage payload (see §6.2). Mirrors the Architecture spec syntax, not raw Python (e.g., `Module EBITDA = Revenue − COGS`).
3. **Resolved inputs table:**

   | Input | Source cell | Resolved value | Lineage |
   |---|---|---:|---|
   | Revenue 2026 | `Starlink!R8:E` | 18,210 | [open ↗] |
   | COGS 2026 | `Starlink!R9:E` | 7,310 | [open ↗] |

4. **Computed value:** the result, with the V2.16 cached value adjacent and a status pill (`match` / `divergence Δ X mm` / `intentional divergence — see §11.6`).
5. **Dependency graph (collapsible):** see §4.4.

### §4.4 Dependency flow diagram

Inline interactive diagram showing the upstream graph rooted at the active cell, 2 levels deep by default with an "expand" affordance per leaf.

**Library:** `react-flow` (xyflow). Each node is a cell; each edge is a "consumed by" relation derived from the lineage `input_labels` array (already in v0 `LineageEntry`).

```
   ┌──────────────────────┐         ┌─────────────────────┐
   │ Assumptions!B Mars % │────┐    │ Allocator!D8 Cash   │
   └──────────────────────┘    │    │ BoY                 │
                               ▼    └─────────┬───────────┘
                       ┌─────────────────────┐│
                       │ Allocator!D## Mars  │┼──┐
                       │ carveout            ││  │
                       └─────────┬───────────┘│  │
                                 ▼            │  │
                          ┌────────────────────▼──▼──────┐
                          │  GROUP P&L R##  Group FCF    │  ← active cell
                          │  2026 = $X,XXX mm            │
                          └──────────────────────────────┘
```

Node click navigates the grid to that cell (URL update + grid scroll + active-cell change). Edge hover shows the consuming function and the architecture-spec section. Diagrams are pure SVG (no canvas) so they remain accessible and exportable as static images on right-click.

### §4.5 Run Audit tab

A dynamic tab populated from `io/audit_log.py`. Shows the current run's:

- Solver convergence (iterations, max residual, damping).
- Conservation block R99–R108 results per year, colored green / red.
- 2025 calibration anchors vs targets table (mirrors `tests/reconciliation/test_calibration_2025.py`).
- Divergence triage list against V2.16 (top 50 by absolute Δ, with §11.6 disposition).
- Link to download the full audit log as JSON.

---

## §5 — Minimap (Right Rail)

### §5.1 Purpose

Persistent context: where am I in the model, what feeds this section, what depends on it. The minimap is the navigational equivalent of Excel's sheet-tab strip combined with a model-graph view.

### §5.2 Anatomy

```
┌──────────────────────┐
│   MODEL MAP          │
├──────────────────────┤
│  Inputs              │
│   ▣ Assumptions      │  ← if active sheet feeds from Assumptions
│                      │
│  Allocation          │
│   □ Allocator        │
│   □ Launch Capacity  │
│                      │
│  Modules             │
│   ▣ Customer Launch  │  ← active
│   □ Starlink         │
│   □ Starlink Cap.    │
│   □ ODC              │
│   □ AI Stack         │
│   □ Lunar Mars       │
│                      │
│  Cross-cutting       │
│   □ OpEx             │
│   □ CapEx            │
│   □ Group P&L        │
│                      │
│  Outputs             │
│   □ Valuation        │
├──────────────────────┤
│  LIFECYCLE STAGE     │
│   Input → Demand →   │
│   ▣ Allocation →     │
│   Output → P&L →     │
│   Conservation →     │
│   Valuation          │
├──────────────────────┤
│  SECTION IN SHEET    │
│   §4.2 — F9 cust.    │
│   launches           │
├──────────────────────┤
│  UPSTREAM (1-hop)    │
│   • Allocator!D54    │
│   • Launch Cap!D12   │
│  DOWNSTREAM (1-hop)  │
│   • Group P&L!R8     │
│   • Valuation!D6     │
└──────────────────────┘
```

### §5.3 Update behavior

The minimap recomputes on:
- Sheet-tab change (active sheet highlight only).
- Cell-selection change (lifecycle stage, section, upstream/downstream lists).

It does not require a server round-trip; the lineage payload returned by `/api/lineage/{key}` (§6.2) carries `lifecycle_stage`, `section_ref`, and the 1-hop upstream/downstream lists. The 15-sheet model graph is a static client-side asset (`frontend/src/data/sheet_graph.ts`) generated at build time from the spec.

### §5.4 Cross-sheet jump

Clicking an upstream or downstream entry navigates the grid to that cell (same behavior as a node click in the dependency diagram).

---

## §6 — Sources & Change History

### §6.1 What "Source" means per cell

Three orthogonal source dimensions, each surfaced as its own row group in the panel:

1. **Input provenance.** Only present for input cells (Assumptions tab and a small set of opening balances). Examples: "S-1 disclosure, page F-12, footnote 14", "Q4'25 anchor, 2025 Anchors from Q4_25.md §2", "Mach33 internal estimate — see DEV_LOG 2026-04-12".
2. **Methodology reference.** Required for every derived cell. Points to: the Architecture & Methodology spec section, the Principle / Rule, and the Python module + function (already in v0 lineage).
3. **Calibration anchor.** Optional. Present only when the cell has an external anchor it's tested against (e.g., 2025 Group Revenue → $14,650mm ± 5%).

### §6.2 What "Change History" means per cell

A reverse-chronological list of events that materially changed this cell's value, formula, or anchor since the first commit. Each event is one row:

```
2026-05-26  Sprint 11e merged                         (commit a1b2c3d)
            Formula refactor: split V2/V3 BB into separate allocator queues.
            Effect on this cell: 2030 value moved from 12,840 → 13,210 ($+370mm).
            Linked DEV_LOG: docs/DEV_LOG.md#sprint-11e-merge

2026-05-19  Anchor revision                            (commit f4e5d6c)
            Q4'25 Starlink BB anchor revised from $7,612mm → $7,852mm per
            Mach33 internal update.
            Effect on this cell: 2025 value moved from 7,610 → 7,852.
            Linked spec: 2025 Anchors from Q4_25.md §2

2026-05-12  Initial Sprint 7 port                       (commit 8a9b0c1)
            First derivation of this cell from the Architecture spec.
```

### §6.3 Where the data comes from

| Source type | System of record | Update cadence |
|---|---|---|
| Input provenance | `inputs/s1_2025_anchors.py`, `inputs/q4_25_anchors.py`, `Assumptions.notes` (column C of the source sheet) | Build time (ingest) |
| Methodology reference | `config/canonical_labels.py` + `docs/model_translation_log.csv` | Build time |
| Calibration anchor | `tests/reconciliation/test_calibration_2025.py` | Test discovery |
| Change history | `git log` over the file containing the function listed in lineage `module_path` + `function`, filtered to commits whose diff hunk overlaps the function body, intersected with `docs/DEV_LOG.md` parsed entries | API request time, cached 15 min |

Change history is computed lazily by a new backend endpoint `/api/lineage/{key}/history` so the audit-log table is not bloated. The first 3 entries are eager-loaded; "show all" expands the rest.

### §6.4 Backend: extended `LineageEntry`

The v0 `LineageEntry` (in `frontend/src/api.ts`) extends to:

```ts
type LineageEntry = {
  // existing v0 fields
  key: string;
  display_name: string;
  module_path: string;
  function: string;
  excel_cell: string;
  excel_label: string;
  architecture_ref: string;
  principle: string;
  input_labels: string[];

  // new in v1.5
  cell_address: { sheet: string; row: string; column: string; year?: number };
  cell_kind: "input" | "derived" | "anchor" | "stub";
  unit: "dollars_mm" | "pct" | "kg_to_leo" | "gbps" | "count" | "ratio";
  formula_expression: string;     // architecture-spec syntax, not Python
  resolved_inputs: Array<{
    label: string;
    cell_address: string;
    value: number;
    unit: string;
    lineage_key: string;
  }>;
  computed_value: number;
  xlsx_cached_value: number | null;
  divergence_status: "match" | "drift" | "intentional" | "n_a";
  divergence_delta_mm: number | null;
  lifecycle_stage:
    | "input"
    | "demand"
    | "allocation"
    | "output"
    | "pnl"
    | "conservation"
    | "valuation";
  section_ref: string;            // e.g., "§6.3 Sigmoid cash queue"
  upstream_keys: string[];        // 1-hop
  downstream_keys: string[];      // 1-hop
  sources: {
    input_provenance?: { source: string; reference: string; url?: string };
    methodology: { spec_section: string; principle: string; rule: string };
    calibration_anchor?: { target: number; tolerance_pct: number; basis: string };
  };
};
```

A separate endpoint serves history:

```ts
type ChangeHistoryEntry = {
  date: string;              // ISO 2026-05-26
  commit_sha: string;
  title: string;             // first line of commit msg
  change_kind: "formula" | "anchor" | "input" | "initial";
  effect_on_cell?: { before: number | null; after: number | null; delta: number | null };
  dev_log_anchor?: string;   // markdown anchor in DEV_LOG.md
};
```

---

## §7 — Client Mode Specification

### §7.1 Curated scenario picker

Three pre-built scenarios shipped with the app, read from `scenarios/*.yaml`:

- **Base Case** — `scenarios/base_case.yaml`.
- **Bear** — `scenarios/bear.yaml` (low Starship learning, high Mars %, low ODC Pr(A)).
- **Bull** — `scenarios/bull.yaml` (high Starship learning, low Mars %, ODC Pr(A) = 0.6).

Each scenario card shows: name, one-line description, the 3–5 inputs that differ from Base, and the resulting Group EV.

### §7.2 Custom scenario builder

A "Custom…" tile opens a form with a **vetted subset** of MC-variable inputs. v1.5 ships these (chosen for narrative clarity and bounded ranges):

| Input | Range | Default (Base) | Plain-language label |
|---|---|---:|---|
| `mars_pct` | 0.00 – 0.20 | 0.05 | "Share of group FCF dedicated to Mars" |
| `starship_dollars_per_kg_2030` | 200 – 3,000 | 1,200 | "Starship cost-to-LEO at 2030 ($/kg)" |
| `odc_prob_a` | 0.00 – 1.00 | 0.40 | "Probability ODC achieves dual revenue (Model A)" |
| `wrights_law_learning_rate` | 0.05 – 0.35 | 0.22 | "Wright's Law learning rate on Starship cadence" |
| `starlink_dtc_arpu_2030` | 5 – 50 | 18 | "Direct-to-Cell ARPU at 2030 ($/month)" |
| `tam_inflation_rate` | 0.00 – 0.06 | 0.025 | "Long-run TAM inflation" |

Outside-range entries are rejected client-side; outside-P10/P90 entries are accepted with a yellow caveat (mirrors v0 `override_warnings`).

### §7.3 Outputs

- **Group EV (2025)** as a big number.
- **Sum-of-parts** as a horizontal bar chart, one bar per module, sorted descending.
- **Group FCF profile** as a sparkline 2025 → 2050.
- **Per-module summary card grid** with module EV, total revenue 2050, blended IRR 2030.

No tornado, no convergence diagnostics, no V2.16 references in Client Mode.

### §7.4 xlsx downloads

Three xlsx artifacts, generated by `io/excel_export.py` (extended):

1. **Active scenario.xlsx** — one sheet per module + a Group sheet + a Valuation sheet + a Cover sheet listing the scenario inputs and the methodology references.
2. **Scenario pack.xlsx** — Base + Bear + Bull side-by-side on each sheet (columns Base / Bear / Bull / 2025 → 2050 per scenario), with a Cover sheet.
3. **Methodology one-pager.pdf** — static asset, regenerated per release.

Each xlsx Cover sheet links cells to the corresponding Audit Tab URL (`https://…/audit/{sheet}?row={row}&col={year}`) so a client can hand the file back to their analyst and the analyst can click through to derivations.

### §7.5 Share link

Custom-scenario state encodes as a URL-safe base64 of the overrides dict: `https://…/client?s=eyJtYXJzX3BjdCI6MC4xLCJzdGFyc2hpcF8u…`. Server validates against MC ranges on load.

---

## §8 — Data & API Contracts

### §8.1 Endpoints (additions to v0)

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/sheets` | List the 15 source sheets + their grid metadata (row count, col count, lifecycle stage, section index). |
| `GET` | `/api/sheets/{sheet}/grid?run_id={id}` | Return the rendered grid for one sheet for one run — labels, units, year values, cell kinds, divergence flags. |
| `GET` | `/api/lineage/{key}` | Extended payload per §6.4. |
| `GET` | `/api/lineage/{key}/history` | Change-history rows per §6.3. |
| `GET` | `/api/lineage/{key}/graph?depth={n}` | Dependency graph for the flow diagram. |
| `POST` | `/api/exports/scenario.xlsx` | Body: `{ run_id }`. Returns the xlsx as a stream. |
| `POST` | `/api/exports/scenario_pack.xlsx` | Body: `{ scenarios: ["base_case", "bear", "bull"] }`. |
| `GET` | `/api/client/scenarios` | Client-mode curated picker payload (subset of `/api/scenarios`). |
| `GET` | `/api/client/inputs/whitelist` | The vetted custom-scenario inputs + ranges + plain-language labels per §7.2. |

### §8.2 Grid payload shape

```ts
type GridPayload = {
  sheet: string;
  rows: Array<{
    row_id: string;               // e.g., "R8"
    label: string;                // canonical-label string
    section_ref: string;          // e.g., "§4.2 F9 customer launches"
    unit: string;
    base_case_value: number | null;
    year_values: number[];        // length 26, 2025..2050
    cell_kinds: Array<"input" | "derived" | "anchor" | "stub">;
    divergence_flags: Array<"match" | "drift" | "intentional" | "n_a">;
    lineage_keys: string[];       // length 26 (or 27 if base-case scalar included)
  }>;
};
```

The frontend asks for one sheet at a time, on first visit, and caches by `run_id`. Payload size for the largest sheet (Allocator, 171 rows × 31 cols) is ≈ 200 KB uncompressed, ≈ 35 KB gzip; well within the latency budget.

### §8.3 Performance budget

- Initial app load < 2 s on cold cache (frontend gzip < 400 KB).
- Sheet first-paint < 800 ms after tab click (eager-fetch the active sheet, lazy-fetch the others on idle).
- Cell-click → derivation panel populated < 250 ms (lineage payload cached client-side keyed by `(run_id, lineage_key)`).
- Cell-click → minimap update < 100 ms (lifecycle & section are part of the lineage payload).
- Dependency-graph render (depth 2, ≤ 20 nodes) < 300 ms.
- xlsx download generation < 5 s for one scenario, < 15 s for the pack.

### §8.4 Caching

- React Query (`@tanstack/react-query` v5) for all API reads. Cache key includes `run_id`; invalidation on new run.
- Backend caches grid payloads in Redis keyed `(run_id, sheet)`, TTL 1 h.
- Change-history caches in Redis keyed `(commit_sha_of_HEAD, lineage_key)`, TTL 15 min.

---

## §9 — Component Inventory

```
frontend/src/
├── app/
│   ├── AuditApp.tsx          (Audit Mode shell)
│   ├── ClientApp.tsx         (Client Mode shell)
│   └── ModeRouter.tsx        (URL routing + auth-claim redirect)
│
├── audit/
│   ├── SheetTabs.tsx
│   ├── Grid.tsx              (ag-grid wrapper; one instance, sheet-switched)
│   ├── DerivationPanel.tsx
│   ├── DependencyGraph.tsx   (react-flow)
│   ├── SourcesPanel.tsx
│   ├── ChangeHistoryList.tsx
│   ├── Minimap.tsx
│   ├── RunAuditTab.tsx
│   └── ScenarioSidebar.tsx   (re-used from v0 ScenarioPicker)
│
├── client/
│   ├── ScenarioCards.tsx
│   ├── HeadlinePanel.tsx
│   ├── SumOfPartsBar.tsx     (recharts)
│   ├── FcfSparkline.tsx      (recharts)
│   ├── CustomBuilder.tsx
│   ├── DownloadsPanel.tsx
│   └── ShareLinkButton.tsx
│
├── shared/
│   ├── api.ts                (extended from v0)
│   ├── types.ts              (LineageEntry, GridPayload, ChangeHistoryEntry, …)
│   ├── format.ts             (formatMm, formatBillions, formatPct, formatCount)
│   ├── unit-coloring.ts
│   └── query-client.ts       (React Query setup)
│
├── data/
│   └── sheet_graph.ts        (static 15-sheet graph; build-time generated)
│
└── styles/
    ├── tokens.css            (Mach33 palette + spacing scale)
    └── grid.css              (ag-grid overrides)
```

Total net new TS lines estimate: ~3,500. v0 reuse: `LineagePanel.tsx` becomes `DerivationPanel.tsx`, `FcfTable.tsx` is replaced by `Grid.tsx`, `ScenarioPicker.tsx` becomes `ScenarioSidebar.tsx`. `TornadoChart.tsx` moves under `audit/` and is hidden in Client Mode.

---

## §10 — Acceptance Criteria

A1. URL `/audit/group_pnl?row=R102&col=2027` loads the Group P&L sheet, scrolls to R102 / column 2027, opens the derivation panel for that cell, and updates the minimap to "Conservation" lifecycle stage and "§15.2 R102 FCF check" section.

A2. Clicking any cell in Allocator!R48 (Starlink V2 BB cash demand) → derivation panel shows formula `anchor × learning × year_mask + exogenous_facility_capex` (per Sprint 11f Option A, `context.md §3.2`), resolved inputs with values, and a depth-2 dependency graph reaching back to Assumptions cells.

A3. For any cell whose code value differs from the V2.16 cached value, the cell renders with amber border and the derivation panel's status pill reads `intentional` (with §11.6 reference) or `drift` (with the Δ in $mm). The Run Audit tab lists this cell in the top-50 divergence table.

A4. Change-history panel for any cell touched by Sprint 11e shows at least one entry dated 2026-05-26 with a working link to the corresponding `DEV_LOG.md` anchor.

A5. Mode switch: in Client Mode there is no path — UI, URL, or API — to surface a formula, an Excel cell address, a V2.16 cached value, a divergence flag, a convergence diagnostic, a build sha, or any `lineage_key`. (Verified by a Playwright assertion that scrapes the rendered DOM for forbidden tokens.)

A6. Custom scenario builder: setting `mars_pct = 0.25` is rejected client-side (outside the 0.00 – 0.20 range); setting `mars_pct = 0.18` is accepted with a yellow caveat ("above P90"); setting `mars_pct = 0.07` is accepted silently.

A7. xlsx download: the "Active scenario.xlsx" file has one tab per module + Group + Valuation + Cover, the Cover sheet lists the active overrides, and every numeric cell in the data tabs has a hyperlink to the corresponding Audit URL.

A8. Performance: a fresh load of `/audit/starlink?row=R8&col=2030` from a cold cache completes in < 2.5 s on a 2022 MacBook Pro over a residential 100 Mbps connection.

A9. Accessibility: the Audit grid is fully keyboard-navigable; the derivation panel, minimap, and dependency graph are reachable via Tab; all interactive elements have aria-labels; color is never the sole indicator of state (the amber-border divergence cells also carry a `▲` glyph).

A10. The "share link" round-trips: copying the URL on Client Mode after building a custom scenario and opening it in a private window reproduces the same outputs.

---

## §11 — Decisions & Trade-offs

| # | Decision | Alternatives rejected | Rationale |
|---|---|---|---|
| F1 | One sheet per Excel tab, no merging | Group everything into a single "all cells" virtual grid | Auditor mental model is the Excel workbook; merging breaks the muscle memory we need to preserve. |
| F2 | Read-only Audit grid (overrides via sidebar) | In-cell editing | Editing in-cell would imply per-cell formula authoring — out of scope for a port reconciliation tool. Sidebar override mirrors v0 contract. |
| F3 | `ag-grid-community` over `glide-data-grid` or hand-rolled | hand-rolled virtualized table; AG Grid Enterprise | Community license is sufficient; ecosystem maturity outweighs the dependency weight. |
| F4 | `react-flow` (xyflow) for dependency graph | d3-force, Mermaid, Cytoscape | Better React integration, declarative node graph fits our pre-computed lineage, no canvas (a11y wins). |
| F5 | URL-routed mode switch | Auth-only mode switch | Lets internal users prototype the Client view from `/client` directly; URL-shareable scenarios free. |
| F6 | Static client-side `sheet_graph.ts` for the 15-sheet model graph | Dynamic API call | The graph changes only when a tab is added (constitutional event, `context.md §3.11`); checking it in is correct. |
| F7 | Change history computed server-side via `git log` filter, cached in Redis | Pre-computed at build time | Build-time computation would require a re-build per commit; lazy on-demand with cache is cheaper and more accurate. |
| F8 | Plain-language input labels in Custom Builder map to canonical labels server-side | Expose canonical labels directly | Canonical labels are model-internal; the whole point of Client Mode is to hide them. |
| F9 | xlsx Cover sheet links to Audit URLs | Embed methodology text in the xlsx | Linking keeps the xlsx light and the methodology source-of-truth in the app, not duplicated in each export. |
| F10 | Hard separation of `/audit` and `/client` codepaths | Conditional rendering inside shared components | Conditional rendering risks accidentally leaking model machinery into Client Mode (acceptance A5). Separation is enforced architecturally. |

---

## §12 — Phasing

**Phase 1 — Audit foundations (2 sprints).**
- Extended `LineageEntry` + `/api/sheets` + `/api/sheets/{sheet}/grid` endpoints.
- AG Grid wired to one sheet (Starlink) end-to-end.
- DerivationPanel reading the extended payload.
- Minimap with lifecycle stage + section + 1-hop graph.

**Phase 2 — Audit completeness (2 sprints).**
- All 15 sheet tabs rendering.
- DependencyGraph (react-flow) at depth 2 with expand.
- Sources & Change History panel + `/api/lineage/{key}/history` endpoint with Redis cache.
- Run Audit tab.

**Phase 3 — Client Mode (1.5 sprints).**
- Curated scenario cards + Headline panel + Sum-of-parts + FCF sparkline.
- Custom scenario builder + `/api/client/inputs/whitelist`.
- xlsx export endpoints + Cover-sheet links.
- Share-link encoding.

**Phase 4 — Polish & a11y (1 sprint).**
- Keyboard nav across grid + cross-sheet jump.
- Playwright suite for acceptance criteria A1–A10.
- Performance regression budget set in CI.

Total: ~6.5 sprints. Phases 1 and 2 ship behind a feature flag for Vlad to use internally during the corresponding port sprints; Phase 3 ships only after numerical sign-off per `PRD.md §10`.

---

## §13 — Open Questions

1. **Auth model.** Production needs role-claim-driven mode routing (§3.1). Which IdP — Auth0, Clerk, in-house? Out of this PRD; flagged for `PRD.md §17` backlog.
2. **xlsx pack regeneration on every Base Case change.** Should the Scenario pack be regenerated automatically on every merge to main that affects Base Case outputs, or only on tagged releases? Recommend: tagged releases only, to keep the pack stable for clients.
3. **Audit history beyond `git log`.** Some inputs are revised in `.yaml` scenario files (not in code). Capture those via the same change-history endpoint by extending the file-filter set; flagged as a Phase 2 implementation detail, not a spec-level question.
4. **Mobile.** Not in scope (§1.3). Confirm with stakeholders that a "read-only / share-link landing page" for mobile is also out of scope, or carve it into v2.

---

## §14 — Amendment Log

| Date | Author | Change |
|---|---|---|
| 2026-05-28 | Dr. Marcus Hale | v1.0 — initial draft. |
