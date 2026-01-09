# edge_ingestion/stream.py

import time
import random
import math
from typing import Iterator
from dataclasses import asdict

from core_types import TelemetryPacket


def telemetry_stream() -> Iterator[TelemetryPacket]:
    """
    Simulates real-time LEO telemetry from multiple sources.
    """

    start_time = time.time()
    beam_offset = 0.0

    while True:
        now = time.time()

        # --- Geometry source ---
        if random.random() > 0.05:  # 5% packet drop
            yield TelemetryPacket(
                timestamp=now + random.uniform(-0.02, 0.02),  # clock skew
                source="geometry",
                payload={
                    "sat_pos": [7000 + random.uniform(-1, 1), 0, 0],
                    "sat_vel": [0, 7.5, 0],
                },
            )

        # --- Beam source ---
        beam_offset += 0.02 + random.uniform(-0.005, 0.005)
        yield TelemetryPacket(
            timestamp=now,
            source="beam",
            payload={
                "beam_offset": beam_offset,
                "beam_radius": 1.0,
            },
        )

        # --- RF source ---
        snr = max(5.0, 30.0 - beam_offset * 10 + random.gauss(0, 0.5))
        yield TelemetryPacket(
            timestamp=now,
            source="rf",
            payload={
                "snr": snr,
                "doppler": random.uniform(-2000, 2000),
                "timing_drift": random.uniform(-5e-6, 5e-6),
            },
        )

        # --- Topology source ---
        yield TelemetryPacket(
            timestamp=now,
            source="topology",
            payload={
                "active_links": ["SAT-A", "SAT-B", "GW-1"],
            },
        )

        # --- Environment source ---
        yield TelemetryPacket(
            timestamp=now,
            source="environment",
            payload={
                "attenuation": random.choice([0.0, 0.1, 0.3]),
            },
        )

        time.sleep(0.2)

