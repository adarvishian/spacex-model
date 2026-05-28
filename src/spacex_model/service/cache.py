"""Result cache — in-memory LRU with optional Redis backend per PRD §9.3."""

from __future__ import annotations

import json
import threading
import time
from collections import OrderedDict
from typing import Any, Protocol

from spacex_model.config.settings import get_settings


class ResultCache(Protocol):
    def get(self, key: str) -> dict[str, Any] | None: ...

    def set(self, key: str, value: dict[str, Any], *, ttl_sec: int | None = None) -> None: ...

    def delete(self, key: str) -> None: ...


class InMemoryCache:
    """Thread-safe LRU cache for deterministic run payloads."""

    def __init__(self, max_entries: int = 128) -> None:
        self._max = max_entries
        self._data: OrderedDict[str, tuple[float | None, dict[str, Any]]] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, key: str) -> dict[str, Any] | None:
        with self._lock:
            entry = self._data.get(key)
            if entry is None:
                return None
            expires_at, payload = entry
            if expires_at is not None and time.time() > expires_at:
                del self._data[key]
                return None
            self._data.move_to_end(key)
            return payload

    def set(self, key: str, value: dict[str, Any], *, ttl_sec: int | None = None) -> None:
        expires = time.time() + ttl_sec if ttl_sec else None
        with self._lock:
            self._data[key] = (expires, value)
            self._data.move_to_end(key)
            while len(self._data) > self._max:
                self._data.popitem(last=False)

    def delete(self, key: str) -> None:
        with self._lock:
            self._data.pop(key, None)


class RedisCache:
    """Optional Redis-backed cache when SPACEX_MODEL_REDIS_URL is set."""

    def __init__(self, url: str) -> None:
        import redis

        self._client = redis.from_url(url, decode_responses=True)

    def get(self, key: str) -> dict[str, Any] | None:
        raw = self._client.get(f"spacex_model:{key}")
        if raw is None:
            return None
        return json.loads(raw)

    def set(self, key: str, value: dict[str, Any], *, ttl_sec: int | None = None) -> None:
        payload = json.dumps(value)
        if ttl_sec:
            self._client.setex(f"spacex_model:{key}", ttl_sec, payload)
        else:
            self._client.set(f"spacex_model:{key}", payload)

    def delete(self, key: str) -> None:
        self._client.delete(f"spacex_model:{key}")


_cache: ResultCache | None = None


def get_cache() -> ResultCache:
    global _cache
    if _cache is None:
        settings = get_settings()
        if settings.redis_url:
            _cache = RedisCache(settings.redis_url)
        else:
            _cache = InMemoryCache(max_entries=settings.cache_max_entries)
    return _cache
