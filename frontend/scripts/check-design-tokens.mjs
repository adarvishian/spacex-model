#!/usr/bin/env node
/**
 * FRONTEND_UX_PRD §6.4 / A6 — single token source; no duplicate :root; no stray hex in CSS.
 */
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join, dirname, relative } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const srcDir = join(__dirname, "../src");
const tokenFile = join(srcDir, "styles/tokens.css");

const HEX_RE = /#[0-9a-fA-F]{3,8}\b/g;
const ROOT_BLOCK_RE = /^\s*:root\b/m;
const VAR_FALLBACK_RE = /var\(--[a-z0-9-]+,\s*#[0-9a-fA-F]+\)/;

function stripCssComments(content) {
  return content.replace(/\/\*[\s\S]*?\*\//g, "");
}

function walkCss(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (!statSync(path).isFile()) continue;
    if (name.endsWith(".css")) out.push(path);
  }
  return out;
}

let failed = false;

const tokenSrc = stripCssComments(readFileSync(tokenFile, "utf-8"));
if (!ROOT_BLOCK_RE.test(tokenSrc)) {
  console.error("tokens.css must define :root { ... }");
  failed = true;
}

for (const file of walkCss(srcDir)) {
  const rel = relative(srcDir, file);
  const content = stripCssComments(readFileSync(file, "utf-8"));

  if (file !== tokenFile && ROOT_BLOCK_RE.test(content)) {
    console.error(`${rel}: duplicate :root block — use styles/tokens.css only`);
    failed = true;
  }

  if (VAR_FALLBACK_RE.test(content)) {
    console.error(`${rel}: var(--token, #hex) fallback — use var(--token) only`);
    failed = true;
  }

  if (file === tokenFile) continue;

  const hexMatches = content.match(HEX_RE);
  if (hexMatches?.length) {
    console.error(`${rel}: hard-coded hex outside token file: ${hexMatches.join(", ")}`);
    failed = true;
  }
}

if (failed) {
  process.exit(1);
}

console.log("Design token check passed (single :root, no stray hex in component CSS).");
