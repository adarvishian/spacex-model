"""Runtime settings and workbook path resolution."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _find_repo_root() -> Path:
    """Resolve project root in dev, editable installs, and Vercel serverless."""
    if override := os.environ.get("SPACEX_MODEL_REPO_ROOT"):
        return Path(override).resolve()
    here = Path(__file__).resolve()
    for candidate in (here, *here.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "scenarios").is_dir():
            return candidate
    for candidate in (Path("/var/task"), Path.cwd()):
        if (candidate / "scenarios").is_dir():
            return candidate.resolve()
    return here.parents[3]


_REPO_ROOT = _find_repo_root()
_DEFAULT_WORKBOOK = _REPO_ROOT / "SpaceX V4.131.xlsx"
_LEGACY_V216_WORKBOOK = (
    _REPO_ROOT
    / "Pre Existing Model Package"
    / "01_Current_State"
    / "SpaceX Model V2.16.xlsx"
)


def is_serverless() -> bool:
    """True on Vercel Functions / AWS Lambda."""
    return bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))


def _default_outputs_dir() -> Path:
    """Use /tmp on serverless — /var/task is read-only."""
    if is_serverless():
        return Path("/tmp/spacex_model/outputs")
    return _REPO_ROOT / "outputs"


def _default_cell_history_read_dir() -> Path:
    """Committed cell-history artifact (bundled on serverless)."""
    return _REPO_ROOT / "data" / "cell_history"


def _default_cell_history_dir() -> Path:
    """Writable store — /tmp on serverless; local dev uses committed path."""
    if is_serverless():
        return Path("/tmp/spacex_model/cell_history")
    return _default_cell_history_read_dir()


def get_repo_root() -> Path:
    return _REPO_ROOT


def get_legacy_v216_workbook() -> Path:
    """V2.16 workbook path (diagnostic / pre-R0 tests only)."""
    return _LEGACY_V216_WORKBOOK


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SPACEX_MODEL_", env_file=".env", extra="ignore")

    workbook_path: Path = _DEFAULT_WORKBOOK
    outputs_dir: Path = _default_outputs_dir()
    scenarios_dir: Path = _REPO_ROOT / "scenarios"
    redis_url: str | None = None
    cache_max_entries: int = 128
    cache_ttl_sec: int = 3600
    job_store_max_entries: int = 32
    job_store_ttl_sec: int = 3600
    run_store_max_entries: int = 16
    run_store_ttl_sec: int = 3600
    api_key: str | None = None
    allowed_origins: str = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173"
    # Serverless (Vercel): MC runs in small batches per poll to avoid FUNCTION_INVOCATION_TIMEOUT
    mc_serverless_batch_trials: int = 3
    mc_serverless_max_trials: int = 200
    # Milestone 3.3 — custom MC deferred on serverless; precache-only until Sandbox executor
    enable_custom_mc: bool = False


def get_settings() -> Settings:
    return Settings()


def is_custom_mc_enabled() -> bool:
    """Local dev keeps live MC; serverless defaults to precache-only."""
    if not is_serverless():
        return True
    return get_settings().enable_custom_mc


def parsed_allowed_origins() -> list[str]:
    """CORS allowlist from SPACEX_MODEL_ALLOWED_ORIGINS (comma-separated)."""
    raw = get_settings().allowed_origins.strip()
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]
