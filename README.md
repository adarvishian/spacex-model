# Mach33 SpaceX Valuation Model (Python Port)

Python port of the Mach33 SpaceX Valuation Model. See `PRD.md` and `context.md` for authority and scope.

## Agent / contributor onboarding

1. **`context.md`** — architecture locks and reconciliation methodology (read first).
2. **`role.md`** — modeling persona and deliverable standards.
3. **`docs/DEV_LOG.md`** — what changed recently and how to run verification (read before editing assumptions or anchors).

Disclosed inputs from the SpaceX S-1 (filed 2026-05-20) are applied automatically after workbook ingest via `apply_s1_adherence_overrides()`; see `scenarios/s1_adherence.yaml` and the dev log entry **2026-05-28 — S-1 adherence audit §7.2 P0**.

## Phase A (Foundation)

- Canonical label registry extracted from V2.16
- Assumptions ingest (openpyxl formula + value pass)
- Zero-stub pipeline and `cli/run_model.py --base-case`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Run Base Case (zero-stub)

```bash
python -m spacex_model.cli.run_model --base-case
```

Default workbook path: `Pre Existing Model Package/01_Current_State/SpaceX Model V2.16.xlsx`

Override with `--workbook PATH` or `SPACEX_MODEL_WORKBOOK`.

## Phase G (FastAPI + Web UI)

### API server

```bash
pip install -e ".[service]"
spacex-api --host 127.0.0.1 --port 8000
```

Endpoints: `/health`, `/scenarios`, `/runs/deterministic`, `/runs/mc`, `/lineage/{key}`.

Optional env: `SPACEX_MODEL_REDIS_URL` (result cache), `SPACEX_MODEL_API_KEY` (auth).

### Web UI

```bash
cd frontend && npm install && npm run dev
```

Open http://localhost:5173 — proxies API requests to port 8000.


```bash
python scripts/extract_canonical_labels.py
```
