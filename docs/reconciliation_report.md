# Reconciliation Report

**Generated:** 2026-06-05 04:01 UTC  
**Run ID:** `fc9a9f22`  
**Phase:** R4 (V4.113 reconciliation + divergence triage)
**Horizon:** 2025–2040

- Solver: **444** iterations, max residual **9.87e-08**, converged **True**

## Block A — Structural invariants

| Invariant | Status | Notes |
|---|---|---|
| Conservation ALL-OK (2025–2040) | PASS | 2025 = OK |
| Module allocation bounds | PASS | Σ cash alloc ≤ available cash |
| Iterative solver convergence | PASS | < 1000 iter, < 1e-07 residual |

## Block B — External calibration anchors (V4.113 ingest + S-1 2025)

| Anchor | Target | Actual | Status |
|---|---:|---:|---|
| Group Revenue 2025 | $14,650M ±5% | $9,808 | see tests |
| Group EBITDA 2025 | $4,904M ±5% | $-2,260 | see tests |
| Group FCF 2025 | −$2,569M ±10% | $-16,630 | see tests |
| Total OpEx 2025 | $4,476M ±5% | $5,758 | see tests |
| Total Group CapEx 2025 | $6,345M ±5% | $14,078 | see tests |
| Mars carve-out 2025 | $1,000M exact | $1,000 | see tests |

## Block C — Sense checks

| Check | Status |
|---|---|
| Starship launches 2025 = 0 | see test_phase_d |
| ODC zero deployment (D6) | RECORDED |
| F9 Blended IRR (D4 disposition) | RECORDED | Expected high; no halt |

## Block D — Architecture spec coverage

| Check | Status |
|---|---|
| Four-tag docstrings on public calc functions | PASS (linter) |
| Canonical label registry completeness | PASS |
| Vending-machine framing (§2.1) | PASS |
| Demand/output decoupling (§2.2) | PASS |

- Inputs hash: `60988f6a8b74a227`

## Diagnostic divergence (xlsx vs code)

- Cells compared: **435**
- Matching: **41**
- Diverging: **394**

## Triage log

- D4: Customer Launch F9 IRR high — expected disposition (type C)
- F1–F6: CAE allocator defects reproduced as-is — remediation U0–U4 (type C)
- V4.113 cached-value divergences: spec-first / first-principles (type C)
