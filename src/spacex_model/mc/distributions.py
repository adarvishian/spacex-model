"""MC distribution samplers — seven types per PRD §8.1 / context.md §9.1."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy import stats

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.inputs.mc_ranges import DistributionType

SampleKind = Literal["scalar", "yearrow_multiplier", "yearrow_fixed"]


@dataclass(frozen=True, slots=True)
class SampledValue:
    """A sampled Assumptions override for one label."""

    kind: SampleKind
    scalar: float | None = None
    year_values: dict[int, float] | None = None


def _base_scalar(base_case: float | str | None, year_values: dict[int, float | str | None]) -> float:
    if isinstance(base_case, (int, float)):
        return float(base_case)
    y0 = year_values.get(FIRST_YEAR)
    if isinstance(y0, (int, float)):
        return float(y0)
    for v in year_values.values():
        if isinstance(v, (int, float)) and v != 0:
            return float(v)
    return 0.0


def fit_lognorm_from_p10_p90(p10: float, p90: float) -> stats.rv_continuous:
    """Fit scipy lognorm so P10 and P90 match MC Min/Max anchors."""
    if p10 <= 0 or p90 <= 0:
        msg = f"lognormal requires positive bounds: p10={p10}, p90={p90}"
        raise ValueError(msg)
    z10 = stats.norm.ppf(0.10)
    z90 = stats.norm.ppf(0.90)
    log_sigma = (math.log(p90) - math.log(p10)) / (z90 - z10)
    log_mu = math.log(p10) - log_sigma * z10
    return stats.lognorm(s=log_sigma, scale=math.exp(log_mu))


def triangle_distribution(
    low: float,
    mode: float,
    high: float,
) -> stats.triang:
    """scipy.stats.triang with Excel-style min / mode / max."""
    if high <= low:
        return stats.triang(c=0.5, loc=low, scale=max(high - low, 1e-12))
    c = (mode - low) / (high - low)
    c = min(max(c, 0.0), 1.0)
    return stats.triang(c=c, loc=low, scale=high - low)


def distribution_std(
    distribution: DistributionType,
    *,
    base: float,
    low: float | None,
    high: float | None,
) -> float:
    """Approximate 1σ spread for tornado ±1σ perturbations."""
    if distribution in (DistributionType.FIXED, DistributionType.FIXED_YEARROW):
        return 0.0
    lo = low if low is not None else base * 0.9
    hi = high if high is not None else base * 1.1
    if distribution == DistributionType.TRIANGLE:
        return float(triangle_distribution(lo, base, hi).std())
    if distribution == DistributionType.UNIFORM:
        return float(stats.uniform(loc=lo, scale=hi - lo).std())
    if distribution == DistributionType.LOGNORMAL and lo > 0 and hi > 0:
        return float(fit_lognorm_from_p10_p90(lo, hi).std())
    if distribution == DistributionType.TRIANGLE_YEARROW:
        m_lo = lo / base if base else lo
        m_hi = hi / base if base else hi
        return float(triangle_distribution(m_lo, 1.0, m_hi).std()) * abs(base)
    return abs(hi - lo) / 6.0


def parse_discrete_choices(
    *,
    mc_min: float | None,
    mc_max: float | None,
    mc_notes: str | None,
    base: float,
) -> list[float]:
    """Resolve discrete option list from MC metadata."""
    if mc_notes:
        nums = [float(x) for x in re.findall(r"-?\d+\.?\d*", mc_notes)]
        if len(nums) >= 2:
            return nums
    choices: list[float] = []
    if mc_min is not None:
        choices.append(float(mc_min))
    if mc_max is not None and mc_max not in choices:
        choices.append(float(mc_max))
    if len(choices) >= 2:
        return choices
    return [base]


def sample_value(
    distribution: DistributionType,
    *,
    base_case: float | str | None,
    year_values: dict[int, float | str | None],
    mc_min: float | None,
    mc_max: float | None,
    mc_notes: str | None = None,
    rng: np.random.Generator,
) -> SampledValue:
    """Draw one sample for an Assumptions row."""
    base = _base_scalar(base_case, year_values)
    lo = float(mc_min) if mc_min is not None else base
    hi = float(mc_max) if mc_max is not None else base
    if lo > hi:
        lo, hi = hi, lo

    if distribution == DistributionType.FIXED:
        return SampledValue(kind="scalar", scalar=base)

    if distribution == DistributionType.FIXED_YEARROW:
        yv = {
            y: float(v) for y, v in year_values.items() if isinstance(v, (int, float))
        }
        return SampledValue(kind="yearrow_fixed", year_values=yv)

    if distribution == DistributionType.TRIANGLE_YEARROW:
        m_lo = lo / base if base else lo
        m_hi = hi / base if base else hi
        mult = float(triangle_distribution(m_lo, 1.0, m_hi).rvs(random_state=rng))
        yv = {}
        for year, val in year_values.items():
            if isinstance(val, (int, float)):
                yv[year] = float(val) * mult
            elif isinstance(base_case, (int, float)):
                yv[year] = float(base_case) * mult
        if not yv and isinstance(base_case, (int, float)):
            yv = {y: float(base_case) * mult for y in range(FIRST_YEAR, FIRST_YEAR + HORIZON_YEARS)}
        return SampledValue(kind="yearrow_multiplier", year_values=yv)

    if distribution == DistributionType.DISCRETE:
        choices = parse_discrete_choices(mc_min=mc_min, mc_max=mc_max, mc_notes=mc_notes, base=base)
        return SampledValue(kind="scalar", scalar=float(rng.choice(choices)))

    if distribution == DistributionType.TRIANGLE:
        return SampledValue(kind="scalar", scalar=float(triangle_distribution(lo, base, hi).rvs(random_state=rng)))

    if distribution == DistributionType.UNIFORM:
        return SampledValue(kind="scalar", scalar=float(stats.uniform(loc=lo, scale=hi - lo).rvs(random_state=rng)))

    if distribution == DistributionType.LOGNORMAL:
        return SampledValue(
            kind="scalar",
            scalar=float(fit_lognorm_from_p10_p90(lo, hi).rvs(random_state=rng)),
        )

    return SampledValue(kind="scalar", scalar=base)


def reference_percentiles(
    distribution: DistributionType,
    *,
    base: float,
    low: float,
    high: float,
    n_samples: int = 10_000,
    seed: int = 0,
) -> dict[str, float]:
    """Empirical P10/P50/P90 from the implementation sampler (validation helper)."""
    rng = np.random.default_rng(seed)
    draws: list[float] = []
    year_stub = {FIRST_YEAR: base}
    for _ in range(n_samples):
        if distribution == DistributionType.FIXED:
            draws.append(base)
            continue
        if distribution == DistributionType.FIXED_YEARROW:
            draws.append(base)
            continue
        sv = sample_value(
            distribution,
            base_case=base,
            year_values=year_stub,
            mc_min=low,
            mc_max=high,
            rng=rng,
        )
        if sv.scalar is not None:
            draws.append(sv.scalar)
        elif sv.year_values:
            draws.append(next(iter(sv.year_values.values())))
    arr = np.asarray(draws, dtype=np.float64)
    return {
        "p10": float(np.percentile(arr, 10)),
        "p50": float(np.percentile(arr, 50)),
        "p90": float(np.percentile(arr, 90)),
    }


def scipy_reference_percentiles(
    distribution: DistributionType,
    *,
    base: float,
    low: float,
    high: float,
    n_samples: int = 10_000,
    seed: int = 0,
) -> dict[str, float]:
    """Direct scipy/numpy reference for distribution validation tests."""
    rng = np.random.default_rng(seed)
    if distribution == DistributionType.TRIANGLE:
        dist = triangle_distribution(low, base, high)
        arr = dist.rvs(size=n_samples, random_state=rng)
    elif distribution == DistributionType.UNIFORM:
        arr = stats.uniform(loc=low, scale=high - low).rvs(size=n_samples, random_state=rng)
    elif distribution == DistributionType.LOGNORMAL:
        arr = fit_lognorm_from_p10_p90(low, high).rvs(size=n_samples, random_state=rng)
    elif distribution == DistributionType.DISCRETE:
        arr = rng.choice([low, high], size=n_samples)
    else:
        arr = np.full(n_samples, base)
    return {
        "p10": float(np.percentile(arr, 10)),
        "p50": float(np.percentile(arr, 50)),
        "p90": float(np.percentile(arr, 90)),
    }
