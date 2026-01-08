from collections import deque
from typing import Dict, Any, Deque

from core_types import AlignedState


class FeatureStore:
    """
    Maintains time-windowed features shared across all ML heads.
    """

    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.history: Deque[Dict[str, Any]] = deque(maxlen=window_size)

    def update(self, state: AlignedState) -> None:
        """
        Extract and store features from the aligned state.
        """

        features = {
            "time": state.time,
            "snr": state.rf.get("snr"),
            "doppler": state.rf.get("doppler"),
            "timing_drift": state.rf.get("timing_drift"),
            "beam_offset": state.beam.get("beam_offset"),
            "beam_radius": state.beam.get("beam_radius"),
            "attenuation": state.environment.get("attenuation"),
        }

        self.history.append(features)

    def get_sequence(self) -> list[Dict[str, Any]]:
        """
        Return the full time-ordered feature window.
        """
        return list(self.history)

    def is_ready(self) -> bool:
        """
        Check if sufficient history exists for time-series models.
        """
        return len(self.history) >= 3
