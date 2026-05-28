import type { ClientRunSummary } from "../shared/types";
import { formatBillions, formatPct } from "../shared/format";

const YEAR_2050 = 2050;
const YEAR_2030 = 2030;

type Props = {
  run: ClientRunSummary | null;
};

export function ModuleSummaryGrid({ run }: Props) {
  if (!run?.modules) return null;

  return (
    <section className="client-modules panel" aria-label="Per-module summary">
      <h2>Per-module summary</h2>
      <div className="client-module-cards">
        {Object.entries(run.modules).map(([key, mod]) => {
          const ev = run.module_ev[key]?.ev_2025_b;
          const revSeries = mod.total_revenue;
          const irrSeries = mod.blended_irr;
          const rev2050 =
            revSeries.values[revSeries.values.length - 1] ??
            revSeries.values[revSeries.values.length - 26];
          const irr2030Idx = irrSeries.values.length >= 6 ? 5 : irrSeries.values.length - 1;
          const irr2030 = irrSeries.values[irr2030Idx];

          return (
            <div key={key} className="client-module-card">
              <h3>{mod.display_name}</h3>
              <dl>
                <div>
                  <dt>Module EV (2025)</dt>
                  <dd>{formatBillions(ev)}</dd>
                </div>
                <div>
                  <dt>Total revenue ({YEAR_2050})</dt>
                  <dd>{formatBillions(rev2050 / 1000)}</dd>
                </div>
                <div>
                  <dt>Blended IRR ({YEAR_2030})</dt>
                  <dd>{formatPct(irr2030)}</dd>
                </div>
              </dl>
            </div>
          );
        })}
      </div>
    </section>
  );
}
