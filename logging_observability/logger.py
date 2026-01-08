import json
import time
from typing import Dict, Any, List


class InferenceLogger:
    """
    Structured logging for observability, auditing, and offline analysis.
    Logs are append-only and insight-only (no control).
    """

    def __init__(self, log_file: str = "inference_logs.jsonl"):
        self.log_file = log_file

    def log(
        self,
        aligned_state: Dict[str, Any],
        twin_constraints: Dict[str, Any],
        ml_outputs: Dict[str, Any],
        explanation: str,
        rtd: float,
    ) -> None:
        """
        Append a single inference record.
        """

        record = {
            "timestamp": time.time(),
            "aligned_state": aligned_state,
            "digital_twin_constraints": twin_constraints,
            "ml_outputs": ml_outputs,
            "explanation": explanation,
            "replication_time_difference": round(rtd, 4),
        }

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
