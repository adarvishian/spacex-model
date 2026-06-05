# Engineering PRD — Lineage Trust & Monte Carlo

**Document version:** 1.0
**Date:** 2026-06-05
**Author:** Dr. Marcus Hale (port lead)
**Status:** Draft for review.
**Type:** Engineering specification. Every item carries *Observed* (current behavior), *Root cause* (concrete code location), *Requirement* (what to change, incl. API/data-contract changes), and *Acceptance* (how we verify).

**Companion documents (read order):**

1. `role.md` — operating persona.
2. `context.md` — §9 Monte Carlo, §10 Traceability, §11 Reconciliation, §2.4 placeholder tabs.
3. `docs/FRONTEND_PRD.md` — v1.5 frontend spec; §6.3 (change history), §6.4 (lineage enrichment).
4. `docs/FRONTEND_UX_PRD_2026-06-05.md` — Audit Mode overhaul; this PRD references its findings (esp. F2, F6).

**Primary code under change:**

- Backend: `src/spacex_model/service/lineage_enrich.py`, `src/spacex_model/service/lineage_history.py`, `src/spacex_model/service/api.py`, `src/spacex_model/service/grid.py`, `src/spacex_model/engine/label_lookup.py`, `src/spacex_model/io/excel_ingest.py`, `src/spacex_model/mc/*`.
- Frontend: `frontend/src/app/{ModeRouter,ClientApp,AuditApp}.tsx`, `frontend/src/audit/{DerivationPanel,SourcesPanel,ChangeHistoryList}.tsx`, `frontend/src/components/TornadoChart.tsx`, `frontend/src/shared/{types.ts,format.ts,api.ts}`.

---

## §1 — Purpose & Scope

### §1.1 Purpose

The model's defining promise (`context.md` §5.4, §10) is that every displayed number is traceable to its derivation, inputs, methodology, and history. Four of the five lineage surfaces currently violate that promise — Formula redirects to a doc, Sources shows code paths, the change log shows file-level commits, and computed cells are mislabeled "stub." Separately, the Monte Carlo engine (`context.md` §9) is fully built and tested but exposed only on the retired `/explorer` route. This PRD specifies the engineering changes to repair the per-cell trace and to surface Monte Carlo in both Client and Audit modes.

### §1.2 In scope

The five items below, spanning the lineage enrichment service, the change-history service, the ingestion layer, the MC service/endpoints, and the Client/Audit frontends.

### §1.3 Out of scope

Core numerical model logic and reconciliation targets (`context.md` §11 unchanged — the data contract may change, the model outputs may not); the legacy `/explorer` route (superseded once MC moves to Client/Audit); correlated MC sampling, new distribution families, cell editing, multi-user, auth.

### §1.4 Findings Summary

| # | Finding | Severity | Area | Root-cause file |
|---|---|---|---|---|
| L1 | Computed cells render as "stub — not yet ported"; grid value and panel disagree | **Critical** | Lineage enrichment | `lineage_enrich.py::enrich_lineage`, `_resolve_cell_context` |
| L2 | Formula shows "{label} — see Architecture §X" for nearly all cells | **Critical** | Lineage enrichment | `lineage_enrich.py::_FORMULA_EXPRESSIONS` + fallback |
| L3 | Change log shows file-level commits + keyword-matched DEV_LOG; before→after always blank | **High** | Change history | `lineage_history.py::fetch_change_history` |
| L4 | Sources panel shows code paths; Principle == Rule (duplicate) | **High** | Lineage enrichment | `lineage_enrich.py::_build_sources` |
| M1 | Monte Carlo absent from Client and Audit modes (only on dead `/explorer`) | **High** | MC surfacing | `app/ModeRouter.tsx`, `App.tsx` |

### §1.5 Success criteria

1. No cell that displays a number in the grid is labeled "stub"; grid value == panel computed value for all derived cells.
2. Formula shows a real expression (operands + operation) for every derived row; the "see Architecture" string appears only on genuine stubs.
3. The change log for a cell contains only events that moved *that cell's* value/formula, each with a real before→after and signed delta, sourced from a version-to-version ingest diff.
4. Sources contains no Python identifiers; Methodology names a concrete spec section + plain-language method; Principle and Rule are distinct and meaningful.
5. A Client-Mode user can run an MC sim and read a Group-EV distribution with percentile bands and CVaR; an auditor can open the MC distribution + sensitivity for any headline output, with trial/seed/convergence provenance.

---

## §2 — L1: Stub-cell misclassification (deep dive)

### §2.1 Observed

Clicking a cell that shows a numeric value in the grid frequently opens a derivation panel that says "No computed value — this cell is a **stub** (not yet ported to a traced derivation)" (`DerivationPanel.tsx`, stub branch). This contradicts the grid (this is finding F6 in `FRONTEND_UX_PRD_2026-06-05.md`) and makes the model look far less complete than it is.

### §2.2 Root cause

In `lineage_enrich.py::enrich_lineage`, classification is:

```python
"cell_kind": "derived" if code_val is not None else "stub",
```

`code_val` is produced by `_resolve_cell_context`, which resolves a value via `lookup_by_label(result, sheet, label, year)`. Three brittleness sources make `code_val` `None` for genuinely-computed cells:

1. **Sheet coverage.** `_resolve_label_to_grid_key` only iterates `("Starlink", "Assumptions", "Allocator", "Group P&L")`. Cells on Launch Capacity, Customer Launch, Starlink Capacity, ODC, Lunar Mars, OpEx, CapEx, Demand Curves never resolve.
2. **Exact-label match.** `_find_label_row` compares `lbl == label` exactly. Any divergence (unit suffix `($mm)`, punctuation, section marker `▸`) yields no row, hence `None`.
3. **Accessor mismatch.** Values reachable only through a typed accessor (e.g. `result.vehicle_pools`) rather than `lookup_by_label` are not found; the function has a one-off special case for `module.starlink.total_revenue` only.

The frontend then trusts `cell_kind` via `format.ts::isStubLineage` (`entry.cell_kind === "stub"`). So "lookup failed" is rendered as "not implemented."

### §2.3 Requirement

- **R-L1.1 Diagnose.** Produce a one-time audit (script + report under `docs/`) that enumerates every cell currently classified `stub`, and partitions into (a) genuinely unported (placeholder tabs per `context.md` §2.4 — AI Stack, Valuation), and (b) computed-but-unresolved. Partition + per-bucket root cause is a required deliverable.
- **R-L1.2 Robust resolution.** Replace the 4-sheet, exact-match resolver with one that covers **every sheet the grid can render** and is tolerant of label normalization (strip unit suffixes, section markers, and punctuation before matching; fall back to the grid cell's own cached/computed value already used to populate the grid in `grid.py`). The value shown in the panel must be the same value `grid.py` used to render the cell.
- **R-L1.3 Truth-based classification.** A cell is `stub` **iff** the model genuinely does not derive it (membership in an explicit stub registry of placeholder tabs/rows), **not** when a lookup returns `None`. A `None` on a non-registry cell is a resolver bug → surface as an error in the diagnostic, never as a silent stub.
- **R-L1.4 Stub registry.** Add an explicit registry of true stubs (sheet/row or lineage key → spec section that will implement it). `cell_kind` reads from this registry. The registry is the single source of truth for the "planned — §X" panel state.

### §2.4 Acceptance

- The diagnostic report lists 0 cells in bucket (b) after the fix (all computed cells resolve).
- For a sampled set of ≥1 derived cell per sheet, `cell_kind == "derived"` and `computed_value` equals the grid-rendered value (closes F6).
- The only cells with `cell_kind == "stub"` are those in the stub registry; an e2e/integration test asserts that no grid cell rendering a finite number maps to a `stub` lineage entry.

---

## §3 — L2: Formula must show the derivation

### §3.1 Observed

For nearly every cell the Formula box (`DerivationPanel.tsx`, `data-testid="derivation-formula"`) shows the cell's own label followed by "— see Architecture §X". Only ~8 cells show a real expression.

### §3.2 Root cause

`lineage_enrich.py` defines a hand-maintained dict:

```python
_FORMULA_EXPRESSIONS: dict[str, str] = { ...8 entries... }
```

and the fallback in `enrich_lineage`:

```python
formula = _FORMULA_EXPRESSIONS.get(
    key,
    f"{base.excel_label} — see Architecture {base.architecture_ref or 'spec'}",
)
```

Any key not in the 8-entry dict gets the placeholder. There is no general mechanism mapping a derived row to its formula.

### §3.3 Requirement

- **R-L2.1 Formula library with broad coverage.** Replace the 8-entry dict with a formula registry covering the model's derived rows across all modules (Launch Capacity, Customer Launch, Starlink + Capacity, ODC, Lunar Mars, OpEx, CapEx, Group P&L, Valuation). Each entry is a human-readable expression in operands + operation (e.g. `Module FCF = Module EBITDA − Module CapEx + D&A add-back`), keyed by lineage key (and resilient to year-row vs. scalar).
- **R-L2.2 Source of truth.** Formula text is authored from the constitutional spec (Architecture & Methodology §3, §6–§15) and kept adjacent to the calc docstrings (`context.md` §10.2 four-tag docstrings already carry the formula) so formula and code do not drift. Preferred: derive the registry from the docstring "Formula:" tag rather than a second hand-maintained dict.
- **R-L2.3 Operand consistency.** The operands named in the formula must correspond to the cell's `resolved_inputs` (see L1) so Formula and the Resolved-inputs table agree.
- **R-L2.4 Placeholder only for stubs.** The "see Architecture §X" string is emitted only for cells in the stub registry (L1.4); for all derived cells a real formula is mandatory. Unit context (`$mm`, `%`, `count`) renders correctly.

### §3.4 Acceptance

- For a sampled derived cell per sheet, `formula_expression` is an expression (contains an operator or Σ and ≥1 named operand), not a "see Architecture" string.
- A coverage test asserts every non-stub lineage key returns a non-placeholder `formula_expression`.
- Operands in the formula match labels present in `resolved_inputs` for sampled cells.

---

## §4 — L3: Cell-by-cell change tracking across xlsx versions

### §4.1 Observed

The change log (`ChangeHistoryList.tsx`) shows: commits touching the whole Python module file, plus DEV_LOG entries matched by broad keywords; "Effect: before → after (Δ)" never renders because the data is absent.

### §4.2 Root cause

`lineage_history.py::fetch_change_history`:

1. `_git_log_for_file(rel)` runs `git log -- <module_file>` — every commit to e.g. `starlink/module.py` appears under every cell that module computes, regardless of whether the cell's value moved.
2. `_dev_log_entries()` attaches DEV_LOG entries whose body contains any of `("sprint","frontend","audit","starlink","group","block")` — app-wide notes leak onto cells.
3. Every emitted row sets `"effect_on_cell": None`, so before→after/delta is structurally impossible.

There is **no per-cell value tracking across xlsx ingests** anywhere in the codebase.

### §4.3 Requirement

- **R-L3.1 Per-cell version diff on ingest.** Extend the ingestion layer (`io/excel_ingest.py` / `io/snapshot_store.py`) so that when a new xlsx version is ingested, each cell's value is diffed against the prior ingested snapshot. Persist a per-cell change record:
  - `cell_key` (lineage key, or sheet/row/year), `prior_value`, `new_value`, `delta`, `model_version` (and/or commit SHA), `timestamp`, `change_kind ∈ {value, formula, input, anchor, initial}`.
  - Stored in the snapshot store (parquet/arrow, per `context.md` §4.2/§5.3) keyed for O(1) lookup by `cell_key`.
- **R-L3.2 Cell-scoped history API.** Rewrite `fetch_change_history(key, …)` to return only records keyed to `key` from the per-cell store. Remove `_git_log_for_file` and the keyword DEV_LOG matcher as the primary source. A DEV_LOG/commit reference may be *attached* to a record only when that commit/version is the one that produced the recorded value change.
- **R-L3.3 Real effect_on_cell.** Populate `effect_on_cell = {before, after, delta}` from the diff. The frontend already renders this (`ChangeHistoryList::HistoryRow`); it only needs real data. No frontend redesign required.
- **R-L3.4 Honest empty state.** A cell unchanged since first ingest returns exactly one `change_kind: "initial"` record with its version/date. (Current fabricated "2026-05-12 First derivation" fallback is replaced by a real first-ingest record.)
- **R-L3.5 Trustworthy classification.** `change_kind` is set from what actually changed (value vs. formula vs. input/anchor), not inferred from log prose (`_infer_kind` removed).

### §4.4 Acceptance

- Given two known xlsx versions, for cells whose values changed: the API returns exactly those entries with correct `before`/`after`/`delta`; for cells that did not change: zero spurious entries.
- No returned entry references a commit/version that did not move the cell.
- The `GET /lineage/{key}/history` contract (`api.py`) is unchanged in shape (the frontend `ChangeHistoryEntry` type is already correct); only the data source changes.

---

## §5 — L4: Usable "Sources for this cell"

### §5.1 Observed

`SourcesPanel.tsx` renders: Methodology → "module `spacex_model.calc.starlink.compute_allocator_out`"; spec section often literally "Architecture spec"; Principle/Rule prints the same string twice (the panel guards `methodology.rule !== methodology.principle`, but they are populated identically so Rule never shows).

### §5.2 Root cause

`lineage_enrich.py::_build_sources`:

```python
"methodology": {
    "spec_section": base.architecture_ref or "Architecture spec",
    "principle": base.principle or "—",
    "rule": base.principle or "—",          # <-- same field as principle
    "module": f"{base.module_path}.{base.function}",   # <-- code path surfaced
},
```

Principle and Rule both read `base.principle`; `module` is a code path; `spec_section` falls back to a meaningless literal.

### §5.3 Requirement

- **R-L4.1 No code in the panel.** Remove `module` (the `spacex_model.calc.*` path) from the user-facing `sources.methodology`. If an implementation reference is wanted, it belongs only in the developer audit log (`io/audit_log.py`), not in the Sources payload consumed by `SourcesPanel.tsx`.
- **R-L4.2 Methodology reads as methodology.** `spec_section` must name a concrete Architecture & Methodology section and be accompanied by a plain-language method statement (e.g. "Vending-machine framing: Revenue → COGS → Gross Profit = EBITDA"), sourced from a methodology mapping (see §6). "Architecture spec" with no section is not an acceptable terminal value.
- **R-L4.3 Distinct Principle and Rule.** Populate `principle` from a Lessons-Learned principle and `rule` from a Model Execution Rule — two different, relevant strings, each traceable to its source doc. Never the same string.
- **R-L4.4 Real provenance.** `input_provenance` and `calibration_anchor` reflect the cell's actual grounding (S-1 disclosure, Q4'25 anchor, opening balance) per `context.md` §2.5/§4 — not hardcoded Starlink-only special cases as today.
- **R-L4.5 Coverage.** The methodology mapping spans the model's cells broadly; cells with no mapped methodology are a tracked gap, not silently "Architecture spec."

### §5.4 Acceptance

- For sampled cells across all sheets: `sources.methodology` contains no Python identifier; `spec_section` is a concrete section; `principle` and `rule` differ and are both non-"—".
- A test asserts the Sources payload never contains the substring `spacex_model.` for any key.
- Provenance/anchor fields match the source-of-truth (S-1 / Q4'25) for sampled anchored inputs.

---

## §6 — Methodology & formula mapping (shared dependency of L2 + L4)

L2 (formula) and L4 (methodology/principle/rule) draw from the same constitutional corpus and must not drift apart. Specify a single structured mapping (e.g. `service/methodology_registry.py` or a data file) that, per lineage key, provides: `formula_expression`, `architecture_section`, `method_statement`, `principle`, `rule`. L2 reads the formula fields; L4 reads the methodology fields. Authoring once into this mapping (or extracting it from the calc docstring four-tag block, `context.md` §10.2) keeps Formula, Sources, and the code in sync. This is a shared deliverable, sequenced before L2/L4 completion.

---

## §7 — M1: Monte Carlo in Client + Audit modes

### §7.1 Observed

There is no Monte Carlo UI in Client Mode (`/client/*` → `ClientApp.tsx`) or Audit Mode (`/audit/:sheetSlug` → `AuditApp.tsx`). MC submit/poll and the `TornadoChart` exist only in the legacy `App.tsx`, reachable solely at `/explorer` (`ModeRouter.tsx`).

### §7.2 Existing assets (reuse, do not rebuild)

- Engine: `mc/sampler.py`, `mc/distributions.py` (triangle, lognormal, uniform, discrete, year-row variants per `context.md` §9.1), `mc/runner.py`, `mc/aggregator.py` (`MetricSummary` p5/p10/p25/p50/p75/p90/p95, mean, std, `cvar_5`, `base_case`; `McAggregation.convergence_trace`), `mc/sensitivity.py` (tornado).
- API: `POST /runs/mc` (`McSubmitRequest`: `trials`, `base_seed`, `n_jobs`, `scenario`, `include_tornado`, `tornado_top`), `GET /runs/mc/{job_id}` (status/progress/result), `GET /runs/{run_id}/tornado`, with serverless batching already handled (`is_serverless()`, `mc_serverless_max_trials`).
- Frontend: `api.ts::submitMc/fetchMcJob`, `components/TornadoChart.tsx`.

### §7.3 Requirement

**Backend / data contract**

- **R-M1.1 Distribution payload.** The aggregator returns percentile/CVaR scalars but the surfaces need shape. Add to the MC result payload (no engine recompute): histogram bins for the headline metric (Group EV), and a percentile-by-year series for the Group FCF fan (p5/p25/p50/p75/p95 per forecast year). Expose via the existing `GET /runs/mc/{job_id}` result, or a sibling `GET /runs/mc/{job_id}/distribution`.
- **R-M1.2 Provenance fields.** Ensure the MC job result includes `n_trials`, `n_converged`, `base_seed`, and convergence status for the Audit panel (most already on `McAggregation`; expose them in the serialized result).
- **R-M1.3 Preserve serverless contract.** Keep the batched submit/poll semantics (`out["execution"] = "batched"`); the new payloads must work under the serverless trial cap.

**Client Mode (`/client/*`)**

- **R-M1.4 Run control.** A labeled "Run Monte Carlo" action for the selected scenario, with a trial-count control bounded by the serverless cap (default sensible; see Open Question 1).
- **R-M1.5 Honest progress.** While trials run, show progress + ETA per the loading standard in `FRONTEND_UX_PRD_2026-06-05.md` §1.5.3 — never a blank panel. Poll `GET /runs/mc/{job_id}` transparently.
- **R-M1.6 Distribution view.** Group-EV histogram and/or percentile fan with P5/P50/P95 callouts, the deterministic base-case marker, and a one-line plain-language tail-risk readout from `cvar_5`. A Group-FCF percentile fan-by-year reusing the `FcfTable`/`FcfSparkline` visual language.
- **R-M1.7 Sensitivity.** A ranked "what drives this" view rendered from the existing tornado data (`TornadoChart`, relocated/shared out of `App.tsx`).
- **R-M1.8 Reproducible & addressable.** A completed run is re-openable (run id / share link) and reproducible from `base_seed`.

**Audit Mode (`/audit/*`)**

- **R-M1.9 Per-output MC panel.** From a headline output cell (Group EV, Group FCF, module FCF), open an MC panel showing the distribution, percentile table, and sensitivity for that output, consistent with the derivation rail (deterministic "how derived" ↔ stochastic "how distributed" for the same output).
- **R-M1.10 Audit provenance.** The panel shows `n_trials`, `n_converged`, `base_seed`, and convergence status (the MC analogue of the lineage reproducibility fields, `context.md` §10.4).

**Cleanup**

- **R-M1.11** Once MC is in Client + Audit, retire the `/explorer` legacy route and `App.tsx` MC code, or reduce it to a thin re-export, to avoid two MC code paths.

### §7.4 Acceptance

- In Client Mode, a user goes scenario → "Run Monte Carlo" → readable Group-EV distribution with P5/P50/P95 + CVaR readout, with visible progress and no blank screen.
- The numbers in every MC view equal the engine aggregation for the same `base_seed` (UI invents no numbers); an integration test compares rendered percentiles to `MetricSummary`.
- In Audit Mode, the MC panel for a headline output displays distribution + tornado + `n_trials`/`n_converged`/`base_seed`/convergence.
- Re-opening a completed run by id reproduces identical aggregates.

---

## §8 — Cross-cutting & sequencing

### §8.1 Dependencies

L1 (robust value resolution) unblocks L2 (formula operands), L3 (real before→after), and L4 (provenance), because all three need to reliably resolve a cell to its value/inputs. §6 (methodology+formula registry) is a shared prerequisite of L2 and L4. M1 is independent and can run in parallel.

### §8.2 Suggested order

1. **L1** — stub/resolver fix (highest trust impact, unblocks others).
2. **§6** — methodology + formula registry.
3. **L2, L4** — formula and sources (consume §6).
4. **L3** — ingest-time per-cell diff + history rewrite.
5. **M1** — Monte Carlo surfacing (parallelizable from step 1).

Final sequencing is a planning decision; the dependency edges above are the constraint.

### §8.3 Non-goals reaffirmed

No change to model outputs or reconciliation pass criteria (`context.md` §11). Data-contract additions (cell `cell_kind` truth, `formula_expression` coverage, `effect_on_cell`, MC distribution payload) are API/serialization changes, not model-logic changes.

---

## §9 — Resolved Decisions

These were open questions; resolved as follows and binding on the spec above.

1. **MC trial defaults & pre-cache.** Client Mode default **2,000** trials (≤ `mc_serverless_max_trials`); Audit Mode default **5,000** (full 10,000 available off-serverless). **A base-case MC run is precomputed and shipped at deploy time** — exactly as the deterministic base case is precached (`FRONTEND_UX_PRD_2026-06-05.md` §1.5.3) — so the Client and Audit MC views render a real distribution instantly on first open, with no solver wait. The "Run Monte Carlo" control re-runs only when the user changes scenario/overrides. (Updates R-M1.4/R-M1.5: base case is instant; only non-base runs poll.)
2. **Change-history granularity.** Record **every ingested xlsx version** (no materiality threshold). The store keeps the full per-cell version sequence; the UI may collapse within-tolerance entries visually, but the data is complete. (Confirms R-L3.1.)
3. **Methodology/formula registry source.** **Extract programmatically from the calc docstring four-tag block** (`context.md` §10.2: Excel cell, Excel label, Architecture ref, Principle, plus the `Formula:` line) as the source of truth, so Formula/Sources cannot drift from code; layer a small **curated overlay** file (`methodology_overlay.toml`) for display polish (plain-language method statements, Rule text) where the docstring is terse. The existing docstring linter (`linters/docstrings.py`) gates coverage. (Implements §6.)
4. **True-stub presentation.** Yes — a distinct **"Planned — §X"** panel state for stub-registry cells (AI Stack, Valuation), visually separate from both derived cells and error/unresolved states. (Implements R-L1.4 / R-L2.4.)

---

## §10 — Sprint Plan (for a Cursor AI agent)

Self-contained, ordered sprints. Each lists **scope**, **files**, **steps**, and a **Definition of Done (DoD)** with the exact commands to verify. Run the existing gates after every sprint: `ruff check . && mypy --strict src && pytest -q` (backend) and `cd frontend && npm run lint && npm run build && npx playwright test` (frontend). Do not mark a sprint done with a failing gate. Append a `docs/DEV_LOG.md` entry per sprint (per `role.md`). Do not change model outputs or `context.md` §11 pass criteria.

### Sprint 0 — Diagnostics & guardrails (½ day)

- **Scope:** Establish the stub baseline before touching resolution (L1.1) and lock the no-model-change guarantee.
- **Files:** new `scripts/audit_stub_cells.py`; new `tests/reconciliation/test_no_model_drift.py` (golden snapshot of Group + per-module outputs).
- **Steps:**
  1. Write a script that walks every grid-renderable sheet, calls the lineage enrichment per cell, and emits `docs/stub_audit_2026-06-05.md`: counts of `cell_kind == "stub"` partitioned into (a) placeholder-tab cells (AI Stack, Valuation per `context.md` §2.4) and (b) computed-but-unresolved.
  2. Capture a golden output snapshot so later sprints can prove model numbers didn't move.
- **DoD:** `python scripts/audit_stub_cells.py` produces the report; report shows bucket (b) count > 0 (the bug, quantified). `pytest -q tests/reconciliation/test_no_model_drift.py` passes (baseline recorded).

### Sprint 1 — L1: Robust value resolution & truth-based stub classification (2–3 days)

- **Scope:** L1 (Critical). Fix `cell_kind`; make panel value == grid value.
- **Files:** `src/spacex_model/service/lineage_enrich.py` (`_resolve_cell_context`, `_resolve_label_to_grid_key`, `_find_label_row`, `enrich_lineage`), `src/spacex_model/service/grid.py` (reuse its cell-value path), `src/spacex_model/engine/label_lookup.py`; new `src/spacex_model/service/stub_registry.py`; `frontend/src/shared/format.ts` (`isStubLineage`), `frontend/src/audit/DerivationPanel.tsx` (add "Planned — §X" state).
- **Steps:**
  1. Add a label-normalization helper (strip `($mm)`/`(%)` suffixes, `▸` section markers, punctuation, whitespace) and use it in all label matching.
  2. Replace the 4-sheet list with iteration over **all** grid-renderable sheets; fall back to the exact value `grid.py` used to render the cell so panel and grid cannot disagree.
  3. Create `stub_registry.py` (explicit set of true-stub sheets/rows/lineage-keys → spec section). Set `cell_kind = "stub"` **iff** in registry; otherwise `"derived"`. A `None` value on a non-registry cell raises/logs a resolver error (surfaced in the Sprint 0 report), never silent stub.
  4. Frontend: render `cell_kind === "stub"` as "Planned — §X"; remove the implicit "stub on missing value" path.
- **DoD:** re-run `scripts/audit_stub_cells.py` → bucket (b) == 0. New test `tests/.../test_no_false_stubs.py`: for ≥1 derived cell per sheet, `cell_kind == "derived"` and `computed_value` equals the grid value (closes F6). Playwright: clicking a numeric grid cell never shows the stub copy. No-model-drift test still passes.

### Sprint 2 — §6: Methodology & formula registry (1–2 days)

- **Scope:** Shared dependency for L2+L4 (decision §9.3).
- **Files:** new `src/spacex_model/service/methodology_registry.py`; new `docs/methodology_overlay.toml`; `src/spacex_model/linters/docstrings.py` (extend to expose the `Formula:` tag); reads from `calc/**`docstrings.
- **Steps:**
  1. Parse the four-tag docstring block (+ `Formula:` line) from every public `calc/` function into a registry keyed by lineage key, yielding `{formula_expression, architecture_section, method_statement, principle, rule}`.
  2. Add `methodology_overlay.toml` for plain-language polish where docstrings are terse; overlay wins for display text only.
  3. Extend the docstring linter to fail if a non-stub lineage key lacks a `Formula:` tag (coverage gate).
- **DoD:** `pytest -q tests/.../test_methodology_registry.py`: every non-stub key resolves a non-empty `formula_expression`, `principle`, and `rule`, with `principle != rule`. Docstring linter passes with the new coverage rule.

### Sprint 3 — L2 + L4: Formula display & Sources panel (1–2 days)

- **Scope:** L2 + L4, consuming Sprint 2.
- **Files:** `src/spacex_model/service/lineage_enrich.py` (remove `_FORMULA_EXPRESSIONS` dict + placeholder fallback; remove code path from `_build_sources`); `frontend/src/audit/SourcesPanel.tsx` (verify Rule renders distinctly).
- **Steps:**
  1. `formula_expression` reads from the registry; placeholder string allowed only for stub-registry cells.
  2. `_build_sources`: drop `module` (code path); populate `spec_section`+`method_statement`, distinct `principle`/`rule`, and real `input_provenance`/`calibration_anchor` from registry + `inputs/s1_2025_anchors.py`.
  3. Ensure formula operands correspond to `resolved_inputs` (from Sprint 1).
- **DoD:** test asserts the Sources payload never contains `spacex_model.`; for sampled cells per sheet `formula_expression` contains an operator/Σ + named operand, `spec_section` is concrete, `principle != rule`. Playwright: Formula box shows an expression, not "see Architecture".

### Sprint 4 — L3: Per-cell change tracking on ingest (2–3 days)

- **Scope:** L3. Record every ingested version (decision §9.2).
- **Files:** `src/spacex_model/io/excel_ingest.py`, `src/spacex_model/io/snapshot_store.py` (new per-cell change store, parquet/arrow); `src/spacex_model/service/lineage_history.py` (rewrite `fetch_change_history`; delete `_git_log_for_file` primary use, `_dev_log_entries` keyword matcher, `_infer_kind`); `frontend/src/audit/ChangeHistoryList.tsx` (no redesign — verify `effect_on_cell` renders).
- **Steps:**
  1. On ingest, diff each cell vs. the prior ingested snapshot; persist `{cell_key, prior_value, new_value, delta, model_version, timestamp, change_kind}` for **every** version.
  2. Rewrite `fetch_change_history(key)` to read only records for that key; classify `change_kind` from the actual diff; first-ingest emits one real `initial` record.
  3. `effect_on_cell = {before, after, delta}` populated from the diff. Keep the `GET /lineage/{key}/history` response shape unchanged.
- **DoD:** integration test over two known xlsx versions: changed cells return exactly their changes with correct before/after/delta; unchanged cells return zero spurious entries; no entry references a non-touching commit/version. Frontend renders the Effect line.

### Sprint 5 — M1 backend: MC distribution payloads + base-case precache (2 days)

- **Scope:** R-M1.1/1.2/1.3 + decision §9.1 precache.
- **Files:** `src/spacex_model/mc/aggregator.py` (histogram bins for Group EV; percentile-by-year fan for Group FCF), `src/spacex_model/mc/results.py`, `src/spacex_model/service/serializers.py` (`serialize_mc_aggregation`), `src/spacex_model/service/api.py` (extend `GET /runs/mc/{job_id}` result or add `/runs/mc/{job_id}/distribution`); build/deploy step that precomputes a base-case MC run artifact (mirror the deterministic base-case precache).
- **Steps:**
  1. Add histogram + percentile-fan aggregation reusing existing trial data (no engine recompute); expose `n_trials/n_converged/base_seed/convergence` in the serialized result.
  2. Precompute base-case MC (2,000 trials, seed 42) at deploy and ship as a static artifact the frontend loads instantly.
  3. Preserve serverless batching semantics.
- **DoD:** `pytest -q tests/.../test_mc_distribution_payload.py`: payload exposes bins, per-year percentiles, and provenance; values equal `MetricSummary`/engine aggregates for seed 42. Base-case MC artifact present in build output.

### Sprint 6 — M1 frontend: MC in Client Mode (2–3 days)

- **Scope:** R-M1.4–1.8.
- **Files:** new `frontend/src/client/MonteCarloPanel.tsx`, `frontend/src/client/EvDistributionChart.tsx`, `frontend/src/client/FcfFanChart.tsx`; relocate `components/TornadoChart.tsx` to a shared location; `frontend/src/app/ClientApp.tsx`; `frontend/src/shared/api.ts` (reuse `submitMc/fetchMcJob` + new distribution fetch).
- **Steps:**
  1. Render the precached base-case distribution instantly on open; "Run Monte Carlo" (trial control, default 2,000) only fires for changed scenario/overrides.
  2. Group-EV histogram/percentile fan with P5/P50/P95 + base-case marker + plain-language CVaR readout; Group-FCF fan-by-year reusing `FcfTable`/`FcfSparkline`; tornado "what drives this".
  3. Honest progress + ETA on non-base runs per `FRONTEND_UX_PRD_2026-06-05.md` §1.5.3; reproducible via run id / share link.
- **DoD:** Playwright (`e2e/client-mode.spec.ts`): base case shows a distribution with no wait; a non-base run shows progress then percentiles; rendered P5/P50/P95 equal API aggregates. `npm run build` within bundle budget.

### Sprint 7 — M1 frontend: MC in Audit Mode + legacy cleanup (1–2 days)

- **Scope:** R-M1.9–1.11.
- **Files:** new `frontend/src/audit/McAuditPanel.tsx`; `frontend/src/app/AuditApp.tsx` (open MC from a headline output cell); `frontend/src/app/ModeRouter.tsx` + `frontend/src/App.tsx` (retire `/explorer` or reduce to thin re-export).
- **Steps:**
  1. From Group EV / Group FCF / module FCF, open an MC panel: distribution + percentile table + tornado + `n_trials/n_converged/base_seed/convergence`. User can toggle deterministic derivation ↔ MC distribution for the same output.
  2. Remove the duplicate MC path in `App.tsx`; delete/retire `/explorer`.
- **DoD:** Playwright (`e2e/audit-mode.spec.ts`): MC panel opens from a headline cell with distribution + sensitivity + provenance; re-opening a run by id reproduces identical aggregates; no remaining import of MC from `App.tsx` in Client/Audit paths.

### Sprint sequencing & parallelism

Critical path: **Sprint 0 → 1 → 2 → 3**, then **4**. **Sprints 5–7 (Monte Carlo)** are independent and may run in parallel from the start by a second agent/branch. Merge order is flexible; the only hard edges are 1→2→3 (resolution → registry → display) and 5→6, 5→7 (backend payload → frontend).
