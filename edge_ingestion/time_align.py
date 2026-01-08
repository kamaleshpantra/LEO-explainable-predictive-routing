# edge_ingestion/time_align.py

import time
from collections import defaultdict
from typing import Optional

from core_types import TelemetryPacket, AlignedState


class TimeAligner:
    def __init__(self, window: float = 0.1):
        self.window = window
        self.buffer = defaultdict(list)
        self.last_state = {}

    def add_packet(self, packet: TelemetryPacket) -> Optional[AlignedState]:
        self.buffer[packet.source].append(packet)

        current_time = time.time()

        # Check if we have enough data to align
        aligned_payload = {}

        for source, packets in self.buffer.items():
            # Choose packet closest to current_time
            closest = min(
                packets,
                key=lambda p: abs(p.timestamp - current_time),
                default=None,
            )

            if closest and abs(closest.timestamp - current_time) <= self.window:
                aligned_payload[source] = closest.payload
                self.last_state[source] = closest.payload
            else:
                # Use last known value if missing
                if source in self.last_state:
                    aligned_payload[source] = self.last_state[source]
                else:
                    return None  # cannot align yet

        # Clear buffer to prevent memory growth
        self.buffer.clear()

        return AlignedState(
            time=current_time,
            geometry=aligned_payload.get("geometry", {}),
            rf=aligned_payload.get("rf", {}),
            beam=aligned_payload.get("beam", {}),
            topology=aligned_payload.get("topology", {}),
            environment=aligned_payload.get("environment", {}),
        )
