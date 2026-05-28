import type { LifecycleStage } from "../shared/types";

export type SheetGraphNode = {
  slug: string;
  label: string;
  group: "inputs" | "allocation" | "modules" | "cross" | "outputs";
  lifecycle: LifecycleStage;
};

export const SHEET_GRAPH: SheetGraphNode[] = [
  { slug: "assumptions", label: "Assumptions", group: "inputs", lifecycle: "input" },
  { slug: "allocator", label: "Allocator", group: "allocation", lifecycle: "allocation" },
  { slug: "launch_capacity", label: "Launch Capacity", group: "allocation", lifecycle: "allocation" },
  { slug: "customer_launch", label: "Customer Launch", group: "modules", lifecycle: "output" },
  { slug: "starlink", label: "Starlink", group: "modules", lifecycle: "output" },
  { slug: "starlink_capacity", label: "Starlink Capacity", group: "modules", lifecycle: "output" },
  { slug: "odc", label: "ODC", group: "modules", lifecycle: "output" },
  { slug: "ai_stack", label: "AI Stack", group: "modules", lifecycle: "output" },
  { slug: "lunar_mars", label: "Lunar Mars", group: "modules", lifecycle: "output" },
  { slug: "opex", label: "OpEx", group: "cross", lifecycle: "pnl" },
  { slug: "capex", label: "CapEx", group: "cross", lifecycle: "pnl" },
  { slug: "group_pnl", label: "Group P&L", group: "cross", lifecycle: "pnl" },
  { slug: "valuation", label: "Valuation", group: "outputs", lifecycle: "valuation" },
  { slug: "demand_curves", label: "Demand Curves", group: "inputs", lifecycle: "demand" },
];

export const LIFECYCLE_STAGES: { id: LifecycleStage; label: string }[] = [
  { id: "input", label: "Input" },
  { id: "demand", label: "Demand" },
  { id: "allocation", label: "Allocation" },
  { id: "output", label: "Output" },
  { id: "pnl", label: "P&L" },
  { id: "conservation", label: "Conservation" },
  { id: "valuation", label: "Valuation" },
];

export const SHEET_GROUPS: { id: SheetGraphNode["group"]; title: string }[] = [
  { id: "inputs", title: "Inputs" },
  { id: "allocation", title: "Allocation" },
  { id: "modules", title: "Modules" },
  { id: "cross", title: "Cross-cutting" },
  { id: "outputs", title: "Outputs" },
];
