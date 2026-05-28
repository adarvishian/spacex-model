"""JSON serializers for API responses — Phase G."""

from __future__ import annotations

import math
from typing import Any

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR
from spacex_model.domain.year_vector import YearVector
from spacex_model.engine.pipeline import ModelResult
from spacex_model.mc.aggregator import McAggregation
from spacex_model.mc.sensitivity import TornadoBar
from spacex_model.service.lineage import get_lineage_registry

_MODULE_KEYS = ("customer_launch", "starlink", "odc", "ai_stack", "lunar_mars")
_MODULE_DISPLAY = {
    "customer_launch": "Customer Launch",
    "starlink": "Starlink",
    "odc": "ODC",
    "ai_stack": "AI Stack",
    "lunar_mars": "Lunar Mars",
}
_YEARS = list(range(FIRST_YEAR, LAST_YEAR + 1))


def _year_series(
    label: str,
    vec: YearVector,
    *,
    lineage_key: str,
    unit: str = "$mm",
) -> dict[str, Any]:
    return {
        "label": label,
        "unit": unit,
        "years": _YEARS,
        "values": [float(v) for v in vec.values],
        "lineage_key": lineage_key,
    }


def serialize_model_result(result: ModelResult, *, cached: bool = False) -> dict[str, Any]:
    """Full deterministic run payload for API / cache."""
    group = result.group_pnl
    val = result.valuation
    mods = result.module_outputs

    group_rows = {
        "group_revenue_net": _year_series(
            "Group Revenue (net)",
            group.group_revenue_net,
            lineage_key="group.group_revenue_net",
        ),
        "group_ebitda": _year_series(
            "Group EBITDA",
            group.group_ebitda,
            lineage_key="group.group_ebitda",
        ),
        "group_fcf": _year_series(
            "Group FCF",
            group.group_fcf,
            lineage_key="group.group_fcf",
        ),
        "group_gross_profit": _year_series(
            "Group Gross Profit",
            group.group_gross_profit,
            lineage_key="group.group_gross_profit",
        ),
        "total_opex": _year_series("Total OpEx", group.total_opex, lineage_key="group.total_opex"),
        "total_group_capex": _year_series(
            "Total Group CapEx",
            group.total_group_capex,
            lineage_key="group.total_group_capex",
        ),
    }

    module_tables: dict[str, Any] = {}
    module_ev: dict[str, Any] = {}
    for key in _MODULE_KEYS:
        mod = mods[key]
        ev_mm = float(mod.total_revenue.at(FIRST_YEAR)) * 10.0
        module_ev[key] = {
            "display_name": _MODULE_DISPLAY[key],
            "ev_2025_b": ev_mm / 1000.0,
            "lineage_key": f"module.{key}.total_revenue",
        }
        module_tables[key] = {
            "display_name": _MODULE_DISPLAY[key],
            "total_revenue": _year_series(
                "Total Revenue",
                mod.total_revenue,
                lineage_key=f"module.{key}.total_revenue",
            ),
            "module_fcf": _year_series(
                "Module FCF",
                mod.module_fcf,
                lineage_key=f"module.{key}.module_fcf",
            ),
            "module_ebitda": _year_series(
                "Module EBITDA",
                mod.module_ebitda,
                lineage_key=f"module.{key}.module_ebitda",
            ),
            "blended_irr": _year_series(
                "Blended IRR",
                mod.blended_irr,
                lineage_key=f"module.{key}.blended_irr",
                unit="ratio",
            ),
        }

    return {
        "run_id": result.run_id,
        "scenario": result.audit.get("scenario", "base_case"),
        "cached": cached,
        "audit": result.audit,
        "solver": {
            "iterations": result.solver_trace.iterations,
            "converged": result.solver_trace.converged,
            "max_residual": result.solver_trace.max_residual,
        },
        "valuation": {
            "group_ev_2025_b": val.implied_ev_2025_billions,
            "group_wacc": val.group_wacc,
            "terminal_growth": val.terminal_growth,
            "lineage_key": "valuation.implied_ev_2025",
            "implied_ev_by_year": _year_series(
                "Implied EV (10× rev)",
                val.implied_ev_by_year,
                lineage_key="valuation.implied_ev_2025",
                unit="$mm",
            ),
        },
        "group": group_rows,
        "modules": module_tables,
        "module_ev": module_ev,
        "conservation": {
            "all_ok": result.conservation.all_ok,
            "r108_by_year": {
                str(y): result.conservation.r108_ok_by_year.get(y, "CHECK") == "OK"
                for y in _YEARS
            },
        },
    }


def serialize_tornado(bars: list[TornadoBar]) -> list[dict[str, Any]]:
    def _num(v: float) -> float | None:
        return v if math.isfinite(v) else None

    return [
        {
            "label": b.label,
            "low_ev": _num(b.low_ev),
            "high_ev": _num(b.high_ev),
            "base_ev": _num(b.base_ev),
            "delta": _num(b.delta),
        }
        for b in bars
    ]


def serialize_mc_aggregation(agg: McAggregation) -> dict[str, Any]:
    return agg.to_dict()


def serialize_assumption_catalog(assumptions: Any) -> list[dict[str, Any]]:
    """List assumption inputs with MC ranges for scenario picker."""
    rows: list[dict[str, Any]] = []
    for label, inp in sorted(assumptions.by_label.items()):
        mc = assumptions.mc_ranges.by_label.get(label)
        rows.append(
            {
                "label": label,
                "base_case": inp.base_case,
                "section": inp.section if hasattr(inp, "section") else "",
                "mc_min": mc.mc_min if mc else None,
                "mc_max": mc.mc_max if mc else None,
                "distribution": mc.distribution.value if mc and mc.distribution else "fixed",
            }
        )
    return rows


def serialize_lineage_index() -> list[dict[str, Any]]:
    return [e.to_dict() for e in get_lineage_registry().values()]
