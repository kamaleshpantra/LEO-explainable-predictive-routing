# 📡 LEO Explainable Predictive AI for Link Stability & Parallel Routing

A real-time, explainable, and predictive monitoring system for **Low Earth Orbit (LEO) satellite networks**, designed to anticipate link instability, evaluate parallel alternatives, and provide human-readable insights — **without direct control actions**.

---

## 🚀 Problem Statement

LEO satellite constellations are highly dynamic due to:
- High orbital velocity
- Beam drift and handovers
- RF degradation and environmental effects
- Rapidly changing network topology

Traditional systems react **after** failures occur.  
This project focuses on **predictive, parallel, and explainable inference** to support **proactive decision-making** by human operators.

---

## 🎯 Objectives

- Predict **link instability before failure**
- Identify **parallel alternative links**
- Recommend **safe fallback paths**
- Maintain a **digital twin** of the system
- Provide **explainable, auditable outputs**
- Respect **human-in-the-loop (no direct control)** constraints

---



## 🧠 System Architecture

Telemetry Sources
(Geometry, RF, Beam, Topology, Environment)
↓
Time Alignment
↓
Aligned System State
(Single Source of Truth)
↓
Digital Twin Replication
↓
Parallel Predictive Inference
├─ Link Break Prediction
├─ QoS Ranking
└─ Safe Path Selection
↓
Explainability Engine
↓
Observability & Dashboard
↺ Continuous Insight Cycle


> ⚠️ This is a **continuous insight loop**, not a control loop.  
> The system never enforces routing or switching decisions automatically.

---

## 🧩 System Components (Explained)

### 1️⃣ Telemetry Ingestion
Simulates real-time LEO telemetry from multiple subsystems:
- Geometry (position, velocity)
- Beam alignment
- RF metrics (SNR, Doppler)
- Network topology
- Environmental attenuation

Includes:
- Packet loss
- Clock skew
- Noise and degradation

📁 `edge_ingestion/stream.py`

---

### 2️⃣ Time Alignment
Telemetry arrives asynchronously.  
The time aligner:
- Buffers packets by source
- Selects packets closest in time
- Uses a configurable time window
- Falls back to last-known values if needed

This produces a **single synchronized snapshot**.

📁 `edge_ingestion/time_align.py`

---

### 3️⃣ Aligned State (Single Source of Truth)
A unified snapshot containing:
- Geometry
- RF metrics
- Beam state
- Topology
- Environment

All downstream logic uses **only this state**, never raw telemetry.

📁 `core_types.py`

---

### 4️⃣ Digital Twin
Creates a safe replica of the aligned state for:
- Forward reasoning
- Constraint estimation
- Uncertainty analysis

The real system is never modified.

📁 `digital_twin/`

---

### 5️⃣ Parallel Predictive Models

Predictions are executed **in parallel**, not sequentially:

- **Link Break Prediction**  
  Estimates instability timing and confidence.

- **QoS Ranking**  
  Scores parallel links using throughput, latency, and lifetime heuristics.

- **Safe Path Selection**  
  Evaluates alternative end-to-end paths using graph-based reasoning.

📁 `cloud_ml/`

---

### 6️⃣ Explainability Layer
Transforms raw predictions into **human-readable explanations**, explicitly stating:
- Confidence level
- Reasons for uncertainty
- Available alternatives
- Supporting evidence

📁 `explainability/`

---

### 7️⃣ Observability & Logging
Logs:
- Aligned state
- Predictions
- Confidence values
- Replication Time Difference (RTD)
- Explanations

This ensures traceability and auditability.

📁 `logging_observability/`

---

### 8️⃣ Real-Time Dashboard
An interactive Streamlit dashboard displaying:
- Live telemetry state
- Link break predictions
- Ranked alternatives
- Safe paths
- Natural-language explanations
- Observability logs

📁 `dashboard/app.py`

---

## 📊 Example Output (What the User Sees)

- Physical and RF state
- Predicted link break risk with confidence
- Ranked parallel alternatives
- Safe fallback path
- Explainable narrative
- RTD indicating data freshness

Low confidence at startup is **expected and correct** due to limited history.

---

## 🔁 Continuous Insight Cycle

The system continuously:
1. Observes telemetry
2. Aligns data in time
3. Updates the digital twin
4. Runs parallel predictions
5. Generates explanations
6. Updates dashboard and logs

No automated control actions are taken.

---

## ☁️ Cloud-Based ML (Clarification)

“Cloud-based” in this context means:
- Centralized prediction logic
- Parallel inference
- Shared feature state
- Explainability and observability

The hackathon prototype simulates this architecture locally.

---

## 🛠️ Tech Stack

- Python 3.10+
- Streamlit (dashboard)
- NumPy / Pandas
- Graph-based reasoning
- Explainable AI principles

---

## ⚙️ Setup & Run

```bash
git clone <your-repo-url>
cd LEO-explainable-predictive-routing

python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
streamlit run dashboard/app.py
