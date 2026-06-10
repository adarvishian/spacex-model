#!/usr/bin/env python3
"""Precompute base-case audit grids + Run Audit payload for instant Audit Mode load.

Writes frontend/public/data/base_case_run.json tagged with git short SHA so the
frontend can hydrate synchronously on /audit open without waiting for the solver.

Usage (from repo root):
    uv run python scripts/precompute_base_case.py
    SPACEX_MODEL_SKIP_PRECOMPUTE=1 python3 scripts/precompute_base_case.py  # skip without deps
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / "frontend" / "public" / "data" / "base_case_run.json"

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from precache_skip import should_skip_precache  # noqa: E402


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
    if should_skip_precache(OUT_PATH, repo_root=REPO_ROOT, label="base-case precompute"):
        return 0

    sys.path.insert(0, str(REPO_ROOT / "src"))

    from spacex_model.config.settings import get_settings
    from spacex_model.engine.pipeline import run_pipeline
    from spacex_model.service.grid import build_grid_payload
    from spacex_model.service.run_audit_payload import build_run_audit_payload
    from spacex_model.service.serializers import serialize_model_result
    from spacex_model.service.sheets_meta import SHEETS

    settings = get_settings()
    if not settings.workbook_path.exists():
        print(f"Workbook not found: {settings.workbook_path}", file=sys.stderr)
        return 1

    scenario = "base_case"
    scenario_path = settings.scenarios_dir / f"{scenario}.yaml"
    if not scenario_path.exists():
        print(f"Scenario not found: {scenario_path}", file=sys.stderr)
        return 1

    print(f"Running base-case pipeline ({scenario_path.name})…")
    result = run_pipeline(scenario_path=scenario_path, write_outputs=False)

    audit_grids: dict[str, object] = {}
    for meta in SHEETS:
        if not meta.enabled or meta.slug == "run_audit":
            continue
        print(f"  grid: {meta.slug}")
        audit_grids[meta.slug] = build_grid_payload(meta, result)

    run_audit = build_run_audit_payload(result)
    deterministic = serialize_model_result(result, cached=False)

    artifact = {
        "git_sha": _git_sha(),
        "scenario": scenario,
        "run_id": result.run_id,
        "audit_grids": audit_grids,
        "run_audit": run_audit,
        "deterministic": {
            "run_id": deterministic["run_id"],
            "scenario": deterministic["scenario"],
            "cached": False,
            "solver": deterministic["solver"],
            "conservation": deterministic.get("conservation"),
        },
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(artifact, indent=2), encoding="utf-8")
    size_mb = OUT_PATH.stat().st_size / (1024 * 1024)
    print(f"Wrote {OUT_PATH} ({size_mb:.1f} MB, git_sha={artifact['git_sha']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
