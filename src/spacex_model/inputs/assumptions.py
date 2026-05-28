"""Pydantic Assumptions schema — 11 sections per PRD §5.1 / Assumptions Tab Spec."""

from __future__ import annotations

from typing import Any

import numpy as np
from pydantic import BaseModel, Field, field_validator

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS
from spacex_model.inputs.mc_ranges import DistributionType, MCInputMeta, MCRanges
from spacex_model.io.excel_ingest import AssumptionRowRecord, IngestResult


class AssumptionInput(BaseModel):
    """Single Assumptions row — scalar or year-row."""

    label: str
    section: str
    base_case: float | str | None = None
    year_values: dict[int, float | str | None] = Field(default_factory=dict)
    notes: str | None = None

    model_config = {"frozen": True}

    def as_year_vector(self) -> np.ndarray:
        """Return length-26 float vector; missing years filled from base_case or 0."""
        vec = np.zeros(HORIZON_YEARS, dtype=np.float64)
        for year in range(FIRST_YEAR, FIRST_YEAR + HORIZON_YEARS):
            idx = year - FIRST_YEAR
            if year in self.year_values and self.year_values[year] is not None:
                val = self.year_values[year]
                vec[idx] = float(val) if isinstance(val, (int, float)) else 0.0
            elif self.base_case is not None and isinstance(self.base_case, (int, float)):
                vec[idx] = float(self.base_case)
        return vec

    def scalar(self) -> float | None:
        if isinstance(self.base_case, (int, float)):
            return float(self.base_case)
        if self.year_values:
            y0 = self.year_values.get(FIRST_YEAR)
            if isinstance(y0, (int, float)):
                return float(y0)
        return None


class AssumptionsSection(BaseModel):
    """One logical section of the Assumptions tab."""

    section_id: str
    inputs: dict[str, AssumptionInput] = Field(default_factory=dict)

    model_config = {"frozen": True}

    def get(self, label: str) -> AssumptionInput | None:
        return self.inputs.get(label)

    def require_scalar(self, label: str) -> float:
        row = self.inputs.get(label)
        if row is None:
            msg = f"Missing Assumptions input: {label!r}"
            raise KeyError(msg)
        value = row.scalar()
        if value is None:
            msg = f"Assumptions input {label!r} has no scalar value"
            raise ValueError(msg)
        return value


def _section_key(raw: str) -> str:
    if raw.startswith("§"):
        token = raw.split(maxsplit=1)[0]  # e.g. "§1", "§2"
        return token.lower().replace("§", "section_")
    return "section_unassigned"


class GlobalAssumptions(AssumptionsSection):
    section_id: str = "section_1"


class AllocatorAssumptions(AssumptionsSection):
    section_id: str = "section_2"


class CapacityAssumptions(AssumptionsSection):
    section_id: str = "section_3"


class CustomerLaunchAssumptions(AssumptionsSection):
    section_id: str = "section_4"


class StarlinkAssumptions(AssumptionsSection):
    section_id: str = "section_5"


class ODCAssumptions(AssumptionsSection):
    section_id: str = "section_6"


class AIStackAssumptions(AssumptionsSection):
    section_id: str = "section_7"


class LunarMarsAssumptions(AssumptionsSection):
    section_id: str = "section_8"


class OpExAssumptions(AssumptionsSection):
    section_id: str = "section_9"


class CapExAssumptions(AssumptionsSection):
    section_id: str = "section_10"


class ValuationAssumptions(AssumptionsSection):
    section_id: str = "section_11"


SECTION_MODELS: dict[str, type[AssumptionsSection]] = {
    "section_1": GlobalAssumptions,
    "section_2": AllocatorAssumptions,
    "section_3": CapacityAssumptions,
    "section_4": CustomerLaunchAssumptions,
    "section_5": StarlinkAssumptions,
    "section_6": ODCAssumptions,
    "section_7": AIStackAssumptions,
    "section_8": LunarMarsAssumptions,
    "section_9": OpExAssumptions,
    "section_10": CapExAssumptions,
    "section_11": ValuationAssumptions,
}


class Assumptions(BaseModel):
    """Full Assumptions ingest with 11 nested sections."""

    global_: GlobalAssumptions = Field(default_factory=GlobalAssumptions)
    allocator: AllocatorAssumptions = Field(default_factory=AllocatorAssumptions)
    capacity: CapacityAssumptions = Field(default_factory=CapacityAssumptions)
    customer_launch: CustomerLaunchAssumptions = Field(default_factory=CustomerLaunchAssumptions)
    starlink: StarlinkAssumptions = Field(default_factory=StarlinkAssumptions)
    odc: ODCAssumptions = Field(default_factory=ODCAssumptions)
    ai_stack: AIStackAssumptions = Field(default_factory=AIStackAssumptions)
    lunar_mars: LunarMarsAssumptions = Field(default_factory=LunarMarsAssumptions)
    opex: OpExAssumptions = Field(default_factory=OpExAssumptions)
    capex: CapExAssumptions = Field(default_factory=CapExAssumptions)
    valuation: ValuationAssumptions = Field(default_factory=ValuationAssumptions)
    mc_ranges: MCRanges = Field(default_factory=MCRanges)
    by_label: dict[str, AssumptionInput] = Field(default_factory=dict)

    model_config = {"frozen": True}

    @field_validator("global_", mode="before")
    @classmethod
    def _default_global(cls, v: Any) -> Any:
        return v or GlobalAssumptions(section_id="section_1")

    def lookup(self, label: str) -> AssumptionInput | None:
        return self.by_label.get(label)

    def lookup_scalar(self, label: str, default: float | None = None) -> float:
        row = self.by_label.get(label)
        if row is None:
            if default is not None:
                return default
            msg = f"Unknown Assumptions label: {label!r}"
            raise KeyError(msg)
        value = row.scalar()
        if value is None:
            if default is not None:
                return default
            msg = f"No scalar for label: {label!r}"
            raise ValueError(msg)
        return value

    @property
    def tax_rate(self) -> float:
        return self.global_.require_scalar("Tax rate (corporate, US federal + state blended)")

    @property
    def starting_cash_eoy_2024(self) -> float:
        return self.allocator.require_scalar("Starting cash position EoY 2024 ($mm)")


def _parse_distribution(raw: str | None) -> DistributionType | None:
    if not raw:
        return None
    try:
        return DistributionType(raw.strip().lower())
    except ValueError:
        return None


def _rows_to_sections(rows: list[AssumptionRowRecord]) -> dict[str, dict[str, AssumptionInput]]:
    buckets: dict[str, dict[str, AssumptionInput]] = {}
    current_section = "section_unassigned"
    for row in rows:
        if row.label.startswith("§"):
            current_section = _section_key(row.label)
            buckets.setdefault(current_section, {})
            continue
        section_id = _section_key(row.section) if row.section.startswith("§") else current_section
        inp = AssumptionInput(
            label=row.label,
            section=row.section,
            base_case=row.base_case,
            year_values=row.year_values,
            notes=row.notes,
        )
        buckets.setdefault(section_id, {})[row.label] = inp
    return buckets


def assumptions_from_ingest(ingest: IngestResult) -> Assumptions:
    """Build Assumptions + MCRanges from an excel ingest result."""
    buckets = _rows_to_sections(ingest.value_pass.assumptions_rows)
    by_label: dict[str, AssumptionInput] = {}
    for section_inputs in buckets.values():
        by_label.update(section_inputs)

    mc_by_label: dict[str, MCInputMeta] = {}
    for row in ingest.value_pass.assumptions_rows:
        if row.distribution:
            mc_by_label[row.label] = MCInputMeta(
                label=row.label,
                distribution=_parse_distribution(row.distribution),
                mc_min=row.mc_min if isinstance(row.mc_min, (int, float)) else None,
                mc_max=row.mc_max if isinstance(row.mc_max, (int, float)) else None,
                mc_notes=row.mc_notes,
            )

    def _section(name: str, model: type[AssumptionsSection]) -> AssumptionsSection:
        return model(section_id=name, inputs=buckets.get(name, {}))

    return Assumptions(
        global_=_section("section_1", GlobalAssumptions),
        allocator=_section("section_2", AllocatorAssumptions),
        capacity=_section("section_3", CapacityAssumptions),
        customer_launch=_section("section_4", CustomerLaunchAssumptions),
        starlink=_section("section_5", StarlinkAssumptions),
        odc=_section("section_6", ODCAssumptions),
        ai_stack=_section("section_7", AIStackAssumptions),
        lunar_mars=_section("section_8", LunarMarsAssumptions),
        opex=_section("section_9", OpExAssumptions),
        capex=_section("section_10", CapExAssumptions),
        valuation=_section("section_11", ValuationAssumptions),
        mc_ranges=MCRanges(by_label=mc_by_label),
        by_label=by_label,
    )
