# Financial Model Porting Project Context — Mach33 SpaceX Valuation Model

**Status**: Living context document. Read in full before any code is written. Every code module references this doc; every PR cites the section it implements.

**Companion documents** (repo root + package):
- `docs/DEV_LOG.md` — append-only agent handoff log (what changed, Block B xfail status, how to verify). **Read after this file when resuming work.**
- `role.md` — operating persona; requires dev log updates on material changes.
- `scenarios/s1_adherence.yaml` — S-1 P0 override mirror (also applied in code by `apply_s1_adherence_overrides()` on every pipeline run).

**Companion documents** (in `Pre Existing Model Package/`):
- `00_Constitutional_Docs/02_Architecture_and_Methodology.md` — the model's architecture spec (load-bearing; §6, §10, §11, §15, §20 are most-cited)
- `00_Constitutional_Docs/01_Lessons_Learned.md` — 23 principles with incident traceability
- `00_Constitutional_Docs/Model Execution Rules.md` — 23 operational rules; constrain the workbook but several map directly into code conventions
- `00_Constitutional_Docs/03_Sprint_Roadmap_and_Verification.md` — §6.8 calibration targets, §10 sprint sizing
- `06_Memory_Snapshot/MEMORY_SNAPSHOT_CRITICAL_LOCKS.md` — distilled architectural locks
- `01_Current_State/STATUS_2026_05_26.md` — last-known state of the live workbook
- `02_Fresh_Restart_Inputs/2025 Anchors from Q4_25.md` — 2025 calibration anchors

---

## 1. Project Overview

### 1.1 Model name & purpose

**Mach33 SpaceX Valuation Model** — a 26-year (2025-2050) bottom-up valuation of SpaceX consolidating five operating modules (Customer Launch, Starlink, ODC, AI Stack, Lunar Mars) plus corporate OpEx/CapEx/Tax/Valuation layers. Outputs Group P&L, FCF, DCF-derived Equity Value, Sum-of-Parts valuation, and a Monte-Carlo-driven distribution over equity value.

The model is the product Mach33 ships to clients/consumers; the Excel rebuild has been running sprint-by-sprint since mid-May 2026 and is mid-Sprint-11.

### 1.2 Business context

- **Primary user**: Vlad (Mach33 principal), authors all architectural decisions and signs off sprint PASS.
- **Consumers**: institutional clients viewing scenario-driven equity value and module-level economics; eventually a web UI surfacing scenario explorer, sensitivity tables, and SoTP roll-ups.
- **Use cases**: pre-IPO valuation calibration, scenario sensitivity (Mars carve-out share, Starship $/kg learning, Pr(A) for ODC dual revenue), bear/base/bull bracketing for client conversations, and Monte Carlo distribution for tail risk.

### 1.3 Key stakeholders & sign-off

- **Architecture sign-off**: Vlad. Any deviation from the Architecture & Methodology doc requires updating that doc first.
- **Numerical sign-off**: model-risk-style first-principles derivation against the Architecture & Methodology spec; the four-block pass criteria in §11.1 (structural invariants, external Q4'25 anchors, sense checks, spec coverage). xlsx cell-by-cell comparison is a diagnostic per §11.3 / §11.6, not a sign-off criterion.
- **Consumer-facing sign-off**: a web layer surfacing the model must show audit-grade lineage (every output traceable to its calc + input set).

### 1.4 Target timeline & priority

- **Correctness > speed**. This is an institutional-grade valuation model; numerical fidelity is sacred (per role doc).
- **Inputs are inherited; outputs are independently derived.** The xlsx is the canonical source for inputs (Assumptions, MC ranges, opening balances, demand curve breakpoints) and external calibration anchors (Q4'25 actuals). It is NOT a numerical oracle for derived outputs — the original Excel formulas may contain logic errors that we do not want to carry over. Code computes every derived value from first principles using the Architecture & Methodology spec as the logic specification. Divergence between code outputs and xlsx outputs is a diagnostic signal (one of them has a bug), not a test failure. See §11 for the full reconciliation methodology.
- Port is multi-phase: (1) ingest Assumptions + external anchors, (2) per-module first-principles calc, (3) cross-cutting (OpEx, CapEx, Group P&L, Valuation), (4) conservation + external-anchor + sanity-check PASS, (5) cross-check vs xlsx with divergence triage, (6) MC engine, (7) web UI.
- No hard external deadline; Vlad's internal cadence drives prioritization.

---

## 2. Original Excel Model Inventory

### 2.1 File baseline (locked for the port)

- **Reconciliation baseline**: `01_Current_State/SpaceX Model V2.16.xlsx` (466 KB).
- **Reference baselines**: `02_Fresh_Restart_Inputs/SpaceX Model V30.5.xlsx` (architectural template, legacy); `SpaceX Valuation Model Q4'25 CLEANUP.xlsx` (Q4'25 anchored values).
- **Source workbook is read-only**. All work happens on copies. No code writes back to the source xlsx.

### 2.2 Size & complexity (audited from V2.16)

| Tab | Function | Rows | Cols | Non-empty cells | Formula cells |
|---|---|---:|---:|---:|---:|
| Assumptions | Input source of truth (11 sections, ~290 input rows) | 350 | 36 | 2,700 | 27 |
| Allocator | Cash pool tracker, queue gate, sigmoid IRR queues (cash + kg), vehicle build claim, central IRR display | 171 | 31 | 3,065 | 1,513 |
| Launch Capacity | Starship + F9 supply, Wright's Law cadence, $/kg cost stack, fleet D&A, at-cost launch services rate | 80 | 29 | 1,024 | 795 |
| Customer Launch | External + internal launches, per-launch marginal IRR | 210 | 31 | 1,792 | 1,047 |
| Starlink | BB + DTC + Starshield, V2/V3 vehicle pools, per-vehicle IRR, constellation D&A | 235 | 29 | 3,180 | 1,853 |
| Starlink Capacity | Constellation Gbps aggregation, internal bandwidth claim to ODC, at-cost pricing per pool | 50 | 29 | 329 | 104 |
| ODC | Orbital compute satellites, dual revenue (Model A energy + Model B η), per-sat IRR | 210 | 29 | 2,777 | 2,214 |
| AI Stack | Cursor + Grok consumer + Grok enterprise API; buys compute from ODC at-cost | 210 | 29 | 418 | 83 (stub) |
| Lunar Mars | Strategic carve-out (not in IRR queue); BV engine (labour units + hardware) | 212 | 32 | 2,644 | 1,905 |
| Group P&L | Consolidated walk, conservation block R99-R110, calibration memo block | 125 | 56 | 1,234 | 425 |
| OpEx | Corporate R&D (by module) + SG&A (by function), start% / end% / CAGR pattern | 60 | 29 | 821 | 417 |
| CapEx | Module CapEx aggregation + Corporate CapEx + Spectrum (EchoStar) + Vehicle build claim | 47 | 29 | 759 | 494 |
| Valuation | DCF off Group FCF, SoTP per module, multiples cross-check, sensitivity | 6 | 29 | 53 | 0 (stub) |
| Demand Curves | BB + DTC piecewise-linear Q→Revenue lookup (61 BB breakpoints, 56 DTC breakpoints) | 145 | 36 | 568 | 26 |
| Claude Log | Per-sprint change log | 15 | 6 | 84 | 2 |
| **TOTAL** | | | | **21,448** | **10,905** |

- **Iterative calculation**: ON, 100 iterations / 0.001 tolerance (Memory 1.6, load-bearing for Starlink↔Starlink Capacity %×Revenue cycle).
- **Year horizon**: `D:AC` = 2025-2050 (26 columns). Year header in row 4 (hardcoded ints); year-offset helper in row 5 (`D5=0 ... AC5=25`). Locked; no extension to AD or beyond.
- **Defined names**: none. All cross-references are `Sheet!Cell` or `INDEX/MATCH`-by-label.
- **VBA**: archive present in the .xlsx (`vba_archive` non-null). No defined names attached to VBA; macros appear to be record/playback helpers, not load-bearing. **Action**: extract and inspect `vbaProject.bin` during ingest; treat as evidence only unless a macro is shown to drive a calc.
- **External links**: none.
- **Top function counts**: `MATCH` 5,004, `INDEX` 5,000, `IFERROR` 1,517, `IF` 1,379, `MAX` 1,155, `MIN` 595, `ABS` 266, `LOG` 181, `SUM` 133, `AND` 28, `ROUNDDOWN` 27, `POWER` 26, `DATE` 2. **No `SUMPRODUCT`, `OFFSET`, `FORECAST`, `TREND`, `VLOOKUP`** — the legacy footguns (§2.3, §2.4 of the Memory Snapshot) have been retired.
- **Cross-tab references**: ~9,500 references into Assumptions (Assumptions is the canonical input layer); Allocator OUT reads from each module by canonical label (per Rule 12).

### 2.3 Critical sheets / sections / canonical labels

- **Assumptions** is the input registry. 11 sections (§1 Global, §2 Allocator, §3 Capacity, §4 Customer Launch, §5 Starlink, §6 ODC, §7 AI Stack, §8 Lunar/Mars, §9 OpEx, §10 CapEx, §11 Valuation, §12 Demand Curves Shift). Each input row carries: column A label, column B Base Case (or empty for year-rows), column C notes/source, columns D-AC year-row values, columns AG-AJ MC Min / Max / Distribution / notes. Total ~212 inputs across 11 sections.
- **Allocator** carries the canonical labels module tabs read by INDEX/MATCH: `[module] cash allocation`, `[module] kg allocation`, `Starlink V[2|3] [BB|DTC] cash allocation` (vehicle-level per Sprint 11 Block 1), `[module] Blended IRR`, and §8 vehicle build claim.
- **Group P&L** carries the consolidated walk and the conservation block R99-R110:
  - R99 Revenue check, R100 EBITDA check, R101 CapEx check, R102 FCF check, R103 D&A check, R104 EBIT consistency, R105/R106/R107 internal flow eliminations, R108 ALL OK boolean, R109 cash flow identity, R110 module FCF residual memo.
  - Calibration target memos R111-R125 (vs Q4'25 anchors).
- **Demand Curves**: BB has 61 breakpoints (R82-R142), DTC has 56 (R17-R72), plus year-row curve evaluators R140-R145 read by Starlink revenue rows. Piecewise-linear lookup via INDEX/MATCH bracket-find + manual interp (`FORECAST` is forbidden — Memory 2.4).

### 2.4 Known fragile areas (do NOT replicate the bug; do reproduce the value)

- **Sprint 11d circular dependency at zero attractor** (Memory 2.7, STATUS 2026-05-26 §"What broke tonight"): Allocator cash demand rows R48/R53/R58/R63 read actual Starlink sat CapEx, which is downstream of cash allocation, closing a loop that converges to zero in iterative calc. **Sprint 11f Option A** decouples demand (anchor × learning × year-mask + exogenous facility CapEx) from output (cash-bound MIN). **Port implication**: code implements Option A from day one; demand and output are different types with no shared reference. V2.16 in the package was Vlad's handoff snapshot — the V2.18 collapse state is NOT what V2.16 contains; V2.16 is the reduced-Sprint-11e baseline post-merge.
- **Assumptions write-then-reference calc-engine corruption** (Memory 2.1): an Excel-side footgun, not a calc-logic bug. Does not affect the port. Document for posterity.
- **INDEX with col_num=0 spill** (Memory 2.2): Excel-side. The model has already avoided this; the port should not import it.
- **Mars carve-out uses prior-year FCF** to break circularity with Cash BoY (Architecture §6.2 / §11.1). Code must honor t-1 read; no current-year shortcut.
- **AI Stack tab is a stub** (83 formula cells, mostly empty). Sprint 6 was deferred. Code must support AI Stack as a placeholder with `Total Revenue = 0` until the AI Stack sprint runs and the tab fills out.
- **Valuation tab is empty** (0 formula cells, 53 static). Sprint 11/12 will populate. Code architecture should provide a Valuation module ready to consume Group FCF + per-module FCFs.

### 2.5 Must-match outputs — EXTERNAL ANCHORS ONLY, not xlsx-derived values

The reconciliation target is **external real-world calibration**, not the xlsx's computed outputs. The xlsx cached values for derived rows are diagnostic references, not the target. The values below come from `2025 Anchors from Q4_25.md` (real Q4'25 figures Vlad has high confidence in) and from public / disclosed SpaceX figures — these are anchors the code is required to reproduce within tolerance because they reflect ground truth, not because they appear in V2.16.

**Status of xlsx-derived outputs:** the values in V2.16 for derived rows (Group Revenue 2050 ~$583B, Group D&A 2050 ~$6B, Group FCF 2050 ~−$90B, etc.) are listed in §2.6 below as **diagnostic comparison points**. They tell us where the xlsx implementation currently lands; they do NOT define correct code behavior. If the code derives a different 2050 number from the same inputs + the Architecture spec, that delta opens a divergence investigation (see §11.6).

**2025 anchors (Architecture §17; external Q4'25 actuals — these the code MUST match):**

| Output | 2025 target | Tolerance |
|---|---:|---:|
| Group Revenue | $14,650mm | ±5% |
| Starlink (BB + DTC) revenue | $7,852mm | ±5% |
| of which DTC | $156.91mm | ±10% |
| Starshield revenue | $2,520mm | ±5% |
| Customer Launch revenue (F9 customer) | $4,290mm | ±5% |
| ODC / AI Stack / Lunar Mars revenue | $0 | exact |
| Group EBITDA | $8,690mm (margin 59.3%) | ±5% |
| Group D&A | $1,060mm | ±10% |
| Group FCF | $3,670mm | ±5% |
| Total OpEx | $3,820mm | ±5% |
| Total CapEx | ~$2,030mm | ±10% |
| F9 launches (total) | 171 | ±5 |
| F9 customer launches | 43 (S-1); was 38.58 Q4'25 | ±2 |
| Starship launches | 0 | exact |
| Active sats end-2025 | ~9,800 | ±5% |
| Implied EV (10× rev) | $111B | ±5% |
| Starting cash EoY 2024 | $11,385mm (S-1); was $5,000mm Q4'25 | exact |

**Required structural invariants (must hold regardless of where derived values land):**

| Invariant | Requirement | Source |
|---|---|---|
| R108 conservation | "OK" all years 2025-2050 | Architecture §15.2; non-negotiable |
| R99-R107 residuals | abs() ≤ $1mm all years | Architecture §15.2; integrity proof |
| Σ module cash allocations ≤ Available cash for IRR queue | every year | Allocator design §6.3 |
| Σ module kg allocations ≤ Capacity available for IRR queue | every year | Allocator design §6.4 |
| Modules with Blended IRR ≤ 0 receive zero allocation | strict cutoff every year | Principle 5; §5.4 |
| Module EBITDA == Module Gross Profit | every module, every year | Vending-machine framing |
| Internal flow conservation (launch / bandwidth / compute) | source rev = Σ consumer COGS | Rule 21 |
| Iterative solver convergence | < 100 iters, < 0.001 max residual | Memory 1.6 |

### 2.6 xlsx-derived values — DIAGNOSTIC REFERENCES, not authoritative

These are the values V2.16 currently produces. They are recorded here so that, after code derives its own outputs from first principles, we can diff against the xlsx and triage divergences. Each divergence is then investigated to determine which side has the bug (see §11.6 triage workflow).

| Quantity | V2.16 cached value | Status |
|---|---:|---|
| Group Revenue 2050 | ~$583,059mm (post-Sprint-11e) | diagnostic; the deployment-binding rework (Sprint 11f Option A) may shift this in code |
| Group D&A 2050 | ~$6,000mm (post-LM BV correction) | diagnostic; LM BV $478B/yr phantom D&A bug already excised in V2.16 — but a fresh first-principles derivation may surface other D&A drift |
| Group FCF 2050 | ~−$90,000mm | diagnostic; sign and magnitude reflect post-illusory-FCF state in V2.16 |
| Allocator D29 Available cash 2025 | ~$13,700mm | diagnostic; reflects spectrum fix + bridge loan in V2.16 |
| Starlink Module EBITDA 2050 | (read from V2.16) | diagnostic; per-vehicle ramp depends on Option A binding |
| Per-module 2050 EV (SoTP) | n/a — Valuation tab is stub in V2.16 | not even a diagnostic; code derives independently |

**Rule of engagement for these diagnostics:** if code matches within tolerance → log "agrees with V2.16, no divergence." If code diverges → record both values + the triage outcome in the run audit log. Triage outcomes (per §11.6): (a) code bug, fix code; (b) xlsx bug, code is correct, log for Vlad to amend xlsx; (c) intentional difference because code implements a constitutional lock (e.g., Sprint 11f Option A) that xlsx does not, log for Vlad sign-off.

---

## 3. Architectural Locks (constitutional — do not relitigate in code)

These are the load-bearing decisions from the Memory Snapshot + Architecture & Methodology spec. Every code module honors them. **These locks come from the SPEC, not from the xlsx.** The xlsx is one implementation of the spec; the code is another. Where xlsx and spec diverge, the spec wins.

### 3.1 Vending-machine module framing (Memory 1.1, Architecture §3, Principle 8)

Every module P&L is `Revenue → COGS → Gross Profit = Module EBITDA → CapEx → Module FCF`. **No R&D, no SG&A, no corporate overhead, no taxes** on any module file. Those live in `opex.py` / `group_pnl.py` only. Module `EBITDA` is mathematically Gross Profit (label retained per Principle 7). Module FCF is pre-tax, pre-corp.

**Code implication**: each `calc/modules/<module>.py` has the same five-section structure (`compute_revenue`, `compute_cogs`, `compute_gross_profit`, `compute_capex`, `compute_fcf`). A linter or test enforces that no module file imports the OpEx/Tax modules.

### 3.2 Demand purely exogenous — Sprint 11f Option A (Memory 1.8, Sprint_11f_Spec §2)

| Quantity | Reads from | Recursion? |
|---|---|---|
| **Demand** (sigmoid cash-demand rows + facility CapEx) | anchor × learning × year-mask + exogenous facility CapEx | **No** |
| **Output** (launches → sat CapEx → cash IN) | `MIN(cash_from_allocator / unit_cost, internal_target)` | bounded by cash; never feeds demand |

**Code implication**: enforce at the type level. `DemandInputs` and `OutputResults` are distinct dataclasses; `compute_demand(...)` takes no `OutputResults`; `compute_output(...)` takes a `DemandResult` plus an allocator allocation. A test imports both functions and asserts via inspection that demand has no transitive reference to any output type.

### 3.3 Anchor-and-offset year-row pattern (Memory 1.2, Rule 23)

In Excel, deterministic ramps use `$D$anchor × (1+rate)^E$5`, never `=prior_col × growth`. In code:
- Year vectors are 26-element numpy arrays indexed `[0..25]` = years `[2025..2050]`.
- Each year-row computation is a vectorized expression over the offset vector, not a `for t in range(26): v[t] = v[t-1] * g` loop, unless the formula is genuinely year-chained (cumulative sums, Cash BoY, BV running sums, ratchet latches — flagged as "Rule 23 exception" in a docstring).

### 3.4 Cross-tab references by canonical label only (Memory 1.3, Rule 12, Principle 3)

In Excel: `INDEX(Tab!D:D, MATCH("label", Tab!$A:$A, 0))`. In code: a global registry (`canonical_labels.py`) maps every canonical label to a typed accessor. No code ever indexes a result DataFrame by integer row position. **Renaming a label is a constitutional event** — touches the Excel workbook, the registry, and every reader.

### 3.5 Queue gate reserves non-module claims first (Memory 1.4, Architecture §6.2, Principle 4)

```
Available_cash_for_IRR_queue = max(0, Cash_BoY − OpEx − Corp_CapEx − Spectrum_CapEx − Taxes − Mars_carveout − Vehicle_build_claim)
```

Module CapEx allocation runs AFTER this subtraction. Within-year circularity (OpEx ← Revenue ← CapEx ← Allocator) resolves via the iterative solver (§7 below).

### 3.6 Per-sat / per-launch marginal IRR — no fleet-seeding (Memory 1.5, Architecture §5, Principle 2)

For module M, year T, with economic life N:
```
CF stream = [−cost_per_unit(T), net_marginal_revenue(T+1), …, net_marginal_revenue(T+N)]
Spot IRR(T) = IRR(CF stream evaluated at year T)
Forward IRR(T+2) = IRR(CF stream evaluated at year T+2)
Blended IRR = (1 − w) × Spot + w × Forward,   w = 0.7
```

Per-unit, not fleet-level. No `MAX(CumCapEx − CumD&A, 1)` NIC denominators (legacy footgun). Negative IRR → zero allocation (strict cutoff, no SPW floor multiplier).

### 3.7 Vehicle-level Allocator for Starlink (Memory 1.9, Architecture §20.1)

V2 BB / V2 DTC / V3 BB / V3 DTC are top-level allocator queue entries with their own per-vehicle IRR. V2 vehicles have NO kg allocation (Falcon 9, not Starship). V2→V3 transition emerges from IRR + cash allocation — no hardcoded ratchets.

### 3.8 Mars carve-out off the top, using prior-year FCF (Architecture §6.2, §11.1, Principle 22)

```
Mars_carveout(T) = max(Mars_floor, Group_FCF(T−1) × Mars_pct)
```

The t-1 read is the circularity breaker. `Mars_pct` and `Mars_floor` are both MC-variable (central uncertainty: how much SpaceX dedicates to Mars vs. terrestrial IRR-positive lines).

### 3.9 Internal transfer 4-step pattern (Architecture §7, Principle 9, Rule 21)

For every internal flow (launch services, bandwidth, compute):
1. **Source module** books internal transfer revenue (real cash inflow to source's P&L).
2. **Consuming module** books matching cost in COGS.
3. **Group P&L** elimination row subtracts the flow once.
4. **Conservation check row** verifies `Source internal rev = Σ Consuming module COGS for the flow`.

All three transfer prices are **fully-allocated** (variable cash cost + non-cash D&A share). Locked 2026-05-20.

### 3.10 Iterative-calc convergence is part of the contract (Memory 1.6)

100 iterations, 0.001 absolute tolerance. The model has genuine simultaneity (Starlink↔Starlink Capacity %×Revenue; Allocator↔modules; Cash BoY↔Group FCF where t-1 is used to weaken the loop). Code uses an explicit fixed-point solver; convergence is asserted, not assumed.

### 3.11 No row insertions / no version surfacing (Rule 10, Memory 3.2)

In Excel: cross-references would break. In code: labels are stable; only append-equivalent operations (extending the canonical registry) are allowed. Version numbers ("V2.16", "V2.17", "V2.18") are not surfaced in code or in user-facing state. The codebase has a single canonical model; the snapshot it reconciles against is configured externally.

### 3.12 US English (Memory 3.5)

All identifiers, docstrings, comments, and labels: US English. Common slips to avoid: `modelling → modeling`, `programme → program`, `behaviour → behavior`, `colour → color`, `centre → center`, `organisation → organization`, `optimisation → optimization`, `recognise → recognize`, `labelled → labeled`, `catalogue → catalog`. (`analyses` is identical in US/UK; don't over-correct.)

---

## 4. Data Landscape & Ingestion

### 4.1 Primary input sources

- **Assumptions tab** (V2.16 row-by-row) is the source of truth for ~212 inputs. Each row carries Base Case + MC Min/Max/Distribution. Code ingests this tab as the canonical input layer.
- **Q4'25 anchors** (`2025 Anchors from Q4_25.md`): 2025 calibration targets. Some Assumptions cells are anchored to these and locked (e.g., Starting cash $5,000mm). The MC distribution column reads `fixed` for these.
- **Demand Curves** (V2.16 Demand Curves tab): 61 BB + 56 DTC breakpoint pairs (Q, Revenue) per year. Code ingests as two 2D numpy arrays indexed `[breakpoint_idx, year_idx]`.
- **Constellation opening balances** (Mach33 historical anchors at Assumptions R103-R115): hard-coded baseline; not MC-variable.
- **V30.5 + Q4'25 cleanup workbooks**: reference baselines only; not ingested for runtime. Used during reconciliation when checking against pre-V2.16 logic.

### 4.2 Ingestion pattern

Single ingest module `io/excel_ingest.py` with two passes:

1. **Formula pass** (`load_workbook(..., data_only=False)`): captures formula strings, Allocator OUT label registry, sheet/row structure. Output: `WorkbookStructure` (sheets, label index, formula provenance).
2. **Value pass** (`load_workbook(..., data_only=True)`): captures cached values. Requires that Excel has saved the workbook (cached values are written by Excel, not by openpyxl). Output: `WorkbookSnapshot` (full per-cell value matrix used as the **diagnostic reference** for §11.3 divergence reporting and §11.6 triage — NOT as a per-cell pass/fail oracle).

The Assumptions tab is parsed into a typed `Assumptions` pydantic model with the 11 sections as nested submodels. The MC Min/Max/Distribution columns AG/AH/AI are parsed into a parallel `MCRanges` model. Year-row inputs map to length-26 vectors; single-value inputs to scalars.

### 4.3 Known data-quality issues

- **Array formulas in cached state**: openpyxl returns `ArrayFormula` objects for many year-row cells (Starlink R8, Group P&L R8, etc.). The data-only pass returns the cached value; the formula pass returns the array shape. Document which is which during ingest.
- **Empty cells**: differentiate "intentionally blank" (separator rows) from "missing input" (data gap). The Assumptions build plan (`04_Assumptions_Tab_Build_Plan.xlsx`) has the authoritative section header / subhead / input-row layout.
- **VBA archive**: present but no defined names. Extract `vbaProject.bin` during ingest, disassemble for inspection, but treat as non-load-bearing unless evidence shows otherwise.
- **Stub / placeholder values**: Several Assumptions inputs are stubs (e.g., bandwidth Gbps/GWh conversion at R458, BB/DTC split at R459). Code carries them through with their `triangle` MC range (wide); the MC sweep surfaces sensitivity.
- **Cell-format inheritance**: number formats (%, $, mm) are not preserved cell-by-cell during ingest. Code carries unit awareness explicitly (every quantity has a unit type: `dollars_mm`, `pct`, `kg_to_leo`, `gbps`, `count`).

### 4.4 What we ingest from xlsx vs. what we don't

**Ingest from xlsx (authoritative — code uses these directly):**
- Every cell on the Assumptions tab: Base Case values (col B), year-row values (cols D-AC), MC Min/Max/Distribution metadata (cols AG-AI), notes/source (col C).
- Demand Curves tab: BB + DTC breakpoint pairs (Q, Revenue per year).
- Constellation opening balances (Assumptions R103-R115) and other historical anchor cells.
- Canonical row labels in column A of every tab (the label registry).
- Tab/sheet structure (defines the module-to-package mapping; does NOT define formula logic).

**Do NOT ingest as authoritative (xlsx values used as diagnostic only):**
- Cached formula values for any derived row on any module / cross-cutting tab.
- Conservation block residuals (R99-R107). Code computes its own conservation block from its own outputs.
- Allocator OUT contract values (per-module Revenue, EBITDA, IRR, CapEx, FCF). Code derives these from per-module calc.
- Group P&L walk values. Code derives from module outputs + OpEx + CapEx + tax.
- Valuation tab outputs (currently stub anyway).

**Validation on ingest:**
- **Schema validation**: every Assumptions input passes a pydantic validator on load (type, range, distribution-vs-empty consistency). Failed validation halts ingest with a clear error.
- **External calibration cross-check**: read 2025 anchor cells from V2.16; compare to `2025 Anchors from Q4_25.md`. Drift > tolerance triggers a warning at ingest (V2.16 may already have known anchor drift); the test of record is code-output-vs-Q4'25-anchors, not xlsx-vs-Q4'25-anchors.
- **Structural probe**: load V2.16, verify the canonical labels referenced in code's label registry all resolve (i.e., the workbook structure matches what the code expects). A label that exists in registry but not in V2.16 is a port-vs-workbook drift to investigate.
- **Diagnostic snapshot**: the V2.16 value-pass cached values are saved to a snapshot store (parquet) as the reference for §11.6 divergence triage — NOT as a per-cell pass/fail oracle.

---

## 5. Target Stack & Architecture

### 5.1 Language & libraries

- **Python 3.11+** (typing.dataclasses with kw_only=True, structural pattern matching, exception groups for batch validation errors).
- **numpy** for all year-vector math (26-element arrays).
- **pandas** for tabular outputs only — never for core calc. Calc is pure numpy + dataclasses for auditability.
- **pydantic v2** for the Assumptions schema, MC ranges, and the canonical-label registry.
- **scipy** for `scipy.stats` distributions (`triang`, `lognorm`, `uniform`) and `scipy.optimize.brentq` for any 1D root-finding (rare; IRR is computed via numpy-financial or manual Newton iteration).
- **numpy-financial** (or hand-rolled equivalent) for `IRR` matching Excel's `IRR` (Newton's method with multi-start for negative-IRR detection).
- **openpyxl** for ingest (formula + value passes); **xlsxwriter** for any output write-back (reports, audit logs).
- **pytest** + **pytest-xdist** for parametric reconciliation tests; **hypothesis** for invariant tests (conservation must hold for ALL valid inputs).
- **joblib** for parallel MC trials; **scipy.stats.qmc** for low-discrepancy sampling (Sobol) if MC variance is high.
- **FastAPI** for the service layer (scenario runs, MC submissions, result retrieval).
- **React + TypeScript** (or Next.js) for the consumer-facing web UI; **Streamlit** or **Plotly Dash** acceptable for internal scenario exploration during build.
- **uv** or **poetry** for dependency management; **ruff** + **black** + **mypy --strict** for lint/format/type checks.

### 5.2 Explicitly NOT used

- **sklearn** for any piecewise lookup — `LinearRegression` over Demand Curves breakpoints fits a line through all points (Memory 2.4). Use bracket-find + manual linear interp.
- **scipy.interpolate.interp1d** with `kind='linear'` is acceptable for the Demand Curves bracket interp, with explicit `bounds_error=False, fill_value=(low_clamp, high_clamp)`.
- **eval / exec** for parsing Excel formulas. Treat the Excel formulas as documentation; reimplement the math in Python.
- **Implicit DataFrame indexing by integer position** anywhere in calc code.

### 5.3 Repository layout

```
spacex-modeler/
├── pyproject.toml
├── README.md
├── context.md                       (this file)
├── role.md
├── Pre Existing Model Package/      (reference; not imported)
│
├── src/spacex_model/
│   ├── __init__.py
│   ├── config/
│   │   ├── constants.py             (year horizon, iteration params, tolerances)
│   │   ├── canonical_labels.py      (the label registry — single source of truth for cross-tab refs)
│   │   └── settings.py              (env / baseline file path / scenario config)
│   │
│   ├── inputs/
│   │   ├── assumptions.py           (pydantic models for §1-12)
│   │   ├── mc_ranges.py             (MC Min/Max/Distribution metadata)
│   │   ├── s1_2025_anchors.py       (S-1 audited 2025 Block B / ingest anchors)
│   │   ├── s1_overrides.py          (apply_s1_adherence_overrides — P0 disclosed values)
│   │   ├── s1_profiles.py           (S-1 year-row numpy profiles)
│   │   ├── q4_25_anchors.py         (deprecated alias → s1_2025_anchors)
│   │   └── demand_curves.py         (piecewise-linear BB / DTC curve evaluator)
│   │
│   ├── domain/
│   │   ├── year_vector.py           (length-26 numpy wrapper with year labels)
│   │   ├── units.py                 (DollarsMM, Pct, KgToLEO, Gbps, Count — type-safe quantities)
│   │   └── irr.py                   (per-unit IRR engine — Spot, Forward, Blended)
│   │
│   ├── calc/
│   │   ├── allocator/
│   │   │   ├── cash_pool.py         (Cash BoY tracker — Architecture §6.1)
│   │   │   ├── queue_gate.py        (non-module claims subtraction — §6.2)
│   │   │   ├── sigmoid_cash.py      (cash queue with k=2 sigmoid blend — §6.3)
│   │   │   ├── sigmoid_kg.py        (kg queue — §6.4)
│   │   │   ├── deployment.py        (MIN(cash/cost, kg/mass, internal) — §6.5)
│   │   │   ├── vehicle_build.py     (forward-aggregate kg sized claim — §6.6)
│   │   │   ├── mars_carveout.py     (off-the-top using prior-year FCF — §11.1)
│   │   │   └── irr_display.py       (central Spot/Forward/Blended IRR roll-up)
│   │   ├── launch_capacity.py       (Starship + F9 supply; vehicle D&A; at-cost rate)
│   │   ├── customer_launch.py       (external + internal transfer; per-launch IRR)
│   │   ├── starlink/
│   │   │   ├── module.py            (BB + DTC + Starshield P&L; per-vehicle IRR)
│   │   │   ├── vehicle_pools.py     (V2/V3 BB and DTC pool sigmoid blend — §8.1)
│   │   │   ├── ratchet.py           (V2→V3 latch — §8.2; Rule 23 exception)
│   │   │   ├── deorbit.py           (V2 historical fleet retirement — §8.3)
│   │   │   └── revenue_curve.py     (bandwidth-driven via Demand Curves — §8.4)
│   │   ├── starlink_capacity.py     (constellation Gbps aggregation, internal bandwidth claim, at-cost transfer pricing)
│   │   ├── odc.py                   (dual revenue Pr(A)×A + Pr(B)×B; per-sat IRR; internal/external compute split — §9)
│   │   ├── ai_stack.py              (Cursor + Grok products; buys compute from ODC — §10; stub-friendly)
│   │   ├── lunar_mars.py            (BV engine, no IRR — §11; intentional vending-machine divergence)
│   │   ├── opex.py                  (R&D by module + SG&A by function — §12; switching formula for pre-revenue R&D)
│   │   ├── capex.py                 (module aggregation + corporate + spectrum — §13)
│   │   ├── group_pnl.py             (walk + conservation block — §15)
│   │   └── valuation.py             (Group DCF + SoTP + multiples + comparables — §14)
│   │
│   ├── engine/
│   │   ├── iterative_solver.py      (fixed-point iteration; 100 iter, 0.001 tol; damping; convergence diagnostics)
│   │   ├── pipeline.py              (orchestration: build assumptions → ingest demand curves → solve → emit results)
│   │   └── conservation.py          (R99-R110 equivalents; halt on break)
│   │
│   ├── mc/
│   │   ├── distributions.py         (triangle, lognormal, uniform, discrete, yearrow variants)
│   │   ├── sampler.py               (per-input sampling; correlated/independent flags; per-trial seeds)
│   │   ├── runner.py                (joblib-parallel N-trial driver; checkpointed)
│   │   ├── aggregator.py            (output-vector aggregation; percentiles; CVaR; correlation matrices)
│   │   └── sensitivity.py           (tornado, partial rank correlation, 1D sweeps, 2D sensitivity tables)
│   │
│   ├── io/
│   │   ├── excel_ingest.py          (formula + value pass; openpyxl)
│   │   ├── excel_export.py          (xlsxwriter audit / reconciliation reports)
│   │   ├── snapshot_store.py        (parquet / arrow file format for ingested snapshots — reproducible builds)
│   │   └── audit_log.py             (Model Translation Log writer)
│   │
│   ├── service/
│   │   ├── api.py                   (FastAPI; scenario runs, MC submissions, result retrieval, audit endpoints)
│   │   ├── jobs.py                  (background MC runs; status polling)
│   │   └── auth.py                  (placeholder; production wires SSO)
│   │
│   └── cli/
│       ├── run_model.py             (single Base Case run + reconciliation report)
│       ├── run_mc.py                (MC submission; reads scenario config)
│       └── audit.py                 (regenerate Model Translation Log; divergence report vs xlsx diagnostic snapshot)
│
├── tests/
│   ├── reconciliation/
│   │   ├── conftest.py              (loads V2.16 oracle once per session)
│   │   ├── test_assumptions_ingest.py
│   │   ├── test_per_cell.py         (parametrized over (sheet, row, col); 10k+ assertions)
│   │   ├── test_conservation.py     (R99-R107 = 0; R108 = "OK" all years)
│   │   ├── test_calibration_2025.py (Architecture §17 anchors)
│   │   ├── test_calibration_2050.py (post-11e expected state)
│   │   └── test_iterative_convergence.py
│   ├── unit/
│   │   ├── allocator/               (queue gate, sigmoid blend, vehicle build)
│   │   ├── starlink/                (vehicle pools, ratchet, deorbit, revenue curve)
│   │   ├── odc/                     (dual revenue, per-sat IRR)
│   │   ├── lunar_mars/              (BV engine)
│   │   └── irr/                     (Spot, Forward, Blended; edge cases — negative cash flows, all-positive streams)
│   ├── invariant/                   (hypothesis-driven; conservation holds, monotonicity where stated)
│   └── golden/                      (snapshots; regenerated only on explicit approval)
│
├── frontend/                        (web UI; Next.js or pure React + Vite)
│   └── …                            (separate package.json; deployed independently)
│
├── scenarios/                       (YAML/TOML scenario files — Base Case, bear, bull, custom)
│   ├── base_case.yaml
│   ├── bear.yaml
│   └── bull.yaml
│
└── docs/
    ├── model_translation_log.csv    (sheet, row, label → module, function, line)
    ├── architecture_diagram.md      (mermaid; mirrors Architecture & Methodology §1 tab inventory)
    ├── reconciliation_report.md     (latest run output)
    ├── DEV_LOG.md                   (append-only agent handoff — read before coding)
    └── changelog.md                 (per-port-sprint changelog, mirrors the Excel Claude Log)
```

### 5.4 Web UI considerations

- **Audit-grade transparency for clients**: every displayed number is clickable → opens a lineage panel showing the calc function, the inputs it consumed, the intermediate Excel cell it corresponds to, and the Architecture spec section it implements. The Model Translation Log (§10 below) is the index for this.
- **Scenario explorer**: user picks Base Case + per-input overrides. Backend validates against MC ranges (warn if outside MC P10/P90), runs deterministic, returns Group + per-module outputs.
- **MC dashboard**: distribution of Group EV, per-module EV, sensitivity tornado, percentile bands on Group FCF, joint distribution of (Mars share, Starship $/kg learning) → EV.
- **No client-facing version surfacing** (Memory 3.2). Internal builds may show git SHA; client builds show only "current Base Case" / "scenario X".
- **Latency budget**: deterministic run < 2s for Base Case; MC 10k trials < 60s with joblib parallelism. Cache scenario results in Redis or similar.

---

## 6. Modular Code Architecture Principles

### 6.1 Pure functions

Every calc function is pure: takes typed inputs (frozen dataclasses or pydantic models), returns typed outputs. No mutation. No globals. No I/O. Side-effect-free. This is the auditability rule.

### 6.2 One Excel tab = one module package or file

`calc/starlink/` ↔ Starlink tab; `calc/group_pnl.py` ↔ Group P&L tab; etc. The package-to-tab mapping is part of the Model Translation Log.

### 6.3 Sections within a tab = sections within a file

Architecture §6.1 Cash pool tracker maps to `calc/allocator/cash_pool.py`. Each function within carries a docstring referencing the Architecture spec section AND the Excel cell range it implements.

### 6.4 Explicit type-level decoupling of demand and output

`DemandInputs` and `DemandResult` types live in `calc/<module>/demand.py`; `OutputResult` lives in `calc/<module>/output.py`. The output module imports the demand result and the allocator allocation; the demand module imports neither. A test enforces this via inspection of imports.

### 6.5 Canonical-label registry

`config/canonical_labels.py` exposes string constants for every label used across tabs:

```python
class AllocatorLabels:
    CUSTOMER_LAUNCH_CASH_ALLOC = "Customer Launch cash allocation"
    STARLINK_V2_BB_CASH_ALLOC = "Starlink V2 BB cash allocation"
    # … 50+ canonical labels …
```

Code never inlines string literals. Renaming a label is a one-line change in the registry plus an audit-log entry. A test fails if any module file contains a string literal that looks like a label.

### 6.6 Year-vector arithmetic

Every year-row quantity is a `YearVector` — a thin wrapper around `np.ndarray` of length 26 with `year_2025`, `year_2050` accessors and dunder methods (`__add__`, `__mul__`) that preserve the wrapper. Mixing a `YearVector[DollarsMM]` with a `YearVector[Pct]` raises a unit error; conversions are explicit.

### 6.7 Iterative solver as an explicit orchestrator

The pipeline doesn't run module functions in order once; it runs the convergent loop:

```
state = initial_state()
for iter in range(max_iters):
    new_state = single_pass(state)        # all modules in topological order
    delta = max_abs_delta(state, new_state)
    if delta < tol:
        break
    state = damped_blend(state, new_state, alpha=damping)
else:
    raise NonConvergenceError(...)
```

Damping (0.5 default) helps if the loop oscillates. Convergence diagnostics (per-quantity residual trace) saved to the audit log.

### 6.8 Conservation as a runtime invariant

After every pipeline run, `engine/conservation.py` checks R99-R107. R108 must be "OK" all years. A failure halts the run and writes the failing year + residual to the audit log.

---

## 7. Iterative Solver Requirements

The model has three known simultaneity loops:

1. **Starlink ↔ Starlink Capacity**: Starlink revenue depends on available BB Gbps; Starlink Capacity computes available Gbps net of ODC's internal claim, which depends on Starlink Capacity output. Iterative resolution.
2. **Allocator ↔ modules**: module CapEx depends on cash allocation; cash allocation depends on OpEx which depends on revenue which depends on CapEx. Iterative resolution; queue gate (§3.5) reserves non-module claims first.
3. **Cash BoY ↔ Group FCF**: Cash BoY(T) depends on Group FCF(T-1) — broken with the t-1 read. Mars carve-out: same pattern.

**Solver contract**:
- Max iterations: 100 (matches Excel).
- Tolerance: 0.001 absolute on every monitored quantity (Group Revenue, Group FCF, every Allocator cash allocation, every module CapEx).
- Damping: 0.5 default; configurable per scenario.
- Convergence MUST be asserted. A non-convergent run is a failure, not "close enough."
- Initial state: zeros for all unknowns; first pass runs without iteration to seed.
- **Sprint 11f Option A guarantee**: demand never enters the loop on the output side. The loop is exclusively over cash/output quantities. Demand is computed once from anchors + exogenous CapEx; never re-evaluated.

**Diagnostics**: per-iteration trace of max-residual and which quantity holds it. If iter 100 hits without convergence, the trace is the first thing the audit log shows.

---

## 8. Configuration Approach

### 8.1 Source of truth hierarchy

1. **Architecture & Methodology spec** — locks structure (immutable except via explicit doc amendment).
2. **Assumptions tab** (V2.16) — locks values for the V2.16 reconciliation baseline.
3. **Scenario YAML files** — override Assumptions values for non-Base-Case runs.
4. **Environment** (CLI flags, env vars) — pick scenario file, MC trial count, output destination.

No magic numbers in calc code (Rule 14 carries directly into the port). Every behavior input resolves through the Assumptions registry. The only inline numerical constants permitted in calc code are pure mathematical constants (π, unit conversions like `1e6` for kg-to-mm-tons) and they are constants in `config/constants.py`, not embedded literals.

### 8.2 Scenario file format (illustrative)

```yaml
# scenarios/bear.yaml
name: "Bear Case 2026-05-28"
baseline: "V2.16"
overrides:
  assumptions:
    starlink_bb_arpu_2030: 60     # vs Base 75
    mars_carveout_pct: 0.25       # vs Base 0.15
    starship_per_kg_learning: 0.05 # vs Base 0.10
mc:
  trials: 0                       # 0 = deterministic single run
  seed: 20260528
output:
  dir: "outputs/bear_2026_05_28"
  formats: [json, xlsx]
```

For MC runs, `mc.trials: 10000` and the runner samples each MC-flagged input independently per trial.

### 8.3 Reproducibility

- Every run captures: code git SHA, scenario file SHA, Assumptions ingest SHA, MC seed (if applicable), iteration count to converge.
- Output is byte-stable for deterministic runs (numpy ops are deterministic; pandas is too with explicit dtype).

---

## 9. Monte Carlo Engine (v1 scope)

Per your decision: MC is in v1.

### 9.1 Distributions supported

From the Assumptions MC column AI: `fixed`, `triangle`, `lognormal`, `uniform`, `discrete`, `triangle-yearrow`, `fixed-yearrow`. Each maps to a sampler in `mc/distributions.py`:

- **triangle**: scipy.stats.triang(min, mode=base, max).
- **lognormal**: scipy.stats.lognorm with P10/P90 fit to MC Min/Max.
- **uniform**: scipy.stats.uniform(min, max).
- **discrete**: numpy.random.choice over listed options.
- **triangle-yearrow**: sample one multiplier per trial; apply to the entire year-row (preserves shape, shifts magnitude). OR sample anchor years and re-interpolate (configurable per input).
- **fixed-yearrow**: no sampling; use Base year-row as-is.

### 9.2 Sampling rules

- Independent by default. Future work: correlation matrix between named inputs (e.g., Starship $/kg learning ↔ Starlink TAM inflation rate may be negatively correlated; document if assumed).
- Per-trial seed: `base_seed + trial_idx`. Reproducible.
- Low-discrepancy (Sobol via scipy.stats.qmc) optional for variance reduction on EV-tail percentiles.

### 9.3 Aggregation

- **Per-output percentiles**: P5, P10, P25, P50, P75, P90, P95 on Group EV, Group Revenue 2050, Group FCF 2030/2040/2050, per-module EV, per-module 2050 revenue.
- **CVaR / tail metrics**: CVaR(5%), max drawdown vs Base.
- **Joint distributions**: 2D bins of (Mars carve-out, Starship $/kg) → EV — drives the sensitivity table on the Valuation tab.
- **Convergence diagnostic**: per-output running mean / std vs trial count; flag if not converged at N trials.

### 9.4 Sensitivity

- **Tornado**: Δ output per ±1σ input. Ranked.
- **Partial rank correlation**: robust to monotone non-linearity; standard institutional sensitivity tool.
- **1D sweeps**: per-input grid; deterministic; useful for client-facing "what if X is Y" panels.
- **2D sensitivity table**: 5×5 grid on Starship $/kg learning × Starlink TAM inflation (per Architecture §14.5).

### 9.5 Performance

- 10k trials target < 60s with joblib parallelism on a 16-core box.
- Checkpointed: long runs (>5 min) write partial results every 1000 trials so a crash doesn't lose work.
- Result store: parquet or arrow file in `outputs/mc/<scenario>/<run_id>/`.

---

## 10. Traceability Standards

### 10.1 Model Translation Log

`docs/model_translation_log.csv` is the central audit index. Columns:

| sheet | row | column_a_label | excel_cell_range | module_path | function | docstring_section |
|---|---|---|---|---|---|---|
| Allocator | 29 | Available cash for IRR queue ($mm) | D29:AC29 | calc/allocator/queue_gate.py | available_cash_for_irr_queue | Architecture §6.2 |

Every code function that implements a workbook row gets one entry. The log is generated by `cli/audit.py`, regenerable from docstring annotations.

### 10.2 Docstring convention

```python
def available_cash_for_irr_queue(
    cash_boy: YearVector[DollarsMM],
    non_module_claims: YearVector[DollarsMM],
) -> YearVector[DollarsMM]:
    """Available cash for the IRR queue, after non-module claims are reserved.

    Excel cell:        Allocator!D29:AC29
    Excel label:       "Available cash for IRR queue ($mm)"
    Architecture ref:  §6.2 (queue gate)
    Principle:         4 (queue gate for non-module claims is LOAD-BEARING)

    Formula: max(0, Cash_BoY − non_module_claims)
        where non_module_claims = OpEx + Corp_CapEx + Spectrum_CapEx + Taxes
                                  + Mars_carveout + Vehicle_build_claim
    """
```

A linter checks every public function in `calc/` has the four required tags (Excel cell, Excel label, Architecture ref, Principle).

### 10.3 Variable naming

Snake_case English mirroring the Excel canonical label as closely as possible. `Customer Launch Blended IRR` → `customer_launch_blended_irr`. Memo rows prefixed `memo_`. Year-chained Rule 23 exceptions flagged in the docstring with the exception reason.

### 10.4 Audit log

Every model run writes:
- Inputs hash (Assumptions + scenario overrides)
- Convergence: iterations to converge, final max-residual
- Conservation: R99-R107 residuals per year, R108 boolean per year
- Outputs hash (Group + per-module FCFs, EV)
- Wall-clock time, peak memory

Stored in `outputs/<run_id>/audit.json`. The web UI reads this for the lineage panel.

---

## 11. Reconciliation Framework

The reconciliation philosophy: **code derives outputs from first principles using the Architecture & Methodology spec as the logic source; xlsx values are diagnostic, not authoritative.** This is the institutionally rigorous approach — the entire reason for porting is to produce a model that can be independently audited and trusted, which is impossible if the new model just replays whatever Excel does. The xlsx is allowed to be wrong; the spec is allowed to be ambiguous; we derive what the spec says and triage divergences explicitly.

### 11.1 Pass criteria (what determines reconciliation PASS)

A reconciliation run PASSES if and only if all four blocks pass:

1. **Block A — Structural invariants** (§2.5 table; non-negotiable):
   - R108 = "OK" all years 2025-2050.
   - R99-R107 residuals ≤ $1mm absolute every year.
   - Σ module cash allocations ≤ Available cash for IRR queue every year.
   - Σ module kg allocations ≤ Capacity available for IRR queue every year.
   - Modules with Blended IRR ≤ 0 → zero allocation, every year, strict.
   - Module EBITDA == Module Gross Profit for every module, every year.
   - Internal flow conservation (launch / bandwidth / compute): source rev == Σ consumer COGS, every flow, every year.
   - Iterative solver converges in < 100 iterations with max residual < 0.001.

2. **Block B — External calibration anchors** (Q4'25 actuals; §2.5 + Architecture §17):
   - Every 2025 anchor (Group Revenue, Starlink BB+DTC, Starshield, Customer Launch, EBITDA, D&A, FCF, OpEx, CapEx, F9 launches, active sats, etc.) reconciles within its documented tolerance.
   - Starting cash EoY 2024 = $5,000mm exact.

3. **Block C — Sense / sanity checks** (Rule 15 halts; raise as test failures):
   - Implied Starlink DTC subs 2025 < 15M (the disclosed Starlink total is ~5M; sanity halt threshold).
   - F9 launches 2025 ∈ [165, 177] (anchor ±5).
   - Starship launches 2025 = 0 exact.
   - Wright's Law cost-per-unit monotone non-increasing in cumulative units.
   - All margins ∈ [-1, 1] (no overflow indicators).
   - No `#DIV/0!`-equivalent (no NaN, no inf) in any year-row output.

4. **Block D — Architecture spec coverage**:
   - Every public function in `calc/` carries the four-tag docstring (§10.2) referencing an Architecture section.
   - Every Architecture spec section §1-§17 maps to at least one code module (audited via Model Translation Log).
   - Every canonical label in V2.16 column A maps to a label-registry entry OR is documented as intentionally unused.

xlsx cell-by-cell match is NOT in the pass criteria. It's a diagnostic input to §11.6.

### 11.2 Test structure

**Block A tests** (structural invariants):

```python
def test_conservation_all_years(model_result):
    for year in range(2025, 2051):
        for check_row in CONSERVATION_CHECK_ROWS:  # R99-R107
            residual = model_result.conservation_residual(check_row, year)
            assert abs(residual) < 1.0, f"R{check_row} broken at {year}: {residual:+.4f}"
        assert model_result.conservation_ok(year), f"R108 not OK at {year}"

def test_allocation_bounds(model_result):
    for year in range(2025, 2051):
        assert sum(model_result.module_cash_allocations(year)) <= model_result.available_cash(year) + 1.0
        # … etc per invariant in §11.1 Block A

def test_negative_irr_cutoff(model_result):
    for module, year in itertools.product(MODULES, range(2025, 2051)):
        if model_result.blended_irr(module, year) <= 0:
            assert model_result.cash_allocation(module, year) == 0

def test_vending_machine_framing(model_result):
    for module, year in itertools.product(MODULES, range(2025, 2051)):
        assert model_result.module_ebitda(module, year) == model_result.module_gross_profit(module, year)

def test_internal_flow_conservation(model_result):
    for flow in ["launch_services", "bandwidth", "compute"]:
        for year in range(2025, 2051):
            source_rev = model_result.internal_transfer_revenue(flow, year)
            consumer_cogs = sum(model_result.consumer_cogs(flow, m, year) for m in consumers_of(flow))
            assert abs(source_rev - consumer_cogs) < 1.0

def test_iterative_solver_converges(model_result):
    assert model_result.solver.iterations_to_converge < 100
    assert model_result.solver.final_max_residual < 0.001
```

**Block B tests** (external calibration; from `2025 Anchors from Q4_25.md` + Architecture §17):

```python
@pytest.mark.parametrize("name,target,tolerance", load_external_2025_anchors())
def test_2025_external_anchor(name, target, tolerance, model_result):
    actual = model_result.lookup_anchor(name, year=2025)
    relative_err = abs(actual - target) / abs(target) if target else abs(actual)
    assert relative_err <= tolerance, f"{name} 2025: actual={actual:,.0f} target={target:,.0f} err={relative_err:.2%} tol={tolerance:.2%}"
```

**Block C tests** (sense checks; assertions per Rule 15):

```python
def test_implied_dtc_subs_2025_sane(model_result):
    subs_2025 = model_result.starlink_dtc_subs_eoy(2025)
    assert subs_2025 < 15_000_000, f"DTC subs 2025 = {subs_2025:,.0f}; disclosed Starlink total is ~5M, halt threshold 15M"

# … etc per §11.1 Block C
```

**Block D tests** (architecture coverage; static analysis):

```python
def test_every_public_calc_function_has_full_docstring():
    for fn in iter_public_calc_functions():
        for tag in ["Excel cell:", "Excel label:", "Architecture ref:", "Principle:"]:
            assert tag in fn.__doc__, f"{fn.__qualname__} missing docstring tag {tag!r}"

def test_every_architecture_section_has_code_coverage():
    sections = parse_architecture_sections()  # §1.x … §20.x
    code_refs = parse_docstring_architecture_refs()
    uncovered = sections - code_refs
    assert not uncovered, f"Architecture sections without code: {sorted(uncovered)}"
```

### 11.3 What the xlsx diagnostic comparison looks like

Separate test module — `tests/diagnostics/test_xlsx_divergence.py` — runs alongside reconciliation but produces a **divergence report**, not pass/fail:

```python
@pytest.mark.parametrize("sheet,row,year", load_all_xlsx_formula_cells())
def test_xlsx_divergence(sheet, row, year, xlsx_snapshot, model_result, divergence_report):
    expected_xlsx = xlsx_snapshot.value(sheet, row, year)
    actual_code = model_result.lookup_by_label(sheet, row_label_of(sheet, row), year)
    delta = compute_delta(expected_xlsx, actual_code, tolerance=tolerance_for(sheet, row))
    divergence_report.record(sheet, row, year, expected_xlsx, actual_code, delta)
    # No assert — this test always "passes" structurally. The report is the artifact.
```

The divergence report aggregates: number of cells matching within tolerance, number diverging, divergences ranked by magnitude, grouped by sheet × row. Web UI consumes this for the model-health panel.

### 11.4 Tolerances (when comparing two numerical values)

These tolerances apply both to (a) external-anchor reconciliation (Block B; required) and (b) xlsx diagnostic comparison (§11.3; informational):

- **$-denominated rows**: ±$1mm absolute, OR ±0.1% relative, whichever is larger.
- **%-denominated rows**: ±1e-4 absolute.
- **IRR rows**: ±1e-3 absolute. IRR is noisier; multi-start Newton may converge to slightly different roots than Excel's IRR; both are valid solutions to the same NPV=0 equation.
- **Count rows** (sats, launches, vehicles): exact integers OR ±1 unit with explicit documentation.
- **Boolean rows** (R108-equivalent): exact equality.

### 11.5 Invariant / property tests (hypothesis-driven)

These verify Block A invariants hold under arbitrary valid Assumptions perturbations, not just the Base Case:

```python
@hypothesis.given(perturbation=valid_assumptions_perturbation_strategy())
def test_conservation_holds_under_perturbation(perturbation, base_assumptions):
    perturbed = perturbation.apply_to(base_assumptions)
    result = run_pipeline(perturbed)
    for year in range(2025, 2051):
        assert result.conservation_ok(year), f"Conservation broken under perturbation at {year}: {perturbation}"
```

If Block A invariants fail under some perturbation but hold for Base Case, the code is fragile and the failure surfaces a bug we'd otherwise miss.

### 11.6 Divergence triage workflow (when code and xlsx disagree)

When the diagnostic report (§11.3) flags a cell divergence beyond tolerance, run this triage workflow before deciding what to do:

1. **Identify the divergence**: sheet, row, year, code value, xlsx value, magnitude.
2. **Locate both sides**: which code function produced the code value? which xlsx formula produced the xlsx value?
3. **Read the spec**: what does Architecture & Methodology + Lessons Learned + Memory Snapshot say this row should compute?
4. **Classify** (one of four outcomes):
   - **(A) Code bug**: code implementation deviates from spec. → Fix code. Add unit test reproducing the bug.
   - **(B) xlsx bug**: xlsx formula deviates from spec; code is correct. → Log in `docs/xlsx_bugs_found.md` with sheet/row/year, xlsx formula, spec citation, code's correct value. Flag for Vlad sign-off; Vlad amends xlsx or accepts the divergence.
   - **(C) Intentional architectural difference**: code implements a constitutional lock the xlsx doesn't yet (e.g., Sprint 11f Option A — demand decoupled from output). → Log in `docs/intentional_divergences.md`. No fix; this is expected and documented.
   - **(D) Spec ambiguity**: both sides defensible; spec doesn't pin one. → Halt; ask Vlad to amend the Architecture spec to disambiguate. No code change until spec clarifies.
5. **Document the triage outcome** in the run audit log: `(sheet, row, year, code_val, xlsx_val, classification, citation)`.

The triage workflow is run at every reconciliation milestone, not on every PR. The divergence report (§11.3) groups cells so a single root-cause divergence (e.g., a different Group D&A formula) produces one triage entry, not 26 (one per year).

### 11.7 Reconciliation report deliverable

`docs/reconciliation_report.md` regenerated on every run:

- **Block A status**: per-invariant PASS/FAIL with year breakdown if FAIL.
- **Block B status**: per-anchor actual vs target vs tolerance with delta and PASS/FAIL.
- **Block C status**: per-sense-check actual value vs threshold.
- **Block D status**: per-section coverage gap list.
- **Diagnostic divergence summary**: matching cells / diverging cells; top 20 divergences ranked by magnitude; cumulative-by-tab table.
- **Triage log entries** open since last milestone.

Web UI exposes this as the model-health panel; clients see Block A + Block B status (operational health) and an opt-in view of the divergence summary (transparency about what is and isn't matched to xlsx).

---

## 12. Institutional & Governance Constraints

### 12.1 Model risk / audit

- Audit-grade lineage: every output traceable to its inputs through pure-function call graph.
- Reproducibility: same inputs + same code SHA = byte-identical outputs.
- Change log: every code change ≥ logic-affecting carries a Claude Log-style entry referencing the sprint or PR.
- Sign-off: numerical PASS requires all four blocks in §11.1 — Structural invariants (R108 OK, conservation, allocation bounds, vending-machine, internal flow conservation, convergence) + External Q4'25 anchors within tolerance + Sense checks + Spec coverage. xlsx divergences are triaged per §11.6 and either fixed (code bug), logged for Vlad (xlsx bug), accepted (intentional architectural difference), or halted for spec amendment (ambiguity).

### 12.2 Regulatory / compliance

- No PII in the model (it's a corporate valuation).
- No third-party data with redistribution restrictions (the model uses public anchors + Mach33 internal estimates).
- If client-facing: SOC 2-style audit trail on data access (who ran which scenario, when, with what inputs).

### 12.3 Approved / prohibited patterns

**Approved:**
- pydantic v2 for inputs
- numpy + dataclasses for calc
- pytest + hypothesis for tests
- FastAPI for service layer

**Prohibited:**
- sklearn regression-style fits for piecewise-linear lookup (Memory 2.4)
- Excel-side `SUMPRODUCT × INDEX(...,0)` patterns reproduced in code (Memory 2.3)
- Mutating global state in calc functions
- `eval` / `exec` for formula evaluation
- Hardcoded behavior constants in calc code (Rule 14)
- Cross-module imports that re-introduce demand ← output recursion (Memory 1.8)

### 12.4 Documentation deliverables

Required artifacts alongside code:
- **Model Translation Document** — auto-generated from docstrings; map of Excel cell → code function.
- **Architecture diagram** — mermaid in `docs/architecture_diagram.md`, mirrors Architecture §1 tab list.
- **Reconciliation report** — per-run, latest in `docs/reconciliation_report.md`.
- **MC methodology note** — distributions, sampling, aggregation, sensitivity methods; one page.
- **Run instructions** — `README.md` covers CLI usage; web UI has its own onboarding.
- **Development log** — `docs/DEV_LOG.md` append-only handoff for agents (S-1 P0, Block B status).
- **Changelog** — per-port-sprint, mirrors Excel Claude Log.

### 12.5 US English

All identifiers, docstrings, comments, labels, error messages, log lines: US English (Memory 3.5).

---

## 13. Success Criteria

### 13.1 Numerical PASS (v1)

- [ ] **Block A — Structural invariants** all pass (§11.1 Block A): R108 = "OK" all years; R99-R107 ≤ $1mm; allocation bounds hold; negative-IRR cutoff holds; vending-machine framing holds; internal flow conservation holds; iterative solver converges < 100 iter.
- [ ] **Block B — External calibration anchors** within tolerance (§11.1 Block B): Architecture §17 / Q4'25 actuals reproduced from first principles. Including Group Revenue 2025 $14,650mm ±5%, EBITDA $8,690mm ±5%, FCF $3,670mm ±5%, etc.
- [ ] **Block C — Sense checks** pass (§11.1 Block C): no Rule 15 halt threshold breached (DTC subs < 15M in 2025; Starship launches 2025 = 0; etc.).
- [ ] **Block D — Spec coverage** complete (§11.1 Block D): every public calc function has the four-tag docstring; every Architecture §1-§20 section has at least one code module.
- [ ] Iterative solver converges on Base Case + 3 stress scenarios (bear, bull, +Mars share).
- [ ] All Block A invariants hold under hypothesis-driven perturbation testing (§11.5).
- [ ] xlsx diagnostic divergence report generated (§11.7); each divergence outside tolerance triaged to outcome (A) / (B) / (C) / (D) per §11.6 and logged.
- [ ] Zero open triage outcomes of type (A) "code bug" or (D) "spec ambiguity."

### 13.2 Architectural PASS

- [ ] Vending-machine framing enforced (no module file imports OpEx/Tax).
- [ ] Demand decoupled from output by type (Sprint 11f Option A — Memory 1.8).
- [ ] All cross-tab references through canonical-label registry.
- [ ] All year-row computations vectorized (anchor-and-offset; no `v[t] = v[t-1] * g` outside Rule 23 exceptions).
- [ ] Conservation invariants assert at runtime.

### 13.3 MC PASS

- [ ] 7 distribution types implemented, validated against scipy reference.
- [ ] 10k-trial Base Case run completes < 60s on 16-core.
- [ ] Tornado + PRCC + 1D sweeps + 2D sensitivity table all generated.
- [ ] Per-output percentile bands (P5-P95) on Group EV, per-module EV.

### 13.4 Deliverables checklist

- [ ] Modular codebase under `src/spacex_model/`
- [ ] Model Translation Document auto-generated, current
- [ ] Reconciliation harness with full V2.16 oracle integration
- [ ] MC engine with documented methodology
- [ ] FastAPI service layer (scenario runs, MC submissions, audit endpoints)
- [ ] Web UI (consumer-facing; scenario explorer, MC dashboard, audit lineage panel)
- [ ] CLI for local runs (Base Case + MC)
- [ ] README + run instructions + architecture diagram + reconciliation report

---

## 14. Open Items & Risks

### 14.1 Open items requiring Vlad's call

1. **Sprint 11f execution timing**: Sprint 11f spec is drafted but not executed in V2.16. The code port targets Option A from day one (per §3.2). Does Vlad want the port to (a) reconcile against V2.16 as-shipped and surface Sprint 11f's expected delta as known divergence, or (b) wait for Sprint 11f PASS in Excel and reconcile against the new baseline? Default in this doc: (a). Revisit before reconciliation milestone.
2. **AI Stack module scope**: AI Stack tab is stub. The port stubs it the same way (`compute_ai_stack` returns zeros). Full AI Stack module ships when the AI Stack sprint runs (per `Colleague_A_Brief_AI_Stack.md` scoping). Code structure ready.
3. **Bridge loan repayment + interest expense**: V2.16 has $20B bridge loan inflow with no repayment / interest. STATUS notes this as deferred. Code carries the inflow; flags the repayment/interest as a known stub.
4. **Per-mission Lunar Mars IRR**: Vlad has deferred ("we can change this later"). Code keeps Lunar Mars outside the IRR queue per §11.6; per-mission engine is not built.
5. **ODC unit economics — per-sat compute revenue OR per-sat cost inputs**: Vlad-pending decision. Code uses dual-revenue Model A + Model B with credence-weight (Pr(A) = 0.6 default) per §9.2. Revisit when ODC sprint refines.

### 14.2 Risks

- **Source workbook drift**: V2.16 is mid-build. If Vlad executes Sprint 11f / 11.5 / etc. between now and code port, the **input set** (Assumptions tab additions, demand-curve breakpoint updates, opening-balance edits) may shift and the **diagnostic snapshot** the code compares against changes. Mitigation: pin V2.16 SHA at ingest time; document the input snapshot date; rerun diagnostic divergence report after any workbook update.
- **Excel iterative-calc determinism vs Python solver determinism**: Excel iterates differently per recalc; values can drift by 1e-6 across Excel sessions. Python solver is deterministic given inputs + iteration cap. Expected: minor cell-level differences within tolerance. Document.
- **IRR root-finding multi-start**: Excel's IRR can find different roots than Newton's method. For some negative-IRR streams, both Excel and our IRR return -1 (the cutoff convention). Tolerance ±1e-3 absolute should accommodate.
- **MC trial count vs runtime**: 10k trials in 60s assumes 16-core. On 4-core dev boxes, runtime scales to ~4 min. Acceptable.
- **Web UI scope creep**: client-facing UI can absorb unbounded design work. Lock v1 UI scope to: scenario picker + Group + per-module EV/FCF tables + tornado + audit lineage. Defer charts, comparables overlays, time-series animations to v2.

### 14.3 Out of scope (v1)

- Real-time data feeds (the model is annual; Q4'25 anchors are manually curated).
- Multi-user collaboration on the web UI (single-user scenarios in v1).
- Comparison views across multiple historical model versions (V30.5 vs V2.16 vs current port).
- Public S-1 import / variance analysis (`SpaceX S-1 vs Mach33 Model — Variance Analysis.xlsx` is reference only).
- Plugin-style execution chats / sprint workflow (the Excel-side process; the code port is sprint-equivalent but in PRs).

---

## 15. Reading Order for New Contributors

1. **This file** (`context.md`) — 30 min — full read; the load-bearing context.
2. `docs/DEV_LOG.md` — 5 min — latest port changes and verification commands.
3. `role.md` — 5 min — operating persona (Marcus Hale).
3. `Pre Existing Model Package/06_Memory_Snapshot/MEMORY_SNAPSHOT_CRITICAL_LOCKS.md` — 15 min — distilled locks.
4. `Pre Existing Model Package/00_Constitutional_Docs/02_Architecture_and_Methodology.md` — 45 min — skim §1-5, read §6, §10, §11, §15, §20 carefully.
5. `Pre Existing Model Package/00_Constitutional_Docs/Model Execution Rules.md` — 20 min — Rules 12, 14, 21, 23 carry into code.
6. `Pre Existing Model Package/00_Constitutional_Docs/01_Lessons_Learned.md` — 30 min — Principles 1-23.
7. `Pre Existing Model Package/01_Current_State/STATUS_2026_05_26.md` — 10 min — what state V2.16 is in.
8. `Pre Existing Model Package/01_Current_State/Sprint_11f_Spec.md` — 15 min — the Option A architectural lock the code implements from day one.
9. `Pre Existing Model Package/02_Fresh_Restart_Inputs/2025 Anchors from Q4_25.md` — 10 min — calibration targets.

Total onboarding: ~3 hours before writing any code.

---

## 16. Glossary (canonical terms — never alias)

- **Module**: one of the five P&L tabs (Customer Launch, Starlink, ODC, AI Stack, Lunar Mars). Each has a vending-machine P&L.
- **Module EBITDA**: mathematically Gross Profit (Revenue − COGS, where COGS includes fleet D&A and spectrum amort). Label retained per Principle 7; reader must understand the math.
- **Module FCF**: pre-tax, pre-corp. `EBITDA + module_D&A_addback − Module_CapEx`.
- **Allocator IN**: top-of-module-tab block reading cash + kg allocations from the Allocator.
- **Allocator OUT**: bottom-of-module-tab 11-row contract the Allocator reads (Total Revenue, Module EBITDA, Module EBITDA Margin %, Module FCF, Module CapEx, Capital deployed, Spot IRR, Forward IRR, Blended IRR, Capacity Demand kg).
- **Vending-machine framing**: P&L structure shared by all modules; no R&D / SG&A / tax / overhead.
- **Queue gate**: Allocator section that reserves non-module claims before the IRR queue allocates.
- **Sigmoid blend**: IRR-priority allocation: `weight = max(IRR, 0)^k, k=2`, `share = weight / Σ`, `alloc = min(masked_demand, available × share)`.
- **Anchor-and-offset**: year-row formula pattern `$D$anchor × (1+rate)^E$5`; vectorized in code.
- **Canonical label**: column-A row label used for INDEX/MATCH cross-tab refs; in code, a string constant in the registry.
- **Option A** (Sprint 11f): demand purely exogenous (anchor × learning + facility CapEx); output bounded by cash; never feeds back.
- **Mars carve-out**: off-the-top cash for Lunar Mars module, sized as `max(floor, prior_year_FCF × pct)`; not in IRR queue.
- **At-cost transfer**: internal flow (launch services, bandwidth, compute); fully-allocated cost (variable cash + non-cash D&A share).
- **Conservation block**: Group P&L R99-R110; R108 = "OK" required for any run to PASS.
- **2025 anchors**: locked calibration targets per Architecture §17 / Q4'25 cleanup workbook.
- **Sprint**: a discrete Excel-side change with a spec + execution chat. In code port, the analog is a PR or series of PRs scoped equivalently (3-5 logical sections per PR, per the sprint-sizing convention).

---

## 17. Decision Log (port-specific — append-only)

| Date | Decision | Rationale |
|---|---|---|
| 2026-05-28 | Reconciliation baseline = V2.16 inputs ingested; outputs independently derived from spec (NOT V2.16 cached values), with Sprint 11f Option A applied in code from day one | User amendment 2026-05-28: "I want the modeler to independently code and verify formulas and outputs. This is because if there are logic errors in the original xlsx model, I do not want those carried over." xlsx serves as input oracle + diagnostic reference only; first-principles derivation against the Architecture spec is the logic source. Supersedes the earlier "exact cell-by-cell vs V2.16" framing. |
| 2026-05-28 | Stack = Python 3.11+ / numpy / pydantic v2 / pandas (output only) / FastAPI / React + TypeScript | User: "handle a lot of complexity, transparent, eventual web UI for clients/consumers" — Python is auditor-standard; FastAPI + React is the lowest-friction transparent web layer |
| 2026-05-28 | MC engine in v1 | User explicit |
| 2026-05-28 | Tolerances locked: $-rows ±$1mm absolute / 0.1% relative; %-rows ±1e-4; IRR ±1e-3; counts exact ±1 | Aligns with R99-R107 conservation tolerance ($1mm) and standard institutional reconciliation practice. Applies to both external-anchor reconciliation (Block B; required) and xlsx diagnostic comparison (§11.3; informational). |
| 2026-05-28 | Pass criteria reframed into 4 blocks (Structural invariants / External anchors / Sense checks / Spec coverage); xlsx cell-by-cell match is diagnostic, not pass/fail | Direct consequence of the user's amendment above. The xlsx may contain bugs; pass criteria therefore measure (a) the code's adherence to internal invariants the model is supposed to obey, (b) reproduction of external real-world calibration anchors, (c) sense / sanity, (d) coverage of the spec. Divergence vs xlsx is investigated via the §11.6 triage workflow, not asserted as a test failure. |
| 2026-05-28 | Web UI v1 scope = scenario picker + Group/per-module EV + FCF tables + tornado + audit lineage panel; charts/comparables/animations deferred to v2 | Scope control; UI scope creep is the documented v1 risk |
| 2026-05-28 | S-1 adherence P0 backlog (audit §7.2): `apply_s1_adherence_overrides()` on every pipeline run; Block B tests use S-1 2025 anchors; AI Stack populated with S-1 AI + Anthropic lines + terrestrial CapEx | `SpaceX_Modeler_S1_Adherence_Audit_2026-05-28.docx`; see `docs/DEV_LOG.md` |

---

**END OF CONTEXT DOCUMENT.** Update via append (decision log, open items). Structural changes to §1-§16 require Vlad-equivalent sign-off and a Decision Log entry.
