"""CLI: workbook rebase — drift report, remap proposal, validation, registry apply."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from spacex_model.config.settings import get_repo_root
from spacex_model.io.label_remaps import (
    load_remap_table,
    validate_remap_table,
    write_remap_table,
)
from spacex_model.io.rebase_drift import (
    apply_remap_strings,
    compute_drift,
    propose_remap,
    validate_or_raise,
    write_drift_report,
)


def _repo_root() -> Path:
    return get_repo_root()


def _cmd_drift(args: argparse.Namespace) -> int:
    from_wb = args.from_workbook or (_repo_root() / "SpaceX V4.113.xlsx")
    to_wb = args.to_workbook or (_repo_root() / "SpaceX V4.131.xlsx")
    if not from_wb.is_file():
        print(f"Missing workbook: {from_wb}", file=sys.stderr)
        return 1
    if not to_wb.is_file():
        print(f"Missing workbook: {to_wb}", file=sys.stderr)
        return 1
    drift = compute_drift(from_wb, to_wb)
    if args.output:
        write_drift_report(drift, args.output)
        print(f"Wrote drift report: {args.output}")
    else:
        print(json.dumps(drift.to_dict(), indent=2))
    print(
        f"Summary: {len(drift.exact_matches)} exact, {len(drift.moved)} moved, "
        f"{len(drift.removed)} removed, {len(drift.added)} added, "
        f"{len(drift.fuzzy_candidates)} fuzzy",
        file=sys.stderr,
    )
    return 0


def _cmd_propose(args: argparse.Namespace) -> int:
    from_wb = args.from_workbook or (_repo_root() / "SpaceX V4.113.xlsx")
    to_wb = args.to_workbook or (_repo_root() / "SpaceX V4.131.xlsx")
    drift = compute_drift(from_wb, to_wb)
    table = propose_remap(drift, fuzzy_threshold=args.fuzzy_threshold)
    out = args.output or (_repo_root() / "data" / "label_remaps" / "proposed.json")
    write_remap_table(table, out)
    errors = validate_remap_table(table, allow_flagged=True)
    print(f"Wrote remap proposal: {out} ({len(table.entries)} entries)")
    if errors:
        print("Validation notes:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    path = args.remap_file
    table = load_remap_table(path)
    if table is None:
        print(f"Could not load remap file: {path}", file=sys.stderr)
        return 1
    errors = validate_remap_table(table, allow_flagged=not args.strict)
    if errors:
        print("Validation failed:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print(f"Remap file OK: {path} ({len(table.entries)} entries)")
    return 0


def _cmd_apply(args: argparse.Namespace) -> int:
    path = args.remap_file
    table = load_remap_table(path)
    if table is None:
        print(f"Could not load remap file: {path}", file=sys.stderr)
        return 1
    if args.check_units:
        validate_or_raise(table)
    if args.dry_run:
        print(
            f"Dry run: would patch sources from {path} ({len(table.entries)} entries)"
        )
        return 0
    count = apply_remap_strings(table)
    print(f"Applied remap strings to {count} files")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Workbook rebase workflow — drift, remap proposal, validation, apply"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_drift = sub.add_parser(
        "drift", help="Structural drift report between two workbooks"
    )
    p_drift.add_argument("--from-workbook", type=Path, default=None)
    p_drift.add_argument("--to-workbook", type=Path, default=None)
    p_drift.add_argument("--output", type=Path, default=None)
    p_drift.set_defaults(func=_cmd_drift)

    p_prop = sub.add_parser("propose", help="Propose label remap JSON from drift")
    p_prop.add_argument("--from-workbook", type=Path, default=None)
    p_prop.add_argument("--to-workbook", type=Path, default=None)
    p_prop.add_argument("--output", type=Path, default=None)
    p_prop.add_argument("--fuzzy-threshold", type=float, default=0.72)
    p_prop.set_defaults(func=_cmd_propose)

    p_val = sub.add_parser("validate", help="Validate a remap JSON file")
    p_val.add_argument("remap_file", type=Path)
    p_val.add_argument(
        "--strict",
        action="store_true",
        help="Fail on flagged many-to-one remaps",
    )
    p_val.set_defaults(func=_cmd_validate)

    p_apply = sub.add_parser(
        "apply", help="Apply remap strings to Python source registry"
    )
    p_apply.add_argument("remap_file", type=Path)
    p_apply.add_argument("--dry-run", action="store_true")
    p_apply.add_argument(
        "--check-units",
        action="store_true",
        help="Hard-fail on unit-incompatible unflagged remaps before apply",
    )
    p_apply.set_defaults(func=_cmd_apply)

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
