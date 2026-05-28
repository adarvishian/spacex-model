"""Vercel ASGI entrypoint — bootstrap src layout before importing the FastAPI app."""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from spacex_model.service.api import app  # noqa: E402

__all__ = ["app"]
