# SpaceX Modeler — Frontend

React 18 + TypeScript + Vite UI for audit-grade model exploration and client-facing scenario views.

## Modes

| Route | App | Purpose |
|---|---|---|
| `/audit/:sheetSlug` | `src/app/AuditApp.tsx` | Grid, lineage, derivation, MC audit — for model owners |
| `/client/*` | `src/app/ClientApp.tsx` | Scenario cards, headline EV, FCF fan, MC panel — for end users |

Mode routing lives in `src/app/ModeRouter.tsx`. Shared API client: `src/shared/api.ts`.

## Precache strategy

Production and Vercel builds serve **committed JSON artifacts** from `public/data/` instead of running the Python pipeline at page load:

- `base_case_run.json` — deterministic base-case audit grids + run metadata
- `base_case_mc.json` — 2,000-trial MC aggregation

Regenerate from repo root:

```bash
./scripts/regenerate_precache.sh
git add frontend/public/data/
```

The `prebuild` script in `package.json` also runs precompute scripts before `vite build`. Client mode reads MC/headline data via `src/shared/base-case-artifact.ts` and `src/shared/base-case-mc-artifact.ts`.

When `VITE_API_BASE` points at a live API, audit mode can fetch fresh runs; client mode still prefers precache for latency.

## Local development

```bash
npm install
npm run dev          # http://localhost:5173 — proxies /api → :8000
```

Start the API separately (`spacex-api` from repo root). Optional: `VITE_API_KEY` if the backend requires auth.

## Tests

| Command | Scope |
|---|---|
| `npm test` | Vitest unit tests — `src/shared/*.test.ts`, `src/audit/grid-navigation.test.ts` |
| `npm run test:e2e` | Playwright — audit + client flows against **mocked API** |

E2e mocking is in `e2e/mock-api.ts`: it intercepts `/api/*` and serves patched payloads from `public/data/base_case_run.json` plus a fixed MC aggregation fixture. No backend required in CI.

Playwright config: `playwright.config.ts` (Chromium, accessibility via `@axe-core/playwright`).

## Build output

`npm run build` emits to `../static/ui/` (served by the FastAPI app and Vercel). Bundle budget check: `npm run check:bundle`.
