"""Ingest-time cross-checks against S-1 audited anchors (warnings only)."""

from __future__ import annotations

from spacex_model.inputs.assumptions import Assumptions
from spacex_model.inputs.s1_2025_anchors import S1_INGEST_ANCHORS_2025


def _check_anchors(assumptions: Assumptions, anchors: tuple) -> list[str]:
    warnings: list[str] = []
    for anchor in anchors:
        if not anchor.assumptions_label:
            continue
        try:
            row = assumptions.by_label[anchor.assumptions_label]
            actual = row.scalar()
            if actual is None and row.year_values.get(2025) is not None:
                y0 = row.year_values[2025]
                actual = float(y0) if isinstance(y0, (int, float)) else None
            if actual is None:
                raise ValueError("no value")
        except (KeyError, ValueError):
            warnings.append(f"Anchor {anchor.name}: label {anchor.assumptions_label!r} not found")
            continue
        if anchor.tolerance_pct == 0:
            if abs(actual - anchor.target) > 1e-6:
                warnings.append(
                    f"Anchor {anchor.name}: expected {anchor.target}, got {actual}"
                )
        else:
            rel = abs(actual - anchor.target) / abs(anchor.target)
            if rel > anchor.tolerance_pct:
                warnings.append(
                    f"Anchor {anchor.name}: expected {anchor.target}, got {actual} "
                    f"(rel err {rel:.1%} > tol {anchor.tolerance_pct:.1%})"
                )
    return warnings


def check_s1_anchors(assumptions: Assumptions) -> list[str]:
    """Return warning strings when Assumptions Base Case drifts from S-1 anchors."""
    return _check_anchors(assumptions, S1_INGEST_ANCHORS_2025)


def check_q4_25_anchors(assumptions: Assumptions) -> list[str]:
    """Deprecated alias — use check_s1_anchors."""
    return check_s1_anchors(assumptions)
