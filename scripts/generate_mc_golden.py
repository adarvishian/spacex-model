#!/usr/bin/env python3
"""Generate MC golden baseline for equivalence harness (PRD §3.1).

Usage (from repo root):
    python scripts/generate_mc_golden.py
    python scripts/generate_mc_golden.py --trials 2000 --seed 42
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GOLDEN_DIR = REPO_ROOT / "tests" / "golden"
DEFAULT_TRIALS = 2000
DEFAULT_SEED = 42


def _git_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def _workbook_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate MC golden baseline")
    parser.add_argument("--trials", type=int, default=DEFAULT_TRIALS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    sys.path.insert(0, str(REPO_ROOT / "src"))

    from spacex_model.config.settings import get_settings
    from spacex_model.engine.pipeline import run_base_case
    from spacex_model.mc.aggregator import aggregate_trials
    from spacex_model.mc.results import extract_trial_metrics, read_trials_parquet
    from spacex_model.mc.runner import McRunConfig, run_mc

    settings = get_settings()
    if not settings.workbook_path.exists():
        print(f"Workbook not found: {settings.workbook_path}", file=sys.stderr)
        return 1

    print(f"Generating golden MC baseline ({args.trials} trials, seed {args.seed})…")
    mc = run_mc(
        workbook_path=settings.workbook_path,
        config=McRunConfig(
            trials=args.trials,
            base_seed=args.seed,
            n_jobs=-1,
            checkpoint_interval=max(100, args.trials // 10),
            scenario_name="base_case",
            sampling="mc",
            warm_start=True,
            mc_lite=True,
            adaptive=False,
            conservation_audit_every=0,
        ),
        run_id="golden",
    )

    table = read_trials_parquet(mc.trials_parquet)
    base = run_base_case(workbook_path=settings.workbook_path, write_outputs=False)
    base_metrics = extract_trial_metrics(base)
    agg = aggregate_trials(table, base_metrics=base_metrics, base_seed=args.seed)

    GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    stem = f"mc_baseline_seed{args.seed}_{args.trials}"
    parquet_path = GOLDEN_DIR / f"{stem}.parquet"
    agg_path = GOLDEN_DIR / f"{stem}_agg.json"

    shutil.copy(mc.trials_parquet, parquet_path)

    meta = {
        "git_sha": _git_sha(),
        "workbook_sha": _workbook_sha(settings.workbook_path),
        "trials": args.trials,
        "base_seed": args.seed,
        "trials_converged": mc.trials_converged,
        "non_convergence_rate": mc.audit["non_convergence_rate"],
        "wall_clock_sec": mc.wall_clock_sec,
        "aggregation": agg.to_dict(),
    }
    agg_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Wrote {parquet_path}")
    print(f"Wrote {agg_path}")
    print(f"Converged: {mc.trials_converged}/{args.trials}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
