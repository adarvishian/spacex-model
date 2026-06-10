#!/usr/bin/env python3
"""Fail CI when committed precache artifacts are stale or malformed."""

from __future__ import annotations

import json
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(REPO_ROOT / "scripts"))
from precache_config import (  # noqa: E402
    DEFAULT_MC_TRIALS,
    PRECACHE_SCENARIOS,
    mc_artifact_path,
    run_artifact_path,
)

RUN_REQUIRED_KEYS = ("git_sha", "scenario", "run_id", "audit_grids", "run_audit", "deterministic")
MC_REQUIRED_KEYS = (
    "git_sha",
    "scenario",
    "trials",
    "base_seed",
    "trials_completed",
    "trials_converged",
    "convergence_status",
    "aggregation",
)
MC_AGG_REQUIRED_KEYS = ("n_trials", "metrics", "group_ev_histogram", "group_fcf_fan")


def _git_sha() -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        print(f"ERROR: cannot resolve git HEAD: {exc}", file=sys.stderr)
        sys.exit(1)


def _precache_data_commit_sha() -> str:
    """Short sha of the commit that last updated precache JSON (not necessarily HEAD)."""
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%h", "--", "frontend/public/data"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except subprocess.CalledProcessError:
        return _git_sha()


def _acceptable_artifact_shas() -> set[str]:
    """SHAs that may appear in artifact git_sha (handles stamp-on-amend workflow)."""
    shas = {_git_sha(), _precache_data_commit_sha()}
    precache_commit = _precache_data_commit_sha()
    try:
        parent = subprocess.check_output(
            ["git", "rev-parse", "--short", f"{precache_commit}^"],
            cwd=REPO_ROOT,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
        shas.add(parent)
    except subprocess.CalledProcessError:
        pass
    return shas


def _validate_run_artifact(data: object, scenario: str) -> list[str]:
    if not isinstance(data, dict):
        return ["root must be a JSON object"]
    errors: list[str] = []
    for key in RUN_REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing key: {key}")
    if data.get("scenario") != scenario:
        errors.append(f"scenario must be {scenario!r}")
    det = data.get("deterministic")
    if isinstance(det, dict):
        for key in ("run_id", "scenario", "solver"):
            if key not in det:
                errors.append(f"deterministic missing key: {key}")
    elif "deterministic" in data:
        errors.append("deterministic must be an object")
    grids = data.get("audit_grids")
    if isinstance(grids, dict) and not grids:
        errors.append("audit_grids must not be empty")
    return errors


def _validate_mc_artifact(data: object, scenario: str) -> list[str]:
    if not isinstance(data, dict):
        return ["root must be a JSON object"]
    errors: list[str] = []
    for key in MC_REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing key: {key}")
    if data.get("scenario") != scenario:
        errors.append(f"scenario must be {scenario!r}")
    trials = data.get("trials")
    if isinstance(trials, int):
        if trials < 1:
            errors.append("trials must be >= 1")
        if trials != DEFAULT_MC_TRIALS:
            errors.append(f"trials must be {DEFAULT_MC_TRIALS} (got {trials})")
    agg = data.get("aggregation")
    if isinstance(agg, dict):
        for key in MC_AGG_REQUIRED_KEYS:
            if key not in agg:
                errors.append(f"aggregation missing key: {key}")
        if isinstance(trials, int) and agg.get("n_trials") != trials:
            errors.append("aggregation.n_trials must match trials")
    elif "aggregation" in data:
        errors.append("aggregation must be an object")
    return errors


def _artifact_specs() -> list[tuple[Path, Callable[[object], list[str]]]]:
    specs: list[tuple[Path, Callable[[object], list[str]]]] = []
    for scenario in PRECACHE_SCENARIOS:
        specs.append(
            (
                run_artifact_path(REPO_ROOT, scenario),
                lambda data, s=scenario: _validate_run_artifact(data, s),
            )
        )
        specs.append(
            (
                mc_artifact_path(REPO_ROOT, scenario),
                lambda data, s=scenario: _validate_mc_artifact(data, s),
            )
        )
    return specs


def main() -> int:
    head = _git_sha()
    expected_sha = _precache_data_commit_sha()
    acceptable_shas = _acceptable_artifact_shas()
    failed = False

    for path, validator in _artifact_specs():
        rel = path.relative_to(REPO_ROOT)
        if not path.exists():
            print(f"ERROR: {rel}: file missing", file=sys.stderr)
            failed = True
            continue

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"ERROR: {rel}: cannot read JSON ({exc})", file=sys.stderr)
            failed = True
            continue

        artifact_sha = data.get("git_sha") if isinstance(data, dict) else None
        if artifact_sha not in acceptable_shas:
            print(
                f"ERROR: {rel}: git_sha={artifact_sha!r} not in "
                f"{sorted(acceptable_shas)!r} (precache commit {expected_sha!r}, HEAD {head!r})",
                file=sys.stderr,
            )
            failed = True

        for err in validator(data):
            print(f"ERROR: {rel}: {err}", file=sys.stderr)
            failed = True

    if failed:
        print(
            "Precache artifacts are stale or invalid. Run ./scripts/regenerate_precache.sh",
            file=sys.stderr,
        )
        return 1

    print(
        f"Precache artifacts OK ({len(PRECACHE_SCENARIOS)} scenarios, "
        f"git_sha={expected_sha}, HEAD={head})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
