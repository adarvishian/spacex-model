import { afterEach, describe, expect, it, vi } from "vitest";
import {
  clientWorkbookLabel,
  formatDataAsOf,
  freshnessLabel,
  provenanceLabel,
  resolveArtifactFreshness,
} from "./provenance";

describe("provenance helpers", () => {
  it("formats workbook mtime as locale date", () => {
    const label = formatDataAsOf(1_718_000_000);
    expect(label).toMatch(/2024/);
  });

  it("strips version numbers for client workbook label", () => {
    expect(clientWorkbookLabel("SpaceX V4.131.xlsx")).toBe("valuation model");
  });

  it("maps run provenance to display labels", () => {
    expect(provenanceLabel("precomputed")).toBe("precomputed");
    expect(provenanceLabel("fresh")).toBe("live");
  });

  afterEach(() => {
    vi.unstubAllEnvs();
  });

  it("resolves artifact freshness from deploy sha", () => {
    vi.stubEnv("VITE_DEPLOY_SHA", "abc1234");
    expect(resolveArtifactFreshness("abc1234", null)).toBe("matched");
    expect(resolveArtifactFreshness("deadbeef", null)).toBe("stale");
  });

  it("labels freshness states", () => {
    expect(freshnessLabel("unknown")).toBe("freshness unknown");
    expect(freshnessLabel("stale")).toBe("stale");
  });
});
