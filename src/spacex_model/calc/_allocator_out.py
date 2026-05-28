"""Allocator OUT contract — 11 canonical rows per module (Phase A: zeros)."""

from __future__ import annotations

from dataclasses import dataclass

from spacex_model.domain.year_vector import YearVector


@dataclass(frozen=True, slots=True)
class AllocatorOut:
    total_revenue: YearVector
    total_cogs: YearVector
    gross_profit: YearVector
    module_ebitda: YearVector
    module_capex: YearVector
    module_fcf: YearVector
    capital_deployed: YearVector
    capacity_demand_kg: YearVector
    spot_irr: YearVector
    forward_irr: YearVector
    blended_irr: YearVector

    @classmethod
    def zeros(cls) -> AllocatorOut:
        z = YearVector.zeros()
        return cls(
            total_revenue=z,
            total_cogs=z,
            gross_profit=z,
            module_ebitda=z,
            module_capex=z,
            module_fcf=z,
            capital_deployed=z,
            capacity_demand_kg=z,
            spot_irr=z,
            forward_irr=z,
            blended_irr=z,
        )
