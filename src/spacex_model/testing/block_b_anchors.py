"""Pytest helpers for Block B — anchor data lives in inputs.block_b_anchors."""

from __future__ import annotations

import pytest

from spacex_model.inputs.block_b_anchors import (
    BLOCK_B_CALIBRATION_PENDING,
    BlockBAnchor,
    load_block_b_anchors_v1,
)

__all__ = [
    "BLOCK_B_CALIBRATION_PENDING",
    "BlockBAnchor",
    "load_block_b_anchors_v1",
    "load_block_b_parametrize_args",
]


def load_block_b_parametrize_args() -> list:
    rows: list = []
    for anchor in load_block_b_anchors_v1():
        row = (anchor.name, anchor.target, anchor.tolerance, anchor.halt_low, anchor.halt_high)
        if anchor.name in BLOCK_B_CALIBRATION_PENDING:
            rows.append(
                pytest.param(
                    *row,
                    marks=pytest.mark.xfail(
                        reason="S-1 full-segment reconciliation pending — P0 inputs landed",
                        strict=False,
                    ),
                )
            )
        else:
            rows.append(row)
    return rows
