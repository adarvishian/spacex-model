# Stub-cell audit baseline

**Generated:** 2026-06-10
**Script:** `scripts/audit_stub_cells.py`
**PRD:** `docs/PRD_Lineage_Trust_and_Monte_Carlo_2026-06-05.md` §10 Sprint 0 (L1.1)
**Model outputs hash:** `0cad99976022195d731db8be822b3006fd452997646d147fe24e67459c0da42a`

## Summary

| Metric | Count |
|--------|------:|
| Grid-renderable sheets walked | 14 |
| Cells with finite display value | 15841 |
| Classified derived/input (non-stub) | 12022 |
| Classified stub (total) | 3819 |
| **Bucket (a)** — placeholder tabs (AI Stack, Valuation) | **3819** |
| **Bucket (b)** — computed-but-unresolved (the bug) | **0** |

## Interpretation

- **Bucket (a):** Genuine stubs on placeholder audit views (`ai_stack`, `valuation`).
- **Bucket (b):** Grid renders a number but `enrich_lineage` returns `cell_kind == "stub"` because `_resolve_cell_context` failed to resolve `computed_value` (4-sheet resolver, exact-label match, accessor gaps — PRD §2.2).
- Sprint 1 target: bucket (b) == 0.

## Bucket (b) breakdown by sheet

| Sheet slug | Count |
|------------|------:|
| *(none)* | 0 |

## Bucket (a) breakdown by sheet

| Sheet slug | Count |
|------------|------:|
| `ai_stack` | 3552 |
| `valuation` | 267 |

## Bucket (b) sample (first 50)

| # | Sheet | Row | Year | Lineage key | Grid value | Label |
|---|-------|-----|------|-------------|------------|-------|

## Bucket (a) sample (first 20)

| # | Sheet | Row | Year | Lineage key | Grid value | Label |
|---|-------|-----|------|-------------|------------|-------|
| 1 | `ai_stack` | R8 | 2025 | `grid.ai_stack.R8.2025` | 483.1 | Revenue |
| 2 | `ai_stack` | R8 | 2026 | `grid.ai_stack.R8.2026` | 1,813 | Revenue |
| 3 | `ai_stack` | R8 | 2027 | `grid.ai_stack.R8.2027` | 6,528 | Revenue |
| 4 | `ai_stack` | R8 | 2028 | `grid.ai_stack.R8.2028` | 8,768 | Revenue |
| 5 | `ai_stack` | R8 | 2029 | `grid.ai_stack.R8.2029` | 1.776e+04 | Revenue |
| 6 | `ai_stack` | R8 | 2030 | `grid.ai_stack.R8.2030` | 4.718e+04 | Revenue |
| 7 | `ai_stack` | R8 | 2031 | `grid.ai_stack.R8.2031` | 1.044e+05 | Revenue |
| 8 | `ai_stack` | R8 | 2032 | `grid.ai_stack.R8.2032` | 1.595e+05 | Revenue |
| 9 | `ai_stack` | R8 | 2033 | `grid.ai_stack.R8.2033` | 1.844e+05 | Revenue |
| 10 | `ai_stack` | R8 | 2034 | `grid.ai_stack.R8.2034` | 2.301e+05 | Revenue |
| 11 | `ai_stack` | R8 | 2035 | `grid.ai_stack.R8.2035` | 3.092e+05 | Revenue |
| 12 | `ai_stack` | R8 | 2036 | `grid.ai_stack.R8.2036` | 4.484e+05 | Revenue |
| 13 | `ai_stack` | R8 | 2037 | `grid.ai_stack.R8.2037` | 6.162e+05 | Revenue |
| 14 | `ai_stack` | R8 | 2038 | `grid.ai_stack.R8.2038` | 7.876e+05 | Revenue |
| 15 | `ai_stack` | R8 | 2039 | `grid.ai_stack.R8.2039` | 1.041e+06 | Revenue |
| 16 | `ai_stack` | R8 | 2040 | `grid.ai_stack.R8.2040` | 1.382e+06 | Revenue |
| 17 | `ai_stack` | R9 | 2025 | `grid.ai_stack.R9.2025` | 51.87 | Module OpEx |
| 18 | `ai_stack` | R9 | 2026 | `grid.ai_stack.R9.2026` | 97.35 | Module OpEx |
| 19 | `ai_stack` | R9 | 2027 | `grid.ai_stack.R9.2027` | 297.8 | Module OpEx |
| 20 | `ai_stack` | R9 | 2028 | `grid.ai_stack.R9.2028` | 406.2 | Module OpEx |

*…and 3799 more (truncated).*
