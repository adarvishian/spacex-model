import { useState } from "react";
import { shareUrlFromState } from "../shared/share-link";

type Props = {
  scenario: string;
  overrides: Record<string, number>;
  disabled?: boolean;
};

export function ShareLinkButton({ scenario, overrides, disabled }: Props) {
  const [copied, setCopied] = useState(false);

  const copy = async () => {
    const url = shareUrlFromState(window.location.origin, scenario, overrides);
    await navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  const preview = shareUrlFromState(window.location.origin, scenario, overrides);

  return (
    <div className="client-share panel">
      <h2>Share this scenario</h2>
      <p className="client-share-url" title={preview}>
        {preview}
      </p>
      <button
        type="button"
        className="btn-secondary"
        onClick={() => void copy()}
        disabled={disabled}
      >
        {copied ? "Copied" : "Copy share link"}
      </button>
    </div>
  );
}
