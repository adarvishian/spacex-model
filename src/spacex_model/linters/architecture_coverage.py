"""Block D architecture-section coverage linter — PRD §7.4."""

from __future__ import annotations

import ast
import re
from pathlib import Path

from spacex_model.linters.docstrings import CALC_ROOT, iter_calc_sources

_REPO_ROOT = CALC_ROOT.parents[1]
_ARCHITECTURE_DOC = (
    _REPO_ROOT
    / "Pre Existing Model Package"
    / "00_Constitutional_Docs"
    / "02_Architecture_and_Methodology.md"
)

_SECTION_HEADER = re.compile(r"^## (§\d+)\b", re.MULTILINE)
_ARCH_REF = re.compile(r"Architecture ref:\s*(.+)", re.MULTILINE)

# Sections deferred to v1.x / stub modules per PRD D3 and audit backlog.
INTENTIONALLY_UNCOVERED_SECTIONS: frozenset[str] = frozenset(
    {
        "§14",  # Demand Curves tab — read-only ingest, no calc module
        "§18",  # Open items — meta section
        "§19",  # Amendment log — meta section
        "§20",  # Sprint amendments — meta section
    }
)


def parse_architecture_sections(doc_path: Path | None = None) -> set[str]:
    """Return top-level §N section ids from Architecture & Methodology."""
    path = doc_path or _ARCHITECTURE_DOC
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return set(_SECTION_HEADER.findall(text))


def parse_docstring_architecture_refs() -> set[str]:
    """Aggregate Architecture ref: §N tokens from public calc functions."""
    refs: set[str] = set()
    for path in iter_calc_sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("_"):
                continue
            doc = ast.get_docstring(node) or ""
            match = _ARCH_REF.search(doc)
            if not match:
                continue
            for token in re.findall(r"§\d+(?:\.\d+)?", match.group(1)):
                refs.add(token.split(".")[0])
    return refs


def find_uncovered_architecture_sections() -> list[str]:
    """Sections in Architecture doc with no calc function citing them."""
    sections = parse_architecture_sections()
    code_refs = parse_docstring_architecture_refs()
    uncovered = sorted(
        s for s in sections - code_refs if s not in INTENTIONALLY_UNCOVERED_SECTIONS
    )
    return uncovered
