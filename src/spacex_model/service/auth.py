"""Optional API key auth — fail-closed for mutating routes on serverless."""

from __future__ import annotations

import hmac

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from spacex_model.config.settings import get_settings, is_serverless

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def _validate_api_key(api_key: str | None) -> None:
    settings = get_settings()
    if not settings.api_key:
        return
    if not api_key or not hmac.compare_digest(api_key, settings.api_key):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


def require_read_auth(api_key: str | None = Security(_api_key_header)) -> None:
    """Enforce API key on reads when SPACEX_MODEL_API_KEY is configured."""
    _validate_api_key(api_key)


def require_write_auth(api_key: str | None = Security(_api_key_header)) -> None:
    """Enforce API key on writes; fail-closed on serverless when unset (M1.4)."""
    settings = get_settings()
    if settings.api_key:
        _validate_api_key(api_key)
        return
    if is_serverless():
        raise HTTPException(status_code=401, detail="API key required")


# Backward-compatible alias for imports that predate read/write split.
require_api_key = require_read_auth
