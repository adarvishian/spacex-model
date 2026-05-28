import { formatBillions } from "../shared/format";

type ModuleEv = Record<string, { display_name: string; ev_2025_b: number }>;

type Props = {
  moduleEv: ModuleEv;
};

export function SumOfPartsBar({ moduleEv }: Props) {
  const items = Object.entries(moduleEv)
    .map(([, m]) => ({ name: m.display_name, ev: m.ev_2025_b }))
    .sort((a, b) => b.ev - a.ev);
  const max = Math.max(...items.map((i) => Math.abs(i.ev)), 1);

  return (
    <div className="sop-chart" role="img" aria-label="Sum of parts by module">
      {items.map((item) => {
        const widthPct = Math.max(4, (Math.abs(item.ev) / max) * 100);
        return (
          <div key={item.name} className="sop-row">
            <span className="sop-label">{item.name}</span>
            <div className="sop-bar-track">
              <div
                className="sop-bar-fill"
                style={{ width: `${widthPct}%` }}
              />
            </div>
            <span className="sop-value">{formatBillions(item.ev)}</span>
          </div>
        );
      })}
    </div>
  );
}
