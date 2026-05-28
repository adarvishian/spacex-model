"""Engine package — pipeline and solver (lazy exports to avoid import cycles)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spacex_model.engine.pipeline import ModelResult

__all__ = ["ModelResult", "run_base_case"]


def run_base_case(*args, **kwargs):
    from spacex_model.engine.pipeline import run_base_case as _run

    return _run(*args, **kwargs)


def __getattr__(name: str):
    if name == "ModelResult":
        from spacex_model.engine.pipeline import ModelResult

        return ModelResult
    raise AttributeError(name)
