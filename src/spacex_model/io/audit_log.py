"""Run audit log helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_audit_log(audit: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(audit, indent=2), encoding="utf-8")
