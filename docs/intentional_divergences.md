# Intentional Divergences (Type C)

Per PRD §7.6 / context.md §11.6. Code implements constitutional locks the xlsx may not yet reflect.

| Item | Classification | Notes |
|---|---|---|
| V4.113 cached vs Python (R4) | (C) spec-first | Entire model derived first-principles; xlsx is diagnostic reference only |
| CAE allocator F1–F6 (as-is R3) | (C) documented | F4 fixed U0; F1 cap-base fixed U1; F2 fixed U2; F5 fixed U3; F6 R14 fixed U4 in Python; xlsx cached CAE remains diagnostic |
| CAE F6 Conservation R14 (U4) | (C) Python-only fix | Python R14 includes facility flows + bridge/IPO reconciliation; V4.113 cached Conservation R14 still omits ODC facility (diagnostic) |
| CAE F5 seed + debt (U3) | (C) Python-only fix | Python folds ODC into spine (seed + alloc); Terafab repaid via chip transfer; V4.113 cached CAE still bypasses pool R134 (diagnostic) |
| CAE F1 cap-base (U1) | (C) Python-only fix | Python water-fill caps at R64–R66 growth slice; V4.113 cached CAE still uses pre-U1 deploy base (diagnostic) |
| CAE F2 two-resource (U2) | (C) Python-only fix | Python unifies cash+Gigabay in one pass; V4.113 cached CAE still uses independent softmax + pro-rata kg (diagnostic) |
| CAE F4 demand-spine (U0) | (C) Python-only fix | Python unifies R102≡R46; V4.113 cached CAE still shows inflated R99/R102 (diagnostic) |
| Cash Allocation Engine rows | (C) auto-triaged | Four-program two-resource fill diverges from cached CAE softmax/Level-2/pro-rata by design until U3–U4 |
| Group P&L 2025 vs xlsx cached | (C) auto-triaged | S-1 adherence path; full GAAP reconciliation xfails in Block B |
| Module outputs 2026+ | (C) auto-triaged | First-principles derivation on 2025–2040 horizon |
| Sprint 11f Option A (legacy) | (C) preregistered | Superseded by V4.113 CAE map; retained for V2.16 diagnostic runs |
| Starship R&D vs CapEx (D-A-03) | (C) documented | Port capitalizes Starship via vehicle build; S-1 expenses pre-commercialization R&D until 2H 2026. P1-4 adds explicit R&D memo line ($3,004M FY25). |
| Starshield scope (P1-10) | (C) S-1 scope adopted | Port Starshield scaled by `Starshield S-1 Government Connectivity scope factor` (~0.694) to align with S-1 Government Connectivity (~$1.75B) vs port mechanic (~$2.52B). Classified launch revenue remains in Customer Launch, not Starshield. Pending Vlad sign-off for final scope. |

## V4.113 → V4.131 label remaps (Milestone 1.3)

Source of truth: `data/label_remaps/v4_113__v4_131.json` (generated from `scripts/rebase_v4131.py`).

**Resolution (2026-06-10):** The 05c34af calc refactor + full remap application broke solver convergence (residual ≈145, holder `group_fcf`). M1.3 reverted `src/spacex_model/calc/` and `canonical_labels_supplement.py` to `cc78fcf`; legacy V4.113 label strings remain in code because V4.131 workbook rows still match. Flagged/fixed remaps below are **not applied** — queued for owner sign-off before any registry rewrite.

| Bucket | Count | Action |
|---|---:|---|
| Faithful (cosmetic / same dimension) | 32 label + 13 supplement | Safe to apply when calc stack is reconciled |
| Flagged (many-to-one or semantic shift) | 36 label + 11 supplement | Do not apply silently; owner must pick V4.131 intent |
| Fixed (objective unit mismatch) | 1 label + 2 supplement | Block until corrected target label exists |

**High-priority flagged pairs** (see JSON for full list):

| Old label (V4.113) | Proposed V4.131 target | Issue |
|---|---|---|
| `Starlink insurance % of revenue` + `Starlink other COGS % of revenue` | both → `Asset insurance COGS (% of revenue)` | Two inputs collapsed to one row |
| `DTC ARPU ($/sub/mo): year-row` | `Broadband ARPU floor ($/mo)` | DTC pricing vs BB floor |
| `TAM inflation rate (annual)` | `Terminal growth rate g (group + most modules)` | TAM inflation vs terminal value rate |
| `Subsidy mix (% of net adds subsidized)` | `Terminal kits per net subscriber add` | Mix fraction vs kits/sub |
| `Terminal retail price ($, subsidized/non-subsidized)` | both → `Terminal kit cost ($/kit)` | Retail price vs kit cost; two→one |
| `V3 BB/DTC first launch year` + `V2 phase-out year` | all → `V3 Starlink launch trigger year` | Three timing inputs → one |
| `Satellite useful life — V2/V3/V2 DTC/V3 DTC` | all → `Sat operational life L (years)` | Four vehicle lives → one |
| `STARTING_CASH…` / `PRE_IPO_DEBT_FACILITY` | `Minimum cash buffer ($mm)` | Dead remap — `cash_pool.py` uses S-1 hardcoded defaults |

**Fixed (dimensional mismatch — do not apply):**

| Constant / old label | Proposed target | Mismatch |
|---|---|---|
| `F9 booster accounting depreciation cap (flights)` | `F9 booster economic life (years)` | flights → years |
| `ANTHROPIC_COMPUTE_REVENUE_YEAR_ROW` | `External compute 2025 seed (M H100-eq GPU)` | revenue $ → GPU count |
| `ECHOSTAR_MID_BAND_CAPEX_MM_YEAR_ROW` | `Spectrum licence OpEx (% of revenue)` | CapEx $mm/yr → OpEx % |
