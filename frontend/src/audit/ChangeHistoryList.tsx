import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { fetchLineageHistory } from "../api";
import type { ChangeHistoryEntry } from "../shared/types";
import { formatGridNumber } from "../shared/format";

type Props = {
  lineageKey: string | null;
};

const KIND_LABELS: Record<ChangeHistoryEntry["change_kind"], string> = {
  formula: "FORMULA",
  anchor: "ANCHOR",
  input: "INPUT",
  initial: "INITIAL",
};

function HistoryRow({ entry }: { entry: ChangeHistoryEntry }) {
  const effect = entry.effect_on_cell;
  const delta = effect?.delta;
  const deltaClass =
    delta != null && delta > 0 ? "delta-pos" : delta != null && delta < 0 ? "delta-neg" : "";

  return (
    <div className="history-row">
      <span className="history-date">{entry.date}</span>
      <span className="history-kind">{KIND_LABELS[entry.change_kind] ?? entry.change_kind}</span>
      {entry.summary && <div className="history-summary">{entry.summary}</div>}
      <div className="history-meta">
        {effect && effect.before != null && effect.after != null && (
          <>
            Effect: {formatGridNumber(effect.before, "dollars_mm")} →{" "}
            <strong>{formatGridNumber(effect.after, "dollars_mm")}</strong>
            {delta != null && (
              <span className={deltaClass}>
                {" "}
                ({delta >= 0 ? "+" : ""}
                {formatGridNumber(delta, "dollars_mm")} mm)
              </span>
            )}
            {" · "}
          </>
        )}
        <a
          href={`https://github.com/search?q=${entry.commit_sha}&type=commits`}
          target="_blank"
          rel="noreferrer"
        >
          commit {entry.commit_sha}
        </a>
        {entry.dev_log_anchor && (
          <>
            {" · "}
            <a href={`/${entry.dev_log_anchor}`} target="_blank" rel="noreferrer">
              DEV_LOG ↗
            </a>
          </>
        )}
      </div>
      <div className="history-title">{entry.title}</div>
    </div>
  );
}

export function ChangeHistoryList({ lineageKey }: Props) {
  const [showAll, setShowAll] = useState(false);

  const historyQ = useQuery({
    queryKey: ["lineage-history", lineageKey],
    queryFn: () => fetchLineageHistory(lineageKey!),
    enabled: Boolean(lineageKey),
  });

  const entries = historyQ.data?.entries ?? [];
  const visible = showAll ? entries : entries.slice(0, 3);

  if (!lineageKey) {
    return (
      <section className="change-history empty" aria-label="Change history">
        <p className="panel-hint">Select a cell to view change history.</p>
      </section>
    );
  }

  return (
    <section className="change-history" aria-label="Change history">
      <p className="group-title">Change history</p>
      {historyQ.isLoading && <p className="muted">Loading history…</p>}
      {historyQ.error && <p className="audit-alert error">{String(historyQ.error)}</p>}
      {visible.map((entry, i) => (
        <HistoryRow key={`${entry.date}-${entry.commit_sha}-${i}`} entry={entry} />
      ))}
      {entries.length === 0 && !historyQ.isLoading && (
        <p className="muted">No change history recorded for this cell.</p>
      )}
      {entries.length > 3 && !showAll && (
        <div className="history-show-all">
          <button type="button" className="link-btn" onClick={() => setShowAll(true)}>
            Show all {entries.length} entries →
          </button>
        </div>
      )}
    </section>
  );
}
