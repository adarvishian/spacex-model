"""Independent per-trial MC sampling — PRD §8.2."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from spacex_model.inputs.assumptions import Assumptions
from spacex_model.inputs.mc_ranges import DistributionType
from spacex_model.inputs.scenarios import apply_assumption_overrides
from spacex_model.mc.distributions import SampledValue, sample_value


@dataclass(frozen=True, slots=True)
class TrialSamples:
    """Sampled overrides for one MC trial."""

    trial_idx: int
    seed: int
    overrides: dict[str, float | dict[int, float]] = field(default_factory=dict)


def _is_variable(meta_distribution: DistributionType | None) -> bool:
    if meta_distribution is None:
        return False
    return meta_distribution not in (
        DistributionType.FIXED,
        DistributionType.FIXED_YEARROW,
    )


def list_variable_labels(assumptions: Assumptions) -> list[str]:
    """Labels with non-fixed MC distributions."""
    out: list[str] = []
    for label, meta in assumptions.mc_ranges.by_label.items():
        if meta.distribution and _is_variable(meta.distribution):
            out.append(label)
    return sorted(out)


def sample_trial(
    assumptions: Assumptions,
    *,
    trial_idx: int,
    base_seed: int = 0,
) -> TrialSamples:
    """Draw independent samples for every variable MC input."""
    seed = base_seed + trial_idx
    rng = np.random.default_rng(seed)
    overrides: dict[str, float | dict[int, float]] = {}

    for label, meta in assumptions.mc_ranges.by_label.items():
        if not meta.distribution or not _is_variable(meta.distribution):
            continue
        row = assumptions.by_label.get(label)
        if row is None:
            continue
        sampled = sample_value(
            meta.distribution,
            base_case=row.base_case,
            year_values=row.year_values,
            mc_min=meta.mc_min,
            mc_max=meta.mc_max,
            mc_notes=meta.mc_notes,
            rng=rng,
        )
        override = _sampled_to_override(sampled)
        if override is not None:
            overrides[label] = override

    return TrialSamples(trial_idx=trial_idx, seed=seed, overrides=overrides)


def _sampled_to_override(sampled: SampledValue) -> float | dict[int, float] | None:
    if sampled.kind == "scalar" and sampled.scalar is not None:
        return sampled.scalar
    if sampled.year_values:
        return sampled.year_values
    return None


def apply_trial_samples(
    base_assumptions: Assumptions,
    trial: TrialSamples,
) -> Assumptions:
    """Return Assumptions with trial overrides applied."""
    if not trial.overrides:
        return base_assumptions
    return apply_assumption_overrides(base_assumptions, trial.overrides)


def samples_to_input_matrix(
    trials: list[TrialSamples],
    labels: list[str],
) -> np.ndarray:
    """Matrix (n_trials × n_inputs) of scalar samples for PRCC / diagnostics."""
    mat = np.zeros((len(trials), len(labels)), dtype=np.float64)
    for i, trial in enumerate(trials):
        for j, label in enumerate(labels):
            val = trial.overrides.get(label)
            if isinstance(val, dict):
                mat[i, j] = float(next(iter(val.values()), 0.0))
            elif isinstance(val, (int, float)):
                mat[i, j] = float(val)
    return mat
