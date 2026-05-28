"""Model Translation Log generator — PRD §11.1 / §15."""

from __future__ import annotations

import ast
import csv
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from spacex_model.linters.docstrings import CALC_ROOT, iter_calc_sources

_TAG_PATTERNS = {
    "excel_cell": re.compile(r"Excel cell:\s*(.+)", re.MULTILINE),
    "excel_label": re.compile(r'Excel label:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE),
    "architecture_ref": re.compile(r"Architecture ref:\s*(.+)", re.MULTILINE),
    "principle": re.compile(r"Principle:\s*(.+)", re.MULTILINE),
}

_SHEET_FROM_REF = re.compile(r"^([A-Za-z][\w ]+)!", re.MULTILINE)


@dataclass(frozen=True, slots=True)
class TranslationLogRow:
    sheet: str
    row: str
    column_a_label: str
    excel_cell_range: str
    module_path: str
    function: str
    docstring_section: str


def _parse_docstring_tags(doc: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for tag, pattern in _TAG_PATTERNS.items():
        match = pattern.search(doc)
        if match:
            out[tag] = match.group(1).strip()
    return out


def _sheet_from_excel_cell(excel_cell: str) -> str:
    match = _SHEET_FROM_REF.match(excel_cell.strip())
    if match:
        return match.group(1).strip()
    if excel_cell.strip().endswith(" tab") or excel_cell.strip().endswith(" Tab"):
        return excel_cell.replace(" tab", "").replace(" Tab", "").strip()
    return ""


def iter_public_calc_functions() -> Iterator[tuple[Path, ast.FunctionDef | ast.AsyncFunctionDef]]:
    """Yield (source_path, AST node) for every public top-level calc function."""
    for path in iter_calc_sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            is_fn = isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            if is_fn and not node.name.startswith("_"):
                yield path, node


def _rows_from_ast(path: Path, node: ast.FunctionDef | ast.AsyncFunctionDef) -> TranslationLogRow:
    rel = path.relative_to(CALC_ROOT.parent)
    module_path = str(rel.with_suffix("")).replace("/", ".")
    doc = ast.get_docstring(node) or ""
    tags = _parse_docstring_tags(doc)
    excel_cell = tags.get("excel_cell", "")
    return TranslationLogRow(
        sheet=_sheet_from_excel_cell(excel_cell),
        row="",
        column_a_label=tags.get("excel_label", ""),
        excel_cell_range=excel_cell,
        module_path=module_path,
        function=node.name,
        docstring_section=tags.get("architecture_ref", ""),
    )


def generate_translation_log_rows() -> list[TranslationLogRow]:
    return [_rows_from_ast(path, node) for path, node in iter_public_calc_functions()]


def write_translation_log_csv(path: Path) -> int:
    """Write model_translation_log.csv; return row count."""
    rows = generate_translation_log_rows()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "sheet",
                "row",
                "column_a_label",
                "excel_cell_range",
                "module_path",
                "function",
                "docstring_section",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.sheet,
                    row.row,
                    row.column_a_label,
                    row.excel_cell_range,
                    row.module_path,
                    row.function,
                    row.docstring_section,
                ]
            )
    return len(rows)


def generate_architecture_diagram() -> str:
    """Mermaid tab→package mapping from translation log rows."""
    rows = generate_translation_log_rows()
    sheet_to_modules: dict[str, set[str]] = {}
    for row in rows:
        sheet = row.sheet or "Unmapped"
        if ".calc." in row.module_path:
            pkg = row.module_path.split(".calc.")[-1].split(".")[0]
        else:
            pkg = row.module_path
        sheet_to_modules.setdefault(sheet, set()).add(pkg)

    lines = [
        "# Architecture Diagram",
        "",
        "Auto-generated tab→package mapping per PRD §15.",
        "",
        "```mermaid",
        "flowchart LR",
    ]
    for sheet in sorted(sheet_to_modules):
        sid = re.sub(r"[^a-zA-Z0-9]", "_", sheet)
        for pkg in sorted(sheet_to_modules[sheet]):
            pid = re.sub(r"[^a-zA-Z0-9]", "_", pkg)
            lines.append(f'  {sid}["{sheet}"] --> {pid}["calc/{pkg}"]')
    lines.extend(["```", ""])
    return "\n".join(lines)


def write_architecture_diagram(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(generate_architecture_diagram(), encoding="utf-8")


def generate_translation_log(docs_dir: Path) -> tuple[Path, Path]:
    """Regenerate both PRD §15 deliverables under docs/."""
    csv_path = docs_dir / "model_translation_log.csv"
    md_path = docs_dir / "architecture_diagram.md"
    write_translation_log_csv(csv_path)
    write_architecture_diagram(md_path)
    return csv_path, md_path
