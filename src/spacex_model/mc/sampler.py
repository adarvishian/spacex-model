"""Independent per-trial MC sampling — PRD §8.2."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np
from scipy.stats import qmc

from spacex_model.inputs.assumptions import Assumptions
from spacex_model.inputs.mc_ranges import DistributionType
from spacex_model.inputs.scenarios import apply_assumption_overrides
from spacex_model.mc.distributions import SampledValue, inverse_cdf_value, sample_value

SamplingMode = Literal["mc", "qmc"]


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


def _sample_label(
    assumptions: Assumptions,
    label: str,
    *,
    rng: np.random.Generator | None = None,
    u: float | None = None,
) -> float | dict[int, float] | None:
    meta = assumptions.mc_ranges.by_label.get(label)
    if meta is None or not meta.distribution or not _is_variable(meta.distribution):
        return None
    row = assumptions.by_label.get(label)
    if row is None:
        return None
    if u is not None:
        sampled = inverse_cdf_value(
            meta.distribution,
            u,
            base_case=row.base_case,
            year_values=row.year_values,
            mc_min=meta.mc_min,
            mc_max=meta.mc_max,
            mc_notes=meta.mc_notes,
        )
    else:
        assert rng is not None
        sampled = sample_value(
            meta.distribution,
            base_case=row.base_case,
            year_values=row.year_values,
            mc_min=meta.mc_min,
            mc_max=meta.mc_max,
            mc_notes=meta.mc_notes,
            rng=rng,
        )
    return _sampled_to_override(sampled)


def generate_sobol_unit_cube(
    n_trials: int,
    d: int,
    *,
    base_seed: int,
) -> np.ndarray:
    """Scrambled Sobol points in [0, 1)^d; n_trials rounded up to next power of two."""
    if d <= 0:
        return np.empty((n_trials, 0), dtype=np.float64)
    m = int(np.ceil(np.log2(max(n_trials, 1))))
    n_sobol = 2**m
    engine = qmc.Sobol(d=d, scramble=True, seed=base_seed)
    points = engine.random(n_sobol)
    return points[:n_trials]


def sample_trial(
    assumptions: Assumptions,
    *,
    trial_idx: int,
    base_seed: int = 0,
    sampling: SamplingMode = "mc",
    qmc_point: np.ndarray | None = None,
) -> TrialSamples:
    """Draw independent samples for every variable MC input."""
    seed = base_seed + trial_idx
    overrides: dict[str, float | dict[int, float]] = {}
    labels = list_variable_labels(assumptions)

    if sampling == "qmc":
        if qmc_point is None:
            qmc_point = generate_sobol_unit_cube(trial_idx + 1, len(labels), base_seed=base_seed)[trial_idx]
        for i, label in enumerate(labels):
            override = _sample_label(assumptions, label, u=float(qmc_point[i]))
            if override is not None:
                overrides[label] = override
    else:
        rng = np.random.default_rng(seed)
        for label in labels:
            override = _sample_label(assumptions, label, rng=rng)
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
