from typing import List, Dict, Any


class QoSRanker:
    """
    Ranks alternate links based on latency, throughput, and stability.
    """

    def rank(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        ranked = []

        for link in candidates:
            latency = link.get("latency", float("inf"))
            bandwidth = link.get("bandwidth", 0.0)
            snr = link.get("snr", 0.0)
            lifetime = link.get("lifetime", 0.0)

            # Throughput approximation (PDF-inspired)
            throughput = bandwidth * (1 + snr)

            # Simple QoS score (higher is better)
            score = throughput - latency + lifetime

            ranked.append({
                "link_id": link.get("id"),
                "score": round(score, 3),
                "latency": latency,
                "throughput": throughput,
                "lifetime": lifetime,
            })

        return sorted(ranked, key=lambda x: x["score"], reverse=True)
