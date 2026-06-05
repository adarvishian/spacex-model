#!/usr/bin/env python3
"""Precompute base-case Monte Carlo for instant Client/Audit MC views.

Writes frontend/public/data/base_case_mc.json tagged with git short SHA.
Default: 2,000 trials, seed 42 (PRD §9.1). Override trials via
SPACEX_MODEL_MC_PRECOMPUTE_TRIALS for CI or local smoke runs.

Usage (from repo root):
    python scripts/precompute_base_case_mc.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / "frontend" / "public" / "data" / "base_case_mc.json"
DEFAULT_TRIALS = 2000
DEFAULT_SEED = 42


def _git_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def main() -> int:
    sys.path.insert(0, str(REPO_ROOT / "src"))

    from spacex_model.config.settings import get_settings
    from spacex_model.engine.pipeline import run_base_case
    from spacex_model.mc.aggregator import aggregate_trials
    from spacex_model.mc.results import extract_trial_metrics, read_trials_parquet
    from spacex_model.mc.runner import McRunConfig, run_mc
    from spacex_model.service.serializers import serialize_mc_aggregation

    settings = get_settings()
    if not settings.workbook_path.exists():
        print(f"Workbook not found: {settings.workbook_path}", file=sys.stderr)
        return 1

    trials = int(os.environ.get("SPACEX_MODEL_MC_PRECOMPUTE_TRIALS", str(DEFAULT_TRIALS)))
    base_seed = int(os.environ.get("SPACEX_MODEL_MC_PRECOMPUTE_SEED", str(DEFAULT_SEED)))
    scenario = "base_case"

    print(f"Running base-case MC ({trials} trials, seed {base_seed})…")
    mc = run_mc(
        workbook_path=settings.workbook_path,
        config=McRunConfig(
            trials=trials,
            base_seed=base_seed,
            n_jobs=-1,
            checkpoint_interval=max(100, trials // 10),
            scenario_name=scenario,
        ),
        run_id="precache",
    )

    table = read_trials_parquet(mc.trials_parquet)
    base = run_base_case(workbook_path=settings.workbook_path, write_outputs=False)
    base_metrics = extract_trial_metrics(base)
    agg = aggregate_trials(table, base_metrics=base_metrics, base_seed=base_seed)

    artifact = {
        "git_sha": _git_sha(),
        "scenario": scenario,
        "job_id": "precache",
        "run_id": mc.run_id,
        "trials": trials,
        "base_seed": base_seed,
        "trials_completed": mc.trials_completed,
        "trials_converged": mc.trials_converged,
        "n_trials": agg.n_trials,
        "n_converged": agg.n_converged,
        "convergence_status": agg.convergence_status,
        "wall_clock_sec": round(mc.wall_clock_sec, 3),
        "aggregation": serialize_mc_aggregation(agg),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    size_mb = OUT_PATH.stat().st_size / (1024 * 1024)
    print(
        f"Wrote {OUT_PATH} ({size_mb:.2f} MB, "
        f"git_sha={artifact['git_sha']}, converged={mc.trials_converged}/{trials})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
