"""Milestone 2.1 — process-local workbook ingest memo."""

from __future__ import annotations

from pathlib import Path

import pytest

from spacex_model.config.settings import get_settings
from spacex_model.io.excel_ingest import clear_ingest_cache, ingest_workbook


@pytest.fixture(autouse=True)
def _clear_cache() -> None:
    clear_ingest_cache()
    yield
    clear_ingest_cache()


def test_ingest_workbook_returns_same_object_for_same_path() -> None:
    path = get_settings().workbook_path
    if not path.exists():
        pytest.skip(f"Workbook not present: {path}")
    first = ingest_workbook(path)
    second = ingest_workbook(path)
    assert first is second


def test_ingest_cache_invalidates_on_mtime_change(tmp_path: Path, monkeypatch) -> None:
    path = get_settings().workbook_path
    if not path.exists():
        pytest.skip(f"Workbook not present: {path}")
    copy = tmp_path / "workbook.xlsx"
    copy.write_bytes(path.read_bytes())
    first = ingest_workbook(copy)
    copy.write_bytes(path.read_bytes())
    second = ingest_workbook(copy)
    assert first is not second
