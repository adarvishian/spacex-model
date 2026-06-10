#!/usr/bin/env bash
# Regenerate committed precache artifacts for all scenarios (run from repo root).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export SPACEX_MODEL_FORCE_PRECOMPUTE="${SPACEX_MODEL_FORCE_PRECOMPUTE:-1}"
SCENARIOS=(base_case bear bull mars_share)

for scenario in "${SCENARIOS[@]}"; do
  echo "==> ${scenario}: deterministic grids"
  uv run python scripts/precompute_base_case.py "${scenario}"
  echo "==> ${scenario}: Monte Carlo (${SPACEX_MODEL_MC_PRECOMPUTE_TRIALS:-5000} trials)"
  uv run python scripts/precompute_base_case_mc.py "${scenario}"
done

echo "==> Done. Commit when ready:"
echo "    git add frontend/public/data/*.json"
