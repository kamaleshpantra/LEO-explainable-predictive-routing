# core_types.py (conceptual, no need separate file yet)

from dataclasses import dataclass
from typing import Dict, Any
import time

@dataclass
class TelemetryPacket:
    timestamp: float          # source timestamp
    source: str               # geometry / rf / topology / env
    payload: Dict[str, Any]   # actual data


@dataclass
class AlignedState:
    time: float
    geometry: Dict[str, Any]
    rf: Dict[str, Any]
    beam: Dict[str, Any]
    topology: Dict[str, Any]
    environment: Dict[str, Any]
