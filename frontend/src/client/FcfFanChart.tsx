import type { McFcfFan } from "../shared/types";
import { formatMm } from "../shared/format";

type Props = {
  fan: McFcfFan;
};

const W = 480;
const H = 120;
const PAD = { top: 8, right: 8, bottom: 20, left: 8 };

function bandPath(
  years: number[],
  upper: number[],
  lower: number[],
  min: number,
  span: number,
): string {
  const n = years.length;
  if (n === 0) return "";
  const xAt = (i: number) => PAD.left + (i / Math.max(n - 1, 1)) * (W - PAD.left - PAD.right);
  const yAt = (v: number) => H - PAD.bottom - ((v - min) / span) * (H - PAD.top - PAD.bottom);

  const upperPts = upper.map((v, i) => `${xAt(i)},${yAt(v)}`).join(" ");
  const lowerPts = [...lower].reverse().map((v, i) => {
    const idx = n - 1 - i;
    return `${xAt(idx)},${yAt(v)}`;
  }).join(" ");
  return `M ${upperPts} L ${lowerPts} Z`;
}

function linePath(values: number[], years: number[], min: number, span: number): string {
  return values
    .map((v, i) => {
      const x = PAD.left + (i / Math.max(years.length - 1, 1)) * (W - PAD.left - PAD.right);
      const y = H - PAD.bottom - ((v - min) / span) * (H - PAD.top - PAD.bottom);
      return `${i === 0 ? "M" : "L"} ${x},${y}`;
    })
    .join(" ");
}

export function FcfFanChart({ fan }: Props) {
  const { years, p5, p25, p50, p75, p95, base_case } = fan;
  if (!years.length) return null;

  const allVals = [...p5, ...p95, ...base_case.filter((v): v is number => v != null)];
  const min = Math.min(...allVals);
  const max = Math.max(...allVals);
  const span = max - min || 1;

  const tickYears = years.filter((y) => y % 5 === 0 || y === years[0]);

  return (
    <div className="mc-fcf-fan" data-testid="mc-fcf-fan">
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height={H} aria-label="Group FCF percentile fan">
        <path d={bandPath(years, p95, p5, min, span)} className="mc-fan-outer" />
        <path d={bandPath(years, p75, p25, min, span)} className="mc-fan-inner" />
        <path d={linePath(p50, years, min, span)} className="mc-fan-median" fill="none" />
        {base_case.some((v) => v != null) && (
          <path
            d={linePath(
              base_case.map((v, i) => v ?? p50[i] ?? 0),
              years,
              min,
              span,
            )}
            className="mc-fan-base"
            fill="none"
          />
        )}
      </svg>
      <div className="mc-fcf-fan-axis">
        {tickYears.map((y) => (
          <span key={y}>{y}</span>
        ))}
      </div>
      <div className="mc-fcf-fan-legend">
        <span className="mc-fan-legend-outer">P5–P95</span>
        <span className="mc-fan-legend-inner">P25–P75</span>
        <span className="mc-fan-legend-median">P50</span>
        <span className="mc-fan-legend-base">Base case</span>
      </div>
      <p className="mc-fcf-fan-caption muted">
        Group FCF ($mm) — shaded bands show trial uncertainty by year; median line is P50.
        {p50.length > 0 && (
          <> 2030 P50: {formatMm(p50[years.indexOf(2030)] ?? p50[Math.floor(p50.length / 2)])}.</>
        )}
      </p>
    </div>
  );
}
