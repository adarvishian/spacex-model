import type { SheetMeta } from "../shared/types";
import { SHEET_GROUPS } from "../data/sheet_graph";

type Props = {
  sheets: SheetMeta[];
  activeSlug: string;
  onSelect: (slug: string) => void;
};

export function SheetTabs({ sheets, activeSlug, onSelect }: Props) {
  return (
    <nav className="sheet-tabs" aria-label="Sheet tabs">
      {SHEET_GROUPS.map((group) => {
        const groupSheets = sheets.filter((s) => {
          if (s.is_run_audit) return false;
          const node = group.id;
          if (node === "inputs") return s.slug === "assumptions" || s.slug === "demand_curves";
          if (node === "allocation")
            return s.slug === "allocator" || s.slug === "launch_capacity";
          if (node === "modules")
            return [
              "customer_launch",
              "starlink",
              "starlink_capacity",
              "odc",
              "ai_stack",
              "lunar_mars",
            ].includes(s.slug);
          if (node === "cross") return ["opex", "capex", "group_pnl"].includes(s.slug);
          return s.slug === "valuation";
        });
        if (groupSheets.length === 0) return null;
        return (
          <div key={group.id}>
            <div className="tabs-group">{group.title}</div>
            {groupSheets.map((sheet) => (
              <button
                key={sheet.slug}
                type="button"
                className={`tab-btn ${activeSlug === sheet.slug ? "active" : ""}`}
                onClick={() => onSelect(sheet.slug)}
                aria-current={activeSlug === sheet.slug ? "page" : undefined}
              >
                {sheet.display_name}
              </button>
            ))}
          </div>
        );
      })}

      {sheets.some((s) => s.is_run_audit) && (
        <div className="tabs-run-audit">
          <div className="tabs-group">Audit</div>
          <button
            type="button"
            className={`tab-btn ${activeSlug === "run_audit" ? "active" : ""}`}
            onClick={() => onSelect("run_audit")}
            aria-current={activeSlug === "run_audit" ? "page" : undefined}
          >
            Run Audit
          </button>
        </div>
      )}
    </nav>
  );
}
