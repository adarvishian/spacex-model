"""Shared skip logic for prebuild precache scripts (Option F — decouple from Vercel)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def git_sha(repo_root: Path) -> str:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=repo_root,
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def _env_bool(name: str) -> bool:
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


def should_skip_precache(out_path: Path, *, repo_root: Path, label: str) -> bool:
    """Return True when an existing committed artifact can be reused."""
    if _env_bool("SPACEX_MODEL_FORCE_PRECOMPUTE"):
        return False

    if not out_path.exists():
        if _env_bool("SPACEX_MODEL_SKIP_PRECOMPUTE"):
            print(f"ERROR: {label}: SPACEX_MODEL_SKIP_PRECOMPUTE=1 but {out_path} missing", file=sys.stderr)
            sys.exit(1)
        return False

    if _env_bool("SPACEX_MODEL_SKIP_PRECOMPUTE"):
        print(f"Skipping {label} (SPACEX_MODEL_SKIP_PRECOMPUTE=1, reusing {out_path.name})")
        return True

    try:
        data = json.loads(out_path.read_text(encoding="utf-8"))
        if data.get("git_sha") == git_sha(repo_root):
            print(f"Skipping {label} (artifact git_sha matches HEAD)")
            return True
    except (json.JSONDecodeError, OSError):
        pass

    return False
