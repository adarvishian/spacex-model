import type { ClientScenarioCard } from "../shared/types";
import { formatBillions } from "../shared/format";

export type ScenarioChoice = "base_case" | "bear" | "bull" | "custom";

type Props = {
  cards: ClientScenarioCard[];
  selected: ScenarioChoice;
  onSelect: (id: ScenarioChoice) => void;
};

export function ScenarioCards({ cards, selected, onSelect }: Props) {
  const presets = cards.filter((c) => c.id !== "custom");

  return (
    <div className="client-scenario-row" role="radiogroup" aria-label="Scenario">
      {presets.map((card) => (
        <label
          key={card.id}
          className={`client-scenario-card ${selected === card.id ? "selected" : ""}`}
        >
          <input
            type="radio"
            name="scenario"
            value={card.id}
            checked={selected === card.id}
            onChange={() => onSelect(card.id as ScenarioChoice)}
          />
          <span className="client-scenario-name">{card.name}</span>
          <span className="client-scenario-desc">{card.description}</span>
          {card.group_ev_2025_b != null && (
            <span className="client-scenario-ev">
              Group EV: {formatBillions(card.group_ev_2025_b)}
            </span>
          )}
          <ul className="client-scenario-inputs">
            {card.key_inputs.slice(0, 3).map((line) => (
              <li key={line}>{line}</li>
            ))}
          </ul>
        </label>
      ))}
      <label
        className={`client-scenario-card ${selected === "custom" ? "selected" : ""}`}
      >
        <input
          type="radio"
          name="scenario"
          value="custom"
          checked={selected === "custom"}
          onChange={() => onSelect("custom")}
        />
        <span className="client-scenario-name">Custom…</span>
        <span className="client-scenario-desc">
          Adjust vetted inputs and run a bespoke scenario
        </span>
      </label>
    </div>
  );
}
