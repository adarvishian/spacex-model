"""Shared precache scenario list and artifact paths (Milestone 3)."""

from __future__ import annotations

from pathlib import Path

PRECACHE_SCENARIOS: tuple[str, ...] = ("base_case", "bear", "bull", "mars_share")
DEFAULT_MC_TRIALS = 5000
DEFAULT_MC_SEED = 42


def precache_data_dir(repo_root: Path) -> Path:
    return repo_root / "frontend" / "public" / "data"


def run_artifact_path(repo_root: Path, scenario: str) -> Path:
    return precache_data_dir(repo_root) / f"{scenario}_run.json"


def mc_artifact_path(repo_root: Path, scenario: str) -> Path:
    return precache_data_dir(repo_root) / f"{scenario}_mc.json"
