# Mach33 SpaceX Valuation Model (Python Port)

Python port of the Mach33 SpaceX Valuation Model. Workbook baseline: **SpaceX V4.113.xlsx**.

## Agent / contributor onboarding

1. **`context.md`** — architecture locks and reconciliation methodology (read first).
2. **`role.md`** — modeling persona and deliverable standards.
3. **`docs/DEV_LOG.md`** — what changed recently and how to run verification (read before editing assumptions or anchors).

Disclosed inputs from the SpaceX S-1 (filed 2026-05-20) are applied automatically after workbook ingest via `apply_s1_adherence_overrides()`; see `scenarios/s1_adherence.yaml` and the dev log entry **2026-05-28 — S-1 adherence audit §7.2 P0**.

## Documentation index

| Topic | Authoritative doc |
|---|---|
| Architecture locks, reconciliation methodology | `context.md` (V4.113 deferral header → PRD + `constants.py`) |
| Active product requirements (V4.113 re-base) | `PRD_V4.113_Unified_Allocation_2026-06-04.md` |
| Modeling persona & deliverable standards | `role.md` |
| Recent changes, verification commands, Block B status | `docs/DEV_LOG.md` |
| Reconciliation pass/fail table (generated) | `docs/reconciliation_report.md` |
| Excel→Python label mapping (drift-checked in CI) | `docs/model_translation_log.csv` |
| Frontend modes, precache, e2e | [`frontend/README.md`](frontend/README.md) |
| Frontend UX spec | `docs/FRONTEND_UX_PRD_2026-06-05.md` |
| Lineage / MC product spec | `docs/PRD_Lineage_Trust_and_Monte_Carlo_2026-06-05.md` |
| Superseded V2.16 PRD & planning docs | `docs/archive/` (historical only) |
| Legacy sprint package (Mach33 workbook era) | `Pre Existing Model Package/` |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Locked installs (CI/Vercel): `uv sync` from `uv.lock`.

## Run Base Case

```bash
python -m spacex_model.cli.run_model --base-case
```

Default workbook: `SpaceX V4.113.xlsx` (override with `--workbook PATH` or `SPACEX_MODEL_WORKBOOK`).

## API + Web UI

### API server

```bash
pip install -e ".[service]"
spacex-api --host 127.0.0.1 --port 8000
```

Endpoints: `/api/health`, `/api/scenarios`, `/api/runs/deterministic`, `/api/runs/mc`, `/api/lineage/{key}`.

Optional env: `SPACEX_MODEL_REDIS_URL` (result cache), `SPACEX_MODEL_API_KEY` (auth).

### Web UI

See [`frontend/README.md`](frontend/README.md). Quick start:

```bash
cd frontend && npm install && npm run dev
```

Open http://localhost:5173 — proxies API requests to port 8000.

## Maintenance

```bash
python scripts/extract_canonical_labels.py   # regenerate label registry
./scripts/regenerate_precache.sh             # refresh committed frontend JSON artifacts
```
