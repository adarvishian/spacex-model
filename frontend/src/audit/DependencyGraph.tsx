import {
  Background,
  Controls,
  Handle,
  MarkerType,
  Position,
  ReactFlow,
  type Edge,
  type Node,
  type NodeProps,
} from "@xyflow/react";
import { useQuery } from "@tanstack/react-query";
import { useCallback, useMemo, useState } from "react";
import { fetchLineageGraph } from "../api";
import type { LineageGraphNode } from "../shared/types";
import "@xyflow/react/dist/style.css";

type AuditNodeData = LineageGraphNode["data"] & { expanded?: boolean };

type Props = {
  lineageKey: string | null;
  runId: string | null;
  year?: number;
  sheet?: string;
  row?: number;
  scenario?: string;
  onNavigateCell?: (opts: { sheetSlug: string; rowId?: string; year?: number; lineageKey: string }) => void;
};

function AuditCellNode({ data }: NodeProps<Node<AuditNodeData>>) {
  return (
    <div className={`dep-node ${data.active ? "active" : ""}`}>
      <Handle type="target" position={Position.Left} />
      <div className="dep-node-label">{data.label}</div>
      <div className="dep-node-sub">{data.subtitle}</div>
      <Handle type="source" position={Position.Right} />
    </div>
  );
}

const nodeTypes = { auditCell: AuditCellNode };

function slugFromSheet(sheet?: string): string {
  if (!sheet) return "starlink";
  return sheet.toLowerCase().replace(/&/g, "").replace(/\s+/g, "_").replace(/_+/g, "_");
}

export function DependencyGraph({
  lineageKey,
  runId,
  year,
  sheet,
  row,
  scenario,
  onNavigateCell,
}: Props) {
  const [depth, setDepth] = useState(2);

  const graphQ = useQuery({
    queryKey: ["lineage-graph", runId, lineageKey, depth, year, sheet, row, scenario],
    queryFn: () =>
      fetchLineageGraph(lineageKey!, {
        runId: runId!,
        depth,
        year,
        sheet,
        row,
        scenario,
      }),
    enabled: Boolean(runId && lineageKey),
  });

  const onNodeClick = useCallback(
    (_: React.MouseEvent, node: Node<AuditNodeData>) => {
      const d = node.data;
      if (!d.key || !onNavigateCell) return;
      onNavigateCell({
        sheetSlug: slugFromSheet(d.sheet),
        rowId: d.row,
        year: d.year,
        lineageKey: d.key,
      });
    },
    [onNavigateCell],
  );

  const nodes = useMemo(
    () => (graphQ.data?.nodes ?? []) as Node<AuditNodeData>[],
    [graphQ.data?.nodes],
  );
  const edges = useMemo(
    () =>
      (graphQ.data?.edges ?? []).map(
        (edge): Edge => ({
          id: edge.id,
          source: edge.source,
          target: edge.target,
          type: edge.type ?? "smoothstep",
          style: { stroke: "var(--muted)", strokeWidth: 1.5, ...edge.style },
          markerEnd: { type: MarkerType.ArrowClosed, color: "var(--muted)" },
        }),
      ),
    [graphQ.data?.edges],
  );

  const hasUpstream = edges.length > 0;

  if (!lineageKey || !runId) {
    return null;
  }

  return (
    <div className="depgraph-wrap" aria-label="Dependency graph" tabIndex={0}>
      <div className="depgraph-header">
        <p className="panel-title">Dependency graph (depth {depth})</p>
        {hasUpstream && (
          <div className="depgraph-controls">
            <button
              type="button"
              className="dep-depth-btn"
              disabled={depth <= 1}
              aria-label="Decrease graph depth"
              onClick={() => setDepth((d) => Math.max(1, d - 1))}
            >
              −
            </button>
            <button
              type="button"
              className="dep-depth-btn"
              disabled={depth >= 4}
              aria-label="Increase graph depth"
              onClick={() => setDepth((d) => Math.min(4, d + 1))}
            >
              Expand +
            </button>
          </div>
        )}
      </div>
      {graphQ.isLoading && <p className="muted">Loading graph…</p>}
      {graphQ.error && <p className="audit-alert error">{String(graphQ.error)}</p>}
      {!graphQ.isLoading && !graphQ.error && !hasUpstream && (
        <p className="depgraph-empty muted" data-testid="depgraph-empty">
          No upstream dependencies traced for this cell.
        </p>
      )}
      {hasUpstream && (
        <div className="depgraph-canvas">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodeClick={onNodeClick}
            fitView
            fitViewOptions={{ padding: 0.2 }}
            defaultEdgeOptions={{
              style: { stroke: "var(--muted)", strokeWidth: 1.5 },
              markerEnd: { type: MarkerType.ArrowClosed, color: "var(--muted)" },
            }}
            nodesDraggable={false}
            nodesConnectable={false}
            elementsSelectable
            proOptions={{ hideAttribution: true }}
          >
            <Background gap={16} color="var(--border)" />
            <Controls showInteractive={false} />
          </ReactFlow>
        </div>
      )}
    </div>
  );
}
