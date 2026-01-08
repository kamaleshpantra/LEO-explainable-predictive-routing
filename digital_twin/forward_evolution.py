from typing import Dict, Any
import math

from core_types import AlignedState


class ForwardEvolution:
    """
    Deterministically projects near-future constraint evolution
    using physics-based approximations.
    """

    def __init__(self, horizon_seconds: float = 10.0):
        self.horizon = horizon_seconds

    def predict_beam_exit(self, state: AlignedState) -> Dict[str, Any]:
        """
        Predict time until beam exit based on beam offset dynamics.
        """

        beam = state.beam
        if not beam:
            return {"beam_exit_time": None, "reason": "missing_beam_data"}

        offset = beam.get("beam_offset")
        radius = beam.get("beam_radius")

        if offset is None or radius is None:
            return {"beam_exit_time": None, "reason": "incomplete_beam_data"}

        # If already outside beam
        if offset >= radius:
            return {"beam_exit_time": 0.0, "reason": "already_outside"}

        # Estimate offset velocity (simple linear approximation)
        # Assumption: offset increases monotonically near beam edge
        estimated_offset_rate = 0.02  # units per second (from simulation)

        if estimated_offset_rate <= 0:
            return {"beam_exit_time": None, "reason": "non_progressing_offset"}

        time_to_exit = (radius - offset) / estimated_offset_rate

        # Clamp to horizon
        if time_to_exit > self.horizon:
            return {
                "beam_exit_time": None,
                "reason": "outside_prediction_horizon",
            }

        return {
            "beam_exit_time": round(time_to_exit, 3),
            "reason": "predicted",
        }

    def evolve(self, state: AlignedState) -> Dict[str, Any]:
        """
        Perform forward evolution and return constraint predictions.
        """

        return {
            "beam_exit": self.predict_beam_exit(state),
            # Future: visibility loss, route expiry
        }
