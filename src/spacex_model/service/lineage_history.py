"""Per-cell change history from xlsx ingest diffs — PRD L3 / FRONTEND_PRD §6.3."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from spacex_model.io.snapshot_store import read_cell_changes


def _title_for_change(record: dict[str, Any]) -> str:
    kind = record["change_kind"]
    version = record["model_version"]
    year = record.get("year")
    year_part = f" {year}" if year else ""
    if kind == "initial":
        return f"First ingest — {version}{year_part}"
    if kind == "formula":
        return f"Formula updated — {version}{year_part}"
    if kind == "anchor":
        return f"Anchor value moved — {version}{year_part}"
    if kind == "input":
        return f"Input assumption changed — {version}{year_part}"
    if kind == "added":
        return f"Variable added — {version}{year_part}"
    if kind == "removed":
        return f"Variable removed — {version}{year_part}"
    if kind == "renamed":
        prior = record.get("prior_label") or "prior label"
        return f"Renamed from {prior!r} — {version}{year_part}"
    return f"Value updated — {version}{year_part}"


def _effect_on_cell(record: dict[str, Any]) -> dict[str, float | None] | None:
    kind = record["change_kind"]
    after = record.get("new_value")
    if kind == "initial":
        return {"before": None, "after": after, "delta": None}
    before = record.get("prior_value")
    if before is None and after is None:
        return None
    return {
        "before": before,
        "after": after,
        "delta": record.get("delta"),
    }


def _to_api_entry(record: dict[str, Any]) -> dict[str, Any]:
    timestamp = record.get("timestamp", "")
    date = timestamp[:10] if len(timestamp) >= 10 else timestamp
    commit = record.get("commit_sha") or record.get("model_version") or "—"
    return {
        "date": date,
        "commit_sha": commit,
        "title": _title_for_change(record),
        "change_kind": record["change_kind"],
        "effect_on_cell": _effect_on_cell(record),
        "dev_log_anchor": None,
        "summary": None,
        "model_version": record.get("model_version"),
        "year": record.get("year"),
    }


def fetch_change_history(
    key: str,
    *,
    year: int | None = None,
    limit: int = 20,
    store_dir: Path | None = None,
) -> list[dict[str, Any]]:
    """Return reverse-chronological change history for a lineage key."""
    records = read_cell_changes(key, year=year, store_dir=store_dir)
    records.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    return [_to_api_entry(r) for r in records[:limit]]


def history_cache_key(lineage_key: str, *, year: int | None = None) -> str:
    from spacex_model.io.snapshot_store import _metadata_path, cell_history_dir

    root = cell_history_dir()
    meta = ""
    meta_path = _metadata_path(root)
    if meta_path.is_file():
        meta = meta_path.read_text(encoding="utf-8")[:64]
    year_tag = str(year) if year is not None else "all"
    return f"history:{meta}:{year_tag}:{lineage_key}"
