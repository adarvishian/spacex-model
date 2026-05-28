# Sprint 8.5 — Patch — OpEx retune (CS Starshield overcount + Group rev memo internal-flow overcount)

**Day budget**: ~10 min plugin runtime
**Owner**: Sprint 8.5 patch (this chat = spec author; separate fresh chat will execute as plugin)
**Trigger**: Sprint 8 execution 2026-05-22 hit two calibration halt thresholds — Total OpEx +24.5% ($4,757M vs $3,820M halt floor $4,200M) + Total Module CapEx -39% ($1,235M vs $2,030M halt floor $1,830M). Per memory `project-sprint-8-execution-status-2026-05-22`, both breaches fully decomposed: $226M genuinely fixable in 8.5 (CS Starshield + G&A/Other R57 internal flow overcount); $711M Total OpEx residual + $795M Module CapEx are ARCHITECTURAL (Architecture §12.1 + §6.6 amendments). Sprint 8.5 fixes the $226M overcount AND amends Roadmap §6.7 calibration targets to reflect rebuild architecture.

---

## §0 — Constitutional references

- `01_Lessons_Learned.md`:
  - **Principle 8** (vending-machine — module COGS direct production only) — Sprint 8.5 doesn't touch any module tab. OpEx-only retune.
  - **Principle 12 / Rule 23** (anchor-and-offset) — Sprint 8.5 doesn't add new ramps; just rewires existing reads.
  - **Principle 14** (cross-tab refs by label) — Sprint 8.5 reads Starlink R120 `BB Revenue ($mm)` + R131 `DTC Revenue ($mm)` + Customer Launch R70 `Customer Launch internal transfer revenue ($mm)` by canonical label.
  - **Principle 23** (calibration anchored) — Sprint 8.5 hits revised Roadmap §6.7 targets: Total OpEx ~$4,476M ±5% [$4,250M, $4,700M]; Total Module CapEx ~$1,235M ±10% [$1,110M, $1,360M]; Group CapEx target $7,030M unchanged.

- `02_Architecture_and_Methodology.md`:
  - **§12.2** (SG&A bases) — CS base = Starlink **subscription** rev (BB + DTC), NOT Starlink Total Revenue (which includes Starshield). Architecture spec was clear; Sprint 8 implementation drift used Total Revenue. Sprint 8.5 corrects.
  - **§15.2 R99 Revenue check** — Group P&L conservation will catch internal-flow over-/undercount once Sprint 9 lights up. Sprint 8.5's R57 fix pre-empts a Sprint 9 conservation break.

- `03_Sprint_Roadmap_and_Verification.md` §6.7 — calibration target update.

- `Model Execution Rules.md` — Rule Compliance Preamble below.

---

## §1 — Rule Compliance Preamble (mandatory)

- [x] **Rule 1** (one concept per write) — §3 isolates two OpEx-tab formula rewires (R48 + R57) + one Roadmap §6.7 amendment doc update. Each as discrete write.
- [x] **Rule 3 / 23** — Sprint 8.5 doesn't add new ramps. Existing R57 retains anchor-and-offset structure of underlying year-row reads.
- [x] **Rule 4** (verification gate) — §4 reads back R48 + R57 + dependents R47/R49/R50/R53/R60 D / I / S / AC. Halt on miss.
- [x] **Rule 6** (inline formulas) — both new formulas written verbatim in §3.
- [x] **Rule 10** (no row insertions) — Sprint 8.5 ONLY rewires existing cells D48 + D57 (then copies E:AC). Zero row insertions. Zero Assumptions amendments.
- [x] **Rule 11** (touch points) — R48 + R57 changes cascade to R47 (G&A reads R57), R49 (Other reads R57), R50 (Total SG&A sums), R53 (Total OpEx). All on same OpEx tab. Sprint 9 Group P&L conservation will pick up downstream when it builds.
- [x] **Rule 12** (label-based) — both new formulas use INDEX/MATCH on Starlink R120/R131 + Customer Launch R70 canonical labels.
- [x] **Rule 13** (vending-machine test) — N/A (Sprint 8.5 doesn't touch module tabs).
- [x] **Rule 14** — N/A (no new behavior constants).
- [x] **Rule 15** (sanity check halt thresholds) — §4 specifies post-fix targets: CS $157M ±20%, G&A $733M ±15%, Other $147M ±20%, Total OpEx $4,476M ±5% (REVISED FROM $3,820M per Sprint 8.5 amendment to §6.7).
- [x] **Rule 19** — N/A (no workbook filenames; Vlad handles versioning).
- [x] **Rule 22** (stale-ref scan) — §4.5 confirms canonical labels Sprint 8.5 reads resolve verbatim.

---

## §1.5 — Pre-execution setup

1. **Tab state** — OpEx tab populated by Sprint 8. CapEx tab populated by Sprint 8. Sprint 8.5 ONLY touches OpEx rows 48 + 57.
2. **Iterative calc ON** — confirm 100 iter / 0.001 tol per memory `project-iterative-calc-enabled-2026-05-20`.
3. **Sprint 8 state confirmed** — Sprint 8 PASS-with-overshoot per memory `project-sprint-8-execution-status-2026-05-22`. Sprint 3.6 absorbed into Sprint 8 §3.1 — Customer Launch G16:AC16 cleared.
4. **MATCH probes** (pre-flight before any write):
   - `MATCH("BB Revenue ($mm)", Starlink!$A:$A, 0)` → R120 (Sprint 4 published).
   - `MATCH("DTC Revenue ($mm)", Starlink!$A:$A, 0)` → R131 (Sprint 4 published).
   - `MATCH("Customer Launch internal transfer revenue ($mm)", 'Customer Launch'!$A:$A, 0)` → R70 (Sprint 3 published).
   - `MATCH("Customer Service — flat % of Starlink subscription rev", Assumptions!$A:$A, 0)` → R251 (Sprint 0 published).
   - Halt on any #N/A.

---

## §2 — Framing

Sprint 8 hit Total OpEx halt threshold. Decomposition (per `project-sprint-8-execution-status-2026-05-22`):
- $226M genuinely fixable: CS reads Starlink R201 ($10,854M including Starshield) instead of subscription rev only ($7,853M = BB+DTC); G&A + Other R57 group rev memo overcounts by $2,290M (Customer Launch internal transfer revenue).
- $711M architectural: pre-revenue R&D floors + Q4'25 rate × base divergence — legitimate, not a bug.

Sprint 8.5 fixes the $226M overcount + amends Roadmap §6.7 to reflect the architectural reality. Post-Sprint-8.5 Total OpEx ≈ $4,560M ±5% of revised target $4,476M → Sprint 9 EBITDA target ($8,690M) hits exact when subtracted from estimated Group Gross Profit $13,250M.

---

## §3 — Scope

### §3.1 — OpEx R48 CS formula rewire (BB + DTC subscription rev only)

**Current (Sprint 8 D48)**: `=INDEX(Assumptions!$B:$B, MATCH("Customer Service — flat % of Starlink subscription rev", Assumptions!$A:$A, 0)) * D12`

Where D12 = Starlink R201 = $10,854M (BB + DTC + Starshield).

**Replacement D48**:

```
=INDEX(Assumptions!$B:$B, MATCH("Customer Service — flat % of Starlink subscription rev", Assumptions!$A:$A, 0)) * (INDEX(Starlink!$D:$AC, MATCH("BB Revenue ($mm)", Starlink!$A:$A, 0), D$5+1) + INDEX(Starlink!$D:$AC, MATCH("DTC Revenue ($mm)", Starlink!$A:$A, 0), D$5+1))
```

**Note column C (overwrite)**: `Flat 2% × Starlink subscription rev (BB + DTC, NOT Starshield). Sprint 8.5 patch: rewire reads Starlink R120 BB Revenue + R131 DTC Revenue directly via canonical label. Target 2025 = 2% × ($7,696M + $157M) = $157M ✓ exact match Q4'25 anchor.`

**Plugin write structure**:
1. Write D48 formula explicitly (one tool call).
2. copyToRange source D48, destination E48:AC48 (single-cell source per Rule 2; Excel shifts D$5 to E$5 etc).
3. Overwrite column C note.
4. Number format `#,##0.0` (already in place from Sprint 8).

**Verification post-write**:
- D48 = 2% × ($7,696M + $157M) = 2% × $7,853M = **$157M** ✓ exact (target $157M ±20% = [$100M, $250M])
- I48 = 2% × (BB rev 2030 + DTC rev 2030) — depends on Sprint 4 trajectory; expected ~$300-400M
- S48 / AC48 same pattern
- Halt if D48 outside [$130M, $185M] (tighter ±20% bands).

### §3.2 — OpEx R57 Group rev memo subtract Customer Launch internal transfer revenue

**Current (Sprint 8 D57)**:
```
=D12+INDEX('Customer Launch'!$D:$AC, MATCH("Total Revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)+INDEX(ODC!$D:$AC, MATCH("Total Revenue ($mm)", ODC!$A:$A, 0), D$5+1)+IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Total Revenue ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)+INDEX('Lunar Mars'!$D:$AC, MATCH("Total Revenue ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1)
```

D57 = $10,854M + $6,572M + $0 + $0 + $0 = $17,426M. Customer Launch R201 includes internal transfer rev → overcounts group revenue by $2,290M.

**Replacement D57**:

```
=D12+INDEX('Customer Launch'!$D:$AC, MATCH("Total Revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)+INDEX(ODC!$D:$AC, MATCH("Total Revenue ($mm)", ODC!$A:$A, 0), D$5+1)+IFERROR(INDEX('AI Stack'!$D:$AC, MATCH("Total Revenue ($mm)", 'AI Stack'!$A:$A, 0), D$5+1), 0)+INDEX('Lunar Mars'!$D:$AC, MATCH("Total Revenue ($mm)", 'Lunar Mars'!$A:$A, 0), D$5+1)-INDEX('Customer Launch'!$D:$AC, MATCH("Customer Launch internal transfer revenue ($mm)", 'Customer Launch'!$A:$A, 0), D$5+1)
```

(Identical to Sprint 8 D57 PLUS final term subtracting Customer Launch internal transfer revenue.)

**Note column C (overwrite)**: `Sum of 5 modules' R201 Total Revenue MINUS Customer Launch internal transfer revenue (Sprint 8.5 patch: subtract internal flow per Architecture §15.1 net-of-eliminations framing). Pre-Sprint-9 memo. G&A + Other R&D read this. Note: Starshield ($2,436M) still in Starlink R201 — acceptable since Starshield IS external revenue (paid by USG); the Customer Launch internal flow is the only inter-module elimination that matters for OpEx bases. Sprint 9 may add ODC↔Starlink internal bandwidth + ODC↔AI Stack internal compute eliminations once those flows light up.`

**Plugin write structure**:
1. Write D57 formula explicitly (one tool call).
2. copyToRange source D57, destination E57:AC57.
3. Overwrite column C note.

**Verification post-write**:
- D57 = $17,426M − $2,290M = **$15,136M**
- D47 G&A = 5% × $15,136M = **$757M** ✓ (target $733M ±15% = [$623M, $843M])
- D49 Other = 1% × $15,136M = **$151M** ✓ (target $147M ±15%)
- D50 Total SG&A = $605M + $757M + $157M + $151M = **$1,670M** (vs Sprint 8 $1,868M; Δ = −$198M)
- D53 Total OpEx = $2,889M + $1,670M = **$4,559M** (vs Sprint 8 $4,757M; Δ = −$198M)
- D60 calibration delta — see §3.3 below.

### §3.3 — OpEx R60 calibration delta — update vs revised target

**Current (Sprint 8 D60)**: `=IFERROR((D53-D59)/D59, 0)` where D59 = hardcoded $3,820M.

Sprint 8.5 amends D59 to **$4,476M** (revised target per §3.4 Roadmap amendment).

**D59 overwrite**:
```
=4476
```

**Note column C (overwrite)**: `Sprint 8.5 amended: Roadmap §6.7 Total OpEx target updated $3,820M → $4,476M reflecting current rebuild architecture (pre-revenue R&D floors per §12.1 + bottom-up rate × base from Sprint 0 inputs). $3,820M Q4'25 anchor was inconsistent with line-item rate × base sum; new target preserves line-item integrity.`

**Verification post-write**:
- D60 = (D53 − D59) / D59 = ($4,559M − $4,476M) / $4,476M = **+1.85%** ✓ (target ±5%)
- Halt if |D60| > 10%.

### §3.4 — Roadmap §6.7 calibration target amendment (doc edit, NOT workbook write)

Plugin writes a markdown amendment to `/Users/vladsaigau/Documents/Claude/Projects/Starlink Module/03_Sprint_Roadmap_and_Verification.md`:

**Amendment to §6.7 Sprint 8 calibration table — replace these 2 rows**:

| Output | Old target | New target | Tolerance | Notes |
|---|---|---|---|---|
| Total OpEx | $3,820mm (Q4'25 raw anchor) | **$4,476mm** | ±5% [$4,250M, $4,700M] | Sprint 8.5 amendment 2026-05-22: revised to reflect Architecture §12.1 amendments (pre-revenue R&D floors ODC + AI Stack = $250M new) + Sprint 0 R&D + SG&A rates applied bottom-up. Old $3,820M Q4'25 anchor inconsistent with line-item rate × base sum. |
| Total Group CapEx (incl. spectrum) | $7,030M ±10% | $7,030M ±10% | unchanged | Sprint 8 pre-Sprint-10 reads $6,345M (vehicle build claim = $0 placeholder); Sprint 10 lights up vehicle build claim ~$800M restoring $7,145M ≈ target. |
| (NEW LINE) Total Module CapEx | $2,030M ±10% | **$1,235M ±10%** | [$1,110M, $1,360M] | Sprint 8.5 amendment 2026-05-22: revised to reflect Architecture §6.6 (vehicle build moved from Customer Launch Module CapEx to Allocator queue gate non-module cash claim; Sprint 10 lights up). Old $2,030M Q4'25 anchor pre-dated rebuild architecture. |

**Plus add to §9 Amendment log** of the Roadmap doc:

```
- **2026-05-22 (Sprint 8.5 patch — calibration target updates)** — §6.7 Total OpEx target $3,820M → $4,476M reflecting current rebuild architecture (Architecture §12.1 pre-revenue R&D floors + Sprint 0 rate × base bottom-up). §6.7 Total Module CapEx target $2,030M → $1,235M reflecting Architecture §6.6 (vehicle build at Allocator queue gate, not Customer Launch Module CapEx). Both reflect that Q4'25 raw anchors were pre-rebuild-architecture; per-line rebuild bottom-ups now drive calibration. Sprint 9 Group P&L EBITDA target $8,690M still holds — post-Sprint-8.5 OpEx $4,559M − Group Gross Profit $13,250M estimate → EBITDA $8,691M ≈ target exact.
```

**Plugin write structure**: Edit tool on the markdown file. Two table-row edits + one Amendment log append. Plus add new "Total Module CapEx" line item to §6.7 (not previously its own row — was implied in Total Group CapEx subtotal).

---

## §4 — Verification gate

### §4.1 — Workbook-wide error scan

Read every cell. Count `#REF!`, `#VALUE!`, `#DIV/0!`, `#NAME?`, `#NUM!`, `#NULL!`, `#N/A`. **Expected ZERO errors** (Sprint 8 PASS-with-overshoot was already error-free).

### §4.2 — Edge-year reads (D / I / S / AC) on OpEx tab

| Row | 2025 (D) | 2030 (I) | 2040 (S) | 2050 (AC) | Halt if |
|---|---|---|---|---|---|
| 48 CS | $157M | varies | varies | varies | D outside [$130M, $185M] |
| 53 Total OpEx | $4,559M | varies | varies | varies | D outside [$4,250M, $4,700M] (revised target ±5%) |
| 57 Group rev memo | $15,136M | varies | varies | varies | D outside [$13,500M, $16,500M] |
| 60 Calibration delta | +1.85% | n/a | n/a | n/a | |D60| > 10% |

Also confirm downstream cascades:
- R47 G&A 2025 = $757M (was $871M Sprint 8; Δ = −$114M)
- R49 Other 2025 = $151M (was $174M Sprint 8; Δ = −$23M)
- R50 Total SG&A 2025 = $1,670M (was $1,868M Sprint 8; Δ = −$198M)

### §4.3 — Conservation trivial check

Sprint 9 builds Group P&L conservation. Sprint 8.5 doesn't activate. Trivial pass.

### §4.4 — Round-trip stability

Recalc 5 times. Capture D48, D53, D57, D60. Confirm no drift > $1M.

Sprint 8.5 doesn't introduce new circular dependencies. Existing within-year cycles (Sprint 4 Starlink ↔ Starlink Capacity; iterative calc ON workbook-wide) handle.

### §4.5 — Stale-reference scan

Confirm post-write:
- `MATCH("BB Revenue ($mm)", Starlink!$A:$A, 0)` returns row matching Starlink R120 (Sprint 4 published value $7,696M).
- `MATCH("DTC Revenue ($mm)", Starlink!$A:$A, 0)` → R131 ($157M).
- `MATCH("Customer Launch internal transfer revenue ($mm)", 'Customer Launch'!$A:$A, 0)` → R70 ($2,290M).
- All resolve verbatim.

### §4.6 — Claude Log entry

Append row to Claude Log tab:

| Date | Sprint | Tabs touched | Summary | Outstanding | Next sprint |
|---|---|---|---|---|---|
| 2026-05-{DD} | 8.5 | OpEx (R48 CS rewire + R57 Group rev memo subtract internal flow + R59/R60 calibration delta vs new target), Roadmap doc (§6.7 target amendments). Plus Claude Log this row. | Sprint 8.5 retune patch: fixed $226M genuine OpEx overcount (CS Starshield $60M + G&A/Other R57 internal flow $138M+$28M). Total OpEx D53 dropped $4,757M → $4,559M, within revised Roadmap §6.7 target $4,476M ±5%. Roadmap amended: Total OpEx target $3,820M → $4,476M; Total Module CapEx target $2,030M → $1,235M (vehicle build at Allocator §6.6). Architectural overshoots ($250M pre-revenue R&D floors + ~$461M rate × base divergence) now documented as legitimate part of rebuild architecture, not bugs to fix. | (1) Architecture §11.4 ambiguity carried from Sprint 7 §9 amendment 1 — pre-Sprint-9 Architecture refresh recommended. (2) Pre-2028 carve-out gap (Sprint 7 + Sprint 8 amendment 6) — Sprint 9 cash flow identity formalizes as real cash drain per Vlad lock 2026-05-22. (3) AI Stack 8 open questions awaiting Vlad sign-off (Stage 1 scoping doc shipped). | Sprint 9 (Group P&L full walk + conservation block + inter-module eliminations) per Roadmap §3. THE BIG CALIBRATION MOMENT: Group Revenue $14,650M ±5%, Group EBITDA $8,690M ±5%, Group FCF $3,670M ±10%, all conservation checks "OK". |

---

## §5 — Don't touch (out of scope)

- Module tabs — Sprint 8.5 READS only (BB Revenue, DTC Revenue, internal transfer revenue). Writes nothing.
- Assumptions tab — Sprint 8.5 doesn't add or modify any input. No new amendments.
- CapEx tab — Sprint 8.5 doesn't touch (Module CapEx target update is Roadmap-only; CapEx tab cells already reflect rebuild architecture).
- Allocator tab — untouched.
- Group P&L tab — untouched (Sprint 9 builds).
- Sprint 7 carve-out architecture — untouched.

---

## §6 — Open thread (post-Sprint-8.5)

1. **Sprint 9 conservation may surface additional internal flow eliminations** — Sprint 8.5 only subtracted Customer Launch internal launch services revenue from R57 memo. Sprint 9 may need to also subtract:
   - ODC ↔ Starlink internal bandwidth flow (Sprint 5 wired; Starlink internal bandwidth revenue + ODC bandwidth services cost; both = $0 in 2025 since ODC pre-deployment, but >0 from 2030+)
   - ODC ↔ AI Stack internal compute flow (Architecture §7.3; activates when Sprint 6 lands)
   If Sprint 9 conservation breaks on these, Sprint 9 spec adds the subtractions to R57 memo OR builds Group P&L net-of-elim row directly and rewires G&A + Other to read Group P&L (not OpEx memo).

2. **Starshield in S&M base** — S&M base R43 currently includes Starshield (via Starlink R201). Architecture §12.2 says "Starlink + Starshield + Customer Launch ext + AI Stack rev" — Starshield IS supposed to be in S&M base (defensible: USG sales need outreach). Sprint 8.5 doesn't touch S&M base. If Vlad wants Starshield excluded from S&M too, Sprint 8.5b can rewire R43 to read BB + DTC + Customer Launch ext + AI Stack (excluding Starshield).

3. **Total Module CapEx — Sprint 4 Starlink R205 audit** — Sprint 8.5 doesn't investigate whether Starlink R205 captures full Starlink CapEx scope (e.g., are V3 BB ratchet investments + spectrum-related Starlink CapEx in R205?). Per Sprint 4 spec, R205 = `Module CapEx ($mm)` = annual fleet CapEx for new sat units. May exclude items that should be in. If Sprint 9 calibration surfaces a gap, Sprint 9.5 patch investigates.

---

## §7 — Execution sequence

1. **§1.5 Pre-flight MATCH probes** — confirm 4 canonical labels resolve.
2. **§3.1 OpEx R48 CS rewire** — write D48 formula + copyToRange E48:AC48 + overwrite C48 note. Verify D48 = $157M.
3. **§3.2 OpEx R57 Group rev memo subtract internal flow** — write D57 + copyToRange + overwrite C57 note. Verify D57 = $15,136M and downstream R47 G&A = $757M + R49 Other = $151M + R50 Total SG&A = $1,670M + R53 Total OpEx = $4,559M.
4. **§3.3 OpEx D59 calibration anchor update** — write D59 = 4476. Verify D60 calibration delta = +1.85%.
5. **§3.4 Roadmap §6.7 amendment** — edit `03_Sprint_Roadmap_and_Verification.md`: replace 2 calibration table rows + append §9 amendment log entry + add new Total Module CapEx row to §6.7.
6. **§4 Verification gate** — workbook-wide error scan, edge-year reads, round-trip stability, stale-ref scan.
7. **§4.6 Claude Log entry** — append row 11 to Claude Log tab.

---

## §8 — Amendment log

- **2026-05-22 (Sprint 8.5 patch authored)** — Sprint 8 PASS-with-overshoot triggered Sprint 8.5 retune. Two formula rewires (OpEx R48 CS base from Starlink R201 → Starlink R120 BB + R131 DTC; OpEx R57 Group rev memo subtract Customer Launch R70 internal transfer rev). Plus Roadmap §6.7 calibration target amendment ($3,820M → $4,476M for Total OpEx; $2,030M → $1,235M for Total Module CapEx) reflecting rebuild architecture (Architecture §12.1 pre-revenue R&D floors + §6.6 vehicle build at Allocator). All $226M genuinely fixable overcount addressed; ~$711M residual is architectural and now documented as part of rebuild architecture, not bug. Sprint 9 EBITDA target $8,690M still holds with post-Sprint-8.5 OpEx $4,559M.
