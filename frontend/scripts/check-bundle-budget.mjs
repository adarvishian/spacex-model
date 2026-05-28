#!/usr/bin/env node
/**
 * FRONTEND_PRD §8.3 — performance regression budget in CI.
 * - Client route: synchronously loaded JS gzip ≤ 400 KB (initial /client visit).
 * - Full audit app: all JS chunks gzip ≤ 520 KB (ag-grid + react-flow).
 */
import { gzipSync } from "node:zlib";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const assetsDir = join(__dirname, "../../static/ui/assets");

const CLIENT_INITIAL_MAX = Number(process.env.FRONTEND_CLIENT_GZIP_MAX ?? 400 * 1024);
const AUDIT_TOTAL_JS_MAX = Number(process.env.FRONTEND_AUDIT_JS_GZIP_MAX ?? 520 * 1024);

function gzipSize(filePath) {
  return gzipSync(readFileSync(filePath)).length;
}

const files = readdirSync(assetsDir).filter((f) => f.endsWith(".js"));

let clientInitial = 0;
let auditJsTotal = 0;

for (const f of files) {
  const path = join(assetsDir, f);
  if (!statSync(path).isFile()) continue;
  const size = gzipSize(path);
  auditJsTotal += size;

  const isClientChunk =
    f.includes("ClientApp") ||
    f.includes("vendor-react") ||
    f.includes("vendor-query") ||
    f.startsWith("index-");
  if (isClientChunk) clientInitial += size;

  console.log(`  ${f}: ${(size / 1024).toFixed(1)} KB gzip`);
}

console.log(
  `Client initial JS gzip: ${(clientInitial / 1024).toFixed(1)} KB (budget ${(CLIENT_INITIAL_MAX / 1024).toFixed(0)} KB)`,
);
console.log(
  `All JS gzip: ${(auditJsTotal / 1024).toFixed(1)} KB (budget ${(AUDIT_TOTAL_JS_MAX / 1024).toFixed(0)} KB)`,
);

let failed = false;
if (clientInitial > CLIENT_INITIAL_MAX) {
  console.error("Client initial bundle budget exceeded.");
  failed = true;
}
if (auditJsTotal > AUDIT_TOTAL_JS_MAX) {
  console.error("Total JS bundle budget exceeded.");
  failed = true;
}
process.exit(failed ? 1 : 0);
