"""
ResilientAI - Page 2: Agent Workspace (Collaborative AI Analysis)
Interactive multi-agent workflow DAG, agent inspector, inputs/outputs, and conflict reconciliation.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from core.state import init_session_state
from core.ui_components import apply_custom_css

st.set_page_config(page_title="Agent Workspace | ResilientAI", page_icon="🤖", layout="wide")
apply_custom_css()
init_session_state()

st.markdown('<div class="hero-badge">PAGE 2 • AGENT WORKSPACE</div>', unsafe_allow_html=True)
st.title("Collaborative AI Agent Workspace")
st.caption("Inspect the 5 specialized autonomous agents, their inputs, outputs, schemas, and conflict resolution.")

wf = st.session_state.workflow_execution
agent_results = wf["agent_results"]

# Workflow Pipeline Diagram
st.markdown("### 🔄 Multi-Agent Directed Acyclic Graph (DAG)")
st.markdown("""
<div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(51, 65, 85, 0.8); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px;">
        <div style="text-align: center; flex: 1; min-width: 130px; background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #38bdf8; font-weight: 700;">STEP 1</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 0.95rem;">Demand Agent</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Customer Tiers & Needs</div>
            <div style="font-size: 0.7rem; color: #34d399; margin-top: 4px;">● COMPLETED</div>
        </div>
        <div style="color: #64748b; font-weight: bold; font-size: 1.2rem;">➔</div>
        <div style="text-align: center; flex: 1; min-width: 130px; background: rgba(248, 113, 113, 0.1); border: 1px solid #f87171; padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #f87171; font-weight: 700;">STEP 2</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 0.95rem;">Inventory Agent</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Runway & Starvation</div>
            <div style="font-size: 0.7rem; color: #34d399; margin-top: 4px;">● COMPLETED</div>
        </div>
        <div style="color: #64748b; font-weight: bold; font-size: 1.2rem;">➔</div>
        <div style="text-align: center; flex: 1; min-width: 130px; background: rgba(251, 191, 36, 0.1); border: 1px solid #fbbf24; padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #fbbf24; font-weight: 700;">STEP 3</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 0.95rem;">Supplier Risk Agent</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Capacity & Dual-Source</div>
            <div style="font-size: 0.7rem; color: #34d399; margin-top: 4px;">● COMPLETED</div>
        </div>
        <div style="color: #64748b; font-weight: bold; font-size: 1.2rem;">➔</div>
        <div style="text-align: center; flex: 1; min-width: 130px; background: rgba(52, 211, 153, 0.1); border: 1px solid #34d399; padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #34d399; font-weight: 700;">STEP 4</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 0.95rem;">Logistics Agent</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Lead Time & Expediting</div>
            <div style="font-size: 0.7rem; color: #34d399; margin-top: 4px;">● COMPLETED</div>
        </div>
        <div style="color: #64748b; font-weight: bold; font-size: 1.2rem;">➔</div>
        <div style="text-align: center; flex: 1.2; min-width: 150px; background: rgba(168, 85, 247, 0.15); border: 1px solid #a855f7; padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #c084fc; font-weight: 700;">COORDINATION</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 0.95rem;">Coordinator Agent</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Conflict Gating & Solver</div>
            <div style="font-size: 0.7rem; color: #34d399; margin-top: 4px;">● PLAN SYNTHESIZED</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Agent Inspector Tabs
st.markdown("### 🔍 Specialized Agent Telemetry Inspector")
tab_dem, tab_inv, tab_sup, tab_log, tab_coord = st.tabs([
    "1. 📊 Demand Agent",
    "2. 📦 Inventory Agent",
    "3. 🏭 Supplier Risk Agent",
    "4. 🚚 Logistics Agent",
    "5. 🧠 Coordinator Agent"
])

# 1. Demand Agent Tab
with tab_dem:
    d_data = agent_results["demand"]
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        st.markdown("#### 🎯 Role & Analysis Scope")
        st.write(
            "Analyzes customer demand across the 14-day planning horizon with special emphasis on "
            "the 7-day Supplier A shutdown period. Segregates customers by SLA penalty tier to prevent high-liability stockouts."
        )
        st.markdown("**Key Findings:**")
        st.json(d_data["findings"])
        
    with col_d2:
        st.markdown("#### 📈 Customer Tier Demand Breakdown")
        tier_list = d_data["findings"]["tier_summary"]
        df_tiers = pd.DataFrame(tier_list)
        fig_tier = px.pie(
            df_tiers, 
            values="units", 
            names="label", 
            color_discrete_sequence=["#ef4444", "#38bdf8", "#94a3b8"],
            hole=0.45
        )
        fig_tier.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=250, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_tier, use_container_width=True)
        
        st.markdown("#### 📜 Formal Proposal Output")
        prop = d_data["proposal"]
        st.markdown(f"**Confidence:** `{int(prop.confidence_score*100)}%` | **Action:** `{prop.action_type}`")
        st.info(prop.rationale)

# 2. Inventory Agent Tab
with tab_inv:
    i_data = agent_results["inventory"]
    col_i1, col_i2 = st.columns([1, 1])
    with col_i1:
        st.markdown("#### 📦 Runway & Buffer Health")
        st.write(
            "Evaluates current on-hand inventory of MCU-900 at Central Assembly Plant Alpha. "
            "Calculates daily consumption rate, safety-stock depletion curve, and line starvation threshold."
        )
        st.markdown("**Inventory Telemetry:**")
        st.json(i_data["findings"])
        
    with col_i2:
        st.markdown("#### 📉 Stock Depletion Trajectory (Runout Analysis)")
        # Trajectory chart without intervention
        days = list(range(1, 9))
        stock_trajectory = [max(0, 900 - (d * 430)) for d in days]
        fig_traj = go.Figure()
        fig_traj.add_trace(go.Scatter(x=days, y=stock_trajectory, mode="lines+markers", line=dict(color="#f87171", width=3), name="Buffer MCU-900"))
        fig_traj.add_hline(y=450, line_dash="dash", line_color="#fbbf24", annotation_text="Safety Stock Threshold (450)")
        fig_traj.add_vline(x=2.08, line_dash="dot", line_color="#ef4444", annotation_text="Starvation Day (2.08)")
        fig_traj.update_layout(
            title="Plant Alpha Inventory Depletion (Zero Inbound Scenario)",
            xaxis_title="Planning Day",
            yaxis_title="Units On-Hand",
            height=280,
            margin=dict(l=10, r=10, t=30, b=10),
            plot_bgcolor="rgba(15, 23, 42, 0.4)",
            paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_traj, use_container_width=True)
        
        prop_inv = i_data["proposal"]
        st.markdown(f"**Confidence:** `{int(prop_inv.confidence_score*100)}%` | **Action:** `{prop_inv.action_type}`")
        st.error(prop_inv.rationale)

# 3. Supplier Risk Agent Tab
with tab_sup:
    s_data = agent_results["supplier_risk"]
    col_s1, col_s2 = st.columns([1, 1])
    with col_s1:
        st.markdown("#### 🏭 Backup Supplier Qualification & Risk")
        st.write(
            "Screens registered alternate vendors capable of supplying MCU-900. "
            "Evaluates unit cost premiums, available daily production headroom, and historical reliability."
        )
        st.json(s_data["findings"])
        
    with col_s2:
        st.markdown("#### ⚖️ Supplier Comparison Matrix")
        cand_df = pd.DataFrame(s_data["findings"]["candidates"])
        st.dataframe(
            cand_df[["name", "daily_capacity", "unit_cost", "cost_premium_pct", "reliability_score", "composite_qualification_score"]],
            hide_index=True,
            use_container_width=True
        )
        
        prop_sup = s_data["proposal"]
        st.markdown(f"**Confidence:** `{int(prop_sup.confidence_score*100)}%` | **Action:** `{prop_sup.action_type}`")
        st.success(prop_sup.rationale)

# 4. Logistics Agent Tab
with tab_log:
    l_data = agent_results["logistics"]
    col_l1, col_l2 = st.columns([1, 1])
    with col_l1:
        st.markdown("#### 🚚 Freight Mode & Lead Time Feasibility")
        st.write(
            "Compares standard ground/ocean freight versus expedited air cargo. "
            "Cross-references transit lead times against the Day 2.08 inventory starvation deadline."
        )
        st.json(l_data["findings"])
        
    with col_l2:
        st.markdown("#### ⏱️ Transit Lead Time vs Runout Deadline")
        lanes_df = pd.DataFrame(l_data["findings"]["lanes"])
        fig_lead = px.bar(
            lanes_df,
            x="name",
            y=["std_lead_time_days", "exp_lead_time_days"],
            barmode="group",
            labels={"value": "Lead Time (Days)", "variable": "Freight Mode", "name": "Supplier"},
            color_discrete_map={"std_lead_time_days": "#64748b", "exp_lead_time_days": "#38bdf8"}
        )
        fig_lead.add_hline(y=2.08, line_dash="dash", line_color="#f87171", annotation_text="Plant Runout Deadline (2.08d)")
        fig_lead.update_layout(height=260, margin=dict(l=10, r=10, t=20, b=10), plot_bgcolor="rgba(15, 23, 42, 0.4)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_lead, use_container_width=True)
        
        prop_log = l_data["proposal"]
        st.markdown(f"**Confidence:** `{int(prop_log.confidence_score*100)}%` | **Action:** `{prop_log.action_type}`")
        st.warning(prop_log.rationale)

# 5. Coordinator Agent Tab
with tab_coord:
    st.markdown("#### 🧠 Conflict Resolution & Multi-Objective Synthesis")
    st.write(
        "The Coordinator Agent acts as the central orchestrator. It collects all individual proposals, "
        "identifies conflicting goals, resolves them via business priorities, and invokes the mathematical optimization solver."
    )
    
    st.markdown("##### ⚡ Resolved Conflicts Between Agents:")
    for c in wf["conflicts_resolved"]:
        with st.container(border=True):
            st.markdown(f"**Conflict:** `{c['conflict']}`")
            st.caption(f"Agents Involved: {', '.join(c['agents_involved'])}")
            st.markdown(f"**Problem:** {c['issue']}")
            st.markdown(f"**Coordinator Resolution:** ✅ {c['resolution']}")
            
    st.markdown("##### 📋 Consolidated Action Plan Payload (JSON Schema)")
    prop_coord = wf["recovery_plan"].executive_summary
    st.info(prop_coord)
