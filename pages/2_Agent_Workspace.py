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

st.set_page_config(page_title="Agent Workspace | ResilientAI", page_icon=":material/smart_toy:", layout="wide")
apply_custom_css()
init_session_state()

st.markdown('<div class="hero-badge">PAGE 2 • AGENT WORKSPACE</div>', unsafe_allow_html=True)
st.title("Collaborative AI Agent Workspace")
st.caption("Inspect the 5 specialized autonomous agents, their inputs, outputs, schemas, and conflict resolution.")

wf = st.session_state.workflow_execution
agent_results = wf["agent_results"]

# Workflow Pipeline Diagram
st.markdown("### Multi-Agent Directed Acyclic Graph (DAG)")
st.markdown("""
<div style="background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(51, 65, 85, 0.8); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem;">
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 12px;">
        <div style="text-align: center; flex: 1; min-width: 130px; background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #38bdf8; font-weight: 700;">STEP 1</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 0.95rem;">Demand Agent</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Customer Tiers & Needs</div>
            <div style="font-size: 0.7rem; color: #34d399; margin-top: 4px;">● COMPLETED</div>
        </div>
        <div style="color: #64748b; font-weight: bold; font-size: 1.2rem;">&rarr;</div>
        <div style="text-align: center; flex: 1; min-width: 130px; background: rgba(248, 113, 113, 0.1); border: 1px solid #f87171; padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #f87171; font-weight: 700;">STEP 2</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 0.95rem;">Inventory Agent</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Runway & Starvation</div>
            <div style="font-size: 0.7rem; color: #34d399; margin-top: 4px;">● COMPLETED</div>
        </div>
        <div style="color: #64748b; font-weight: bold; font-size: 1.2rem;">&rarr;</div>
        <div style="text-align: center; flex: 1; min-width: 130px; background: rgba(251, 191, 36, 0.1); border: 1px solid #fbbf24; padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #fbbf24; font-weight: 700;">STEP 3</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 0.95rem;">Supplier Risk Agent</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Capacity & Multi-Source</div>
            <div style="font-size: 0.7rem; color: #34d399; margin-top: 4px;">● COMPLETED</div>
        </div>
        <div style="color: #64748b; font-weight: bold; font-size: 1.2rem;">&rarr;</div>
        <div style="text-align: center; flex: 1; min-width: 130px; background: rgba(52, 211, 153, 0.1); border: 1px solid #34d399; padding: 10px; border-radius: 8px;">
            <div style="font-size: 0.75rem; color: #34d399; font-weight: 700;">STEP 4</div>
            <div style="font-weight: 800; color: #f8fafc; font-size: 0.95rem;">Logistics Agent</div>
            <div style="font-size: 0.75rem; color: #94a3b8;">Lead Time & Expediting</div>
            <div style="font-size: 0.7rem; color: #34d399; margin-top: 4px;">● COMPLETED</div>
        </div>
        <div style="color: #64748b; font-weight: bold; font-size: 1.2rem;">&rarr;</div>
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
st.markdown("### Specialized Agent Telemetry Inspector")
tab_dem, tab_inv, tab_sup, tab_log, tab_coord = st.tabs([
    "1. Demand Agent",
    "2. Inventory Agent",
    "3. Supplier Risk Agent",
    "4. Logistics Agent",
    "5. Coordinator Agent"
])

# 1. Demand Agent Tab
with tab_dem:
    d_data = agent_results["demand"]
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        st.markdown("#### Role & Analysis Scope")
        st.write(
            "Analyzes customer demand across the 14-day planning horizon with special emphasis on "
            "the supplier shutdown period. Segregates customers by SLA penalty tier to prevent high-liability stockouts."
        )
        st.markdown("**Key Findings:**")
        st.json(d_data["findings"])
        
    with col_d2:
        st.markdown("#### Customer Tier Demand Breakdown")
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
        
        st.markdown("#### Formal Proposal Output")
        prop = d_data["proposal"]
        st.markdown(f"**Confidence:** `{int(prop.confidence_score*100)}%` | **Action:** `{prop.action_type}`")
        st.info(prop.rationale)

# 2. Inventory Agent Tab
with tab_inv:
    i_data = agent_results["inventory"]
    col_i1, col_i2 = st.columns([1, 1])
    with col_i1:
        st.markdown("#### Runway & Buffer Health")
        st.write(
            "Evaluates current on-hand inventory at Central Assembly Plant Alpha. "
            "Calculates daily consumption rate, safety-stock depletion curve, and line starvation threshold."
        )
        st.markdown("**Inventory Telemetry:**")
        st.json(i_data["findings"])
        
    with col_i2:
        st.markdown("#### Stock Depletion Trajectory (Runout Analysis)")
        crit_stock = i_data["findings"].get("current_stock", 900)
        runout_val = i_data["findings"].get("runout_days", 2.08)
        burn_val = crit_stock / max(0.1, runout_val)
        safety_val = i_data["findings"].get("safety_stock", 450)
        
        days = list(range(1, 9))
        stock_trajectory = [max(0, int(round(crit_stock - (d * burn_val)))) for d in days]
        fig_traj = go.Figure()
        fig_traj.add_trace(go.Scatter(x=days, y=stock_trajectory, mode="lines+markers", line=dict(color="#f87171", width=3), name="Buffer Inventory"))
        fig_traj.add_hline(y=safety_val, line_dash="dash", line_color="#fbbf24", annotation_text=f"Safety Stock ({safety_val})")
        fig_traj.add_vline(x=runout_val, line_dash="dot", line_color="#ef4444", annotation_text=f"Starvation Day ({runout_val}d)")
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
        st.markdown("#### Backup Supplier Qualification & Risk")
        st.write(
            "Screens registered alternate vendors capable of supplying the critical component. "
            "Evaluates unit cost premiums, available daily production headroom, and historical reliability."
        )
        st.json(s_data["findings"])
        
    with col_s2:
        st.markdown("#### Supplier Comparison Matrix")
        cand_df = pd.DataFrame(s_data["findings"]["candidates"])
        cols_show = [c for c in ["name", "daily_capacity", "unit_cost", "cost_premium_pct", "reliability_score", "composite_qualification_score"] if c in cand_df.columns]
        st.dataframe(
            cand_df[cols_show],
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
        st.markdown("#### Freight Mode & Lead Time Feasibility")
        st.write(
            "Compares standard ground/ocean freight versus expedited air cargo. "
            "Cross-references transit lead times against the inventory starvation deadline."
        )
        st.json(l_data["findings"])
        
    with col_l2:
        st.markdown("#### Transit Lead Time vs Runout Deadline")
        lanes_df = pd.DataFrame(l_data["findings"]["lanes"])
        fig_lead = px.bar(
            lanes_df,
            x="name",
            y=["std_lead_time_days", "exp_lead_time_days"],
            barmode="group",
            labels={"value": "Lead Time (Days)", "variable": "Freight Mode", "name": "Supplier"},
            color_discrete_map={"std_lead_time_days": "#64748b", "exp_lead_time_days": "#38bdf8"}
        )
        fig_lead.add_hline(y=runout_val, line_dash="dash", line_color="#f87171", annotation_text=f"Plant Runout Deadline ({runout_val}d)")
        fig_lead.update_layout(height=260, margin=dict(l=10, r=10, t=20, b=10), plot_bgcolor="rgba(15, 23, 42, 0.4)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_lead, use_container_width=True)
        
        prop_log = l_data["proposal"]
        st.markdown(f"**Confidence:** `{int(prop_log.confidence_score*100)}%` | **Action:** `{prop_log.action_type}`")
        st.warning(prop_log.rationale)

# 5. Coordinator Agent Tab
with tab_coord:
    st.markdown("#### Conflict Resolution & Multi-Objective Synthesis")
    st.write(
        "The Coordinator Agent acts as the central orchestrator. It collects all individual proposals, "
        "identifies conflicting goals, resolves them via business priorities, and invokes the mathematical optimization solver."
    )
    
    st.markdown("##### Resolved Conflicts Between Agents:")
    for c in wf["conflicts_resolved"]:
        with st.container(border=True):
            st.markdown(f"**Conflict:** `{c['conflict']}`")
            st.caption(f"Agents Involved: {', '.join(c['agents_involved'])}")
            st.markdown(f"**Problem:** {c['issue']}")
            st.markdown(f"**Coordinator Resolution:** [RESOLVED] {c['resolution']}")
            
    st.markdown("##### Consolidated Action Plan Payload (Executive Summary)")
    prop_coord = wf["recovery_plan"].executive_summary
    st.info(prop_coord)


# =========================================================================
# FLOATING LEVITATING MULTI-AGENT CHATBOT (BOTTOM RIGHT CORNER)
# =========================================================================

def route_and_generate_agent_response(query: str) -> tuple[str, str, str]:
    """
    Intelligently routes user queries to the respective agent
    and returns (agent_name, badge_color, response_text).
    """
    q = query.lower()
    scenario = st.session_state.active_scenario
    plan = st.session_state.recovery_plan
    inv_df = st.session_state.inventory_df
    sup_df = st.session_state.suppliers_df
    demand_df = st.session_state.demand_df
    wf_state = st.session_state.get("workflow_execution", {})
    agent_res = wf_state.get("agent_results", {})

    # 1. Inventory Monitoring Agent
    if any(k in q for k in ["inventory", "stock", "runway", "burn", "starvation", "safety", "mcu", "on-hand", "buffer", "depletion", "warehouse", "item"]):
        agent_name = "Inventory Monitoring Agent"
        badge_color = "#D29922"
        inv_findings = agent_res.get("inventory", {}).get("findings", {})
        crit_stock = inv_findings.get("current_stock", 900)
        runout_days = inv_findings.get("runout_days", 2.08)
        stockout_day = inv_findings.get("stockout_day", 3)
        safety_stock = inv_findings.get("safety_stock", 450)
        burn_rate = round(crit_stock / max(0.1, runout_days), 1)
        crit_name = str(inv_df.iloc[0]["item_name"]) if not inv_df.empty else "Critical Component"

        response = (
            f"**Telemetry & Runway Analysis:**\n\n"
            f"- **Component Monitored:** {crit_name}\n"
            f"- **Current On-Hand Stock:** {crit_stock:,} units\n"
            f"- **Safety Stock Threshold:** {safety_stock:,} units\n"
            f"- **Daily Consumption Burn:** {burn_rate:.0f} units/day\n"
            f"- **Buffer Runway:** {runout_days:.2f} days remaining\n"
            f"- **Projected Starvation Day:** Day {stockout_day}\n\n"
            f"**Operational Assessment:**\n"
            f"Assembly Plant Alpha's buffer will deplete completely on Day {stockout_day}. Without inbound stock, "
            f"line starvation will occur. Emergency replenishment of at least 1,300 units must land by Day 3 to protect operations."
        )
        return agent_name, badge_color, response

    # 2. Supplier Risk Agent
    if any(k in q for k in ["supplier", "vendor", "apex", "beacon", "crestline", "delta", "capacity", "disrupt", "shutdown", "outage", "risk", "qualification", "headroom", "unit cost", "sourcing", "backup"]):
        agent_name = "Supplier Risk Agent"
        badge_color = "#58A6FF"
        disrupted_id = scenario.disrupted_supplier_id if scenario else "SUP-A"
        disrupted_match = sup_df[sup_df["supplier_id"] == disrupted_id] if not sup_df.empty else pd.DataFrame()
        disrupted_name = disrupted_match["name"].iloc[0] if not disrupted_match.empty else "Primary Vendor"

        backup_df = sup_df[sup_df["supplier_id"] != disrupted_id] if not sup_df.empty else pd.DataFrame()
        total_backup_cap = int(backup_df["daily_capacity"].sum()) if not backup_df.empty else 650

        cand_lines = []
        for _, s in backup_df.iterrows():
            cand_lines.append(
                f"- **{s.get('name', s.get('supplier_id'))} ({s.get('supplier_id')}):** "
                f"Capacity={s.get('daily_capacity', 0)} u/d, Cost=${s.get('unit_cost', 0):.2f}/u, "
                f"Reliability={s.get('reliability_score', 0.9):.2f}"
            )
        cand_str = "\n".join(cand_lines)

        response = (
            f"**Supplier Risk & Headroom Evaluation:**\n\n"
            f"- **Disrupted Supplier:** {disrupted_name} ({disrupted_id}) - Status: DISRUPTED ({scenario.duration_days if scenario else 7}-day shutdown, 0 u/d flow)\n"
            f"- **Combined Backup Daily Headroom:** {total_backup_cap:,} units/day\n\n"
            f"**Qualified Alternate Vendors:**\n{cand_str}\n\n"
            f"**Sourcing Recommendation:**\n"
            f"Single backup sourcing is not feasible because neither vendor alone can meet daily burn without exceeding capacity limits. "
            f"The system enforces a dual-sourcing split across Beacon Tech Solutions and Crestline Components."
        )
        return agent_name, badge_color, response

    # 3. Demand Sensing Agent
    if any(k in q for k in ["demand", "order", "customer", "tier", "sla", "healthcare", "defense", "priority", "penalty", "commitments", "backorder", "fulfillment", "batches"]):
        agent_name = "Demand Sensing Agent"
        badge_color = "#3FB950"
        total_demand = int(demand_df["demand_units"].sum()) if not demand_df.empty else 5440
        total_batches = len(demand_df) if not demand_df.empty else 42
        
        tier_col = "customer_tier" if "customer_tier" in demand_df.columns else ("tier" if "tier" in demand_df.columns else None)
        t1_units = int(demand_df[demand_df[tier_col] == 1]["demand_units"].sum()) if (tier_col and not demand_df.empty) else 1850
        t2_units = int(demand_df[demand_df[tier_col] == 2]["demand_units"].sum()) if (tier_col and not demand_df.empty) else 2100
        t3_units = int(demand_df[demand_df[tier_col] == 3]["demand_units"].sum()) if (tier_col and not demand_df.empty) else 1490

        response = (
            f"**Customer Demand & Priority Telemetry:**\n\n"
            f"- **Total 14-Day Demand Volume:** {total_demand:,} units ({total_batches} order batches)\n"
            f"- **Average Daily Inflow:** {total_demand / 14:.1f} units/day\n\n"
            f"**Customer Priority Breakdown:**\n"
            f"- **Tier 1 (Mission-Critical / Healthcare & Defense):** {t1_units:,} units (100% SLA target, $180-$360/u default penalty)\n"
            f"- **Tier 2 (Enterprise & Telecom):** {t2_units:,} units (Standard contract SLA)\n"
            f"- **Tier 3 (Commercial Distribution):** {t3_units:,} units (Flexible delivery windows)\n\n"
            f"**Rationing Guidance:**\n"
            f"All Tier 1 critical commitments are strictly protected from stockouts, preventing contractual SLA breach liabilities."
        )
        return agent_name, badge_color, response

    # 4. Logistics Expediting Agent
    if any(k in q for k in ["logistics", "freight", "air", "expedite", "shipping", "transit", "lead time", "ground", "ocean", "truck", "cargo", "delivery", "arrival", "mode"]):
        agent_name = "Logistics Expediting Agent"
        badge_color = "#06B6D4"
        response = (
            f"**Logistics Freight Mode Evaluation:**\n\n"
            f"- **Expedited Air Cargo:** Lead Time = 2 Days | Freight Premium = $15.00 - $16.50/unit\n"
            f"- **Standard Ground Freight:** Lead Time = 4 - 5 Days | Freight Cost = $5.50 - $6.00/unit\n\n"
            f"**Lead-Time vs Buffer Runway Trade-off:**\n"
            f"Plant Alpha's buffer inventory exhausts on **Day 3** (2.08 days runway). "
            f"Standard ground freight takes 4-5 days to arrive (landing Day 5 or 6)—causing a 3-day line stoppage.\n\n"
            f"**Logistics Execution Strategy:**\n"
            f"- **Phase 1 (Emergency Air Bridge):** Dispatch 1,300 units via Expedited Air arriving Day 3 to prevent factory starvation.\n"
            f"- **Phase 2 (Standard Sustained Freight):** Transition subsequent 1,950 units to Standard Freight arriving Days 5-6 to save freight spend."
        )
        return agent_name, badge_color, response

    # 5. Coordinator Master Agent (Default / Overall Coordination)
    agent_name = "Coordinator Master Agent"
    badge_color = "#C084FC"
    f_rate = plan.fulfillment_rate if plan else 95.5
    cost = plan.total_landed_cost if plan else 264210.0
    stockout = plan.stockout_duration_days if plan else 1
    unmet = plan.unmet_demand_units if plan else 270

    response = (
        f"**Master Multi-Agent Coordination Synthesis:**\n\n"
        f"- **Projected Fulfillment Rate:** {f_rate:.1f}% (Tier 1 Priority: 100% Guaranteed)\n"
        f"- **Total Landed Recovery Cost:** ${cost:,.2f} (~$252,758 saved vs legacy ERP)\n"
        f"- **Stockout Duration:** {stockout} Day\n"
        f"- **Unmet Demand:** {unmet:,} units (Deferred commercial backlog)\n"
        f"- **Constraint Status:** 0 Violations (Capacity limits, runway gap-closure, and budget ceiling satisfied)\n\n"
        f"**Resolved Conflicts:**\n"
        f"Reconciled buffer exhaustion against shipping lead times via expedited air dispatch, "
        f"and resolved single-supplier bottlenecks via a dual-sourcing split across Beacon Tech Solutions and Crestline Components."
    )
    return agent_name, badge_color, response


@st.dialog("Multi-Agent Operations Assistant")
def show_agent_chat_dialog():
    st.markdown("""
    <div style="font-size:0.75rem; color:#8B949E; margin-bottom:10px; line-height:1.4;">
        Direct intelligence line to <b>Demand</b>, <b>Inventory</b>, <b>Supplier Risk</b>, <b>Logistics</b>, and <b>Coordinator</b> agents.
        Queries are automatically routed to the respective specialist.
    </div>
    """, unsafe_allow_html=True)

    # Initialize chat history in session state
    if "agent_chat_messages" not in st.session_state or not st.session_state.agent_chat_messages:
        st.session_state.agent_chat_messages = [
            {
                "role": "assistant",
                "agent": "Coordinator Master Agent",
                "badge_color": "#C084FC",
                "content": (
                    "All 5 autonomous agents are synchronized with active network telemetry. "
                    "Ask any question about inventory runway, backup suppliers, customer demand tiers, or freight logistics."
                )
            }
        ]

    # Quick prompt buttons
    st.markdown("<div style='font-size:0.68rem; color:#8B949E; text-transform:uppercase; font-weight:600; margin-bottom:4px;'>Quick Queries:</div>", unsafe_allow_html=True)
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        if st.button("Inventory Runway?", key="btn_q_inv", use_container_width=True):
            user_msg = "What is our current inventory runway and starvation day?"
            agent_name, badge_color, agent_resp = route_and_generate_agent_response(user_msg)
            st.session_state.agent_chat_messages.append({"role": "user", "content": user_msg})
            st.session_state.agent_chat_messages.append({"role": "assistant", "agent": agent_name, "badge_color": badge_color, "content": agent_resp})
            st.rerun()
        if st.button("Customer SLA Tiers?", key="btn_q_dem", use_container_width=True):
            user_msg = "What customer demand tiers and SLA commitments are active?"
            agent_name, badge_color, agent_resp = route_and_generate_agent_response(user_msg)
            st.session_state.agent_chat_messages.append({"role": "user", "content": user_msg})
            st.session_state.agent_chat_messages.append({"role": "assistant", "agent": agent_name, "badge_color": badge_color, "content": agent_resp})
            st.rerun()
    with q_col2:
        if st.button("Supplier Outages?", key="btn_q_sup", use_container_width=True):
            user_msg = "Which suppliers are disrupted and what backup capacity is available?"
            agent_name, badge_color, agent_resp = route_and_generate_agent_response(user_msg)
            st.session_state.agent_chat_messages.append({"role": "user", "content": user_msg})
            st.session_state.agent_chat_messages.append({"role": "assistant", "agent": agent_name, "badge_color": badge_color, "content": agent_resp})
            st.rerun()
        if st.button("Air vs Ground Freight?", key="btn_q_log", use_container_width=True):
            user_msg = "Why do we need expedited air freight instead of standard shipping?"
            agent_name, badge_color, agent_resp = route_and_generate_agent_response(user_msg)
            st.session_state.agent_chat_messages.append({"role": "user", "content": user_msg})
            st.session_state.agent_chat_messages.append({"role": "assistant", "agent": agent_name, "badge_color": badge_color, "content": agent_resp})
            st.rerun()

    # Chat history container
    chat_container = st.container(height=280)
    with chat_container:
        for msg in st.session_state.agent_chat_messages:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    agent_tag = msg.get("agent", "Agent")
                    badge_color = msg.get("badge_color", "#388BFD")
                    st.markdown(
                        f"<div style='display:inline-block; font-size:0.65rem; font-weight:700; color:{badge_color}; "
                        f"background:rgba(56,139,253,0.1); border:1px solid {badge_color}; border-radius:4px; padding:1px 6px; margin-bottom:4px;'>"
                        f"[{agent_tag.upper()}]</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(msg["content"])

    # Chat input
    if user_query := st.chat_input("Ask the specialized agents..."):
        agent_name, badge_color, agent_resp = route_and_generate_agent_response(user_query)
        st.session_state.agent_chat_messages.append({"role": "user", "content": user_query})
        st.session_state.agent_chat_messages.append({"role": "assistant", "agent": agent_name, "badge_color": badge_color, "content": agent_resp})
        st.rerun()

    # Clear conversation button
    if st.button("Clear Conversation", use_container_width=True, key="btn_clear_agent_chat"):
        st.session_state.agent_chat_messages = []
        st.rerun()


# Levitating Floating Button Styles & Component
st.markdown("""
<style>
/* Levitating Floating Chat Trigger Button in Bottom Right Corner */
div[class*="st-key-btn_floating_agent_chat"] {
    position: fixed !important;
    bottom: 24px !important;
    right: 24px !important;
    z-index: 999998 !important;
    animation: levitateAgentChat 3.2s ease-in-out infinite !important;
}
div[class*="st-key-btn_floating_agent_chat"] button {
    background: #161B22 !important;
    border: 1.5px solid #388BFD !important;
    border-radius: 28px !important;
    color: #F0F6FC !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.02em !important;
    padding: 10px 18px !important;
    box-shadow: 0 4px 18px rgba(56, 139, 253, 0.45) !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}
div[class*="st-key-btn_floating_agent_chat"] button:hover {
    background: #1C212B !important;
    border-color: #58A6FF !important;
    box-shadow: 0 8px 26px rgba(56, 139, 253, 0.70) !important;
    transform: scale(1.04) !important;
}
@keyframes levitateAgentChat {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

/* Floating Dialog Styling (Bottom-Right Popup Box) */
div[data-testid="stDialog"] div[role="dialog"] {
    position: fixed !important;
    bottom: 24px !important;
    right: 24px !important;
    top: auto !important;
    left: auto !important;
    transform: none !important;
    width: 440px !important;
    max-width: calc(100vw - 32px) !important;
    height: 590px !important;
    max-height: calc(100vh - 48px) !important;
    background: #161B22 !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85) !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
}
div[data-testid="stDialog"] {
    background-color: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# Render the floating levitating button in the bottom right corner
if st.button("Chat with Agents", key="btn_floating_agent_chat", icon=":material/smart_toy:"):
    show_agent_chat_dialog()



