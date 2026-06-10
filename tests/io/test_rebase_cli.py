"""Tests for spacex-rebase CLI and drift analysis."""

from __future__ import annotations

import pytest

from spacex_model.config.settings import get_repo_root
from spacex_model.io.label_remaps import load_remap_table, validate_remap_table
from spacex_model.io.rebase_drift import compute_drift, propose_remap

REPO = get_repo_root()
FROM = REPO / "SpaceX V4.113.xlsx"
TO = REPO / "SpaceX V4.131.xlsx"
REMAP = REPO / "data" / "label_remaps" / "v4_113__v4_131.json"


@pytest.mark.skipif(not FROM.exists() or not TO.exists(), reason="workbooks missing")
def test_compute_drift_v4_113_to_v4_131() -> None:
    drift = compute_drift(FROM, TO)
    assert drift.from_workbook == FROM.name
    assert drift.to_workbook == TO.name
    assert drift.removed or drift.added or drift.moved or drift.exact_matches


@pytest.mark.skipif(not FROM.exists() or not TO.exists(), reason="workbooks missing")
def test_propose_remap_has_entries() -> None:
    drift = compute_drift(FROM, TO)
    table = propose_remap(drift)
    assert table.entries


@pytest.mark.skipif(not REMAP.exists(), reason="remap file missing")
def test_committed_remap_table_loads() -> None:
    table = load_remap_table(REMAP)
    assert table is not None
    assert len(table.entries) >= 60
    errors = validate_remap_table(table, allow_flagged=True)
    blocking = [
        e for e in errors if "Unit-incompatible" in e and "flagged" not in e.lower()
    ]
    assert not blocking


def test_rebase_cli_validate(capsys) -> None:
    pytest.importorskip("spacex_model.cli.rebase")
    from spacex_model.cli.rebase import main

    if not REMAP.exists():
        pytest.skip("remap file missing")
    rc = main(["validate", str(REMAP)])
    assert rc == 0
