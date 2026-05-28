# SpaceX S-1 Historicals Import — Parallel Build Plan

**Filed:** 2026-05-20
**Track:** Separate chat, parallel to main rebuild — no Sprint roadmap dependency
**Lead deliverable:** Standalone workbook with a variance/reconciliation tab against current Q4'25 anchors
**Merge into main model:** Future sprint, scoped after variance work stabilises

---

## Why this is a big deal

The S-1 is the first audited financial disclosure SpaceX has ever published. Every input that was sourced from management commentary, secondary press, or backed-into estimates can now be calibrated against audited primary source — including the figure we've been chasing for years (Starlink vs Launch revenue split, audited).

## What's typically in an S-1 / EDGAR filing

Since you flagged you're newer to public-markets disclosure, here's the full menu. Tiered by model relevance.

**Tier 1 — directly recalibrates model inputs:**

- **Audited income statement** (3 prior fiscal years — FY2023, FY2024, FY2025): Revenue, COGS, Gross Profit, OpEx (R&D, S&M, G&A), EBIT, Interest, Tax, Net Income.
- **Segment reporting** (in financial statement notes): Starlink vs Launch vs Other, with segment revenue and segment profit. First audited Starlink standalone.
- **Cash flow statement** (3 years): CapEx, D&A, working capital, FCF. Anchors module CapEx and D&A directly.
- **Balance sheet** (2 years): Cash, PP&E (constellation + vehicles), intangibles, debt.
- **Debt schedule** (notes): Each tranche — term loans, senior notes, revolver. Principal, rate, maturity, covenants. Drives EV→equity bridge and interest expense forecast.
- **Capitalisation table**: Share classes (likely dual-class with super-voting Elon shares), share count, IPO proceeds. Drives per-share valuation.
- **D&A schedule** (notes): Useful lives by asset class. This is the source-of-truth for Sprint 4.5's Constellation D&A $437M vs $707M gap.

**Tier 2 — high-value calibration:**

- **Customer concentration** (notes): NASA, USSF, DoD as % of Launch revenue.
- **Backlog / contracted revenue** (notes or MD&A): Forward-booked Launch and Starlink government contracts.
- **Stock-based compensation** (notes): Large at IPO. Affects EBITDA→FCF bridge.
- **Lease obligations** (notes): Starbase, Hawthorne, ground stations.
- **Related-party transactions** (notes): Starlink ↔ Launch intercompany pricing — directly calibrates our internal launch transfer assumption (and per-sat IRR queue).
- **Geographic revenue mix**: Starlink US vs ROW.
- **Operational KPIs in MD&A**: Subscriber count, ARPU, launch cadence, sat count delivered. Sometimes disclosed for narrative, sometimes not.
- **Headcount**.

**Tier 3 — interesting, not load-bearing for the model:**

Risk factors, executive compensation, principal stockholders, legal proceedings, underwriter list, use-of-proceeds narrative, properties section.

## Workbook structure

One tab per disclosure block. Every cell carries a source comment with S-1 page reference.

| Tab | Contents |
|---|---|
| `00_README` | Filing date, version, link to SEC EDGAR doc, methodology note |
| `01_P&L` | 3-year audited income statement + segment breakdown |
| `02_BS` | 2-year balance sheet |
| `03_CF` | 3-year cash flow statement |
| `04_CapEx_Detail` | CapEx by asset class (constellation, vehicles, facilities, ground) |
| `05_DnA_Schedule` | Useful lives + D&A by asset class |
| `06_Debt_Schedule` | Each tranche: principal, rate, maturity, covenants |
| `07_Cap_Table` | Share classes, counts, IPO terms |
| `08_Customer_Concentration` | Top-customer disclosure |
| `09_Backlog` | Contracted forward revenue |
| `10_Related_Party` | Intercompany (Starlink ↔ Launch, plus other Musk-co transactions) |
| `11_Operational_KPIs` | Sub count, ARPU, launches, sats delivered — whatever MD&A surfaces |
| `12_Variance_vs_Anchors` | The reconciliation tab |

## Variance / reconciliation methodology (Tab 12)

Side-by-side layout:

| Metric | 2023 anchor | 2023 S-1 | Δ | 2024 anchor | 2024 S-1 | Δ | 2025 anchor | 2025 S-1 | Δ | Notes |

Pulls anchors from current `project_anchored_assumptions_2025.md` and V30.5 / Q4'25 source files. Every non-trivial delta becomes a follow-on action: either correct the anchor file or document why the S-1 figure can't be used directly (e.g., different consolidation scope, post-period adjustment, segment mapping mismatch).

S-1 audited numbers override anchors as canonical. Anchors get updated after Tab 12 stabilises.

## Debt → Valuation workstream (priority lift)

This is the highest-leverage extraction in the entire S-1 because SpaceX has never publicly disclosed debt structure. The Tab 06 debt schedule isn't just another input — it's a discrete workstream that feeds the valuation engine.

**Extract (Tab 06):** Every tranche from financial-statement notes: principal, coupon/rate, maturity date, security (secured vs unsecured), covenants (financial maintenance + negative covenants), prepayment / call features, original issuance date, any embedded options or PIK features.

**Build (Tab 06 continued):** Forward amortisation schedule by tranche → annual principal repayments + interest expense (years 2026–2050, matching the workbook horizon `D:AC` per [[project-year-horizon]]). Refinancing assumption stated explicitly per tranche (roll at maturity at then-prevailing rate? pay down with FCF? amend & extend?).

**Feed three downstream consumers:**

1. **Main P&L interest line** — replaces inferred interest expense in the main rebuild model. Affects net income and tax shield.
2. **EV → Equity bridge** — net debt at any forecast date = gross debt schedule minus modelled cash balance. This was previously a guess; now it's anchored.
3. **WACC / cost of capital** — implied pre-tax cost of debt from the weighted-average coupon, plus credit-spread benchmark for any refinancing rate assumption. Feeds the discount rate used in DCF/IRR.

**Triangulation check (new today):** Once IPO prices, observable equity value + audited debt = observable enterprise value. That's a calibration target for our DCF/IRR engine — first time we've had one. If our terminal-year EV implies a number wildly off the IPO-derived EV, that's a thesis-disconfirming signal worth investigating before publication.

## Output: Integration spec for main rebuild

The parallel build produces three deliverables:

1. **The historicals workbook** (tabs 00–12) — standalone reference, source-of-truth for every audited 2023–2025 figure.
2. **The debt → valuation tab** (Tab 06 extended) — forward schedule ready to plug into main-model interest + net debt lines.
3. **An integration spec** — sprint-style document the main rebuild chat runs as a future sprint. Tells the main workbook exactly what to override, where, with what formula change, and what variance to expect against pre-merge anchors.

The integration spec is the bridge between the parallel build and the main rebuild. It uses the same Rule Compliance Preamble and execution rules ([[reference-execution-rules]]) the main sprints use. Vlad runs it against the main workbook in a future kickoff. It does not name workbook files per [[feedback-no-workbook-names-in-specs]].

## Immediate calibration impact — flag forward

1. **Sprint 4.5 Constellation D&A** ($437M actual vs $707M target): D&A schedule from S-1 notes resolves this. Once extracted, drop into Sprint 4.5 spec as the authoritative calibration target.
2. **Anchored 2025 assumptions**: Expect wholesale re-anchor once Tab 12 work completes. `project_anchored_assumptions_2025.md` should be rewritten, not patched.
3. **Intercompany transfer pricing** (Starlink launches on Falcon): Related-party note may give the first audited number for what Launch charges Starlink internally — directly affects per-sat IRR queue economics and the allocator OUT contract.
4. **Vending-machine module P&L mapping**: SpaceX's segment reporting probably won't map cleanly to our modules (Starlink, Launch, ODC-future, AI Stack-future). Build a Tab-12 cross-reference between SpaceX-disclosed segments and Mach33 modules.

## Kickoff protocol for the separate chat

Day 1 of the parallel-build chat should:

1. **Source the filing.** Pull the S-1 from SEC EDGAR (search "Space Exploration Technologies Corp" on edgar.sec.gov). Save full PDF + extract financial-statement pages to `/Starlink Module/S1_Source/`.
2. **Build the empty workbook scaffold first** (tabs 00–12) before any data entry. Prevents structure-drift mid-extraction.
3. **Page-reference every input.** Every cell gets a comment with S-1 page number. No exceptions. This is the only way variance investigations stay tractable.
4. **Read the mach33-model-build skill** for the Rule Compliance Preamble. Even though this isn't a sprint, the execution rules (anchor-and-offset, INDEX/MATCH by label, no OFFSET, stale-ref scan) apply.
5. **Variance tab last.** Don't start Tab 12 until all source data is in tabs 01–11. Otherwise we're reconciling against a moving target.

## Open questions for the parallel chat

- Does SpaceX file as an EGC (Emerging Growth Company)? If yes, they can disclose only 2 years of audited P&L rather than 3 — affects how much history we can pull.
- What's the segment-reporting breakdown? Two segments (Starlink / Launch) is the optimistic case; one-segment ("Space technology") would be a disclosure black-out and forces us back on inference for the split.
- Is there a non-GAAP "Contribution Margin" or "Adjusted EBITDA" measure with bridge? If yes, lift the definition into the workbook — useful for bull/bear thesis prose.
- Pro-forma adjustments: Has any post-period restructuring (Starlink subsidiary spin, etc.) been done? S-1 will disclose under "Subsequent Events".
- Is Starshield broken out, or rolled into Launch / Other? National-security customer concentration disclosure depends on this.

## Out of scope for this build

- No edits to the main rebuild workbook. Tab 12 is the merge point; merging into the main model is a future sprint.
- No update to Sprint 4.5 / Sprint 5 deliverables. Parallel track.
- No public-output deliverables (weekly analysis, X post on the IPO). Separate workstream — would use mach33-weekly-analysis / mach33-x-post.
