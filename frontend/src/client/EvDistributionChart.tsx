import type { McHistogram, McMetricSummary } from "../shared/types";
import { formatBillions } from "../shared/format";

type Props = {
  histogram: McHistogram;
  metrics: McMetricSummary;
};

export function EvDistributionChart({ histogram, metrics }: Props) {
  const { bin_edges, counts } = histogram;
  const maxCount = Math.max(...counts, 1);
  const lo = bin_edges[0] ?? metrics.p5;
  const hi = bin_edges[bin_edges.length - 1] ?? metrics.p95;
  const span = hi - lo || 1;

  const markerX = (v: number) => `${Math.min(100, Math.max(0, ((v - lo) / span) * 100))}%`;

  return (
    <div className="mc-ev-chart" data-testid="mc-ev-distribution">
      <div className="mc-ev-histogram" aria-hidden>
        {counts.map((count, i) => {
          const edgeLo = bin_edges[i] ?? lo;
          const edgeHi = bin_edges[i + 1] ?? hi;
          const mid = (edgeLo + edgeHi) / 2;
          const height = (count / maxCount) * 100;
          return (
            <div
              key={i}
              className="mc-ev-bar"
              style={{ height: `${height}%` }}
              title={`${formatBillions(mid)}: ${count} trials`}
            />
          );
        })}
        {metrics.base_case != null && (
          <div
            className="mc-ev-marker base-case"
            style={{ left: markerX(metrics.base_case) }}
            title={`Base case ${formatBillions(metrics.base_case)}`}
          />
        )}
        <div
          className="mc-ev-marker p5"
          style={{ left: markerX(metrics.p5) }}
          title={`P5 ${formatBillions(metrics.p5)}`}
        />
        <div
          className="mc-ev-marker p50"
          style={{ left: markerX(metrics.p50) }}
          title={`P50 ${formatBillions(metrics.p50)}`}
        />
        <div
          className="mc-ev-marker p95"
          style={{ left: markerX(metrics.p95) }}
          title={`P95 ${formatBillions(metrics.p95)}`}
        />
      </div>
      <div className="mc-ev-percentiles" data-testid="mc-ev-percentiles">
        <div className="mc-percentile-callout">
          <span className="mc-percentile-label">P5</span>
          <span className="mc-percentile-value" data-testid="mc-p5">
            {formatBillions(metrics.p5)}
          </span>
        </div>
        <div className="mc-percentile-callout primary">
          <span className="mc-percentile-label">P50</span>
          <span className="mc-percentile-value" data-testid="mc-p50">
            {formatBillions(metrics.p50)}
          </span>
        </div>
        <div className="mc-percentile-callout">
          <span className="mc-percentile-label">P95</span>
          <span className="mc-percentile-value" data-testid="mc-p95">
            {formatBillions(metrics.p95)}
          </span>
        </div>
        {metrics.base_case != null && (
          <div className="mc-percentile-callout base">
            <span className="mc-percentile-label">Base</span>
            <span className="mc-percentile-value" data-testid="mc-base-case">
              {formatBillions(metrics.base_case)}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
