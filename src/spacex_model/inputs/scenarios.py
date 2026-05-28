"""Scenario YAML loader and Assumptions override application — Phase E."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from spacex_model.inputs.assumptions import AssumptionInput, Assumptions, AssumptionsSection


class ScenarioSpec(BaseModel):
    """Parsed scenario file per context.md §8.2."""

    name: str
    description: str = ""
    baseline_workbook: str = ""
    overrides: dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


def load_scenario(path: Path) -> ScenarioSpec:
    """Load a scenario YAML file."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        msg = f"Invalid scenario file: {path}"
        raise ValueError(msg)
    return ScenarioSpec.model_validate(raw)


def _normalize_override(raw: Any) -> dict[str, Any]:
    """Accept scalar or {base_case, year_values} override shapes."""
    if isinstance(raw, dict):
        update: dict[str, Any] = {}
        if "base_case" in raw:
            update["base_case"] = raw["base_case"]
        if "year_values" in raw:
            year_values = raw["year_values"]
            if isinstance(year_values, dict):
                update["year_values"] = {int(k): v for k, v in year_values.items()}
        if update:
            return update
        if raw and all(isinstance(k, int) for k in raw):
            return {"year_values": {int(k): v for k, v in raw.items()}}
    if isinstance(raw, (int, float, str)):
        return {"base_case": raw}
    msg = f"Unsupported override value type: {type(raw)!r}"
    raise TypeError(msg)


def _rebuild_section(section: AssumptionsSection, by_label: dict[str, AssumptionInput]) -> AssumptionsSection:
    return section.model_copy(
        update={"inputs": {label: by_label[label] for label in section.inputs if label in by_label}}
    )


def apply_assumption_overrides(
    assumptions: Assumptions,
    overrides: dict[str, Any],
) -> Assumptions:
    """Return a new Assumptions with scenario overrides applied."""
    if not overrides:
        return assumptions

    new_by_label: dict[str, AssumptionInput] = dict(assumptions.by_label)
    for label, raw_override in overrides.items():
        existing = new_by_label.get(label)
        if existing is None:
            msg = f"Scenario override references unknown Assumptions label: {label!r}"
            raise KeyError(msg)
        new_by_label[label] = existing.model_copy(update=_normalize_override(raw_override))

    return Assumptions(
        global_=_rebuild_section(assumptions.global_, new_by_label),
        allocator=_rebuild_section(assumptions.allocator, new_by_label),
        capacity=_rebuild_section(assumptions.capacity, new_by_label),
        customer_launch=_rebuild_section(assumptions.customer_launch, new_by_label),
        starlink=_rebuild_section(assumptions.starlink, new_by_label),
        odc=_rebuild_section(assumptions.odc, new_by_label),
        ai_stack=_rebuild_section(assumptions.ai_stack, new_by_label),
        lunar_mars=_rebuild_section(assumptions.lunar_mars, new_by_label),
        opex=_rebuild_section(assumptions.opex, new_by_label),
        capex=_rebuild_section(assumptions.capex, new_by_label),
        valuation=_rebuild_section(assumptions.valuation, new_by_label),
        mc_ranges=assumptions.mc_ranges,
        by_label=new_by_label,
    )
