/**
 * Prebuild gate — verify committed precache JSON exists (no Python on Vercel).
 * Freshness is enforced in CI via scripts/check_precache_artifacts.py.
 */
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const dataDir = join(root, "public", "data");
const scenarios = ["base_case", "bear", "bull", "mars_share"];

const missing = [];
for (const scenario of scenarios) {
  for (const kind of ["run", "mc"]) {
    const path = join(dataDir, `${scenario}_${kind}.json`);
    if (!existsSync(path)) missing.push(path);
  }
}

if (missing.length) {
  console.error("Missing precache artifacts:");
  for (const path of missing) console.error(`  ${path}`);
  console.error("Run ./scripts/regenerate_precache.sh from repo root.");
  process.exit(1);
}

console.log(`Precache artifacts present (${scenarios.length} scenarios)`);
