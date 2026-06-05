/** Headline outputs eligible for Audit Mode MC panel (R-M1.9). */

export type McOutputKind = "group_ev" | "group_fcf" | "module_fcf";

export function resolveMcOutputKind(
  lineageKey: string,
  label: string,
): McOutputKind | null {
  const key = lineageKey.toLowerCase();
  const lbl = label.toLowerCase();

  if (
    key.includes("group_ev") ||
    key.includes("implied_ev") ||
    /^group ev/i.test(label) ||
    lbl.startsWith("group ev:")
  ) {
    return "group_ev";
  }

  if (
    key === "group.group_fcf" ||
    lbl === "group fcf ($mm)" ||
    /^group fcf \(/.test(lbl)
  ) {
    return "group_fcf";
  }

  if (
    /^module\.[^.]+\.module_fcf$/.test(key) ||
    lbl.includes("module fcf ($mm)") ||
    lbl === "module fcf"
  ) {
    return "module_fcf";
  }

  return null;
}

export function isMcHeadlineOutput(lineageKey: string, label: string): boolean {
  return resolveMcOutputKind(lineageKey, label) != null;
}
