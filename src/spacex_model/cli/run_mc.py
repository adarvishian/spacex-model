"""CLI: Monte Carlo runner — Phase F."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_base_case
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.inputs.demand_curves import demand_curves_from_ingest
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.mc.aggregator import aggregate_trials
from spacex_model.mc.results import extract_trial_metrics, read_trials_parquet
from spacex_model.mc.runner import McRunConfig, run_mc
from spacex_model.mc.sampler import list_variable_labels, sample_trial
from spacex_model.mc.sensitivity import (
    DEFAULT_2D_COL,
    DEFAULT_2D_ROW,
    prcc_sensitivity,
    sweep_2d_table,
    tornado_sensitivity,
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Mach33 SpaceX Monte Carlo study")
    parser.add_argument("--workbook", type=Path, default=None, help="Path to V2.16 xlsx")
    parser.add_argument("--trials", type=int, default=10_000, help="Number of MC trials")
    parser.add_argument("--seed", type=int, default=42, help="Base random seed")
    parser.add_argument("--jobs", type=int, default=-1, help="joblib parallel workers (-1 = all cores)")
    parser.add_argument(
        "--checkpoint-interval",
        type=int,
        default=1000,
        help="Write checkpoint parquet every N trials",
    )
    parser.add_argument("--run-id", type=str, default=None, help="Optional run identifier")
    parser.add_argument(
        "--sensitivity",
        action="store_true",
        help="After MC, compute tornado / PRCC / 2D table (adds runtime)",
    )
    parser.add_argument(
        "--tornado-top",
        type=int,
        default=10,
        help="Number of tornado bars (with --sensitivity)",
    )
    args = parser.parse_args(argv)

    settings = get_settings()
    workbook = args.workbook or settings.workbook_path
    print(f"MC study: {args.trials} trials, seed={args.seed}, workbook={workbook}")

    mc_result = run_mc(
        workbook_path=workbook,
        config=McRunConfig(
            trials=args.trials,
            base_seed=args.seed,
            n_jobs=args.jobs,
            checkpoint_interval=args.checkpoint_interval,
        ),
        run_id=args.run_id,
    )

    table = read_trials_parquet(mc_result.trials_parquet)
    base = run_base_case(workbook_path=workbook, write_outputs=False)
    base_metrics = extract_trial_metrics(base)
    agg = aggregate_trials(table, base_metrics=base_metrics)

    out_dir = mc_result.output_dir
    (out_dir / "aggregation.json").write_text(json.dumps(agg.to_dict(), indent=2), encoding="utf-8")

    print(f"Run ID: {mc_result.run_id}")
    print(f"Trials: {mc_result.trials_completed} ({mc_result.trials_converged} converged)")
    print(f"Wall clock: {mc_result.wall_clock_sec:.1f}s")
    print(f"Outputs: {out_dir}")

    ev = agg.metrics.get("group_ev_2025_b")
    if ev:
        print(
            f"Group EV 2025 ($B): P5={ev.p5:,.1f} P50={ev.p50:,.1f} P95={ev.p95:,.1f} "
            f"(base={ev.base_case:,.1f})"
        )

    if args.sensitivity:
        ingest = ingest_workbook(workbook)
        assumptions = assumptions_from_ingest(ingest)
        demand = demand_curves_from_ingest(ingest)
        print("Computing sensitivity (tornado + PRCC + 2D)...")
        tornado = tornado_sensitivity(
            assumptions,
            ingest=ingest,
            demand=demand,
            top_n=args.tornado_top,
        )
        (out_dir / "tornado.json").write_text(
            json.dumps([b.__dict__ for b in tornado], indent=2),
            encoding="utf-8",
        )

        import numpy as np

        mask = None
        if "converged" in table.column_names:
            mask = np.array([bool(x) for x in table.column("converged").to_pylist()])
        trial_idx_col = table.column("trial_idx").to_pylist()
        indices = [
            int(trial_idx_col[i])
            for i in range(table.num_rows)
            if mask is None or mask[i]
        ][:200]
        trials = [
            sample_trial(assumptions, trial_idx=idx, base_seed=args.seed) for idx in indices
        ]
        ev_col = np.asarray(table.column("group_ev_2025_b").to_numpy(), dtype=np.float64)
        y = ev_col[mask] if mask is not None else ev_col
        prcc = prcc_sensitivity(trials, y, labels=list_variable_labels(assumptions)[:30])
        (out_dir / "prcc.json").write_text(
            json.dumps([e.__dict__ for e in prcc[:20]], indent=2),
            encoding="utf-8",
        )

        grid_2d = sweep_2d_table(
            assumptions,
            ingest=ingest,
            demand=demand,
            row_label=DEFAULT_2D_ROW,
            col_label=DEFAULT_2D_COL,
        )
        (out_dir / "sensitivity_2d.json").write_text(json.dumps(grid_2d, indent=2), encoding="utf-8")
        print(f"Sensitivity artifacts written under {out_dir}")

    non_conv = mc_result.trials_completed - mc_result.trials_converged
    if non_conv > mc_result.trials_completed * 0.01:
        print(f"WARN: non-convergence rate {non_conv / mc_result.trials_completed:.2%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
