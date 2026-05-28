"""Pydantic request/response models for FastAPI — Phase G."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class DeterministicRunRequest(BaseModel):
    scenario: str = "base_case"
    overrides: dict[str, Any] = Field(default_factory=dict)
    client_overrides: dict[str, float] = Field(default_factory=dict)
    use_cache: bool = True


class McSubmitRequest(BaseModel):
    trials: int = Field(default=10_000, ge=1, le=100_000)
    base_seed: int = 42
    n_jobs: int = -1
    scenario: str = "base_case"
    include_tornado: bool = False
    tornado_top: int = Field(default=10, ge=1, le=50)


class OverrideWarning(BaseModel):
    label: str
    value: float
    message: str


class ScenarioInfo(BaseModel):
    name: str
    description: str
    path: str


class ExportScenarioRequest(BaseModel):
    run_id: str | None = None
    scenario: str = "base_case"
    overrides: dict[str, float] = Field(default_factory=dict)
    public_base_url: str = ""


class ExportScenarioPackRequest(BaseModel):
    scenarios: list[str] = Field(default_factory=lambda: ["base_case", "bear", "bull"])
    public_base_url: str = ""


class ClientShareValidateRequest(BaseModel):
    scenario: str = "base_case"
    overrides: dict[str, float] = Field(default_factory=dict)
