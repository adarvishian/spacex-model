type Props = {
  nTrials: number;
  nConverged: number;
  convergenceStatus: string;
  baseSeed?: number;
  compact?: boolean;
};

function statusLabel(status: string): string {
  if (status === "converged") return "complete";
  if (status === "partial") return "partial";
  if (status === "failed") return "incomplete";
  return status;
}

export function McTrialSummary({
  nTrials,
  nConverged,
  convergenceStatus,
  baseSeed,
  compact = false,
}: Props) {
  const label = statusLabel(convergenceStatus);
  if (compact) {
    return (
      <span className="mc-trial-summary compact" data-testid="mc-trial-summary">
        {nConverged.toLocaleString()} / {nTrials.toLocaleString()} trials · {label}
      </span>
    );
  }
  return (
    <div className="mc-trial-summary" data-testid="mc-trial-summary">
      <p>
        <strong>Trials:</strong> {nConverged.toLocaleString()} converged of{" "}
        {nTrials.toLocaleString()}
      </p>
      {baseSeed != null && (
        <p>
          <strong>Seed:</strong> {baseSeed}
        </p>
      )}
      <p>
        <strong>Convergence:</strong> {label}
      </p>
    </div>
  );
}
