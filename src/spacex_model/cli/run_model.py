"""CLI: run Base Case model and Phase E reconciliation harness."""

from __future__ import annotations

import argparse
from pathlib import Path

from spacex_model.config.settings import get_settings
from spacex_model.engine.pipeline import run_base_case, run_pipeline
from spacex_model.io.reconciliation_report import write_reconciliation_report


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Mach33 SpaceX valuation model")
    parser.add_argument(
        "--base-case",
        action="store_true",
        help="Run Base Case deterministic pipeline",
    )
    parser.add_argument("--workbook", type=Path, default=None, help="Path to V2.16 xlsx")
    parser.add_argument("--run-id", type=str, default=None, help="Optional run identifier")
    parser.add_argument(
        "--scenario",
        type=Path,
        default=None,
        help="Path to scenario YAML file",
    )
    parser.add_argument(
        "--reconcile",
        action="store_true",
        help="Run full Phase E reconciliation harness (base + stress scenarios)",
    )
    parser.add_argument(
        "--no-write-outputs",
        action="store_true",
        help="Skip writing outputs/ and reconciliation report",
    )
    args = parser.parse_args(argv)

    if args.reconcile:
        from spacex_model.engine.reconciliation import run_reconciliation_harness

        print("Running Phase E reconciliation harness...")
        harness = run_reconciliation_harness(write_outputs=not args.no_write_outputs)
        print(harness.summary())
        if harness.errors:
            for err in harness.errors:
                print(f"ERROR: {err}")
            return 1
        if not harness.all_stress_converged or not harness.all_stress_block_a:
            print("FAIL: stress scenario convergence or Block A")
            return 1
        if not harness.zero_open_triage_a_or_d:
            print("FAIL: open type-(A) or type-(D) triage entries remain")
            return 1
        base = harness.scenario_results.get("base_case")
        if base and not args.no_write_outputs:
            stress_summary = {
                name: {
                    "converged": harness.stress_convergence.get(name, False),
                    "block_a": harness.stress_block_a.get(name, False),
                }
                for name in harness.scenario_results
            }
            report_path = _repo_root() / "docs" / "reconciliation_report.md"
            write_reconciliation_report(
                base,
                report_path,
                divergence=harness.divergence,
                stress_summary=stress_summary,
            )
            print(f"Reconciliation report: {report_path}")
        print("Phase E reconciliation PASS")
        return 0

    if not args.base_case and args.scenario is None:
        parser.print_help()
        return 0

    settings = get_settings()
    workbook = args.workbook

    if args.scenario:
        print(f"Running scenario: {args.scenario}")
        result = run_pipeline(
            workbook_path=workbook,
            scenario_path=args.scenario,
            run_id=args.run_id,
            write_outputs=not args.no_write_outputs,
        )
    else:
        print(f"Ingesting workbook: {workbook or settings.workbook_path}")
        result = run_base_case(
            workbook_path=workbook,
            run_id=args.run_id,
            write_outputs=not args.no_write_outputs,
        )

    print(f"Run ID: {result.run_id}")
    print(f"Scenario: {result.audit.get('scenario', 'base_case')}")
    print(f"Assumptions rows: {len(result.assumptions.by_label)}")
    print(f"Solver: {result.solver_trace.iterations} iter, converged={result.solver_trace.converged}")
    print(f"Wall clock: {result.audit['wall_clock_sec']}s")

    if not args.no_write_outputs and args.scenario is None:
        report_path = _repo_root() / "docs" / "reconciliation_report.md"
        write_reconciliation_report(result, report_path)
        print(f"Reconciliation report: {report_path}")
        print(f"Outputs: {settings.outputs_dir / result.run_id}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
