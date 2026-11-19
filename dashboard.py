
import json
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Federated Learning Dashboard",
    page_icon="FL",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
RESULTS_PATH = BASE_DIR / "results.json"

# ============================================================
# LOAD EXPERIMENT RESULTS
# ============================================================

def load_results():
    if not RESULTS_PATH.exists():
        return None

    try:
        with open(RESULTS_PATH, "r", encoding="utf-8-sig") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return None

results = load_results()

if results is None:
    st.error("results.json tidak ditemukan atau tidak dapat dibaca.")
    st.info("Pastikan results.json berada di folder utama proyek.")
    st.stop()

round_history = results.get("round_history", [])

if not round_history:
    st.error("Riwayat training belum tersedia.")
    st.stop()

total_rounds = results.get("total_rounds", len(round_history))
total_clients = results.get("total_clients", 3)
samples_per_client = results.get("samples_per_client", 40)

final_accuracy = round_history[-1].get("accuracy")
final_loss = round_history[-1].get("loss")

if final_accuracy is None or final_loss is None:
    st.error("Data akurasi atau loss belum lengkap.")
    st.stop()

# ============================================================
# DASHBOARD STYLE
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(ellipse at 50% 0%, rgba(104,78,210,.13), transparent 45%),
        linear-gradient(135deg, #0d1025 0%, #151a37 55%, #1d2045 100%);
    color: #ffffff;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: #10142d;
    border-right: 1px solid rgba(150,140,255,.15);
}

.section-title {
    color: #ffffff;
    font-size: 19px;
    font-weight: 700;
    margin-top: 28px;
    margin-bottom: 14px;
}

.metric-card {
    background: linear-gradient(145deg, #242b55, #191e40);
    border: 1px solid rgba(160,170,255,.19);
    border-radius: 17px;
    padding: 20px;
    min-height: 128px;
    box-shadow: 0 8px 28px rgba(0,0,0,.18);
    transition: .25s ease;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: rgba(167,139,250,.65);
    box-shadow: 0 12px 35px rgba(100,80,220,.18);
}

.metric-label {
    color: #b8c2e8;
    font-size: 13px;
    margin-bottom: 12px;
}

.metric-value {
    color: #ffffff;
    font-size: 30px;
    font-weight: 800;
}

.metric-caption {
    color: #9ca9d5;
    font-size: 12px;
    margin-top: 5px;
}

.stButton button {
    background: linear-gradient(90deg, #7657e8, #477de8);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 600;
}

[data-testid="stDataFrame"] {
    border: 1px solid rgba(160,170,255,.18);
    border-radius: 12px;
    overflow: hidden;
}

.footer {
    text-align: center;
    color: #8491bd;
    font-size: 12px;
    padding: 28px 0 10px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIMPLE DASHBOARD TITLE
# ============================================================

st.title("Federated Learning Dashboard")

st.caption(
    "Distributed Machine Learning | Flower Framework | FedAvg Architecture"
)

st.markdown(
    "**Dechinta Mutiara Hazrina**  |  24221022"
)

st.markdown("---")

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## FEDERATED LEARNING")
    st.caption("EXPERIMENT CONTROL PANEL")
    st.markdown("---")

    st.markdown("### Experiment Status")
    st.success("COMPLETED")

    st.markdown("### Configuration")
    st.write(f"Training Rounds: **{total_rounds}**")
    st.write(f"Participating Clients: **{total_clients}**")
    st.write(f"Samples per Client: **{samples_per_client}**")
    st.write("Aggregation: **FedAvg**")
    st.write("Model: **Logistic Regression**")

    st.markdown("---")

    if st.button("Refresh Results", use_container_width=True):
        st.rerun()

    st.caption("Source: results.json")

# ============================================================
# EXPERIMENT METRICS
# ============================================================

st.markdown(
    '<div class="section-title">Experiment Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

metrics = [
    ("GLOBAL ACCURACY", f"{final_accuracy * 100:.2f}%", "Final global evaluation"),
    ("FINAL LOSS", f"{final_loss:.4f}", "Last training round"),
    ("TRAINING ROUNDS", f"{total_rounds}/{total_rounds}", "Completed rounds"),
    ("PARTICIPATING CLIENTS", f"{total_clients}/{total_clients}", "Clients participated"),
]

for col, (label, value, caption) in zip(
    [col1, col2, col3, col4], metrics
):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-caption">{caption}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# FEDERATED NETWORK ARCHITECTURE
# ============================================================

st.markdown(
    '<div class="section-title">Federated Network Architecture</div>',
    unsafe_allow_html=True
)

network_html = """
<!DOCTYPE html>
<html>
<head>
<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Arial, sans-serif;
    color: white;
}

.network-wrapper {
    background:
        radial-gradient(ellipse at center, rgba(105,75,220,.22), transparent 58%),
        linear-gradient(145deg, #11152f, #171b3b 65%, #11162e);
    border: 1px solid rgba(150,130,255,.28);
    border-radius: 23px;
    padding: 16px 10px;
    overflow: hidden;
    box-shadow: 0 15px 45px rgba(0,0,0,.25);
}

.heading {
    text-align: center;
    color: #c4b5fd;
    font-size: 13px;
    font-weight: bold;
    letter-spacing: 3px;
    padding: 8px;
}

svg {
    display: block;
    width: 100%;
    height: auto;
}

.network-label {
    fill: white;
    font-size: 17px;
    font-weight: bold;
    text-anchor: middle;
}

.network-sub {
    fill: #aab8e8;
    font-size: 11px;
    text-anchor: middle;
}

.flow-forward {
    fill: none;
    stroke: #38d9e8;
    stroke-width: 3;
    stroke-dasharray: 9 10;
    animation: forward 1.4s linear infinite;
}

.flow-return {
    fill: none;
    stroke: #a78bfa;
    stroke-width: 3;
    stroke-dasharray: 9 10;
    animation: backward 1.4s linear infinite;
}

@keyframes forward {
    to { stroke-dashoffset: -38; }
}

@keyframes backward {
    to { stroke-dashoffset: 38; }
}

.pulse {
    fill: none;
    stroke: #a78bfa;
    stroke-width: 2;
    transform-box: fill-box;
    transform-origin: center;
    animation: pulse 2.4s ease-out infinite;
}

.client-pulse {
    stroke: #38bdf8;
    animation-delay: .6s;
}

@keyframes pulse {
    0% { transform: scale(.85); opacity: .9; }
    100% { transform: scale(1.65); opacity: 0; }
}

.server-core {
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { opacity: .7; }
    to { opacity: 1; }
}

.caption {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 25px;
    color: #bdc8ed;
    font-size: 12px;
    padding: 12px 5px 6px;
}

.dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    margin-right: 6px;
}

@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; }
}
</style>
</head>
<body>

<div class="network-wrapper">

<div class="heading">DISTRIBUTED INTELLIGENCE NETWORK</div>

<svg viewBox="0 0 1000 570" xmlns="http://www.w3.org/2000/svg">

<defs>
    <radialGradient id="serverGradient">
        <stop offset="0%" stop-color="#765ce9"/>
        <stop offset="100%" stop-color="#25235d"/>
    </radialGradient>

    <radialGradient id="clientGradient">
        <stop offset="0%" stop-color="#245c86"/>
        <stop offset="100%" stop-color="#172447"/>
    </radialGradient>

    <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
        <feGaussianBlur stdDeviation="7" result="blur"/>
        <feMerge>
            <feMergeNode in="blur"/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>

    <marker id="arrowCyan" markerWidth="10" markerHeight="10"
            refX="8" refY="5" orient="auto">
        <path d="M0 0 L10 5 L0 10 Z" fill="#38d9e8"/>
    </marker>

    <marker id="arrowPurple" markerWidth="10" markerHeight="10"
            refX="8" refY="5" orient="auto">
        <path d="M0 0 L10 5 L0 10 Z" fill="#a78bfa"/>
    </marker>
</defs>

<g fill="none" stroke="#7778bd" stroke-width="1" opacity=".17">
    <circle cx="500" cy="280" r="115"/>
    <circle cx="500" cy="280" r="185"/>
    <circle cx="500" cy="280" r="255"/>
</g>

<path d="M450 250 Q300 85 205 125"
      class="flow-forward" marker-end="url(#arrowCyan)"/>
<path d="M205 155 Q320 220 450 285"
      class="flow-return" marker-end="url(#arrowPurple)"/>

<path d="M550 250 Q700 85 795 125"
      class="flow-forward" marker-end="url(#arrowCyan)"/>
<path d="M795 155 Q680 220 550 285"
      class="flow-return" marker-end="url(#arrowPurple)"/>

<path d="M500 340 Q500 420 500 465"
      class="flow-forward" marker-end="url(#arrowCyan)"/>
<path d="M530 465 Q555 405 530 340"
      class="flow-return" marker-end="url(#arrowPurple)"/>

<g fill="#a5f3fc" filter="url(#glow)">
    <circle r="7">
        <animateMotion dur="2.8s" repeatCount="indefinite"
            path="M450 250 Q300 85 205 125"/>
    </circle>
    <circle r="7">
        <animateMotion dur="3.1s" begin=".6s" repeatCount="indefinite"
            path="M550 250 Q700 85 795 125"/>
    </circle>
    <circle r="7">
        <animateMotion dur="2.5s" begin="1s" repeatCount="indefinite"
            path="M500 340 Q500 420 500 465"/>
    </circle>
</g>

<g fill="#c4b5fd" filter="url(#glow)">
    <circle r="6">
        <animateMotion dur="3s" begin=".4s" repeatCount="indefinite"
            path="M205 155 Q320 220 450 285"/>
    </circle>
    <circle r="6">
        <animateMotion dur="2.7s" begin="1s" repeatCount="indefinite"
            path="M795 155 Q680 220 550 285"/>
    </circle>
    <circle r="6">
        <animateMotion dur="2.9s" begin=".8s" repeatCount="indefinite"
            path="M530 465 Q555 405 530 340"/>
    </circle>
</g>

<!-- CLIENT 01 -->
<circle cx="180" cy="140" r="49" class="pulse client-pulse"/>
<circle cx="180" cy="140" r="39" fill="#172d50"
        stroke="#38bdf8" stroke-width="2.5" filter="url(#glow)"/>
<circle cx="180" cy="140" r="29" fill="url(#clientGradient)"/>
<text x="180" y="146" class="network-label">C1</text>
<text x="180" y="202" class="network-label">CLIENT 01</text>
<text x="180" y="220" class="network-sub">LOCAL TRAINING</text>

<!-- CLIENT 02 -->
<circle cx="820" cy="140" r="49" class="pulse client-pulse"/>
<circle cx="820" cy="140" r="39" fill="#172d50"
        stroke="#38bdf8" stroke-width="2.5" filter="url(#glow)"/>
<circle cx="820" cy="140" r="29" fill="url(#clientGradient)"/>
<text x="820" y="146" class="network-label">C2</text>
<text x="820" y="202" class="network-label">CLIENT 02</text>
<text x="820" y="220" class="network-sub">LOCAL TRAINING</text>

<!-- CLIENT 03 -->
<circle cx="500" cy="485" r="49" class="pulse client-pulse"/>
<circle cx="500" cy="485" r="39" fill="#172d50"
        stroke="#38bdf8" stroke-width="2.5" filter="url(#glow)"/>
<circle cx="500" cy="485" r="29" fill="url(#clientGradient)"/>
<text x="500" y="491" class="network-label">C3</text>
<text x="500" y="545" class="network-label">CLIENT 03</text>

<!-- CENTRAL SERVER -->
<circle cx="500" cy="280" r="76" class="pulse"/>
<circle cx="500" cy="280" r="65" fill="#20234e"
        stroke="#a78bfa" stroke-width="2.5" filter="url(#glow)"/>
<circle cx="500" cy="280" r="53" fill="url(#serverGradient)"
        class="server-core"/>
<circle cx="500" cy="280" r="40" fill="none"
        stroke="#c4b5fd" stroke-width="1.5" opacity=".7"/>

<text x="500" y="276" class="network-label" font-size="23">FL</text>
<text x="500" y="296" class="network-sub">SERVER</text>
<text x="500" y="375" class="network-label">FEDAVG AGGREGATION</text>

</svg>

<div class="caption">
    <span>
        <span class="dot" style="background:#38d9e8;"></span>
        Global Model Distribution
    </span>
    <span>
        <span class="dot" style="background:#a78bfa;"></span>
        Local Model Updates
    </span>
</div>

</div>
</body>
</html>
"""

components.html(
    network_html,
    height=650,
    scrolling=False
)

# ============================================================
# HOW FEDERATED LEARNING WORKS
# ============================================================

st.markdown(
    '<div class="section-title">How Federated Learning Works</div>',
    unsafe_allow_html=True
)

process_col1, process_col2 = st.columns(2)

process_steps = [
    (
        "01 — SERVER",
        "Global Model Distribution",
        "The server distributes the current global model to all participating clients."
    ),
    (
        "02 — CLIENTS",
        "Local Model Training",
        "Each client trains its own model using local data. Raw training data remains on the client."
    ),
    (
        "03 — COMMUNICATION",
        "Model Update Transmission",
        "Clients send model parameters and updates back to the central server."
    ),
    (
        "04 — FEDAVG",
        "Global Aggregation",
        "The server aggregates client model parameters to produce an updated global model."
    ),
]

for index, (number, heading, description) in enumerate(process_steps):
    col = process_col1 if index % 2 == 0 else process_col2

    with col:
        st.markdown(f"""
        <div class="metric-card" style="min-height:145px; margin-bottom:15px;">
            <div style="color:#a78bfa; font-size:12px; font-weight:700;">
                {number}
            </div>
            <div style="color:white; font-size:17px; font-weight:700; margin:10px 0;">
                {heading}
            </div>
            <div style="color:#b8c2e8; font-size:13px; line-height:1.7;">
                {description}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# TRAINING PERFORMANCE CHART
# ============================================================

st.markdown(
    '<div class="section-title">Training Performance</div>',
    unsafe_allow_html=True
)

round_numbers = [item["round"] for item in round_history]
accuracies = [item["accuracy"] * 100 for item in round_history]
losses = [item["loss"] for item in round_history]

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(
        x=round_numbers,
        y=accuracies,
        name="Accuracy",
        mode="lines+markers",
        line=dict(color="#9b87ff", width=3),
        marker=dict(size=10),
        hovertemplate="Round %{x}<br>Accuracy: %{y:.2f}%<extra></extra>"
    ),
    secondary_y=False
)

fig.add_trace(
    go.Scatter(
        x=round_numbers,
        y=losses,
        name="Loss",
        mode="lines+markers",
        line=dict(color="#42d6d0", width=3),
        marker=dict(size=9),
        hovertemplate="Round %{x}<br>Loss: %{y:.4f}<extra></extra>"
    ),
    secondary_y=True
)

fig.update_layout(
    height=420,
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(32,38,75,0.65)",
    font=dict(color="#dce3ff"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    margin=dict(l=20, r=20, t=45, b=20),
    hovermode="x unified"
)

fig.update_xaxes(
    title_text="Training Round",
    dtick=1,
    gridcolor="rgba(255,255,255,0.08)"
)

fig.update_yaxes(
    title_text="Accuracy (%)",
    gridcolor="rgba(255,255,255,0.08)",
    secondary_y=False
)

fig.update_yaxes(
    title_text="Loss",
    secondary_y=True
)

st.plotly_chart(fig, use_container_width=True)

# ============================================================
# ROUND RESULTS TABLE
# ============================================================

st.markdown(
    '<div class="section-title">Detailed Round Results</div>',
    unsafe_allow_html=True
)

table_data = []

for item in round_history:
    table_data.append({
        "Round": item["round"],
        "Global Accuracy": f'{item["accuracy"] * 100:.2f}%',
        "Loss": f'{item["loss"]:.6f}',
        "Status": "Completed"
    })

st.dataframe(
    table_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# EXPERIMENT SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">Experiment Summary</div>',
    unsafe_allow_html=True
)

summary_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 0;
    background: transparent;
    font-family: Arial, sans-serif;
    color: white;
}}

.summary-card {{
    background: linear-gradient(145deg, #242b55, #191e40);
    border: 1px solid rgba(160,170,255,.25);
    border-radius: 18px;
    padding: 26px;
    box-shadow: 0 8px 28px rgba(0,0,0,.18);
}}

.summary-heading {{
    color: #c4b5fd;
    font-size: 21px;
    font-weight: 700;
    margin: 0 0 18px 0;
}}

.summary-description {{
    color: #dce3ff;
    font-size: 14px;
    line-height: 1.9;
    margin-bottom: 18px;
}}

.highlight {{
    color: #55e6c1;
    font-weight: bold;
}}

.accuracy-badge {{
    display: inline-block;
    color: white;
    font-size: 27px;
    font-weight: bold;
    padding: 12px 19px;
    border-radius: 12px;
    margin: 5px 0 12px;
    background: linear-gradient(90deg, #7657e8, #477de8);
    box-shadow: 0 5px 18px rgba(100,80,220,.25);
}}

.summary-loss {{
    color: #dce3ff;
    font-size: 14px;
    line-height: 1.9;
    margin-top: 8px;
}}

.summary-note {{
    color: #9ca9d5;
    font-size: 12px;
    line-height: 1.7;
    border-top: 1px solid rgba(160,170,255,.18);
    padding-top: 14px;
    margin-top: 18px;
}}

@media (max-width: 600px) {{
    .summary-card {{
        padding: 19px;
    }}

    .summary-heading {{
        font-size: 18px;
    }}

    .accuracy-badge {{
        font-size: 23px;
    }}
}}
</style>
</head>

<body>
    <div class="summary-card">

        <h3 class="summary-heading">
            Federated Learning Experiment Completed
        </h3>

        <p class="summary-description">
            The experiment involved
            <span class="highlight">{total_clients} participating clients</span>,
            each containing
            <span class="highlight">{samples_per_client} local samples</span>,
            and completed
            <span class="highlight">{total_rounds} training rounds</span>
            using the Federated Averaging (FedAvg) algorithm.
        </p>

        <div class="accuracy-badge">
            {final_accuracy * 100:.2f}% Accuracy
        </div>

        <p class="summary-loss">
            Final global evaluation achieved a loss value of
            <span class="highlight">{final_loss:.4f}</span>.
        </p>

        <div class="summary-note">
            The network animation is a visual representation of the
            Federated Learning communication workflow. It does not
            represent a live connection to the completed experiment.
        </div>

    </div>
</body>
</html>
"""

components.html(
    summary_html,
    height=310,
    scrolling=False
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">
    FEDERATED LEARNING PROJECT
    <br>
    Dechinta Mutiara Hazrina • 24221022
    <br>
    Flower Framework • FedAvg • Streamlit Dashboard
</div>
""", unsafe_allow_html=True)