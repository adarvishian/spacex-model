"""Fixed-point iterative solver — Phase D damped convergence per PRD §6."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

from spacex_model.config.constants import (
    SOLVER_DAMPING,
    SOLVER_MAX_ITERATIONS,
    SOLVER_TOLERANCE,
)


class NonConvergenceError(RuntimeError):
    """Raised when the solver exceeds max iterations without meeting tolerance."""

    def __init__(self, message: str, *, diagnostic_trace: list[dict[str, Any]] | None = None) -> None:
        super().__init__(message)
        self.diagnostic_trace = diagnostic_trace or []


@dataclass
class SolverTrace:
    iterations: int
    converged: bool
    max_residual: float
    per_iteration: list[dict[str, Any]] = field(default_factory=list)


def damped_blend(
    prior: np.ndarray,
    proposed: np.ndarray,
    *,
    alpha: float,
) -> np.ndarray:
    """Convex blend: alpha × proposed + (1 − alpha) × prior."""
    return alpha * proposed + (1.0 - alpha) * prior


def max_abs_delta(prior: dict[str, np.ndarray], proposed: dict[str, np.ndarray]) -> tuple[float, str]:
    """Max absolute delta across monitored quantity vectors."""
    max_residual = 0.0
    holder = ""
    for key, proposed_vec in proposed.items():
        prior_vec = prior.get(key)
        if prior_vec is None:
            delta = float(np.max(np.abs(proposed_vec)))
        else:
            delta = float(np.max(np.abs(proposed_vec - prior_vec)))
        if delta > max_residual:
            max_residual = delta
            holder = key
    return max_residual, holder


def solve_fixed_point(
    initial_state: dict[str, Any],
    single_pass: Callable[[dict[str, Any]], dict[str, Any]],
    *,
    max_iterations: int = SOLVER_MAX_ITERATIONS,
    tolerance: float = SOLVER_TOLERANCE,
    damping: float = SOLVER_DAMPING,
    extract_monitored: Callable[[dict[str, Any]], dict[str, np.ndarray]] | None = None,
) -> tuple[dict[str, Any], SolverTrace]:
    """Damped fixed-point iteration until max monitored residual < tolerance.

    Excel cell:        — (solver orchestrator)
    Excel label:       "Iterative calc convergence"
    Architecture ref:  §6.2 / Memory 1.6
    Principle:         22 (Mars t−1 read breaks Cash BoY ↔ FCF loop)

    """
    if extract_monitored is None:
        extract_monitored = lambda state: {"state": np.array([0.0])}

    state = dict(initial_state)
    prior_monitored = extract_monitored(state)
    trace: list[dict[str, Any]] = []
    converged = False
    iterations = 0
    max_residual = 0.0

    for iter_idx in range(max_iterations):
        proposed_state = single_pass(state)
        proposed_monitored = extract_monitored(proposed_state)
        max_residual, holder = max_abs_delta(prior_monitored, proposed_monitored)
        trace.append(
            {
                "iter": iter_idx,
                "max_residual": max_residual,
                "residual_holder_quantity": holder,
            }
        )

        if max_residual < tolerance:
            state = proposed_state
            converged = True
            iterations = iter_idx + 1
            break

        blended_monitored: dict[str, np.ndarray] = {}
        for key, proposed_vec in proposed_monitored.items():
            prior_vec = prior_monitored.get(key, proposed_vec)
            blended_monitored[key] = damped_blend(prior_vec, proposed_vec, alpha=damping)

        state = {**proposed_state, "monitored_blend": blended_monitored}
        prior_monitored = blended_monitored
        iterations = iter_idx + 1

    if not converged:
        raise NonConvergenceError(
            f"Solver did not converge in {max_iterations} iterations "
            f"(max_residual={max_residual:.6f}, holder={trace[-1]['residual_holder_quantity']})",
            diagnostic_trace=trace,
        )

    solver_trace = SolverTrace(
        iterations=iterations,
        converged=converged,
        max_residual=max_residual,
        per_iteration=trace,
    )
    return state, solver_trace
