"""Sprint R0 gate tests — V4.131 ingest, horizon 2025–2040, canonical labels."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from spacex_model.config.constants import FIRST_YEAR, HORIZON_YEARS, LAST_YEAR
from spacex_model.config.canonical_labels import CANONICAL_LABELS, LABELS_BY_SHEET
from spacex_model.config.settings import get_settings
from spacex_model.domain.year_vector import YearVector
from spacex_model.inputs.assumptions import assumptions_from_ingest
from spacex_model.inputs.v4_131_2025_anchors import V4_131_INGEST_ANCHORS_2025
from spacex_model.io.anchor_checks import check_s1_anchors
from spacex_model.io.excel_ingest import ingest_workbook
from spacex_model.io.snapshot_store import ingest_to_snapshot_dict, write_diagnostic_snapshot
from spacex_model.linters.canonical_labels import find_workbook_labels_missing_from_registry

REPO = Path(__file__).resolve().parents[1]
WORKBOOK = REPO / "SpaceX V4.131.xlsx"

V4_131_TABS = frozenset(
    {
        "Assumptions",
        "Demand Curves",
        "Starlink",
        "Customer Launch",
        "Cash Allocation Engine",
        "AI - Compute",
        "Lunar - Mars",
        "Vehicle Build",
        "Launch Dashboard",
        "Facilities Build",
        "Group P&L",
        "Segment P&L",
        "Conservation",
        "SoTP - Valuation",
    }
)


@pytest.fixture(scope="module")
def ingest():
    if not WORKBOOK.exists():
        pytest.skip("V4.131 workbook not present")
    return ingest_workbook(WORKBOOK)


def test_settings_default_workbook_v4_131() -> None:
    settings = get_settings()
    assert settings.workbook_path.name == "SpaceX V4.131.xlsx"


def test_horizon_constants() -> None:
    assert FIRST_YEAR == 2025
    assert LAST_YEAR == 2040
    assert HORIZON_YEARS == 16


def test_year_vector_shape() -> None:
    z = YearVector.zeros()
    assert len(z) == 16
    assert z.year_index(2040) == 15
    with pytest.raises(ValueError, match="outside horizon"):
        z.year_index(2041)


def test_v4_131_tab_inventory(ingest) -> None:
    assert V4_131_TABS <= frozenset(ingest.formula_pass.sheet_names)


def test_every_column_a_label_resolves(ingest) -> None:
    violations = find_workbook_labels_missing_from_registry(LABELS_BY_SHEET, intentionally_unused=frozenset())
    assert violations == [], "\n".join(violations[:30])


def test_assumptions_schema_validates(ingest) -> None:
    assumptions = assumptions_from_ingest(ingest)
    assert len(assumptions.by_label) > 200
    assert 0.20 <= assumptions.tax_rate <= 0.22
    assert assumptions.starting_cash_eoy_2024 == 11_385.0
    vec = assumptions.by_label["Broadband ARPU ($/sub/mo): year-row"].as_year_vector()
    assert vec.shape == (HORIZON_YEARS,)
    assert vec[0] == 81.0


def test_2025_anchors_load(ingest) -> None:
    assumptions = assumptions_from_ingest(ingest)
    warnings = check_s1_anchors(assumptions)
    assert warnings == [], "\n".join(warnings)
    for anchor in V4_131_INGEST_ANCHORS_2025:
        assert anchor.assumptions_label in assumptions.by_label


def test_diagnostic_snapshot_rebuilt(ingest, tmp_path: Path) -> None:
    snap = ingest_to_snapshot_dict(ingest)
    assert len(snap["horizon"]["years"]) == 16
    assert snap["workbook_version"] == "SpaceX V4.131.xlsx"
    assert len(snap["label_rows"]) == len(V4_131_TABS)
    assert "duplicate_labels" in snap
    assert all(snap["year_value_coverage"][str(y)] > 0 for y in range(2025, 2041))

    out = tmp_path / "xlsx_snapshot.json"
    write_diagnostic_snapshot(ingest, out)
    assert out.exists()


def test_canonical_registry_nonempty() -> None:
    assert len(CANONICAL_LABELS) > 1500


@pytest.mark.slow
def test_v4_131_audit_grid_sheets_have_rows() -> None:
    """Audit tabs must resolve V4.131 workbook names (not legacy V2.16 tab names)."""
    from spacex_model.engine.pipeline import run_base_case
    from spacex_model.service.grid import build_grid_payload
    from spacex_model.service.sheets_meta import get_sheet

    result = run_base_case(WORKBOOK, write_outputs=False)
    for slug in (
        "allocator",
        "launch_capacity",
        "starlink_capacity",
        "ai_stack",
        "lunar_mars",
        "opex",
        "capex",
        "valuation",
    ):
        meta = get_sheet(slug)
        assert meta is not None
        assert meta.source_sheet in result.ingest.value_pass.labels_by_sheet
        grid = build_grid_payload(meta, result)
        assert len(grid["rows"]) > 0, slug
