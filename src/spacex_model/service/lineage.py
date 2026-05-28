"""Lineage registry for audit panel — PRD §11.1 / context.md §5.4."""

from __future__ import annotations

import inspect
import re
from dataclasses import dataclass
from typing import Any

_TAG_PATTERNS = {
    "excel_cell": re.compile(r"Excel cell:\s*(.+)", re.MULTILINE),
    "excel_label": re.compile(r'Excel label:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE),
    "architecture_ref": re.compile(r"Architecture ref:\s*(.+)", re.MULTILINE),
    "principle": re.compile(r"Principle:\s*(.+)", re.MULTILINE),
}


@dataclass(frozen=True, slots=True)
class LineageEntry:
    """Audit lineage for one displayed output."""

    key: str
    display_name: str
    module_path: str
    function: str
    excel_cell: str
    excel_label: str
    architecture_ref: str
    principle: str
    input_labels: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "display_name": self.display_name,
            "module_path": self.module_path,
            "function": self.function,
            "excel_cell": self.excel_cell,
            "excel_label": self.excel_label,
            "architecture_ref": self.architecture_ref,
            "principle": self.principle,
            "input_labels": list(self.input_labels),
        }


def _parse_docstring(fn: Any) -> dict[str, str]:
    doc = inspect.getdoc(fn) or ""
    out: dict[str, str] = {}
    for tag, pattern in _TAG_PATTERNS.items():
        match = pattern.search(doc)
        if match:
            out[tag] = match.group(1).strip()
    return out


def _entry_from_fn(
    key: str,
    display_name: str,
    fn: Any,
    *,
    input_labels: tuple[str, ...] = (),
) -> LineageEntry:
    tags = _parse_docstring(fn)
    module = inspect.getmodule(fn)
    module_path = module.__name__ if module else "unknown"
    return LineageEntry(
        key=key,
        display_name=display_name,
        module_path=module_path,
        function=fn.__qualname__,
        excel_cell=tags.get("excel_cell", ""),
        excel_label=tags.get("excel_label", display_name),
        architecture_ref=tags.get("architecture_ref", ""),
        principle=tags.get("principle", ""),
        input_labels=input_labels,
    )


def build_lineage_registry() -> dict[str, LineageEntry]:
    """Build metric-key → lineage map from calc function docstrings."""
    from spacex_model.calc.group_pnl import (
        compute_group_ebitda,
        compute_group_fcf,
        compute_group_revenue_net,
    )
    from spacex_model.calc.valuation import compute_valuation

    entries = [
        _entry_from_fn(
            "group.group_revenue_net",
            "Group Revenue (net of eliminations)",
            compute_group_revenue_net,
            input_labels=("Σ module revenues", "inter-module eliminations"),
        ),
        _entry_from_fn(
            "group.group_ebitda",
            "Group EBITDA",
            compute_group_ebitda,
            input_labels=("Group Gross Profit", "Total OpEx"),
        ),
        _entry_from_fn(
            "group.group_fcf",
            "Group FCF",
            compute_group_fcf,
            input_labels=("NOPAT", "Total D&A add-back", "Total Group CapEx", "Mars carve-out"),
        ),
        _entry_from_fn(
            "valuation.implied_ev_2025",
            "Implied EV (10× revenue cross-check)",
            compute_valuation,
            input_labels=("Group Revenue net", "Revenue multiple"),
        ),
    ]

    module_labels = {
        "customer_launch": "Customer Launch",
        "starlink": "Starlink",
        "odc": "ODC",
        "ai_stack": "AI Stack",
        "lunar_mars": "Lunar Mars",
    }
    for mod_key, mod_name in module_labels.items():
        entries.append(
            LineageEntry(
                key=f"module.{mod_key}.module_fcf",
                display_name=f"{mod_name} Module FCF",
                module_path=f"spacex_model.calc.{mod_key.replace('_', '_')}",
                function="compute_allocator_out",
                excel_cell=f"{mod_name}!—",
                excel_label="Module FCF ($mm)",
                architecture_ref="§3 vending-machine framing",
                principle="8 (module FCF pre-tax, pre-corp)",
                input_labels=("Module EBITDA", "Module D&A add-back", "Module CapEx"),
            )
        )
        entries.append(
            LineageEntry(
                key=f"module.{mod_key}.total_revenue",
                display_name=f"{mod_name} Total Revenue",
                module_path=f"spacex_model.calc.{mod_key.replace('_', '_')}",
                function="compute_allocator_out",
                excel_cell=f"{mod_name}!—",
                excel_label="Total Revenue ($mm)",
                architecture_ref="§3 vending-machine framing",
                principle="7 (Module EBITDA = Gross Profit)",
            )
        )

    return {e.key: e for e in entries}


_REGISTRY: dict[str, LineageEntry] | None = None


def get_lineage_registry() -> dict[str, LineageEntry]:
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = build_lineage_registry()
    return _REGISTRY


def lookup_lineage(key: str) -> LineageEntry | None:
    return get_lineage_registry().get(key)
