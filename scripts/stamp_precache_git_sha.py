#!/usr/bin/env python3
"""Rewrite git_sha in committed precache JSON to match HEAD (after amend/rebase)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "frontend" / "public" / "data"


def main() -> int:
    try:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: cannot resolve git HEAD: {exc}", file=sys.stderr)
        return 1

    updated = 0
    for path in sorted(DATA_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            continue
        if data.get("git_sha") == sha:
            continue
        data["git_sha"] = sha
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print(f"stamped {path.name} -> {sha}")
        updated += 1

    if updated:
        print(f"Updated {updated} artifact(s) to git_sha={sha}")
    else:
        print(f"All artifacts already at git_sha={sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
