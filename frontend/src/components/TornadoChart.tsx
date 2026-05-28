import { TornadoBar } from "../api";

type Props = {
  bars: TornadoBar[];
};

export function TornadoChart({ bars }: Props) {
  const maxDelta = Math.max(...bars.map((b) => b.delta), 1);

  return (
    <div className="tornado-list">
      {bars.map((bar) => {
        const span = bar.high_ev - bar.low_ev || 1;
        const lowPct = ((bar.base_ev - bar.low_ev) / span) * 100;
        const width = (bar.delta / maxDelta) * 100;
        return (
          <div key={bar.label} className="tornado-row">
            <span title={bar.label}>
              {bar.label.length > 22 ? `${bar.label.slice(0, 20)}…` : bar.label}
            </span>
            <div className="tornado-bar-wrap">
              <div
                className="tornado-bar"
                style={{
                  left: `${Math.max(0, 50 - lowPct * (width / 100))}%`,
                  width: `${Math.min(100, width)}%`,
                }}
              />
            </div>
            <span className="num">${bar.delta.toFixed(1)}B</span>
          </div>
        );
      })}
    </div>
  );
}
