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
          style: { stroke: "#8a93a8", strokeWidth: 1.5, ...edge.style },
          markerEnd: { type: MarkerType.ArrowClosed, color: "#8a93a8" },
        }),
      ),
    [graphQ.data?.edges],
  );

  if (!lineageKey || !runId) {
    return null;
  }

  return (
    <div className="depgraph-wrap" aria-label="Dependency graph">
      <div className="depgraph-header">
        <p className="panel-title">Dependency graph (depth {depth})</p>
        <div className="depgraph-controls">
          <button
            type="button"
            className="dep-depth-btn"
            disabled={depth <= 1}
            onClick={() => setDepth((d) => Math.max(1, d - 1))}
          >
            −
          </button>
          <button
            type="button"
            className="dep-depth-btn"
            disabled={depth >= 4}
            onClick={() => setDepth((d) => Math.min(4, d + 1))}
          >
            Expand +
          </button>
        </div>
      </div>
      {graphQ.isLoading && <p className="muted">Loading graph…</p>}
      {graphQ.error && <p className="audit-alert error">{String(graphQ.error)}</p>}
      {nodes.length > 0 && (
        <div className="depgraph-canvas">
          <ReactFlow
            nodes={nodes}
            edges={edges}
            nodeTypes={nodeTypes}
            onNodeClick={onNodeClick}
            fitView
            fitViewOptions={{ padding: 0.2 }}
            defaultEdgeOptions={{
              style: { stroke: "#8a93a8", strokeWidth: 1.5 },
              markerEnd: { type: MarkerType.ArrowClosed, color: "#8a93a8" },
            }}
            nodesDraggable={false}
            nodesConnectable={false}
            elementsSelectable
            proOptions={{ hideAttribution: true }}
          >
            <Background gap={16} color="#2a3544" />
            <Controls showInteractive={false} />
          </ReactFlow>
        </div>
      )}
    </div>
  );
}
