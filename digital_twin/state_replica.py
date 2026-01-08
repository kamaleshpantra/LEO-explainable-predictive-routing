from typing import Dict, Any
from copy import deepcopy

from core_types import AlignedState


class DigitalTwinState:
    """
    Maintains a mirrored copy of the latest aligned physical state.
    """

    def __init__(self):
        self._state: AlignedState | None = None

    def update(self, aligned_state: AlignedState) -> None:
        """
        Update the twin with the latest aligned state.
        A deep copy is used to avoid mutation from upstream layers.
        """
        self._state = deepcopy(aligned_state)

    def get_state(self) -> AlignedState:
        """
        Return the current replicated state.
        """
        if self._state is None:
            raise RuntimeError("Digital Twin state has not been initialized yet.")
        return deepcopy(self._state)
