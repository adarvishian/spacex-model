# Reconciliation Report

**Generated:** 2026-06-10 18:16 UTC  
**Run ID:** `6b0dcaf7`  
**Phase:** R4 (V4.131 reconciliation + divergence triage)
**Horizon:** 2025–2040

- Solver: **135** iterations, max residual **8.69e-08**, converged **True**

## Block A — Structural invariants

| Invariant | Status | Notes |
|---|---|---|
| Conservation ALL-OK (2025–2040) | PASS | 2025 = OK |
| Module allocation bounds | PASS | Σ cash alloc ≤ available cash |
| Iterative solver convergence | PASS | < 1000 iter, < 1e-07 residual |

## Block B — Calibration burn-down (S-1 disclosure)

**Enforced:** 5/15 anchors  
**Pending:** 10 anchors (xfail strict-on-fix in CI)

| Anchor | Target | Actual | Status | Enforcement |
|---|---:|---:|---|---|
| Group Revenue 2025 | $18,674M | $9,808 | PENDING | pending (xfail) |
| Space segment revenue 2025 | $4,086M | $7,096 | PENDING | pending (xfail) |
| Connectivity segment revenue 2025 | $11,387M | $1,834 | PENDING | pending (xfail) |
| AI segment revenue 2025 | $3,201M | $3,201 | PASS | strict |
| F9 customer launches 2025 | $43M | $43 | PASS | strict |
| Starting cash EoY 2024 | $11,385M | $11,385 | PASS | strict |
| Total Group CapEx 2025 | $20,737M | $14,057 | PENDING | pending (xfail) |
| Group Gross Profit 2025 | $9,223M | $3,498 | PENDING | pending (xfail) |
| Group EBITDA 2025 | $6,584M | $1,010 | PENDING | pending (xfail) |
| Group D&A 2025 | $6,701M | $828 | PENDING | pending (xfail) |
| Group FCF 2025 | $-13,952M | $-13,526 | PASS | strict |
| Total OpEx 2025 | $11,287M | $2,488 | PENDING | pending (xfail) |
| Cash EoY 2025 | $24,747M | $-2,141 | PENDING | pending (xfail) |
| Adjusted EBITDA 2025 | $6,584M | $3,785 | PENDING | pending (xfail) |
| Mars carve-out 2025 | $1,000M | $1,000 | PASS | strict |

> Provenance: S-1 audited 2025 disclosure (`inputs/block_b_anchors.py`). Pending anchors are work-in-progress, not regressions.

## Block B — V4.131 ingest anchors (Assumptions frozen inputs)

| Anchor | Target | Actual | Status |
|---|---:|---:|---|
| Tax rate | 0.21 | 0.21 | PASS |
| Broadband ARPU 2025 | 81 | 81 | PASS |
| F9 customer launch price 2025 | 54.8 | 54.8 | PASS |
| AI segment total revenue 2025 | 3,201 | 3,201 | PASS |

> Provenance: V4.131 Assumptions tab (`inputs/v4_131_2025_anchors.py`). Input-freeze checks, distinct from S-1 disclosure roll-ups above.

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

- Inputs hash: `711111f0a8d0325e`

## Diagnostic divergence (xlsx vs code)

- Cells compared: **530**
- Matching: **57**
- Diverging: **473**

## Triage log

- D4: Customer Launch F9 IRR high — expected disposition (type C)
- F1–F6: CAE allocator defects reproduced as-is — remediation U0–U4 (type C)
- V4.131 cached-value divergences: spec-first / first-principles (type C)
