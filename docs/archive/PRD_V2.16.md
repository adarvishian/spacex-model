# Product Requirements Document — Mach33 SpaceX Valuation Model (Python Port)

**Document version:** 1.0
**Date:** 2026-05-28
**Author:** Dr. Marcus Hale (port lead, per `role.md`)
**Status:** Locked for v1 execution. Amendments require an entry in §20 Amendment Log.

**Companion documents (read order — none of this PRD restates them; cite as authority):**

1. `role.md` — operating persona for the port lead.
2. `context.md` — living project context (1,005 lines, dated 2026-05-28). This PRD operationalizes context.md; conflicts resolve in favor of context.md unless this PRD records an explicit Decision Log entry overriding it.
3. `phase1_research_synthesis.md` — Phase 1 research artifact, dated 2026-05-28. Open questions §10 are resolved into this PRD per Vlad-equivalent sign-off 2026-05-28.
4. `Pre Existing Model Package/00_Constitutional_Docs/02_Architecture_and_Methodology.md` — authoritative architecture spec.
5. `Pre Existing Model Package/00_Constitutional_Docs/01_Lessons_Learned.md` — 23 Principles.
6. `Pre Existing Model Package/00_Constitutional_Docs/03_Sprint_Roadmap_and_Verification.md` — §6.8 revised calibration targets are the Block B target set per this PRD.
7. `Pre Existing Model Package/00_Constitutional_Docs/Model Execution Rules.md` — 23 Rules; Rules 12, 13, 14, 21, 22, 23 carry into code.
8. `Pre Existing Model Package/06_Memory_Snapshot/MEMORY_SNAPSHOT_CRITICAL_LOCKS.md` — distilled architectural locks.
9. `Pre Existing Model Package/01_Current_State/Sprint_11f_Spec.md` — Option A locked; code implements from day one.
10. `Pre Existing Model Package/01_Current_State/Sprint_11e_Spec.md` — V2.16's shipped state.
11. `Pre Existing Model Package/02_Fresh_Restart_Inputs/2025 Anchors from Q4_25.md` — informational external reasonableness anchors.

---

## §1 — Purpose, Scope, Stakeholders

### §1.1 Purpose

Port the Mach33 SpaceX Valuation Model — currently a 466 KB Excel workbook (`SpaceX Model V2.16.xlsx`) with ~10,900 formula cells across 15 sheets — to a Python codebase that meets institutional model-risk standards: audit-grade traceability, reproducible byte-stable outputs, comprehensive reconciliation, and a client-facing web UI for scenario exploration and Monte Carlo distribution viewing.

The port is **not a transliteration of the Excel formulas**. Per context.md Decision Log 2026-05-28, the code derives every value from first principles using the Architecture & Methodology spec as the logic source. The xlsx is the canonical source for inputs (Assumptions, Demand Curves, opening balances) and an informational reference for derived values. Where the xlsx implementation contains a bug the spec doesn't authorize, the code is allowed to be correct and the xlsx is allowed to be wrong; divergence is triaged per §11.6 of context.md.

### §1.2 In-scope (v1)

- Deterministic Base Case run reproducing the Mach33 architectural framing.
- Per-module 2025 calibration against the Sprint Roadmap §6.8 revised targets.
- All four reconciliation blocks (A structural / B Sprint §6.8 anchors / C sense checks / D spec coverage) passing.
- Monte Carlo engine with the seven distribution types per context.md §9.1 and the four sensitivity outputs per §9.4.
- FastAPI service layer for scenario runs, MC submissions, and audit endpoints.
- Web UI v1 per context.md §5.4: scenario picker, Group + per-module EV + FCF tables, tornado, audit lineage panel.
- Diagnostic divergence report against the V2.16 cached values per context.md §11.3, with triage outcomes per §11.6.
- Model Translation Document, reconciliation report, architecture diagram, run instructions.

### §1.3 Out of scope (v1; see §17 backlog)

- S-1 reconciliation against the SpaceX S-1 filing — **post-v1 work item per user direction 2026-05-28**.
- Real-time data feeds.
- Multi-user collaboration on the web UI.
- Comparison views across multiple historical model versions.
- Charts, comparables overlays, time-series animations on the web UI (locked per context.md §14.5).
- Bridge loan repayment + interest expense modeling (v1.1 backlog per §10.5 of phase1_research_synthesis.md).
- Customer Launch IRR engine fundamental reformulation (only the per-booster annual IRR pattern ships in v1; the documented Block C sanity failure is accepted disposition per §10.4).
- Per-mission Lunar Mars IRR engine (deferred per §10.7; pluggable hook only).
- AI Stack full three-sub-module body (stub only in v1 per §10.3; structural pre-wire in place for Sprint 6 to land later).

### §1.4 Stakeholders & sign-off authority

- **Architecture sign-off:** Vlad (per context.md §1.3). Any deviation from Architecture & Methodology §1–§20 requires updating that doc first.
- **Numerical sign-off:** Vlad, against the four-block pass criteria in §10 of this PRD. xlsx cell-by-cell match is diagnostic per §11.6 of context.md, not a sign-off criterion.
- **Port lead:** Dr. Marcus Hale (this document's author).
- **Consumer-facing sign-off:** the web UI surfacing the model must show audit-grade lineage (every output traceable to its calculation function + the input set that produced it).

### §1.5 Authority hierarchy

When sources conflict, the higher authority wins. From highest to lowest:

1. `02_Architecture_and_Methodology.md` (constitutional architecture & methodology) — locks structural and methodological decisions.
2. This PRD — locks the Python port's interpretation of the architecture.
3. `context.md` — living project context; binds where not amended by §1.5.1–§1.5.2 above or by this PRD's Decision Log.
4. `Sprint Roadmap §6.8` (revised 2026-05-22) — Block B calibration targets.
5. The remaining constitutional documents (Lessons Learned, Execution Rules, Memory Snapshot, sprint specs, anchors) — operationalize §1.5.1–§1.5.4.
6. `V2.16.xlsx` cached values — diagnostic reference for §11.6 triage only.

### §1.6 Decision log (port-specific, locked 2026-05-28)

Per phase1_research_synthesis.md §10 Vlad-equivalent sign-off:

| Ref | Decision | Source |
|---|---|---|
| D1 | Block B reconciliation target = Sprint Roadmap §6.8 revised set (Group EBITDA 2025 = $4,904M; Group FCF 2025 = −$2,569M). Q4'25 raw figures are informational external reasonableness anchors only. | §10.1 |
| D2 | Sprint 11f Option A applied from day one. Code reconciles against V2.16 with the Option A divergence classified as type (C) intentional architectural difference. | §10.2 |
| D3 | AI Stack v1 = zeros stub. Three-sub-module architecture (Compute / Application / Orchestration) pre-wired structurally; full body lands in v1.x when Sprint 6 / AI Stack scoping doc Q1–Q8 are Vlad-locked. | §10.3 |
| D4 | Customer Launch F9 IRR Block C sanity failure accepted as known disposition; recorded in run audit log. v1 implements per-booster annual IRR pattern (mirroring Starlink). | §10.4 |
| D5 | Bridge loan v1 carries V2.16 stub: $20B drawn 2025, no repayment, no interest. v1.1 backlog. | §10.5 |
| D6 | ODC accepts model verdict (negative per-sat IRR throughout horizon under V2.16 input set → zero deployment). Per-sat revenue and cost exposed as MC inputs for scenario stress. | §10.6 |
| D7 | Mars per-mission IRR deferred. LM stays strategic carve-out + BV engine. Pluggable hook in code. | §10.7 |
| D8 | Web UI v1 scope locked per context.md §5.4 / §14.5. | §10.8 |
| D9 | Repository layout per context.md §5.3 adopted as-is. | §10.9 |
| D10 | S-1 reconciliation is a post-v1 work item. v1 ships and is signed off before S-1 reconciliation begins. | User direction 2026-05-28 |

---

## §2 — Architectural locks (binding, non-negotiable)

These are inherited from the constitutional layer and recorded here so the PRD is self-contained. Each lock has a code implication and a test that enforces it.

### §2.1 Vending-machine module framing

**Lock:** Module P&L = `Revenue → COGS → Gross Profit = Module EBITDA → CapEx → Module FCF`. No R&D, no SG&A, no corporate overhead, no taxes on any module. Architecture §3, Principle 8, Rule 13.

**Code implication:** each `calc/modules/<module>.py` has the five-section structure (`compute_revenue`, `compute_cogs`, `compute_gross_profit`, `compute_capex`, `compute_fcf`). The Module EBITDA label is retained mathematically equal to Gross Profit per Principle 7.

**Enforcement test:** a static-analysis test asserts no module file imports `calc/opex.py`, `calc/group_pnl.py::compute_taxes`, or any function whose qualified name contains `tax` or `corporate_overhead`. Failure halts the build.

### §2.2 Demand purely exogenous — Sprint 11f Option A

**Lock:** Demand reads `anchor × learning × year_mask + exogenous_facility_capex`. Output reads `MIN(cash_from_allocator / unit_cost, internal_target)`. Output never feeds back into demand. Architecture §6.5 + §20.3 amendments, Memory 1.8, Sprint_11f_Spec §2.

**Code implication:** `DemandInputs` and `DemandResult` are frozen dataclass types in `calc/<module>/demand.py`. `OutputResult` is a distinct frozen dataclass in `calc/<module>/output.py`. `compute_demand(...)` takes only `DemandInputs`. `compute_output(...)` takes `DemandResult + AllocatorAllocation`.

**Enforcement test:** an `inspect`-based test imports both function signatures and asserts the demand-function call graph (via `ast`-walk of the module's source) contains no reference to `OutputResult` or any name beginning with `output_`. Failure halts the build.

### §2.3 Anchor-and-offset year-row pattern

**Lock:** deterministic ramps use `$D$anchor × (1+rate)^E$5` in Excel; vectorized numpy expression over the offset vector in code. No `v[t] = v[t-1] × g` recursion outside Rule 23 exceptions. Architecture §16, Rule 23, Principle 12.

**Code implication:** year vectors are length-26 `np.ndarray` indexed `[0..25]` = years `[2025..2050]`. Year-chained Rule 23 exceptions (Cash BoY, cumulative CapEx, BV running sums, ratchet latches, EoY = BoY + adds − retires) are flagged inline in a `"Rule 23 exception: <reason>"` docstring line.

**Enforcement test:** the docstring linter (§14.3) checks every year-chained function (identified by a `@year_chained` decorator) has the Rule 23 justification line.

### §2.4 Cross-tab references by canonical label only

**Lock:** every cross-module reference resolves via the canonical-label registry. No integer row indexing of result containers. Architecture §16, Rule 12, Principle 3 / 14.

**Code implication:** `config/canonical_labels.py` exposes a string constant for every label used across modules. Code never inlines string literals that look like labels. The registry is populated from V2.16's column-A labels via a one-time extraction script (`scripts/extract_canonical_labels.py`), then is append-only.

**Enforcement test:** (a) a regex linter scans all `calc/` files for string literals matching the label-shape pattern (`[A-Z][a-zA-Z ]+\([a-z/$ ]+\)` etc.) and fails if any are not registry entries; (b) a registry-completeness test asserts every column-A label in V2.16's value pass resolves to a registry entry OR is recorded in `docs/intentionally_unused_labels.md`.

### §2.5 Queue gate reserves non-module claims first

**Lock:** `Available_cash_for_IRR_queue = max(0, Cash_BoY − OpEx − Corp_CapEx − Spectrum_CapEx − Taxes − Mars_carveout − Vehicle_build_claim)`. Architecture §6.2, Principle 4, Memory 1.4.

**Code implication:** `calc/allocator/queue_gate.py::available_cash_for_irr_queue(...)` is the single function that computes this. All module cash allocations downstream of it depend on its output.

**Enforcement test:** an invariant test asserts `sum(module_cash_allocations(year)) ≤ available_cash_for_irr_queue(year) + 1.0` every year.

### §2.6 Per-unit marginal IRR

**Lock:** `CF stream = [−cost_per_unit(T), net_marginal_revenue(T+1), …, net_marginal_revenue(T+N)]`; `Spot IRR(T)`, `Forward IRR(T+2)`, `Blended IRR = 0.3 × Spot + 0.7 × Forward` (w = 0.7 per Assumptions). Architecture §5, Memory 1.5, Principle 2.

**Code implication:** `domain/irr.py` exposes a single `compute_irr_engine(...)` function that takes per-unit cost + per-unit net marginal revenue + N + forward_weight and returns `IrrResult { spot, forward, blended }`. Used by Starlink (per vehicle × 4), Customer Launch (per booster × 2: F9, Starship), ODC (per sat), AI Stack (when full body lands; per product). Lunar Mars has no IRR engine.

**Enforcement test:** per-engine unit tests cover edge cases — all-negative cash flows return `−1.0` (cutoff convention), all-positive cash flows return a valid IRR, multi-start Newton converges to the right root for mixed-sign streams.

### §2.7 Vehicle-level Allocator for Starlink

**Lock:** V2 BB / V2 DTC / V3 BB / V3 DTC are top-level allocator queue entries with per-vehicle IRR. V2 vehicles have NO kg allocation row (fly on F9, not Starship). Three physical gates: V3 startup year (= 2027), V2 phase-out year (= 2028, MC-variable), F9 supply gate (for V2 deployment). Architecture §20.1 / §20.2 / §20.6.

**Code implication:** Starlink's Allocator IN block reads four cash allocations and two kg allocations (V3 BB, V3 DTC); the gates are evaluated in `compute_demand(...)` and produce a zero demand vector for the gated years. V2→V3 transition emerges from sigmoid weighting + the gates; no ratchet flag.

**Enforcement test:** parametrized invariant tests: for V2 BB and V2 DTC, demand = 0 in every year ≥ V2 phase-out year; for V3 BB and V3 DTC, demand = 0 in every year < V3 startup year.

### §2.8 Mars carve-out off the top, prior-year FCF

**Lock:** `Mars_carveout(T) = max(Mars_floor, Group_FCF(T−1) × Mars_pct)`. Architecture §6.2 / §11.1, Principle 22.

**Code implication:** the carve-out reads `Group_FCF[T−1]`, not `Group_FCF[T]`. This is the circularity breaker. `Mars_pct` and `Mars_floor` are both MC-variable.

**Enforcement test:** static analysis asserts the carve-out function signature takes `prior_year_group_fcf` (not `group_fcf` indexed by year). At runtime, asserts the carve-out value for 2025 = `max(Mars_floor, 0)` because there's no 2024 Group FCF in scope.

### §2.9 Internal transfer 4-step pattern, fully-allocated

**Lock:** source books internal transfer revenue, consumer books matching cost in COGS, Group P&L elimination row subtracts once, conservation check row verifies `source_rev = Σ consumer_cogs`. All three transfer prices (launch services, bandwidth, compute) are **fully-allocated** (variable cash cost + non-cash D&A share) per the 2026-05-20 accounting methodology lock. Architecture §7.1 / §7.2 / §7.3, Principle 9, Rule 21.

**Code implication:** three internal-flow modules in `calc/internal_flows/`: `launch_services.py`, `bandwidth.py`, `compute.py`. Each exposes a `rate_per_unit(...)` function (fully-allocated) and a `conservation_residual(...)` function.

**Enforcement test:** Block A invariant — for each flow `f`, `abs(internal_transfer_revenue[f](year) - sum(consumer_cogs[f](year) for consumer in consumers_of(f))) < 1.0` every year.

### §2.10 LM BV = SoTP terminal value INPUT, NOT P&L D&A flow

**Lock:** Lunar Mars Module D&A in Group P&L = proper cash-cap depreciation (cumulative LM Module CapEx ÷ capital_lifetime 10y). BV decay rows are memo-only inputs to the Valuation tab terminal anchor (`1.5 × Lunar+Mars BV at 2050`). Architecture §20.5, Sprint 11e shipped.

**Code implication:** `calc/lunar_mars/bv_engine.py` produces `accumulated_book_value` (Valuation input) and `module_da` (Group D&A input). The two are different quantities with different consumers. Group D&A formula reads `module_da`, never `accumulated_book_value × decay_rate`.

**Enforcement test:** static analysis asserts `group_pnl.compute_group_da(...)` has no transitive reference to `accumulated_book_value` symbol or to any function whose name contains `bv_dep`.

### §2.11 Iterative-calc convergence

**Lock:** 100 iterations max, 0.001 absolute tolerance. Genuine simultaneity loops: Starlink ↔ Starlink Capacity, Allocator ↔ modules, Cash BoY ↔ Group FCF (broken with t-1 read). Memory 1.6.

**Code implication:** `engine/iterative_solver.py` is an explicit fixed-point solver with damping (default 0.5), convergence asserted not assumed, per-iteration max-residual trace saved to audit log. Non-convergence raises `NonConvergenceError`.

**Enforcement test:** a reconciliation test asserts the Base Case run converges in < 100 iterations with final max residual < 0.001.

### §2.12 No row insertions / no version surfacing / US English

**Lock:** label-registry is append-only; version numbers (V2.16, V2.17, etc.) not surfaced in code or user-facing state; US English everywhere (modeling, optimization — not modelling, optimisation). Rule 10, Memory 3.2, Memory 3.5.

**Code implication:** the canonical-label registry is checked in as append-only via a CI test that diffs against the prior commit. Git SHA may appear in internal audit logs; never in client-facing UI. A spell-check CI step enforces US English on `*.py`, `*.md`, `*.yaml`, `*.json` files.

**Enforcement test:** see Code implication; CI lint job.

### §2.13 Pre-IPO debt facility

**Lock:** `Cash_BoY(N) = Cash_BoY(N−1) + Group_FCF(N−1) + IPO_injection(N) + Pre_IPO_debt_facility(N)`. $20B drawn in 2025 per S-1 disclosure, $0 from 2026 onwards (Base Case). Architecture §20.9.

**Code implication:** `Pre_IPO_debt_facility` is a year-vector Assumptions input. v1 carries no repayment or interest (per D5).

**Enforcement test:** Block A invariant — R109 cash flow identity includes the bridge loan term: `Σ bridge_loan_drawdown ∈ cash_identity_equation`.

### §2.14 Pre-revenue R&D switching formula

**Lock:** for ODC and AI Stack, `R&D_t = MAX($-profile_t, % × revenue_t)`. Architecture §12.1 amendment 2026-05-20.

**Code implication:** `calc/opex.py` exposes a `switching_rd(module, year, dollar_profile_vec, pct_rate, revenue_vec)` helper. ODC and AI Stack R&D rows use this; Starlink, Customer Launch, Lunar Mars use the standard `% × revenue` form (Lunar Mars uses a $-profile only, no `%` since revenue = 0).

**Enforcement test:** unit test asserts that for ODC year 2025 (where revenue = 0), the R&D output equals the ODC R&D $-profile ($200M Base Case).

### §2.15 Fully-allocated at-cost transfer pricing

**Lock:** rate per launch = variable cost + vehicle D&A per launch; rate per Gbps/yr = pool cost basis ÷ total active pool Gbps (BB pool basis includes spectrum amort); rate per PFLOP-hr = ODC fully-allocated annual cost ÷ ODC total annual PFLOP-hrs. Architecture §7.1 / §7.2 / §7.3.

**Code implication:** the three rate functions are in `calc/internal_flows/`. Each produces a single per-year rate that is the same for all consumers of that flow.

**Enforcement test:** invariant — for each year, `len(set(rate_charged_to_consumer)) == 1` (all consumers see the same rate).

### §2.16 First-year (2025) override

**Lock:** column D (2025) module CapEx = historical actual, locked. Allocator drives column E:AC (2026+) only. Architecture-equivalent locked at Sprint Roadmap §6.9 / Assumptions Tab Spec §5.

**Code implication:** the Allocator's per-module output exposes `cash_allocation[0]` as `MAX(allocator_proposed_allocation[0], historical_actual_2025)`. The historical-actual values are Assumptions inputs (V2 BB 2,987 launched, V2 DTC 182, F9 manufactured 17, F9 customer launches 38.58, etc.).

**Enforcement test:** parametrized test — for each module, `module_capex[year=2025] == historical_actual_2025` exactly.

---

## §3 — Architecture & Topology

The code's module structure mirrors the Excel tab inventory but reorganizes the work by code dependency graph rather than Excel cell-write graph. Repository layout per context.md §5.3 (adopted as-is per D9).

### §3.1 Module dependency graph

```
[Foundation: config + canonical_labels + units + year_vector + Assumptions ingest + IRR engine]
                                  │
                                  ▼
[Module shells: vending-machine framing + Allocator OUT contract — all 5 modules, OpEx, CapEx, Group P&L, Valuation]
                                  │
                                  ▼
[Per-module calc in dependency order:]
       ┌──────────────────────────┼──────────────────────────┐
       ▼                          ▼                          ▼
[Launch Capacity]          [Lunar Mars]                   [Demand Curves]
       │                          │                          │
       ▼                          │                          ▼
[Customer Launch]                 │                  [Starlink + Starlink Capacity]
                                  │                          │
                                  │                          ▼
                                  │                       [ODC]
                                  │                          │
                                  │                          ▼
                                  │                       [AI Stack stub]
                                  │                          │
                                  └──────┬───────────────────┘
                                         ▼
                                       [OpEx]
                                         │
                                         ▼
                                       [CapEx]
                                         │
                                         ▼
                                       [Group P&L + Conservation]
                                         │
                                         ▼
                                       [Valuation]
                                         │
                                         ▼
[Allocator brain + iterative solver — closes the loops; Sprint 11f Option A enforced]
                                  │
                                  ▼
[Reconciliation framework — Blocks A/B/C/D]
                                  │
                                  ▼
[MC engine]
                                  │
                                  ▼
[FastAPI service layer]
                                  │
                                  ▼
[Web UI v1]
```

### §3.2 Iterative-solve loops (per §2.11)

Three within-year simultaneity loops resolve via fixed-point iteration:

1. **Starlink ↔ Starlink Capacity** (%×Revenue cycle): Starlink revenue depends on available BB Gbps; Starlink Capacity computes available Gbps net of ODC internal claim; ODC bandwidth claim depends on ODC compute output, which depends on ODC revenue, which depends on Starlink Capacity at-cost rate.
2. **Allocator ↔ modules**: module CapEx ← module cash allocation ← module Blended IRR ← module FCF ← module CapEx. Sprint 11f Option A weakens this by decoupling demand from output, but the output side still loops via `cash_allocation → CapEx → FCF → next year`.
3. **Cash BoY ↔ Group FCF**: broken by the t-1 read in the cash pool tracker and Mars carve-out.

Convergence target: < 100 iterations, < 0.001 absolute residual on every monitored quantity. Damping 0.5 default. Per-iteration trace saved to audit log.

### §3.3 Cross-tab references

All cross-module references resolve through `config/canonical_labels.py`. Code never indexes by integer row. The registry is populated from V2.16's actual column-A labels via `scripts/extract_canonical_labels.py` (run once during Phase A); thereafter it is append-only with CI enforcement.

---

## §4 — Module Functional Requirements

Each module specification below has the same structure: Purpose, Upstream dependencies, Inputs (canonical labels read), Calculations (algorithm summary with spec citations), Outputs (canonical labels published), IRR engine (if applicable), 2025 calibration target with tolerance and halt threshold, Block A invariants the module preserves, Block C sense checks, Known edge cases / open threads.

### §4.1 Launch Capacity (`calc/launch_capacity.py`)

**Purpose.** Supply-side tab: Starship + F9 fleet, Wright's Law cadence, $/kg cost stack, vehicle D&A, at-cost launch services rate. NOT a P&L module (no vending-machine output).

**Upstream dependencies.** Assumptions §3 Capacity inputs only.

**Inputs (Assumptions §3):** Super Heavy mfg cost, Starship 2nd-stage mfg cost, Starship payload (booster-only mode 150K kg, fully reusable 100K kg), F9 mfg cost, F9 payload 22.8K kg, F9 base build rate 8/yr, F9 build-rate decay window 8 years, V3 Starlink launch trigger year 2027, Wright's Law manufacturing learning rate, cum-units anchor, launches per Starship vehicle per year (B500 = 24), etc.

**Calculations.**
- Booster build per year (units) = `IFERROR(vehicle_build_claim_cash / blended_cost_per_starship_vehicle, 0)` per Architecture §20.4. Per Phase D, this reads from Allocator vehicle build claim.
- Booster fleet EoY = BoY + built − retired (Rule 23 exception).
- Total Starship launches per year = fleet × launches per Starship per year (Wright's-Law-modulated cadence).
- Total Annual Capacity (kg-to-LEO) = launches × per-launch upmass.
- F9 fleet build: pre-V3-trigger at base rate (8/yr); post-trigger linear decay over R57 window (8 years).
- F9 retired per year: launch-driven (1% of booster life per launch per Sprint 2→3 patch).
- F9 launches per year: demand-driven sum of F9 Starlink internal (V2 BB + V2 DTC) + F9 customer.
- Vehicle D&A = cumulative vehicle CapEx through year T ÷ weighted-average useful life.
- At-cost launch services rate = variable cost per launch + vehicle D&A per launch per Architecture §6.6 (fully-allocated lock 2026-05-20).

**Outputs (canonical labels published):** `Total Starship launches per year`, `Total Annual Capacity (kg-to-LEO)`, `F9 launches per year`, `F9 fleet end-of-year`, `F9 manufactured per year (boosters)`, `Per-launch upmass (kg)`, `Annual vehicle D&A ($mm)`, `At-cost launch services rate ($mm/launch)`, `Blended cost per Starship vehicle`.

**IRR engine:** none (supply-side tab; not a P&L module).

**2025 calibration (per Sprint Roadmap §6.1):**
- F9 total launches = 171 ±5; HALT if < 160 or > 185.
- F9 fleet end-2025 = 39 ±5; HALT if < 30 or > 50.
- F9 manufactured 2025 = 17 ±2; HALT if < 13 or > 22.
- Starship launches = 0 exact; HALT if > 0.
- Total Starship capacity (kg) ~450K ±30%; HALT if < 250K or > 700K.
- Blended $/kg ∈ [$400, $800].

**Block A invariants preserved:**
- Vehicle D&A appears exactly once in Group D&A (via consuming modules' COGS lines, not as a separate line). R103 D&A check catches double-counting.
- At-cost launch services rate is fully-allocated (variable + D&A share). All consumers see the same rate.

**Block C sense checks:**
- Cost-per-unit monotone non-increasing in cumulative units (Wright's Law).

**Known threads:**
- F9 launches per year is a sum from downstream consumers (Starlink V2 + Customer Launch). Iterative-solver dependency.

### §4.2 Customer Launch (`calc/customer_launch.py`)

**Purpose.** Module: F9 + Starship external customer launches + at-cost internal launch transfer to consuming modules. Per-booster annual marginal IRR (mirroring Starlink pattern per Customer_Launch_IRR_Fix_Plan.md).

**Upstream dependencies.** Launch Capacity (kg, launches, at-cost rate, vehicle D&A).

**Inputs (Assumptions §4):** F9 customer launch price 2025 = $111M (Q4'25 anchor R195 correction), CAGR. Starship customer launch price = $100M in 2027, −8%/yr decline. F9 customer launches market sizing (= 38.58 in 2025 per Q4'25 anchor). Starship customer launches year-row (= 0 through 2026). Cost components: variable cost per launch, insurance %, other COGS %.

**Calculations.**
- External revenue = F9 customer launches × F9 customer launch price + Starship customer launches × Starship customer launch price.
- Internal transfer revenue = (F9 internal launches + Starship internal launches) × at-cost launch services rate per Architecture §7.1.
- F9 internal launches = Starlink V2 BB launches + Starlink V2 DTC launches per Sprint 2→3 patch (Starlink consumes F9 for V2).
- Starship internal launches = Starlink V3 BB + V3 DTC + ODC launches.
- Total revenue = external + internal.
- COGS: at-cost rate × (F9 customer + Starship customer launches) — Customer Launch pays at-cost for the launches it consumes (i.e., its OWN external customer launches; this is the trick — Customer Launch's per-launch margin is its external price minus at-cost rate).
- Per-booster annual IRR: per Customer_Launch_IRR_Fix_Plan.md §2. CF stream = [−(booster_mfg_cost + facility_allocation_per_booster), +per_booster_annual_margin × N years]. N = booster economic life in years. Per-booster annual margin = (external_price − at_cost_rate − insurance% − other_COGS%) × cadence_per_booster_per_year. Forward IRR offsets +2 years. Blended IRR = 0.3 × Spot + 0.7 × Forward.

**Outputs:** `Total Revenue ($mm)`, `Module EBITDA ($mm)`, `Module FCF ($mm)`, `Module CapEx ($mm)` (ground equipment + customer integration; NOT vehicle build), `Capital deployed ($mm)`, `Spot IRR`, `Forward IRR (Y+2)`, `Blended IRR`, `Capacity Demand (kg-to-LEO)` (= Starship customer launches × per-launch upmass per Architecture §20.7).

**IRR engine:** per-booster annual, two-engine (F9 + Starship), blended at module level by weighted launches.

**2025 calibration (per Sprint Roadmap §6.2):**
- F9 customer launches = 38.58 ±2; HALT if < 30 or > 50.
- F9 customer revenue = $4,290M ±5%; HALT if < $3,800M or > $4,800M.
- F9 customer launch price = $111M ±5%; HALT if < $95M or > $130M.
- Starship customer revenue = $0 exact; HALT if > 0.

**Block A invariants preserved:**
- Internal transfer revenue (Customer Launch booked) = Σ Launch services cost (Starlink, ODC consumers' COGS) — R105 conservation check.
- No vehicle build cost in Module CapEx (that's at the queue gate per §6.6).

**Block C sense checks:**
- Per-launch Blended IRR ∈ [8%, 25%] is the published target. **Per D4, F9 IRR is expected to fail this check; documented disposition; recorded in run audit log, no halt.**

**Known threads:**
- The F9 IRR will print high (estimated ~1700% per Customer_Launch_IRR_Fix_Plan §7) because the per-booster cost slug is thin relative to the cashflow stream it underwrites. Mitigated by D4: failure is accepted disposition. The Allocator queue will over-prioritize Customer Launch; expected and documented.

### §4.3 Starlink + Starlink Capacity (`calc/starlink/`)

**Purpose.** Most complex module. Two tabs / two sub-packages. Starlink = BB + DTC + Starshield revenue, constellation D&A, terminal COGS, spectrum amort, V2/V3 vehicle queue. Starlink Capacity = bandwidth aggregation, internal claim to ODC, at-cost transfer pricing per pool.

**Upstream dependencies.** Launch Capacity (kg, launches, at-cost rate). Demand Curves (BB + DTC piecewise-linear lookup).

**Sub-package structure:**
- `calc/starlink/module.py` — top-level orchestrator.
- `calc/starlink/vehicle_pools.py` — V2 BB / V2 DTC / V3 BB / V3 DTC per-vehicle sigmoid blend (Architecture §8.1).
- `calc/starlink/deorbit.py` — V2 historical fleet retirement (5,246 V2 BB + 650 V2 DTC linear over N=5 years per §8.3).
- `calc/starlink/revenue_curve.py` — bandwidth-driven revenue via Demand Curves piecewise-linear lookup with multiplicative annual TAM shift `(1+inflation)^t × (1+GNI)^t` per Sprint 10.5.
- `calc/starlink/per_vehicle_irr.py` — per-vehicle marginal IRR engines (4 engines: V2 BB, V2 DTC, V3 BB, V3 DTC).
- `calc/starlink_capacity.py` — bandwidth aggregation, ODC internal claim, at-cost pricing per pool.

**Inputs (Assumptions §5):** sat physical specs per vehicle (mass, BB Gbps, DTC Gbps), satellite cost per kg (Wright's Law learning rate), V2 BB sat unit cost, V2 DTC sat unit cost, V3 BB sat unit cost, V3 DTC sat unit cost, facility CapEx per sat per vehicle, V3 Mass (kg), V2 Mini BB Sats Launched 2025 = 2,987 (first-year anchor), V2 Mini DTC Sats Launched 2025 = 182 (first-year anchor), Starshield Reserved % decay rate = 0.25 (Q4'25 anchor R53 correction), Starshield Rev per Gbps base = $164,699 (Q4'25 anchor R54 correction), V2 BB historical baseline = 5,246, V2 DTC historical baseline = 650, BB ARPU 2025 $100/mo → $75/mo 2030 (flat), DTC ARPU 2025 $16/mo → $10/mo 2030 (flat), V2 phase-out year = 2028 (Assumptions R350; MC range 2026–2032 triangle), CapEx Lag = 1 year (Assumptions R82).

**Calculations (Starlink):**
- Active V2 BB fleet = historical baseline + Σ V2 BB launched − Σ V2 BB deorbit − Σ V2 BB opening-balance deorbit.
- Active V2 DTC fleet, V3 BB fleet, V3 DTC fleet (same pattern).
- Total active sats = sum of four fleets + legacy V1/V1.5 residual.
- V2 BB launches per year: per Sprint 11f Option A, demand is exogenous (anchor × learning × year-mask + facility CapEx); output is `MIN(cash_allocation / unit_cost, F9_supply_constraint, internal_uncapped_target)`. V2 phase-out gate zeros demand for year ≥ V2 phase-out year.
- V3 BB / V3 DTC launches per year: same pattern; V3 startup gate zeros demand for year < V3 startup year; kg constraint applies (`D12_kg / V3_Mass`).
- BB Gbps = sum over vehicles of active fleet × BB Gbps per sat.
- DTC Gbps = sum over vehicles of active fleet × DTC Gbps per sat.
- BB Revenue = Demand Curves BB piecewise-linear lookup(Available BB Gbps, year) × annual TAM shift.
- DTC Revenue = Demand Curves DTC piecewise-linear lookup(Available DTC Gbps, year) × annual TAM shift.
- Starshield Revenue = Starshield Reserved Gbps × Starshield Rev/Gbps × (1 − decay)^year_offset.
- Hardware Revenue (Terminals) = Net subscriber adds × blended retail price per terminal.
- Net subscriber adds = (BB Revenue / BB ARPU − BB Revenue prior year / BB ARPU prior year) + DTC equivalent. Derived per Architecture §8.4.
- Constellation D&A = active mass × $128.80/kg (or computed per cumulative CapEx ÷ useful life).
- Spectrum amort (BB only) = read from CapEx tab `Annual spectrum amortization`.
- Terminal COGS = Net adds × terminal COGS per unit.
- Total COGS = Constellation D&A + Launch services cost (Σ V2 launches × at-cost F9 rate + Σ V3 launches × at-cost Starship rate) + Ground ops % × Revenue + Spectrum amort + Terminal COGS + Insurance % × Revenue + Other COGS % × Revenue.

**Calculations (Starlink Capacity):**
- Total BB Gbps from Starlink, Total DTC Gbps.
- ODC bandwidth claim (read from ODC).
- Available BB Gbps for external = Total BB − ODC BB claim.
- Available DTC Gbps for external = Total DTC − ODC DTC claim.
- BB pool cost basis = Gbps-share-weighted Constellation D&A + Ground ops + Spectrum amort (BB only).
- DTC pool cost basis = same minus Spectrum.
- BB at-cost rate $/Gbps/yr = BB pool cost basis ÷ Total active BB Gbps.
- DTC at-cost rate = analogous.

**Outputs:** standard Allocator OUT (Total Revenue, Module EBITDA, etc.) at module level + per-vehicle CapEx + per-vehicle IRR memo rows. Plus from Starlink Capacity: `Available BB Gbps`, `Available DTC Gbps`, `BB at-cost rate ($/Gbps/yr)`, `DTC at-cost rate ($/Gbps/yr)`.

**IRR engines:** four — V2 BB, V2 DTC, V3 BB, V3 DTC. Per-sat per-year marginal economics. CF stream length N+1 = 6 (N = 5 design life).

**2025 calibration (per Sprint Roadmap §6.3):**
- Starlink BB + DTC revenue = $7,852M ±5%; HALT if < $7,000M or > $8,700M.
- DTC = $157M ±15%; HALT if < $80M or > $250M.
- Starshield = $2,520M ±5%; HALT if < $2,200M or > $2,900M.
- Active V2 BB sats end-2025 = 5,246 exact (hardcoded baseline).
- Active V2 DTC sats end-2025 = 650 exact.
- V2 BB launched 2025 = 2,987 exact (first-year override per §2.16).
- V2 DTC launched 2025 = 182 exact.
- Total active sats end-2025 ∈ [6,650, 9,800] (depends on V1/V1.5 inclusion convention).
- V3 launches 2025 = 0 exact.
- Constellation D&A = $707M ±10%.
- Module EBITDA margin ∈ [55%, 75%].

**Block A invariants preserved:**
- Per-vehicle EBITDA = per-vehicle Gross Profit (vending-machine).
- Sum of per-vehicle launches × at-cost rate = Internal launch services cost (consumer side of Customer Launch's internal flow).
- Bandwidth flow: ODC pays Σ (its Gbps claim × pool rate) = Starlink internal bandwidth revenue.

**Block C sense checks:**
- Implied total Starlink subs end-2025 ∈ [5.5M, 7.5M]; HALT if < 3M or > 10M.
- Implied DTC subs 2025 < 15M (Mach33 disclosed ~5M total Starlink; halt at 3× total).

**Known threads:**
- The Starlink ↔ Starlink Capacity %×Revenue loop is the canonical iterative-solver loop. Loop monitored quantities: Total BB Gbps, Total DTC Gbps, BB Revenue, DTC Revenue, ODC bandwidth claim.

### §4.4 ODC (`calc/odc.py`)

**Purpose.** Orbital compute satellites. Dual revenue (Model A energy-anchored + Model B η-anchored) credence-weighted. Per-sat marginal IRR. Cash-driven deployment.

**Upstream dependencies.** Launch Capacity (kg). Starlink Capacity (BB + DTC at-cost rates for bandwidth services cost).

**Inputs (Assumptions §6):** ODC compute power per sat = 140 kW (V30.5 V2 Compute config, Vlad-confirmed). Solar gen per sat 156 kW. Thermal mass 480 kg. Chip cost per chip × chip count per sat. ODC fleet design life N = 5 years. Per-sat external compute revenue (= $0 in 2025, $0.5M in 2030+ per V2.16 baseline; **MC-variable per D6**). CoreWeave $/GW_IT/yr 2026 baseline = $12B. Orbital PUE = 1.12. Pr(A) credence default = 0.6 (MC-variable). F_ref H100 = 1979, ECR = 0.6, Workload mix 85% inference. Internal compute share to AI Stack year-row (default trajectory 95% in 2025 → 50% in 2040 → 40% in 2050).

**Calculations.**
- Per-sat Model A revenue = (compute_power/1e6) × CoreWeave_baseline_year × PUE_uplift × util_factor × 1000.
- Per-sat Model B revenue = (compute_power / chip_TDP) × chip_FP8 / 1e6 × 8760 × util × ECR × price_per_GPU_hr / 1e6.
- Per-sat combined revenue = Pr(A) × A + (1 − Pr(A)) × B.
- Per-sat marginal opex = combined revenue × (ground_ops% + insurance% + other%).
- Per-sat bandwidth cost = (per-sat BB Gbps + DTC Gbps) × respective $/Gbps from Starlink Capacity.
- Per-sat net marginal revenue = combined revenue − opex − bandwidth.
- Cost per sat ($mm) = sat unit cost (subsystems + chips) + launch cost per sat.
- Per-sat Spot IRR, Forward, Blended IRR with N=5.
- Wanted deployment in cash terms = wanted_sat_count × cost_per_sat (per Sprint 11f Option A; demand exogenous).
- Actual deployment = MIN(cash_allocation / cost_per_sat, kg_allocation / mass_per_sat, internal_uncapped_target). Per D6, allocator allocations expected to be zero throughout horizon → actual deployment = 0.
- ODC external compute revenue = external_share × Fleet PFLOPS × external $/PFLOP-hr.
- ODC internal transfer revenue = internal_share × Fleet PFLOPS × internal at-cost rate per PFLOP-hr.
- At-cost rate per PFLOP-hr (fully-allocated per Architecture §7.3) = (annual sat D&A + annual launch services cost + annual bandwidth services cost + insurance + other COGS) ÷ annual Fleet PFLOP-hrs.

**Outputs:** standard Allocator OUT. Plus `ODC at-cost compute rate ($/PFLOP-hr)`, `Internal compute transfer revenue ($mm)`, `External compute revenue ($mm)`, `Bandwidth services cost ($mm)`, ODC bandwidth claim (BB Gbps and DTC Gbps to Starlink Capacity).

**IRR engine:** per-sat per-year marginal economics. Reads external compute revenue only (Principle 9 — internal at-cost transfers don't contribute IRR signal).

**2025 calibration (per Sprint Roadmap §6.4):**
- ODC revenue = $0 exact.
- ODC sats deployed = 0 exact.
- ODC fleet end-2025 = 0 exact.
- Per-sat marginal IRR 2025 ≤ 0 (no positive reads).
- Bandwidth services cost paid to Starlink 2025 = $0 exact.

**Block A invariants preserved:**
- Negative IRR ⇒ zero allocation (strict cutoff). Per D6, this is the binding case for ODC throughout horizon.
- ODC internal transfer revenue = AI Stack internal compute cost (R107 conservation).

**Block C sense checks:**
- ODC fleet 2030 ∈ [0, 15000] (sanity range; per D6 expected to land at 0).

**Known threads:**
- Per-sat IRR negative throughout horizon. Architecture §20.8 accepts as model verdict. Per D6, expose per-sat revenue and cost as MC inputs for scenario stress.

### §4.5 AI Stack stub (`calc/ai_stack.py`)

**Purpose.** Per D3, v1 stub. Allocator OUT contract wired with `Total Revenue = 0`, all IRR rows = 0, Capacity Demand = 0 permanently (per `project_ai_stack_no_launch_demand` lock). Internal compute cost from ODC = 0 (because ODC deployment = 0 per D6).

**Upstream dependencies.** None binding in v1. Pre-wired to read from ODC's `ODC at-cost compute rate ($/PFLOP-hr)` and `Total Fleet PFLOPS` for when Sprint 6 lands.

**Inputs (Assumptions §7):** Cursor seats (stub trajectory 1M 2025 → 50M 2035, multiplied by stub flag = 0 in v1), Grok consumer subs (stub), Grok enterprise API tokens (stub), Cursor ARPU, Grok consumer ARPU, Grok enterprise $/Mtoken. v1 ignores the stub trajectories; the inputs persist for the v1.x Sprint 6 landing.

**Calculations.** Trivial:
- `Total Revenue = zeros(26)`.
- `Total COGS = zeros(26)`.
- `Gross Profit = Module EBITDA = zeros(26)`.
- `Module CapEx = zeros(26)`.
- `Module FCF = zeros(26)`.
- IRR rows = 0.
- Capacity Demand (kg) = 0 permanently.

**Outputs:** standard Allocator OUT, all zeros.

**IRR engine:** none in v1. Hook present for Sprint 6 landing.

**2025 calibration (per Sprint Roadmap §6.5):** AI Stack revenue 2025 = $0 exact.

**Block A invariants preserved:** trivially.

**Known threads:**
- The full AI Stack body per AI Stack Module Architecture Scoping doc (three sub-modules: Compute, Application, Orchestration; Terafab toggle; Business Model Switch A/B/C credence-weighted) is v1.x scope. The code structure has placeholder sub-package `calc/ai_stack/` with `compute.py`, `application.py`, `orchestration.py`, `business_model_switch.py` as empty stubs to make Sprint 6's landing a fill-in rather than a restructuring.

### §4.6 Lunar Mars (`calc/lunar_mars/`)

**Purpose.** Strategic carve-out, NOT in IRR queue. Pre-revenue throughout 2025-2050. BV engine (labour units + hardware) drives book value accumulation. Mars carve-out off-the-top via prior-year Group FCF × 15%.

**Upstream dependencies.** Assumptions §8 + prior-year Group FCF (resolved by iterative solver via t-1 read).

**Sub-package structure:**
- `calc/lunar_mars/module.py` — top-level.
- `calc/lunar_mars/bv_engine.py` — accumulated book value (Valuation input + BV decay memos).
- `calc/lunar_mars/deployment.py` — Lunar / Mars ships per year, derived from carve-out cash.
- `calc/lunar_mars/carveout.py` — Mars carve-out per Architecture §6.2 / §11.1.

**Inputs (Assumptions §8):** Mars pct = 15% (MC range 3%-35% triangle), Mars floor = $1B (MC range $500M-$2.5B), Mars share of carve-out year-row, Lunar share of carve-out year-row, Lunar payload per ship 50K kg, Mars payload per ship 100K kg, Lunar depot multiplier 1×, Mars depot multiplier 5×, capital lifetime = 10 years, labour unit mass 60 kg, labour hourly output $22/0.7 burdened, daily working hours 22, productivity factor 1.0, productivity learning 5%/yr, useful life 5 yrs, hardware $/kg, Mars/Moon R&D year-row $-profile (anchored 2025 = $700M per Q4'25 R425 correction).

**Calculations.**
- Mars carve-out (year T) = `MAX(Mars_floor, Group_FCF[T-1] × Mars_pct)`. Cash BoY 2025 has no T-1 → carve-out 2025 = Mars_floor = $1,000M.
- Lunar share of carve-out × carve-out → Lunar ships deployed = Lunar cash / per-Lunar-ship cost. Same for Mars (5× depot multiplier).
- Surface-landed Starships (year) = ships deployed ÷ (1 + depot multiplier).
- Surface payload (kg) = surface_starships × payload per surface ship.
- Labour units landed = surface_payload × labour_share ÷ labour_unit_mass.
- Hardware mass landed (kg) = surface_payload × (1 − labour_share).
- Active labour fleet (running sum, net of retirements at lifespan) — Rule 23 exception.
- Annual production output ($mm) = active_labour_fleet × labour_annual_output × productivity_learning.
- Annual hardware value add ($mm) = hardware_mass_landed × hardware_$/kg.
- Annual book value contribution = production_output + hardware_value_add.
- Accumulated book value (year) = contribution(year) + prior_year_BV × (1 − 1/capital_lifetime) — Rule 23 exception.
- Lunar Mars Module D&A = cumulative LM Module CapEx ÷ capital_lifetime (proper cash-cap depreciation per Architecture §20.5).
- Revenue = 0 every year.
- COGS = mission ops only (% of CapEx); NO BV depreciation in COGS per §20.5.
- Module EBITDA = −COGS.
- Module CapEx = annual carve-out cash deployed.
- Module FCF = Module EBITDA + Module D&A − Module CapEx (heavily negative).
- Kg reserved off-the-top = (Lunar ships + Mars ships) × Starship LEO payload × (1 + depot_multiplier_average).

**Outputs:** standard Allocator OUT (IRR rows = 0; Total Revenue = 0). Plus two memo rows: `Memo: BV decay — Lunar ($mm/yr) — Valuation input only, NOT in Group D&A`, `Memo: BV decay — Mars ($mm/yr) — Valuation input only, NOT in Group D&A`. Plus `Lunar Accumulated Book Value ($mm)`, `Mars Accumulated Book Value ($mm)`, `Lunar Mars Module D&A ($mm)`, `Capacity Demand (kg-to-LEO)`.

**IRR engine:** none (per D7; strategic carve-out). Per-mission IRR hook present for v1.x.

**2025 calibration (per Sprint Roadmap §6.6):**
- Lunar Mars revenue 2025 = $0 exact.
- Mission CapEx 2025 = $0 exact (pre-window for physical launches).
- Lunar BV accumulated 2025 = $0 exact.
- Mars BV accumulated 2025 = $0 exact.

**Block A invariants preserved:**
- LM Module D&A is proper cash-cap depreciation, not BV-engine output (per §2.10).
- Mars carve-out uses prior-year Group FCF (t-1) — circularity breaker preserved.

**Block C sense checks:**
- Mars BV 2040 ∈ [$500B, $5T] (sanity).
- Mars carve-out floor 2025 = $1,000M exact.

**Known threads:**
- Mars/Moon R&D 2025 $700M flows through OpEx, not Lunar Mars module.

### §4.7 Module-stub validation pass

Before any per-module calc lands, every module file MUST:
1. Expose its Allocator OUT contract (the 11 canonical rows, zero values).
2. Pass the vending-machine linter (§2.1).
3. Pass the demand-output decoupling linter (§2.2).
4. Have its Architecture spec section citation in its module docstring.

---

## §5 — Cross-Cutting Layers

### §5.1 Assumptions ingest (`io/excel_ingest.py` + `inputs/assumptions.py`)

Per Architecture §1 + Assumptions Tab Spec.

**Ingest mechanism.** Two passes (formula + value) using openpyxl, per context.md §4.2. Formula pass captures formula strings, label registry, sheet/row structure. Value pass captures cached values (used for the diagnostic snapshot in §11.6 triage, NOT as a per-cell pass/fail oracle).

**Schema.** Pydantic v2 `Assumptions` model with 11 nested submodels:
- §1 Global (Tax rate 21%, TAM inflation 2.5%, GNI growth)
- §2 Allocator (Starting cash $5B EoY 2024, IPO year 2027 $30B, Pre-IPO bridge loan $20B 2025, Mars pct 15%, Mars floor $1B, Sigmoid k = 2, Forward weight w = 0.7, Vehicle build claim toggle, lead time 2y, launches per vehicle 24)
- §3 Capacity (28 inputs; Starship costs, payload, Wright's Law, F9 fleet decay)
- §4 Customer Launch (9 inputs; F9 price $111M Q4'25 anchor, Starship price $100M 2027)
- §5 Starlink (47 inputs; sat physical, Wright's Law, Starshield 0.25 decay, opening balances)
- §6 ODC (30 inputs; sat physical, chip roadmap, Pr(A), internal/external split)
- §7 AI Stack (9 inputs; Cursor, Grok consumer, Grok enterprise API stubs — v1 ignores)
- §8 Lunar/Mars (18 inputs; BV engine parameters, carve-out share)
- §9 OpEx (16 inputs; R&D by module with $-profile + % rates, SG&A by function)
- §10 CapEx (11 inputs; HQ/IT/Eng/Other + spectrum trajectory)
- §11 Valuation (23 inputs; WACC + risk premia, terminal, comparables, multiples)

Plus parallel `MCRanges` model with the same nested structure (Min, Max, Distribution, Notes per input).

**Validation.** Each input has a pydantic validator on load (type, range, distribution-vs-empty consistency). Failed validation halts ingest with a clear error citing the Assumptions cell.

**On-ingest cross-checks (§4.4 context.md):**
- 2025 anchor cells from V2.16 vs `2025 Anchors from Q4_25.md`. Drift > tolerance triggers a warning at ingest (not a halt — context.md notes V2.16 may already have known anchor drift).
- Canonical label registry resolution: every label expected by code must exist in V2.16.
- Diagnostic snapshot to parquet store for §11.6 use.

### §5.2 OpEx (`calc/opex.py`)

Per Architecture §12.

**Inputs.** Assumptions §9 + module revenue reads.

**Calculations.**
- R&D by module with anchor-and-offset bounded CAGR:
  - Starlink: start 8% → end 3%, CAGR −10%/yr on Starlink + Starshield revenue.
  - Customer Launch: start 25% → end 4%, CAGR −20%/yr on Customer Launch external revenue.
  - ODC: switching formula `MAX($-profile, 30% × revenue)`; $-profile $200M 2025 → $500M 2027 → declining (Vlad-locked Base Case).
  - AI Stack: switching formula `MAX($-profile, 15% × revenue)`; $-profile $50M 2025 → $300M 2028 → declining.
  - Moon/Mars: $-profile only; anchor 2025 = $700M (Q4'25 anchor).
- SG&A by function:
  - Sales & Marketing: start 4% → end 2%, CAGR −8%/yr on Starlink + Starshield + Customer Launch external + AI Stack revenue base (per Architecture §12.2 amendment 2026-05-20).
  - General & Admin: start 5% → end 6%, CAGR +1%/yr on Group revenue net of eliminations.
  - Customer Service: 2% flat on Starlink subscription revenue (BB + DTC).
  - Other corporate operating: 1% flat on Group revenue.
- Total OpEx = Σ R&D + Σ SG&A + Other.

**Calibration (Sprint Roadmap §6.7):**
- Total OpEx 2025 = $4,476M ±5% (Sprint 8.5 revised target; HALT if < $4,250M or > $4,700M).
- Starlink R&D 2025 ≈ $830M; CL R&D ≈ $1,073M; ODC R&D = $200M floor; AI Stack R&D = $50M floor; Mars/Moon R&D = $700M.

**Block A invariants:** none direct (OpEx feeds Group P&L; conservation checks at Group P&L level).

### §5.3 CapEx (`calc/capex.py`)

Per Architecture §13.

**Inputs.** Module CapEx rows (Rule 12 INDEX/MATCH on `Module CapEx ($mm)` label — NOT `Capital deployed`, which is diagnostic-only per Architecture §4.2). Assumptions §10. Allocator vehicle build claim.

**Calculations.**
- Module CapEx aggregation = Σ (Customer Launch + Starlink + ODC + AI Stack + Lunar Mars) Module CapEx.
- Corporate CapEx: HQ $50M/yr (30y life), IT $30M/yr (7y), Gen eng $20M/yr (20y), Other $10M/yr (20y).
- Spectrum CapEx (EchoStar): year-row 2025 $5B / 2026 $8B / 2027 $5B / 2028 $2B / 2029+ $0 (total $20B). Useful life 15 years. Cumulative intangible running sum; annual amortization = cumulative ÷ 15. Flows to Starlink BB COGS.
- Vehicle build claim (from Allocator §6.6) — sized at forward-aggregate kg demand.
- Total Group CapEx = Total Module CapEx + Corp CapEx + Annual Spectrum CapEx + Vehicle build claim.
- Corporate D&A = Σ cumulative_CapEx_per_line ÷ useful_life_per_line (straight-line).

**Calibration (Sprint Roadmap §6.7):**
- Total Group CapEx 2025 = $6,345M ±5% (Sprint 8 anchor, post-vehicle-build).
- Total Group D&A 2025 ≈ $1,261M ±10% (per §6.8 revised).
- Spectrum CapEx 2025 = $5B exact.

### §5.4 Group P&L (`calc/group_pnl.py`)

Per Architecture §15.

**Walk:**
- Group Revenue (net of eliminations) = Σ module revenues − Σ inter-module eliminations.
- Group Gross Profit = Group Revenue − Group COGS.
- Group EBITDA = Group Gross Profit − Total OpEx.
- Group EBIT = Group EBITDA − Corporate D&A (spectrum amort and module D&A are inside module COGS already; don't double-count).
- Taxes = MAX(0, Group EBIT) × 21%.
- NOPAT = Group EBIT − Taxes.
- Group FCF = NOPAT + Total D&A add-back (module D&A + Corporate D&A + Spectrum amort) − Total Group CapEx.

**Conservation block R99-R110:**
- R99 Revenue check = Total Revenue − Σ module revenues + Σ eliminations.
- R100 EBITDA check = Total EBITDA − Σ module EBITDAs.
- R101 CapEx check = Total Module CapEx − Σ module CapEx rows.
- R102 FCF check = Total Module FCF − Σ module FCF rows.
- R103 D&A check = Group D&A − (Σ module D&A in COGS + Corporate D&A).
- R104 EBIT consistency = Group EBIT − (Group EBITDA − Group D&A).
- R105 Launch services elimination = Customer Launch internal transfer rev − Σ consuming modules' Launch services cost.
- R106 Bandwidth elimination = Starlink internal bandwidth rev − ODC bandwidth services cost.
- R107 Compute elimination = ODC internal transfer rev − AI Stack internal compute cost.
- R108 ALL OK = `AND(ABS(R99:R107) < 1)` → "OK" / "CHECK".
- R109 cash flow identity = Starting cash + Σ IPO + Σ Group FCF + Σ Bridge loan − Σ deployed CapEx − Σ strategic carve-out − Cash EoY (final year).
- R110 Σ Module FCF residual (memo only; currently −$1,640M trajectory in V2.16; module-owner audit pending).

**Calibration (Sprint Roadmap §6.8 REVISED — the binding target per D1):**
- Group Revenue 2025 = $14,650M ±5%. HALT if < $13,917M or > $15,382M.
- Group Gross Profit 2025 = $9,463M ±10%. HALT if < $8,517M or > $10,409M.
- Group EBITDA 2025 = $4,904M ±5%. HALT if < $4,659M or > $5,149M.
- Group EBITDA Margin 2025 = 32.4% ±3pp. HALT if outside [29.4%, 35.4%].
- Group D&A 2025 = $1,261M ±10%. HALT if < $1,135M or > $1,387M.
- Group EBIT 2025 ≈ $4,450M (derived ±$50M).
- Taxes (21%) 2025 ≈ $934M (derived ±$50M).
- NOPAT 2025 ≈ $3,516M (derived).
- Total Group CapEx 2025 = $6,345M ±5%.
- Mars carve-out 2025 = $1,000M exact (floor).
- **Group FCF 2025 = −$2,569M ±10%. HALT if < −$2,826M or > −$2,312M.**
- Conservation R108 = "OK" every year (exact; any "CHECK" HALTs).

**Block A invariants enforced at runtime:**
- R108 = "OK" all 26 years 2025-2050 (raise on break).
- R99-R107 residuals ≤ $1M absolute every year (raise on break).
- R109 cash identity balances within $1M.

### §5.5 Valuation (`calc/valuation.py`)

Per Architecture §14.

**Inputs.** Group FCF (from Group P&L). Per-module FCFs (for SoTP). Lunar Mars accumulated BV at 2050 (for SoTP terminal). Assumptions §11.

**Calculations:**
- Group DCF: WACC 10%, terminal g 2.5%. Discount factor per year. Smoothed terminal FCF = AVERAGE of last 5 years (2046-2050). Terminal value = smoothed × (1+g) ÷ (WACC − g). PV of FCF + PV of Terminal = EV (raw). EV (clamped) = Σ MAX(0, PV of FCF) + PV of Terminal (memo for cliff value-at-risk).
- SoTP DCF: per-module WACC = group + risk premium (Starlink 0bps, CL 100bps, ODC 200bps, AI Stack 300bps, LM 500bps). Terminal: Gordon Growth for SL/CL/ODC/AIS; BV-anchored (1.5× LM BV at 2050) for LM.
- SoTP Multiples: SL 10×, ODC 6×, CL 5×, AIS 5×, LM $50B anchor.
- Comparables anchors (memo): MS $350B, Brant $2.5T (do not quote per Architecture §14.4), SL standalone (Bernstein/JPM) $150B, ODC (CoreWeave-anchored) $50B, CL (Rocket Lab) $40B, LM (NASA HLS) $50B.
- Sensitivity table: 5×5 grid Starship $/kg learning × Starlink TAM inflation. Plus 1D sweeps on WACC, terminal g.

**Calibration (Sprint Roadmap §6.10):**
- Implied EV 2025 (10× rev) = $146.5B ±5%.
- Group DCF EV ∈ [$500B, $1.5T] sanity range.
- SoTP DCF total within ±30% of Group DCF.

### §5.6 Allocator (`calc/allocator/`)

Per Architecture §6 + §20 amendments. Sub-package structure:
- `cash_pool.py` — Cash BoY tracker per Architecture §6.1 + §20.9 (bridge loan).
- `queue_gate.py` — non-module claims subtraction per §6.2.
- `mars_carveout.py` — off-the-top prior-year FCF per §11.1.
- `sigmoid_cash.py` — 7 sub-blocks (CL + 4 SL vehicles + ODC + AIS) per §20.2.
- `sigmoid_kg.py` — 5 sub-blocks (CL external Starship + 2 V3 SL vehicles + ODC + AIS=0) per §20.2. V2 vehicles NOT in kg queue.
- `vehicle_build.py` — forward-aggregate kg demand sized claim per §6.6.
- `irr_display.py` — central Spot/Forward/Blended IRR roll-up.
- `physical_gates.py` — V3 startup gate, V2 phase-out gate, F9 supply gate per §20.2.

**Sprint 11f Option A enforcement (per §2.2):**
- `compute_demand(...)` in each module reads anchor × learning × year-mask + exogenous facility CapEx. No reference to `OutputResult` types.
- `compute_output(...)` reads `MIN(cash_alloc / unit_cost, kg_alloc / mass_per_unit, internal_target)`. Bounded by cash; never feeds back.
- Sigmoid cash queue per sub-block:
  ```
  masked_demand_V = IF(IRR_V > 0, demand_V, 0)
  weight_V        = MAX(IRR_V, 0)^k × IF(demand_V > 0, 1, 0)         (k=2)
  share_V         = weight_V / Σ weights
  allocation_V    = MIN(masked_demand_V, Available_cash × share_V)
  ```

**Calibration (Sprint Roadmap §6.9):**
- Cash BoY 2025 = $5,000M (= starting cash; bridge loan adds to make Cash BoY-after-bridge = $25,000M per §3.1.5 of Sprint 11e).
- Year-N non-module claims 2025 ~$11.6B.
- Available cash for IRR queue 2025 ~$13.7B (after bridge loan; was $0 pre-bridge).
- Mars carve-out 2025 = $1B (floor).
- Conservation post-allocator-light-up = "OK".

### §5.7 Demand Curves (`inputs/demand_curves.py`)

Per Sprint 10.5 architecture.

**Form.** 61 BB breakpoints (Q, Revenue) + 56 DTC breakpoints, year-row. Piecewise-linear lookup via bracket-find (`np.searchsorted` analog) + manual linear interp. Clip at min and max.

**Annual TAM shift.** Multiplicative `(1+inflation)^t × (1+GNI)^t`. Read by Starlink revenue rows.

**Forbidden:** `scipy.interpolate.UnivariateSpline` or any regression fit (`np.polyfit`, `sklearn.LinearRegression`, etc.) — these would replicate the V30.5 `FORECAST` bug (Memory 2.4).

**Allowed:** `scipy.interpolate.interp1d(kind='linear', bounds_error=False, fill_value=(low_clamp, high_clamp))` or hand-rolled `np.searchsorted` + interp.

---

## §6 — Iterative Solver

Per context.md §7.

**Contract:**
- Max iterations: 100.
- Tolerance: 0.001 absolute on every monitored quantity.
- Damping: 0.5 default; configurable per scenario.
- Convergence MUST be asserted (`NonConvergenceError` on failure, not silent).
- Initial state: zeros for all unknowns; first pass without iteration to seed.

**Monitored quantities** (per-iteration max-residual computed across):
- Group Revenue
- Group FCF
- Every Allocator cash allocation row (R83-R91 module + vehicle level)
- Every Allocator kg allocation row
- Every module CapEx row
- Cash BoY per year
- Mars carve-out per year

**Sprint 11f Option A guarantee** (per §2.2): demand never enters the loop on the output side. The loop is exclusively over cash/output quantities. Demand is computed once from anchors + exogenous CapEx; never re-evaluated.

**Diagnostics.** Per-iteration trace of `(iter_idx, max_residual, residual_holder_quantity)` saved to `outputs/<run_id>/solver_trace.json`. If iter 100 hits without convergence, the trace is the first thing the audit log shows.

**Solver implementation:**
```python
state = initial_state()
for iter_idx in range(max_iters):
    new_state = single_pass(state)        # all modules in topological order
    delta = max_abs_delta(state, new_state)
    if delta < tol:
        break
    state = damped_blend(state, new_state, alpha=damping)
else:
    raise NonConvergenceError(diagnostic_trace=...)
```

---

## §7 — Reconciliation Framework

Per context.md §11.

A reconciliation run PASSES if and only if all four blocks pass.

### §7.1 Block A — Structural invariants (non-negotiable)

Enforced at runtime via `engine/conservation.py` (halt on break) AND as a pytest module.

- R108 = "OK" every year 2025-2050.
- R99-R107 residuals ≤ $1M absolute every year.
- Σ module cash allocations ≤ Available cash for IRR queue every year (within $1M rounding).
- Σ module kg allocations ≤ Capacity available for IRR queue every year.
- Modules with Blended IRR ≤ 0 → zero cash + zero kg allocation every year (strict).
- Module EBITDA == Module Gross Profit for every module, every year.
- Internal flow conservation: source rev = Σ consumer COGS for every flow (launch services, bandwidth, compute), every year.
- Iterative solver converges in < 100 iterations with max residual < 0.001.

### §7.2 Block B — External calibration anchors

Per D1, the Sprint Roadmap §6.8 revised target set is the binding Block B reconciliation target. Each anchor parametrized into a test:

```python
@pytest.mark.parametrize("name,target,tolerance,halt_low,halt_high", load_block_b_anchors_v1())
def test_block_b_anchor(name, target, tolerance, halt_low, halt_high, model_result):
    actual = model_result.lookup_anchor(name, year=2025)
    relative_err = abs(actual - target) / abs(target) if target else abs(actual)
    assert halt_low <= actual <= halt_high, f"{name} 2025: actual={actual:,.0f} HALT range [{halt_low:,.0f}, {halt_high:,.0f}]"
    assert relative_err <= tolerance, f"{name} 2025: err={relative_err:.2%} > tol={tolerance:.2%}"
```

Targets (the full §6.8 revised set):
- Group Revenue 2025 = $14,650M ±5%.
- Group Gross Profit 2025 = $9,463M ±10%.
- Group EBITDA 2025 = $4,904M ±5%.
- Group D&A 2025 = $1,261M ±10%.
- Group FCF 2025 = −$2,569M ±10%.
- Total OpEx 2025 = $4,476M ±5%.
- Total Group CapEx 2025 = $6,345M ±5%.
- Mars carve-out 2025 = $1,000M exact.
- Plus per-module 2025 targets per §4.

Q4'25 raw figures (Group EBITDA $8,690M, FCF +$3,670M, etc.) recorded as **informational external reasonableness anchors** in a separate test module that runs alongside but produces a report rather than pass/fail.

### §7.3 Block C — Sense / sanity checks

Per Rule 15 halts. Documented disposition exceptions per the Decision Log:

```python
def test_implied_dtc_subs_2025_sane(model_result):
    subs_2025 = model_result.starlink_dtc_subs_eoy(2025)
    assert subs_2025 < 15_000_000, ...

def test_f9_launches_2025(model_result):
    assert 165 <= model_result.f9_launches(2025) <= 177

def test_starship_launches_2025_exact(model_result):
    assert model_result.starship_launches(2025) == 0

def test_no_nan_or_inf(model_result):
    for var, vec in model_result.all_year_vectors():
        assert not np.any(np.isnan(vec)), f"{var} contains NaN"
        assert not np.any(np.isinf(vec)), f"{var} contains inf"

def test_wrights_law_monotone(model_result):
    cost = model_result.starlink_sat_cost_per_kg()
    assert all(cost[i] >= cost[i+1] for i in range(25)), "Wright's Law violation"

def test_starlink_v3_pre_trigger_zero(model_result):
    for year in [2025, 2026]:
        assert model_result.starlink_v3_bb_launches(year) == 0
        assert model_result.starlink_v3_dtc_launches(year) == 0

def test_starlink_v2_post_phaseout_zero(model_result):
    for year in range(2028, 2051):
        assert model_result.starlink_v2_bb_launches(year) == 0
        assert model_result.starlink_v2_dtc_launches(year) == 0
```

**Documented disposition (per D4):** F9 Blended IRR ∈ [8%, 25%] from Sprint Roadmap §6.2 is **expected to fail**. Test marker `@pytest.mark.expected_disposition_D4`. Recorded in run audit log; does not halt.

**Documented disposition (per D6):** ODC fleet 2030 ∈ [500, 15000] from Sprint Roadmap §6.4 is **expected to land at 0**. Test marker `@pytest.mark.expected_disposition_D6`. Recorded.

### §7.4 Block D — Architecture spec coverage

Static analysis tests:

```python
def test_every_public_calc_function_has_full_docstring():
    for fn in iter_public_calc_functions():
        for tag in ["Excel cell:", "Excel label:", "Architecture ref:", "Principle:"]:
            assert tag in fn.__doc__, f"{fn.__qualname__} missing docstring tag {tag!r}"

def test_every_architecture_section_has_code_coverage():
    sections = parse_architecture_sections()  # §1.x ... §20.x
    code_refs = parse_docstring_architecture_refs()
    uncovered = sections - code_refs
    assert not uncovered

def test_every_v216_label_in_registry():
    labels_v216 = extract_column_a_labels_from_v216()
    intentionally_unused = load_intentionally_unused_labels()
    for label in labels_v216:
        assert label in CANONICAL_LABEL_REGISTRY or label in intentionally_unused
```

### §7.5 Hypothesis-driven invariant tests

Per context.md §11.5. Block A invariants must hold under arbitrary valid Assumptions perturbations:

```python
@hypothesis.given(perturbation=valid_assumptions_perturbation_strategy())
@hypothesis.settings(max_examples=200, deadline=10000)
def test_conservation_holds_under_perturbation(perturbation, base_assumptions):
    perturbed = perturbation.apply_to(base_assumptions)
    try:
        result = run_pipeline(perturbed)
    except NonConvergenceError:
        return  # Some perturbations may not converge; that's a Block A failure to investigate separately
    for year in range(2025, 2051):
        assert result.conservation_ok(year), f"Conservation broken at {year}: {perturbation}"
        for check_row in CONSERVATION_CHECK_ROWS:
            assert abs(result.conservation_residual(check_row, year)) < 1.0
```

### §7.6 Diagnostic divergence report

Per context.md §11.3 + §11.6. Separate test module that runs alongside reconciliation but produces a report, not pass/fail:

```python
@pytest.mark.parametrize("sheet,row,year", load_all_xlsx_formula_cells_v216())
def test_xlsx_divergence(sheet, row, year, xlsx_snapshot, model_result, divergence_report):
    expected_xlsx = xlsx_snapshot.value(sheet, row, year)
    actual_code = model_result.lookup_by_label(sheet, row_label_of(sheet, row), year)
    delta = compute_delta(expected_xlsx, actual_code, tolerance=tolerance_for(sheet, row))
    divergence_report.record(sheet, row, year, expected_xlsx, actual_code, delta)
```

**Triage workflow (per context.md §11.6):** every divergence beyond tolerance triaged into one of:
- (A) Code bug — fix code; add unit test reproducing the bug.
- (B) xlsx bug — log to `docs/xlsx_bugs_found.md`; flag for Vlad sign-off.
- (C) Intentional architectural difference — log to `docs/intentional_divergences.md`. Sprint 11f Option A divergences (R48/R53/R58/R63 demand, R88-R91 allocation) preregistered as type (C).
- (D) Spec ambiguity — halt; ask Vlad to amend spec.

### §7.7 Tolerances (per context.md §11.4)

- $-denominated rows: ±$1M absolute OR ±0.1% relative, whichever is larger.
- %-denominated rows: ±1e-4 absolute.
- IRR rows: ±1e-3 absolute.
- Count rows (sats, launches, vehicles): exact integers OR ±1 unit with explicit documentation.
- Boolean rows: exact equality.

### §7.8 Reconciliation report deliverable

`docs/reconciliation_report.md` regenerated on every run. Per context.md §11.7:

- Block A status: per-invariant PASS/FAIL with year breakdown.
- Block B status: per-anchor actual vs target vs tolerance with delta and PASS/FAIL.
- Block C status: per-sense-check actual vs threshold. Expected-disposition entries (D4 / D6) shown with disposition tag.
- Block D status: per-section coverage gap list.
- Diagnostic divergence summary: matching cells / diverging cells; top 20 divergences by magnitude; cumulative-by-tab table.
- Triage log entries open since last milestone.

---

## §8 — Monte Carlo Engine

Per context.md §9.

### §8.1 Distributions (`mc/distributions.py`)

Seven types per Assumptions column AI:
- `fixed`: no sampling; Base Case used always.
- `triangle`: `scipy.stats.triang(min, mode=base, max)`.
- `lognormal`: `scipy.stats.lognorm` with P10/P90 fit to MC Min/Max.
- `uniform`: `scipy.stats.uniform(min, max)`.
- `discrete`: `numpy.random.choice` over listed options.
- `triangle-yearrow`: sample one multiplier per trial; apply to entire year-row (preserves shape, shifts magnitude). OR sample anchor years and re-interpolate (configurable per input).
- `fixed-yearrow`: no sampling; use Base year-row as-is.

Each distribution unit-tested against scipy reference for P10/P50/P90 with N=10,000 samples.

### §8.2 Sampler (`mc/sampler.py`)

- Independent by default.
- Per-trial seed: `base_seed + trial_idx`. Reproducible.
- Low-discrepancy (Sobol via `scipy.stats.qmc.Sobol`) optional for variance reduction.
- Correlated sampling deferred to v2 (documented assumption: inputs are independent unless otherwise noted).

### §8.3 Runner (`mc/runner.py`)

- `joblib.Parallel` for 16-core parallelism.
- Checkpointed: write partial results every 1000 trials to `outputs/mc/<scenario>/<run_id>/checkpoint_<N>.parquet`.
- Result store: parquet/arrow file format.
- Target: 10k trials in < 60s on a 16-core box. On 4-core dev: ~4 min acceptable.

### §8.4 Aggregator (`mc/aggregator.py`)

- Per-output percentiles: P5, P10, P25, P50, P75, P90, P95 on Group EV, Group Revenue 2050, Group FCF 2030/2040/2050, per-module EV, per-module 2050 revenue.
- CVaR (5%), max drawdown vs Base.
- Joint distributions: 2D bins of (Mars carve-out pct, Starship $/kg learning) → EV.
- Convergence diagnostic: running mean / std vs trial count.

### §8.5 Sensitivity (`mc/sensitivity.py`)

- Tornado: Δ output per ±1σ input. Ranked.
- Partial rank correlation: robust to monotone non-linearity; standard institutional tool.
- 1D sweeps: per-input grid, deterministic.
- 2D sensitivity table: 5×5 grid on Starship $/kg learning × Starlink TAM inflation (per Architecture §14.5).

### §8.6 MC PASS criteria (context.md §13.3)

- All 7 distribution types validated against scipy reference.
- 10k-trial Base Case run completes < 60s on 16-core.
- Tornado + PRCC + 1D sweeps + 2D sensitivity table all generated.
- Per-output percentile bands (P5-P95) on Group EV, per-module EV.

---

## §9 — Web UI v1 (`frontend/`)

Per context.md §5.4 + §14.5 + D8. Separate package (Next.js or React + Vite); deployed independently from the Python service.

### §9.1 v1 scope (locked)

- **Scenario picker**: user selects Base Case + per-input overrides. Backend validates against MC ranges (warn if outside P10/P90), runs deterministic, returns Group + per-module outputs.
- **Group EV table**: Group DCF EV, SoTP DCF total, Multiples cross-check, Comparables anchors, with per-cell tooltips citing source.
- **Per-module EV table**: SoTP per-module EVs.
- **Per-module + Group FCF table**: 2025-2050 year-columns.
- **Tornado**: top 10 inputs by Δ output per ±1σ.
- **Audit lineage panel**: every displayed number is clickable → opens a lineage panel showing the calc function, the inputs it consumed, the intermediate Excel cell it corresponds to (per Model Translation Log), and the Architecture spec section it implements.

### §9.2 v1 explicitly out of scope

- Charts (other than tornado bar).
- Comparables overlays / charts.
- Time-series animations.
- Multi-user collaboration.
- Multi-version comparison.

### §9.3 Performance budget

- Deterministic run < 2s for Base Case (cached via Redis or similar).
- MC dashboard render < 60s with joblib-parallelized backend.

### §9.4 No client-facing version surfacing

Per Memory 3.2. Internal builds may show git SHA in a debug panel; client builds show only "current Base Case" / "scenario X".

---

## §10 — Test Strategy

Five test tiers, all running in CI on every PR. Plus the hypothesis-driven invariant suite and diagnostic divergence harness.

### §10.1 Unit tests (`tests/unit/`)

Every public calc function. Edge cases enumerated per module per §4. The IRR engine has dedicated tests for:
- All-negative cash flows return −1.0 (cutoff convention).
- All-positive cash flows return a valid IRR.
- Mixed-sign streams converge to the correct root via multi-start Newton.
- Excel `IRR` parity within 1e-3 absolute tolerance on randomly generated streams.

### §10.2 Per-module integration tests (`tests/integration/`)

Each module's 2025 calibration anchor parametrized into a test. Runs against synthetic isolated inputs (not full pipeline) so a module failure points cleanly at that module.

### §10.3 Block A invariants (`tests/reconciliation/test_block_a.py`)

Runs as runtime assertion in `engine/conservation.py` AND as pytest. Per §7.1.

### §10.4 Block B + C tests (`tests/reconciliation/test_block_b.py` + `test_block_c.py`)

Parametrized over the Sprint Roadmap §6.8 revised anchors and the Rule 15 halt thresholds. Per §7.2 + §7.3.

### §10.5 Block D static analysis (`tests/reconciliation/test_block_d.py`)

Per §7.4.

### §10.6 Hypothesis-driven invariant tests (`tests/invariant/`)

Per §7.5. Block A invariants hold under arbitrary valid Assumptions perturbations.

### §10.7 Diagnostic divergence harness (`tests/diagnostics/`)

Per §7.6. Produces report; does not assert pass/fail.

### §10.8 Golden snapshots (`tests/golden/`)

For deterministic runs. Snapshots regenerated only on explicit approval (CI fails on unexpected snapshot drift).

### §10.9 CI configuration

- `pytest` + `pytest-xdist` for parametric reconciliation tests.
- `hypothesis` for invariant tests; `max_examples=200` per test, `deadline=10000`ms.
- `mypy --strict` + `ruff` + `black` lint pass.
- Spell-check pass (US English per §2.12).
- Vending-machine linter (§2.1).
- Demand-output decoupling linter (§2.2).
- Canonical-label registry completeness check (§2.4).
- Docstring four-tag linter (§7.4 Block D).
- Memory profile (peak < 8GB on Base Case run).

---

## §11 — Audit & Traceability

Per context.md §10.

### §11.1 Model Translation Log (`docs/model_translation_log.csv`)

Columns: `sheet, row, column_a_label, excel_cell_range, module_path, function, docstring_section`.

Every code function that implements a workbook row gets one entry. The log is auto-generated by `cli/audit.py` from docstring annotations.

### §11.2 Docstring convention (the four required tags)

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

A docstring linter checks every public function in `calc/` has the four required tags.

### §11.3 Variable naming

Snake_case English mirroring the Excel canonical label as closely as possible. `Customer Launch Blended IRR` → `customer_launch_blended_irr`. Memo rows prefixed `memo_`. Year-chained Rule 23 exceptions flagged in docstring with the exception reason.

### §11.4 Audit log per run (`outputs/<run_id>/audit.json`)

- Inputs hash: SHA256 of (Assumptions ingest + scenario overrides).
- Code SHA: git HEAD.
- Convergence: iterations to converge, final max-residual, per-iteration trace.
- Conservation: R99-R107 residuals per year, R108 boolean per year.
- Outputs hash: SHA256 of (Group + per-module FCFs + EV).
- Wall-clock time, peak memory.
- Disposition entries: F9 IRR Block C failure (D4), ODC zero deployment (D6).
- Divergence triage log entries.

The web UI reads this audit log for the lineage panel.

### §11.5 Reproducibility

Every run captures: code git SHA, scenario file SHA, Assumptions ingest SHA, MC seed (if applicable), iteration count.

Output is byte-stable for deterministic runs (numpy ops are deterministic; pandas is too with explicit dtype + sort_index).

---

## §12 — Milestone Plan & Sign-Off Gates

Per Phase 2 build approach proposal (Phase A through Phase G). Estimated 17–22 days for build work; G1–G5 numerical correctness gates account for 11–14 days.

### Phase A — Foundation (1-2 days)

**Ships:** repo skeleton; canonical_labels.py populated from V2.16 extraction; year_vector + units types; pydantic Assumptions schema; openpyxl ingest (formula + value pass); empty `calc/` package importing cleanly; iterative_solver as single-pass stub; reconciliation report Markdown writer with placeholders; `cli/run_model.py --base-case` runs zero-stub end-to-end.

**G1 sign-off gate:** Vlad reviews repo layout + canonical-label registry + Assumptions ingestion. Confirms before any calc logic lands.

### Phase B — Module scaffolding (1 day)

**Ships:** vending-machine framing on all five module files; Allocator OUT contract wired with zeros; linter tests live (vending-machine linter, demand-output decoupling linter, canonical-label registry linter, docstring four-tag linter).

**G2 sign-off gate:** Vlad reviews module file structure + linter assertions.

### Phase C — Per-module calc, sprint-by-sprint (6-8 days)

Order:
1. Launch Capacity (1d). Calibration: F9 launches 171 ±5, F9 fleet 39 ±5, $/kg ∈ [$400, $800], Starship launches 0 exact.
2. Customer Launch (1d). Calibration: F9 customer revenue $4,290M ±5%; F9 customer launches 38.58 ±2. Per-booster annual IRR pattern implemented. F9 IRR sanity failure recorded per D4.
3. Starlink + Starlink Capacity (1.5d). Calibration: BB+DTC $7,852M ±5%, DTC $157M ±15%, Starshield $2,520M ±5%, V2 BB launched 2,987 exact, V3 launches 0 exact.
4. ODC (1.5d). Calibration: ODC revenue $0 exact, ODC sats 0 exact. Per D6 disposition.
5. AI Stack stub (0.5d). Calibration: AI Stack revenue $0 exact. Three-sub-module placeholder structure in place per D3.
6. Lunar Mars (1d). Calibration: revenue $0 exact, Mission CapEx $0 exact, BV 2025 $0 exact.
7. OpEx + CapEx (1d). Calibration: Total OpEx $4,476M ±5%, Total CapEx $6,345M ±5%.
8. Group P&L (1d). Calibration: §6.8 revised set per D1. R108 = "OK" all years (mandatory).
9. Valuation stub (0.5d). Implied EV 2025 (10× rev) = $146.5B ±5% (calibrated; full DCF lights up in Phase D after Allocator).

**G3 sign-off gate (per-module):** at the end of each module commit; per-module 2025 calibration PASS.

### Phase D — Allocator brain + iterative solver (2 days)

**Ships:** Cash Pool Tracker, Queue Gate, Mars carve-out, Vehicle build claim, cash sigmoid queue (7 sub-blocks), kg sigmoid queue (5 sub-blocks), three physical gates, central IRR display. **Sprint 11f Option A enforced.** First-year (2025) override convention live. iterative_solver upgrades from single-pass to fixed-point iterator with damping + convergence assertion.

**Exit criterion:** deterministic Base Case run converges (< 100 iter, < 0.001 residual); Block A passes; Block B passes (§6.8 revised); Block C passes (with D4 + D6 dispositions recorded); Block D coverage complete; hypothesis-driven invariant tests pass.

**G4 sign-off gate:** Vlad reviews full reconciliation PASS report.

### Phase E — Reconciliation hardening + divergence report (1-2 days)

**Ships:** reconciliation harness across three stress scenarios (bear, bull, +Mars share); hypothesis-driven invariant tests across thousands of perturbations; full xlsx diagnostic divergence report per §7.6; triage log entries.

**Exit criterion:** zero open type-(A) or type-(D) triage entries; type-(B) and type-(C) entries logged with Vlad sign-off where applicable.

**G5 sign-off gate:** Vlad reviews divergence report.

### Phase F — Monte Carlo engine (2 days)

**Ships:** seven distribution types validated against scipy; sampler with per-trial seeds; joblib runner; aggregator; sensitivity (tornado, PRCC, 1D sweeps, 2D table); checkpointed result store.

**Exit criterion:** MC PASS criteria per §8.6.

**G6 sign-off gate:** Vlad reviews MC methodology.

### Phase G — FastAPI service + Web UI (3-5 days each)

**Service ships:** `service/api.py` with scenario runs, MC submissions, result retrieval, audit endpoints. Background jobs for MC. Result caching via Redis or similar.

**UI ships:** scenario picker, Group + per-module EV/FCF tables, tornado, audit lineage panel per §9.1.

**Exit criterion:** deterministic run < 2s; MC dashboard < 60s; lineage panel resolves to source.

**G7 sign-off gate:** usability review.

### Post-v1 — S-1 reconciliation (per D10)

After v1 sign-off (G7), the team reconciles assumptions, inputs, formulas, and outputs against the SpaceX S-1 filing (`Pre Existing Model Package/02_Fresh_Restart_Inputs/SpaceX S-1 vs Mach33 Model — Variance Analysis.xlsx` and the S-1 .mhtml). Outputs of that reconciliation pass include: (a) updated Assumptions Base Case values where S-1 disclosure tightens a stub; (b) new external reasonableness anchors specific to S-1 disclosed figures; (c) a Variance Report against the published Mach33 vs S-1 deltas. **This work is scoped separately and is NOT part of v1 sign-off.**

---

## §13 — Risk Register

In rough order of probability × impact.

### §13.1 Calibration miss against §6.8 revised targets

**Risk.** Sprint 9 hit the revised targets exact in Excel; the code's first-principles derivation may surface drift.

**Likelihood:** Medium. **Impact:** High (Block B failure → no reconciliation PASS).

**Mitigation:** per-module Phase C calibration tests catch drift module-by-module before Group P&L closes the walk. Halt-and-trace per Sprint Roadmap §7 escalation protocol. If a per-module miss surfaces, trace through the relevant module sprint spec; the most likely culprits per Sprint Roadmap §6.8 amendment are: (i) module D&A treatment in COGS; (ii) fully-allocated launch transfer pricing; (iii) pre-revenue R&D floors; (iv) Mars carve-out as real cash drain; (v) EchoStar as cash CapEx.

### §13.2 Sprint 11f Option A produces materially different Group Revenue 2050 vs V2.16's $583B

**Risk.** Could shift either direction. Modules can deploy more (V3 BB at high IRR absorbs cash) OR less (cash starvation in early years no longer masked by advisory-only allocator).

**Likelihood:** High. **Impact:** Medium (documented as expected type-(C) divergence; magnitude is the artifact).

**Mitigation:** documented in `docs/intentional_divergences.md`. Surfaced in the divergence report for Vlad review. The fact of the divergence is expected; the magnitude is informational.

### §13.3 Customer Launch F9 IRR distorts the cash queue priority

**Risk.** Per §10.4 / D4, F9 IRR prints high (~1700% even post-fix). Allocator queue over-prioritizes CL.

**Likelihood:** Certain. **Impact:** Medium (CL gets more cash than economically justified; affects per-module deployment trajectories).

**Mitigation:** documented disposition; recorded in audit log. If the distortion materially affects Block A allocation bounds (Σ module allocations exceeds Available cash for IRR queue, or no other module gets non-trivial allocation), escalate to Vlad for the v1.x Customer Launch IRR fundamental reformulation per Customer_Launch_IRR_Fix_Plan.md §6 Q1 / Q2 / Q3.

### §13.4 Iterative-solver non-convergence under MC perturbations

**Risk.** The fixed-point solver could oscillate under some Assumptions configurations (Principle 22).

**Likelihood:** Medium (some configurations will hit this). **Impact:** Medium (MC trial fails; aggregator drops the trial).

**Mitigation:** damping (default 0.5); explicit `NonConvergenceError` (not silent); full per-iteration trace in audit log; MC runner records non-convergence rate; if > 1% of trials non-converge, escalate to Vlad for damping retune.

### §13.5 AI Stack scoping Q3 (at-cost vs at-market) lands later, changes upstream contract

**Risk.** Per §10.3 / D3, AI Stack ships as zero stub in v1. Sprint 6 / Q3 may resolve Q3 with at-market pricing, contradicting the 2026-05-20 at-cost lock.

**Likelihood:** Low (architectural lock 2026-05-20 likely holds; Q3 conflict resolves in favor of at-cost). **Impact:** Low (only AI Stack's internal-revenue side changes; ODC's at-cost rate is unaffected).

**Mitigation:** AI Stack sub-package structure pre-wired so Sprint 6's landing is a fill-in, not a restructuring.

### §13.6 Bridge loan with no repayment/interest materially affects Cash BoY in 2026+ years

**Risk.** Per §10.5 / D5, v1.1 backlog. V2.16 has the same stub.

**Likelihood:** Certain (it's a known modeling gap). **Impact:** Low for v1 reconciliation (V2.16 has the same gap; calibration targets reflect the stub state).

**Mitigation:** documented in audit log. v1.1 implements repayment schedule + interest expense once Vlad provides assumptions.

### §13.7 V2.16 drifts (Vlad continues Excel-side sprints during the port)

**Risk.** Sprint 11f / 11.5 / 12 may execute on the xlsx during the port.

**Likelihood:** Medium. **Impact:** Medium (input set + diagnostic snapshot shift).

**Mitigation:** pin V2.16 SHA at ingest; document input snapshot date; rerun divergence report after any workbook update; the input snapshot is reproducible.

### §13.8 ODC zero deployment masks a different bug

**Risk.** Per §10.6 / D6, ODC stays at zero deployment under V2.16 input set. This is correct model verdict, but it means ODC's Allocator-side and internal-flow logic is never exercised on non-trivial inputs in v1 reconciliation.

**Likelihood:** Medium. **Impact:** Low for v1; Medium for v1.x if ODC inputs are revised to produce positive deployment and an ODC-side bug surfaces.

**Mitigation:** hypothesis-driven invariant tests (§7.5) perturb Assumptions including ODC inputs; if Block A breaks under perturbation, the bug surfaces before v1.x input revision.

### §13.9 Excel `IRR` Newton convergence vs numpy-financial `IRR` produces small divergence

**Risk.** Excel's `IRR` may converge to a slightly different root than Newton with the same tolerance.

**Likelihood:** Low. **Impact:** Low (within the 1e-3 IRR tolerance per §7.7).

**Mitigation:** documented; falls under acceptable IRR tolerance.

---

## §14 — Glossary

Per context.md §16, with port-specific additions. Canonical terms — never aliased.

- **Allocator IN** — top-of-module-tab block reading cash + kg allocations from the Allocator.
- **Allocator OUT** — bottom-of-module-tab 11-row contract the Allocator reads.
- **Anchor-and-offset** — year-row formula pattern `$D$anchor × (1+rate)^E$5`; vectorized in code.
- **At-cost transfer** — internal flow (launch services, bandwidth, compute); fully-allocated cost.
- **Block A invariants** — structural conservation, allocation bounds, vending-machine, internal flow conservation, solver convergence.
- **Block B anchors** — external calibration; per D1, Sprint Roadmap §6.8 revised target set.
- **Block C sense checks** — Rule 15 halt thresholds + Block A sanity.
- **Block D coverage** — every public calc function has four-tag docstring; every Architecture §1-§20 section maps to code.
- **Canonical label** — column-A row label used for INDEX/MATCH cross-tab refs; in code, a string constant in the registry.
- **Conservation block** — Group P&L R99-R110; R108 = "OK" required for any run to PASS.
- **Disposition (D4 / D6)** — documented test failures that do not halt; recorded in audit log per the Decision Log.
- **Module** — one of the five P&L tabs (Customer Launch, Starlink, ODC, AI Stack, Lunar Mars).
- **Module EBITDA** — mathematically Gross Profit. Label retained per Principle 7.
- **Module FCF** — pre-tax, pre-corp; `EBITDA + module_D&A_addback − Module_CapEx`.
- **Option A** (Sprint 11f) — demand purely exogenous; output bounded by cash; never feeds back.
- **Queue gate** — Allocator section that reserves non-module claims before the IRR queue allocates.
- **Sigmoid blend** — IRR-priority allocation: `weight = max(IRR, 0)^k, k=2`, `share = weight / Σ`, `alloc = min(masked_demand, available × share)`.
- **Vending-machine framing** — module P&L structure; no R&D / SG&A / tax / overhead.

---

## §15 — Repository Layout (reference)

Per context.md §5.3 / D9. Reproduced here for v1 confirmation:

```
spacex-modeler/
├── pyproject.toml
├── README.md
├── context.md
├── role.md
├── phase1_research_synthesis.md
├── PRD.md (this document)
├── Pre Existing Model Package/      (reference; not imported)
│
├── src/spacex_model/
│   ├── config/
│   │   ├── constants.py
│   │   ├── canonical_labels.py
│   │   └── settings.py
│   ├── inputs/
│   │   ├── assumptions.py
│   │   ├── mc_ranges.py
│   │   ├── q4_25_anchors.py
│   │   └── demand_curves.py
│   ├── domain/
│   │   ├── year_vector.py
│   │   ├── units.py
│   │   └── irr.py
│   ├── calc/
│   │   ├── allocator/
│   │   │   ├── cash_pool.py
│   │   │   ├── queue_gate.py
│   │   │   ├── mars_carveout.py
│   │   │   ├── sigmoid_cash.py
│   │   │   ├── sigmoid_kg.py
│   │   │   ├── deployment.py
│   │   │   ├── vehicle_build.py
│   │   │   ├── physical_gates.py
│   │   │   └── irr_display.py
│   │   ├── launch_capacity.py
│   │   ├── customer_launch.py
│   │   ├── starlink/
│   │   │   ├── module.py
│   │   │   ├── vehicle_pools.py
│   │   │   ├── deorbit.py
│   │   │   ├── revenue_curve.py
│   │   │   └── per_vehicle_irr.py
│   │   ├── starlink_capacity.py
│   │   ├── odc.py
│   │   ├── ai_stack/
│   │   │   ├── module.py (v1 = stub)
│   │   │   ├── compute.py (v1.x placeholder)
│   │   │   ├── application.py (v1.x placeholder)
│   │   │   ├── orchestration.py (v1.x placeholder)
│   │   │   └── business_model_switch.py (v1.x placeholder)
│   │   ├── lunar_mars/
│   │   │   ├── module.py
│   │   │   ├── bv_engine.py
│   │   │   ├── deployment.py
│   │   │   └── carveout.py
│   │   ├── internal_flows/
│   │   │   ├── launch_services.py
│   │   │   ├── bandwidth.py
│   │   │   └── compute.py
│   │   ├── opex.py
│   │   ├── capex.py
│   │   ├── group_pnl.py
│   │   └── valuation.py
│   ├── engine/
│   │   ├── iterative_solver.py
│   │   ├── pipeline.py
│   │   └── conservation.py
│   ├── mc/
│   │   ├── distributions.py
│   │   ├── sampler.py
│   │   ├── runner.py
│   │   ├── aggregator.py
│   │   └── sensitivity.py
│   ├── io/
│   │   ├── excel_ingest.py
│   │   ├── excel_export.py
│   │   ├── snapshot_store.py
│   │   └── audit_log.py
│   ├── service/
│   │   ├── api.py
│   │   ├── jobs.py
│   │   └── auth.py
│   └── cli/
│       ├── run_model.py
│       ├── run_mc.py
│       └── audit.py
│
├── tests/
│   ├── reconciliation/
│   ├── unit/
│   ├── integration/
│   ├── invariant/
│   ├── diagnostics/
│   └── golden/
│
├── frontend/        (Next.js or React + Vite; deployed independently)
│
├── scenarios/
│   ├── base_case.yaml
│   ├── bear.yaml
│   └── bull.yaml
│
└── docs/
    ├── model_translation_log.csv
    ├── architecture_diagram.md
    ├── reconciliation_report.md
    ├── intentional_divergences.md
    ├── xlsx_bugs_found.md
    ├── intentionally_unused_labels.md
    └── changelog.md
```

---

## §16 — Success Criteria

### §16.1 Numerical PASS (v1)

- [ ] Block A — Structural invariants all pass per §7.1.
- [ ] Block B — External calibration anchors within tolerance per §7.2 (Sprint Roadmap §6.8 revised set per D1).
- [ ] Block C — Sense checks pass per §7.3 (with D4 + D6 dispositions recorded).
- [ ] Block D — Spec coverage complete per §7.4.
- [ ] Iterative solver converges on Base Case + 3 stress scenarios (bear, bull, +Mars share).
- [ ] All Block A invariants hold under hypothesis-driven perturbation testing per §7.5.
- [ ] xlsx diagnostic divergence report generated per §7.6; each divergence outside tolerance triaged.
- [ ] Zero open triage outcomes of type (A) "code bug" or type (D) "spec ambiguity."

### §16.2 Architectural PASS (v1)

- [ ] Vending-machine framing enforced (no module file imports OpEx/Tax) per §2.1.
- [ ] Demand decoupled from output by type (Sprint 11f Option A) per §2.2.
- [ ] All cross-tab references through canonical-label registry per §2.4.
- [ ] All year-row computations vectorized per §2.3.
- [ ] Conservation invariants assert at runtime per §2.5.

### §16.3 MC PASS (v1)

- [ ] 7 distribution types implemented and validated against scipy reference per §8.1.
- [ ] 10k-trial Base Case run completes < 60s on 16-core per §8.3.
- [ ] Tornado + PRCC + 1D sweeps + 2D sensitivity table all generated per §8.5.
- [ ] Per-output percentile bands (P5-P95) on Group EV, per-module EV per §8.4.

### §16.4 Deliverables checklist (v1)

- [ ] Modular codebase under `src/spacex_model/` per §15.
- [ ] Model Translation Document auto-generated, current per §11.1.
- [ ] Reconciliation harness with full V2.16 oracle integration per §10.
- [ ] MC engine with documented methodology per §8.
- [ ] FastAPI service layer per §9.
- [ ] Web UI v1 per §9.1.
- [ ] CLI for local runs (Base Case + MC).
- [ ] README + run instructions + architecture diagram + reconciliation report.

---

## §17 — Backlog (v1.1 / v2 / Post-v1)

### §17.1 v1.1 backlog (queued for after v1 sign-off)

- **S-1 reconciliation pass** (per D10) — reconcile Assumptions, inputs, formulas, outputs vs SpaceX S-1 filing. Produces variance report.
- **Customer Launch IRR fundamental reformulation** — address the ~1700% F9 IRR per Customer_Launch_IRR_Fix_Plan.md §6 Q1/Q2/Q3.
- **Bridge loan repayment + interest expense** — per D5. Vlad provides assumptions for repayment schedule + rate.
- **AI Stack full body** — three sub-modules (Compute / Application / Orchestration), Terafab toggle, Business Model Switch A/B/C credence-weighted. Pre-wired structurally per D3.
- **ODC unit economics revision** — per D6 and Architecture §20.8; Vlad-pending decision on per-sat compute revenue OR per-sat cost inputs.
- **R110 Σ Module FCF residual audit** — currently −$1,640M trajectory in V2.16; module-owner audit pending.

### §17.2 v2 backlog

- Charts (other than tornado bar) on Web UI.
- Comparables overlays.
- Time-series animations.
- Multi-user collaboration on Web UI.
- Multi-version comparison views (V2.16 vs V30.5 vs current port).
- Correlated MC sampling (correlation matrix between named inputs).
- Per-mission Lunar Mars IRR engine (per D7).

### §17.3 Open architectural questions to monitor

- AI Stack Q3 (at-cost vs at-market internal transfer pricing) — currently locked at at-cost per Architecture §7.3; AI Stack scoping doc Q3 may surface a conflict in v1.x.
- Lunar Mars per-mission IRR — Vlad deferred ("we can change this later").
- ODC strategic carve-out vs IRR queue — currently in queue per Architecture; alternative is to move ODC to strategic carve-out like Lunar Mars (Architecture §11 amendment).

---

## §18 — Reading order for new contributors

In this order, ~3.5 hours total:

1. `role.md` (5 min) — Marcus Hale persona.
2. `context.md` (45 min) — full read; load-bearing project context.
3. `phase1_research_synthesis.md` (30 min) — Phase 1 research artifact.
4. This PRD (40 min) — §1-§5 in detail, skim §6-§17.
5. `Pre Existing Model Package/06_Memory_Snapshot/MEMORY_SNAPSHOT_CRITICAL_LOCKS.md` (15 min).
6. `Pre Existing Model Package/00_Constitutional_Docs/02_Architecture_and_Methodology.md` (45 min) — skim §1-5, read §6, §10, §11, §15, §20 carefully.
7. `Pre Existing Model Package/00_Constitutional_Docs/03_Sprint_Roadmap_and_Verification.md` §6.8 (10 min) — the revised calibration target set.
8. `Pre Existing Model Package/01_Current_State/Sprint_11f_Spec.md` (15 min) — Option A.
9. `Pre Existing Model Package/01_Current_State/Sprint_11e_Spec.md` (10 min) — V2.16 baseline.

---

## §19 — How to operate against this PRD

**For contributors:**
- Every PR cites the PRD section it implements (e.g., "Implements §4.3 Starlink revenue curve").
- Every public calc function has the four-tag docstring (§11.2).
- Every cross-module reference resolves through `config/canonical_labels.py` (§2.4).
- Every PR runs CI: unit + integration + Block A + Block B + Block C + Block D + invariant + linters.
- Per-module 2025 calibration tests must pass before a module merges into main.

**For sign-off gates G1-G7:**
- Each gate has a defined exit criterion (per §12).
- Sign-off recorded in a CHANGELOG entry with date + reviewer.
- Failures at a gate halt forward progress; back-and-forth with Vlad until resolved.

**For amendments:**
- Architecture & Methodology changes require updating that doc first, then this PRD, then the affected code.
- Decision Log entries (this PRD §1.6) are append-only; updates require Vlad-equivalent sign-off.
- Risk register (§13) updated as new risks surface.

**For divergence triage:**
- Per §7.6 workflow: identify, locate both sides, read the spec, classify (A/B/C/D), document.
- Triage workflow run at every reconciliation milestone (G4, G5), not on every PR.

---

## §20 — Amendment Log

- **2026-05-28 (initial draft)** — PRD v1.0 authored after Phase 1 deep research + Phase 2 build approach approval. Locks the Decision Log §1.6 entries D1–D10. Scopes v1, v1.1, v2 work. Aligns with Sprint Roadmap §6.8 revised target set per D1. Implements Sprint 11f Option A from day one per D2. AI Stack ships as zeros stub with sub-package structure pre-wired per D3. F9 IRR Block C failure accepted disposition per D4. Bridge loan stub carries V2.16 state per D5. ODC zero deployment per model verdict per D6. Mars per-mission IRR deferred per D7. Web UI v1 scope locked per D8. Repository layout per context.md §5.3 per D9. S-1 reconciliation as post-v1 work item per D10.

---

**END OF PRD.**
