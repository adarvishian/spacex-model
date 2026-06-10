# Phase 1 Research Synthesis — Pre Existing Model Package

**Author:** Dr. Marcus Hale (port lead)
**Date:** 2026-05-28
**Status:** Phase 1 deliverable. Read before Phase 2 (build approach proposal). Open questions in §10 need Vlad sign-off before Phase 3 (PRD).

---

## 1. Executive summary

The Pre Existing Model Package is the corpus behind a 26-year (2025–2050) bottom-up valuation of SpaceX — five operating modules (Customer Launch, Starlink, ODC, AI Stack, Lunar Mars) plus cross-cutting Allocator, OpEx, CapEx, Group P&L, and Valuation layers. The live workbook (`SpaceX Model V2.16.xlsx`, 466 KB, 15 sheets, ~21,500 non-empty cells, ~10,900 formula cells) is the product of an Excel-based sprint workflow that has been running since mid-May 2026 and is mid-Sprint-11 as of the package's prep date (2026-05-27).

V2.16's structure exactly matches what `context.md` §2.2 asserts — sheet inventory, row/column counts, formula counts, and array-formula counts all reconcile cell-for-cell. Iterative calc is ON workbook-wide; the VBA archive is present but non-load-bearing per Memory Snapshot 1.6 / context.md §2.2; zero defined names (every cross-tab reference resolves via `INDEX/MATCH` on canonical column-A labels).

The package contains the **constitutional layer** (7 docs in `00_Constitutional_Docs/`), the **current state** (V2.16 + Sprint 11 series specs in `01_Current_State/`), **fresh-restart inputs** (V30.5 + Q4'25 Cleanup + Assumptions Build Plan in `02_Fresh_Restart_Inputs/`), **sprint history** (Sprints 1–10.7 + patches in `03_Sprint_History/`), **module briefs** for two parallel collaborators (`04_Module_Briefs/`), **reference material** (notably the AI Stack scoping doc in `05_Reference_Material/`), and a **memory snapshot** (`06_Memory_Snapshot/`).

**The package was prepared for human collaborators (Colleague A, Colleague B) to continue the Excel sprint workflow** — not directly for the code port. The constitutional layer (23 Execution Rules, 23 Lessons Learned, the Architecture & Methodology spec with its §20 Sprint 11 amendments block, and the Memory Snapshot critical locks) is identical regardless of language. The port runs in a different cognitive mode (porting to Python rather than wiring Excel cells) but honors the same locks.

---

## 2. Architectural locks digested (constitutional layer)

The locks below are taken from `02_Architecture_and_Methodology.md`, the 23 Execution Rules, the 23 Lessons Learned, and the §20 Sprint 11 amendments block. They are the load-bearing decisions the code port must honor. Where context.md already summarizes a lock, I cross-reference rather than restate.

**2.1 Vending-machine module framing** (Architecture §3, Principle 8, Rule 13). Every module P&L: `Revenue → COGS → Gross Profit = Module EBITDA → CapEx → Module FCF`. No R&D, no SG&A, no corporate overhead, no taxes on any module — those live in `opex.py` and `group_pnl.py` only. Module COGS contains only direct production costs (constellation/fleet D&A, internal at-cost launch services, internal bandwidth services, internal compute services, ground ops %, spectrum amort BB-only, terminal COGS Starlink-only, insurance, other COGS catch-all). `Module EBITDA` is mathematically Gross Profit but the label is retained per Principle 7.

**2.2 Demand purely exogenous (Sprint 11f Option A)** (Memory 1.8, Sprint_11f_Spec §2, Architecture §6.5 + §20.3 amendments). The single most important architectural lock. **The code implements this from day one.** Demand reads anchor × learning × year-mask + exogenous facility CapEx — no recursion. Output reads `MIN(cash_from_allocator / unit_cost, internal_target)` — bounded by cash, never feeds demand. Enforced at the type level: `DemandInputs` and `OutputResult` are distinct dataclasses; `compute_demand(...)` has no transitive reference to any output type. A test imports both functions and asserts this via inspection.

**2.3 Anchor-and-offset year-row pattern** (Memory 1.2, Rule 23, Principle 12). In Excel: `$D$anchor × (1+rate)^E$5`. In code: 26-element numpy arrays indexed `[0..25]` = years `[2025..2050]`; vectorized expression over the offset vector. Year-chained Rule 23 exceptions (cumulative sums, Cash BoY, BV running sums, ratchet latches) flagged inline.

**2.4 Cross-tab references by canonical label only** (Memory 1.3, Rule 12, Principle 3/14). Code never indexes a result by integer row position. A `canonical_labels.py` registry maps every canonical label to a typed accessor. Renaming a label is a constitutional event.

**2.5 Queue gate reserves non-module claims first** (Memory 1.4, Architecture §6.2, Principle 4). `Available_cash_for_IRR_queue = max(0, Cash_BoY − OpEx − Corp_CapEx − Spectrum_CapEx − Taxes − Mars_carveout − Vehicle_build_claim)`. Module CapEx allocation runs after this subtraction. Within-year circularity resolved by iterative solver.

**2.6 Per-sat / per-launch marginal IRR** (Memory 1.5, Architecture §5, Principle 2). `CF stream = [−cost_per_unit(T), net_marginal_revenue(T+1), …, net_marginal_revenue(T+N)]`; `Spot IRR(T)`, `Forward IRR(T+2)`, `Blended IRR = 0.3 × Spot + 0.7 × Forward`. Per-unit, not fleet-level. No `MAX(CumCapEx − CumD&A, 1)` NIC denominators. Negative IRR → zero allocation (strict cutoff).

**2.7 Vehicle-level Allocator for Starlink** (Memory 1.9, Architecture §20.1, Sprint 11 Block 1). V2 BB / V2 DTC / V3 BB / V3 DTC are top-level allocator queue entries with their own per-vehicle IRR. V2 vehicles have NO kg allocation (fly on F9, not Starship). V2→V3 transition emerges from IRR + cash allocation + three physical gates (V3 startup year, V2 phase-out year, F9 supply); no hardcoded ratchets (the R43 ratchet flag and Assumptions R320 V2 DTC cap are retired per §20.6).

**2.8 Mars carve-out off the top, prior-year FCF** (Architecture §6.2 / §11.1, Principle 22). `Mars_carveout(T) = max(Mars_floor, Group_FCF(T−1) × Mars_pct)`. The t-1 read is the circularity breaker. Both `Mars_pct` and `Mars_floor` are MC-variable (Base Case 15% / $1B floor; MC range 3%-35% / $500M-$2.5B).

**2.9 Internal transfer 4-step pattern** (Architecture §7, Principle 9, Rule 21). For every internal flow (launch services, bandwidth, compute): source books internal transfer revenue, consumer books matching cost in COGS, Group P&L elimination row subtracts the flow once, conservation check row verifies source rev = Σ consumer COGS. All three transfer prices locked **fully-allocated** (variable cash cost + non-cash D&A share) per the 2026-05-20 accounting methodology amendments. This means consuming modules absorb vehicle D&A / bandwidth D&A / compute D&A in their COGS.

**2.10 LM BV is a SoTP terminal value input, NOT a P&L D&A flow** (Architecture §20.5, Sprint 11e shipped). Critical correction. Sprint 7 originally routed `BV depreciation — Lunar` + `BV depreciation — Mars` into Group P&L R28 Group D&A formula, producing phantom $478B/yr D&A by 2050 from accumulated $5.6T LM BV. **V2.16 has this excised**: LM Module D&A is now proper cash-cap depreciation (cumulative LM Module CapEx ÷ capital_lifetime); the BV decay rows are retained as memos only for Valuation tab terminal anchor calculation per Architecture §11.4. Effect: Group D&A 2050 collapses from $484B → ~$6B; Group FCF 2050 swings from +$337B (illusory) → ~−$90B (correct). Calibration targets revise accordingly (see §3 below).

**2.11 Iterative-calc convergence is part of the contract** (Memory 1.6). 100 iterations, 0.001 absolute tolerance. Three known simultaneity loops: Starlink ↔ Starlink Capacity (%×Revenue), Allocator ↔ modules (CapEx ← cash alloc ← IRR ← FCF ← CapEx), Cash BoY ↔ Group FCF (broken by t-1 read).

**2.12 No row insertions / no version surfacing / US English** (Rule 10, Memory 3.2, Memory 3.5). Code analog: canonical-label registry is append-only; version numbers not surfaced in code or user-facing state; US English everywhere (modeling, optimization — not modelling, optimisation).

**2.13 Pre-IPO debt facility** (Architecture §20.9, Sprint 11c partial / Sprint 11e completed). $20B bridge loan drawn in 2025 per S-1 disclosure, with no repayment or interest expense modeled (deferred). Cash Pool Tracker formula: `Cash_BoY(N) = Cash_BoY(N−1) + Group_FCF(N−1) + IPO_injection(N) + Pre_IPO_debt_facility(N)`. IPO 2027, $30B. Effect: Available cash for IRR queue 2025 ≈ $13.7B (vs $0 in pre-bridge state).

**2.14 Pre-revenue R&D switching formula** (Architecture §12.1, locked 2026-05-20, Sprint 8 implements). ODC and AI Stack have heavy R&D pre-revenue but the standard `% × revenue` formula gives zero. Switching formula: `R&D_t = MAX($-profile_t, % × revenue_t)`. Two new Assumptions year-rows: `ODC R&D $-profile` (Base Case $200M 2025 → $500M 2027 → declining), `AI Stack R&D $-profile` (Base Case $50M 2025 → $300M 2028 → declining). Both MC-variable (lognormal).

**2.15 Fully-allocated at-cost transfer pricing** (Architecture §7.1/7.2/7.3, locked 2026-05-20). Symmetric across all three internal flows: launch services (rate per launch = variable cost + vehicle D&A per launch), bandwidth (rate per Gbps/yr = pool cost basis ÷ total active pool Gbps; BB pool basis includes spectrum amort), compute (rate per PFLOP-hr = ODC fully-allocated annual cost ÷ ODC total annual PFLOP-hrs; fully-allocated cost = sat D&A + paid launch services + paid bandwidth + insurance + other COGS). This is a major architectural lock — module-side IRRs and at-cost pricing depend on it.

**2.16 First-year (2025) override convention** (Sprint Roadmap §6.9, Assumptions Tab Spec §5, Sprint 10 lock). Once the allocator brain lights up, it tries to drive 2025 module CapEx from the IRR queue, but 2025 historical actuals are Mach33-anchored (V2 BB 2,987 launched, V2 DTC 182, F9 manufactured 17, F9 customer launches 38.58). Convention: column D (2025) = historical actual, locked; allocator drives column E:AC (2026+) only. The code should expose this as an explicit "first-year override" flag on the Allocator, not bury it in a magic constant.

---

## 3. Critical calibration finding — REVISED 2025 anchors

**This is the single most important point of attention in Phase 2 / Phase 3.** The context.md §2.5 anchor table lists the Q4'25 raw numbers (Group EBITDA $8,690M, Group FCF $3,670M). But **Sprint Roadmap §6.8 was revised 2026-05-22** under a Vlad lock and Sprint 9 executed PASS exact against the revised numbers:

| Anchor (2025) | Context.md §2.5 (Q4'25 raw) | Sprint Roadmap §6.8 (REVISED, the actual target) | Tolerance |
|---|---:|---:|---|
| Group Revenue | $14,650M | $14,650M (unchanged) | ±5% |
| Group Gross Profit | n/a | $9,463M | ±10% |
| **Group EBITDA** | **$8,690M (59.3% margin)** | **$4,904M (32.4% margin)** | **±5% / ±3pp** |
| Group D&A | $1,060M | $1,261M | ±10% |
| Group EBIT | ~$7,630M | ~$4,450M | derived |
| Taxes (21%) | ~$1,600M | ~$934M | derived |
| NOPAT | ~$6,030M | ~$3,516M | derived |
| **Group FCF** | **+$3,670M** | **−$2,569M** | **±10%** |
| Total OpEx | $3,820M | (Sprint 8.5 revised to $4,476M) | ±5% |
| Total Group CapEx | ~$2,030M | $6,345M (Sprint 8 anchor) / ~$7,030M post-Sprint-10 with vehicle build | ±5–10% |
| Mars carve-out | n/a | $1,000M (floor) | exact |

**Why the revision.** Five architectural decompositions explain the gap, per the §6.8 amendment header:
(i) Module D&A is inside COGS via vending-machine framing — so "Group EBITDA" mathematically equals Group Gross Profit minus OpEx (not the standard "Operating Income + D&A"). The Q4'25 raw $8,690M is a standard-EBITDA figure; the Mach33 framing produces $4,904M because the constellation D&A is already netted into module COGS.
(ii) Fully-allocated launch transfer pricing pushes ~$1,200M of vehicle D&A into consuming modules' COGS.
(iii) Pre-revenue R&D $-profile floors ODC $200M + AI Stack $50M (vs pure `% × revenue` which gives $0).
(iv) EchoStar $5B treated as cash CapEx in year 2025.
(v) Mars carve-out $1B treated as real cash drain (Vlad lock 2026-05-22).

The Q4'25 raw anchors are retained as memo rows R122/R123 on Group P&L "for archaeology only — NOT used as halt thresholds."

**Implication for the code port.** The reconciliation framework in context.md §11 and the success criteria in §13 still cite the Q4'25 raw $8,690M EBITDA / $3,670M FCF numbers as Block B external anchors. This is a real conflict that needs Vlad sign-off (see §10.1 below): **does Block B reconcile against the Q4'25 raw anchors (context.md §2.5) or the Sprint Roadmap §6.8 revised targets (Sprint 9 execution)?** They imply different valuations and the code can't target both at once.

My recommendation as port lead: **target the §6.8 revised numbers** as the primary Block B set, because (a) they reflect the Mach33 architectural framing that the code must implement to be internally consistent (module D&A in COGS, fully-allocated at-cost, pre-revenue R&D floors, etc.); (b) Sprint 9 actually executed PASS exact against them, so we know the model can hit them; (c) the Q4'25 raw numbers correspond to a different accounting framework. The Q4'25 raw figures should be retained as "external reasonableness anchors" — informational, not pass/fail.

---

## 4. Module-by-module findings (port scoping)

**4.1 Customer Launch.** Mature in V2.16. F9 external customer launches + Starship customer launches from 2027 with price decline. Per-launch marginal IRR engine. Internal transfer revenue line live. At-cost transfer pricing per Architecture §7.1 (fully-allocated, locked 2026-05-20). The Allocator OUT contract is wired. **Known open thread: the per-launch IRR engine has three compounding bugs** (Customer_Launch_IRR_Fix_Plan.md): unit mismatch on N (years vs launches), per-launch margin masquerading as annual margin, cost slug not fully-allocated. Even after the proposed fix, sanity check still flags ~1700% F9 IRR; deeper rework needed before lock. **The port should implement the per-booster annual IRR with N-years pattern (mirroring Starlink) from day one** and flag the IRR magnitude as a calibration concern rather than replicating the V2.16 bug.

**4.2 Starlink + Starlink Capacity.** Most complex module sprint. Vehicle-level structure (V2 BB / V2 DTC / V3 BB / V3 DTC) per Sprint 11 Block 1. V2 historical fleet retirement (5,246 V2 BB + 650 V2 DTC linear over N=5 years). Bandwidth-driven revenue via Demand Curves (61 BB breakpoints + 56 DTC breakpoints, piecewise-linear lookup via `INDEX/MATCH` bracket-find + manual interp — no `FORECAST` regression). Subscribers DERIVED from revenue ÷ ARPU, not the other way around. Starshield revenue (Mach33 anchor 2025 $2.52B; decay rate 0.25/yr per Q4'25 anchor doc R53 correction). Three physical gates (V3 startup year = 2027, V2 phase-out year = 2028, F9 supply for V2). Starlink Capacity tab aggregates BB + DTC Gbps, ODC bandwidth claim, available bandwidth for external Starlink revenue. **Within-year iterative loop: Starlink ↔ Starlink Capacity %×Revenue.** Code must support iterative solve.

**4.3 ODC.** Dual revenue (Model A energy-anchored + Model B η-anchored), credence-weighted (Pr(A) = 0.6 default, MC-variable). Per-sat marginal IRR engine — and **per-sat IRR is negative throughout the horizon** (Spot -0.39 in 2025, -0.10 in 2030, -0.15 in 2050). Architecture §20.8 explicitly accepts this as "model verdict, not bug" — the allocator correctly refuses to allocate cash to ODC. Sprint 11.5 may revise per-sat revenue OR per-sat cost inputs; until then, ODC stays at zero deployment and zero revenue every year. The code implements the architectural mechanism (allocator masks negative-IRR modules to zero allocation) — does NOT band-aid the IRR to force positive deployment. Internal compute revenue to AI Stack uses at-cost transfer (fully-allocated rate per PFLOP-hr per Architecture §7.3).

**4.4 AI Stack.** Stub in V2.16 — 83 formula cells, mostly empty. Sprint 6 deferred. Code must support AI Stack as a placeholder with `Total Revenue = 0` until the AI Stack sprint runs. The AI Stack architecture is fully scoped in `05_Reference_Material/AI_Stack_Module_Architecture_Scoping.md`: three sub-modules (Compute, Application, Orchestration), business model switch with credence-weighted A/B/C capture matrix, Terafab toggle in L2 COGS, terrestrial-only at the kg-to-LEO claim layer (`Capacity Demand (kg-to-LEO) = 0` permanently per `project_ai_stack_no_launch_demand` lock). Internal compute from ODC at fully-allocated at-cost per Architecture §7.3. **Eight epistemic questions still await Vlad sign-off**, of which Q3 (at-cost vs at-market internal transfer pricing) is the architectural conflict with the 2026-05-20 lock. The port should structure AI Stack as a swappable module that starts as a zeros stub and can be replaced with the full implementation when Sprint 6 lands; the code architecture must be ready for the three-sub-module layout from day one.

**4.5 Lunar Mars.** Strategic carve-out, **NOT in IRR queue**. Pre-revenue throughout 2025-2050. BV engine (labour units 60 kg × hourly output × productivity learning 5%/yr × useful life 5 yrs + hardware mass landed × hardware $/kg) per Sprint 4 / Q4'25 methodology. Mars carve-out off-the-top using prior-year Group FCF × 15% (MC-variable, floor $1B). Lunar Mars Module D&A is proper cash-cap depreciation (cumulative Module CapEx ÷ capital_lifetime 10y). BV decay rows retained as memo only for Valuation tab terminal anchor (`1.5 × Lunar+Mars BV at 2050` per §14.2). Kg reservation off-the-top before kg queue runs. Per-mission IRR deferred (Vlad: "we can change this later").

**4.6 Valuation.** Empty stub in V2.16 (0 formula cells). Architecture §14 fully spec'd: Group DCF with 5-yr-smoothed terminal FCF + Gordon Growth (WACC 10%, g 2.5%); SoTP per-module DCF (per-module WACC = group + risk premium: SL 0bps, CL 100bps, ODC 200bps, AIS 300bps, LM 500bps); SoTP multiples cross-check; comparables anchors; 5×5 sensitivity table on Starship $/kg learning × Starlink TAM inflation. **The port builds the Valuation module ready to consume Group FCF + per-module FCFs from day one**, even though V2.16 has no Valuation logic to reconcile against.

---

## 5. Cross-cutting layers

**5.1 Assumptions tab** is the input source of truth. 11 sections, ~212 inputs, ~290 rows. Column convention: A label, B Base Case (single-value), C notes/source, D-AC year columns 2025-2050, AG MC Min, AH MC Max, AI MC Distribution (`fixed` / `triangle` / `lognormal` / `uniform` / `discrete` / `triangle-yearrow` / `fixed-yearrow`), AJ MC notes. Every input has its MC range populated at creation (Principle 18). Code ingests as a typed `Assumptions` pydantic model with 11 nested submodels + parallel `MCRanges` model.

**5.2 OpEx.** R&D by module (start% / end% / CAGR per line, anchor-and-offset bounded CAGR) + Moon/Mars $-profile + the switching formula for pre-revenue ODC + AI Stack. SG&A by function (S&M 4%→2% → −8%/yr on Starlink+Starshield+CL ext+AI Stack revenue base; G&A 5%→6% +1%/yr on Group rev net of elim; CS 2% flat on Starlink subscription rev; Other 1% flat on Group rev). Total OpEx 2025 = $4,476M (revised per Sprint 8.5; the original $3,820M target was pre-vending-machine-correction).

**5.3 CapEx.** Module CapEx aggregation (reads Module CapEx row from each module via canonical label, **NOT** Capital deployed row — that's diagnostic-only per Architecture §4.2). Corporate CapEx ($110M/yr from HQ + IT + Gen Eng + Other line items with useful lives 30/7/20/20). Spectrum CapEx (EchoStar year-row 2025 $5B / 2026 $8B / 2027 $5B / 2028 $2B / 2029+ $0 = $20B total; 15-yr amortization → flows to Starlink BB COGS as spectrum amort). Vehicle build claim sized at queue gate (forward-aggregate kg demand at year T+lead ÷ payload ÷ launches per vehicle per year × blended build cost).

**5.4 Group P&L.** Conservation block R99-R110: R99 Revenue check, R100 EBITDA check, R101 CapEx check, R102 FCF check, R103 D&A check, R104 EBIT consistency, R105 launch elim, R106 bandwidth elim, R107 compute elim, R108 ALL OK boolean (= `AND(ABS(R99:R107) < 1)`), R109 cash flow identity (= Starting cash + Σ IPO + Σ Group FCF + Σ Bridge loan − Σ deployed CapEx − Σ strategic carve-out − Cash EoY), R110 Σ Module FCF residual (currently −$1,640M trajectory; flagged for module-owner audit). Code computes its own R99-R110; R108 = "OK" all years is a runtime invariant assertion that halts on break.

**5.5 Allocator.** Cash Pool Tracker (Cash BoY year-chained Rule 23 exception, with bridge loan + IPO + prior-FCF inflows). Queue Gate (Architecture §6.2 — reserves non-module claims before IRR queue). Mars carve-out (off-the-top, prior-year FCF, floor + pct both MC-variable). Cash sigmoid queue (7 sub-blocks: CL + 4 SL vehicles + ODC + AIS; per-block 5 rows: label, IRR, demand, weight, proposed allocation). Kg sigmoid queue (5 sub-blocks: CL external Starship + 2 V3 SL vehicles + ODC + AIS; V2 SL vehicles NOT in kg queue because they fly on F9). Vehicle build claim (forward-aggregate kg demand). Central IRR display panel. V2.16 state: queue is wired but deployment binding (§6.5) is NOT yet implemented in V2.16 because Sprint 11d's attempt collapsed due to circular dependency. **Sprint 11f Option A is spec'd but not executed in V2.16 — the code port implements it from day one** (per context.md Decision Log 2026-05-28).

**5.6 Demand Curves.** Piecewise-linear BB + DTC Q→Revenue lookup tables (61 BB breakpoints R82-R142, 56 DTC breakpoints R17-R72) + multiplicative annual TAM shift `(1+inflation)^t × (1+GNI)^t`. Year-row curve evaluators R140-R145 read by Starlink revenue rows via `INDEX/MATCH` bracket-find + manual interp. `FORECAST` is explicitly forbidden (Memory 2.4 — fits a regression line through all points instead of bracket interp).

---

## 6. Sprint history arc (compressed)

The Excel build went sprint-by-sprint from mid-May 2026 (Sprint 0) through 2026-05-26 (Sprint 11e shipped). The arc:

- **Sprint 0** — Assumptions tab (~290 rows, 11 sections).
- **Sprint 1** — Allocator skeleton + module shells (IN/OUT contract pre-wired, bodies empty).
- **Sprint 2** — Launch Capacity tab (Starship + F9, Wright's Law cadence, $/kg cost stack).
- **Sprint 2→3 patch** — F9 retirement engine (launch-driven, not flat 6/yr), F9 demand wiring, Starship ops cost.
- **Sprint 3** — Customer Launch module body.
- **Sprint 3.5 patch** — Drop cadence multiplier from per-launch IRR (was producing 3,272% F9 IRR by treating per-launch margin × cadence; reality is the marginal booster captures ~1 customer launch/yr, not full cadence).
- **Sprint 4** — Starlink module + Starlink Capacity tab.
- **Sprint 5** — ODC module (dual revenue Model A/B, per-sat IRR).
- **Sprint 6** — AI Stack — **deferred** (eight epistemic questions still open). Stub remains.
- **Sprint 7** — Lunar Mars module (BV engine).
- **Sprint 8** — OpEx + CapEx tabs.
- **Sprint 8.5 patch** — OpEx retune ($226M overcount fix on CS Starshield + G&A internal flow); calibration targets amended.
- **Sprint 9** — Group P&L full walk + R99-R110 conservation + **revised §6.8 calibration targets** (the Vlad lock 2026-05-22 that produced the EBITDA $8.69B → $4.90B revision).
- **Sprint 10** — Allocator brain light-up (Cash Pool, Queue Gate, sigmoid blends, Vehicle build claim, First-year override).
- **Sprint 10.5** — Demand Curves rebuild (piecewise-linear Q→Revenue lookup tables; retires Q+P year-row stubs).
- **Sprint 10.7** — Vehicle-level allocator (drafted; superseded by Sprint 11 combined cleanup).
- **Sprint 10.8** — Spectrum License Fee (unblock queue gate by treating EchoStar as cash CapEx).
- **Sprint 11 combined** — Tried to ship vehicle-level allocator + deployment binding + endogenous fleet wiring + LM BV correction + ODC audit all at once. Four plugin chats (11a, 11b/Block 2, 11c, 11d) each got partway. **Sprint 11d collapsed via the circular dependency at zero attractor** (Allocator demand reading actual sat CapEx, which is downstream of cash).
- **Sprint 11e (shipped 2026-05-26, IS V2.16)** — Reduced Sprint 11: LM BV correction + Launch Capacity endogenous Starship fleet + CL R210 + bridge loan Cash BoY completion. Skipped deployment binding (deferred to 11f).
- **Sprint 11f (spec drafted, NOT executed in V2.16)** — Option A architectural rework: decouple sigmoid demand from sigmoid output by type. **The code port implements Option A from day one** per context.md Decision Log 2026-05-28.

The arc tells us: (a) the architecture was hammered into shape through retrofit cascades — most load-bearing methodology surfaced late, after downstream consumers existed; (b) the constitutional discipline (Rule Compliance Preamble, Architecture §20 amendments block, Memory Snapshot critical locks) is the accumulated debugging knowledge; (c) the port has the advantage of starting with the constitutional layer fully formed, but the disadvantage of porting a model whose architecture is still being amended (Sprint 11f spec'd but not in V2.16; Sprint 11.5 ODC unit economics revision pending; bridge loan repayment + interest expense deferred).

---

## 7. V2.16 structural verification

Probed V2.16.xlsx with openpyxl (formula + structure pass; no value-pass consumption, per project rule that xlsx values are diagnostic only). All counts reconcile to context.md §2.2:

| Sheet | Max row | Max col | Non-empty | Formula | Array formula | Matches context.md §2.2 |
|---|---:|---:|---:|---:|---:|---|
| Assumptions | 350 | 36 | 2,700 | 27 | 0 | ✓ |
| Allocator | 171 | 31 | 3,065 | 1,513 | 1,352 | ✓ |
| Launch Capacity | 80 | 29 | 1,024 | 795 | 102 | ✓ |
| Customer Launch | 210 | 31 | 1,792 | 1,047 | 598 | ✓ |
| Starlink | 235 | 29 | 3,180 | 1,853 | 1,142 | ✓ |
| Starlink Capacity | 50 | 29 | 329 | 104 | 156 | ✓ |
| ODC | 210 | 29 | 2,777 | 2,214 | 365 | ✓ |
| AI Stack | 210 | 29 | 418 | 83 | 0 | ✓ (stub confirmed) |
| Lunar Mars | 212 | 32 | 2,644 | 1,905 | 494 | ✓ |
| Group P&L | 125 | 56 | 1,234 | 425 | 650 | ✓ |
| OpEx | 60 | 29 | 821 | 417 | 312 | ✓ |
| CapEx | 47 | 29 | 759 | 494 | 182 | ✓ |
| Valuation | 6 | 29 | 53 | 0 | 0 | ✓ (stub confirmed) |
| Demand Curves | 145 | 36 | 568 | 26 | 104 | ✓ |
| Claude Log | 15 | 6 | 84 | 2 | 0 | ✓ |

Additional structural facts:
- Iterative calc: **ON** (confirmed). `iterateCount` and `iterateDelta` are not explicitly set in the workbook XML — they default to 100 / 0.001 per Excel convention and per Memory 1.6 lock.
- Defined names: **0**. Every cross-tab reference is `Sheet!Cell` literal or `INDEX/MATCH` by canonical column-A label.
- VBA archive: **present** (non-empty `vba_archive`). No defined names attached to VBA. Per context.md §2.2, treat as evidence only — extract and inspect during ingest, but assume non-load-bearing unless a macro is shown to drive a calc.
- External links: **0**.

Context.md is current. No drift detected between the constitutional docs and V2.16's actual structure.

---

## 8. Test strategy implications (inherited from constitutional docs)

The port's reconciliation framework (context.md §11) defines four pass blocks: Block A structural invariants, Block B external Q4'25 anchors, Block C sense / sanity checks, Block D Architecture spec coverage. The constitutional docs further specify:

**8.1 Block A invariants** (already enumerated in context.md §2.5). R108 "OK" all years; R99-R107 residuals ≤ $1mm; Σ module cash allocations ≤ Available cash for IRR queue; Σ module kg allocations ≤ Capacity available for IRR queue; negative-IRR cutoff strict every year; Module EBITDA == Module Gross Profit every module every year; internal flow conservation every flow every year; iterative solver converges in < 100 iters with < 0.001 residual.

**8.2 Block B anchors** — needs Vlad sign-off whether to use the Q4'25 raw figures in context.md §2.5 or the Sprint Roadmap §6.8 revised figures. See §10.1 below.

**8.3 Block C sense checks** (Architecture / Roadmap §5.6, Rule 15). Implied DTC subs 2025 < 15M; F9 launches 2025 ∈ [165, 177]; Starship launches 2025 = 0 exact; Wright's Law cost-per-unit monotone non-increasing in cumulative units; ODC fleet 2030 ∈ [500, 15000] (sanity range — and given the negative-IRR-throughout-horizon lock, ODC should land at 0 unless inputs are revised); Mars BV 2040 ∈ [$500B, $5T]; Group FCF 2025 ∈ [$2B, $6B] vs Q4'25 raw OR Group FCF 2025 ∈ [−$3.5B, −$2.0B] vs Sprint 9 revised — needs to align with §10.1 resolution; no `#DIV/0!`-equivalent (no NaN, no inf) in any year-row output.

**8.4 Block D coverage**. Every public function in `calc/` has the four-tag docstring (Excel cell, Excel label, Architecture ref, Principle). Every Architecture spec section §1-§20 maps to at least one code module. Every canonical label in V2.16 column A maps to a label-registry entry OR is documented as intentionally unused.

**8.5 Hypothesis-driven invariant tests** (context.md §11.5). Block A invariants must hold under arbitrary valid Assumptions perturbations, not just Base Case. If conservation holds for Base Case but breaks under perturbation, the code is fragile and the failure surfaces a bug. This is the institutional-grade addition that catches code-side bugs the Excel-side workflow couldn't.

**8.6 Diagnostic divergence reporting vs xlsx** (context.md §11.3, §11.6). Separate test module that produces a divergence report (not pass/fail) against the V2.16 cached values. Each divergence beyond tolerance triggers triage classification: (A) code bug, (B) xlsx bug, (C) intentional architectural difference (e.g., Sprint 11f Option A), (D) spec ambiguity. The code port has a hard advantage here — Sprint 11f Option A in code means significant divergence vs V2.16 in the Allocator demand / allocation rows, all of which classify as (C) and are documented as expected.

---

## 9. Reference-doc nuance (where I disagree with context.md)

context.md is overwhelmingly correct and current. Three points where my reading of the constitutional docs suggests minor refinement:

**9.1 The Block B anchor set conflict** (already covered in §3 above). context.md §2.5 lists Q4'25 raw anchors as the Block B reconciliation target; Sprint Roadmap §6.8 (amended 2026-05-22 with Vlad lock; Sprint 9 PASS exact) revises to a different set. Both can't be Block B at once. Recommendation: §6.8 revised set is primary; Q4'25 raw is informational external reasonableness anchor. Needs Vlad sign-off.

**9.2 The "$293B unallocated cash by 2050" pathology and its resolution.** Memory Snapshot 1.10 says the allocator is "advisory not binding" until Sprint 11f wires deployment binding. The code port implements Option A from day one, which closes this pathology. **The port should expect Group Revenue 2050 to differ from V2.16's $583B in either direction** once deployment binding is live — modules can deploy more (V3 BB at high IRR absorbs cash) OR less (cash starvation in early years no longer masked by advisory-only allocator). This is a diagnostic (C) divergence per §11.6, expected and documented. Should be called out as a known-and-accepted divergence in the PRD.

**9.3 Customer Launch IRR fix is more involved than a "later" patch.** context.md Open Item #1 frames Sprint 11f execution timing decision but doesn't surface the Customer Launch IRR fix as part of the v1 scope. Per Customer_Launch_IRR_Fix_Plan.md, the V2.16 F9 IRR engine prints 287% (the pre-Sprint-3.5 number; 3,272% pre-Sprint-3.5) which the Allocator queue reads. Even the proposed three-bug fix produces ~1,700% F9 IRR — sanity check still flags. The code port must mirror Starlink's per-sat per-year pattern (per-booster annual IRR with N-years) from day one, but should accept that the IRR magnitude will likely fail sanity checks (Block C) until a Sprint 11.5-or-later input revision lands. The PRD should flag this as a known Block C halt expected in early reconciliation runs, with documented disposition.

---

## 10. Open questions requiring Vlad sign-off (before Phase 3 PRD finalizes)

These are the items where I can't make the call alone. Some have a recommended default; some are genuinely open.

**10.1 Block B reconciliation target — Q4'25 raw or Sprint Roadmap §6.8 revised?** Per §3 above. Recommendation: §6.8 revised as primary Block B (it reflects the architectural framing the code must implement and Sprint 9 PASSed exact against it); Q4'25 raw as informational external reasonableness anchor (R122/R123 archaeology memo treatment). **Needs explicit Vlad sign-off because context.md §2.5 currently disagrees with this recommendation.**

**10.2 Sprint 11f Option A execution timing.** Per context.md Open Item #1. Two paths: (a) code reconciles against V2.16 as-shipped and surfaces Sprint 11f's expected delta as a known (C)-type divergence per §11.6; or (b) wait for Sprint 11f PASS in Excel and reconcile against the new baseline. Recommendation: **(a)**. Code implements Option A from day one per the existing context.md Decision Log 2026-05-28; the divergence vs V2.16's pre-Option-A state is documented and accepted; we do not block on Excel-side Sprint 11f execution.

**10.3 AI Stack v1 scope.** Per context.md Open Item #2 and AI_Stack_Module_Architecture_Scoping.md. The Scoping doc has eight open epistemic questions (Q1-Q8) for Vlad sign-off; Q3 (at-cost vs at-market internal transfer pricing) is the architectural conflict with the 2026-05-20 accounting locks. Three options: (a) port stubs AI Stack as zeros, full module ships when Sprint 6 runs in Excel and is then ported (cleanest separation); (b) port implements the Scoping doc's three-sub-module architecture immediately under the Scoping doc's provisional defaults, with the eight Vlad-locks left as configurable; (c) port implements only the Allocator OUT contract for AI Stack (Total Revenue = 0, no IRR engine), defers the three-sub-module build. Recommendation: **(a)** for v1 reconciliation cleanliness; the code architecture must be ready for the three-sub-module layout (Compute / Application / Orchestration) so (b) can be added without restructuring.

**10.4 Customer Launch IRR — accept Block C sanity failure, or block on Vlad-locked fix?** Per §9.3 above and Customer_Launch_IRR_Fix_Plan.md. The code implements the per-booster annual IRR pattern (mirroring Starlink) from day one. Even the post-fix sanity number is ~1,700%, which fails any reasonable Block C threshold. Recommendation: **accept** F9 IRR Block C failure as a known disposition (documented in the PRD), proceed with reconciliation, surface in the divergence report; expected resolution path is a Sprint 11.5-or-later Vlad-locked input revision to the per-launch cost basis or per-launch market price (or a fundamental IRR engine reformulation — e.g., loading expected fleet build cost over the booster's economic life). Block on Vlad only if the IRR signal materially distorts the cash queue's allocation decisions (which it does — CL R42 / R99 IRR signals drive queue priority).

**10.5 Bridge loan repayment and interest expense.** Per context.md Open Item #3 and Architecture §20.9 closing paragraph. V2.16 has $20B bridge loan inflow in 2025 with no repayment or interest expense modeled. Two options: (a) v1 carries the same stub (matches V2.16; flag as known limitation in the PRD); (b) v1 implements a stub repayment schedule (e.g., paid back from 2027 IPO proceeds) and an interest expense line in OpEx. Recommendation: **(a)** for V2.16 reconciliation alignment; introduce (b) in a clearly-tagged "v1.1" scope after Vlad provides assumptions for the repayment schedule and rate.

**10.6 ODC unit economics — model verdict accepted, OR revise per-sat revenue / per-sat cost inputs?** Per Architecture §20.8. V2.16 accepts the negative-IRR-throughout-horizon outcome as model verdict; ODC stays at zero deployment. The code mirrors this by construction (negative-IRR cutoff in the Allocator). Recommendation: **accept model verdict** for v1; document that ODC deployment is expected to be zero throughout horizon under the V2.16 input set; expose ODC per-sat revenue and per-sat cost as MC inputs so scenario runs can stress-test what input revisions would produce positive IRR. This is the institutionally correct treatment — let the model speak.

**10.7 Mars per-mission IRR engine — implement, or defer to "v1.1"?** Per context.md Open Item #4. Vlad explicitly deferred ("we can change this later"). Recommendation: **defer**. v1 implements Lunar Mars as the strategic carve-out with BV engine + no IRR; expose a `module.per_mission_irr_engine` hook so the engine can be plugged in when Vlad locks the methodology.

**10.8 Web UI v1 scope.** Per context.md §5.4 and §14.5. Scope locked in context.md (scenario picker + Group + per-module EV + FCF tables + tornado + audit lineage panel; charts/comparables/animations deferred to v2). No additional Vlad sign-off needed unless the user wants to revise.

**10.9 Repository layout.** context.md §5.3 specifies a layout. Recommendation: **adopt as-is**. The layout mirrors the constitutional documents' module decomposition and the Sprint Roadmap's dependency graph, and it accommodates the v1 / v2 scope split cleanly.

---

## 11. Phase 1 verification

Confirming Phase 1 was conducted as scoped:

| Phase 1 task | Status | Evidence |
|---|---|---|
| Read role.md | ✓ | Dr. Marcus Hale persona internalized; numerical equivalence sacred; traceability non-negotiable |
| Read context.md in full | ✓ | 1,005 lines; §15 reading order followed |
| Read 06_Memory_Snapshot critical locks | ✓ | 23 locks across architectural / Excel-side / process meta-lessons |
| Read 00_README_Sprint_Kickoff | ✓ | Standing process rules digested |
| Read 01_Lessons_Learned (23 Principles) | ✓ | All 23 principles tied to V30.5 incidents |
| Read 02_Architecture_and_Methodology in full | ✓ | All 20 sections + §20 Sprint 11 amendments block |
| Read Model Execution Rules (23 rules, A-G groups) | ✓ | Rules 12, 14, 21, 22, 23 carry directly into code |
| Read Sprint Roadmap & Verification (Parts A + B + §10) | ✓ | Particularly §6.8 revised calibration targets and §10 sprint sizing |
| Read STATUS_2026_05_26 | ✓ | Sprint 11 collapse / 11e shipped / 11f pending |
| Read Sprint_11f_Spec deeply | ✓ | Option A architecture digested; code implements from day one |
| Read Sprint_11e_Spec (V2.16 baseline) | ✓ | LM BV correction + Launch Capacity wiring + CL R210 + bridge loan |
| Read Sprint_11_Spec (original combined) | ✓ | Vehicle-level allocator + deployment binding intent (deferred to 11f) |
| Read Customer_Launch_IRR_Fix_Plan | ✓ | Three compounding bugs; per-booster annual IRR pattern is the target |
| Read 2025 Anchors from Q4'25 | ✓ | Q4'25 raw anchors / V30.5 corrections / structural ODC change |
| Read 04_Assumptions_Tab_Spec | ✓ | 36-column convention; 11 sections; ~212 inputs |
| Read Colleague A Brief (AI Stack) | ✓ | Sprint 6 deferred, eight Q1-Q8 open |
| Read Colleague B Brief (Sprint 11f) | ✓ | Option A architectural rework scoped |
| Read AI Stack Module Architecture Scoping | ✓ | Three sub-modules (Compute / Application / Orchestration); Terafab toggle; Business Model Switch |
| Skim Sprint History 1-10.7 for arc | ✓ | Sprint 0 → 11e arc mapped; key patches (3.5, 8.5, 10.5, 10.8) identified |
| Structural probe V2.16 | ✓ | 15 sheets exactly match context.md §2.2; iterative calc ON; VBA present but non-load-bearing; zero defined names |
| Write phase1_research_synthesis.md | ✓ | This document |

**Phase 1 deliverable check.** This synthesis (a) confirms my digestion of the constitutional layer + active state; (b) surfaces the major calibration target conflict (§3 / §10.1) that needs Vlad sign-off; (c) maps module-by-module the v1 implementation considerations and known open threads (§4); (d) verifies V2.16's actual structure matches the constitutional claims (§7); (e) enumerates nine open questions requiring Vlad sign-off before Phase 3 PRD finalizes (§10).

I am ready for Phase 2 on your green light. Phase 2 will explain the proposed build approach — module sequencing, dependency ordering, reconciliation milestones, risk surfaces, test strategy, and sign-off gates. Phase 3 (PRD) then converts the build approach into a detailed development specification.

---

## 12. Source documents cited (Sources)

- `role.md` — Dr. Marcus Hale operating persona.
- `context.md` — living context document, 1,005 lines, dated 2026-05-28.
- `Pre Existing Model Package/INITIATION_README.md`
- `Pre Existing Model Package/00_Constitutional_Docs/00_README_Sprint_Kickoff.md`
- `Pre Existing Model Package/00_Constitutional_Docs/01_Lessons_Learned.md` (23 Principles).
- `Pre Existing Model Package/00_Constitutional_Docs/02_Architecture_and_Methodology.md` (1,102 lines; §1–§20 + amendments).
- `Pre Existing Model Package/00_Constitutional_Docs/03_Sprint_Roadmap_and_Verification.md` (Parts A + B + §6.8 revised + §10 sprint sizing).
- `Pre Existing Model Package/00_Constitutional_Docs/Model Execution Rules.md` (23 rules, A–G groups).
- `Pre Existing Model Package/06_Memory_Snapshot/MEMORY_SNAPSHOT_CRITICAL_LOCKS.md`
- `Pre Existing Model Package/06_Memory_Snapshot/SPRINT_CHAT_WORKFLOW.md`
- `Pre Existing Model Package/01_Current_State/STATUS_2026_05_26.md`
- `Pre Existing Model Package/01_Current_State/Sprint_11f_Spec.md`
- `Pre Existing Model Package/01_Current_State/Sprint_11e_Spec.md`
- `Pre Existing Model Package/01_Current_State/Sprint_11_Spec.md`
- `Pre Existing Model Package/01_Current_State/Customer_Launch_IRR_Fix_Plan.md`
- `Pre Existing Model Package/01_Current_State/SpaceX Model V2.16.xlsx` (structural probe only — not value-pass consumed).
- `Pre Existing Model Package/02_Fresh_Restart_Inputs/2025 Anchors from Q4_25.md`
- `Pre Existing Model Package/02_Fresh_Restart_Inputs/04_Assumptions_Tab_Spec.md`
- `Pre Existing Model Package/03_Sprint_History/Sprint_1_Spec.md` through `Sprint_10.7_Spec.md` (16 files, skimmed for arc).
- `Pre Existing Model Package/04_Module_Briefs/Colleague_A_Brief_AI_Stack.md`
- `Pre Existing Model Package/04_Module_Briefs/Colleague_B_Brief_Deployment_Binding.md`
- `Pre Existing Model Package/05_Reference_Material/AI_Stack_Module_Architecture_Scoping.md`

**END OF PHASE 1 SYNTHESIS.**
