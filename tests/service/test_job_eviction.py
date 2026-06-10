"""In-memory job store TTL and capacity bounds."""

from __future__ import annotations

import time
from unittest.mock import patch

from spacex_model.service.jobs import JobManager, JobStatus, McJob


def _terminal_job(job_id: str, *, age_sec: float = 0.0) -> McJob:
    return McJob(
        job_id=job_id,
        status=JobStatus.COMPLETED,
        created_at=time.time() - age_sec,
    )


def test_job_store_evicts_by_ttl() -> None:
    mgr = JobManager()
    with patch("spacex_model.service.jobs.get_settings") as mock_settings:
        mock_settings.return_value.job_store_ttl_sec = 60
        mock_settings.return_value.job_store_max_entries = 100
        mgr._jobs["old"] = _terminal_job("old", age_sec=120)
        mgr._jobs["fresh"] = _terminal_job("fresh", age_sec=5)
        mgr._evict_stale()
        assert "old" not in mgr._jobs
        assert "fresh" in mgr._jobs


def test_job_store_caps_terminal_jobs() -> None:
    mgr = JobManager()
    with patch("spacex_model.service.jobs.get_settings") as mock_settings:
        mock_settings.return_value.job_store_ttl_sec = 3600
        mock_settings.return_value.job_store_max_entries = 2
        mgr._jobs["a"] = _terminal_job("a")
        mgr._jobs["b"] = _terminal_job("b")
        mgr._jobs["c"] = McJob(job_id="c", status=JobStatus.RUNNING)
        mgr._evict_stale()
        assert len(mgr._jobs) == 2
        assert "c" in mgr._jobs
