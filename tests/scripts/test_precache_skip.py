"""Milestone 1.2 — prebuild skip runs before spacex_model imports."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def test_precompute_base_case_skip_without_spacex_model_deps() -> None:
    env = os.environ.copy()
    env["SPACEX_MODEL_SKIP_PRECOMPUTE"] = "1"
    env.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "precompute_base_case.py")],
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_precompute_base_case_mc_skip_without_spacex_model_deps() -> None:
    env = os.environ.copy()
    env["SPACEX_MODEL_SKIP_PRECOMPUTE"] = "1"
    env.pop("PYTHONPATH", None)
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "precompute_base_case_mc.py")],
        cwd=REPO,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr or result.stdout
