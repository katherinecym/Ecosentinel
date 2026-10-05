"""EcoSentinel-DipteraCAST | Interactive Decision-Support Dashboard
Run locally:
    streamlit run app.py
Deploy to Streamlit Community Cloud:
    Point main file path to app.py
"""
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="EcoSentinel Policy Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

@st.cache_data
def load_data():
    station_path = DATA_DIR / "Project_A_Module5_ECDC_Alert_Station_Roster.csv"
    health_path = DATA_DIR / "Project_A_Module2_DALY_Health_Economics.csv"
    
    if not station_path.exists() or not health_path.exists():
        st.error(f"Required data files not found in {DATA_DIR}. Please check data folder.")
        st.stop()
        
    station = pd.read_csv(station_path)
    health = pd.read_csv(health_path)
    return station, health

def scale_intensity(do_gain, flow_gain, bod_reduction):
    # Transparent interpolation to the precomputed fixed NbS package; no model refitting occurs.
    return min(1.0, (min(do_gain / 3.0, 1.0) + min(flow_gain / 0.35, 1.0) + min(bod_reduction / 0.65, 1.0)) / 3.0)

def assign_level(prob, elderly, impulse, dry_days, stagnation):
    if prob >= 0.75 and elderly > 500:
        return "Level_4_Red"
    if prob >= 0.50 or impulse > 4:
        return "Level_3_Orange"
    if prob >= 0.25 or (3 <= dry_days <= 5) or stagnation >= 0.10:
        return "Level_2_Yellow"
    return "Level_1_Green"

# --- Header & Overview ---
st.title("🌊 EcoSentinel-DipteraCAST | Scenario Decision Dashboard")
st.markdown("""
**Physics-informed Causal AI for Urban River Biosecurity & Nature-based Solutions (NbS)**  
*Evaluating early-warning vector escalation risks across European pilot river networks.*
""")
st.caption("⚠️ Real-data-only inputs; all intervention results are interpolated model-counterfactual scenarios requiring field validation and local municipal authorization.")

station, health = load_data()

# --- Sidebar Controls ---
st.sidebar.header("🎯 Pilot Basin & Scenario Tuning")
cities = sorted(station.city.unique())
city = st.sidebar.selectbox("Select Pilot City", cities, index=0)

st.sidebar.markdown("---")
st.sidebar.subheader("🌿 NbS Hydrological Interventions")
do_gain = st.sidebar.slider("Δ Dissolved Oxygen (mg/L)", 0.0, 5.0, 1.0, 0.1, help="Aeration / re-oxygenation gain")
flow_gain = st.sidebar.slider("Δ Baseflow Velocity (m/s)", 0.0, 0.40, 0.10, 0.01, help="Flushing / hydraulic control increase")
bod_reduction = st.sidebar.slider("BOD5 Reduction Fraction", 0.0, 0.80, 0.30, 0.01, help="Organic load abatement")

scale = scale_intensity(do_gain, flow_gain, bod_reduction)

# --- Computation ---
d = station[station.city.eq(city)].copy()
d["scenario_p_vector"] = (d.p_vector_baseline - scale * d.delta_p_vector).clip(0, 1)
d["scenario_delta_par"] = scale * d.delta_par_total
d["scenario_delta_par65"] = scale * d.delta_par_age65
d["scenario_alert"] = d.apply(
    lambda r: assign_level(
        r.scenario_p_vector,
        r.buffer_500m_pop_age65,
        r.dry_to_wet_impulse,
        r.consecutive_dry_days,
        r.vector_stagnation_index
    ),
    axis=1
)

h = health[health.city.eq(city)].iloc[0]

# --- Key Metrics ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Mean Vector Risk Drop", f"{(d.p_vector_baseline - d.scenario_p_vector).mean():.1%}")
m2.metric("Protected PAR Index", f"{d.scenario_delta_par.sum():,.0f} people")
m3.metric("Avoided Elder WNND Cases", f"{scale * h.avoided_expected_wnnd_cases:.2f}")
m4.metric("Avoided Acute Costs (€)", f"€{scale * h.avoided_acute_medical_cost_eur:,.0f}")

st.info(f"💡 Current Intervention Intensity: **{scale:.1%}** of precomputed full NbS restoration package. Interpolated scenario projection.")

# --- Spatial Map ---
color_map = {
    "Level_1_Green": "#2ecc71",
    "Level_2_Yellow": "#f1c40f",
    "Level_3_Orange": "#e67e22",
    "Level_4_Red": "#e74c3c"
}

fig = px.scatter_mapbox(
    d,
    lat="latitude",
    lon="longitude",
    color="scenario_alert",
    size="scenario_p_vector",
    hover_name="station_id",
    hover_data={
        "scenario_p_vector": ":.3f",
        "scenario_delta_par": ":.0f",
        "buffer_500m_pop_age65": True,
        "latitude": False,
        "longitude": False
    },
    color_discrete_map=color_map,
    zoom=11,
    height=520,
    title=f"Monitoring Station Alert Distribution - {city}"
)
fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=30, b=0))
st.plotly_chart(fig, use_container_width=True)

# --- Detail Breakdown ---
col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("📋 Station Alert Roster")
    display_df = d[[
        "station_id", "scenario_alert", "scenario_p_vector",
        "scenario_delta_par", "scenario_delta_par65",
        "dry_to_wet_impulse", "vector_stagnation_index"
    ]].sort_values("scenario_p_vector", ascending=False)
    st.dataframe(display_df, use_container_width=True, height=350)

with col_right:
    st.subheader("📊 Alert Level Breakdown")
    alert_counts = d["scenario_alert"].value_counts().reindex(
        ["Level_1_Green", "Level_2_Yellow", "Level_3_Orange", "Level_4_Red"],
        fill_value=0
    )
    st.bar_chart(alert_counts, color="#3498db")
    st.caption("📌 Alert thresholds conform to EcoSentinel operational rules for decision support.")
