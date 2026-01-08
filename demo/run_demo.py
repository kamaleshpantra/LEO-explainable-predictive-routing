import time
import networkx as nx

from edge_ingestion.stream import telemetry_stream
from edge_ingestion.time_align import TimeAligner

from digital_twin.state_replica import DigitalTwinState
from digital_twin.forward_evolution import ForwardEvolution
from digital_twin.rtd import RTDEstimator

from cloud_ml.feature_store import FeatureStore
from cloud_ml.lstm_link_break import LinkBreakPredictor
from cloud_ml.ann_qos_ranker import QoSRanker
from cloud_ml.gnn_path_selector import SafePathSelector

from explainability.reasoning_object import ReasoningObject
from explainability.narrative_engine import NarrativeEngine


def build_demo_topology():
    """
    Build a simple LEO topology graph for demo purposes.
    """
    G = nx.Graph()
    G.add_edge("SAT-A", "SAT-B", latency=20, stability=8, switch_cost=1)
    G.add_edge("SAT-B", "SAT-C", latency=15, stability=7, switch_cost=1)
    G.add_edge("SAT-C", "GW-1", latency=25, stability=9, switch_cost=2)
    return G


def run_demo():
    print("\n=== LEO Explainable Predictive AI – DEMO START ===\n")

    # --- Initialize system ---
    stream = telemetry_stream()
    aligner = TimeAligner()

    twin = DigitalTwinState()
    evolver = ForwardEvolution()
    rtd_estimator = RTDEstimator()

    features = FeatureStore()
    link_predictor = LinkBreakPredictor()
    qos_ranker = QoSRanker()
    path_selector = SafePathSelector()
    narrative_engine = NarrativeEngine()

    topology = build_demo_topology()

    step = 0

    while step < 20:
        packet = next(stream)
        aligned = aligner.add_packet(packet)

        if aligned is None:
            continue

        twin.update(aligned)
        twin_state = twin.get_state()

        # --- Digital Twin ---
        constraints = evolver.evolve(twin_state)
        rtd = rtd_estimator.compute(twin_state)

        # --- Cloud ML ---
        features.update(twin_state)
        link_pred = link_predictor.predict(features)

        candidates = [
            {"id": "L1", "latency": 35, "bandwidth": 12, "snr": 14, "lifetime": 6},
            {"id": "L2", "latency": 45, "bandwidth": 18, "snr": 11, "lifetime": 10},
        ]
        qos = qos_ranker.rank(candidates)

        safe_path = path_selector.select(topology, "SAT-A", "GW-1")

        # --- Explainability ---
        reasoning = ReasoningObject(
            link_prediction=link_pred,
            qos_ranking=qos,
            path_selection=safe_path,
            twin_constraints=constraints,
            rtd=rtd
        )

        explanation = narrative_engine.generate(reasoning.as_dict())

        # --- Demo Output ---
        print(f"\n[STEP {step}]")
        print(f"Beam Offset: {twin_state.beam.get('beam_offset')}")
        print(f"Predicted Time-to-Break: {link_pred.get('time_to_break')}")
        print(f"Parallel Alternatives: {[l['link_id'] for l in qos]}")
        print(f"Safe Path: {safe_path['path'] if safe_path else None}")
        print("Explanation:")
        print(explanation)

        step += 1
        time.sleep(0.5)

    print("\n=== DEMO COMPLETE ===\n")


if __name__ == "__main__":
    run_demo()
