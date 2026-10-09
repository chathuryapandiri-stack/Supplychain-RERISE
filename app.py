"""
ResilientAI: Agentic AI-Based Supply Chain Decision-Support System
Application Router & Navigation Orchestrator
"""

import streamlit as st

# Configure global app shell
st.set_page_config(
    page_title="ResilientAI | Supply Chain Command Room",
    page_icon=":material/shield:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Protect subsequent set_page_config calls in individual page files so they don't error
_orig_set_page_config = st.set_page_config
def _noop_set_page_config(*args, **kwargs):
    pass
st.set_page_config = _noop_set_page_config

# Navigation definition (Removes the redundant 'app' page from the sidebar)
pages = [
    st.Page("pages/1_Command_Center.py", title="Command Center", icon=":material/dashboard:", default=True),
    st.Page("pages/2_Agent_Workspace.py", title="Agent Workspace", icon=":material/smart_toy:"),
    st.Page("pages/3_Recovery_Planner.py", title="Recovery Planner", icon=":material/alt_route:"),
    st.Page("pages/4_What_If_Simulator.py", title="What-If Simulator", icon=":material/science:"),
    st.Page("pages/5_Performance_Audit.py", title="Performance & Audit", icon=":material/fact_check:"),
    st.Page("pages/6_Supply_Chain_Data.py", title="Supply Chain Data", icon=":material/database:"),
]

pg = st.navigation(pages)
pg.run()
