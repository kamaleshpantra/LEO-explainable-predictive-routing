from typing import Dict, Any


class NarrativeEngine:
    """
    Converts structured reasoning into
    clear, operator-friendly explanations.
    """

    def generate(self, reasoning: Dict[str, Any]) -> str:
        parts = []

        # --- Link break explanation ---
        lb = reasoning.get("link_break_prediction", {})
        ttb = lb.get("time_to_break")

        if ttb is not None:
            parts.append(
                f"The current link is predicted to become infeasible in approximately "
                f"{ttb} seconds."
            )
            parts.append(
                f"This estimate is based on observed temporal trends in beam alignment."
            )
        else:
            parts.append(
                "The system does not yet have sufficient confidence to predict link failure timing."
            )

        # --- Digital twin constraints ---
        twin = reasoning.get("twin_constraints", {})
        beam_exit = twin.get("beam_exit", {})

        if beam_exit.get("beam_exit_time") is not None:
            parts.append(
                f"The digital twin indicates a beam exit event in "
                f"{beam_exit['beam_exit_time']} seconds."
            )

        # --- Parallel alternatives ---
        qos = reasoning.get("parallel_link_qos", [])
        if qos:
            best = qos[0]
            parts.append(
                f"{len(qos)} parallel alternatives are available. "
                f"The strongest candidate offers an estimated throughput of "
                f"{round(best['throughput'], 2)} units."
            )
        else:
            parts.append(
                "No viable parallel links are currently available."
            )

        # --- Safe path ---
        path = reasoning.get("safe_path")
        if path:
            parts.append(
                f"The safest alternate path spans {len(path['path'])} nodes "
                f"with a composite stability score of {path['score']}."
            )

        # --- Uncertainty ---
        rtd = reasoning.get("uncertainty_rtd", 0.0)
        parts.append(
            f"Prediction uncertainty is influenced by a replication time difference "
            f"of {rtd} seconds."
        )

        return " ".join(parts)
