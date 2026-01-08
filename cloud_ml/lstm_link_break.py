from typing import Dict, Any, Optional

from cloud_ml.feature_store import FeatureStore


class LinkBreakPredictor:
    """
    Predicts time-to-link-break using temporal feature trends.
    """

    def predict(self, feature_store: FeatureStore) -> Dict[str, Any]:
        if not feature_store.is_ready():
            return {
                "time_to_break": None,
                "confidence": "low",
                "reason": "insufficient_history",
            }

        seq = feature_store.get_sequence()

        # Use most recent samples
        latest = seq[-1]
        prev = seq[-2]

        beam_offset = latest.get("beam_offset")
        beam_radius = latest.get("beam_radius")

        if beam_offset is None or beam_radius is None:
            return {
                "time_to_break": None,
                "confidence": "low",
                "reason": "missing_beam_data",
            }

        if beam_offset >= beam_radius:
            return {
                "time_to_break": 0.0,
                "confidence": "high",
                "reason": "already_outside_beam",
            }

        # Estimate offset velocity
        delta_offset = beam_offset - prev.get("beam_offset", beam_offset)
        delta_time = latest["time"] - prev["time"]

        if delta_time <= 0:
            return {
                "time_to_break": None,
                "confidence": "low",
                "reason": "invalid_time_delta",
            }

        offset_rate = delta_offset / delta_time

        if offset_rate <= 0:
            return {
                "time_to_break": None,
                "confidence": "medium",
                "reason": "non_increasing_offset",
            }

        time_to_break = (beam_radius - beam_offset) / offset_rate

        return {
            "time_to_break": round(time_to_break, 3),
            "confidence": "medium",
            "reason": "temporal_trend_extrapolation",
        }
