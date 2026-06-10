"""In-memory store of recent ModelResult instances keyed by run_id — audit grid API."""

from __future__ import annotations

import threading
import time
from collections import OrderedDict

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import ModelResult


class RunStore:
    """Thread-safe LRU of pipeline results for sheet grid / extended lineage."""

    def __init__(self, max_entries: int | None = None, ttl_sec: int | None = None) -> None:
        settings = get_settings()
        self._max = max_entries if max_entries is not None else settings.run_store_max_entries
        self._ttl_sec = ttl_sec if ttl_sec is not None else settings.run_store_ttl_sec
        self._data: OrderedDict[str, ModelResult] = OrderedDict()
        self._timestamps: OrderedDict[str, float] = OrderedDict()
        self._lock = threading.Lock()

    def put(self, run_id: str, result: ModelResult) -> None:
        now = time.time()
        with self._lock:
            self._evict_expired_locked(now)
            self._data[run_id] = result
            self._timestamps[run_id] = now
            self._data.move_to_end(run_id)
            self._timestamps.move_to_end(run_id)
            while len(self._data) > self._max:
                oldest = next(iter(self._data))
                self._data.pop(oldest)
                self._timestamps.pop(oldest, None)

    def get(self, run_id: str) -> ModelResult | None:
        with self._lock:
            self._evict_expired_locked(time.time())
            result = self._data.get(run_id)
            if result is not None:
                self._data.move_to_end(run_id)
                self._timestamps.move_to_end(run_id)
            return result

    def _evict_expired_locked(self, now: float) -> None:
        for run_id in list(self._timestamps.keys()):
            if now - self._timestamps[run_id] > self._ttl_sec:
                self._data.pop(run_id, None)
                self._timestamps.pop(run_id, None)


_store: RunStore | None = None


def get_run_store() -> RunStore:
    global _store
    if _store is None:
        _store = RunStore()
    return _store
