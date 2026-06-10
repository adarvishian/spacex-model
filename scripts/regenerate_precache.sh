#!/usr/bin/env bash
# Regenerate committed Vercel precache artifacts (run from repo root).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

export SPACEX_MODEL_FORCE_PRECOMPUTE="${SPACEX_MODEL_FORCE_PRECOMPUTE:-1}"

echo "==> Base-case audit grids"
python scripts/precompute_base_case.py

echo "==> Base-case Monte Carlo (2000 trials — ~15 min optimized)"
python scripts/precompute_base_case_mc.py

echo "==> Done. Commit when ready:"
echo "    git add frontend/public/data/base_case_run.json frontend/public/data/base_case_mc.json"
