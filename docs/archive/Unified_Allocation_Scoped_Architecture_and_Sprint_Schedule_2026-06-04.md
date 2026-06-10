# Unified Cash + Launch Allocation — Scoped Architecture & Sprint Schedule

**Status:** Stage 2 scoping. Architecture locked with Vlad (2026-06-04). Decision-independent prerequisite (U0) ready to author; U1–U4 sequenced. No cells changed by this doc.
**Companion:** `Stage1_Unified_Cash_Launch_Allocation_Architecture_2026-06-04.md` (the analysis this builds on).
**Discipline:** `mach33-model-build`, `mach33-irr-canonical`, project constitution. Iteration stays ON. Direct cell refs only (INDEX/MATCH banned). 2025 anchor frozen.

---

## 1. Locked decisions

| # | Decision | Resolution |
|---|---|---|
| D1 | Priority weight | **Keep the 5% soft floor** (`share = floor + (1−N·floor)·w_i`). Optional later refinement: make the floor *asymmetric* (protects pre-graduation/growing programs, drops once IRR<0 with falling deployment) to avoid funding declining negative-IRR Starlink — Vlad's call, not in base scope. |
| D2 | What the allocator gates | **Growth slice only**, generalised to the **three-bucket CapEx taxonomy** (§2). |
| D3 | Smoothing | **2-year prior-IRR average** for priority; α as MC. |
| D4 | Strategic seed | **Pre-revenue ODC only**, off both pools, graduates on lagged IRR. |
| D5 | Debt / facilities | **Keep Terafab as genuine project-finance debt, OUT of the IRR**, repaid from at-cost chip transfer over the fab life. Re-scope the ODC bypass facility into the unified spine (ODC funded by seed + allocation, no pool bypass). Repair Conservation R14. |
| D6 | LM kg bound | **Yes** — MC-bounded share cap; fleet build target includes LM demand. |
| D7 | Forward-demand buffer | **1.25×** base, MC. |
| D8 | Launch-vehicle capital | **Same-year build, sized to exogenous module demand, ranked by prior-year IRR.** Keep module-owned launch CapEx. Second resource pool = **Gigabay build throughput (ships/yr)**, not abstract kg. |

---

## 2. The organizing principle — three CapEx buckets

Every dollar of CapEx is classified once, and that classification decides how it's funded and whether it touches the IRR:

| Bucket | Examples | Funding | In the per-unit IRR? |
|---|---|---|---|
| **1. Growth** | new Starlink sats, new ODC sats, new Terr MW, marginal Starship/F9 launches | **IRR-ranked allocation** (prior-year IRR + 5% floor) from the cash pool | **Yes** — per-unit marginal CapEx is the IRR's `−CapEx` leg |
| **2. Enabling infrastructure** | **Terafab** chip fab, **Gigabay** ship factory, ground stations / optical ground, launch-site infra | **Senior claim + project-finance debt**, sized to *forward exogenous demand*; books **no FCF**; transfers output (chips, launches) **at-cost** | **No** — only the *at-cost unit price* (chip $/sat, launch $/kg) enters module COGS/IRR; the lumpy build never does |
| **3. Maintenance / refresh** | replacement sats, fleet refurb, sustaining capex | **Predetermined senior claim** in the queue gate (like corporate CapEx) | No — not discretionary growth |

**Why this is the spine of the fix:** it resolves audit F1 (caps vs deploy mismeasure) *and* Vlad's lumpy-Terafab nervousness in one stroke. The per-unit IRR only ever sees smooth, per-unit numbers; lumpy capacity-ahead-of-demand assets are funded like the launch fleet and recovered through at-cost transfer pricing.

**Acyclicity rule for at-cost transfer prices (bucket 2):** struck on a *predetermined* basis — amortised build cost over **design capacity / planned lifetime output**, or a Wright's-law unit cost on **prior cumulative** volume. **Never** build-cost ÷ this-year realised volume (that crushes early-life IRR on an idle asset *and* closes a within-year loop).

---

## 3. The unified engine — target logic

```
ONE cash pool, computed as today through the queue gate, then senior claims off the top:
   Pool after gate R21
     − corporate claims (existing)
     − MAINTENANCE capex (NEW senior claim, bucket 3)
     − ENABLING-INFRA equity portion (bucket 2; debt covers the rest, incl. Terafab)
     − LM carve-out R24 (keep; IRR-responsive, prior-yr FCF — already acyclic)
     − ODC strategic seed (NEW; pre-revenue ramp, off both pools)
   = Remaining pool for IRR-weighted GROWTH allocation

PRIORITY (order only, never quantity):
   w_i from 2-yr-avg PRIOR-year marginal IRR, across {Starlink, ODC, Terrestrial, Customer Launch}
   share_i = floor + (1 − N·floor)·(w_i / Σw)          [5% floor kept]
   (retire the AI roll-up IRR and the Level-2 ODC/Terr softmax — ODC & Terr go first-class)

TWO RESOURCES:
   cash pool  (above)
   Gigabay build throughput (ships/yr)  — the real shared launch bottleneck; Terr is cash-only
   Same-year build: vehicles built this year, sized to EXOGENOUS demand, capped by Gigabay rate, ranked by prior-yr IRR

RECONCILE (deterministic finite cascade — NO iteration):
   cash_funded_i  = fill(cash pool, by w_i, capped at growth-demand_i × unit cost)
   slot_funded_i  = fill(Gigabay throughput, by w_i, capped at demand_i × ships-per-unit)
   units_i = MIN(cash_funded_i, slot_funded_i, demand_i)
   release the slack resource on bound programs → ONE re-cascade → park residual (cash leftover / idle slots), both carry to next year
   reported share = the CAPPED share

ACYCLICITY FIREWALL (every new cell):
   may reference: exogenous demand, prior-year IRR, prior cost/volume, chosen ramp/leverage policy, predetermined cash pool / BoY fleet
   may NOT reference: this-year IRR, this-year realised deployment, this-year returns
   the ONLY within-year loop is the existing queue gate (iteration ON); add no second one
```

**Growth engine (how short-run CapEx → long-run growth, acyclically):** deploy → cumulative volume↑ → Wright's cost↓ (prior cumulative) → next-year prior-year IRR↑ → next-year share↑. Compounds across years via the cash spine; never forecast within a year. Seed (bucket-2-funded ODC ramp) and project debt (Terafab) bootstrap programs to the point the lagged loop ignites.

---

## 4. Sprint schedule (dependency-ordered)

> Author U0 now (this chat). Author U1–U4 each against the **live book after the prior sprint executes** (direct-ref specs go stale on row shifts). Each spec executes in its own plugin chat; Vlad saves.

### U0 — Demand-spine unification  *(hard prerequisite; decision-independent)*
- **Scope:** one realistic annual *exogenous* deployable-demand number per program. De-inflate Starlink desired-kg `CAE!R99` (today = saturation-headroom × mass = 431.7M kg) to the realistic annual basis already used by `R46` (`Starlink!R159`). Make `R102 ≡ R46`; point `VB!R104` and the binding flag `R49` at the same total. Retire orphaned `VB!R67`.
- **Touch points:** `CAE!R99/R100/R101/R102/R46/R49`; `VB!R104/R67`; verify nothing else reads R67.
- **Gate:** 2030 Starlink desired-kg ≈ realistic annual (not 431.7M); fleet sizing, rationing and the binding flag read one number; 2025 unchanged; conservation OK; 5× stable.

### U1 — Three-bucket CapEx split + cap-base reconciliation
- **Scope:** route **enabling infra out of the per-unit IRR/deploy base** — pull `Facilities!R63` (Terafab) and kin out of `AI!R161`; install **at-cost chip transfer** into ODC/Terr COGS on a predetermined absorption basis (§2). Add the **maintenance senior claim** to the queue gate. Align growth caps `R64/65/66` to the growth slice so `allocated_growth ≈ deployed_growth`. **Verify/clear the Terafab double-count** (fab in `R161` *and* possibly in per-sat chip COGS `AI!R38/39`).
- **Gate:** allocated_growth ≈ deployed_growth (≤ small park); ODC/Terr IRR no longer crushed by lumpy fab; "leftover" reconciles; edge years 2025/30/35/40; conservation OK.

### U2 — Unified two-resource allocator
- **Scope:** one 2-yr-avg prior-IRR weight + 5% floor across **{Starlink, ODC, Terrestrial, CL}**; retire AI roll-up IRR `R30` + Level-2 `R76–R94`. Two-resource fill (cash + Gigabay throughput) + cross-resource MIN + bounded finite cascade; reported capped share. Convert launch capacity to **same-year build** (exogenous-demand-sized, Gigabay-capped, prior-yr-IRR-ranked) — with the firewall proof obligation called out explicitly.
- **Gate:** acyclicity diff = 0 new circular cells (iteration-OFF); Σalloc ≤ pool, Σslots ≤ throughput; no negative-IRR program funded beyond the (kept) floor; capped shares sane (CL never 80%); 5× stable.

### U3 — Strategic seed + debt re-scope
- **Scope:** ODC pre-revenue seed ramp off both pools, graduates on lagged IRR. Re-scope **Terafab** as genuine project-finance debt (out of IRR, repaid from at-cost chip transfer over fab life). Re-scope the **ODC bypass facility** into the spine (ODC funded by seed + allocation; remove the `AI!R30 += R134` bypass). No double-fund.
- **Gate:** seed deploys the ramp and sunsets on graduation; Terafab debt cash-neutral over life (Σdraw=Σrepay−interest); ODC no longer pool-bypassed; conservation OK.

### U4 — Guardrail repair + supersession sweep
- **Scope:** repair/extend **Conservation R14** for all facility + enabling-infra flows; add the new identities (Σalloc ≤ pool; Σslots ≤ throughput; deploy = seed + queue per program; both leftovers parked; at-cost transfer conservation). Clear confirmed dead residue (§5).
- **Gate:** R14 OK every year; all conservation green; supersession list cleared; full 5× stability + calibration ±5%.

---

## 5. Supersession list (retire in U2–U4, after replacements prove out — track only)
- Dead/empty now: `CAE!R67–R72` (rank residue), `R74` (TEMP placeholder), `VB!R67` (orphan, retired in U0).
- Superseded by the unified spine: pro-rata kg gate `R50/51/52`; AI roll-up IRR `R30` + Level-2 `R76–R94`; binding flag `R49` (wrong total); cash water-fill `R112–R129` (logic reused, re-pointed); Level-2 memo `R93`.
- Re-scoped (not deleted): Terafab facility `R103–111` (→ project debt, out of IRR); ODC facility `R131–140` (→ folded into spine); LM carve-out + kg reserve (kept, bounded).
- Repair not retire: `Conservation!R14`.

---

## 6. New MC inputs (register at creation, Rule 18)

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

---

## 7. Authoring & execution logistics
- **Scope + U0:** this chat.
- **U1:** draftable here; **re-validate row map against the post-U0 book before execution.**
- **U2 / U3 / U4:** one spec-author chat each, authored against the live book *after* the prior sprint executes.
- **Execution:** each spec in its own plugin chat; Vlad pre-names the workbook and saves. Every spec opens with the Rule Compliance Preamble and ends with the universal verification protocol + a Claude Log entry.
```
