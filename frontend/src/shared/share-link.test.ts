import { describe, expect, it } from "vitest";
import { decodeShareState, encodeShareState, shareUrlFromState } from "./share-link";

describe("share link round-trip", () => {
  it("encodes and decodes scenario overrides", () => {
    const overrides = { mars_pct: 0.07 };
    const token = encodeShareState("base_case", overrides);
    expect(decodeShareState(token)).toEqual({ scenario: "base_case", overrides });
  });

  it("builds a client URL with share token", () => {
    const url = shareUrlFromState("https://example.com", "bull", { mars_pct: 0.1 });
    expect(url).toMatch(/^https:\/\/example\.com\/client\?s=/);
    const token = new URL(url).searchParams.get("s");
    expect(token).toBeTruthy();
    expect(decodeShareState(token!)).toEqual({
      scenario: "bull",
      overrides: { mars_pct: 0.1 },
    });
  });
});
