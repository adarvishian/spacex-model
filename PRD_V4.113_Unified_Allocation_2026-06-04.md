# Product Requirements Document — Mach33 SpaceX Valuation Model, V4.113 Re-Baseline & Unified Allocation (Python)

**Document version:** 2.0 (supersedes `PRD.md` v1.0, 2026-05-28)
**Date:** 2026-06-04
**Author:** Dr. Marcus Hale (port lead, per `role.md`)
**Status:** Locked for execution. Amendments require an entry in §16 Amendment Log.
**Primary user / sign-off:** Vlad (Mach33 principal) — architecture and numerical sign-off.

---

## §0 — Why this PRD exists (executive summary)

`PRD.md` v1.0 ported the model against **V2.16**, whose workbook was organised around an `Allocator` tab, separate `ODC` and `AI Stack` tabs, and a 2025–2050 horizon. The canonical workbook is now **`SpaceX V4.113.xlsx`**, a structurally different, *unified-era* model: the allocator has become the **`Cash Allocation Engine`** tab, ODC and AI roll into a single **`AI - Compute`** tab, enabling infrastructure is carved into a **`Facilities Build`** tab, and a dedicated **`Conservation`** tab carries the integrity guardrails. The horizon is **truncated to 2025–2040**. The V2.16-targeted Python port is therefore pointed at an architecture that no longer exists in the canonical book.

This PRD does three things, per direction locked with Vlad on 2026-06-04:

1. **Re-baselines the entire Python model to V4.113** — every tab, ingest path, canonical label, and calc module re-pointed from V2.16 to the V4.113 structure (decision: *full re-baseline*).
2. **Makes Python the single authoritative implementation of the whole model** — not just the allocator. The entire model, all features and functions, are computed in Python. Excel (`SpaceX V4.113.xlsx`) is retained as the **canonical input source** (Assumptions, Demand Curves, opening balances, MC ranges) and as a **diagnostic reference** for derived values — never as a numerical oracle (decision: *entire model in Python*).
3. **Prepares to fix the highlighted allocator defects** documented in the three 2026-06-04 source docs, by folding the locked **Unified Allocation architecture (U0–U4)** into the Python target design from day one — so the re-baselined model is born fix-ready rather than replicating the broken Excel allocator and then unwinding it.

**Adherence philosophy (locked):** *spec-first, divergence-triaged.* "Adhere completely to V4.113" means the Python model consumes the **same exogenous inputs** as V4.113 and reproduces its **structural invariants and external calibration anchors**, deriving every value from first principles against the Architecture & Methodology spec. Where V4.113's cached cell values disagree with a first-principles derivation, that delta opens a divergence investigation (code-bug / xlsx-bug / intentional-spec-difference), **not** an automatic test failure. Cell-by-cell equality is a diagnostic, not a sign-off gate. This is the same philosophy `context.md` §11 established for V2.16, carried forward unchanged.

---

## §1 — Companion documents & authority order

This PRD does not restate the sources; it cites them. On conflict, the order below governs.

1. `role.md` — operating persona (Dr. Marcus Hale; numerical equivalence sacred, traceability non-negotiable, DEV_LOG entry on every material change).
2. **Project constitution** — `Pre Existing Model Package/00_Constitutional_Docs/*` (Architecture & Methodology, Lessons Learned, Model Execution Rules, Sprint Roadmap & Verification) and the `mach33-model-build` / `mach33-irr-canonical` discipline. **Authoritative on any process question.**
3. `Unified_Allocation_MASTER_CONTEXT_and_Handoff_2026-06-04.md` — the verified as-is allocator map, the 8 resolved decisions, the conceptual resolutions, the supersession list. **Authoritative on the allocator re-architecture** (supersedes the original V4.109 audit where it notes corrections).
4. `Unified_Allocation_Scoped_Architecture_and_Sprint_Schedule_2026-06-04.md` — the U0–U4 sprint plan, gates, and MC-input table.
5. `Current_Allocator_Issues_and_the_Case_for_Python_2026-06-04.md` — the seven defects and the rationale for Python.
6. `context.md` — living project context (V2.16-era; this PRD updates its tab/horizon/architecture assumptions to V4.113 but keeps its reconciliation, MC, traceability, and code-architecture principles).
7. `PRD.md` v1.0 — superseded by this document; retained for history.

**Two cardinal rules inherited from the source docs, binding on all execution:**

- **Row numbers shift between builds.** Every cell address in this PRD that comes from the V4.109-era docs, *and even the V4.113 addresses extracted for this PRD*, must be **re-resolved against the live open workbook** before any code references them. `INDEX/MATCH`-by-label is the resolution mechanism in Excel; in Python the equivalent is the canonical-label registry (§7.5). No code or spec hard-codes a row position without re-resolving the label first.
- **2025 is the frozen anchor year.** The 2025 column is calibrated to external Q4'25 / S-1 actuals and is not recomputed by the allocator (allocated cash = 0 in 2025). No sprint touches it.

---

## §2 — The canonical workbook: V4.113 as-is (verified 2026-06-04)

Extracted directly from `SpaceX V4.113.xlsx` on 2026-06-04. These are load-bearing facts the Python re-baseline must honour.

### §2.1 Tab inventory (15 sheets)

| Tab | Role | Dim (r×c) | Maps to (Python) |
|---|---|---|---|
| Assumptions | Input source of truth; 11+ sections | 530×36 | `inputs/assumptions.py`, `inputs/mc_ranges.py` |
| Demand Curves | BB + DTC piecewise-linear Q→Revenue | 151×19 | `inputs/demand_curves.py` |
| Starlink | BB+DTC+Starshield P&L; per-vehicle IRR | 205×78 | `calc/starlink/` |
| Customer Launch | External + internal launch; per-launch IRR | 142×78 | `calc/customer_launch/` |
| **Cash Allocation Engine (CAE)** | Unified cash pool, queue gate, IRR-softmax, water-fill, kg-rationing, debt facilities | 169×34 | `calc/allocator/` (rebuilt) |
| **AI - Compute** | ODC + Terrestrial unified (was 2 tabs in V2.16) | 255×78 | `calc/ai_compute/` (new) |
| Lunar - Mars | Strategic carve-out, BV engine, no IRR | 120×29 | `calc/lunar_mars.py` |
| Vehicle Build (VB) | Demand-pulled Starship+F9 fleet; module-owned launch CapEx | 107×19 | `calc/vehicle_build.py` |
| Launch Dashboard | Aggregation/memo | 28×29 | reporting only |
| **Facilities Build (FB)** | 7-bucket enabling-infra CapEx engine (Redmond, Gigabay, pads, engines, terminals, HQ) | 84×78 | `calc/facilities_build.py` (new) |
| Group P&L | Consolidated walk | 112×29 | `calc/group_pnl.py` |
| Segment P&L | Segment roll-up | 129×29 | `calc/segment_pnl.py` (new) |
| **Conservation** | Integrity guardrails (R8–R19) | 19×19 | `engine/conservation.py` (rebuilt) |
| SoTP - Valuation | DCF + sum-of-parts | 114×19 | `calc/valuation.py` |
| Claude Log | Per-sprint change log | 9×6 | `docs/changelog.md` |

### §2.2 Horizon & calc settings (CHANGED from V2.16 — load-bearing)

- **Year horizon: 2025–2040, 16 years, 17 columns `D:S`.** Year header in row 4 (`D4=2025 … S4=2040`). **This is truncated** from the V2.16 26-year 2025–2050 horizon. *All length-26 numpy vectors in the current port become length-16.* `config/constants.py` `HORIZON` changes accordingly; every `YearVector` and every test parametrised over `range(2025, 2051)` must be re-pointed to `range(2025, 2041)`.
- **Iterative calculation: ON**, `iterateCount=1000`, `iterateDelta≈1e-7` (verified in `xl/workbook.xml`). Tighter than V2.16's 100/0.001. The Python fixed-point solver's contract (§7.4 of context.md) updates to match: assert convergence within 1000 iterations to 1e-7 absolute on every monitored quantity.
- The only legitimate within-year cycle is the **queue gate** (pool ↔ taxes ↔ EBIT). No second within-year loop may exist (acyclicity firewall, §5.3).

### §2.3 Cash Allocation Engine — live row map (V4.113, re-resolve before coding)

The CAE is the heart of the re-baseline and the locus of every defect in §4. Live map as extracted 2026-06-04 (labels are stable; **row numbers must be re-resolved per sprint**):

```
CASH POOL (R7–R11):  R8 Cash BoY ← prior R56 · R9 IPO · R10 bridge · R11 Cash available
QUEUE GATE (R13–R21): R14 memo Group revenue · R15 Corp SG&A · R16 shared R&D · R17 corp CapEx
                      · R18 spectrum · R19 taxes · R20 non-module claims total · R21 Pool after gate
CARVE-OUT (R23–R25):  R24 Lunar/Mars carve-out (SENIOR, off the top) · R25 Remaining pool (0 in 2025)
TOP-LEVEL IRR-SOFTMAX (R27–R44): R28/29/30 Spot IRR {SL, CL, AI-Compute} · R31/32/33 exp(β·IRR)
                      · R34 Σ · R35/36/37 shares · R39/40/41 Allocated cash {SL, CL, AI}
                      · R43 memo cash deployed · R44 leftover cash
KG-RATIONING (R45–R52): R46 memo total kg demand · R47 LM kg reserved off-top · R48 capacity after LM
                      · R49 kg-binding flag · R50/51/52 allotment {SL, CL, AI} [PRO-RATA — defect]
CASH EoY (R54–R57):   R55 Group FCF · R56 Cash EoY (feeds next-yr R8 — the cash spine) · R57 cumulative memo
CONSERVATION (R59–R61): R60 carve-out tie · R61 VB fleet CapEx tie
CAPACITY-PRIORITY (R63–R74): R64/65/66 caps max deployable {SL,CL,AI} · R67–72 rank keys/higher-rank caps
                      · R74 TEMP placeholder (retire)
LEVEL-2 WITHIN-AI (R76–R94): R77/78 Spot IRR {ODC, Terr} · R82/83 shares · R85/86 desired
                      · R88 allocated ODC · R90 allocated Terr · R89/94 spillovers · R93 L2 cash tie
CARVE-OUT IRR RESPONSE (R95–R98): R96 avg prior-yr IRR · R97 ramp · R98 effective % (acyclic, LIVE)
DESIRED LAUNCH KG (R99–R102): R99 SL · R100 CL · R101 AI · R102 total → feeds VB!R104
TERAFAB FACILITY (R103–R111): R104 CapEx · R105 draw→R11 · R106 interest · R107 repay · R108 balance
                      · R111 Σdraw−Σrepay−balance=0 [debt layer — KEEP, re-scope out of IRR]
WATER-FILL (R112–R129): R113/114/115 desired · R116/117/118 capped · R119 residual · R120–122 headroom
                      · R123–126 spill weights · R127/128/129 allocated final [SINGLE PASS]
ODC FACILITY (R131–R140): R134 draw BYPASSES pool → AI!R30 · R140 Σdraw−Σrepay−balance=0
                      [distributional defect — fold into spine]
```

Note the V4.113 map differs from the V4.109 map in the source docs in several row positions (e.g., the carve-out IRR-response sits at R95–R98 here; Terafab at R103–R111; ODC facility at R131–R140). This *confirms* the cardinal rule: trust labels, re-resolve rows.

### §2.4 Vehicle Build, Facilities Build, Conservation — key as-is anchors

- **VB** (107 rows): forward-demand-pulled fleet sizing. `R104 Total desired upmass ◄ CAE!R102`; `R106 desired Starship launches`; `R55/R84 built = MIN(need, Gigabay R107)`; `R107 Gigabay ◄ Assumptions`. **Modules own launch CapEx** (`R25 transfer revenue RETIRED`, `R77 VB FCF = 0 by construction`, `R28–R30` launch-CapEx roll-up with conservation tie). `R67 "Total launch kg demand N+1 (fleet)"` present — confirm consumer count (orphan candidate per docs).
- **FB** (84 rows): 7 enabling-infra buckets. `R14 sat-mfg facility CapEx ◄ Starlink`; `R19 installed Starship build capacity (ships/yr): rate-limited ramp` (the live Gigabay throughput cap, FB-1); `R26 launch/vehicle facility CapEx`; `R39 HQ facility CapEx ◄ Group P&L`; `R43 total facility CapEx`; `R44 conservation: max bucket (cum D&A − cum CapEx) ≤ 0`. **This tab is the "enabling infrastructure" bucket of the three-bucket taxonomy (§5.1).**
- **Conservation** (R8–R19): R8 Revenue tie · R9 EBITDA foot · R10 D&A + LM book-value guard · R11 EBIT consistency · R12 accrual↔cash FCF · R13 FCF foot · **R14 Cash-flow identity** · R15 elimination conservation (Rule 21) · **R17 ALL OK (R108-equivalent)** · R18 ΣFCF cumulative · R19 normalization delta. **R14 is the broken guardrail of defect #6 (§4).**

---

## §3 — V2.16 → V4.113 architecture drift (what the re-baseline must change)

The current Python port (`src/spacex_model/`) is structured for V2.16. The re-baseline re-points it to V4.113. The table is the work inventory.

| Area | V2.16 port (current) | V4.113 target | Action |
|---|---|---|---|
| Horizon | length-26 vectors, 2025–2050 | length-16, 2025–2040 | **Re-point** `constants.py`, all `YearVector`, all tests/scenarios |
| Allocator | `calc/allocator/{cash_pool,queue_gate,sigmoid_cash,sigmoid_kg,deployment,vehicle_build,mars_carveout,irr_display}.py` | CAE: queue gate → carve-out → IRR-softmax (β·IRR) → water-fill → kg-rationing → debt facilities | **Rebuild** allocator package to the CAE structure; replace sigmoid-blend with the softmax+soft-floor+water-fill design |
| ODC / AI | separate `odc.py` + `ai_stack.py` (stub) | single `AI - Compute` tab (ODC + Terrestrial, dual-revenue, on-tab WL) | **Merge** into `calc/ai_compute/`; ODC & Terrestrial become first-class |
| Facilities | none (folded into module CapEx) | `Facilities Build` 7-bucket enabling-infra engine | **New module** `calc/facilities_build.py` |
| Segment P&L | none | `Segment P&L` roll-up tab | **New module** `calc/segment_pnl.py` |
| Conservation | R99–R110 (Group P&L block) | dedicated `Conservation` tab R8–R19 | **Re-point** `engine/conservation.py` to the 8 checks; **repair R14** (§4 #6, §6 U4) |
| Valuation | `valuation.py` (stub) | `SoTP - Valuation` populated | **Implement** DCF + SoTP off the 2025–2040 FCF |
| Debt facilities | none | Terafab (CAE R103–R111) + ODC (CAE R131–R140) | **New**: project-finance debt layer, re-scoped per D5 |
| Demand spine | single exogenous demand (Option A) | three inconsistent kg demands (defect #4) | **Unify** to one exogenous demand per program (U0) |
| Canonical labels | V2.16 Allocator/ODC labels | V4.113 CAE/AI-Compute/FB labels | **Re-author** `config/canonical_labels.py` |

**Carried forward unchanged from `context.md` (still binding):** vending-machine module framing (§3.1), demand⊥output type decoupling / Sprint-11f Option A (§3.2), anchor-and-offset year-rows (§3.3), cross-tab refs by canonical label only (§3.4), queue-gate-reserves-first (§3.5), per-unit marginal IRR no fleet-seeding (§3.6), vehicle-level Starlink allocator (§3.7), Mars carve-out off the top on prior-year FCF (§3.8), internal-transfer 4-step pattern (§3.9), explicit fixed-point solver (§3.10), US English (§3.12). The pure-function / one-tab-one-module / canonical-registry / runtime-conservation code principles (`context.md` §6) are unchanged.

---

## §4 — The defects to be fixed (the "highlighted issues")

From `Current_Allocator_Issues_and_the_Case_for_Python_2026-06-04.md`, cross-referenced to the as-is map. The re-baselined Python model must **reproduce these defects' inputs faithfully** (so we can demonstrate the divergence) and then **resolve each** via the U0–U4 roadmap (§6).

| # | Defect | Root cause (as-is) | Fixed by |
|---|---|---|---|
| **F1** | Allocation ≠ what businesses can absorb. 2040: ~$270B allocated vs ~$681B deployed vs ~$822B reported idle — three irreconcilable bases. | Growth caps `R64/65/66` mismeasure deployment (~2.5×); enabling-infra (Facilities!R63-class) sits in the deploy base but not the cap base. | **U1** three-bucket split + cap-base reconciliation |
| **F2** | Cash & launch decided by unrelated rules → contradict. CL wins ~80% of cash (high per-unit IRR, tiny market) then claws back; needs slots not cash. | Cash softmax (R28–R44) and pro-rata kg gate (R50/51/52) rank independently, never reconciled. | **U2** unified two-resource allocator (cross-resource MIN + bounded cascade) |
| **F3** | Funds negative-return businesses. | 5% floor props every program regardless of economics. | **D1**: keep 5% *soft* floor (base scope); optional **asymmetric floor** (drops once IRR<0 with falling deployment) — Vlad's call, not base |
| **F4** | Three inconsistent demand numbers (~139M / 153M / 527M kg). Binding flag reads the wrong one and reports the opposite of reality. | Fleet-sizing demand (R102, inflated), rationing demand (R46), and binding-flag input differ; `R99` inflated to saturation-headroom max. | **U0** demand-spine unification (one exogenous demand per program) |
| **F5** | Workarounds bypass the engine. ODC funded by a debt facility *around* the allocator (`R134` bypasses pool → `AI!R30 += R134`; ~3× the pool allocation in 2030). | ODC facility sized as "allocator shortfall" and routed outside the spine. | **U3** fold ODC bypass into the spine; re-scope Terafab as genuine project debt |
| **F6** | Safety net broken where most needed. `Conservation!R14` omits ODC facility flows (`R134/135/136`) → fails every year a facility is live (~2028–2036). | R14 never updated when debt facilities were added. | **U4** repair/extend R14 + add new identities |
| **F7** | Fragile to recalculate (circular, iteration-dependent; saved-with-iteration-off has silently zeroed years). | Rank-order cascade hand-unrolled across 150+ rows; circular cash loop needs Excel iterative calc. | **The Python re-base itself** — the allocator becomes a pure function over predetermined inputs; no iterative-calc setting, no bistability (the Case-for-Python thesis) |

**The Case-for-Python thesis, now realised model-wide:** the allocation rule lives in one readable, testable Python function; "fund highest-return first, cap at absorbable demand, cascade the rest" is a loop, not 150 spillover rows; cash and launch are allocated **together in one pass** so they cannot contradict; conservation becomes assertions, not stale formulas; policy (strict-rank vs proportional vs hurdle vs soft-floor) is swappable. Because the design only uses **predetermined inputs** (prior-year IRR, prior-year cash, already-built fleet), the allocator is a pure year-by-year function — eliminating F7 by construction.

---

## §5 — The locked target architecture (the unified engine)

From the two Unified Allocation docs; resolved with Vlad 2026-06-04. **Do not relitigate** these.

### §5.1 Three CapEx buckets — classify every dollar once

| Bucket | Examples | Funding | In per-unit IRR? |
|---|---|---|---|
| **1. Growth** | new Starlink/ODC sats, new Terr MW, marginal Starship/F9 launches | IRR-ranked allocation (prior-yr IRR + 5% floor) from the cash pool | **Yes** — per-unit marginal CapEx is the IRR's `−CapEx` leg |
| **2. Enabling infrastructure** | **Terafab** chip fab, **Gigabay** ship factory (FB!R19), ground/optical stations, launch-site infra (the `Facilities Build` tab) | Senior claim + project-finance debt, sized to forward exogenous demand; books **no FCF**; transfers output **at-cost** | **No** — only the at-cost unit price (chip $/sat, launch $/kg) enters module COGS |
| **3. Maintenance / refresh** | replacement sats, fleet refurb, sustaining capex | Predetermined senior claim in the queue gate | No |

**At-cost transfer-price rule (bucket 2, acyclicity-critical):** struck on a *predetermined* basis — amortised build cost over **design capacity / planned lifetime output**, or Wright's-law unit cost on **prior cumulative** volume. **Never** build-cost ÷ this-year realised volume (crushes early-life IRR on an idle asset *and* closes a within-year loop). This single taxonomy resolves F1 and Vlad's lumpy-Terafab nervousness simultaneously.

### §5.2 The unified engine (target logic)

```
ONE cash pool through the queue gate, then SENIOR CLAIMS off the top, in order:
  Pool after gate (R21)
    − corporate claims (existing)
    − MAINTENANCE capex            (NEW senior claim, bucket 3)
    − ENABLING-INFRA equity portion (bucket 2; project debt covers the lump incl. Terafab)
    − LM carve-out (R24; keep — IRR-responsive on prior-yr FCF, already acyclic)
    − ODC strategic seed           (NEW; pre-revenue ramp, off both pools)
  = Remaining pool for IRR-weighted GROWTH allocation

PRIORITY (order only, never quantity):
  w_i = 2-yr-avg PRIOR-year marginal IRR, across FOUR first-class programs
        {Starlink, ODC, Terrestrial, Customer Launch}
  share_i = floor + (1 − N·floor)·(w_i / Σw)          [5% soft floor KEPT — D1]
  (retire the AI roll-up IRR R30 + the Level-2 ODC/Terr softmax R76–R94 — ODC & Terr go first-class)

TWO RESOURCES:
  cash pool (above)
  Gigabay build throughput (ships/yr)  — the real shared launch bottleneck (FB!R19); Terrestrial is cash-only
  Same-year build: vehicles built this year, sized to EXOGENOUS demand, capped by Gigabay rate,
                   ranked by PRIOR-year IRR

RECONCILE (deterministic finite cascade — NO iteration):
  cash_funded_i = fill(cash pool, by w_i, capped at growth-demand_i × unit cost)
  slot_funded_i = fill(Gigabay throughput, by w_i, capped at demand_i × ships-per-unit)
  units_i = MIN(cash_funded_i, slot_funded_i, demand_i)
  release slack resource on bound programs → ONE re-cascade → park residual (cash leftover / idle slots),
  both carry to next year.   Reported share = the CAPPED share.
```

**Growth engine (short-run CapEx → long-run growth, acyclically):** deploy → cumulative volume↑ → Wright's cost↓ (on *prior* cumulative) → next-year *prior-year* IRR↑ → next-year share↑. Compounds across years via the cash spine; never forecast within a year. The strategic seed (bucket-2-funded ODC ramp) and project debt (Terafab) bootstrap a program until the lagged loop ignites. This is exactly the live LM carve-out machinery (CAE R95–R98), reused.

### §5.3 The acyclicity firewall (binding on every new/edited Python computation)

- **May reference:** exogenous demand (a market forecast), prior-year IRR, prior cost/volume (Wright's), a chosen ramp/leverage policy, the predetermined cash pool / BoY fleet.
- **May NOT reference:** this-year IRR, this-year realised deployment, this-year returns.
- The **only** legitimate within-year cycle is the existing queue gate (iteration ON). **Add no second cycle.** The within-year two-pool reconciliation is a strict feed-forward cascade, never iterated.
- **In Python this is enforced at the type level** (per `context.md` §3.2): demand and output are distinct dataclasses; the allocation function takes *prior-year* IRR/cost/fleet and *exogenous* demand, and returns this-year cash/slots. A test asserts via import inspection that no allocation input transitively references a this-year output type.
- **Proof obligation each sprint:** (a) precedent scan — no new computation touches a realised/this-year-IRR value; (b) iteration-OFF circular-cell diff = 0 new cells; (c) 5× round-trip stability; (d) edge-year conservation (2025 / 2030 / 2035 / 2040).

### §5.4 The eight locked decisions (D1–D8)

| # | Decision | Resolution |
|---|---|---|
| D1 | Priority weight | Keep the **5% soft floor** `share = floor + (1−N·floor)·w`. NOT a hurdle. Optional later: asymmetric floor (Vlad's call, not base scope). |
| D2 | What the allocator gates | **Growth slice only**, via the three-bucket taxonomy. |
| D3 | Smoothing | **2-yr prior-IRR average**; window/α is MC. |
| D4 | Strategic seed | **Pre-revenue ODC only**, off both pools, graduates on lagged IRR. |
| D5 | Debt / facilities | Keep **Terafab as genuine project-finance debt, OUT of the IRR**, repaid from at-cost chip transfer over fab life. Re-scope the **ODC bypass into the spine**. Repair Conservation R14. |
| D6 | LM kg bound | **Yes** — MC-bounded share cap; fleet target includes LM demand. |
| D7 | Forward-demand buffer | **1.25×** base, MC. |
| D8 | Launch-vehicle capital | **Same-year build, sized to exogenous module demand, ranked by prior-year IRR. Keep module-owned launch CapEx.** Second resource = Gigabay throughput (ships/yr). |

---

## §6 — Execution roadmap

The work splits into two phases. **Phase R** re-baselines the model to V4.113 with adherence (spec-first). **Phase U (U0–U4)** lands the unified-allocation fixes. The Unified docs' sprint sequence is preserved; each U-sprint's gate becomes a Python acceptance test.

### Phase R — V4.113 adherence re-baseline

| Sprint | Scope | Gate (acceptance) |
|---|---|---|
| **R0 — Ingest & horizon** | Re-point ingest to `SpaceX V4.113.xlsx`; horizon 2025–2040 (16); re-author `canonical_labels.py` for V4.113 tabs; rebuild the diagnostic value-snapshot. | Every V4.113 column-A label resolves; Assumptions schema validates; horizon vectors length-16; 2025 anchors load. |
| **R1 — Module re-base** | Re-point Starlink, Customer Launch, Lunar-Mars, Group P&L, Demand Curves to V4.113 labels; **merge ODC+AI Stack → `calc/ai_compute/`** (dual-revenue, on-tab Wright's); add `calc/segment_pnl.py`. | Per-module structure mirrors V4.113 tabs; vending-machine framing holds; internal-transfer conservation holds. |
| **R2 — Enabling-infra & debt layer** | New `calc/facilities_build.py` (7 buckets); new debt-facility layer (Terafab CAE R103–R111, ODC CAE R131–R140) as ingested as-is. | FB CapEx conservation (R44 ≤ 0); facility Σdraw−Σrepay−balance = 0 (R111, R140). |
| **R3 — Allocator as-is** | Rebuild `calc/allocator/` to the **current** CAE design (softmax β·IRR + soft floor + water-fill + pro-rata kg) as a faithful baseline — *defects intact*, documented. | Structural invariants hold; allocator outputs reconcile to CAE within divergence-triage; defects F1–F6 reproduce (documented, not "fixed"). |
| **R4 — Reconciliation & calibration** | All four reconciliation blocks (A structural / B 2025 external anchors / C sense / D spec-coverage); divergence report vs V4.113 cached values with triage. | Block A/B/C/D pass; every divergence triaged (code/xlsx/intentional); solver converges <1000 iters @1e-7. |

### Phase U — Unified allocation (defect remediation)

Mirrors the Unified docs' U0–U4. **Each U-sprint is authored against the live book *after* the prior lands, and re-resolves the row map first.** In Python each gate is an automated test.

| Sprint | Scope | Gate |
|---|---|---|
| **U0 — Demand-spine unification** *(decision-independent prerequisite, F4)* | One realistic exogenous deployable-demand per program. De-inflate Starlink desired-kg `CAE!R99 → Starlink!R159` basis (2026+); make `R102 ≡ R46`; point `VB!R104` and binding flag `R49` at the same total; retire orphan `VB!R67`. | 2030 desired ≈ realistic annual (not ~527M/431.7M); fleet-sizing, rationing & binding flag read ONE number; binding flag honest (e.g. 2030=1, 2035=0, 2040=1); 2025 frozen; conservation OK; 5× stable; acyclic. |
| **U1 — Three-bucket split + cap-base** *(F1)* | Route enabling infra (FB!R63-class) **out** of the per-unit IRR/deploy base (`AI!R161`); install **at-cost chip transfer** into ODC/Terr COGS on a predetermined absorption basis; add the **maintenance senior claim** to the queue gate; align growth caps `R64/65/66`; verify/clear Terafab double-count (fab in deploy base *and* per-sat chip COGS `AI!R38/39`). | allocated_growth ≈ deployed_growth (≤ small park); ODC/Terr IRR not crushed by the fab; leftover reconciles; edge years 2025/30/35/40; conservation OK. |
| **U2 — Unified two-resource allocator** *(F2, F3)* | One 2-yr-avg prior-IRR weight + 5% floor across {Starlink, ODC, Terrestrial, CL}; retire AI roll-up IRR `R30` + Level-2 `R76–R94`; two-resource fill (cash + Gigabay throughput) + cross-resource MIN + bounded finite cascade; reported capped share; same-year build (exogenous-sized, Gigabay-capped, prior-IRR-ranked). | acyclicity diff = 0 new circular cells (iteration-OFF); Σalloc ≤ pool, Σslots ≤ throughput; no negative-IRR program funded beyond the kept floor; capped shares sane (CL never 80%); 5× stable. |
| **U3 — Seed + debt re-scope** *(F5)* | ODC pre-revenue seed off both pools (graduates on lagged IRR); Terafab → genuine project-finance debt (out of IRR, repaid from at-cost chip transfer over fab life); fold ODC bypass into the spine (remove `AI!R30 += R134`); no double-fund. | seed deploys the ramp and sunsets on graduation; Terafab cash-neutral over life (Σdraw = Σrepay − interest); ODC no longer pool-bypassed; conservation OK. |
| **U4 — Guardrail repair + supersession sweep** *(F6)* | Repair/extend **Conservation R14** for all facility + enabling-infra flows (`… − R134 + R135 + R136`); add new identities (Σalloc ≤ pool; Σslots ≤ throughput; deploy = seed + queue per program; both leftovers parked; at-cost transfer conservation); clear dead residue (§9). | R14 OK every year; all conservation green; supersession list cleared; full 5× stability + calibration ±5%. |

---

## §7 — Code architecture for the re-baseline

Inherits `context.md` §5–§10 wholesale; the deltas below are V4.113-specific.

### §7.1 Package layout deltas

```
src/spacex_model/calc/
  allocator/                 REBUILT to CAE design
    cash_pool.py             R8–R11 (cash spine; Rule-23 year-chained EoY→BoY)
    queue_gate.py            R13–R21 (+ NEW maintenance senior claim, U1)
    carve_out.py             R23–R25, R95–R98 (LM, IRR-responsive on prior-yr FCF)
    priority.py              w_i = 2-yr-avg prior-yr IRR; soft floor; share_i  (D1/D3)
    two_resource_fill.py     cash + Gigabay throughput; cross-resource MIN; bounded cascade (U2)
    kg_rationing.py          R45–R52 as-is in Phase R; SUPERSEDED by two_resource_fill in U2
    water_fill.py            R112–R129 (logic reused/re-pointed)
    strategic_seed.py        NEW (D4; ODC pre-revenue, graduates on lagged IRR)
    debt_facilities.py       Terafab + ODC facilities (D5; re-scoped in U3)
  ai_compute/                NEW (merges V2.16 odc.py + ai_stack.py)
  facilities_build.py        NEW (7-bucket enabling-infra engine; bucket-2 funding)
  vehicle_build.py           demand-pulled fleet; module-owned launch CapEx; Gigabay-capped build
  segment_pnl.py             NEW
engine/conservation.py       REBUILT to Conservation tab R8–R19; R14 repaired in U4
config/constants.py          HORIZON = 2025..2040 (16); ITER = (1000, 1e-7)
config/canonical_labels.py   RE-AUTHORED for V4.113 tabs
```

### §7.2 Demand⊥output decoupling, generalised to the firewall

The Sprint-11f Option A type split (`DemandInputs` ⊥ `OutputResults`) generalises into the acyclicity firewall (§5.3): the allocation function signature takes only **prior-year** economic signals and **exogenous** demand. A linter test inspects the allocator's transitive imports and fails if any allocation input type reaches a this-year output type.

### §7.3 Policy as a swappable strategy

Per the Case-for-Python doc, priority policy is a strategy object: `SoftFloorPolicy` (base, D1), `AsymmetricFloorPolicy` (optional), `StrictRankPolicy`, `ProportionalPolicy`, `HurdlePolicy` (for A/B comparison only — the hard hurdle never landed and is not base scope). One-line swap; each is unit-tested.

### §7.4 Solver contract update

Iteration ON, **1000 iters / 1e-7** (V4.113 settings). The only loop is the queue gate; the two-pool reconciliation is a finite cascade outside the loop. Convergence asserted, not assumed.

### §7.5 Canonical-label registry is the row-shift firewall

Because rows shift between builds, **no integer row position appears in calc code.** `canonical_labels.py` maps every V4.113 label to a typed accessor; renaming a label is a constitutional event (registry + readers + DEV_LOG entry). This is the Python equivalent of the docs' "resolve labels to direct addresses once, write the direct ref."

---

## §8 — Monte Carlo inputs to register (Rule 18, at creation)

New MC inputs introduced by the unified engine (register with ranges; from the Unified docs §6 / §10):

| Param | Base | Range | Dist |
|---|---|---|---|
| Soft floor (kept) | 5% | 0–8% | triangle |
| Priority IRR-avg window / α | 2 yr | 1–3 yr | discrete |
| ODC seed ramp (units/yr) | TBD | bounded | triangle |
| Seed graduation IRR | = floor-implied hurdle | ±4% | triangle |
| Forward-demand buffer | 1.25× | 1.0–1.75× | triangle |
| LM kg cap (share of capacity) | 18% | 10–30% | triangle |
| Chip-transfer absorption basis | design-capacity | lifetime-output ↔ Wright's | discrete (structural) |
| Terafab leverage / draw cap | existing | per facility | structural |

These flow through the existing MC engine (`context.md` §9): seven distribution types, per-trial seeds, tornado / PRCC / 1D-2D sensitivity. Note MC trial counts and percentile bands are unchanged; only the input registry grows.

---

## §9 — Supersession & cleanup (track only; retire after replacements prove out)

- **Dead/empty now:** `CAE!R67–R72` (rank residue), `R74` (TEMP placeholder), `VB!R67` (orphan — retire in U0 once consumer count confirmed 0).
- **Superseded by the unified spine (U2–U4):** pro-rata kg gate `R50/51/52`; AI roll-up IRR `R30` + Level-2 `R76–R94`; binding flag `R49` (re-pointed in U0, may retire); cash water-fill `R112–R129` (logic reused, re-pointed); Level-2 memo `R93`.
- **Re-scoped, not deleted:** Terafab `R103–R111` (→ project debt, out of IRR); ODC facility `R131–R140` (→ folded into spine); LM carve-out + kg reserve (kept, bounded).
- **Repair not retire:** `Conservation!R14`.

In Python, "supersede" = delete the function + its label-registry entry + tests, with a DEV_LOG entry; no dead code lingers once its replacement passes its gate.

---

## §10 — Acceptance criteria (definition of done)

The re-baseline + remediation is **done** when all hold on `SpaceX V4.113.xlsx`:

1. **Adherence (spec-first):** Block A structural invariants pass every year 2025–2040; Block B 2025 external anchors within tolerance; Block C sense checks pass; Block D spec-coverage complete. Every V4.113 cached-value divergence is triaged (code-bug / xlsx-bug / intentional-spec-difference) and logged — *no untriaged divergence*.
2. **All seven defects resolved:** F1 (allocated ≈ deployed, no phantom idle), F2 (cash+launch one pass, CL never ~80%), F3 (no negative-IRR funding beyond the kept floor), F4 (one exogenous demand per program; binding flag honest), F5 (ODC in the spine, Terafab as genuine debt), F6 (Conservation R14 green every year), F7 (allocator is a pure year-by-year function, no iterative-calc fragility).
3. **Acyclicity firewall proven** each U-sprint: precedent scan clean, iteration-OFF diff = 0 new circular cells, 5× round-trip stable, edge-year conservation.
4. **Conservation tab green:** all of R8–R15 within tolerance; R17 ALL-OK true every year.
5. **Traceability:** Model Translation Log regenerated for V4.113; every `calc/` public function carries the four-tag docstring; DEV_LOG entry per material change.
6. **MC:** new inputs registered with ranges; deterministic + MC runs reproducible (seeded, byte-stable).

---

## §11 — Risks & open verification items (carry forward)

- Confirm `Starlink!R159` precedents are exogenous (Demand Curves / row 167 × mass) — no capacity/allocation/this-yr-IRR (U0).
- Confirm the live horizon's last column is **2040** for every tab (verified for CAE; re-confirm Starlink/AI/VB which are 78 cols wide — extra columns are likely scratch/working, not horizon).
- U1: confirm whether the fab (Facilities) is **double-counted** (in the AI roll-up deploy base AND inside per-sat chip COGS `AI!R38/39`).
- U1: confirm LM-in-the-fleet-build-target status — if LM kg is reserved off a fleet sized only for the other three, it crowds them out without growing the fleet.
- Confirm `Conservation!R14` is the only broken guardrail and scope its repair to U4.
- **Version-drift risk:** the Unified docs are written against **V4.109**; the canonical book is **V4.113**. Row maps in those docs are indicative, not literal — re-resolve every label against V4.113 (and the live book per sprint). This PRD's §2.3 map is the V4.113 starting point.
- **Horizon-truncation risk:** any inherited V2.16 ramp, test, or scenario assuming 2050 must be re-pointed to 2040, or it silently runs past the model's end.

---

## §12 — What stays in Excel vs Python

Per the locked decision, **the entire model — all features and functions — is computed in Python.** Excel's role narrows to:

- **Canonical input source:** Assumptions (Base Case + MC ranges), Demand Curves breakpoints, opening balances, the 2025 anchors. Python ingests these (formula pass + value pass) and treats them as authoritative *inputs*.
- **Diagnostic reference:** V4.113 cached *derived* values are a snapshot for divergence triage — not a numerical oracle.

There is no Excel⇄Python co-simulation and no write-back of derived values to the source workbook. The handoff is one-directional: Excel inputs → Python model → reports / web UI / audit logs.

---

## §13 — Deliverables

1. Re-baselined `src/spacex_model/` (all calc modules on V4.113; allocator rebuilt; AI-Compute / Facilities Build / Segment P&L / debt facilities added).
2. Re-authored `config/canonical_labels.py` and `config/constants.py` (2025–2040, 1000/1e-7).
3. Rebuilt `engine/conservation.py` (Conservation tab R8–R19; R14 repaired).
4. Test suite re-pointed to length-16 horizon; per-U-sprint gate tests; acyclicity-firewall linter test; policy-strategy unit tests.
5. Regenerated `docs/model_translation_log.csv`, `docs/reconciliation_report.md`, divergence report, `docs/architecture_diagram.md`.
6. Append-only `docs/DEV_LOG.md` entries per sprint; `docs/changelog.md` mirroring the Claude Log.
7. MC input registry updated (§8).

---

## §14 — Sequencing summary

```
R0 ingest+horizon → R1 modules → R2 enabling-infra+debt → R3 allocator as-is → R4 reconcile/calibrate
   → U0 demand spine → U1 three-bucket → U2 two-resource allocator → U3 seed+debt → U4 guardrails+sweep
```
Phase R establishes faithful V4.113 adherence (defects reproduced & documented). Phase U lands the fixes, each gated, each re-resolving the live row map first, each with a DEV_LOG entry and Vlad sign-off.

---

## §15 — Glossary (selected)

- **CAE** — Cash Allocation Engine tab (V4.113).
- **FB** — Facilities Build tab. **VB** — Vehicle Build tab.
- **Three-bucket taxonomy** — Growth (in IRR) / Enabling infra (debt+senior, at-cost transfer) / Maintenance (senior claim).
- **Soft floor** — `share = floor + (1−N·floor)·w`; the kept 5% (D1).
- **Acyclicity firewall** — the rule that no new computation references this-year IRR / deployment / returns.
- **Cash spine** — R56 Cash EoY → next-year R8 Cash BoY (Rule-23 year-chained).
- **Gigabay throughput** — installed Starship build capacity, ships/yr (FB!R19); the second scarce resource.
- **Divergence triage** — code-bug / xlsx-bug / intentional-spec-difference classification of any code-vs-xlsx delta.

---

## §16 — Amendment Log

| Ver | Date | Change | Author |
|---|---|---|---|
| 2.0 | 2026-06-04 | New PRD: full re-baseline of the entire model to V4.113, end-to-end in Python, spec-first/divergence-triaged adherence, folding in the Unified Allocation U0–U4 remediation. Supersedes PRD.md v1.0. | M. Hale |
