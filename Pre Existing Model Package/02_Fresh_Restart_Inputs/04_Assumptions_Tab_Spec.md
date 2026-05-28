# Assumptions Tab Spec — Constitutional Document for SpaceX Model Rebuild v2

**Status**: Constitutional. Locked 2026-05-19.
**Authority**: Source of truth for the Assumptions tab build (Sprint 0 of v2).
**Primary deliverable**: `04_Assumptions_Tab_Build_Plan.xlsx` — row-by-row build plan, ready for plugin execution.
**Companion docs**: `01_Lessons_Learned.md`, `02_Architecture_and_Methodology.md`, `03_Sprint_Roadmap_and_Verification.md`, `2025 Anchors from Q4_25.md`, memories `project-anchored-assumptions-2025`, `project-rebuild-architecture`.

This doc is the wrapper around the build-plan XLSX. The XLSX is the actionable row-by-row plan. This doc describes conventions, section structure, and the inputs that need Vlad-level attention before Sprint 0 fires.

---

## §1 — Column convention for the Assumptions tab

The Assumptions tab built in Sprint 0 uses 36 columns:

| Cols | Use | Notes |
|---|---|---|
| **A** | Section header / input label | Labels left-justified. Section headers white-on-charcoal. Subsection headers italic on light grey. |
| **B** | Base Case (single-value) | Used for inputs whose value doesn't vary by year. Empty for year-row inputs. |
| **C** | Notes / source (one-liner) | Anchor source, MC rationale, structural note. |
| **D–AC** | Year columns 2025 → 2050 (26 cols) | Hardcoded integers in row 4 header (D=2025, ..., AC=2050). Year-row inputs populate this range. Empty for single-value inputs. |
| **AG** | MC Min | Lower bound of MC range. Empty for `fixed` distribution. |
| **AH** | MC Max | Upper bound. Empty for `fixed`. |
| **AI** | MC Distribution | One of: `triangle`, `lognormal`, `uniform`, `discrete`, `triangle-yearrow`, `fixed-yearrow`, `fixed`. |
| **AJ** | MC notes / rationale | Why the range is what it is; what drives the uncertainty. |

**Row 4** is the year header on every tab including Assumptions (per Architecture §2). **Row 5** is the year-offset helper row (D=0 ... AC=25). Inputs start at row 6 onwards.

Sprint 0 plugin discovery: section headers + subheads + input rows interleave. The XLSX build plan shows exactly which is which. Plugin walks the build plan top-to-bottom and writes the Assumptions tab.

---

## §2 — Section list (11 logical sections)

Maps to Architecture §1 tab content split:

| § | Section | Inputs | Notes |
|---|---|---|---|
| §1 | Global | 3 | Tax rate, TAM inflation, GNI growth. Year horizon hardcoded constants (not inputs). |
| §2 | Allocator | 18 | Cash pool boundary, IPO, Mars carve-out (MC-variable), IRR engine params, vehicle build claim params. |
| §3 | Capacity (Starship + F9) | 28 | Vehicle costs, payload, cadence (Wright's Law on cum upmass), F9 fleet decay logic. |
| §4 | Customer Launch | 9 | F9 + Starship customer launch pricing, market sizing, COGS stubs. |
| §5 | Starlink | 47 | Sat physical, Wright's Law, Starshield (Vlad-corrected from Q4'25), constellation opening balances (Mach33 hard anchors), deorbit, subscribers/ARPU/terminals, BB/DTC market mix, bandwidth flow placeholders, large-default asks. |
| §6 | ODC | 30 | Sat physical (V2 Compute 140 kW kept), subsystem cost stack, Wright's Law, chip roadmap year-rows, dual revenue model, ODC internal/external compute split (NEW). |
| §7 | AI Stack (standalone) | 9 | Cursor + Grok consumer + Grok enterprise API product lines. AI Stack is standalone module per Architecture §10. |
| §8 | Lunar / Mars | 18 | BV engine (labour units + hardware Q4'25 methodology). Carve-out share split (Lunar continuous / Mars window-bound). NOT in IRR queue. |
| §9 | OpEx | 16 | R&D by module (start% / end% / CAGR per Spec 03), R&D Moon/Mars as year-row $-profile, SG&A by function. |
| §10 | CapEx | 11 | Corporate facilities + useful lives + historical base + EchoStar spectrum. |
| §11 | Valuation | 23 | WACC + risk premia, terminal value parameters, comparables anchors, SoTP multiples. |

**Total inputs**: ~212 across 11 sections. Plus ~30 section / subsection header rows. ~290 rows visible in the Assumptions tab.

---

## §3 — MC distribution conventions

Every input has a distribution type in column AI. The MC engine (Sprint 12) samples each input independently according to its distribution.

| Distribution | When to use | Sample method |
|---|---|---|
| `fixed` | Structural input (no variability) or memo-only | No sampling; Base Case used always |
| `triangle` | Most common — bounded uncertainty with central tendency | Triangular distribution: min, mode = Base Case, max. Anchored to physical / industry / Mach33 priors. |
| `lognormal` | Skewed upside risk (e.g., IPO size, Mars carve-out %) | Lognormal: P10 ≈ min, mode ≈ Base Case, P90 ≈ max |
| `uniform` | Pure ignorance, evenly distributed | Uniform: min, max |
| `discrete` | Year choice or binary toggle | Sample uniformly from listed options |
| `triangle-yearrow` | Year-row input where the curve shape is uncertain (e.g., ODC internal share trajectory) | Sample multiplier on entire year-row; preserves shape, shifts magnitude. Or sample anchor points and re-interpolate. |
| `fixed-yearrow` | Year-row that's structurally locked (e.g., variant mix ramp, F9 decay trajectory) | No MC sampling on the year-row itself; year-row read as-is |

**Vlad's load-bearing rule (Principle 18)**: every input has its MC range populated at row creation. No "I'll add MC later." If you don't know the range, mark it `fixed` and add a note explaining why. The 18 MC-variable inputs across V30.5's spec lag never got registered properly; the rebuild doesn't repeat that failure.

---

## §4 — Anchor-and-offset year-row formula pattern (Rule 23 / Principle 12)

The Assumptions tab itself is mostly hardcoded values (no formulas — it's the input source). But year-row inputs that follow a deterministic pattern (e.g., $111M F9 price declining 3%/yr) are stored as year-row VALUES, not formulas. The PLUGIN computes the year-row values during Sprint 0 from the underlying parameters (start, end, CAGR) and writes them as static numbers.

**Why store as values not formulas:** Assumptions tab is the canonical input source. Other tabs read from Assumptions and compute downstream. If Assumptions cells had `=D14×(1+CAGR)` chains, then conservation breaks when you edit one year and forget to propagate. Storing pre-computed values keeps Assumptions tab inspectable cell-by-cell.

**Where formulas DO live on Assumptions**: bounded-CAGR derivations on the OpEx tab (rebuilt during Sprint 8). Those follow Spec 03.2 §12 retrofit pattern — anchor at column D, year-offset row 5, formula in E–AC. The XLSX build plan shows derived values for inspection; the plugin can choose to either (a) write the values directly or (b) write the formula and let Excel compute. Plugin's call, but document choice in Claude Log.

---

## §5 — First-year override convention (Sprint 10 lock)

Per Sprint Roadmap §6.9. Once the allocator brain lights up in Sprint 10, it tries to drive 2025 module CapEx from the IRR queue. But 2025 historical actuals are Mach33-anchored:

- V2 BB sats launched 2025 = 2,987 (Mach33 historical)
- V2 DTC sats launched 2025 = 182 (Mach33 historical)
- F9 boosters manufactured 2025 = ~17 (Q4'25 historical)
- F9 customer launches 2025 = 38.58 (Q4'25)
- ODC sats launched 2025 = 0
- AI Stack revenue 2025 = ~0 (early ramp only)

**Convention**: module CapEx for year 2025 (column D) = historical actual, locked. Allocator drives 2026+ only (columns E–AC). This preserves Q4'25 calibration while allowing IRR-driven dynamics in out-years.

Implementation: in Sprint 10, allocator outputs for column D are overridden by historical-actuals values pulled from Assumptions §5 (Starlink constellation opening balances), §3 (F9 manufactured 2025). Sprint 10 spec includes the override formula explicitly.

---

## §6 — Inputs that need Vlad-level attention BEFORE Sprint 0 fires

Most inputs in the build plan are pre-locked from Q4'25 or V30.5. A handful merit explicit confirmation:

### §6.1 Mars carve-out magnitudes (MC-variable, but Base Case matters)

- **Mars carve-out % of prior-year Group FCF** — Base Case 15%, MC [3%, 35%] triangle. Vlad-locked as MC-variable. Confirm 15% as the Base Case central tendency, or push higher / lower if your thesis priors disagree.
- **Mars carve-out floor ($mm/yr)** — Base Case $1,000M, MC [$500M, $2,500M] triangle.

If you want the rebuild to default to a more aggressive Mars program (e.g., Base Case 25% / $2B floor), say so before Sprint 0 — these inputs drive Lunar Mars deployment trajectory.

### §6.2 ODC internal vs external compute split trajectory

Per Architecture §7.3 / §9.3. NEW input row in §6 ODC. Default trajectory: 95% internal in 2025 → 85% in 2028 → 70% in 2032 → 50% in 2040 → 40% in 2050. External share rises as external compute-as-a-service market matures.

This is **the most speculative new input** in the rebuild. Vlad framed: "most of ODC will feed into AI stack internally, and some will be sold to customer." The Base Case curve reflects "most" interpretation; the MC range is wide. Confirm trajectory or push back.

### §6.3 AI Stack product ramps (Cursor / Grok consumer / Grok enterprise)

Per §7 AI Stack. Stub trajectories:
- Cursor: 1M seats 2025 → 50M by 2035
- Grok consumer: 2M paid subs 2025 → 80M by 2035
- Grok enterprise API: 1T tokens 2025 → 200T by 2035 (dampened from raw stub — original 1000T-by-2035 implied $800B revenue in 2030, implausibly large share of inference market)

Each is a Mach33-thesis-call ramp. The 2025 anchors are essentially zero (these products are early-ramp); the trajectory shape is the bet. Confirm or override.

### §6.4 Mars 2050 Starship slots (resolved as derived, but the carve-out cash sizes it)

V30.5 had R288 = 20,000 Mars slots in 2050 — way above any anchor. In the rebuild, Mars slots are DERIVED from carve-out cash / per-ship cost (not an input). So the 20K number disappears. But the underlying question — how aggressive is Mars by 2050? — is now answered by the carve-out % and growth in prior-year FCF.

At Base Case 15% carve-out and ~$200B Group FCF by 2050, Mars carve-out ≈ $30B/yr in 2050. At $50M per Mars ship × 5 depot multiplier = $300M per surface-landing ship → ~100 surface ships landed in 2050. Plus depot ships → ~600 total Mars launches in 2050. Far less than 20K. **More defensible.**

If you want closer to the 20K scenario, that requires either a much higher Mars carve-out % (45%+) or a different mechanic (e.g., cash sweep into Mars when terrestrial IRR saturates). Sprint 10 / 11 audit can re-examine.

### §6.5 Starship customer launch price trajectory

V30.5 R196: $100M in 2027, -8%/yr decline. Build plan continues this trajectory. Q4'25 R133 has Starship at $240M in 2024 / $266M in 2025 — but those are pre-commercialization synthetic numbers (no actual Starship customer launches yet).

Once Starship goes commercial in 2027, market pricing is unknown. $100M start is bold — current commercial heavy-lift (Ariane 6, Vulcan) sits at $80-150M. Confirm $100M / 8% decline as Base Case, or adjust.

---

## §7 — How Sprint 0 plugin executes against this

Step-by-step:

1. **Plugin reads `04_Assumptions_Tab_Build_Plan.xlsx`** — walks rows top to bottom.
2. **Creates Assumptions tab** on the new workbook (`SpaceX Model V31_rebuild.xlsx` or similar — plugin picks file name).
3. **Writes year header at row 4** (D=2025, E=2026, ..., AC=2050) and year-offset helper at row 5 (D=0, E=1, ..., AC=25). Both as hardcoded integers.
4. **For each section header row** in the build plan: write section header text at column A, apply white-on-charcoal formatting. Skip rows for spacing if needed.
5. **For each subsection header row**: write italic header at column A, apply light grey fill.
6. **For each input row**:
   - Write column-A label
   - If `Base Case` value present: write to column B
   - Write notes to column C
   - If year-row values present (cols D–AC): write each year value to corresponding column
   - Write MC Min to AG, MC Max to AH, MC Distribution to AI, MC Notes to AJ
   - Apply MC-flag highlight to the row (light yellow fill on cols AG–AJ if MC range is non-fixed)
7. **Apply section pastel fills** so inputs are visually grouped.
8. **Sets year header + year-offset helper rows on every OTHER tab** (Allocator, all module tabs, Starlink Capacity, OpEx, CapEx, Valuation, Group P&L) — pre-stages even before those tabs have content. Per Architecture §2.
9. **Verification per Sprint Roadmap §6.X**: read back Base Case values for the key 2025 anchors (starting cash $5B, F9 fleet 28, F9 price $111M, Mars/Moon R&D $700M, Starshield decay 0.25, Starshield rev/Gbps $164,699). Halt if any mismatch.
10. **Append Sprint 0 row to Claude Log** with summary.

Plugin's call on whether to write year-row pre-computed values (per the build plan XLSX) as static numbers, or write the underlying parameters (start, end, CAGR) and let Excel compute. Static numbers are recommended — simpler, no formula drift, inspectable.

---

## §8 — What changes from V30.5 to the rebuild Assumptions tab

For reference, the deltas vs V30.5:

**Dropped (37 stale + 10 decorative rows from V30.5):**
- All Sprint 5 sigmoid inputs (floor unit, initial IRR seeds, AI Stack switch, hardcoded capital pool $15B/20%)
- All Sprint 5.5 corporate overhead inputs (group rate, module multipliers)
- All Sprint 5.6 historical capital base inputs (no per-sat IRR seeding)
- Sprint 6 toggles (Compute tier split method, idle capital recycle)
- Sprint 7 Layer 3 inputs (maintenance threshold, destination split, FCF floor method)
- Legacy Allocator IN/OUT block (R10-R21 in V30.5)
- ODC R247 sat deployment STUB year-row (cash-driven now)
- Lunar Mars R287/R288 slot year-rows (derived from carve-out cash)
- Module-level R&D/SG&A inputs that lived on module tabs (now lives on OpEx tab)

**Added (NEW for rebuild architecture):**
- ODC internal compute share to AI Stack year-row (Vlad's "AI Stack sits on top of ODC" reframe)
- ODC external compute share to customers year-row (derived)
- AI Stack standalone module inputs (Cursor seats + ARPU, Grok consumer subs + ARPU, Grok enterprise API tokens + price)
- Lunar share of carve-out cash year-row
- Mars share of carve-out cash year-row
- MC range columns (Min, Max, Distribution) for every input

**Corrected (Q4'25 anchors applied):**
- Starting cash $20B → $5B (Q4'25 Earth R225)
- Starshield decay rate 1.0 → 0.25 (Q4'25 Valuation Inputs R30)
- Starshield Rev/Gbps $167,421 → $164,699 (Q4'25 Earth R120)
- F9 starting fleet 24 → 28 (Q4'25 Earth R29)
- F9 customer launch price $67M → $111M (Q4'25 Earth R132)
- Mars/Moon R&D 2025 $500M → $700M (Q4'25 Earth R174)

**Kept identical (Q4'25 confirms or Vlad-locked):**
- Satellite Cost per kg $650 base
- V2 Mini Mass 575 kg, BB Gbps 96
- Cumulative sats base year 7,486
- V2 BB/DTC active end-2025 5,246 / 650 (Mach33 hard anchors)
- ODC compute power per sat 140 kW (V30.5 V2 Compute config, Vlad-confirmed)
- All Wright's Law parameters, depreciation rates, lifespan inputs
- All Lunar Mars BV engine inputs (labour units + hardware methodology)
- IPO injection $30B / 2027

---

## §9 — Calibration targets (re-stated for reference)

From Sprint Roadmap §6 + 2025 Anchors doc. Every sprint's verification gate checks these.

| 2025 output | Target | Tolerance |
|---|---|---|
| Group Revenue | $14,650mm | ±5% |
| Group EBITDA | $8,690mm (59.3% margin) | ±5% |
| Group FCF | $3,670mm | ±10% |
| F9 launches (total) | 171 | ±5 |
| F9 customer launches | 38.58 | ±2 |
| Starship launches | 0 | exact |
| Starlink + DTC revenue | $7,852mm | ±5% |
| of which DTC | $156.91mm (~2% of Starlink+DTC) | ±15% |
| Starshield revenue | $2,520mm | ±5% |
| Customer Launch revenue | $4,290mm | ±5% |
| ODC revenue | $0 | exact |
| AI Stack revenue | $0 (or small early-ramp) | ±$500M |
| Lunar Mars revenue | $0 | exact |
| Active sats end-2025 | ~9,800 (V2 + V1/V1.5 residual) | ±5% |
| Implied EV (10× rev) | $111B | ±5% |

---

## §10 — Amendment log

- **2026-05-19 (initial draft)** — Constitutional doc 4 of 4. Pairs with `04_Assumptions_Tab_Build_Plan.xlsx` (300 rows, 11 sections). All 6 Q4'25 corrections applied. All stale/decorative V30.5 rows dropped (37 + 10 = 47 rows removed). 6 new AI-Stack-on-ODC architecture inputs added. ODC R247 stub dropped (cash-driven). Lunar Mars slot year-rows dropped (carve-out-derived). MC range columns populated for every input. Ready for plugin Sprint 0 execution.
