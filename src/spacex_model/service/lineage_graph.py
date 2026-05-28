"""Dependency graph for audit flow diagram — FRONTEND_PRD §4.4 / §8.1."""

from __future__ import annotations

from typing import Any

from spacex_model.engine.pipeline import ModelResult
from spacex_model.service.lineage_enrich import enrich_lineage


def _node_id(key: str) -> str:
    return key.replace(".", "_")


def build_lineage_graph(
    key: str,
    result: ModelResult,
    *,
    depth: int = 2,
    year: int | None = None,
    sheet: str | None = None,
    row: int | None = None,
) -> dict[str, Any]:
    """Return react-flow nodes + edges rooted at `key`, expanded `depth` levels upstream."""
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    visited: set[str] = set()

    def label_for(entry: dict[str, Any]) -> str:
        addr = entry.get("cell_address") or {}
        sheet_name = addr.get("sheet") or ""
        row_id = addr.get("row") or ""
        yr = addr.get("year") or year
        name = entry.get("display_name") or entry.get("key", key)
        if sheet_name and row_id:
            return f"{sheet_name}!{row_id}"
        return name

    def subtitle_for(entry: dict[str, Any]) -> str:
        val = entry.get("computed_value")
        unit = entry.get("unit") or ""
        yr = (entry.get("cell_address") or {}).get("year") or year
        if val is None:
            return str(entry.get("display_name", ""))[:40]
        if unit == "dollars_mm":
            return f"${val:,.0f}mm · {yr}"
        if unit == "pct" or unit == "ratio":
            return f"{val:.1%} · {yr}" if abs(val) < 5 else f"{val:,.2f} · {yr}"
        return f"{val:,.0f} · {yr}"

    def add_node(k: str, entry: dict[str, Any], *, is_active: bool = False) -> None:
        nid = _node_id(k)
        if nid in nodes:
            if is_active:
                nodes[nid]["data"]["active"] = True
            return
        nodes[nid] = {
            "id": nid,
            "type": "auditCell",
            "position": {"x": 0, "y": 0},
            "data": {
                "key": k,
                "label": label_for(entry),
                "subtitle": subtitle_for(entry),
                "active": is_active,
                "sheet": (entry.get("cell_address") or {}).get("sheet"),
                "row": (entry.get("cell_address") or {}).get("row"),
                "year": (entry.get("cell_address") or {}).get("year") or year,
            },
        }

    def walk(k: str, remaining: int, *, is_root: bool = False) -> None:
        if k in visited:
            return
        visited.add(k)
        try:
            entry = enrich_lineage(k, result, year=year, sheet=sheet, row=row if is_root else None)
        except KeyError:
            return

        add_node(k, entry, is_active=is_root)

        upstream = entry.get("upstream") or []
        for u in upstream:
            uk = u.get("key")
            if not uk:
                continue
            try:
                u_entry = enrich_lineage(uk, result, year=year)
            except KeyError:
                u_entry = {
                    "key": uk,
                    "display_name": u.get("label", uk),
                    "computed_value": None,
                    "unit": "",
                }
            add_node(uk, u_entry)
            edges.append(
                {
                    "id": f"{_node_id(uk)}->{_node_id(k)}",
                    "source": _node_id(uk),
                    "target": _node_id(k),
                    "type": "smoothstep",
                    "animated": False,
                }
            )
            if remaining > 1:
                walk(uk, remaining - 1)

        if is_root:
            for inp in entry.get("resolved_inputs") or []:
                ik = inp.get("lineage_key")
                if not ik or ik.startswith("grid.resolved"):
                    continue
                if ik in visited:
                    continue
                u_entry = {
                    "key": ik,
                    "display_name": inp.get("label", ik),
                    "computed_value": inp.get("value"),
                    "unit": inp.get("unit", ""),
                    "cell_address": {
                        "sheet": inp.get("cell_address", "").split("!")[0] if "!" in inp.get("cell_address", "") else "",
                        "row": inp.get("cell_address", "").split("!")[-1] if "!" in inp.get("cell_address", "") else "",
                        "year": year,
                    },
                }
                add_node(ik, u_entry)
                edges.append(
                    {
                        "id": f"{_node_id(ik)}->{_node_id(k)}",
                        "source": _node_id(ik),
                        "target": _node_id(k),
                        "type": "smoothstep",
                    }
                )
                if remaining > 1:
                    walk(ik, remaining - 1)

    walk(key, depth, is_root=True)

    node_list = list(nodes.values())
    _layout_nodes(node_list, edges)

    return {
        "root_key": key,
        "depth": depth,
        "nodes": node_list,
        "edges": edges,
    }


def _layout_nodes(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> None:
    """Simple layered layout: sources left, root right."""
    if not nodes:
        return
    depth_of: dict[str, int] = {n["id"]: 0 for n in nodes}
    for _ in range(len(nodes) + 2):
        changed = False
        for e in edges:
            src, tgt = e["source"], e["target"]
            if depth_of.get(tgt, 0) <= depth_of.get(src, 0):
                depth_of[tgt] = depth_of.get(src, 0) + 1
                changed = True
        if not changed:
            break

    by_depth: dict[int, list[str]] = {}
    for nid, d in depth_of.items():
        by_depth.setdefault(d, []).append(nid)

    x_gap, y_gap = 220, 70
    id_to_node = {n["id"]: n for n in nodes}
    for d, ids in sorted(by_depth.items()):
        for i, nid in enumerate(ids):
            node = id_to_node[nid]
            node["position"] = {"x": d * x_gap, "y": i * y_gap}
