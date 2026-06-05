"""ODC — deprecated; use calc.ai_compute (V4.113 AI - Compute tab)."""

from spacex_model.calc.ai_compute import (
    AiComputeInputs as OdcInputs,
    compute_allocator_out,
    odc_bandwidth_claim,
)

__all__ = ["OdcInputs", "compute_allocator_out", "odc_bandwidth_claim"]
