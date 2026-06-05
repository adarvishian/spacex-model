# Engineering Spec — Monte Carlo Performance, Same Statistical Quality

**Date:** 2026-06-05
**Author:** Dr. Marcus Hale (Principal Financial Engineer)
**Status:** Spec for implementation. Hand to Cursor as the work order.
**Scope:** Speed up the 2,000-trial base-case Monte Carlo so Vercel builds (and local/interactive runs) stop taking ~25 min, **without** degrading the statistical quality of the published distribution.
**Constitutional note:** Numerical fidelity is sacred (`role.md`). Every change below is gated behind an equivalence harness (§3). No change ships until it passes that harness. Any material logic change requires an append-only entry in `docs/DEV_LOG.md`.

---

## 1. Problem statement (grounded in the current code)

The Vercel build runs `frontend` → `prebuild` script:

```jsonc
// frontend/package.json
"prebuild": "python ../scripts/precompute_base_case.py && python ../scripts/precompute_base_case_mc.py",
```

`scripts/precompute_base_case_mc.py` calls `run_mc(...)` with `DEFAULT_TRIALS = 2000`, `seed 42`. Each trial is a **full** model solve:

```
mc.runner._run_single_trial
  → sample_trial()              # mc/sampler.py: per-trial RNG = base_seed + trial_idx
  → apply_trial_samples()
  → engine.pipeline.run_pipeline(write_outputs=False)
  → mc.results.extract_trial_metrics(result)
```

The bottleneck is **2,000 full `run_pipeline` solves on the critical path of every deploy**. Three structural inefficiencies make each solve more expensive than the MC needs:

1. **Cold-start solver every trial.** `run_pipeline` always seeds the fixed-point solver from an all-zero `PipelineState` (`initial_pipeline = PipelineState(cash_alloc=CashAllocations.zeros(), …)`). Perturbed trials sit close to the base case, but the solver re-discovers the solution from zero each time, up to `SOLVER_MAX_ITERATIONS = 1000` at `SOLVER_TOLERANCE = 1e-7` (`config/constants.py`).

2. **Full audit pipeline per trial.** `run_pipeline` runs `tracemalloc`, allocation-bound checks, allocator conservation, the conservation halt, divergence-report imports, anchor checks, and builds the complete `ModelResult` — but `extract_trial_metrics` only reads `result.group_pnl`, `result.valuation`, `result.module_outputs`, and `result.solver_trace`. Everything else is dead weight in the MC path.

3. **Pure Monte Carlo sampling.** `sample_trial` draws independent pseudo-random samples per input. Pure MC error on tail percentiles shrinks as `O(N^-1/2)`; low-discrepancy (QMC) sampling can hit the same percentile accuracy with materially fewer trials.

We address all three while holding the published distribution fixed within a documented tolerance.

---

## 2. Goals & non-goals

### 2.1 Goals

- **G1 — Same statistical quality.** The published base-case distribution (P5/P25/P50/P75/P95 of Group EV and every Group FCF year, plus convergence-failure handling) stays within tolerance of today's 2,000-trial, seed-42 run. See §3 for the exact bar.
- **G2 — Faster trials.** Cut wall-clock per the success metrics in §8 via warm-start (B) + MC-lite pipeline (A).
- **G3 — Fewer trials for the same accuracy.** QMC/Sobol (C) + adaptive stopping (D) reduce trial count without loosening the tolerance in G1.
- **G4 — Auditability preserved.** Reproducibility (seed → identical artifact), convergence-failure semantics, and the four-tag docstring convention (`context.md` §10.2) are unchanged. The MC-lite path is a *strict subset* of the full pipeline math, proven equal on a sample of trials.

### 2.2 Non-goals (explicitly out of scope for this spec)

- **Looser MC-only solver tolerance (Cursor option E).** Deferred. Relaxing `SOLVER_TOLERANCE` for MC trades numerical fidelity for speed and is exactly the kind of "improvement" `role.md` forbids without separate sign-off. Not in this work order. If pursued later, it needs its own spec and its own equivalence study.
- **Build/deploy decoupling (Cursor option F).** Worthwhile and arguably the single biggest deploy win, but it is an infra/CI change, not an MC-quality change. Tracked separately (see §9, "Companion track"). This spec assumes the precompute still runs, and makes *that* run fast and statistically sound.
- **Correlated sampling, GPU, distributed workers, model re-architecture.** Out of scope.

---

## 3. Acceptance bar — the equivalence harness (build this FIRST)

Nothing in §4 ships until it passes this. Build the harness before any optimization so every change is measured against it.

### 3.1 Frozen reference

Generate and commit a **golden baseline** from the *current* code, before any change:

- Run: `run_mc(trials=2000, base_seed=42, scenario="base_case")` on the locked workbook.
- Persist the **full per-trial parquet** (not just aggregates) plus the aggregated percentiles to `tests/golden/mc_baseline_seed42_2000.parquet` and `…/mc_baseline_seed42_2000_agg.json`.
- Record `git_sha`, workbook SHA, and `trials_converged`.

This is the diagnostic oracle for every subsequent change. It is regenerated only on explicit approval (per `context.md` golden-snapshot rule).

### 3.2 Equivalence test (`tests/reconciliation/test_mc_equivalence.py`)

For a candidate MC run, PASS requires **all** of:

1. **Percentile tolerance.** For each metric in {`group_ev_2025_b`, `group_fcf_<year>_mm` for every year in horizon, `group_revenue_2050_mm`, each `*_ev_2025_b`}, the candidate's {P5, P25, P50, P75, P95} are within **±0.5% relative** (or ±$1mm absolute for near-zero FCF years, whichever is looser) of the golden baseline.
2. **Mean/CVaR tolerance.** Candidate mean and CVaR(5%) of `group_ev_2025_b` within **±0.5% relative** of baseline.
3. **Convergence parity.** `non_convergence_rate` within **±0.5 percentage points** of baseline; NaN/inf handling of failed trials identical (failed trials still produce a row with `converged=False` and NaN metrics, per current `_run_single_trial`).
4. **No new tail pathology.** No metric develops a new NaN/inf that the baseline didn't have; min/max of each metric stay within baseline min/max ±0.5%.

### 3.3 Technique-specific acceptance notes

- **Warm-start (B) and MC-lite (A)** change *how* a trial is solved, not *which* points are sampled. For these, the per-trial metrics must match the baseline **per trial** within solver tolerance — a far stricter test than §3.2. Add `test_mc_lite_matches_full_per_trial` and `test_warm_start_matches_cold_per_trial`: run e.g. 200 trials both ways and assert each metric agrees to ≤ `10 × SOLVER_TOLERANCE` (warm-start) / exactly (MC-lite, see §4.1). This is the real guardrail; §3.2 is the aggregate backstop.
- **QMC (C) and adaptive stopping (D)** deliberately change the sample, so per-trial matching does **not** apply. They are held to the §3.2 aggregate tolerance only, against the **same number of effective draws** where applicable (see §4.3, §4.4).

---

## 4. Workstreams

Implement in this order. Each is independently shippable and independently gated by §3.

### 4.1 WS-A — MC-lite pipeline (lean solve path)

**Objective:** a pipeline entry point that computes exactly the quantities `extract_trial_metrics` reads and nothing else, producing per-trial metrics **bit-identical** to the full path.

**Design:**

- Add `run_pipeline_mc(...)` (or `run_pipeline(..., mode="mc")`) in `engine/pipeline.py` that:
  - Reuses the identical `_single_pass` and `solve_fixed_point` core — **the solved fixed point must be the same object math as the full path**, so the converged state is numerically identical.
  - **Skips** (relative to `run_pipeline`): `tracemalloc` start/stop and peak-memory capture; `check_allocation_bounds`; `compute_allocator_conservation` / `merge_allocator_conservation`; the conservation halt; divergence-report imports and `build_divergence_report`; anchor-warning extension; audit-JSON / outputs writing. None of these feed `extract_trial_metrics`.
  - **Keeps:** ingest reuse (already passed in), S-1 overrides (`apply_s1_adherence_overrides`), scenario/trial overrides, the solve, and assembly of `group_pnl`, `valuation`, `module_outputs`, `solver_trace`.
  - Returns a lightweight result object exposing the four attributes `extract_trial_metrics` needs, or the existing `ModelResult` with the unused-but-required fields populated lazily/None.
- `mc.runner._run_single_trial` calls `run_pipeline_mc` instead of `run_pipeline`.
- **Conservation is not silently dropped.** Because Block A invariants (`context.md` §11.1) are a contract, add a **periodic conservation audit**: every K-th trial (configurable, default every 100th, plus trial 0) runs the *full* `run_pipeline` and asserts conservation holds. A break aborts the MC run with the failing trial index. This preserves the integrity proof without paying for it on every trial.

**Proof of equivalence:** `test_mc_lite_matches_full_per_trial` (§3.3) — every metric, every trial in the sample, exactly equal (same solver, same converged state → same extraction). Any non-equality is a bug in what WS-A skipped.

**Risk:** accidentally skipping something that *does* influence the monitored state or the extracted metrics. Mitigated by the per-trial exact-match test; if it fails, the skipped step was load-bearing — restore it.

### 4.2 WS-B — Solver warm-start

**Objective:** seed each trial's fixed-point solver from a known-good nearby solution instead of zeros, cutting iterations per trial.

**Design:**

- Compute the **base-case converged `PipelineState` once** (before the trial loop, in `run_mc`) and pass it into workers as `warm_start_state`.
- `run_pipeline_mc(..., initial_state=warm_start_state)` seeds `initial_pipeline` from the warm state rather than `PipelineState(... .zeros())`. The warm state must be **deep-copied / treated immutable per trial** (calc functions are pure per `context.md` §6.1, but the seed dict must not be mutated across workers).
- **Convergence semantics unchanged.** Same `SOLVER_TOLERANCE`, same `SOLVER_MAX_ITERATIONS`, same `NonConvergenceError` behavior. Warm-start only changes the starting point, never the stopping criterion — so the converged answer is identical (a contraction mapping converges to the same fixed point regardless of seed). This is why it preserves quality.
- **Optional escalation (sequential only):** chaining each trial off the previous trial's solution is *not* worker-safe under joblib parallelism and introduces trial-order dependence (hurts reproducibility). **Do not chain across trials.** Seed every trial from the *base-case* solution only. This keeps trials independent and reproducible.

**Guardrail — divergence safety net:** if a warm-started trial hits `NonConvergenceError`, **retry that trial once from the cold zero state** before recording it as non-converged. A perturbation far from base could in principle be a worse starting point; the cold retry guarantees warm-start never *increases* the non-convergence rate. Log any trial that needed the cold retry (expected: near-zero count).

**Proof of equivalence:** `test_warm_start_matches_cold_per_trial` (§3.3) — metrics agree to within solver tolerance; `non_convergence_rate` unchanged (§3.2.3). Also assert mean iterations-to-converge drops (the whole point) via `solver_iterations` in the trial table.

### 4.3 WS-C — QMC / Sobol sampling

**Objective:** replace pure pseudo-random sampling with a low-discrepancy sequence so a given trial count yields lower percentile variance (equivalently, fewer trials for the §3.2 tolerance).

**Design:**

- The sampleable dimension is `len(list_variable_labels(assumptions))` = `d` (the non-`fixed` MC inputs in `mc/sampler.py`).
- Add a QMC path using `scipy.stats.qmc.Sobol(d, scramble=True, seed=base_seed)` (`scipy.stats.qmc` is already named in `context.md` §5.1 and §9.2 as the intended tool). Generate `N` Sobol points in the d-dim unit cube; map each coordinate through the **inverse CDF** of its input's distribution (`triang`, `lognorm`, `uniform`, `discrete`) — i.e. refactor `mc/distributions.sample_value` to expose an `inverse_cdf(u, …)` alongside the existing RNG draw, so MC and QMC share one distribution definition.
- **Use a scrambled Sobol sequence with `N = 2^m`** (power of two) for balance; if adaptive stopping (WS-D) needs intermediate sizes, use the sequence prefix property (Sobol prefixes are still low-discrepancy) or `random_base2`.
- **Scrambling provides reproducible randomization:** fixed `seed=base_seed` → identical point set → byte-stable artifact (preserves `context.md` §8.3 reproducibility). Different seeds give independent QMC replicates, which also enable a variance estimate (see below).
- Sobol is **opt-in via config** (`McRunConfig.sampling: Literal["mc","qmc"] = "mc"` initially), so the change is gated and reversible. Flip the default to `qmc` only after §3.2 passes at the target trial count.

**Quality proof:** Sobol changes the sample, so hold it to §3.2 aggregate tolerance. Demonstrate the *win* with a convergence study: run QMC at N ∈ {256, 512, 1024} and pure MC at N=2000, show QMC reaches the §3.2 band against the golden baseline at a smaller N. Estimate residual QMC error with **randomized QMC**: R independent scrambles (e.g. R=8) at the chosen N; the across-scramble std of each percentile is the error bar, and it must sit inside the §3.2 tolerance.

**Caveats to encode in the spec for Cursor:**
- `discrete` inputs need careful inverse-CDF binning (step function); document the convention.
- `triangle-yearrow` / `fixed-yearrow` (year-row multiplier) inputs occupy **one** Sobol dimension each (single multiplier per trial), matching current `sample_trial` behavior — confirm the dimension count and ordering are stable and seeded deterministically.
- Keep input→dimension ordering **fixed and label-sorted** (`list_variable_labels` already sorts) so the QMC mapping is reproducible across runs.

### 4.4 WS-D — Adaptive stopping

**Objective:** stop at the smallest trial count that already meets the quality bar, instead of a hard-coded 2,000.

**Design:**

- After each checkpoint batch (`run_mc` already batches by `checkpoint_interval`), compute the running estimate of the **monitored aggregates** — at minimum P50 and P5 of `group_ev_2025_b` and the running std of mean Group EV (Cursor's `running_std` of Group EV).
- **Stop when** the change in each monitored percentile between consecutive checkpoints is `< ε` (relative), for `C` consecutive checkpoints (default `ε = 0.25%`, `C = 2`) — i.e. the distribution has stabilized. Enforce a **floor** `min_trials` (default 512) and a **ceiling** `max_trials` (default 2000, today's value) so it can never run away or stop prematurely.
- Record the stopping trial count and the convergence trace in the artifact `audit` block for transparency.
- **Pairs naturally with QMC:** with Sobol prefixes, increasing N is just extending the sequence, and the stabilization check is cleaner because QMC error is monotone-ish.

**Quality proof:** the stopping rule's *definition* is the §3.2 tolerance applied to the running estimate, so a passing adaptive run is by construction within band of a converged run. Validate by replaying the golden 2,000-trial parquet: confirm the rule would have stopped at N* and that the N*-prefix aggregates pass §3.2. Default `ε`/`C` chosen so N* < 2000 on the base case while staying in tolerance.

**Risk:** stopping in a local plateau before a tail fills in. Mitigated by (a) the `min_trials` floor, (b) requiring `C` consecutive stable checkpoints, (c) monitoring the **tail** percentile (P5) and CVaR, not just the median.

---

## 5. Configuration & surface changes

Add to `McRunConfig` (`mc/runner.py`), all defaulting to today's behavior so nothing changes until explicitly enabled:

```python
sampling: Literal["mc", "qmc"] = "mc"        # WS-C
warm_start: bool = False                      # WS-B
mc_lite: bool = False                         # WS-A (then flip default True once proven)
adaptive: bool = False                        # WS-D
adaptive_min_trials: int = 512
adaptive_max_trials: int = 2000
adaptive_eps: float = 0.0025
adaptive_consecutive: int = 2
conservation_audit_every: int = 100           # WS-A periodic full-pipeline check
```

`scripts/precompute_base_case_mc.py` gains the same env-var overrides it already uses for trials/seed, e.g. `SPACEX_MODEL_MC_SAMPLING`, `SPACEX_MODEL_MC_WARM_START`, `SPACEX_MODEL_MC_ADAPTIVE`. The committed `base_case_mc.json` artifact must record which knobs were active (extend the `artifact` dict) so the published distribution is self-describing and auditable.

---

## 6. Files touched (orientation for Cursor)

| File | Change |
|---|---|
| `tests/golden/` | NEW golden baseline parquet + agg JSON (§3.1) |
| `tests/reconciliation/test_mc_equivalence.py` | NEW harness (§3.2, §3.3) |
| `src/spacex_model/engine/pipeline.py` | `run_pipeline_mc` / `mode="mc"` lean path + `initial_state` seed param (WS-A, WS-B) |
| `src/spacex_model/mc/runner.py` | compute warm-start state; per-trial mode; cold-retry safety net; adaptive loop; conservation-audit hook; `McRunConfig` fields |
| `src/spacex_model/mc/sampler.py` | QMC sampler sharing one distribution definition (WS-C) |
| `src/spacex_model/mc/distributions.py` | expose `inverse_cdf` alongside RNG draw (WS-C) |
| `src/spacex_model/mc/aggregator.py` | running-aggregate / stopping diagnostics (WS-D) |
| `scripts/precompute_base_case_mc.py` | env-var knobs; record active config in artifact |
| `docs/DEV_LOG.md` | append-only entry per material change |

No change to `config/constants.py` solver settings (`SOLVER_TOLERANCE`, `SOLVER_MAX_ITERATIONS` untouched — that's the deferred option E).

---

## 7. Sequencing & rollout

1. **WS-A harness + golden baseline** (§3). Land first; it's the measuring stick.
2. **WS-A MC-lite**, prove per-trial exact, flip `mc_lite` default to `True`. *(Pure speed, zero quality risk.)*
3. **WS-B warm-start** + cold-retry net, prove per-trial within tolerance and `non_convergence_rate` unchanged. *(Pure speed, zero quality risk.)*
4. **WS-C QMC**, convergence study, randomized-QMC error bars within §3.2. Flip default to `qmc` only after passing at the target N.
5. **WS-D adaptive**, validate stopping rule on golden replay. Enable with conservative `min_trials` floor.

Steps 2–3 are the safe, high-confidence wins (same sample, same answer, faster). Steps 4–5 reduce trial count and should land behind their config flags with the convergence evidence attached to the DEV_LOG entry.

---

## 8. Success metrics

- **Quality:** §3.2 harness PASS on every shipped configuration. Per-trial exact/within-tolerance for WS-A/WS-B.
- **Speed:** report and commit before/after wall-clock for `precompute_base_case_mc.py` on the build box. Targets: WS-A+WS-B together cut per-trial cost meaningfully (track via mean `solver_iterations` drop and wall-clock); WS-C+WS-D cut trial count from 2,000 to the smallest N that holds §3.2 (expect the published precompute to run in a fraction of today's ~25 min). State the achieved numbers in the DEV_LOG entry rather than asserting a target here.
- **Auditability:** artifact records active knobs, stopping N, convergence rate; reproducibility test (same seed → byte-identical artifact) still passes.

---

## 9. Companion track (not this spec, but the bigger deploy win)

Independent of MC quality, the fastest way to fix a 25-min *deploy* is to stop recomputing the MC on every build (Cursor option F): commit a freshly generated `base_case_mc.json` and set `SPACEX_MODEL_MC_PRECOMPUTE_TRIALS` low (e.g. 64) on Vercel, generating the full artifact in a separate CI/offline job. That is an infra change with its own correctness story (the committed artifact must match a known git SHA and be regenerated on every input change). Recommend doing it in parallel — but it is **out of scope here** because it doesn't touch statistical quality, which is what this spec governs. The two tracks compose: a fast, statistically-sound MC (this spec) generated by a decoupled job (option F) gives both correct numbers and fast deploys.

---

## 10. Open questions for sign-off

1. Confirm **±0.5% relative** percentile tolerance (§3.2) is the right institutional bar, or tighten/loosen with rationale.
2. Confirm the **periodic conservation audit cadence** (every 100th trial) is acceptable given Block A is otherwise a per-run contract.
3. Confirm **QMC default flip** requires Vlad sign-off (changes the published sample, even if within tolerance), per the constitutional "no improvements without approval" rule.
