import networkx as nx
from typing import Dict, Any, Optional


class SafePathSelector:
    """
    Selects the safest feasible path using topology-aware reasoning.
    """

    def select(self, graph: nx.Graph, source: str, target: str) -> Optional[Dict[str, Any]]:
        try:
            paths = nx.all_simple_paths(graph, source, target, cutoff=4)
        except (nx.NodeNotFound, nx.NetworkXNoPath):
            return None

        best_path = None
        best_score = float("-inf")

        for path in paths:
            score = 0.0

            for u, v in zip(path[:-1], path[1:]):
                edge = graph[u][v]
                latency = edge.get("latency", 0)
                stability = edge.get("stability", 0)
                switch_cost = edge.get("switch_cost", 0)

                score += stability - latency - switch_cost

            if score > best_score:
                best_score = score
                best_path = path

        if best_path is None:
            return None

        return {
            "path": best_path,
            "score": round(best_score, 3),
        }
