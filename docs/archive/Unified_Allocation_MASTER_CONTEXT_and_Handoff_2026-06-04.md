# Unified Cash + Launch Allocation — MASTER CONTEXT & HANDOFF

**Purpose:** single reference for the unified-allocation workstream. A fresh chat should read this to get fully attuned without re-running the investigation. It consolidates the verified V4.109 as-is map, the corrections to the original audit, the locked architecture, every resolved decision, the conceptual reasoning (so nothing gets relitigated), the post-U0 state, the supersession list, and exactly what each remaining sprint must do.

**Authoritative on conflict:** the project constitution (`Starter_Package_2026_05_28/01_Constitutional/*`) and `mach33-model-build` / `mach33-irr-canonical` skills supersede this doc on any process question. This doc supersedes the original audit where noted (§3 corrections).

**Companion docs (read order for a new chat):**
1. This doc (orientation + decisions + as-is + what's next).
2. `Unified_Allocation_Scoped_Architecture_and_Sprint_Schedule_2026-06-04.md` (the U0–U4 plan + gates).
3. `Sprint_U0_Demand_Spine_Unification_Spec.md` (the executed/landing prerequisite).
4. `Stage1_Unified_Cash_Launch_Allocation_Architecture_2026-06-04.md` (the full analysis, risk register, impact map).
5. `Cash_vs_Capacity_Allocation_Audit_V4.109_2026-06-04.md` (the motivating audit — but apply §3 corrections below).

**Cardinal rule for the next chat:** module OUT-block and engine rows **shift between builds**. Re-resolve every label against the *live* open workbook before trusting any row number here. INDEX/MATCH is banned for new/edited cells — resolve labels to direct addresses once, write the direct ref.

---

## 1. The problem we are fixing (one sentence)

The model runs **two separate allocators on two different principles over two slices of capital against three inconsistent demand signals, never reconciled** — cash by IRR-softmax + 5% floor + demand-buildable caps + water-fill; launch-kg pro-rata Starlink-vs-AI with Customer Launch residual — so cash can fund a module the capacity gate starves (and vice-versa), the caps mismeasure deployment by ~2.5×, and a lumpy demand signal over-sizes everything.

---

## 2. The locked architecture (the WHAT)

### 2.1 Three CapEx buckets — classify every dollar once
| Bucket | Examples | Funding | In the per-unit IRR? |
|---|---|---|---|
| **1. Growth** | new Starlink/ODC sats, new Terr MW, marginal Starship/F9 launches | **IRR-ranked allocation** (prior-yr IRR + 5% floor) from the cash pool | **Yes** (per-unit marginal CapEx) |
| **2. Enabling infrastructure** | **Terafab** chip fab, **Gigabay** ship factory, ground/optical stations, launch-site infra | **Senior claim + project-finance debt**, sized to forward exogenous demand; books no FCF; transfers output **at-cost** | **No** — only the at-cost unit price (chip $/sat, launch $/kg) enters module COGS |
| **3. Maintenance/refresh** | replacement sats, refurb, sustaining capex | **Predetermined senior claim** in the queue gate | No |

This single idea fixes audit F1 (cap-vs-deploy mismeasure) *and* keeps lumpy Terafab out of the IRR.

### 2.2 The unified engine (target logic)
- **One cash pool** through the existing queue gate, then senior claims off the top: corporate claims → **maintenance capex (NEW)** → **enabling-infra equity (NEW; debt covers the lump, incl. Terafab)** → LM carve-out → **ODC strategic seed (NEW)** → remaining pool for growth.
- **Priority** = 2-yr-avg prior-year marginal IRR, with the **5% soft floor kept**, across **four first-class programs {Starlink, ODC, Terrestrial, Customer Launch}** (retire the AI roll-up IRR + the Level-2 ODC/Terr softmax — ODC & Terr go first-class).
- **Two resources:** the cash pool + **Gigabay build throughput (ships/yr)** (the real shared launch bottleneck; Terrestrial is cash-only).
- **Same-year build:** vehicles built this year, sized to **exogenous** demand, capped by the Gigabay rate, ranked by **prior-year** IRR.
- **Reconcile** (deterministic finite cascade, NO iteration): `units_i = MIN(cash-funded, slot-funded, demand)`; release the slack resource on bound programs; ONE re-cascade; park residual (leftover cash / idle slots) to next year. Reported share = the **capped** share.

### 2.3 The acyclicity firewall (every new/edited cell)
- **May reference:** exogenous demand (a market forecast), prior-year IRR, prior cost/volume (Wright's), a chosen ramp/leverage policy, the predetermined cash pool / BoY fleet.
- **May NOT reference:** this-year IRR, this-year realized deployment, this-year returns.
- The **only** legitimate within-year cycle is the existing queue gate (pool↔taxes↔EBIT), handled by **iteration ON**. Add no second cycle. The within-year two-pool reconciliation must be a strict feed-forward cascade, never iterated.
- **Proof obligation each sprint:** precedent scan (no new cell touches a realized/this-year-IRR cell) + iteration-OFF circular-cell diff = 0 new cells + 5× round-trip stability + edge-year conservation.

---

## 3. Decisions — RESOLVED with Vlad (2026-06-04)

| # | Decision | Resolution |
|---|---|---|
| D1 | Priority weight | **Keep the 5% soft floor** (`share = floor + (1−N·floor)·w`). NOT the hurdle. Optional later: asymmetric floor (protect growing programs, drop once IRR<0 with falling deployment) — Vlad's call, not base scope. |
| D2 | What the allocator gates | **Growth slice only**, via the three-bucket taxonomy (§2.1). |
| D3 | Smoothing | **2-yr prior-IRR average**; α as MC. |
| D4 | Strategic seed | **Pre-revenue ODC only**, off both pools, graduates on lagged IRR. |
| D5 | Debt / facilities | **Keep Terafab as genuine project-finance debt, OUT of the IRR**, repaid from at-cost chip transfer over fab life. Re-scope the ODC bypass into the spine. Repair Conservation R14. |
| D6 | LM kg bound | **Yes** — MC-bounded share cap; fleet target includes LM demand. |
| D7 | Forward-demand buffer | **1.25×** base, MC. |
| D8 | Launch-vehicle capital | **Same-year build, sized to exogenous module demand, ranked by prior-year IRR. Keep module-owned launch CapEx.** Second pool = Gigabay throughput (ships/yr). |

### 3.1 Conceptual resolutions (do not relitigate)
- **"High CapEx now → growth later" without circularity:** forward intent enters as a *lagged signal* or an *exogenous commitment*, never as a model-computed forward return. Three tools by module maturity: **(a) prior-year IRR + learning curve** (the growth engine — deploy → cum volume↑ → Wright's cost↓ → next-yr prior IRR↑; compounds across years via the cash spine, never within a year); **(b) strategic seed** for pre-revenue modules (exogenous ramp off the top, graduates on lagged IRR — same machinery as the LM carve-out, which is already live and IRR-responsive); **(c) debt/leverage** for profitable-but-cash-short modules (external capital, repaid from own FCF — doesn't starve others).
- **Lumpy Terafab nervousness — resolved:** Terafab is *enabling infrastructure*, not a marginal growth unit. Do **not** wrap its lumpy CapEx in a per-unit IRR (dividing a $70B lump by a build-year's tiny chip output crushes IRR → chicken-and-egg). Fund it senior + project debt, transfer chips at-cost; only the at-cost chip $/sat enters ODC/Terr COGS. The at-cost price must be struck on a **predetermined basis** — amortized fab cost over **design capacity / planned lifetime output** (or Wright's on prior cumulative chips) — **never** fab cost ÷ this-year realized volume (crushes early-life IRR AND closes a loop).
- **Debt is the right tool, not a workaround** — for a lumpy long-lived asset with clear multi-year demand (Terafab) or a profitable-but-constrained module. The current facilities' bug is sizing as "allocator shortfall" + the ODC one bypassing the pool, not that debt exists.
- **Same-year build is deliverable** iff sized to exogenous demand and ranked by prior-year IRR (never realized units / this-year IRR).

---

## 4. The verified as-is cell map (V4.109) — load-bearing

Calc: **iteration ON** (`iterate=1`, 1000 / 1e-7). Year header row 4: **D=2025, E=2026, I=2030, N=2035, S=2040** (horizon to AC=2050 unless truncated — re-confirm last column on the live book). All cells below verified directly against the uploaded V4.109.

### 4.1 Cash path (`Cash Allocation Engine` = CAE)
```
R8 Cash BoY (=prior R56) + R9 IPO + R10 bridge + R105 Terafab draw → R11 Cash available
 → queue gate R15 SG&A / R16 shared R&D / R17 corp capex / R18 spectrum / R19 taxes (total R20)
 → R21 Pool after gate = MAX(0,R11−R20)
 → R24 Lunar/Mars carve-out  [SENIOR, off the top]
 → R25 Remaining pool = MAX(0,R21−R24)   (gated to blank/0 in 2025 anchor)
 → top-level softmax: R28/29/30 prior-yr IRR → R31/32/33 exp(β·IRR), β=Assumptions!B17=3, NO hurdle
     → R35/36/37 shares = B473(0.05) + (1−3·B473)·exp_i/Σ   [SOFT FLOOR]
 → caps R64 (SL hdrm×slug) / R65 (CL ModuleCapEx) / R66 (AI demand-buildable = R202+R203)  [NEW-BUILD slice — F1]
 → WATER-FILL R112–R129: desired=share·R25 → capped=MIN(desired,cap) → residual R119 → spill weight R123-125=IF(headroom>0,exp,0) → final R127/128/129   [SINGLE PASS]
 → allocated cash R39=R127 (SL), R40=R128 (CL), R41=R88+R90 (AI)
 → AI LEVEL-2 R76–R94: IRR R77/78 → shares R82/83 → desired R85/86 → allocated R88/90 (capped ODC/Terr buildable)
```

### 4.2 Carve-out IRR-response (CORRECTION — see §3 audit fix; this is LIVE)
`R24 = IF(year<B115[=2030], B15[$700M R&D override], MAX(B13[$1bn floor], R98 × IF(B14[=1]=1, H55[prior-yr Group FCF], 0)))`
where `R98 = B12[15%] + R97·(B409−B12)`, `R97 = ramp` from `R96 = AVERAGE(R28,R29,R30)` prior-yr IRRs. Fully **acyclic** (prior-yr FCF + prior-yr IRR). This IS the "strategic seed expresses commitment, IRR-responsive" machinery — reuse it for the ODC seed.

### 4.3 Capacity path (CAE, separate block — different principle)
```
R47 LM kg reserved off-top (=Lunar-Mars!R114)   [SENIOR]
R48 Capacity after LM = MIN(ceiling B488, MAX(0, VB!R68 − R47))      (VB!R68 = BoY fleet stock kg)
R49 binding flag = IF(R46>R48)   ← reads R46 (realistic), the WRONG total [F4] — U0 repoints to R102
R99 Desired kg Starlink = saturation-headroom sats × mass [INFLATED 431.7M@2030] — U0 de-inflates
R100 Desired kg CL = (commercial+gov demand)×readiness×payload [realistic, exogenous]
R101 Desired kg AI = sats-added-target × dry mass [realistic]
R102 = R99+R100+R101 [527M@2030 inflated] ; R104(VB) reads R102 → fleet sizing
Allotment R50 = R99·MIN(1,R48/(R99+R101)) ; R52 symmetric (AI) ; R51 = residual (CL)  [PRO-RATA SL-vs-AI]
```

### 4.4 Vehicle Build (capacity governor — already forward-demand-pulled, acyclic)
```
R104 Total desired upmass ← CAE!R102   (currently the INFLATED total — U0 fixes via R102)
R106 Desired launches = MAX(0,(R104 − F9 cap R105)/payload R44)
R54/R83 boosters/ships needed = R106/cadence ; R55/R84 BUILT = MIN(need−BoY+retired, Gigabay R107)
R107 Gigabay ← Facilities Build "Installed Starship build capacity (ships/yr): rate-limited ramp" (FB-1)
R56/R85 fleet BoY = prior EoY → R68 capacity   [ACYCLIC via build-to-operate lag]
Module-owned launch CapEx (Sprint 4.5): VB books no FCF (R77=0); launch cost sits in each module's CapEx.
R67 "Total launch kg demand N+1 (fleet)" = ORPHAN (0 consumers) — U0 retires it.
```

### 4.5 Debt facilities
- **Terafab** R103–111: draw `R105` → pool at `R11`. Genuine revolver (S-1 $20bn analogue). **KEEP** (re-scope as project finance, out of IRR — D5).
- **ODC** R131–140: draw `R134` **bypasses pool** → `AI!R30 = CAE!R88 + CAE!R134` (so it can't leak to SL/CL). In 2030 the draw (~$29B) is ~3× the pool allocation. **Distributional patch — fold into the spine (D5).**
- Both sized as `need − pool`; interest on prior-yr balance ~4.58%; FCF-sweep repay; conservation rows R111/R140 = 0.

### 4.6 Module deployment gates (the interface)
- Starlink: cash `R19`←CAE R39; capacity ceiling `R162`←CAE R50. Deploys `MIN(cash/slug, capacity/mass, demand)`.
- Customer Launch: `R47`←CAE R51 (capacity residual). Cash cap R65 = its own Module CapEx.
- ODC (AI): `R45 = ROUNDDOWN(MIN(target R32, cash R42←R30, capacity R52/mass))`; `R30 = CAE!R88 + CAE!R134`.
- AI roll-up Module CapEx `R161 = R74 + R107 + R135 + Facilities!R63(Terafab) + R212` — **note Facilities!R63 (the fab) is in the deploy base but NOT in cap R66** (a big F1 driver and the U1 hook).
- Terrestrial: cash-only (no launch mass).

### 4.7 Conservation (guardrail) — BROKEN (F2)
`Conservation!R14 = ABS(CAE R56 − R11 − R55 + R106 + R107) <1` includes Terafab interest/repay but **omits the ODC facility flows** (`R134/135/136`) that the spine R56 carries → R14 FAILs every year the ODC facility is live (≈2028–2036). Repair in U4: `… − R134 + R135 + R136`. (Also: R8 revenue-tie shows benign "n/a" at the horizon edge.)

### 4.8 Direct consumers of CAE (repoint/verify on any rescope)
`Starlink!R19, R162` · `Customer Launch!R47` · `AI - Compute!R30, R45, R186` · `Lunar - Mars!R30` · `Vehicle Build!R104` · `Group P&L!R43/R47` (read queue-gate R16/R15 — unaffected unless the gate changes) · `Conservation!R8/R12/R14/R18`. Group P&L / SoTP / Launch Dashboard aggregate module lines **by label** → values change, refs don't.

---

## 5. Three corrections to the original V4.109 audit (re-resolved on the open book)
1. **The IRR-responsive carve-out DID land** — `R95–R98` live, `R24` consumes `R98` (§4.2). The audit described R24 as a flat carve-out. Matters: the seed-as-commitment machinery already exists and is acyclic.
2. **The fleet builds off the *inflated* demand** — `VB!R106` ← `R104` ← `CAE!R102` (527M), while the realistic `VB!R67` (153M) has **no consumers** (orphan). So the demand inflation reaches fleet sizing, not just rationing.
3. **Dead-in-place residue:** `CAE!R67–R72` (rank keys / higher-rank-caps) are **empty**; `R74` ("Placeholder AI/strategic CapEx: TEMP") is stale now that AI-Compute is loaded.

---

## 6. What landed vs didn't (so the next chat doesn't re-tread)
- **Cash allocator evolution:** softmax β10 (S8) → β5 (8.3) → **β3 live**. Hard **5% IRR hurdle = NEVER landed** (killed AI seed years; B470 repurposed). **5% soft floor = LANDED** (B473). **Absorptive water-fill = LANDED** (R112–129). Leftover→Starship **sweep = REMOVED** in 8.11.
- **Launch allocator:** **IRR-priority rationing = NEVER landed** (still pro-rata R50/51/52). Value-gate/elasticity patch = latest authored design, not confirmed live.
- **Vehicle Build:** the 35× under-supply (realized-pull) bug was fixed by re-pointing R106/R77 to **forward demand** (VB1); payload ramp 100→200t (VB2/2.1); Gigabay rate-limited ramp (FB-1) is the live build cap.
- **Seed precedent (LM):** cash `MAX($1bn, IRR-resp% × prior FCF)` off the top (R24) + kg reserve off the top (R47, ~32% of capacity by 2040 — needs a bound). Already acyclic.

---

## 7. Supersession list (retire AFTER replacements prove out — track only, no deletions yet)
- **Already dead/empty:** `CAE!R67–R72`, `R74`, `VB!R67` (retired in U0).
- **Newly unconsumed after U0:** `CAE!R46` (was only read by R49) → flag for U4.
- **Superseded by the unified spine (U2–U4):** pro-rata kg gate `R50/51/52`; AI roll-up IRR `R30` + Level-2 `R76–R94`; binding flag `R49` (re-pointed in U0, may retire); cash water-fill `R112–R129` (logic reused, re-pointed); Level-2 memo `R93`.
- **Re-scoped, not deleted:** Terafab `R103–111` (→ project debt, out of IRR); ODC facility `R131–140` (→ folded into spine); LM carve-out + kg reserve (kept, bounded).
- **Repair not retire:** `Conservation!R14`.

---

## 8. Sprint schedule (status + gates)

| Sprint | Status | Scope | Gate |
|---|---|---|---|
| **U0 — Demand-spine unification** | **SPEC AUTHORED → executing/landing** | De-inflate `R99`→`Starlink!R159` (2026+); `R49`→`R102`; retire `VB!R67`. | 2030 desired 527M→166M; Starlink ≥90% of real demand; binding flag honest; 2025 frozen; conservation OK; acyclic. |
| **U1 — Three-bucket split + cap-base** | NEXT (own chat, post-U0) | Route enabling infra (`Facilities!R63` etc.) **out** of `AI!R161`/IRR; install **at-cost chip transfer** (design-capacity absorption) into ODC/Terr COGS; add **maintenance senior claim** to queue gate; align growth caps `R64/65/66`; **check Terafab double-count** (R63 in R161 *and* maybe in `AI!R38/39`). | allocated_growth ≈ deployed_growth; ODC/Terr IRR not crushed by the fab; leftover reconciles; edge years; conservation OK. |
| **U2 — Unified two-resource allocator** | own chat, post-U1 | One 2-yr-avg prior-IRR weight + 5% floor across {Starlink, ODC, Terr, CL}; retire AI roll-up IRR + Level-2; two-pool fill (cash + Gigabay throughput) + cross-resource MIN + bounded cascade; same-year build (exogenous-sized, Gigabay-capped, prior-IRR-ranked). | acyclicity diff = 0; Σalloc ≤ pool, Σslots ≤ throughput; capped shares sane (CL never 80%); 5× stable. |
| **U3 — Seed + debt re-scope** | own chat, post-U2 | ODC pre-revenue seed off both pools (graduates on lagged IRR); Terafab → project debt (out of IRR, repaid from at-cost chip transfer); fold ODC bypass into the spine. | seed deploys + sunsets on graduation; Terafab cash-neutral over life; ODC no longer pool-bypassed; conservation OK. |
| **U4 — Guardrail repair + supersession sweep** | own chat, post-U3 | Repair/extend Conservation R14 (+ facility/enabling flows); add new identities (Σalloc≤pool; Σslots≤throughput; deploy=seed+queue; both leftovers parked; at-cost transfer conservation); clear dead residue (§7). | R14 OK every year; all conservation green; supersession cleared; 5× stable + calibration ±5%. |

**Cadence:** each spec authored against the live book *after* the prior lands; each executed in its own plugin chat; Vlad saves. Author U1 only once U0 has executed and the row map is re-resolved.

---

## 9. Post-U0 state (what U1 inherits, once U0 lands)
- `CAE!R99` (2026→horizon) = `=IFERROR(Starlink!E159,0)` — realistic Starlink launch-kg. 2025 (D99) unchanged.
- `CAE!R102` realistic (2030 ≈166M, was 527M); `VB!R104/R106` and the fleet build re-sized down accordingly; ODC capacity allotment `R52` up ~3.5× (2030 ≈73M); Starlink still ~98% of real demand.
- `CAE!R49` = `IF(R102>R48)` — honest binding flag (2030=1, 2035=0, 2040=1).
- `Vehicle Build!R67` retired (cleared + memo-relabelled); `CAE!R46` now unconsumed.
- Everything else structurally unchanged. **Re-read R99/R102/R49/R50/R52/VB!R104/R106 values on the live book before authoring U1.**

---

## 10. New MC inputs to register (Rule 18, at creation)
soft floor 5% (0–8%, tri) · IRR-avg window 2yr (1–3, disc) · ODC seed ramp (units/yr, tri) · seed graduation IRR (=floor-implied ±4%, tri) · forward-demand buffer 1.25× (1.0–1.75, tri) · LM kg cap 18% of capacity (10–30%, tri) · chip-transfer absorption basis = design-capacity (structural) · Terafab leverage/draw cap (structural).

---

## 11. Open verification items (carry forward)
- Confirm `Starlink!R159` precedents are exogenous (Demand Curves / row 167 × mass) — no capacity/allocation/this-yr-IRR (U0 §4.4).
- Confirm the live horizon's last year column (2040 vs 2050) before copying ramps.
- U1: confirm whether `Facilities!R63` (Terafab) is double-counted (in `AI!R161` deploy base AND inside per-sat chip COGS `AI!R38/39`).
- U1: confirm `Lunar_Mars_Fix_Spec_Round2 §G` (LM in the fleet build target `VB!R104`) status — if LM kg is reserved off a fleet sized only for the other three, it crowds them out without growing the fleet.
- Confirm `Conservation!R14` is the only broken guardrail (F2) and scope its repair to U4.
```
