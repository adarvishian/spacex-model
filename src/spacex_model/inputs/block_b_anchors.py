"""Block B S-1 audited 2025 anchors — shared by API Run Audit tab and reconciliation tests."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BlockBAnchor:
    name: str
    target: float
    tolerance: float
    halt_low: float
    halt_high: float


def _anchor(
    name: str,
    target: float,
    tolerance: float,
    *,
    halt_margin: float | None = None,
) -> BlockBAnchor:
    margin = halt_margin if halt_margin is not None else tolerance * 2
    if target == 0:
        halt_low = target - margin * 1000
        halt_high = target + margin * 1000
    elif target < 0:
        halt_low = target * (1 + margin)
        halt_high = target * (1 - margin)
    else:
        halt_low = target * (1 - margin)
        halt_high = target * (1 + margin)
    return BlockBAnchor(name, target, tolerance, halt_low, halt_high)


# Full model may not yet reconcile every S-1 line after P0 inputs-only pass.
BLOCK_B_CALIBRATION_PENDING: frozenset[str] = frozenset(
    {
        "Group Revenue 2025",
        "Group Gross Profit 2025",
        "Group EBITDA 2025",
        "Group D&A 2025",
        "Group FCF 2025",
        "Total OpEx 2025",
        "Total Group CapEx 2025",
        "Connectivity segment revenue 2025",
        "Space segment revenue 2025",
        "Cash EoY 2025",
        "Adjusted EBITDA 2025",
    }
)


def load_block_b_anchors_v1() -> list[BlockBAnchor]:
    """S-1 audited 2025 anchors per adherence audit §7.5."""
    return [
        _anchor("Group Revenue 2025", 18_674.0, 0.02),
        _anchor("Space segment revenue 2025", 4_086.0, 0.02),
        _anchor("Connectivity segment revenue 2025", 11_387.0, 0.02),
        _anchor("AI segment revenue 2025", 3_201.0, 0.02),
        _anchor("F9 customer launches 2025", 43.0, 0.0, halt_margin=0.05),
        _anchor("Starting cash EoY 2024", 11_385.0, 0.0, halt_margin=0.001),
        _anchor("Total Group CapEx 2025", 20_737.0, 0.05),
        _anchor("Group Gross Profit 2025", 9_223.0, 0.10),
        _anchor("Group EBITDA 2025", 6_584.0, 0.10),
        _anchor("Group D&A 2025", 6_701.0, 0.10),
        _anchor("Group FCF 2025", -13_952.0, 0.15),
        _anchor("Total OpEx 2025", 11_287.0, 0.10),
        _anchor("Cash EoY 2025", 24_747.0, 0.02),
        _anchor("Adjusted EBITDA 2025", 6_584.0, 0.10),
        BlockBAnchor("Mars carve-out 2025", 1_000.0, 0.0, 999.0, 1_001.0),
    ]
