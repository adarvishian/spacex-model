/** URL-safe share state for custom scenarios (FRONTEND_PRD §7.5). */

export function encodeShareState(scenario: string, overrides: Record<string, number>): string {
  const raw = JSON.stringify({ scenario, overrides });
  const bytes = new TextEncoder().encode(raw);
  let binary = "";
  bytes.forEach((b) => {
    binary += String.fromCharCode(b);
  });
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

export function decodeShareState(token: string): {
  scenario: string;
  overrides: Record<string, number>;
} {
  const pad = "=".repeat((4 - (token.length % 4)) % 4);
  const b64 = token.replace(/-/g, "+").replace(/_/g, "/") + pad;
  const json = atob(b64);
  const data = JSON.parse(json) as { scenario?: string; overrides?: Record<string, number> };
  return {
    scenario: data.scenario ?? "base_case",
    overrides: data.overrides ?? {},
  };
}

export function shareUrlFromState(
  origin: string,
  scenario: string,
  overrides: Record<string, number>,
): string {
  const token = encodeShareState(scenario, overrides);
  const url = new URL("/client", origin);
  url.searchParams.set("s", token);
  return url.toString();
}
