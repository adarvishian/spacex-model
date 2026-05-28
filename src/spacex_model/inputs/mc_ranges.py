"""Monte Carlo range metadata — populated from Assumptions MC columns."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class DistributionType(str, Enum):
    FIXED = "fixed"
    TRIANGLE = "triangle"
    LOGNORMAL = "lognormal"
    UNIFORM = "uniform"
    DISCRETE = "discrete"
    TRIANGLE_YEARROW = "triangle-yearrow"
    FIXED_YEARROW = "fixed-yearrow"


class MCInputMeta(BaseModel):
    label: str
    distribution: DistributionType | None = None
    mc_min: float | None = None
    mc_max: float | None = None
    mc_notes: str | None = None

    model_config = {"frozen": True}


class MCRanges(BaseModel):
    """MC metadata keyed by Assumptions label."""

    by_label: dict[str, MCInputMeta] = Field(default_factory=dict)

    model_config = {"frozen": True}
