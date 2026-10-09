"""
ResilientAI: Agentic AI-Based Supply Chain Decision-Support System
Main Application Entrypoint & Executive Overview
"""

import streamlit as st
from core.state import init_session_state, run_multi_agent_workflow
from core.ui_components import apply_custom_css, render_metric_card

st.set_page_config(
    page_title="ResilientAI | Supply Chain Command Room",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global styling
apply_custom_css()
init_session_state()

# Sidebar Navigation Header
st.sidebar.markdown("""
<div style="padding: 10px 0 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
    <div style="font-size: 1.3rem; font-weight: 800; color: #38bdf8; display: flex; align-items: center; gap: 8px;">
        🛡️ ResilientAI
    </div>
    <div style="font-size: 0.8rem; color: #94a3b8; margin-top: 4px;">
        Autonomous Supply Chain Decision Support
    </div>
</div>
""", unsafe_allow_html=True)

# Main Title & Hero
st.markdown('<div class="hero-badge">AI-DRIVEN SUPPLY CHAIN RESILIENCE POC</div>', unsafe_allow_html=True)
st.title("ResilientAI: Autonomous Decision-Support System")
st.markdown(
    "A multi-agent decision support platform engineered for a **three-echelon manufacturing network** "
    "facing acute disruption: an unexpected **7-day shutdown of critical primary Supplier A**."
)

# Active Disruption Banner
scenario = st.session_state.active_scenario
plan = st.session_state.recovery_plan

st.markdown(f"""
<div class="disruption-banner">
    <div style="font-size: 1.8rem;">🚨</div>
    <div style="flex-grow: 1;">
        <div class="disruption-title">ACTIVE INCIDENT: {scenario.disrupted_supplier_id} SHUTDOWN ({scenario.duration_days} DAYS)</div>
        <div class="disruption-desc">
            Primary supplier <b>Apex Microelectronics</b> is 100% offline. 
            Assembly Plant Alpha's MCU-900 buffer will deplete in <b>2.08 days</b>. 
            Coordinated agents have synthesized an optimal dual-sourcing recovery plan.
        </div>
    </div>
    <div>
        <span class="badge-passed">AGENTS READY</span>
    </div>
</div>
""", unsafe_allow_html=True)

# High-Level Real-Time KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    render_metric_card(
        "Available Buffer Runway",
        "2.08 Days",
        "Depletion: Day 2 at 16:00",
        "red"
    )

with col2:
    render_metric_card(
        "Projected Fill Rate",
        f"{plan.fulfillment_rate}%",
        f"Unmet demand: {plan.unmet_demand_units:,} units",
        "green" if plan.fulfillment_rate >= 95 else "amber"
    )

with col3:
    render_metric_card(
        "Landed Recovery Cost",
        f"${plan.total_landed_cost:,.0f}",
        f"Material + Freight + Holding",
        "blue"
    )

with col4:
    approval_color = "green" if st.session_state.plan_approval_status == "APPROVED" else "amber"
    render_metric_card(
        "Planner Approval Status",
        st.session_state.plan_approval_status.replace("_", " "),
        "Human-in-the-Loop Gating",
        approval_color
    )

st.markdown("---")

# Interconnected Modules Architecture Guide
st.markdown("### 🧭 Interconnected Control Room Architecture")
st.markdown(
    "All 6 modules share identical underlying 3-echelon network data, simulation state, and live agent interactions:"
)

c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.markdown("#### 1. 📊 Command Center")
        st.caption(
            "Executive situational awareness. View real-time KPIs, interactive 3-echelon network topology, "
            "active disruption nodes, and quick recommendations."
        )
        st.page_link("pages/1_Command_Center.py", label="Open Command Center ➔", icon="📊")

    with st.container(border=True):
        st.markdown("#### 4. 🧪 What-If Simulator")
        st.caption(
            "Stress-test the supply chain under varying disruption durations, demand spikes, supplier capacity constraints, and freight choices."
        )
        st.page_link("pages/4_What_If_Simulator.py", label="Open What-If Simulator ➔", icon="🧪")

with c2:
    with st.container(border=True):
        st.markdown("#### 2. 🤖 Agent Workspace")
        st.caption(
            "Inspect the collaborative multi-agent workflow. Review Demand, Inventory, Supplier Risk, Logistics, "
            "and Coordinator agent proposals and conflict resolution."
        )
        st.page_link("pages/2_Agent_Workspace.py", label="Open Agent Workspace ➔", icon="🤖")

    with st.container(border=True):
        st.markdown("#### 5. ⚖️ Performance & Audit")
        st.caption(
            "Benchmark ResilientAI against traditional rule-based ERP and no-action baselines across landed cost, service fill rate, and recovery time."
        )
        st.page_link("pages/5_Performance_Audit.py", label="Open Performance & Audit ➔", icon="⚖️")

with c3:
    with st.container(border=True):
        st.markdown("#### 3. 🎯 Recovery Planner")
        st.caption(
            "Inspect the final actionable recovery plan: multi-source purchase allocations, expedited air schedules, "
            "constraint validations, and planner sign-off."
        )
        st.page_link("pages/3_Recovery_Planner.py", label="Open Recovery Planner ➔", icon="🎯")

    with st.container(border=True):
        st.markdown("#### 6. 🗄️ Supply Chain Data")
        st.caption(
            "Inspect and edit underlying datasets: supplier capacity, bill of materials, inventory stock, customer tiers, and CSV export/import."
        )
        st.page_link("pages/6_Supply_Chain_Data.py", label="Open Supply Chain Data ➔", icon="🗄️")

st.markdown("---")

# Quick Actions
q1, q2 = st.columns([2, 1])
with q1:
    st.info(
        "💡 **Planner Quick Action**: To review and approve the recommended multi-agent recovery plan, "
        "navigate directly to the **Recovery Planner** or click below."
    )
with q2:
    if st.button("🚀 Re-Run Multi-Agent Workflow", use_container_width=True):
        with st.spinner("Executing agent DAG and solver..."):
            run_multi_agent_workflow()
        st.success("Workflow refreshed successfully!")
        st.rerun()
