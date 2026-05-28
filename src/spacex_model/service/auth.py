"""Optional API key auth — Phase G stub (disabled when no key configured)."""

from __future__ import annotations

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from spacex_model.config.settings import get_settings

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def require_api_key(api_key: str | None = Security(_api_key_header)) -> None:
    """Enforce API key when SPACEX_MODEL_API_KEY is set."""
    settings = get_settings()
    if not settings.api_key:
        return
    if api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
