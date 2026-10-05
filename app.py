"""EcoSentinel Horizon | Global Nature Watch River Edition
Streamlit Deployment Wrapper
Seamlessly delivers the full-fidelity EcoSentinel Horizon UI within Streamlit Cloud.
"""
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="EcoSentinel Horizon | Global Nature Watch River Edition",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Seamless CSS injection: removes Streamlit default padding and borders so the Horizon dashboard fills the entire viewport
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {display: none;}
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
        max-width: 100% !important;
    }
    iframe {
        width: 100% !important;
        height: 100vh !important;
        border: none !important;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

html_file = Path(__file__).resolve().parent / "EcoSentinel_GNW_Horizon_Edition.html"

if not html_file.exists():
    st.error("EcoSentinel_GNW_Horizon_Edition.html not found. Please ensure the dashboard HTML exists in the root directory.")
else:
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=980, scrolling=True)
