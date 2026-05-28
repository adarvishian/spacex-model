"""In-memory store of recent ModelResult instances keyed by run_id — audit grid API."""

from __future__ import annotations

import threading
from collections import OrderedDict

from spacex_model.engine.pipeline import ModelResult

_MAX_RUNS = 16


class RunStore:
    """Thread-safe LRU of pipeline results for sheet grid / extended lineage."""

    def __init__(self, max_entries: int = _MAX_RUNS) -> None:
        self._max = max_entries
        self._data: OrderedDict[str, ModelResult] = OrderedDict()
        self._lock = threading.Lock()

    def put(self, run_id: str, result: ModelResult) -> None:
        with self._lock:
            self._data[run_id] = result
            self._data.move_to_end(run_id)
            while len(self._data) > self._max:
                self._data.popitem(last=False)

    def get(self, run_id: str) -> ModelResult | None:
        with self._lock:
            result = self._data.get(run_id)
            if result is not None:
                self._data.move_to_end(run_id)
            return result


_store: RunStore | None = None


def get_run_store() -> RunStore:
    global _store
    if _store is None:
        _store = RunStore()
    return _store
