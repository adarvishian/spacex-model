import { describe, expect, it } from "vitest";
import { isMcHeadlineOutput, resolveMcOutputKind } from "./mc-headline";

describe("resolveMcOutputKind", () => {
  it("detects group EV headlines", () => {
    expect(resolveMcOutputKind("valuation.group_ev", "Group EV ($B)")).toBe("group_ev");
  });

  it("detects group FCF", () => {
    expect(resolveMcOutputKind("group.group_fcf", "Group FCF ($mm)")).toBe("group_fcf");
  });

  it("detects module FCF", () => {
    expect(resolveMcOutputKind("module.starlink.module_fcf", "Starlink module FCF ($mm)")).toBe(
      "module_fcf",
    );
  });

  it("returns null for non-headline outputs", () => {
    expect(resolveMcOutputKind("starlink.revenue", "Total revenue")).toBeNull();
  });
});

describe("isMcHeadlineOutput", () => {
  it("mirrors resolveMcOutputKind", () => {
    expect(isMcHeadlineOutput("group.group_fcf", "Group FCF ($mm)")).toBe(true);
    expect(isMcHeadlineOutput("starlink.revenue", "Revenue")).toBe(false);
  });
});
