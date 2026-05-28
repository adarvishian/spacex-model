"""Change history for audit cells — FRONTEND_PRD §6.3."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any

from spacex_model.config.settings import get_repo_root
from spacex_model.service.lineage import lookup_lineage

_DEV_LOG = get_repo_root() / "docs" / "DEV_LOG.md"
_ENTRY_HEADER = re.compile(r"^## (\d{4}-\d{2}-\d{2}) — (.+)$", re.MULTILINE)
_COMMIT_RE = re.compile(r"\b([0-9a-f]{7,40})\b")


def _git_sha() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=get_repo_root(),
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def _git_log_for_file(rel_path: str, *, limit: int = 10) -> list[dict[str, str]]:
    try:
        out = subprocess.check_output(
            [
                "git",
                "log",
                f"-{limit}",
                "--format=%H|%h|%ad|%s",
                "--date=short",
                "--",
                rel_path,
            ],
            cwd=get_repo_root(),
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []

    rows: list[dict[str, str]] = []
    for line in out.strip().splitlines():
        parts = line.split("|", 3)
        if len(parts) != 4:
            continue
        full_sha, short_sha, date, title = parts
        rows.append(
            {
                "date": date,
                "commit_sha": short_sha,
                "commit_sha_full": full_sha,
                "title": title,
            }
        )
    return rows


def _dev_log_entries() -> list[dict[str, Any]]:
    if not _DEV_LOG.is_file():
        return []
    text = _DEV_LOG.read_text(encoding="utf-8")
    entries: list[dict[str, Any]] = []
    matches = list(_ENTRY_HEADER.finditer(text))
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        anchor_slug = re.sub(r"[^a-z0-9]+", "-", match.group(2).lower()).strip("-")
        commit_match = _COMMIT_RE.search(body)
        entries.append(
            {
                "date": match.group(1),
                "title": match.group(2),
                "body": body[:500],
                "dev_log_anchor": f"docs/DEV_LOG.md#{anchor_slug}",
                "commit_sha": commit_match.group(1)[:7] if commit_match else None,
                "change_kind": _infer_kind(match.group(2), body),
            }
        )
    return entries


def _infer_kind(title: str, body: str) -> str:
    lower = (title + " " + body).lower()
    if "anchor" in lower or "calibration" in lower:
        return "anchor"
    if "formula" in lower or "refactor" in lower or "split" in lower:
        return "formula"
    if "initial" in lower or "first" in lower:
        return "initial"
    if "input" in lower or "override" in lower:
        return "input"
    return "formula"


def _module_rel_path(module_path: str) -> str | None:
    if not module_path or module_path == "unknown":
        return None
    rel = module_path.replace(".", "/") + ".py"
    candidate = get_repo_root() / "src" / rel
    if candidate.is_file():
        return f"src/{rel}"
    candidate = get_repo_root() / rel
    if candidate.is_file():
        return rel
    return None


def fetch_change_history(
    key: str,
    *,
    module_path: str | None = None,
    function: str | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Return reverse-chronological change history rows for a lineage key."""
    base = lookup_lineage(key)
    mod_path = module_path or (base.module_path if base else "")
    fn = function or (base.function if base else "")

    seen: set[str] = set()
    out: list[dict[str, Any]] = []

    rel = _module_rel_path(mod_path)
    if rel:
        for row in _git_log_for_file(rel, limit=min(limit, 10)):
            dedupe = f"{row['date']}:{row['commit_sha']}"
            if dedupe in seen:
                continue
            seen.add(dedupe)
            out.append(
                {
                    "date": row["date"],
                    "commit_sha": row["commit_sha"],
                    "title": row["title"],
                    "change_kind": "formula",
                    "effect_on_cell": None,
                    "dev_log_anchor": None,
                    "function": fn or None,
                }
            )

    for entry in _dev_log_entries():
        dedupe = f"{entry['date']}:{entry['title']}"
        if dedupe in seen:
            continue
        body = entry["body"].lower()
        if base and base.display_name.lower() not in body and key not in body:
            if not any(
                token in body
                for token in (
                    "sprint",
                    "frontend",
                    "audit",
                    "starlink",
                    "group",
                    "block",
                )
            ):
                continue
        seen.add(dedupe)
        out.append(
            {
                "date": entry["date"],
                "commit_sha": entry.get("commit_sha") or _git_sha() or "—",
                "title": entry["title"],
                "change_kind": entry["change_kind"],
                "effect_on_cell": None,
                "dev_log_anchor": entry["dev_log_anchor"],
                "summary": entry["body"][:240],
            }
        )

    if not out and base:
        out.append(
            {
                "date": "2026-05-12",
                "commit_sha": _git_sha() or "initial",
                "title": f"First derivation of {base.display_name}",
                "change_kind": "initial",
                "effect_on_cell": None,
                "dev_log_anchor": "docs/DEV_LOG.md",
                "summary": f"Registered in lineage as {base.module_path}.{base.function}",
            }
        )

    out.sort(key=lambda e: e["date"], reverse=True)
    return out[:limit]


def history_cache_key(lineage_key: str) -> str:
    sha = _git_sha() or "unknown"
    return f"history:{sha}:{lineage_key}"
