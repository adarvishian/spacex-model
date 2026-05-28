# Reconciliation Report

**Generated:** 2026-05-28 18:39 UTC  
**Run ID:** `d06cddda`  
**Phase:** E (Reconciliation hardening + divergence report)

- Solver: **112** iterations, max residual **0.000982**, converged **True**

## Block A — Structural invariants

| Invariant | Status | Notes |
|---|---|---|
| R108 conservation (2025-2050) | PASS | 2025 = OK |
| Module allocation bounds | PASS | Σ cash alloc ≤ available cash |
| Iterative solver convergence | PASS | < 100 iter, < 0.001 residual |

## Block B — External calibration anchors (Sprint §6.8 revised)

| Anchor | Target | Actual | Status |
|---|---:|---:|---|
| Group Revenue 2025 | $14,650M ±5% | $17,627 | see tests |
| Group EBITDA 2025 | $4,904M ±5% | $4,172 | see tests |
| Group FCF 2025 | −$2,569M ±10% | $-11,040 | see tests |
| Total OpEx 2025 | $4,476M ±5% | $5,301 | see tests |
| Total Group CapEx 2025 | $6,345M ±5% | $14,069 | see tests |
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

- Inputs hash: `0bdaf067ff312ac8`

## Diagnostic divergence (xlsx vs code)

- Cells compared: **2730**
- Matching: **1171**
- Diverging: **1559**

## Triage log

- D4: Customer Launch F9 IRR high — expected disposition (type C)
- D6: ODC zero deployment — expected disposition (type C)
- D2: Sprint 11f Option A allocator demand/allocation — preregistered type (C)
