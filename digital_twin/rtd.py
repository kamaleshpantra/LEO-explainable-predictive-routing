import time
from typing import Optional

from core_types import AlignedState


class RTDEstimator:
    """
    Computes Replication Time Difference (RTD) between
    real system time and digital twin time.
    """

    def compute(self, state: AlignedState) -> float:
        """
        RTD = | current wall time - state timestamp |
        """
        now = time.time()
        return abs(now - state.time)
