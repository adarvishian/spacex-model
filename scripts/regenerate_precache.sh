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

echo "==> Stamping git_sha for commit"
uv run python scripts/stamp_precache_git_sha.py

echo "==> Done. Commit when ready (stamp must match final commit — amend after commit):"
echo "    git add frontend/public/data/*.json"
echo "    git commit -m 'chore: regenerate precache artifacts'"
echo "    uv run python scripts/stamp_precache_git_sha.py"
echo "    git add frontend/public/data/*.json && git commit --amend --no-edit"
