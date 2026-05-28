"""Runtime settings and workbook path resolution."""

from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).resolve().parents[3]
_DEFAULT_WORKBOOK = (
    _REPO_ROOT
    / "Pre Existing Model Package"
    / "01_Current_State"
    / "SpaceX Model V2.16.xlsx"
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SPACEX_MODEL_", env_file=".env", extra="ignore")

    workbook_path: Path = _DEFAULT_WORKBOOK
    outputs_dir: Path = _REPO_ROOT / "outputs"
    scenarios_dir: Path = _REPO_ROOT / "scenarios"
    redis_url: str | None = None
    cache_max_entries: int = 128
    cache_ttl_sec: int = 3600
    api_key: str | None = None


def get_settings() -> Settings:
    return Settings()
