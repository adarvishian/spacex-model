import type { ClientRunSummary } from "../shared/types";
import { formatBillions } from "../shared/format";
import { FcfSparkline } from "./FcfSparkline";
import { SumOfPartsBar } from "./SumOfPartsBar";

type Props = {
  run: ClientRunSummary | null;
  loading?: boolean;
};

export function HeadlinePanel({ run, loading }: Props) {
  const ev = run?.valuation.group_ev_2025_b;
  const fcf = run?.group?.group_fcf;

  return (
    <section className="client-headline panel" aria-label="Headline outputs">
      <h2>Headline</h2>
      {loading && <p className="muted">Running scenario…</p>}
      {!loading && run && (
        <>
          <div className="client-ev-big">
            <span className="client-ev-label">Group Equity Value (2025)</span>
            <span className="client-ev-value">{formatBillions(ev)}</span>
            <span className="client-ev-caption">
              Implied enterprise value from the active scenario run
            </span>
          </div>
          <div className="client-headline-charts">
            <div className="client-chart-block">
              <h3>Sum of parts</h3>
              <SumOfPartsBar moduleEv={run.module_ev} />
            </div>
            <div className="client-chart-block">
              <h3>Group FCF profile</h3>
              {fcf && <FcfSparkline years={fcf.years} values={fcf.values} />}
            </div>
          </div>
        </>
      )}
    </section>
  );
}
