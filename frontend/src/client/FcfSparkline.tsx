type Props = {
  years: number[];
  values: number[];
};

export function FcfSparkline({ years, values }: Props) {
  if (!values.length) return null;
  const w = 320;
  const h = 56;
  const pad = 4;
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max - min || 1;
  const pts = values
    .map((v, i) => {
      const x = pad + (i / Math.max(values.length - 1, 1)) * (w - pad * 2);
      const y = h - pad - ((v - min) / span) * (h - pad * 2);
      return `${x},${y}`;
    })
    .join(" ");

  const lastYear = years[years.length - 1];
  const firstYear = years[0];

  return (
    <div className="fcf-sparkline">
      <svg viewBox={`0 0 ${w} ${h}`} width="100%" height={h} aria-hidden>
        <polyline
          fill="none"
          stroke="var(--accent)"
          strokeWidth="2"
          points={pts}
        />
      </svg>
      <div className="fcf-sparkline-axis">
        <span>{firstYear}</span>
        <span>{lastYear}</span>
      </div>
    </div>
  );
}
