"""Client Mode — curated scenarios, vetted inputs, share-link overrides (FRONTEND_PRD §7)."""

from __future__ import annotations

import base64
import json
from typing import Any

from pydantic import BaseModel, Field

# PRD §7.2 — id → canonical Assumptions label; year_index for year-row overrides
CLIENT_INPUT_SPECS: tuple[dict[str, Any], ...] = (
    {
        "id": "mars_pct",
        "canonical_label": "Mars carve-out % of prior-year Group FCF",
        "min": 0.0,
        "max": 0.20,
        "default": 0.05,
        "plain_label": "Share of group FCF dedicated to Mars",
        "year": None,
    },
    {
        "id": "starship_dollars_per_kg_2030",
        "canonical_label": "Blended $/kg",
        "min": 200.0,
        "max": 3000.0,
        "default": 1200.0,
        "plain_label": "Starship cost-to-LEO at 2030 ($/kg)",
        "year": 2030,
    },
    {
        "id": "odc_prob_a",
        "canonical_label": "Credence on Model A (Pr(A))",
        "min": 0.0,
        "max": 1.0,
        "default": 0.40,
        "plain_label": "Probability ODC achieves dual revenue (Model A)",
        "year": None,
    },
    {
        "id": "wrights_law_learning_rate",
        "canonical_label": "Starship manufacturing WL learning rate (% reduction per doubling cum stacks)",
        "min": 0.05,
        "max": 0.35,
        "default": 0.22,
        "plain_label": "Wright's Law learning rate on Starship cadence",
        "year": None,
    },
    {
        "id": "starlink_dtc_arpu_2030",
        "canonical_label": "DTC ARPU ($/sub/mo, year-row)",
        "min": 5.0,
        "max": 50.0,
        "default": 18.0,
        "plain_label": "Direct-to-Cell ARPU at 2030 ($/month)",
        "year": 2030,
    },
    {
        "id": "tam_inflation_rate",
        "canonical_label": "TAM inflation rate (annual)",
        "min": 0.0,
        "max": 0.06,
        "default": 0.025,
        "plain_label": "Long-run TAM inflation",
        "year": None,
    },
)

CLIENT_SCENARIO_IDS = ("base_case", "bear", "bull")

_SPEC_BY_ID = {s["id"]: s for s in CLIENT_INPUT_SPECS}


class ClientOverridesPayload(BaseModel):
    """Share-link / custom builder body."""

    scenario: str = "base_case"
    overrides: dict[str, float] = Field(default_factory=dict)


def serialize_input_whitelist() -> list[dict[str, Any]]:
    return [
        {
            "id": s["id"],
            "plain_label": s["plain_label"],
            "min": s["min"],
            "max": s["max"],
            "default": s["default"],
        }
        for s in CLIENT_INPUT_SPECS
    ]


def client_overrides_to_canonical(overrides_by_id: dict[str, float]) -> dict[str, Any]:
    """Map client ids to Assumptions override dict (scalar or year_values)."""
    out: dict[str, Any] = {}
    for key, value in overrides_by_id.items():
        spec = _SPEC_BY_ID.get(key)
        if spec is None:
            msg = f"Unknown client override id: {key!r}"
            raise KeyError(msg)
        label = spec["canonical_label"]
        year = spec.get("year")
        if year is not None:
            out[label] = {int(year): float(value)}
        else:
            out[label] = float(value)
    return out


def validate_client_overrides(overrides_by_id: dict[str, float]) -> list[dict[str, str]]:
    """Hard range validation — returns error messages (empty if ok)."""
    errors: list[dict[str, str]] = []
    for key, value in overrides_by_id.items():
        spec = _SPEC_BY_ID.get(key)
        if spec is None:
            errors.append({"id": key, "message": "Unknown input"})
            continue
        lo, hi = spec["min"], spec["max"]
        if value < lo or value > hi:
            errors.append(
                {
                    "id": key,
                    "message": f"Must be between {lo} and {hi} (got {value})",
                }
            )
    return errors


def encode_share_state(scenario: str, overrides_by_id: dict[str, float]) -> str:
    payload = {"scenario": scenario, "overrides": overrides_by_id}
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_share_state(token: str) -> ClientOverridesPayload:
    pad = "=" * (-len(token) % 4)
    raw = base64.urlsafe_b64decode(token + pad)
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        msg = "Invalid share token"
        raise ValueError(msg)
    scenario = str(data.get("scenario", "base_case"))
    overrides_raw = data.get("overrides") or {}
    if not isinstance(overrides_raw, dict):
        msg = "Invalid overrides in share token"
        raise ValueError(msg)
    overrides = {str(k): float(v) for k, v in overrides_raw.items()}
    errors = validate_client_overrides(overrides)
    if errors:
        msg = "; ".join(e["message"] for e in errors)
        raise ValueError(msg)
    return ClientOverridesPayload(scenario=scenario, overrides=overrides)


def scenario_card_overrides_human(name: str, spec_overrides: dict[str, Any]) -> list[str]:
    """Plain-language diff lines for scenario cards (no canonical labels)."""
    if not spec_overrides:
        return ["Matches Base Case assumptions"]
    lines: list[str] = []
    for inp in CLIENT_INPUT_SPECS:
        label = inp["canonical_label"]
        if label not in spec_overrides:
            continue
        val = spec_overrides[label]
        if isinstance(val, dict) and "year_values" in val:
            yv = val["year_values"]
            if isinstance(yv, dict) and yv:
                val = next(iter(yv.values()))
        lines.append(f"{inp['plain_label']}: {val}")
    if name == "bear" and not lines:
        lines = [
            "Lower TAM inflation",
            "Higher Mars carve-out share",
            "Slower Starship learning",
        ]
    elif name == "bull" and not lines:
        lines = [
            "Higher TAM inflation",
            "Lower Mars carve-out share",
            "Faster Starship learning",
        ]
    return lines[:5]
