#!/usr/bin/env python3
"""Generate committed cell-history store from workbook lineage (Milestone 2.4)."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from spacex_model.config.settings import get_repo_root  # noqa: E402
from spacex_model.io.excel_ingest import run_formula_pass, run_value_pass  # noqa: E402
from spacex_model.io.excel_ingest import IngestResult, _parse_demand_curves_pass  # noqa: E402
from spacex_model.io.snapshot_store import (  # noqa: E402
    _changes_path,
    _metadata_path,
    _snapshot_path,
    record_ingest_changes,
)


def _ingest(path: Path) -> IngestResult:
    formula = run_formula_pass(path)
    values = run_value_pass(path)
    demand = _parse_demand_curves_pass(path)
    values.warnings.extend(demand.warnings)
    return IngestResult(
        workbook_path=path,
        formula_pass=formula,
        value_pass=values,
        demand_curves=demand,
    )


def generate_cell_history(
    *,
    from_workbook: Path,
    to_workbook: Path,
    output_dir: Path,
    reset: bool = True,
) -> int:
    if reset and output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ingest_old = _ingest(from_workbook)
    record_ingest_changes(ingest_old, store_dir=output_dir)

    ingest_new = _ingest(to_workbook)
    changes = record_ingest_changes(ingest_new, store_dir=output_dir)

    kinds = {c["change_kind"] for c in changes}
    print(f"Cell history: {output_dir}")
    print(f"  From: {from_workbook.name}")
    print(f"  To:   {to_workbook.name}")
    print(f"  Changes on migration: {len(changes)} ({', '.join(sorted(kinds))})")
    print(f"  Snapshot: {_snapshot_path(output_dir)}")
    print(f"  Changes:  {_changes_path(output_dir)}")
    print(f"  Meta:     {_metadata_path(output_dir)}")
    return 0


def main() -> int:
    root = get_repo_root()
    parser = argparse.ArgumentParser(description="Generate committed cell-history parquet store")
    parser.add_argument(
        "--from-workbook",
        type=Path,
        default=root / "SpaceX V4.113.xlsx",
    )
    parser.add_argument(
        "--to-workbook",
        type=Path,
        default=root / "SpaceX V4.131.xlsx",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=root / "data" / "cell_history",
    )
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Append to existing store instead of wiping",
    )
    args = parser.parse_args()
    if not args.from_workbook.is_file():
        print(f"Missing: {args.from_workbook}", file=sys.stderr)
        return 1
    if not args.to_workbook.is_file():
        print(f"Missing: {args.to_workbook}", file=sys.stderr)
        return 1
    return generate_cell_history(
        from_workbook=args.from_workbook,
        to_workbook=args.to_workbook,
        output_dir=args.output_dir,
        reset=not args.no_reset,
    )


if __name__ == "__main__":
    raise SystemExit(main())
