import time
import streamlit as st
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


# -------------------- Streamlit Setup --------------------
st.set_page_config(
    page_title="LEO Explainable Predictive AI Dashboard",
    layout="wide"
)

st.title("LEO Explainable Predictive AI – Real-Time Dashboard")
st.caption("Predictive, parallel, and explainable inference for LEO link stability")

# -------------------- System Initialization --------------------
aligner = TimeAligner()
twin = DigitalTwinState()
evolver = ForwardEvolution()
rtd_estimator = RTDEstimator()

features = FeatureStore()
link_predictor = LinkBreakPredictor()
qos_ranker = QoSRanker()
path_selector = SafePathSelector()
narrative_engine = NarrativeEngine()

stream = telemetry_stream()

# -------------------- Dashboard Layout --------------------
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col5 = st.container()
col6 = st.container()

# -------------------- Main Loop --------------------
if "logs" not in st.session_state:
    st.session_state.logs = []

while True:
    packet = next(stream)
    aligned = aligner.add_packet(packet)

    if aligned is None:
        time.sleep(0.1)
        continue

    # --- Digital Twin ---
    twin.update(aligned)
    twin_state = twin.get_state()
    constraints = evolver.evolve(twin_state)
    rtd = rtd_estimator.compute(twin_state)

    # --- Cloud ML ---
    features.update(twin_state)
    link_pred = link_predictor.predict(features)

    # Dummy parallel links (demo purpose)
    candidates = [
        {"id": "L1", "latency": 30, "bandwidth": 10, "snr": 15, "lifetime": 6},
        {"id": "L2", "latency": 45, "bandwidth": 20, "snr": 10, "lifetime": 9},
    ]
    qos = qos_ranker.rank(candidates)

    # Dummy topology graph
    G = nx.Graph()
    G.add_edge("SAT-A", "SAT-B", latency=20, stability=8, switch_cost=1)
    G.add_edge("SAT-B", "GW-1", latency=25, stability=7, switch_cost=1)

    path = path_selector.select(G, "SAT-A", "GW-1")

    # --- Explainability ---
    reasoning = ReasoningObject(
        link_prediction=link_pred,
        qos_ranking=qos,
        path_selection=path,
        twin_constraints=constraints,
        rtd=rtd
    )

    reasoning_dict = reasoning.as_dict()
    narrative = narrative_engine.generate(reasoning_dict)

    # --- Logging ---
    st.session_state.logs.append({
        "time": time.strftime("%H:%M:%S"),
        "prediction": link_pred,
        "rtd": rtd
    })
    st.session_state.logs = st.session_state.logs[-10:]

    # -------------------- UI Rendering --------------------

    with col1:
        st.subheader("📡 Physical / Ingested State")
        st.json({
            "SNR": twin_state.rf.get("snr"),
            "Beam Offset": twin_state.beam.get("beam_offset"),
            "Doppler": twin_state.rf.get("doppler"),
        })

    with col2:
        st.subheader("🧠 Digital Twin – Future Constraints")
        st.json(constraints)

    with col3:
        st.subheader("⏳ Link Break Prediction")
        st.json(link_pred)

    with col4:
        st.subheader("🔀 Parallel Links & Safe Path")
        st.json({
            "QoS Ranking": qos,
            "Safe Path": path
        })

    with col5:
        st.subheader("📝 Explainable Inference")
        st.write(narrative)

    with col6:
        st.subheader("📊 Observability / Logs")
        st.table(st.session_state.logs)

    time.sleep(1)
