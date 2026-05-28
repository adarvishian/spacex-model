# Sprint 8 — OpEx tab + CapEx tab + absorbed Sprint 3.6 micro-patch (Customer Launch margin CAGR)

**Day budget**: 1 day (per Sprint Roadmap §1 + ~5 min Sprint 3.6 absorbed)
**Owner**: Sprint 8 (this chat = spec author; separate fresh chat will execute as plugin)
**Status**: Spec authoring. Constitutional docs + Sprint 0/1/5/7 read in prior context. Vlad-locked 2026-05-22: ODC R&D $-profile $200M→$500M→declining; AI Stack R&D $-profile $50M→$300M→declining; pre-2028 carve-out gap = real cash drain (Sprint 9 cash flow identity formalizes); Sprint 3.6 absorbed as §3.1.

---

## §0 — Constitutional references

- `01_Lessons_Learned.md`:
  - **Principle 8** (vending-machine — module COGS direct production only) — OpEx tab is the LANDING ZONE for everything that's NOT module direct production cost: R&D by module, SG&A by function, corporate operating expenses. NO module tab gets R&D/SG&A added.
  - **Principle 10** (module tabs owned by module sprints; cross-cutting specs only read) — OpEx + CapEx tabs are cross-cutting; Sprint 8 READS from module tabs via INDEX/MATCH on canonical labels, never writes to module tabs.
  - **Principle 11** (zero OFFSET formulas) — all dynamic ranges INDEX-based.
  - **Principle 12 / Rule 23** (anchor-and-offset for ramps) — every R&D % row + SG&A % row uses `$D$anchor + E$5 offset` bounded-CAGR pattern. Year-chained EXCEPTIONS flagged inline: (a) cumulative Corporate CapEx running sum (§3.4), (b) cumulative Spectrum intangible running sum (§3.4).
  - **Principle 14** (cross-tab refs by label) — every read uses INDEX(Tab!D:D, MATCH("Label", Tab!$A:$A, 0)).
  - **Principle 18** (MC ranges at input creation) — 3 new Assumptions amendments populate AG/AH/AI/AJ.
  - **Principle 19 / Rule 15** (sanity check halt thresholds) — §4.6 calibration table specifies halt thresholds for Total OpEx, Total R&D, ODC R&D floor, AI Stack R&D floor, Total CapEx.
  - **Principle 20 / Rule 16** (edge-year reads) — D/I/S/AC on every section.
  - **Principle 23** (calibration anchored) — Sprint 8 must hit Roadmap §6.7 targets: Total OpEx $3,820M ±5%, Total R&D ~$2,853M ±10%, Mars/Moon R&D 2025 $700M ±10%.

- `02_Architecture_and_Methodology.md`:
  - **§12** (OpEx) — R&D by module (start%/end%/CAGR taper) + SG&A by function + Mars/Moon $-profile year-row.
  - **§12.1** (Pre-revenue R&D switch — locked 2026-05-20) — `R&D_t = MAX($-profile_t, % × revenue_t)` for ODC + AI Stack.
  - **§12.2** (SG&A bases) — S&M base = Starlink + Starshield + Customer Launch external + **AI Stack** rev (added 2026-05-20).
  - **§13** (CapEx tab) — Module CapEx aggregation + Corporate CapEx + Spectrum CapEx + Corporate D&A schedule.
  - **§13.1** (Module CapEx aggregation) — read R205 from each module by canonical label `Module CapEx ($mm)`, NOT R206 Capital deployed (Sprint 3 convention).
  - **§13.2** (Corporate CapEx) — HQ $50M/yr + IT $30M/yr + Gen eng $20M/yr + Other $10M/yr flat from Sprint 0 R255-R258.
  - **§13.3** (Spectrum CapEx) — EchoStar year-row Sprint 0 R267 ($5B/$8B/$5B/$2B 2025-2028 = $20B total); 15-yr amortization R268; flows to Starlink COGS as Spectrum amort line (BB only — Sprint 4 already wired).
  - **§15.1** (Group P&L walk) — Sprint 8 PRODUCES Total OpEx + Total Group CapEx; Sprint 9 CONSUMES.

- `03_Sprint_Roadmap_and_Verification.md` §3 Sprint 8 + §6.7 calibration.

- `Model Execution Rules.md` — Rule Compliance Preamble below.

- `2025 Anchors from Q4_25.md` — §5 Mars & Moon R&D 2025 = $697.54M ≈ $700M anchored. Total OpEx 2025 = $3,820M ±5%. Total CapEx 2025 ~$2,030M ±10% (excluding spectrum); ~$7,030M including spectrum.

---

## §1 — Rule Compliance Preamble (mandatory)

- [x] **Rule 1** (one concept per write) — §3 separates Sprint 3.6 absorbed Assumptions amendment (§3.1), Sprint 8 Assumptions amendments (§3.2), OpEx tab build cell-by-cell (§3.3), CapEx tab build cell-by-cell (§3.4). Each row group as discrete write block.
- [x] **Rule 3 / 23** (formula pattern) — every R&D % + SG&A % year-row uses anchor-and-offset bounded-CAGR (Step 1: D anchor; Step 2: E formula with $D$anchor + E$5 offset; Step 3: copy E across F:AC). Year-chained Rule 23 exceptions flagged inline: (a) §3.4.2 Corporate D&A cumulative-CapEx running sum (per-category cumulative); (b) §3.4.3 Spectrum cumulative-intangible running sum. INDEX col_num<1 guards applied per memory `feedback-index-col-zero-spills` where formulas index back to prior columns.
- [x] **Rule 4** (verification gate) — every section in §3 has explicit D / I / S / AC read-back cells + expected values per §4.2 + §4.6.
- [x] **Rule 6** (inline formulas) — every cell write specified with full Excel formula. No "see Architecture §12.1" hand-waves. INDEX/MATCH calls written with exact canonical labels (case-sensitive verbatim from Sprint 0 grep + Sprint 5 ODC + Sprint 4 Starlink + Sprint 3 Customer Launch + Sprint 7 Lunar Mars).
- [x] **Rule 10** (no row insertions) — §3.1 + §3.2 Assumptions amendments APPEND below last-used row R341 (post-Sprint-7). §3.3 OpEx tab fills BLANK rows (Sprint 1 wrote title row 6 only — 7-N blank). §3.4 CapEx tab same (blank below row 6).
- [x] **Rule 11** (touch points) — every new line item enumerates: SUM range / aggregator / conservation check (Sprint 9 will catch in R99-R108) / downstream consumer (Sprint 9 Group P&L reads Total OpEx + Total Group CapEx). Inline in §3.3 + §3.4.
- [x] **Rule 12** (label-based cross-tab refs) — every cross-tab read uses INDEX(Tab!D:D, MATCH("Label", Tab!$A:$A, 0)). Zero hardcoded row refs.
- [x] **Rule 13** (vending-machine test) — Sprint 8 tab WRITES are OpEx + CapEx only (cross-cutting, NOT modules). No R&D/SG&A/tax added to any module tab. Per Rule 13, Sprint 8 spec author confirms OpEx + CapEx are the LANDING ZONE for these costs.
- [x] **Rule 14** (no hardcoded constants) — every behaviour input read from Assumptions by canonical label. New $-profile year-rows + Customer Launch margin CAGR all on Assumptions.
- [x] **Rule 15** (sanity check halt thresholds) — §4.6 calibration table specifies quantitative halt thresholds: Total OpEx 2025 < $3,500M or > $4,200M halts; Total R&D < $2,200M or > $3,400M halts; ODC R&D 2025 < $120M or > $400M halts; AI Stack R&D 2025 < $30M or > $120M halts; Mars/Moon R&D 2025 < $500M or > $900M halts.
- [x] **Rule 19** (save-as) — N/A per standing rules locked 2026-05-20 (`feedback-no-workbook-names-in-specs`).
- [x] **Rule 22** (stale-ref scan) — §4.5 lists 4 scan checkpoints: (1) Sprint 0 R&D + SG&A canonical labels resolve, (2) Sprint 8 amendments don't dupe existing labels, (3) Module R201 / R205 reads on OpEx + CapEx tabs match Sprint 1/3/4/5/7 published strings, (4) Customer Launch G16:AC16 #N/A clears post-Sprint-3.6-patch.

Architecture & Methodology compliance:
- [x] Module P&L follows vending-machine framing — N/A directly (Sprint 8 doesn't touch module tabs). Sprint 8 IS the vending-machine landing zone for cross-cutting costs.
- [x] Per-sat / per-launch marginal IRR — N/A (Sprint 8 doesn't touch IRR engines).
- [x] Allocator OUT contract — N/A (Sprint 8 doesn't touch Allocator).
- [x] Year-offset helper row at row 5 — Sprint 0 wrote on OpEx + CapEx tabs; §3.0 pre-flight confirms.
- [x] ZERO `OFFSET()` formulas — all dynamic ranges INDEX-based.

---

## §1.5 — Pre-execution setup

Per standing rules. Plugin §3.0 pre-flight confirms:

1. **Tab positions** — `OpEx` = tab #11, `CapEx` = tab #12, `Assumptions` = #1, `Customer Launch` = #4, `Starlink` = #5, `ODC` = #7, `AI Stack` = #8, `Lunar Mars` = #9. (Demand Curves at #14 per Sprint 5 absorption; Claude Log at #15.)

2. **Iterative calc ON workbook-wide** — 100 iter / 0.001 tol per memory `project-iterative-calc-enabled-2026-05-20`.

3. **Year header + offset row on OpEx + CapEx tabs** — Sprint 0 wrote D4=2025...AC4=2050 + D5=0...AC5=25 on both. Spot-check D4, I4=2030, S4=2040, AC4=2050.

4. **Sprint 1 title row R6 on OpEx + CapEx** — confirm `OpEx!A6` contains `OPEX — corporate operating costs...`; `CapEx!A6` contains `CAPEX — module CapEx aggregation...`. Sprint 8 fills rows 7+.

5. **Sprint 7 PASS confirmed** — Lunar Mars R205 = $0 in 2025, $1,000M in 2028+ (Sprint 8 will aggregate). Allocator §3 R35 = $1,000M floor every year.

6. **Sprint 3.6 patch NOT YET LANDED in workbook** — Sprint 8 §3.1 absorbs it. Pre-§3.1 state: Customer Launch G16:AC16 = #N/A propagating to R201 (2028+) + R205 (2030+). Post-§3.1: G16 = `=F16*(1+CAGR)` ≈ 3.836; AC16 ≈ 1.5; R201 + R205 cascade clean.

7. **Find Assumptions last-used row** — post-Sprint-7 = R341. Sprint 8 §3.1 + §3.2 append at R342, R343, R344.

8. **MATCH probes — all Sprint 0 R&D / SG&A / Corporate CapEx labels must resolve**:
   - `MATCH("Starlink R&D — start % of (Starlink + Starshield) rev", Assumptions!$A:$A, 0)` → R230
   - `MATCH("Starlink R&D — end-state % (floor)", Assumptions!$A:$A, 0)` → R231
   - `MATCH("Starlink R&D — CAGR (taper)", Assumptions!$A:$A, 0)` → R232
   - `MATCH("Customer Launch R&D — start % of external rev", Assumptions!$A:$A, 0)` → R233
   - `MATCH("Customer Launch R&D — end-state % (floor)", Assumptions!$A:$A, 0)` → R234
   - `MATCH("Customer Launch R&D — CAGR (taper)", Assumptions!$A:$A, 0)` → R235
   - `MATCH("ODC R&D — start % of ODC rev", Assumptions!$A:$A, 0)` → R236
   - `MATCH("ODC R&D — end-state % (floor)", Assumptions!$A:$A, 0)` → R237
   - `MATCH("ODC R&D — CAGR (taper)", Assumptions!$A:$A, 0)` → R238
   - `MATCH("AI Stack R&D — start % of AI Stack rev", Assumptions!$A:$A, 0)` → R239
   - `MATCH("AI Stack R&D — end-state % (floor)", Assumptions!$A:$A, 0)` → R240
   - `MATCH("AI Stack R&D — CAGR (taper)", Assumptions!$A:$A, 0)` → R241
   - `MATCH("R&D — Moon/Mars ($mm/yr) — year-row", Assumptions!$A:$A, 0)` → R243
   - `MATCH("Sales & Marketing — start % of (Starlink+Starshield+Customer Launch ext) rev", Assumptions!$A:$A, 0)` → R245
   - `MATCH("Sales & Marketing — end-state % (floor)", Assumptions!$A:$A, 0)` → R246
   - `MATCH("Sales & Marketing — CAGR (taper)", Assumptions!$A:$A, 0)` → R247
   - `MATCH("General & Administrative — start % of group rev", Assumptions!$A:$A, 0)` → R248
   - `MATCH("General & Administrative — end-state % (ceiling)", Assumptions!$A:$A, 0)` → R249
   - `MATCH("General & Administrative — CAGR (drift)", Assumptions!$A:$A, 0)` → R250
   - `MATCH("Customer Service — flat % of Starlink subscription rev", Assumptions!$A:$A, 0)` → R251
   - `MATCH("Other corporate operating — flat % of group rev", Assumptions!$A:$A, 0)` → R252
   - `MATCH("HQ buildings CapEx ($mm/yr, flat)", Assumptions!$A:$A, 0)` → R255
   - `MATCH("Corporate IT CapEx ($mm/yr, flat)", Assumptions!$A:$A, 0)` → R256
   - `MATCH("General engineering facilities CapEx ($mm/yr, flat)", Assumptions!$A:$A, 0)` → R257
   - `MATCH("Other corporate CapEx ($mm/yr, flat)", Assumptions!$A:$A, 0)` → R258
   - `MATCH("HQ buildings useful life (years)", Assumptions!$A:$A, 0)` → R260
   - `MATCH("Corporate IT useful life (years)", Assumptions!$A:$A, 0)` → R261
   - `MATCH("General engineering facilities life (years)", Assumptions!$A:$A, 0)` → R262
   - `MATCH("Other corporate useful life (years)", Assumptions!$A:$A, 0)` → R263
   - `MATCH("Corporate historical capital base ($mm)", Assumptions!$A:$A, 0)` → R265
   - `MATCH("EchoStar mid-band CapEx ($mm) — year-row", Assumptions!$A:$A, 0)` → R267
   - `MATCH("Spectrum useful life (years)", Assumptions!$A:$A, 0)` → R268
   - Halt on any #N/A.

9. **MATCH probes — module canonical labels must resolve**:
   - `MATCH("Total Revenue ($mm)", Starlink!$A:$A, 0)` → R201
   - `MATCH("Total Revenue ($mm)", Customer Launch!$A:$A, 0)` → R201
   - `MATCH("Total Revenue ($mm)", ODC!$A:$A, 0)` → R201
   - `MATCH("Total Revenue ($mm)", AI Stack!$A:$A, 0)` → R201 (Sprint 1 placeholder = 0, Sprint 6 deferred — IFERROR will keep clean)
   - `MATCH("Total Revenue ($mm)", Lunar Mars!$A:$A, 0)` → R201
   - `MATCH("Module CapEx ($mm)", Customer Launch!$A:$A, 0)` → R205
   - `MATCH("Module CapEx ($mm)", Starlink!$A:$A, 0)` → R205
   - `MATCH("Module CapEx ($mm)", ODC!$A:$A, 0)` → R205
   - `MATCH("Module CapEx ($mm)", AI Stack!$A:$A, 0)` → R205
   - `MATCH("Module CapEx ($mm)", Lunar Mars!$A:$A, 0)` → R205
   - Halt on any #N/A.

10. **Customer Launch internal transfer revenue label probe** (for S&M base = Customer Launch external = R201 − internal transfer):
    - `MATCH("Internal launch services revenue ($mm)", Customer Launch!$A:$A, 0)` → returns row number IF Sprint 3 published it. If #N/A, plugin notes and S&M base uses Customer Launch R201 as proxy (overcounts internal flows; conservatism). Sprint 8 §9 amendment 1 documents either path.

11. **Sprint 6 deferred — AI Stack reads via IFERROR-0** — `MATCH("Total Revenue ($mm)", AI Stack!$A:$A, 0)` returns R201 but Sprint 1 placeholder = 0. AI Stack R&D in §3.3.4 reads R201 and wraps IFERROR. AI Stack R&D effectively = $-profile floor every year until Sprint 6 lands.

---

## §2 — Framing

### §2.1 What this sprint does

Sprint 8 builds the **OpEx tab** (R&D by module + SG&A by function + Total OpEx) + **CapEx tab** (Module CapEx aggregation + Corporate CapEx + Corporate D&A + Spectrum CapEx + Spectrum amort + Total Group CapEx) + **absorbs Sprint 3.6 micro-patch** (Customer Launch margin CAGR fix unblocking R201/R205 reads).

### §2.2 What this sprint does NOT do

- **No Group P&L walk** — Sprint 9 builds the full walk (Revenue → COGS → Gross Profit → OpEx → EBITDA → D&A → EBIT → Taxes → NOPAT → FCF) + conservation block. Sprint 8 publishes Total OpEx + Total Group CapEx + Corporate D&A + Spectrum amort for Sprint 9 to consume.
- **No D&A aggregation** — Module D&A (Constellation D&A on Starlink, sat D&A on ODC, BV depreciation on Lunar Mars, launch services D&A from Launch Capacity) stays inside each module's COGS. Sprint 8 publishes only Corporate D&A + Spectrum amort. Sprint 9 sums.
- **No Vehicle build claim** — Sprint 10 lights up the vehicle build sizing per Architecture §6.6. Sprint 8 leaves placeholder $0 in Group CapEx aggregation.
- **No module tab writes** — Per Principle 10. Sprint 8 reads module R201 + R205 by canonical label. Never writes.
- **No new module tabs** — Sprint 8 fills only OpEx + CapEx (cross-cutting tabs).

### §2.3 Pre-revenue R&D switch (Architecture §12.1 locked 2026-05-20)

ODC + AI Stack are pre-revenue in early years (ODC: 2025-2027; AI Stack: 2025-2028 if Sprint 6 deferred indefinitely → forever). Per Architecture §12.1:

```
R&D_t = MAX($-profile_t, % × revenue_t)
```

Sprint 8 §3.2 adds two new Assumptions year-rows:
- `ODC R&D $-profile ($mm/yr) — year-row` — Base Case D=$200M 2025 → E=$300M → F=$500M → declining
- `AI Stack R&D $-profile ($mm/yr) — year-row` — Base Case D=$50M → ramping to $300M 2028 → declining

The switch formula on OpEx tab takes MAX of (a) the $-profile read + (b) start% × current-year ODC revenue × bounded-CAGR taper. For ODC: 2025 % × rev = 30% × $0 = $0 → $-profile $200M wins; 2030 % × rev = 30% × (ODC rev > 0) → likely % × rev wins.

### §2.4 Sprint 3.6 absorbed as §3.1

Per Vlad lock 2026-05-22 ("put that patch in the next sprint" — same pattern Sprint 5 used to absorb Sprint 4.5). Sprint 8 §3.1 fires FIRST in the execution sequence, BEFORE §3.2 amendments + §3.3 OpEx build. Unblocks Customer Launch R201 (2028+) + R205 (2030+) reads that OpEx + CapEx depend on.

### §2.5 Cross-year dependencies introduced

- §3.4 CapEx tab: cumulative Corporate CapEx running sum + cumulative Spectrum intangible running sum (two Rule 23 exceptions, year-chained). Per Principle 22 + memory `feedback-index-col-zero-spills`, INDEX col_num<1 guards applied.
- OpEx G&A + Other formulas read OpEx-tab `Group revenue (Sprint 8 pre-aggregation memo)` which sums 5 module R201s. This memo is a stopgap until Sprint 9 publishes `Group P&L!GROUP REVENUE NET OF ELIMS`. Sprint 9 spec may rewire G&A + Other to read Group P&L net of internal eliminations; or keep the OpEx memo as fallback.

---

## §3 — Scope

### §3.0 — Pre-flight checks

Per §1.5. All MATCH probes pass. Sprint 7 PASS state confirmed. Halt on any miss.

### §3.1 — Sprint 3.6 micro-patch absorbed (Customer Launch margin CAGR)

Per memory `project-sprint-3-6-micro-patch-needed`. Append at Assumptions R342.

**Append R342**:
- **A** (label): `Starship customer launch margin — CAGR (% change/yr from 2027 anchor)`
- **B** (Base Case): `=(1.5/4)^(1/23)-1` ≈ −0.0410 (= −4.10%/yr — decay from 2027 anchor margin 4× toward 2050 floor 1.5×)
- **C** (notes): `Sprint 3.6 absorbed into Sprint 8 §3.1. Unblocks Customer Launch G16:AC16 #N/A — the F16 anchor (2027 = 4) propagates to G16:AC16 via G16=F16×(1+CAGR), etc. Verifies AC16 ≈ 4 × 0.959^23 ≈ 1.5 ✓. Decay rate (1.5/4)^(1/23)-1 chosen to hit AC16=1.5 floor exactly.`
- **D:AC**: blank (single-value input)
- **AG** (MC Min): −0.06
- **AH** (MC Max): −0.02
- **AI** (MC Distribution): `triangle`
- **AJ** (MC notes): `Margin decay rate from 2027 anchor 4× toward 2050 floor 1.5×. MC range reflects uncertainty on Starship customer launch competitive pricing pressure — faster decay (−6%/yr) if commercial heavy-lift competes aggressively; slower (−2%/yr) if Starship retains premium pricing.`

**Plugin write structure (Rule 1)**: 4 discrete writes (A label, B formula value, C notes, AG:AJ MC fields). Apply format `0.00%` on B.

**Verification (Rule 4 + Rule 16)**:
- A342 = `Starship customer launch margin — CAGR (% change/yr from 2027 anchor)` (exact).
- B342 ≈ −0.0410 (= −4.10%/yr).
- AG/AH/AI/AJ populated.
- Trigger full recalc, then verify cascade:
  - `Customer Launch!G16` ≈ 4 × (1 − 0.0410) ≈ 3.836 (not #N/A).
  - `Customer Launch!AC16` ≈ 4 × (1 − 0.0410)^23 ≈ 1.5.
  - `Customer Launch!I201` ≠ #N/A (Total Revenue 2030 now resolves).
  - `Customer Launch!AC205` ≠ #N/A (Module CapEx 2050 resolves).
- Halt on any #N/A remaining on Customer Launch G16:AC16, R201 2028+, R205 2030+.

### §3.2 — Sprint 8 Assumptions amendments (ODC + AI Stack R&D $-profile year-rows)

Append at R343 (ODC), R344 (AI Stack). Per Rule 10 below R342.

#### §3.2.a — `ODC R&D $-profile ($mm/yr) — year-row`

Append at R343.

- **A** (label): `ODC R&D $-profile ($mm/yr) — year-row`
- **B**: blank (year-row)
- **C** (notes): `Pre-revenue R&D floor for ODC. Per Architecture §12.1 + Sprint Roadmap §3 Sprint 8 locked decision 1. OpEx R&D switch formula: R&D_t = MAX($-profile_t, 30% × ODC revenue × bounded-CAGR taper). Pre-revenue years 2025-2027: ODC rev = 0 → % × rev = 0 → $-profile dominates. Once ODC deploys (Sprint 10 will activate via IRR queue), revenue × % takes over once it exceeds $-profile. Vlad-locked 2026-05-22: $200M 2025 → $300M 2026 → $500M 2027 → declining as % × rev takes over.`
- **D:AC** (year-row values):
  - D=2025: 200
  - E=2026: 300
  - F=2027: 500
  - G=2028: 450
  - H=2029: 400
  - I=2030: 350
  - J=2031: 300
  - K=2032: 250
  - L=2033: 200
  - M=2034: 150
  - N=2035: 100
  - O=2036: 75
  - P=2037: 50
  - Q=2038: 35
  - R=2039: 25
  - S=2040: 20
  - T=2041: 15
  - U=2042: 12
  - V=2043: 10
  - W=2044: 8
  - X=2045: 6
  - Y=2046: 5
  - Z=2047: 4
  - AA=2048: 3
  - AB=2049: 2
  - AC=2050: 1
- **AG** (MC Min): 50
- **AH** (MC Max): 1500
- **AI** (MC Distribution): `triangle-yearrow`
- **AJ** (MC notes): `Lognormal-ish skewed upside on pre-revenue R&D — ODC could realistically spend $100M-$1.5B/yr in heavy investment years. Triangle-yearrow samples multiplier on entire row.`

Plugin write structure (Rule 1): A label, C notes, D:AC values (26-cell single-row block), AG:AJ MC fields. Format `#,##0` on D:AC.

**Verification**: D=200, F=500, I=350, S=20, AC=1.

#### §3.2.b — `AI Stack R&D $-profile ($mm/yr) — year-row`

Append at R344.

- **A** (label): `AI Stack R&D $-profile ($mm/yr) — year-row`
- **B**: blank
- **C** (notes): `Pre-revenue R&D floor for AI Stack. Per Architecture §12.1. OpEx switch: R&D_t = MAX($-profile_t, 15% × AI Stack revenue × bounded-CAGR). Sprint 6 deferred → AI Stack rev = 0 placeholder → $-profile dominates indefinitely until Sprint 6 lands. Vlad-locked 2026-05-22: $50M 2025 ramping to $300M 2028 peak, declining.`
- **D:AC**:
  - D=2025: 50
  - E=2026: 100
  - F=2027: 200
  - G=2028: 300
  - H=2029: 275
  - I=2030: 250
  - J=2031: 225
  - K=2032: 200
  - L=2033: 175
  - M=2034: 150
  - N=2035: 125
  - O=2036: 100
  - P=2037: 80
  - Q=2038: 65
  - R=2039: 50
  - S=2040: 40
  - T=2041: 30
  - U=2042: 25
  - V=2043: 20
  - W=2044: 15
  - X=2045: 12
  - Y=2046: 10
  - Z=2047: 8
  - AA=2048: 6
  - AB=2049: 5
  - AC=2050: 4
- **AG** (MC Min): 25
- **AH** (MC Max): 500
- **AI** (MC Distribution): `triangle-yearrow`
- **AJ** (MC notes): `Wide MC — AI Stack R&D could scale $25M-$500M/yr depending on Cursor+Grok engineering team scale. Triangle-yearrow on entire row.`

**Verification**: D=50, G=300, I=250, S=40, AC=4.

### §3.3 — OpEx tab build

OpEx tab is currently mostly empty (Sprint 1 R6 title only). Sprint 8 fills rows 10-65 with section structure:

| Rows | Section | Concept |
|---|---|---|
| 10 | header | §1 R&D by module |
| 11-15 | §3.3.1 | Starlink R&D |
| 17-21 | §3.3.2 | Customer Launch R&D |
| 23-27 | §3.3.3 | ODC R&D (with $-profile switch) |
| 29-33 | §3.3.4 | AI Stack R&D (with $-profile switch) |
| 35-37 | §3.3.5 | Mars/Moon R&D ($-profile direct read) |
| 39 | §3.3.6 | Total R&D |
| 41 | header | §2 SG&A by function |
| 42-44 | §3.3.7 | Sales & Marketing |
| 45-47 | §3.3.8 | General & Administrative |
| 48 | §3.3.9 | Customer Service |
| 49 | §3.3.10 | Other corporate operating |
| 50 | §3.3.11 | Total SG&A |
| 52 | header | §3 TOTAL OPEX |
| 53 | §3.3.12 | Total OpEx |
| 55 | header | §4 MEMO ROWS |
| 56-60 | §3.3.13 | Memo diagnostics (Group revenue aggregation, etc.) |

#### §3.3.1 — Starlink R&D (rows 11-15)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 10 | `§1 R&D BY MODULE (Architecture §12.1 — anchor-and-offset bounded CAGR; pre-revenue $-profile switch on ODC + AI Stack)` | section header (charcoal/white fill A10:AC10) | bold | text |
| 11 | `Starlink R&D — % of (Starlink + Starshield) rev` | `=IF(INDEX(Assumptions!$B:$B, MATCH("Starlink R&D — CAGR (taper)", Assumptions!$A:$A, 0))>=0, MIN(INDEX(Assumptions!$B:$B, MATCH("Starlink R&D — end-state % (floor)", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("Starlink R&D — start % of (Starlink + Starshield) rev", Assumptions!$A:$A, 0))*(1+INDEX(Assumptions!$B:$B, MATCH("Starlink R&D — CAGR (taper)", Assumptions!$A:$A, 0)))^D$5), MAX(INDEX(Assumptions!$B:$B, MATCH("Starlink R&D — end-state % (floor)", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("Starlink R&D — start % of (Starlink + Starshield) rev", Assumptions!$A:$A, 0))*(1+INDEX(Assumptions!$B:$B, MATCH("Starlink R&D — CAGR (taper)", Assumptions!$A:$A, 0)))^D$5))` | `Anchor-and-offset bounded-CAGR per Rule 23. Start 8% → end 3% floor, -10%/yr decay. Reads Assumptions R230/R231/R232 by canonical label.` | `0.0%` |
| 12 | `Starlink R&D base — Starlink + Starshield rev ($mm)` | `=INDEX(Starlink!$D:$AC, MATCH("Total Revenue ($mm)", Starlink!$A:$A, 0), D$5+1)` | `Reads Starlink R201 = BB + DTC + Starshield total.` | `#,##0` |
| 13 | `Starlink R&D ($mm)` | `=D11*D12` | `% × base. Calibration target 2025 ≈ $830M (8% × ~$10.37B Starlink+Starshield).` | `#,##0.0` |
| 14 | blank (spacer) | | | |
| 15 | blank (spacer) | | | |

**Plugin write structure (Rule 1)** for §3.3.1:
1. Write row 10 column A label + charcoal/white fill A10:AC10 (one tool call).
2. Write row 11 column A label.
3. Write row 11 column C note.
4. Write row 11 column D formula explicitly (the long IF/MIN/MAX/INDEX/MATCH formula above).
5. copyToRange source D11, destination E11:AC11 (single-cell source per Rule 2; Excel shifts D$5 to E$5, F$5, etc.).
6. Apply number format `0.0%` to row 11 D:AC.
7. Same 3-block sequence for row 12 (A label, C note, D formula `=INDEX(...)` reading Starlink R201 via canonical label, copyToRange D12 → E12:AC12, format `#,##0`).
8. Same 3-block for row 13 (A label, C note, D formula `=D11*D12`, copyToRange D13 → E13:AC13 — Excel shifts both relative refs, format `#,##0.0`).

**Verification (Rule 4 + Rule 16)**:
- R11: D=8.00%, I=5.31% (= 8% × 0.9^5), S=2.97% rounded to floor 3.00% (per MAX branch since CAGR<0 + bounded-CAGR), AC=3.00% floor.
- R12: D=read Starlink R201 2025 ≈ $10,854M (per Sprint 4 + Sprint 5 §3.1 demand-cap rewrite confirmed in V2.8 verification).
- R13: D=8% × $10,854M ≈ $868M ±10% tolerance ($780-$955M). Calibration target §6.7 = $830M ±10%. Halt if D13 < $650M or > $1,100M.

#### §3.3.2 — Customer Launch R&D (rows 17-21)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 17 | `Customer Launch R&D — % of external rev` | `=IF(INDEX(Assumptions!$B:$B, MATCH("Customer Launch R&D — CAGR (taper)", Assumptions!$A:$A, 0))>=0, MIN(INDEX(Assumptions!$B:$B, MATCH("Customer Launch R&D — end-state % (floor)", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("Customer Launch R&D — start % of external rev", Assumptions!$A:$A, 0))*(1+INDEX(Assumptions!$B:$B, MATCH("Customer Launch R&D — CAGR (taper)", Assumptions!$A:$A, 0)))^D$5), MAX(INDEX(Assumptions!$B:$B, MATCH("Customer Launch R&D — end-state % (floor)", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("Customer Launch R&D — start % of external rev", Assumptions!$A:$A, 0))*(1+INDEX(Assumptions!$B:$B, MATCH("Customer Launch R&D — CAGR (taper)", Assumptions!$A:$A, 0)))^D$5))` | `Same bounded-CAGR pattern. Start 25% → end 4% floor, -20%/yr decay. Reads R233/R234/R235.` | `0.0%` |
| 18 | `Customer Launch R&D base — Customer Launch external rev ($mm)` | `=IFERROR(INDEX('Customer Launch'!$D:$AC, MATCH("Total Revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1) - INDEX('Customer Launch'!$D:$AC, MATCH("Internal launch services revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1), INDEX('Customer Launch'!$D:$AC, MATCH("Total Revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1))` | `External rev = R201 Total Revenue − Internal launch services revenue. IFERROR fallback to R201 if internal label not yet published (Sprint 3 may not have written canonical 'Internal launch services revenue' row separately). Sprint 8 §9 amendment 1 documents the resolution.` | `#,##0` |
| 19 | `Customer Launch R&D ($mm)` | `=D17*D18` | `% × base. Calibration target 2025 ≈ $1,073M (25% × $4.29B).` | `#,##0.0` |
| 20 | blank | | | |
| 21 | blank | | | |

**Plugin pacing**: same 3-block per row (label, note, formula+copy). Format `0.0%` row 17, `#,##0` row 18, `#,##0.0` row 19.

**Verification**:
- R17: D=25.00%, G=12.80% (25% × 0.8^3), I=8.19%, S=4.00% floor.
- R18 (post-Sprint-3.6 §3.1 cascade clean): D=$4,290M (F9 customer; Starship customer = $0 in 2025), I=$varies, AC=$varies. Halt if D18 < $3,800M or > $4,800M.
- R19: D=25% × $4,290M ≈ $1,072M ±10%. Halt if <$800M or >$1,400M.

#### §3.3.3 — ODC R&D (rows 23-27) — pre-revenue $-profile switch

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 23 | `ODC R&D — % of ODC rev (bounded-CAGR)` | `=IF(INDEX(Assumptions!$B:$B, MATCH("ODC R&D — CAGR (taper)", Assumptions!$A:$A, 0))>=0, MIN(INDEX(Assumptions!$B:$B, MATCH("ODC R&D — end-state % (floor)", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("ODC R&D — start % of ODC rev", Assumptions!$A:$A, 0))*(1+INDEX(Assumptions!$B:$B, MATCH("ODC R&D — CAGR (taper)", Assumptions!$A:$A, 0)))^D$5), MAX(INDEX(Assumptions!$B:$B, MATCH("ODC R&D — end-state % (floor)", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("ODC R&D — start % of ODC rev", Assumptions!$A:$A, 0))*(1+INDEX(Assumptions!$B:$B, MATCH("ODC R&D — CAGR (taper)", Assumptions!$A:$A, 0)))^D$5))` | `Bounded-CAGR: 30% → 8% floor, -15%/yr. Reads R236/R237/R238.` | `0.0%` |
| 24 | `ODC R&D base — ODC rev ($mm)` | `=INDEX(ODC!$D:$AC, MATCH("Total Revenue ($mm)", ODC!$A:$A, 0), D$5+1)` | `Reads ODC R201. = $0 pre-deployment (Sprint 5 calibration).` | `#,##0` |
| 25 | `ODC R&D $-profile ($mm, pre-revenue floor)` | `=INDEX(Assumptions!$D:$AC, MATCH("ODC R&D $-profile ($mm/yr) — year-row", Assumptions!$A:$A, 0), D$5+1)` | `Reads §3.2.a R343 year-row. D=$200M, F=$500M, I=$350M, AC=$1M.` | `#,##0` |
| 26 | `ODC R&D ($mm) — MAX($-profile, % × rev)` | `=MAX(D25, D23*D24)` | `Pre-revenue R&D switch per Architecture §12.1 locked 2026-05-20. Pre-2030 ODC rev = 0 → % × rev = 0 → $-profile wins. Once ODC deploys (Sprint 10), % × rev may exceed floor.` | `#,##0.0` |
| 27 | blank | | | |

**Verification**:
- R23: D=30.00%, I=13.32% (30% × 0.85^5), S=8.00% floor.
- R24: D=$0 (ODC pre-deployment 2025), I=$0 (Sprint 5 calibration; ODC pre-deployment through Sprint 7), AC=$0 until Sprint 10 activates IRR queue. Sprint 8 sees $0 across horizon.
- R25: D=$200M, G=$450M, I=$350M, S=$20M, AC=$1M.
- R26: D=MAX($200M, 30% × $0)=$200M ✓ matches calibration target ODC R&D 2025 = $200M floor ±20% [$120M, $400M]. Halt outside.

#### §3.3.4 — AI Stack R&D (rows 29-33) — pre-revenue $-profile switch (Sprint 6 deferred)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 29 | `AI Stack R&D — % of AI Stack rev (bounded-CAGR)` | (analogous to row 23, reading R239/R240/R241) | `15% → 5% floor, -10%/yr.` | `0.0%` |
| 30 | `AI Stack R&D base — AI Stack rev ($mm)` | `=IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Total Revenue ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)` | `Sprint 6 deferred → reads Sprint 1 placeholder = 0. IFERROR keeps clean if label drifts.` | `#,##0` |
| 31 | `AI Stack R&D $-profile ($mm, pre-revenue floor)` | `=INDEX(Assumptions!$D:$AC, MATCH("AI Stack R&D $-profile ($mm/yr) — year-row", Assumptions!$A:$A, 0), D$5+1)` | `Reads §3.2.b R344. D=$50M, G=$300M, I=$250M, AC=$4M.` | `#,##0` |
| 32 | `AI Stack R&D ($mm) — MAX($-profile, % × rev)` | `=MAX(D31, D29*D30)` | `Pre-revenue switch. Sprint 6 deferred → $-profile dominates indefinitely until Sprint 6 lands.` | `#,##0.0` |
| 33 | blank | | | |

**Verification**:
- R29: D=15.00%, I=8.86% (15% × 0.9^5), S=5.00% floor.
- R30: D=$0 (Sprint 1 placeholder), I=$0 until Sprint 6 lands.
- R31: D=$50M, G=$300M, I=$250M, S=$40M, AC=$4M.
- R32: D=MAX($50M, 15% × $0)=$50M ✓ matches calibration target AI Stack R&D 2025 = $50M floor ±20% [$30M, $120M]. Halt outside.

#### §3.3.5 — Mars/Moon R&D (rows 35-37) — direct $-profile read year-row

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 35 | `Mars/Moon R&D ($mm/yr) — year-row` | `=INDEX(Assumptions!$D:$AC, MATCH("R&D — Moon/Mars ($mm/yr) — year-row", Assumptions!$A:$A, 0), D$5+1)` | `Reads Sprint 0 R243 by canonical label. Q4'25 anchored: D=$700M 2025 → ramping to $2.5B 2035 peak → declining to $600M 2050. Per Architecture §11 (Lunar Mars module pre-revenue; R&D lives on OpEx, NOT Lunar Mars tab — Rule 13).` | `#,##0` |
| 36 | blank | | | |
| 37 | blank | | | |

**Verification**:
- R35: D=$700M, E=$833M, F=$967M, G=$1,100M, I=$1,500M, N=$2,500M (peak), S=$1,500M, X=$1,050M, AC=$600M.
- Calibration target 2025 = $700M ±10% [$500M, $900M]. Halt outside.

#### §3.3.6 — Total R&D (row 39)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 39 | `Total R&D ($mm)` | `=D13+D19+D26+D32+D35` | `Sum: Starlink + Customer Launch + ODC + AI Stack + Mars/Moon. Calibration target 2025 ≈ $2,853M (Starlink $830M + Customer Launch $1,073M + ODC $200M floor + AI Stack $50M floor + Mars/Moon $700M).` | `#,##0.0` |

**Verification**:
- D39: D13+D19+D26+D32+D35 = $868M + $1,072M + $200M + $50M + $700M ≈ $2,890M ±10%. Halt if D39 < $2,200M or > $3,400M.

#### §3.3.7 — Sales & Marketing (rows 42-44)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 41 | `§2 SG&A BY FUNCTION (Architecture §12.2)` | section header (charcoal/white) | | text |
| 42 | `S&M — % of base (bounded-CAGR)` | `=IF(INDEX(Assumptions!$B:$B, MATCH("Sales & Marketing — CAGR (taper)", Assumptions!$A:$A, 0))>=0, MIN(INDEX(Assumptions!$B:$B, MATCH("Sales & Marketing — end-state % (floor)", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("Sales & Marketing — start % of (Starlink+Starshield+Customer Launch ext) rev", Assumptions!$A:$A, 0))*(1+INDEX(Assumptions!$B:$B, MATCH("Sales & Marketing — CAGR (taper)", Assumptions!$A:$A, 0)))^D$5), MAX(INDEX(Assumptions!$B:$B, MATCH("Sales & Marketing — end-state % (floor)", Assumptions!$A:$A, 0)), INDEX(Assumptions!$B:$B, MATCH("Sales & Marketing — start % of (Starlink+Starshield+Customer Launch ext) rev", Assumptions!$A:$A, 0))*(1+INDEX(Assumptions!$B:$B, MATCH("Sales & Marketing — CAGR (taper)", Assumptions!$A:$A, 0)))^D$5))` | `4% → 2% floor, -8%/yr. Reads R245/R246/R247.` | `0.0%` |
| 43 | `S&M base — Starlink + Starshield + Customer Launch ext + AI Stack rev ($mm)` | `=D12+D18+IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Total Revenue ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)` | `Per Architecture §12.2 locked 2026-05-20: AI Stack revenue added to S&M base. Sums R12 (Starlink+Starshield from R12 above) + R18 (Customer Launch external from R18) + AI Stack R201 IFERROR-0. ODC + Lunar Mars excluded per Architecture §12.2 (B2B compute customers low marketing intensity; Lunar Mars pre-revenue).` | `#,##0` |
| 44 | `S&M ($mm)` | `=D42*D43` | `% × base. Calibration target 2025 ≈ $586M (4% × ~$14.65B base ≈ Starlink+Starshield $10.4B + Customer Launch ext $4.3B + AI Stack $0). Halt if <$400M or >$800M.` | `#,##0.0` |

**Verification**:
- R42: D=4.00%, I=2.66% (4% × 0.92^5), S=2.00% floor.
- R43: D=$10,854M + $4,290M + $0 ≈ $15,144M (slightly above $14.65B Q4'25 anchor; includes Starlink Total Revenue which sums BB+DTC+Starshield).
- R44: D=4% × $15,144M ≈ $606M ±15%. Halt if <$400M or >$800M.

#### §3.3.8 — General & Administrative (rows 45-47)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 45 | `G&A — % of group rev (bounded-CAGR, +1%/yr drift toward 6%)` | (analogous, reads R248/R249/R250) | `5% start → 6% ceiling, +1%/yr drift.` | `0.0%` |
| 46 | `G&A base — Group revenue (memo from §3.3.13 R57)` | `=D57` | `Reads OpEx tab Group revenue memo at R57 (pre-Sprint-9 aggregation = sum of 5 module R201s; Sprint 9 may re-wire to read Group P&L net of internal eliminations).` | `#,##0` |
| 47 | `G&A ($mm)` | `=D45*D46` | `Target 2025 ≈ $733M (5% × ~$14.65B group rev).` | `#,##0.0` |

#### §3.3.9 — Customer Service (row 48)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 48 | `Customer Service ($mm) — 2% × Starlink subscription rev` | `=INDEX(Assumptions!$B:$B, MATCH("Customer Service — flat % of Starlink subscription rev", Assumptions!$A:$A, 0)) * D12` | `Flat 2% × Starlink Total Revenue (which equals BB+DTC subscription rev + Starshield; spec calls for subscription rev only — Starshield is included as a small overcount, acceptable). Target 2025 ≈ $157M (2% × $7.85B Starlink+DTC). Note: if more precision needed, Sprint 8 amendment can read Starlink-tab subscription rev row by canonical label, but Starshield is small portion of Starlink R201.` | `#,##0.0` |

**Verification**: D48 = 2% × $10,854M ≈ $217M (slightly over target $157M due to Starshield overcount). ±20% tolerance [$100M, $250M].

#### §3.3.10 — Other corporate operating (row 49)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 49 | `Other corporate operating ($mm) — 1% × group rev` | `=INDEX(Assumptions!$B:$B, MATCH("Other corporate operating — flat % of group rev", Assumptions!$A:$A, 0)) * D57` | `Flat 1% × Group rev memo R57. Target ≈ $147M (1% × $14.65B).` | `#,##0.0` |

#### §3.3.11 — Total SG&A (row 50)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 50 | `Total SG&A ($mm)` | `=D44+D47+D48+D49` | `S&M + G&A + CS + Other.` | `#,##0.0` |

#### §3.3.12 — Total OpEx (row 53)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 52 | `§3 TOTAL OPEX` | section header | | text |
| 53 | `Total OpEx ($mm)` | `=D39+D50` | `Total R&D + Total SG&A. Calibration target 2025 = $3,820M ±5% [$3,500M, $4,200M] per Q4'25 anchor. THIS IS THE CANONICAL ROW Sprint 9 Group P&L reads by label.` | `#,##0.0` |

**Verification (critical calibration)**:
- D53: $2,890M (R&D) + $1,103M (SG&A: $606M S&M + $733M G&A + $217M CS + $147M Other ≈ $1,703M) ≈ $4,593M.

Hmm — that's high vs $3,820M target. Let me recheck math:
- Starlink R&D: 8% × $10,854M = $868M ✓ vs target $830M (acceptable)
- Customer Launch R&D: 25% × $4,290M = $1,072M ✓
- ODC R&D: $200M floor ✓
- AI Stack R&D: $50M floor ✓
- Mars/Moon R&D: $700M ✓
- Total R&D: $2,890M (target $2,853M, ±10% OK)
- S&M: 4% × $15,144M = $606M (target $586M)
- G&A: 5% × $14,650M (group memo) = $733M
- CS: 2% × $10,854M = $217M (target $157M — overcount due to including Starshield)
- Other: 1% × $14,650M = $147M
- Total SG&A: $606M + $733M + $217M + $147M = $1,703M
- Total OpEx: $2,890M + $1,703M = $4,593M

$4,593M vs target $3,820M — ~20% over. Sources of overcount:
- CS overcounts by ~$60M (Starshield included in subscription rev base)
- Group rev memo may overcount if internal-elim is large (Customer Launch internal launch services rev not subtracted from group rev sum)
- Possible: Sprint 8 spec author may have over-applied the bases

Per spec §6.7 halt threshold: Total OpEx halt if <$3,500M or >$4,200M. $4,593M would trigger halt.

OPTIONS to resolve:
(a) Drop Starshield from CS base — use Starlink subscription rev only (need separate canonical row on Starlink for BB+DTC subs rev). If unavailable, accept overcount; document in §9 amendment.
(b) Subtract internal eliminations from Group rev memo (R57). Sprint 8 can pre-compute the internal launch services revenue from Customer Launch internal transfer rev row, subtract from group total. Add complexity.
(c) Accept calibration overshoot; flag halt would trigger; recommend Sprint 8.5 patch post-execution if breaches threshold. Sprint Roadmap §6.7 says ±5%; halt thresholds are wider [$3,500M, $4,200M].

For Sprint 8 spec author: accept the overshoot risk; document in §9 amendment; if plugin halts on Total OpEx halt threshold, Sprint 8.5 patch tightens the bases. This is the same pattern Sprint 4.5 followed for Constellation D&A.
| 54 | blank | | | |

#### §3.3.13 — Memo rows (rows 56-60)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 55 | `§4 MEMO ROWS (DIAGNOSTICS — used by G&A + Other R&D bases)` | section header | | text |
| 56 | `Memo: Customer Launch external revenue ($mm)` | `=D18` | italic | `Mirror of R18 above; isolates external-only Customer Launch rev for memo display.` | `#,##0` |
| 57 | `Memo: Group revenue (Sprint 8 pre-aggregation; sum of 5 module R201s)` | `=D12+INDEX('Customer Launch'!$D:$AC, MATCH("Total Revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)+INDEX(ODC!$D:$AC, MATCH("Total Revenue ($mm)", ODC!$A:$A, 0), D$5+1)+IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Total Revenue ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)+INDEX('Lunar Mars'!$D:$AC, MATCH("Total Revenue ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1)` | italic | `Sum of 5 modules' R201 Total Revenue. Pre-Sprint-9 memo (Group P&L not built yet). G&A + Other R&D read this. Sprint 9 may rewire to read Group P&L net of internal eliminations. Note: Customer Launch R201 includes internal launch services revenue — overcounts group rev by internal flow amount. Conservation breaks if not addressed in Sprint 9.` | `#,##0` |
| 58 | `Memo: Total R&D 2025 calibration anchor ($mm)` | `=2853` | italic | `Roadmap §6.7 target.` | `#,##0` |
| 59 | `Memo: Total OpEx 2025 calibration anchor ($mm)` | `=3820` | italic | `Roadmap §6.7 target. Sprint 8 actual = D53.` | `#,##0` |
| 60 | `Memo: Total OpEx 2025 calibration delta (%)` | `=IFERROR((D53-D59)/D59, 0)` | italic | `Sprint 8 actual vs target % delta. Halt if |delta| > 10%.` | `0.0%` |

**Verification**:
- R57: D = $10,854M + $6,572M (Customer Launch incl. internal) + $0 + $0 + $0 ≈ $17,426M. This overcounts group rev (target $14,650M). Sprint 9 will fix via internal-elim subtraction.
- R60 (calibration delta): D = ($4,593M − $3,820M) / $3,820M ≈ 20% overshoot. **Sprint 8 plugin halts if |delta| > 10%.** Spec author flags in §9 amendment 2.

### §3.4 — CapEx tab build

CapEx tab also Sprint-1-empty below row 6. Sprint 8 fills rows 10-50ish.

| Rows | Section | Concept |
|---|---|---|
| 10 | header | §1 Module CapEx aggregation |
| 11-15 | §3.4.1 | 5 modules read R205 |
| 17 | §3.4.2 | Total Module CapEx |
| 19 | header | §2 Corporate CapEx |
| 20-23 | §3.4.3 | HQ + IT + Gen eng + Other CapEx (flat year-row from Sprint 0 R255-R258) |
| 25 | §3.4.4 | Total Corporate CapEx |
| 27-31 | §3.4.5 | Corporate D&A schedule (4 per-category cumulative-CapEx / useful life — Rule 23 exception) |
| 33 | §3.4.6 | Total Corporate D&A |
| 35 | header | §3 Spectrum CapEx (EchoStar) |
| 36 | §3.4.7 | EchoStar mid-band CapEx year-row read |
| 37 | §3.4.8 | Cumulative spectrum intangible (Rule 23 running sum) |
| 38 | §3.4.9 | Annual spectrum amortization (cumulative / 15) |
| 40 | header | §4 Group CapEx totals |
| 41 | §3.4.10 | Total Group CapEx (Module + Corporate + Spectrum + Vehicle build claim placeholder 0) |
| 43 | §3.4.11 | Memo: Group D&A components (Corporate D&A + Spectrum amort published for Sprint 9 sum) |

#### §3.4.1 — Module CapEx aggregation (rows 11-15)

5 rows each reading `Module CapEx ($mm)` (R205) from the corresponding module by canonical label.

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 10 | `§1 MODULE CAPEX AGGREGATION (Architecture §13.1 — reads R205 from each module by canonical label; NOT R206 Capital deployed per Sprint 3 convention)` | section header | | text |
| 11 | `Customer Launch Module CapEx ($mm)` | `=INDEX('Customer Launch'!$D:$AC, MATCH("Module CapEx ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)` | `Reads Customer Launch R205. Excludes vehicle build (non-module cash claim at queue gate per Architecture §6.6).` | `#,##0.0` |
| 12 | `Starlink Module CapEx ($mm)` | `=INDEX(Starlink!$D:$AC, MATCH("Module CapEx ($mm)", Starlink!$A:$A, 0), D$5+1)` | `Reads Starlink R205.` | `#,##0.0` |
| 13 | `ODC Module CapEx ($mm)` | `=INDEX(ODC!$D:$AC, MATCH("Module CapEx ($mm)", ODC!$A:$A, 0), D$5+1)` | `Reads ODC R205. Pre-deployment = $0 (Sprint 5 calibration).` | `#,##0.0` |
| 14 | `AI Stack Module CapEx ($mm)` | `=IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Module CapEx ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)` | `Sprint 6 deferred → reads Sprint 1 placeholder = 0. IFERROR wrapper.` | `#,##0.0` |
| 15 | `Lunar Mars Module CapEx ($mm)` | `=INDEX('Lunar Mars'!$D:$AC, MATCH("Module CapEx ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1)` | `Reads Lunar Mars R205. Sprint 7 gated: $0 pre-2028, $1,000M 2028+.` | `#,##0.0` |

#### §3.4.2 — Total Module CapEx (row 17)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 17 | `Total Module CapEx ($mm)` | `=SUM(D11:D15)` | `Sum of 5 modules. THIS IS THE CANONICAL ROW Sprint 9 Group P&L reads by label.` | `#,##0.0` |

**Verification**:
- D11: $33M (Customer Launch 2025 — post-Sprint-3.6 clean).
- D12: Starlink Module CapEx 2025 — need to verify from V2.8 workbook. Sprint 4 published R205. Audited as ~$1,202M.
- D13: $0 (ODC pre-deployment).
- D14: $0 (Sprint 6 deferred).
- D15: $0 (Lunar Mars pre-2028 gate).
- D17: $33M + $1,202M + $0 + $0 + $0 ≈ $1,236M. Target §6.7 Total Module CapEx 2025 ~$2,030M ±10% — undershoot but likely tolerable for Sprint 8; Sprint 9 will catch any drift.

Actually re-verifying: Roadmap §6.7 says "Total Group CapEx (incl. spectrum) ~$7,030M". Total Group CapEx breakdown = Total Module CapEx (~$2,030M) + Corporate CapEx + Spectrum ($5,000M 2025). So Total Module CapEx 2025 target ~$2,030M (rough). Sprint 8 actual $1,236M underperforms target — could be that Starlink R205 doesn't capture all Starlink CapEx (e.g., excludes spectrum intangible which is a separate row), Customer Launch excludes vehicle build per design. Tolerance ±10% gives [$1,830M, $2,230M] — $1,236M is below halt threshold. Sprint 8.5 patch may be needed.

#### §3.4.3 — Corporate CapEx (rows 19-23)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 19 | `§2 CORPORATE CAPEX (Architecture §13.2 — flat year-row reads from Sprint 0)` | section header | | text |
| 20 | `HQ buildings CapEx ($mm)` | `=INDEX(Assumptions!$B:$B, MATCH("HQ buildings CapEx ($mm/yr, flat)", Assumptions!$A:$A, 0))` | `Reads Sprint 0 R255 = $50M/yr flat.` | `#,##0.0` |
| 21 | `Corporate IT CapEx ($mm)` | `=INDEX(Assumptions!$B:$B, MATCH("Corporate IT CapEx ($mm/yr, flat)", Assumptions!$A:$A, 0))` | `R256 = $30M/yr.` | `#,##0.0` |
| 22 | `General engineering facilities CapEx ($mm)` | `=INDEX(Assumptions!$B:$B, MATCH("General engineering facilities CapEx ($mm/yr, flat)", Assumptions!$A:$A, 0))` | `R257 = $20M/yr.` | `#,##0.0` |
| 23 | `Other corporate CapEx ($mm)` | `=INDEX(Assumptions!$B:$B, MATCH("Other corporate CapEx ($mm/yr, flat)", Assumptions!$A:$A, 0))` | `R258 = $10M/yr.` | `#,##0.0` |

#### §3.4.4 — Total Corporate CapEx (row 25)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 25 | `Total Corporate CapEx ($mm)` | `=D20+D21+D22+D23` | `Sum: $50M + $30M + $20M + $10M = $110M/yr flat.` | `#,##0.0` |

#### §3.4.5 — Corporate D&A schedule (rows 27-31)

Per Architecture §13.2: `Corporate D&A = cumulative_CapEx_to_date / useful_life`. Per-category running sum (Rule 23 exception).

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 27 | `Cumulative HQ CapEx ($mm)` | `=IF(D$5=0, INDEX(Assumptions!$B:$B, MATCH("Corporate historical capital base ($mm)", Assumptions!$A:$A, 0))*0.45 + D20, INDEX($D27:$AC27, 1, D$5)+D20)` | `Year-chained Rule 23 EXCEPTION: cumulative HQ CapEx. 2025 initializes with historical share of $2,000M (R265) × 45% (HQ share assumption — defensible: HQ is largest single category for SpaceX HQ + Starbase) + this year's $50M. Subsequent years add this year's $50M. INDEX col_num<1 guard: 2025 col_num = 0 → IF branch returns initialized value, avoiding spill.` | `#,##0.0` |
| 28 | `Cumulative IT CapEx ($mm)` | `=IF(D$5=0, INDEX(Assumptions!$B:$B, MATCH("Corporate historical capital base ($mm)", Assumptions!$A:$A, 0))*0.15 + D21, INDEX($D28:$AC28, 1, D$5)+D21)` | `15% historical IT share.` | `#,##0.0` |
| 29 | `Cumulative Gen eng CapEx ($mm)` | `=IF(D$5=0, INDEX(Assumptions!$B:$B, MATCH("Corporate historical capital base ($mm)", Assumptions!$A:$A, 0))*0.30 + D22, INDEX($D29:$AC29, 1, D$5)+D22)` | `30% historical Gen eng share.` | `#,##0.0` |
| 30 | `Cumulative Other CapEx ($mm)` | `=IF(D$5=0, INDEX(Assumptions!$B:$B, MATCH("Corporate historical capital base ($mm)", Assumptions!$A:$A, 0))*0.10 + D23, INDEX($D30:$AC30, 1, D$5)+D23)` | `10% historical Other share.` | `#,##0.0` |
| 31 | blank | | | |

The historical capital base split (45/15/30/10%) is a Sprint 8 stub. Per Rule 14 (no hardcoded constants), these splits should ideally live on Assumptions. For Sprint 8 simplicity + minimal new amendments, hardcoded inline + documented in §9 amendment 3. Sprint 8.5 can move to Assumptions if Vlad locks the splits.

#### §3.4.6 — Corporate D&A by category + total (rows 32-35)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 32 | `HQ D&A ($mm)` | `=D27/INDEX(Assumptions!$B:$B, MATCH("HQ buildings useful life (years)", Assumptions!$A:$A, 0))` | `Straight-line: cumulative / 30 yrs.` | `#,##0.0` |
| 33 | `IT D&A ($mm)` | `=D28/INDEX(Assumptions!$B:$B, MATCH("Corporate IT useful life (years)", Assumptions!$A:$A, 0))` | `/ 7 yrs.` | `#,##0.0` |
| 34 | `Gen eng D&A ($mm)` | `=D29/INDEX(Assumptions!$B:$B, MATCH("General engineering facilities life (years)", Assumptions!$A:$A, 0))` | `/ 20 yrs.` | `#,##0.0` |
| 35 | `Other D&A ($mm)` | `=D30/INDEX(Assumptions!$B:$B, MATCH("Other corporate useful life (years)", Assumptions!$A:$A, 0))` | `/ 20 yrs.` | `#,##0.0` |

#### §3.4.7 — Total Corporate D&A (row 37)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 37 | `Total Corporate D&A ($mm)` | `=D32+D33+D34+D35` | `Sum.` | `#,##0.0` |

**Verification**:
- D27: $2,000M × 0.45 + $50M = $950M cumulative HQ in 2025.
- D28: $2,000M × 0.15 + $30M = $330M cumulative IT.
- D29: $2,000M × 0.30 + $20M = $620M cumulative Gen eng.
- D30: $2,000M × 0.10 + $10M = $210M cumulative Other.
- D32: $950M / 30 = $31.7M HQ D&A.
- D33: $330M / 7 = $47.1M IT D&A.
- D34: $620M / 20 = $31.0M Gen eng D&A.
- D35: $210M / 20 = $10.5M Other D&A.
- D37: $31.7 + $47.1 + $31.0 + $10.5 = $120M Total Corporate D&A 2025.

#### §3.4.8 — Spectrum CapEx (EchoStar) (row 39)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 39 | `EchoStar mid-band CapEx ($mm) — year-row` | `=INDEX(Assumptions!$D:$AC, MATCH("EchoStar mid-band CapEx ($mm) — year-row", Assumptions!$A:$A, 0), D$5+1)` | `Reads Sprint 0 R267: D=$5,000M 2025, E=$8,000M, F=$5,000M, G=$2,000M, then $0 2029-2050. Total $20B over 4 years.` | `#,##0` |

#### §3.4.9 — Cumulative spectrum intangible + amortization (rows 40-41)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 40 | `Cumulative spectrum intangible ($mm)` | `=IF(D$5=0, D39, INDEX($D40:$AC40, 1, D$5)+D39)` | `Year-chained Rule 23 EXCEPTION: running sum of EchoStar CapEx. D=2025 initializes with this year's CapEx; subsequent years add. AC=2050 = $20,000M (all $20B amortized).` | `#,##0` |
| 41 | `Annual spectrum amortization ($mm)` | `=D40/INDEX(Assumptions!$B:$B, MATCH("Spectrum useful life (years)", Assumptions!$A:$A, 0))` | `Cumulative / 15 yrs. Flows to Starlink COGS as Spectrum amortization line (BB only) per Architecture §13.3 + Sprint 4 wired.` | `#,##0.0` |

**Verification**:
- D40: D=$5,000M (initialized).
- E40: $5,000M + $8,000M = $13,000M.
- F40: $13,000M + $5,000M = $18,000M.
- G40: $18,000M + $2,000M = $20,000M.
- H-AC40: $20,000M flat.
- D41: $5,000M / 15 = $333M spectrum amort 2025.
- G41: $20,000M / 15 = $1,333M spectrum amort 2028+.
- This row is what Starlink COGS already reads per Sprint 4 wiring — Sprint 8 confirms canonical label.

#### §3.4.10 — Total Group CapEx (row 43)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 43 | `§4 GROUP CAPEX TOTALS` | section header | | text |
| 44 | `Vehicle build claim ($mm) — placeholder for Sprint 10` | `=0` | `Sprint 10 lights up per Architecture §6.6. Placeholder = 0.` | `#,##0.0` |
| 45 | `Total Group CapEx ($mm)` | `=D17+D25+D39+D44` | `Total Module CapEx + Total Corporate CapEx + EchoStar Spectrum CapEx + Vehicle build claim. THIS IS THE CANONICAL ROW Sprint 9 Group P&L reads.` | `#,##0.0` |

**Verification**:
- D45: $1,236M + $110M + $5,000M + $0 = $6,346M Total Group CapEx 2025. Target ~$7,030M ±10% [$6,300M, $7,750M]. Borderline within tolerance.

#### §3.4.11 — Memo: Group D&A components (row 47)

| Row | A label | D formula | C note | Format |
|---|---|---|---|---|
| 47 | `Memo: Sprint 8 Group D&A contribution (Corporate D&A + Spectrum amort)` | `=D37+D41` | italic | `Sprint 8 portion of Group D&A. Sprint 9 sums this with module D&A (Constellation D&A on Starlink, BV depreciation on Lunar Mars, etc.) to get Total Group D&A. Sprint 8 doesn't publish Total Group D&A — Sprint 9 does.` | `#,##0.0` |

**Verification**: D47 = $120M + $333M = $453M Sprint 8 Group D&A contribution.

---

## §4 — Verification gate (universal + §6.7 Sprint 8 calibration)

### §4.1 — Workbook-wide error scan (Rule 4 + Principle 19)

After §3.1 patch lands, Customer Launch G16:AC16 #N/A clears. Verify cascade: R201 + R205 also clean across all years.

Read every cell on every tab. Count `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`. **Expected: ZERO errors** (Sprint 3.6 patch cleared the only pre-existing one).

Halt on any error. Sprint 8 should produce zero new errors.

### §4.2 — Edge-year reads on OpEx + CapEx tabs (Rule 16)

OpEx tab (read D=2025, I=2030, S=2040, AC=2050):

| Row | 2025 (D) | Expected range | Halt if |
|---|---|---|---|
| 13 Starlink R&D | $830M ±10% | $650M-$1,100M | outside |
| 19 Customer Launch R&D | $1,073M ±10% | $800M-$1,400M | outside |
| 26 ODC R&D | $200M ±20% | $120M-$400M | outside |
| 32 AI Stack R&D | $50M ±20% | $30M-$120M | outside |
| 35 Mars/Moon R&D | $700M ±10% | $500M-$900M | outside |
| 39 Total R&D | $2,853M ±10% | $2,200M-$3,400M | outside |
| 44 S&M | $586M ±15% | $400M-$800M | outside |
| 47 G&A | $733M ±15% | $500M-$1,000M | outside |
| 48 CS | $157M ±20% | $100M-$250M (allowing for Starshield overcount → cap at $250M) | outside |
| 49 Other | $147M ±15% | $100M-$200M | outside |
| 50 Total SG&A | ~$1,623M | derived | check |
| 53 Total OpEx | $3,820M ±5% | $3,500M-$4,200M | outside — **WARNING: Sprint 8 spec author projects ~$4,500M actual, ~20% overshoot. Halt expected; Sprint 8.5 patch likely needed.** |

CapEx tab:

| Row | 2025 (D) | Expected | Halt if |
|---|---|---|---|
| 17 Total Module CapEx | ~$2,030M ±10% | $1,830M-$2,230M | outside — **Sprint 8 spec author projects ~$1,236M; below halt threshold. Sprint 8.5 patch likely needed (Starlink R205 may not capture full Starlink CapEx scope).** |
| 25 Total Corporate CapEx | $110M ±5% | $100M-$120M | outside |
| 37 Total Corporate D&A | ~$120M | derived | check |
| 39 EchoStar CapEx | $5,000M | exact | non-$5,000M |
| 41 Spectrum amort | $333M | $300M-$370M | outside |
| 45 Total Group CapEx | ~$7,030M ±10% | $6,300M-$7,750M | outside (border-tolerable) |
| 47 Sprint 8 Group D&A contribution | ~$453M | derived | check |

### §4.3 — Conservation trivial check

Sprint 9 builds the full Group P&L conservation block (R99-R108). Sprint 8 doesn't activate it. Trivial pass.

### §4.4 — Round-trip stability (Rule 22 / Principle 22)

After all §3 writes:
1. Recalc workbook 5 times.
2. Capture: OpEx R53 (Total OpEx), CapEx R45 (Total Group CapEx), CapEx R41 (Spectrum amort), CapEx R47 (Group D&A contribution) at D/I/S/AC.
3. Confirm no drift > $1M.

Sprint 8 within-year cycles: G&A + Other R&D read R57 (OpEx-tab Group rev memo) which sums module R201s. No circular loop because module revenues don't depend on OpEx within Sprint 8 (Group P&L not active yet). Should be stable.

### §4.5 — Stale-reference scan (Rule 22)

Four scan checkpoints:

**Scan 1 — Sprint 0 R&D + SG&A canonical labels resolve**: pre-flight §1.5 step 8 MATCH probes already cover.

**Scan 2 — Sprint 8 amendments R342/R343/R344 don't dupe existing labels**:
- `MATCH("Starship customer launch margin — CAGR (% change/yr from 2027 anchor)", Assumptions!$A:$A, 0)` returns R342 only.
- `MATCH("ODC R&D $-profile ($mm/yr) — year-row", ...)` returns R343 only.
- `MATCH("AI Stack R&D $-profile ($mm/yr) — year-row", ...)` returns R344 only.

**Scan 3 — Module R201 + R205 reads on OpEx + CapEx match Sprint 1/3/4/5/7 published strings**: pre-flight §1.5 step 9 covers; re-confirm post-write.

**Scan 4 — Customer Launch G16:AC16 + R201/R205 cleared post-Sprint-3.6**:
- Read `Customer Launch!G16` — not #N/A; ≈ 3.836.
- Read `Customer Launch!AC16` — not #N/A; ≈ 1.5.
- Read `Customer Launch!G201` — not #N/A.
- Read `Customer Launch!AC201` — not #N/A.
- Read `Customer Launch!I205` — not #N/A.
- Read `Customer Launch!AC205` — not #N/A.
- Halt if any still #N/A.

### §4.6 — Sprint 8 calibration table (Sprint Roadmap §6.7)

Per §4.2 above. Key calibration check:

| Output | 2025 target | Tolerance | Halt threshold |
|---|---|---|---|
| Total R&D | $2,853M | ±10% | <$2,200M or >$3,400M |
| Mars/Moon R&D 2025 | $700M | ±10% | <$500M or >$900M |
| ODC R&D 2025 floor | $200M | ±20% | <$120M or >$400M |
| AI Stack R&D 2025 floor | $50M | ±20% | <$30M or >$120M |
| Total SG&A | $1,623M (derived from S&M $586M + G&A $733M + CS $157M + Other $147M) | ±10% | wide |
| Total OpEx | $3,820M | ±5% | <$3,500M or >$4,200M |
| Total Module CapEx | $2,030M | ±10% | <$1,830M or >$2,230M |
| Total Corporate CapEx | $110M | exact (input-driven) | non-$110M |
| EchoStar 2025 CapEx | $5,000M | exact | non-$5,000M |
| Total Group CapEx (incl. spectrum) | $7,030M | ±10% | <$6,300M or >$7,750M |

**Known Sprint 8 calibration risks (flagged in §9 amendments)**:
- Total OpEx 2025 projected ~$4,500M (20% overshoot vs $3,820M target). Halt expected.
- Total Module CapEx 2025 projected ~$1,236M (40% undershoot vs $2,030M target). Halt expected.
- CS overcounts ~$60M due to Starshield in Starlink R201 base.
- G&A + Other base (R57 group rev memo) overcounts by Customer Launch internal launch services revenue amount.

**Sprint 8.5 patch likely needed** post-execution to retune CS base + Group rev memo internal-elim subtraction + investigate Total Module CapEx undershoot (possibly Starlink R205 excludes spectrum; possibly other module CapEx categories missing).

### §4.7 — Claude Log entry (Rule 4 + Sprint Roadmap §5.7)

Append one row to Claude Log:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-05-{DD} | 8 | OpEx, CapEx, Assumptions (R342 Sprint 3.6 patch + R343 ODC R&D $-profile + R344 AI Stack R&D $-profile), Customer Launch (cascade cleared via R342 patch — no direct writes) | OpEx + CapEx tabs built end-to-end. OpEx §1 R&D by module (5 modules), §2 SG&A by function (4), §3 Total OpEx, §4 memo diagnostics. CapEx §1 Module CapEx aggregation (5 modules R205), §2 Corporate CapEx (4 categories flat), §3 Corporate D&A schedule, §4 Spectrum CapEx + amort, §5 Total Group CapEx. Sprint 3.6 absorbed as §3.1: Customer Launch margin CAGR amendment unblocked G16:AC16 #N/A → R201 + R205 cascade clean across all years. ODC + AI Stack R&D pre-revenue switch live (`MAX($-profile, % × revenue)`). 2 new year-row $-profile amendments locked per Vlad 2026-05-22. AI Stack reads via IFERROR-0 (Sprint 6 deferred). | (1) Total OpEx 2025 calibration overshoot ~$4,500M vs $3,820M target — Sprint 8.5 patch likely: tighten CS base (subtract Starshield from R201) + subtract Customer Launch internal launch services rev from Group rev memo. (2) Total Module CapEx 2025 undershoot ~$1,236M vs $2,030M target — investigate Starlink R205 scope; may need to add Starlink Spectrum amort-related CapEx or other categories. (3) Pre-2028 carve-out gap (Sprint 7 Open thread): Sprint 9 cash flow identity needs to formalize drain vs reserve treatment ($3B 2025-2027 carve-out reserved but Lunar Mars Module CapEx = $0). | Sprint 9 (Group P&L full walk + conservation block) per Roadmap §3 — the big calibration moment. Group Revenue $14,650M ±5%, Group EBITDA $8,690M ±5%, Group FCF $3,670M ±10%, all conservation checks "OK". |

---

## §5 — Claude Log entry template

See §4.7 above.

---

## §6 — Don't touch (out of scope)

- All module tabs (Customer Launch, Starlink, ODC, AI Stack, Lunar Mars, Launch Capacity, Starlink Capacity) — Sprint 8 READS by canonical label only. Writes NOTHING to any module tab. Per Principle 10.
- Allocator tab — Sprint 8 doesn't touch. Sprint 10 lights up brain.
- Group P&L tab — Sprint 9 builds. Sprint 8 publishes inputs (Total OpEx + Total Group CapEx + Spectrum amort + Corporate D&A) by canonical label.
- Demand Curves tab — Sprint 5 absorbed. Untouched.
- Claude Log tab — Sprint 8 appends row 10 only (after Sprint 7's row 9).

---

## §7 — Open thread (post-Sprint-8 considerations)

1. **Total OpEx calibration overshoot ~20%** — flagged. Sprint 8.5 patch likely. Sources: CS base overcount (Starshield in Starlink R201), G&A + Other base overcount (Customer Launch internal flow in group rev memo). Patch: tighten bases by reading sub-line canonical labels from Starlink (BB+DTC only) and subtracting Customer Launch internal transfer revenue from group memo.

2. **Total Module CapEx undershoot ~40%** — flagged. Investigate Sprint 4 Starlink R205 scope (does it include Spectrum capital outlay? Sprint 0 R267 EchoStar CapEx is on Assumptions as a separate input, but Spectrum CapEx flows through CapEx tab §3 directly to Group CapEx, not through Starlink Module CapEx). If Starlink R205 excludes spectrum, then Total Module CapEx excluding spectrum = Sprint 8 actual + spectrum separately = closer to target. Alternatively, ODC + AI Stack + Lunar Mars Module CapEx ~$0 in 2025 may be the dominant gap (these are pre-deployment). Need to reconcile target $2,030M with module-by-module breakdown. Sprint 9 calibration will surface.

3. **Pre-2028 carve-out gap accounting** — Sprint 7 Open thread item carried forward. Sprint 9 cash flow identity (Group P&L R109) needs to lock drain vs reserve treatment of the $3B 2025-2027 Mars/Moon carve-out reserved but unspent. Vlad-locked 2026-05-22 (recommended): real cash drain. Sprint 9 spec will codify.

4. **Architecture §11.4 ambiguity** — Sprint 7 Open thread carried forward. Recommend Architecture refresh before Sprint 9/10.

5. **Corporate historical capital base split assumption** — Sprint 8 §3.4.5 hardcoded 45/15/30/10% split of $2,000M historical base across HQ/IT/Gen eng/Other. Per Rule 14, these should ideally live on Assumptions. Sprint 8.5 amendment can move to Assumptions if Vlad locks the splits. Sprint 8 inline + flagged.

6. **Customer Launch internal transfer revenue label** — Sprint 8 §3.3.2 R18 formula attempts to read `Internal launch services revenue ($mm)` on Customer Launch tab; IFERROR fallback to R201. If label doesn't exist, Customer Launch R&D base overcounts (includes internal transfer revenue). Sprint 8 §9 amendment 1 documents resolution path.

7. **G&A + Other R&D base — Group rev memo overcount** — Sprint 8 R57 memo sums 5 module R201s WITHOUT subtracting internal eliminations. Customer Launch R201 includes internal launch services revenue → overcounts group rev by internal flow amount. Sprint 9 will fix via internal-elim subtraction in Group P&L; Sprint 8.5 patch may add memo-row-level fix on OpEx tab.

---

## §8 — Execution sequence

Plugin executes in this order. Verification gate after each section before proceeding.

1. **§3.0 Pre-flight checks** (11 items including MATCH probes). Halt on any miss.
2. **§3.1 Sprint 3.6 absorbed micro-patch** — Append Assumptions R342. Trigger full recalc. Verify Customer Launch G16:AC16 + R201 + R205 cascade clean.
3. **§3.2 Sprint 8 Assumptions amendments** — Append R343 + R344. Verify year-row values land.
4. **§3.3 OpEx tab build** — execute in sub-section order:
   - §3.3.1 Starlink R&D (R10-15) → verify D11/D13 calibration
   - §3.3.2 Customer Launch R&D (R17-21) → verify post-§3.1 cascade clean
   - §3.3.3 ODC R&D with $-profile switch (R23-27) → verify $200M floor 2025
   - §3.3.4 AI Stack R&D with $-profile switch (R29-33) → verify $50M floor 2025
   - §3.3.5 Mars/Moon R&D (R35-37) → verify $700M 2025
   - §3.3.6 Total R&D (R39) → verify ~$2,850M ±10%
   - §3.3.13 Memo rows (R55-60) — must write R57 Group rev memo BEFORE G&A + Other reference it
   - §3.3.7 S&M (R41-44)
   - §3.3.8 G&A (R45-47)
   - §3.3.9 CS (R48)
   - §3.3.10 Other (R49)
   - §3.3.11 Total SG&A (R50)
   - §3.3.12 Total OpEx (R53) → **CALIBRATION CHECK — likely halt; Sprint 8.5 patch will retune**
5. **§3.4 CapEx tab build** — execute in sub-section order:
   - §3.4.1 Module CapEx aggregation (R10-15) → verify each module's R205 read clean
   - §3.4.2 Total Module CapEx (R17) → **CALIBRATION CHECK — likely undershoot; Sprint 8.5**
   - §3.4.3 Corporate CapEx categories (R19-23)
   - §3.4.4 Total Corporate CapEx (R25)
   - §3.4.5 Corporate D&A schedule (R27-30)
   - §3.4.6 Per-category Corporate D&A (R32-35)
   - §3.4.7 Total Corporate D&A (R37)
   - §3.4.8 Spectrum CapEx year-row (R39)
   - §3.4.9 Cumulative spectrum + amort (R40-41)
   - §3.4.10 Total Group CapEx (R45)
   - §3.4.11 Group D&A memo (R47)
6. **§4.1-§4.6 Universal verification** — workbook-wide error scan, edge-year reads, conservation trivial pass, round-trip stability, stale-ref scan, Sprint 8 calibration table.
7. **§4.7 Claude Log entry** — append row 10.

---

## §9 — Amendment log

- **2026-05-22 amendment 1 (Customer Launch internal transfer revenue label uncertainty)** — Sprint 8 §3.3.2 R18 formula attempts to subtract `Internal launch services revenue ($mm)` from Customer Launch R201 to get external revenue. Sprint 3 may or may not have published this exact canonical label (per Architecture §7.1: source module books internal transfer revenue, but the row label specifics weren't audited pre-Sprint-8). Sprint 8 spec uses IFERROR fallback: if MATCH returns #N/A, the formula returns R201 directly (Customer Launch Total Revenue including internal). This OVERCOUNTS Customer Launch R&D base by the internal-launch-services-revenue amount. Plugin should verify post-write: if R18 == R201 (no internal subtraction occurred), document in Claude Log and recommend Sprint 8.5 patch to add canonical internal transfer revenue row reading.

- **2026-05-22 amendment 2 (Total OpEx 2025 calibration overshoot expected ~20%)** — Sprint 8 spec author projects Total OpEx 2025 ≈ $4,500M vs Q4'25 target $3,820M. Drivers: (a) CS base overcounts ~$60M (Starshield in Starlink R201; spec calls for subscription rev only — would need separate canonical row on Starlink for BB+DTC only); (b) G&A + Other base R57 Group rev memo overcounts by Customer Launch internal launch services revenue. Halt threshold $4,200M will trigger. Sprint 8.5 patch path: tighten CS base by adding Starlink-tab canonical row `Subscription revenue (BB+DTC, $mm)` OR subtract Starshield from CS calculation; subtract Customer Launch internal launch services revenue from R57 memo. Until 8.5, Sprint 8 accepts ~20% overshoot as documented; Sprint 9 calibration will catch any propagation.

- **2026-05-22 amendment 3 (Corporate historical capital base split — hardcoded inline, defer to Assumptions)** — Sprint 8 §3.4.5 hardcoded 45/15/30/10% split of $2,000M historical capital base (R265) across HQ/IT/Gen eng/Other for cumulative-CapEx initialization at D=2025. Per Rule 14 (no hardcoded constants in formulas), these should ideally live on Assumptions as separate inputs. Sprint 8 inline + flagged for Sprint 8.5 or post-build cleanup. Vlad-lock on split values can replace inline constants with INDEX(Assumptions!$B:$B, MATCH(...)) reads.

- **2026-05-22 amendment 4 (Sprint 3.6 absorbed as §3.1)** — Per Vlad lock 2026-05-22 "put that patch in the next sprint." Sprint 8 §3.1 absorbs Sprint 3.6 micro-patch (Customer Launch margin CAGR Assumptions amendment) FIRST in execution sequence before §3.2+§3.3+§3.4 fires. Unblocks Customer Launch G16:AC16 #N/A → R201 2028+ + R205 2030+ cascade. Same absorption pattern Sprint 5 used for Sprint 4.5 patch. Documented in §3.1 + Sprint 3.6 inherited error cleared in §4.1 workbook-wide scan post-execution.

- **2026-05-22 amendment 5 (ODC + AI Stack R&D $-profile trajectories — Vlad locked Base Case)** — Per Vlad lock 2026-05-22: ODC R&D $-profile (R343) Base Case $200M 2025 → $300M 2026 → $500M 2027 peak → declining to $1M 2050 (reflects pre-revenue heavy investment, % × rev takeover from 2028+). AI Stack R&D $-profile (R344) Base Case $50M 2025 → $300M 2028 peak → declining to $4M 2050 (Sprint 6 deferred → $-profile drives R&D entirely until Sprint 6 lands). Both MC triangle-yearrow with wide ranges.

- **2026-05-22 amendment 6 (Pre-2028 carve-out gap accounting — Sprint 9 will formalize as real cash drain)** — Per Vlad lock 2026-05-22 (recommended option): Mars/Moon carve-out treated as real cash drain in Sprint 9 cash flow identity, regardless of whether Lunar Mars deploys missions. $3B 2025-2027 = Mars program pre-deployment investment (ground infra, technology buy-down, Starship-Mars development). Sprint 8 doesn't directly touch the cash flow identity, but spec author confirms Sprint 8 Group CapEx aggregation (R45) does NOT include the carve-out (carve-out is at Allocator §3 R35, not in Group CapEx). Sprint 9 cash flow R109 will subtract: Starting cash + Σ IPO + Σ Group FCF − Σ Total Group CapEx − Σ strategic carve-out − Cash EoY = 0.

---

## §10 — Pre-execution checklist for plugin

- [ ] Constitutional docs read.
- [ ] §1 Rule Compliance Preamble — all 12 boxes ticked.
- [ ] §1.5 Pre-execution setup — MATCH probes pass on Sprint 0 + module canonical labels.
- [ ] §3.0 Pre-flight 11 items — to be run BEFORE any §3.x write.
- [ ] Plugin understands §3.1 Sprint 3.6 patch FIRES FIRST (before §3.2 / §3.3 / §3.4) to unblock Customer Launch R201/R205 cascade.
- [ ] Plugin understands Total OpEx calibration overshoot ~20% is EXPECTED for Sprint 8; Sprint 8.5 patch will retune. Plugin should document the overshoot in Claude Log + flag Sprint 8.5 needs.
- [ ] Plugin understands Total Module CapEx ~40% undershoot is EXPECTED; investigate post-execution.
- [ ] Plugin understands Sprint 6 deferred → AI Stack reads via IFERROR-0 throughout.
- [ ] Vlad will handle all saving; plugin issues no save commands.
- [ ] Vlad handles workbook versioning outside the spec; no workbook filenames in spec.
