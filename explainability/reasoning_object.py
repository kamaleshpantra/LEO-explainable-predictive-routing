from typing import Dict, Any, List


class ReasoningObject:
    """
    Structured explanation container.
    This is NOT text generation.
    It is factual, auditable reasoning.
    """

    def __init__(
        self,
        link_prediction: Dict[str, Any],
        qos_ranking: List[Dict[str, Any]],
        path_selection: Dict[str, Any] | None,
        twin_constraints: Dict[str, Any],
        rtd: float,
    ):
        self.link_prediction = link_prediction
        self.qos_ranking = qos_ranking
        self.path_selection = path_selection
        self.twin_constraints = twin_constraints
        self.rtd = rtd

    def as_dict(self) -> Dict[str, Any]:
        """
        Convert reasoning into a structured dictionary.
        """

        return {
            "link_break_prediction": self.link_prediction,
            "parallel_link_qos": self.qos_ranking,
            "safe_path": self.path_selection,
            "twin_constraints": self.twin_constraints,
            "uncertainty_rtd": round(self.rtd, 4),
        }
