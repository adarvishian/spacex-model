# Frontend PRD — Audit Mode Readability & UX Overhaul

**Document version:** 1.0
**Date:** 2026-06-05
**Author:** Dr. Marcus Hale (port lead)
**Status:** Draft for review.
**Scope:** Audit Mode only (`/audit/*`). Client Mode is explicitly out of scope for this document.

**Companion documents (read order):**

1. `role.md` — operating persona.
2. `docs/FRONTEND_PRD.md` — the v1.5 frontend spec this document audits against. Section numbers below (e.g. "FE-PRD §1.4") refer to that file.
3. `frontend/src/app/AuditApp.tsx`, `frontend/src/audit/Grid.tsx`, `frontend/src/audit/DerivationPanel.tsx`, `frontend/src/shared/format.ts` — the v1 implementation this PRD proposes to change.
4. `frontend/src/styles.css`, `frontend/src/styles/tokens.css`, `frontend/src/styles/grid.css` — the styling system to be consolidated.

---

## §1 — Purpose & Scope

### §1.1 Purpose

The shipped Audit Mode is functional but does not yet meet the readability and usability bar required by its own success criteria (FE-PRD §1.4). An auditor cannot reliably *read the numbers* in the grid, and cannot reliably *verify a value by clicking one cell* — the two things Audit Mode exists to do. This PRD specifies a full UX overhaul of Audit Mode: a consolidated visual system, a legible data grid, a trustworthy derivation experience, honest loading/feedback, and accessibility.

This is not a feature-expansion PRD. Every requirement below either fixes something currently broken or makes an existing surface usable. New capability is limited to what is needed to make the existing capability legible.

### §1.2 Methodology

Findings were gathered two ways and cross-checked:

- **Live inspection** of the production deployment (`spacex-model`, Vercel, deployment `dpl_FWoUZmkNt61fj4SbRo4wKgDBUrKU`, build `9fcf9a43`) on 2026-06-05: Starlink grid, Group P&L grid, the derivation rail on two cells, and the Run Audit tab.
- **Source review** of the components and stylesheets listed above, to attribute each observed symptom to a concrete root cause.

Every finding below carries an *Observed* (what the screen does), a *Root cause* (where in the code), a *Requirement* (what to change), and an *Acceptance* (how we know it's fixed).

### §1.3 In scope

Audit Mode data grid, derivation panel, dependency graph, sources & change-history rail, Run Audit tab, sheet navigation, global loading/feedback, the Audit Mode visual/design-token system, and accessibility of all of the above.

### §1.4 Out of scope

- Client Mode (`/client/*`) — separate effort.
- Backend model logic and numerical reconciliation (except where the *contract* the UI consumes must change, e.g. cell `unit` metadata and `computed_value` for stub cells — flagged as API asks, not model changes).
- New audit capabilities beyond those in FE-PRD (no cell editing, no multi-user, no version comparison).

### §1.5 Success criteria

1. **Legibility.** Every numeric cell in every sheet displays its full value at default zoom with no truncation/ellipsis, in the correct unit. (Fixes the central failure.)
2. **One-click verification.** Clicking any *derived* cell populates Formula, Computed value, and at least one Resolved input — or, for a *stub* cell, says so explicitly instead of rendering an empty "= $mm". (FE-PRD §1.4.1.)
3. **Instant base case, honest feedback elsewhere.** Opening Audit Mode on the base case shows real numbers immediately, from a precomputed run shipped at deploy time — no solver wait. For any other scenario/override, there is no blank screen during the ~40 s solver run; the user always sees progress and an ETA, and the grid and Run Audit tab never silently show nothing.
4. **One visual system.** A single set of design tokens governs all Audit Mode color, type, and spacing; the duplicate/conflicting token definitions are removed.
5. **Accessibility.** Audit Mode meets WCAG 2.1 AA contrast, is fully keyboard-operable, and never uses color as the sole signal.

---

## §2 — Findings Summary

| # | Finding | Severity | Area |
|---|---|---|---|
| F1 | Numeric values truncate to ellipsis ("228…", "202…", "48,422" overflow) — numbers unreadable | **Critical** | Grid |
| F2 | Derivation "Computed" shows "= $mm" with no value; "Formula" is a label restatement; no resolved inputs — for many cells | **Critical** | Derivation |
| F3 | ~40 s blank grid on load and on every scenario change, with zero feedback | **Critical** | Feedback |
| F4 | Wrong units: binary 1/0 flags and some $mm rows render as percentages ("100.0%", "51.9%") | High | Grid / data contract |
| F5 | Row labels truncate with no tooltip or wrap ("Starlink BB Revenue from curve…") | High | Grid |
| F6 | Grid value and derivation value disagree (grid shows 3,325; derivation says no computed value) | High | Trust / consistency |
| F7 | Run Audit re-runs the full solver (~40 s) on entry; static "Loading run audit…" only | High | Feedback |
| F8 | Two conflicting `:root` design-token systems (`tokens.css` vs `styles.css`) | High | Design system |
| F9 | Empty-state rail shows three redundant "Select a cell…" prompts; wasted space | Medium | Layout |
| F10 | Title bar crams title + dimensions + keyboard hints + legend into one cramped row | Medium | Layout |
| F11 | Run Audit calibration status uses ambiguous red "CHECK" word vs green ✓ icon | Medium | Run Audit |
| F12 | Dark-only theme; recurring contrast firefighting in git history (no light mode) | Medium | Design system / a11y |
| F13 | Dependency graph frequently renders a single node with no edges | Medium | Derivation |
| F14 | No column resize-to-fit, no density control, no number-format toggle ($mm vs $B) | Medium | Grid |

Severity key: **Critical** = blocks the core job; High = materially impairs it; Medium = friction or polish.

---

## §3 — Detailed Findings & Requirements

### §3.1 Data legibility in the grid (F1, F4, F5, F14)

**F1 — Numeric truncation.**
*Observed:* On Starlink, R22 "Starship operational year" renders `202…`, R24 "F9 payload per launch (kg)" renders `228…`, R25 renders `100…`/`114…`/`131…`. On Group P&L, R25–R27 gross-profit rows render `659…`/`238…`/`483.…`. Even a four-character year is clipped. Values are simply unreadable.
*Root cause:* `Grid.tsx` sets every year column to a fixed `width: 72` and never autosizes to content; `formatGridNumber` (in `format.ts`) emits unscaled `toLocaleString` strings (e.g. `48,422`) that overflow 72 px at the 11.5 px grid font. Columns are technically `resizable`, but nothing fits them on load.
*Requirement:*
- Year columns must size to fit their formatted contents on data load (AG Grid `autoSizeColumns` / `sizeColumnsToFit` with a sensible min width), and re-fit on sheet change.
- Provide a number-format control (per §3.1 F14) so large `$mm` values can be shown as `$B` to stay compact.
- As a floor, no cell may ever show an ellipsis at default zoom for the default scenario on any sheet.
*Acceptance:* Load each of the 13 data sheets; assert (Playwright) that no `.ag-cell` in the viewport contains a trailing `…` and that `scrollWidth <= clientWidth` for every rendered numeric cell.

**F4 — Wrong units.**
*Observed:* R28 "V2 launch window active (1/0)" and R29 "V3 deployment active (1/0)" render as `100.0%` / `0.0%`; on Group P&L, R34 "Module OpEx: AI - Compute" renders `51.9%` where a `$mm` value is expected; inter-module elimination rows render `0.0%`.
*Root cause:* `formatGridNumber`/`formatCellValue` branch on `unit`; rows whose `unit` is `pct`/`ratio` multiply by 100. Binary flag rows and certain `$mm` rows carry the wrong `unit` in the grid payload, so a flag value of `1` becomes `100.0%`.
*Requirement:*
- Introduce an explicit `flag`/`boolean` unit (rendered `1`/`0` or `Yes`/`No`, never as a percentage).
- Correct the `unit` metadata on the affected rows in the grid payload (**API ask** — `GET /api/sheets/{sheet}/grid`); the frontend must render exactly the unit it is given and never infer.
- Add a frontend guard: a `ratio`/`pct` value whose magnitude is implausible as a percentage is shown raw with a `⚠` affordance rather than silently `×100`.
*Acceptance:* Flag rows render `1`/`0`; no `$mm` row renders a `%`; a unit-coverage test asserts every row's `unit` is in the allowed enum.

**F5 — Label truncation.**
*Observed:* `Starlink module — real cohorts …`, `Starlink BB Revenue from curve…`, `Starlink module allocated cash …` all clip.
*Root cause:* `Grid.tsx` label column is fixed `width: 260` with no `tooltipField` and no wrap.
*Requirement:* The label column must (a) carry a native tooltip with the full label, and (b) either autosize to a wider cap or wrap to two lines with increased row height. The full label must also always be visible in the derivation panel address strip.
*Acceptance:* Hovering any clipped label shows the full text; the derivation panel always shows the untruncated label.

**F14 — Grid controls.**
*Requirement:* Add a compact grid toolbar with: number format toggle (`$mm` ↔ `$B` ↔ raw), density toggle (comfortable/compact row height), and "fit columns" / "reset widths". Persist choices in `localStorage` per FE-PRD's stated persistence pattern.
*Acceptance:* Toggling format re-renders all numeric cells; preference survives reload.

### §3.2 Derivation trust & completeness (F2, F6, F13)

**F2 — Empty derivation.**
*Observed:* Clicking Starlink R11 (`9,348` on screen) shows Formula = "Starlink BB Revenue from curve ($mm) — see Architecture §8…", **Computed = "= $mm"** (no number), and "No resolved inputs for this cell." Group P&L R11 behaves identically. The cell `type` reads `stub (year-row)`.
*Root cause:* For stub cells the lineage endpoint returns `computed_value: null` and a placeholder `formula_expression`. `DerivationPanel.tsx` renders `= {formatGridNumber(null, …)}` — which is `""` — then unconditionally appends the `$mm` suffix, producing the misleading `"= $mm"`.
*Requirement:*
- When `computed_value == null`, the Computed box must not render `"= $mm"`. It must render an explicit state: e.g. "No computed value — this cell is a **stub** (not yet ported to a traced derivation). Spec: §8 Starlink module."
- The panel must visually separate "derivation available" from "stub / placeholder" so an auditor instantly knows whether a cell is verifiable.
- For non-stub derived cells, Formula must be the architecture-spec expression and Resolved inputs must be non-empty (**API ask** — these are populated upstream; the UI must surface them when present and degrade honestly when not).
*Acceptance:* No cell ever shows `"= $mm"` as a value; stub cells show the explicit stub state; for a sampled set of known-derived cells (e.g. Group P&L Group Revenue), Formula and ≥1 Resolved input render.

**F6 — Grid/derivation disagreement.**
*Observed:* The grid shows `3,325` for Group P&L R11/2026; the derivation panel for the same cell shows no computed value. Two surfaces disagree about the same cell.
*Root cause:* The grid value comes from `GridPayload.year_values`; the derivation `computed_value` comes from a separate `/api/lineage/{key}` call that is `null` for stubs. Nothing reconciles them.
*Requirement:* The derivation panel must show the grid's displayed value as the authoritative cell value, and clearly distinguish "displayed value" from "traced/recomputed value" when the latter is absent. An auditor must never be left thinking the value is missing when the grid shows one.
*Acceptance:* For any cell, the value shown in the grid and the value shown in the derivation header are identical or explicitly reconciled in copy.

**F13 — Empty dependency graph.**
*Observed:* The depth-2 dependency graph routinely renders only the active node with no edges (Starlink R11, Group P&L R11).
*Root cause:* Stub cells have empty `upstream_keys`/`resolved_inputs`, so there is nothing to draw.
*Requirement:* When there is no upstream, show an explicit empty state ("No upstream dependencies traced for this cell") rather than a lone node in a large empty canvas; reclaim that vertical space for the populated panels.
*Acceptance:* Cells with no upstream show the empty-state message and do not reserve the full 200 px canvas.

### §3.3 Loading & feedback (F3, F7)

**F3 — Blank grid on load.**
*Observed:* On `/audit` load and on every scenario change, the center pane is solid black for ~40 s with no spinner, skeleton, progress, or ETA. (Confirmed live: ~40 s to first paint.)
*Root cause:* `AuditApp.tsx` auto-runs `runDeterministic` on mount and on scenario change; the "Loading grid…" text only renders when `gridQ.isLoading`, but during the deterministic run `runId` is still `null` and `gridQ` is disabled, so nothing renders. The serverless solver legitimately takes ~40 s (documented in deploy history: "surface the expected ~60s serverless wait").

*Requirement — the base case is precomputed and shipped, so numbers are on screen at open (primary).*
- **Precompute the base-case run at build/deploy time** and ship the result as a static artifact (the grid payloads for every sheet + the base-case lineage/Run Audit payloads). The build step runs the deterministic base-case solve once during `npm run build` / the deploy pipeline and writes the output (e.g. `frontend/src/data/base_case_run.json` or a `public/` asset keyed by build `git_sha`).
- **On `/audit` open with the default (base) scenario, the grid hydrates synchronously from this precomputed artifact** — no solver call, no spinner, numbers visible on first paint. The app may still kick off a live `runDeterministic` in the background to obtain a fresh `runId`/Run Audit, but it must not block or blank the already-rendered grid; when the fresh run returns it reconciles silently (and only visibly updates if values differ).
- Invalidate the precomputed artifact by build `git_sha`: a new deploy regenerates it, so it never drifts from the model. If the artifact is missing/stale for the current `git_sha`, fall back to the live-run path below.

*Requirement — graceful feedback for everything that is NOT the precomputed base case (fallback).*
- For non-base scenarios, custom overrides, or a cache miss, show a determinate-feeling progress experience during the run: a skeleton grid plus a status line ("Running {scenario} — solver converging, ~40 s on first run") and, if the backend can stream iteration/elapsed, a progress indicator.
- Cache live results client-side keyed by `(scenario, overrides)` so re-selecting a scenario is instant (FE-PRD §8.4 names React Query for this; ensure the auto-run path uses the cache instead of always re-running).
- Provide a visible "precomputed", "cached", or "freshly run" indicator next to the run id so an auditor always knows the provenance of what they're looking at.

*Acceptance:* Opening `/audit` on the base case paints the grid with real numbers in < 1 s with no solver round-trip (verified by a Playwright assertion that numeric cells are present before any `runDeterministic` network response). For non-base scenarios there is no blank/black pane — only the skeleton-plus-progress state — and re-selecting a previously run scenario paints from cache in < 500 ms. A provenance indicator (precomputed/cached/fresh) is always visible.

**F7 — Run Audit re-run.**
*Observed:* Opening Run Audit triggers another full ~40 s solver run, showing only static "Loading run audit…". (Confirmed live.)
*Root cause:* `RunAuditTab` fetches its own run rather than reusing the current `runId`'s audit payload.
*Requirement:* Reuse the active run's audit artifacts where possible; if a dedicated audit run is required, share the §3.3 progress experience (skeleton + status + ETA), not a bare text line.
*Acceptance:* Navigating to Run Audit for an already-computed run does not re-run the solver; when a run is genuinely needed, the progress experience matches the grid's.

### §3.4 Visual system & contrast (F8, F12)

**F8 — Conflicting token systems.**
*Observed/Root cause:* Two `:root` blocks define overlapping variables with different values — `tokens.css` (`--bg: #0f1115`, `--border: #262b3a`, `--muted: #8a93a8`, `--text: #e6e9f2`) and `styles.css` (`--bg: #0b0f14`, `--border: #2a3544`, `--muted: #8b98a8`, `--text: #e8edf4`, plus `--accent`, `--surface`). Components reference both vocabularies (`--panel`/`--indigo` vs `--surface`/`--accent`), and many rules hard-code fallbacks (`var(--panel, #161922)`). This is the structural reason contrast keeps regressing (git log shows repeated "fix audit grid contrast", "fix label column text contrast", "light text on dark cells").
*Requirement:* Consolidate to **one** token file as the single source of truth for Audit Mode: one palette (background/surface/border/text/muted/accent/state colors), one type scale, one spacing scale. Remove duplicate `:root` declarations and inline color fallbacks; every component reads named tokens only. AG Grid theme variables in `grid.css` must map to the same tokens (no `#0d0f15`/`#11141c` literals).
*Acceptance:* A lint/grep check passes with zero hard-coded hex colors in component CSS outside the single token file; the duplicate `:root` block is gone.

**F12 — Theme & contrast.**
*Requirement:* Establish documented contrast minimums (WCAG AA: ≥ 4.5:1 body text, ≥ 3:1 large text/UI) and verify the consolidated palette against them — in particular muted text on panels, row-id cells, and the green/amber/red state colors on their backgrounds. A light theme is desirable but **deferred to a fast-follow**; the consolidated token system must be structured so a light theme is a token swap, not a rewrite.
*Acceptance:* Automated contrast check (e.g. axe) reports no AA contrast violations on the grid, derivation rail, and Run Audit tab.

### §3.5 Layout & information architecture (F9, F10)

**F9 — Redundant empty states.**
*Observed:* With no cell selected, the right rail stacks three separate prompts: "Click a grid cell to inspect its derivation.", "Select a cell to view sources.", "Select a cell to view change history." — three messages saying the same thing, filling the rail with whitespace.
*Root cause:* Each panel (`DerivationPanel`, `SourcesPanel`, `ChangeHistoryList`) renders its own empty state independently.
*Requirement:* A single, well-designed rail empty state with a short instruction and, ideally, a hint of what selecting a cell reveals (a thumbnail of the populated layout, or a one-line "shows formula, inputs, dependency graph, sources & history").
*Acceptance:* At most one empty-state message in the rail when no cell is selected.

**F10 — Title bar crowding.**
*Observed:* The grid title bar packs sheet name, "166 rows × 16 year-columns" (which wraps), the keyboard-shortcut hint (`↑↓←→ cell · Enter expand · ⌘J upstream · ⌘K search`), and the Input/Derived/Divergence legend into one row; on a 1080-wide capture it wraps awkwardly.
*Requirement:* Reorganize: keep sheet name + dimensions on the left; move the keyboard hints behind a `?` affordance or a help popover; keep the legend but make it the only always-visible secondary element. Nothing in the title bar should wrap at ≥ 1280 px.
*Acceptance:* At 1280 px and 1440 px the title bar is a single non-wrapping row; full shortcut list reachable from the `?`.

### §3.6 Run Audit semantics (F11)

**F11 — Ambiguous status.**
*Observed:* The 2025 calibration table marks failing anchors with a red word **"CHECK"** and passing ones with a green ✓ — an instruction-sounding word for a verdict, and an icon-vs-word inconsistency. (Many anchors currently fail, e.g. Group Revenue target 18,674 vs actual 9,808.1 — so this column is read often.)
*Requirement:* Use a consistent verdict vocabulary: **PASS / FAIL** (or ✓ / ✗) with consistent color *and* glyph, never color alone. "FAIL" replaces the ambiguous "CHECK". Optionally show Δ% against tolerance.
*Acceptance:* Status column uses one PASS/FAIL system with both color and glyph; no cell reads "CHECK".

### §3.7 Accessibility (cross-cutting)

*Requirement:*
- Color is never the sole signal: divergence already pairs amber with a `▲` glyph (good — keep); extend the same rule to calibration status (§3.6), input/derived cells (add a non-color cue or ensure the legend suffices), and lifecycle/state pills.
- Full keyboard operation of grid, rail, dependency graph, and Run Audit (arrow-key cell nav and ⌘K/⌘J already exist in `AuditApp.tsx` — verify and document; ensure the rail and graph are tab-reachable with visible focus).
- Respect `prefers-reduced-motion`; ensure all interactive controls have aria-labels (the grid already sets `role="grid"` and an aria-label — extend to new controls).
*Acceptance:* axe reports no critical violations; a keyboard-only pass can select a cell, read its derivation, jump upstream, search, and open Run Audit.

---

## §4 — Design System Requirements (consolidated)

A single Audit Mode token file must define:

- **Color:** one background, two surface levels, one border, text + muted text, accent (indigo), and state colors (match-green, divergence-amber, fail-red, info-blue) — each verified for AA contrast on its background (§3.4).
- **Type scale:** a small fixed set of sizes (e.g. 11 / 12 / 13 / 14 / 18 px) with tabular-numerics for all numeric cells and panels.
- **Spacing scale:** a single step set (4 / 8 / 12 / 16 / 24) used everywhere; no ad-hoc pixel paddings.
- **Density:** comfortable and compact row heights as tokens, driven by the grid density toggle (§3.1 F14).

The AG Grid theme (`grid.css`) and all components consume these tokens exclusively. No component CSS may hard-code hex colors or inline `var(--x, #hex)` fallbacks.

---

## §5 — Prioritization & Phasing

**Phase 1 — Make the numbers readable, present on open, and honest (highest value, ~1 sprint).**
F3 (precompute & ship base case + load feedback), F1 (autosize/format), F4 (units + flag type), F5 (label tooltip/wrap), F2 (stub-aware derivation), F6 (value reconciliation).

**Phase 2 — Trust the system (~1 sprint).**
F7 (Run Audit reuse + progress), F13 (graph empty state), F11 (PASS/FAIL), F8 (token consolidation), F12 (contrast verification).

**Phase 3 — Polish & controls (~0.5 sprint).**
F14 (grid toolbar: format/density/fit), F9 (single rail empty state), F10 (title bar), §3.7 accessibility pass + axe/keyboard tests in CI.

Rationale: Phase 1 alone removes both Critical legibility failures and the worst feedback gap, restoring the auditor's core loop. Phases 2–3 make it durable and pleasant.

---

## §6 — Sprint Breakdown for a Cursor AI Agent

This section decomposes the work into discrete, sequential sprints sized for an autonomous coding agent (e.g. Cursor). Each sprint is independently shippable behind the existing dev/main flow, lists the exact files to touch, gives numbered tasks, and defines "done when" against the acceptance criteria in §7.

### §6.0 Working agreement (applies to every sprint)

- **Branch per sprint:** `git checkout -b feat/audit-ux-sprintN-<slug>` off `dev`. Open one PR per sprint.
- **Scope discipline:** touch only the files listed for that sprint plus tests. Do not refactor unrelated code.
- **Build & test gates (must pass before PR):**
  - `cd frontend && npm ci && npm run build` (Vite build + `scripts/check-bundle-budget.mjs` gzip budget must stay green).
  - `cd frontend && npm run test:e2e` (Playwright suites in `frontend/e2e/`). Add/extend specs for the sprint's acceptance criteria; use `frontend/e2e/mock-api.ts` so tests do not depend on the ~40 s live solver.
- **Per role.md:** append a dated entry to `docs/DEV_LOG.md` for any material change, noting which acceptance criteria the sprint closes.
- **No backend model-logic changes.** Where a sprint needs data the API doesn't yet provide (units, computed values, precompute artifact), implement the frontend against the contract in §8 and stub/mocked data, and flag the API ask in the PR description. Do not alter `src/spacex_model/` calculation code.
- **Definition of done:** acceptance criteria for the sprint pass in Playwright; build + bundle budget green; DEV_LOG updated; screenshots of before/after attached to the PR.

### §6.1 Sprint 1 — Base case is precomputed and on screen at open (F3, F7)

*Objective:* The grid shows real base-case numbers in < 1 s on `/audit` open, with no solver wait; every non-base path shows a skeleton + progress instead of a blank pane; Run Audit reuses the active run.

*Files:* build/deploy: a new precompute step (recommend a Python script `scripts/precompute_base_case.py` + a pipeline/`package.json` hook) writing `frontend/src/data/base_case_run.json` (or a `public/` asset keyed by `git_sha`). Frontend: `frontend/src/app/AuditApp.tsx`, `frontend/src/audit/RunAuditTab.tsx`, `frontend/src/shared/query-client.ts`, `frontend/src/shared/api.ts`, `frontend/src/audit/Grid.tsx` (skeleton state), `frontend/src/styles.css` (skeleton/progress styles).

*Tasks:*
1. Add a precompute step that runs the deterministic base-case solve once and serializes all sheet grid payloads + base-case lineage + Run Audit payload to a static artifact tagged with the current `git_sha`. Wire it into the deploy pipeline (or `prebuild`) so each deploy regenerates it.
2. In `AuditApp.tsx`, when `sheetSlug` scenario is base and the artifact matches the running `git_sha`, hydrate `embeddedGrids` and the active grid synchronously from the artifact on first render — before any `runDeterministic` call. Kick the live run in the background only to obtain a fresh `runId`; never blank the already-rendered grid; reconcile silently on return.
3. Implement the fallback path: for non-base scenario/overrides or a cache miss, render a skeleton grid + status line (`Running {scenario} — solver converging, ~40 s on first run`); remove the all-black no-indicator state.
4. Cache live results in React Query keyed by `(scenario, overrides)`; ensure scenario re-selection reads cache.
5. Add a provenance indicator near the run id: `precomputed` / `cached` / `fresh`.
6. `RunAuditTab.tsx`: reuse the active run's audit payload (from the artifact for base case, or the current `runId`) instead of triggering a new solve; share the skeleton+progress state when a run is genuinely required.

*Done when:* A4 passes; new Playwright assertions confirm numeric cells are present on base-case open **before** any `runDeterministic` response, and that no black/no-indicator state exists for non-base scenarios.

### §6.2 Sprint 2 — Grid legibility: no truncation, correct units (F1, F4, F5)

*Objective:* Every number and label is fully readable on every sheet, in the correct unit.

*Files:* `frontend/src/audit/Grid.tsx`, `frontend/src/shared/format.ts`, `frontend/src/styles/grid.css`.

*Tasks:*
1. `Grid.tsx`: replace the fixed `width: 72` year columns with autosize-to-content on data load and on sheet change (AG Grid `autoSizeAllColumns` / `sizeColumnsToFit` with a sensible min width); re-fit on sheet switch.
2. Label column: add `tooltipField` for the full label and either widen to a cap or enable two-line wrap with adjusted row height. Ensure the full label always renders in the derivation address strip.
3. `format.ts`: add a `flag`/`boolean` unit rendering `1`/`0` (never `%`); add a guard in the `pct`/`ratio` branch that renders raw + `⚠` when a value's magnitude is implausible as a percentage instead of silently `×100`.
4. Render exactly the `unit` supplied by the payload; never infer. (Unit-metadata correction is the §8 API ask — consume it; mock corrected units in tests.)

*Done when:* A1 passes; Playwright asserts no `.ag-cell` contains a trailing `…` and `scrollWidth <= clientWidth` for numeric cells across all 13 data sheets, flag rows render `1`/`0`, and no `$mm` row renders `%`.

### §6.3 Sprint 3 — Derivation trust & completeness (F2, F6, F13)

*Objective:* Clicking a cell never lies; stub cells say so; the grid value and derivation agree.

*Files:* `frontend/src/audit/DerivationPanel.tsx`, `frontend/src/audit/DependencyGraph.tsx`, `frontend/src/audit/SourcesPanel.tsx`, `frontend/src/shared/format.ts`.

*Tasks:*
1. `DerivationPanel.tsx`: when `computed_value == null`, stop rendering `"= $mm"`. Render an explicit stub state ("No computed value — this cell is a **stub** (not yet ported to a traced derivation). Spec: {section}.") and visually separate "derivation available" from "stub/placeholder".
2. Show the grid's displayed value as the authoritative cell value in the derivation header; clearly distinguish "displayed value" from "traced/recomputed value" when the latter is absent (closes the grid/derivation disagreement).
3. `DependencyGraph.tsx`: render an explicit empty state when there is no upstream and collapse the reserved 200 px canvas so populated panels reclaim the space.
4. For non-stub cells, surface `formula_expression` and `resolved_inputs` when present (consume §8 contract; mock populated cells in tests).

*Done when:* A2 and A3 pass; no cell renders `"= $mm"`; stub cells show the stub state; sampled known-derived cells show a formula and ≥ 1 resolved input.

### §6.4 Sprint 4 — One design system, verified contrast, honest status (F8, F12, F11)

*Objective:* A single token source governs Audit Mode; contrast meets AA; Run Audit verdicts are unambiguous.

*Files:* `frontend/src/styles/tokens.css` (becomes the single source), `frontend/src/styles.css`, `frontend/src/styles/grid.css`, `frontend/src/audit/RunAuditTab.tsx`, any component CSS with inline hex.

*Tasks:*
1. Consolidate all design tokens into one file (color, type scale, spacing scale, density). Delete the duplicate `:root` block and the inline `var(--x, #hex)` fallbacks; map AG Grid theme vars in `grid.css` to the tokens (remove `#0d0f15`/`#11141c` literals).
2. Add a CI grep/lint check that fails on hard-coded hex outside the token file and on a second `:root` token block; wire it next to the bundle-budget check.
3. Verify the consolidated palette against AA (≥ 4.5:1 body, ≥ 3:1 large/UI), especially muted text, row-id cells, and state colors on their backgrounds; adjust tokens to pass. Structure tokens so a future light theme is a swap, not a rewrite.
4. `RunAuditTab.tsx`: replace red "CHECK" with a single PASS/FAIL system using both color **and** glyph (✓ / ✗); optionally show Δ% vs tolerance.

*Done when:* A5, A6, A7 (contrast portion) pass; the CI color check is green; the word "CHECK" no longer appears in the calibration table.

### §6.5 Sprint 5 — Controls, layout, accessibility & test hardening (F14, F9, F10, §3.7)

*Objective:* Polish the surface and lock the gains into CI.

*Files:* `frontend/src/audit/Grid.tsx` (+ a new `GridToolbar.tsx`), `frontend/src/app/AuditApp.tsx`, `frontend/src/audit/DerivationPanel.tsx` / `SourcesPanel.tsx` / `ChangeHistoryList.tsx` (shared empty state), `frontend/src/styles.css`, `frontend/e2e/*`.

*Tasks:*
1. Add a grid toolbar: number-format toggle (`$mm`/`$B`/raw), density toggle (comfortable/compact), and fit/reset columns; persist choices in `localStorage`.
2. Replace the three redundant rail empty states with one well-designed rail empty state.
3. Reorganize the title bar: sheet name + dimensions left; move keyboard hints behind a `?` popover; keep the legend; no wrap at ≥ 1280 px.
4. Accessibility pass: extend "color is never the sole signal" to calibration status and input/derived cells; verify full keyboard operation of grid/rail/graph/Run Audit with visible focus; respect `prefers-reduced-motion`; aria-label all new controls. Add `axe` to the Playwright suite.
5. Add a CI performance/a11y gate (extend `frontend/e2e/performance.spec.ts` + an axe spec).

*Done when:* A7 (full), A8, A9 pass; axe reports no critical/serious violations; bundle budget and performance specs green.

---

## §7 — Acceptance Criteria (consolidated)

A1. On all 13 data sheets at default zoom, no numeric or label cell shows a truncation ellipsis; binary flags render `1`/`0`; no `$mm` row renders a `%`. *(F1, F4, F5)*
A2. No cell's derivation Computed box ever reads `"= $mm"`; stub cells show an explicit stub state; known-derived cells show a formula and ≥ 1 resolved input. *(F2)*
A3. The value in the grid equals the value shown in the derivation header (or the difference is explicitly explained). *(F6)*
A4. There is no app state in which the grid or Run Audit pane is blank/black with no progress indicator; re-selecting a computed scenario paints from cache in < 500 ms. *(F3, F7)*
A5. Run Audit calibration uses a single PASS/FAIL system with both color and glyph; the word "CHECK" no longer appears. *(F11)*
A6. The codebase has exactly one Audit Mode token source; a CI check finds zero hard-coded hex colors in component CSS and zero duplicate `:root` token blocks. *(F8)*
A7. axe reports no critical/serious a11y violations on grid, derivation rail, dependency graph, and Run Audit; a keyboard-only walkthrough completes the core loop. *(§3.7, F12)*
A8. The grid toolbar toggles number format ($mm/$B/raw) and density, fits columns, and persists choices across reload. *(F14)*
A9. The right rail shows at most one empty-state message; the title bar does not wrap at ≥ 1280 px. *(F9, F10)*

---

## §8 — API / Data Contract Asks (not model logic)

These are needed for the UI to be honest; none change the model's numbers:

1. **Correct `unit` metadata** on grid rows, including a `flag`/`boolean` unit for 1/0 rows. *(F4)*
2. **`computed_value` and `resolved_inputs`** populated for ported derived cells; an explicit `cell_kind: "stub"` (already present in the type) reliably set so the UI can branch. *(F2, F13)*
3. A **deterministic, reproducible base-case solve callable from the build/deploy pipeline** so its output can be precomputed and shipped as a static artifact (the grid payloads for all sheets plus base-case lineage and Run Audit payloads), keyed by build `git_sha`. *(F3)*
4. Optional but valuable: a **run progress/status** signal (elapsed, iterations, or a percent) the loading UI can display instead of a guessed ETA, for the non-base (live-run) path. *(F3)*

---

## §9 — Open Questions

1. **Light theme timing.** Deferred here (§3.4 F12) but desirable for client-adjacent reviewers — confirm whether it should be a Phase 3 stretch or a separate effort.
2. **Stub coverage.** What share of cells are currently `stub`? The derivation experience design (F2) depends on whether stubs are the exception or, currently, the rule. A coverage number from the backend would let us decide how prominently to surface "derivation available" filtering.
3. **Precompute mechanics.** Base-case precompute is now a requirement (§3.3 F3). Open detail: should the artifact be generated inside `npm run build` (Node invoking a Python solve) or as a separate deploy-pipeline step that commits/uploads the JSON? Recommend a dedicated pipeline step keyed by `git_sha` to keep the frontend build fast and the solve environment Python-native.
4. **Calibration tolerance display.** Run Audit currently shows many failing anchors; should the table show Δ% against the per-anchor tolerance so reviewers can triage by magnitude (§3.6)?

---

## §10 — Amendment Log

| Date | Author | Change |
|---|---|---|
| 2026-06-05 | Dr. Marcus Hale | v1.0 — initial draft from live inspection of build `9fcf9a43` + source review. |
