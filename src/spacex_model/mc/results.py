"""MC trial output schema and parquet I/O."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

from spacex_model.config.constants import FIRST_YEAR, LAST_YEAR

# Core outputs for aggregation per PRD §8.4
TRIAL_METRIC_KEYS = (
    "group_ev_2025_b",
    "group_revenue_2050_mm",
    "group_fcf_2030_mm",
    "group_fcf_2040_mm",
    "group_fcf_2050_mm",
    "customer_launch_ev_2025_b",
    "starlink_ev_2025_b",
    "odc_ev_2025_b",
    "ai_stack_ev_2025_b",
    "lunar_mars_ev_2025_b",
    "customer_launch_revenue_2050_mm",
    "starlink_revenue_2050_mm",
    "odc_revenue_2050_mm",
    "ai_stack_revenue_2050_mm",
    "lunar_mars_revenue_2050_mm",
    "converged",
    "solver_iterations",
)


def extract_trial_metrics(result: Any, *, revenue_multiple: float = 10.0) -> dict[str, float | bool | int]:
    """Extract scalar MC outputs from a ModelResult."""
    y2030 = 2030
    y2040 = 2040
    y2050 = LAST_YEAR
    group = result.group_pnl
    valuation = result.valuation
    mods = result.module_outputs

    def _mod_ev(key: str) -> float:
        rev = mods[key].total_revenue.at(FIRST_YEAR)
        return rev * revenue_multiple / 1000.0

    return {
        "group_ev_2025_b": float(valuation.implied_ev_2025_billions),
        "group_revenue_2050_mm": float(group.group_revenue_net.at(y2050)),
        "group_fcf_2030_mm": float(group.group_fcf.at(y2030)),
        "group_fcf_2040_mm": float(group.group_fcf.at(y2040)),
        "group_fcf_2050_mm": float(group.group_fcf.at(y2050)),
        "customer_launch_ev_2025_b": _mod_ev("customer_launch"),
        "starlink_ev_2025_b": _mod_ev("starlink"),
        "odc_ev_2025_b": _mod_ev("odc"),
        "ai_stack_ev_2025_b": _mod_ev("ai_stack"),
        "lunar_mars_ev_2025_b": _mod_ev("lunar_mars"),
        "customer_launch_revenue_2050_mm": float(mods["customer_launch"].total_revenue.at(y2050)),
        "starlink_revenue_2050_mm": float(mods["starlink"].total_revenue.at(y2050)),
        "odc_revenue_2050_mm": float(mods["odc"].total_revenue.at(y2050)),
        "ai_stack_revenue_2050_mm": float(mods["ai_stack"].total_revenue.at(y2050)),
        "lunar_mars_revenue_2050_mm": float(mods["lunar_mars"].total_revenue.at(y2050)),
        "converged": bool(result.solver_trace.converged),
        "solver_iterations": int(result.solver_trace.iterations),
    }


def trials_to_table(rows: list[dict[str, Any]]) -> pa.Table:
    """Build Arrow table from trial result dicts."""
    if not rows:
        return pa.table({k: [] for k in ("trial_idx", *TRIAL_METRIC_KEYS)})
    columns: dict[str, list[Any]] = {key: [] for key in rows[0]}
    for row in rows:
        for key in columns:
            columns[key].append(row.get(key))
    return pa.table(columns)


def write_trials_parquet(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(trials_to_table(rows), path)


def read_trials_parquet(path: Path) -> pa.Table:
    return pq.read_table(path)
