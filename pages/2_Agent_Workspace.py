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
# FLOATING LEVITATING AI CHATBOT WIDGET (BOTTOM-LEFT CORNER)
# =========================================================================
if "floating_chat_open" not in st.session_state:
    st.session_state.floating_chat_open = False

if "agent_chat_history" not in st.session_state:
    st.session_state.agent_chat_history = [
        {
            "role": "assistant",
            "content": (
                "Hello Planner. I am your ResilientAI Strategy Copilot powered by Groq LLM intelligence. "
                "I have real-time visibility into plant buffer runway, supplier daily capacities, and optimal recovery purchase allocations. "
                "How can I assist your supply chain decisions today?"
            )
        }
    ]

# Floating Widget Styling
st.markdown("""
<style>
/* Levitating Animation for Floating Button */
@keyframes levitate-float {
    0% {
        transform: translateY(0px) scale(1);
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.5), 0 0 16px rgba(168, 85, 247, 0.4);
    }
    50% {
        transform: translateY(-9px) scale(1.02);
        box-shadow: 0 20px 36px rgba(124, 58, 237, 0.8), 0 0 28px rgba(168, 85, 247, 0.65);
    }
    100% {
        transform: translateY(0px) scale(1);
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.5), 0 0 16px rgba(168, 85, 247, 0.4);
    }
}

/* Floating Action Button (FAB) Anchor */
div[data-testid="stVerticalBlock"]:has(> div .floating-fab-marker) {
    position: fixed !important;
    bottom: 24px !important;
    left: 24px !important;
    z-index: 999999 !important;
    width: auto !important;
    margin: 0 !important;
    padding: 0 !important;
}

div[data-testid="stVerticalBlock"]:has(> div .floating-fab-marker) button {
    width: 62px !important;
    height: 62px !important;
    min-width: 62px !important;
    border-radius: 50% !important;
    background: linear-gradient(135deg, #a855f7 0%, #7c3aed 50%, #4f46e5 100%) !important;
    border: 2.5px solid rgba(255, 255, 255, 0.45) !important;
    color: transparent !important;
    animation: levitate-float 3s ease-in-out infinite !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    padding: 0 !important;
    background-repeat: no-repeat !important;
    background-position: center !important;
    background-size: 28px 28px !important;
}

div[data-testid="stVerticalBlock"]:has(> div .floating-fab-marker.closed) button {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2.2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z'%3E%3C/path%3E%3C/svg%3E") !important;
}

div[data-testid="stVerticalBlock"]:has(> div .floating-fab-marker.opened) button {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='26' height='26' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cline x1='18' y1='6' x2='6' y2='18'%3E%3C/line%3E%3Cline x1='6' y1='6' x2='18' y2='18'%3E%3C/line%3E%3C/svg%3E") !important;
}

div[data-testid="stVerticalBlock"]:has(> div .floating-fab-marker) button:hover {
    transform: scale(1.1) !important;
    animation-play-state: paused !important;
}

/* Floating Popup Container */
div[data-testid="stVerticalBlock"]:has(> div .floating-popup-marker) {
    position: fixed !important;
    bottom: 96px !important;
    left: 24px !important;
    z-index: 999998 !important;
    width: 395px !important;
    max-width: calc(100vw - 48px) !important;
    height: 560px !important;
    max-height: calc(100vh - 120px) !important;
    background: #0f172a !important;
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    border-radius: 20px !important;
    box-shadow: 0 25px 60px -10px rgba(0, 0, 0, 0.9), 0 0 35px rgba(124, 58, 237, 0.35) !important;
    display: flex !important;
    flex-direction: column !important;
    overflow: hidden !important;
    animation: popup-fly-in 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    padding: 0 !important;
}

@keyframes popup-fly-in {
    from {
        opacity: 0;
        transform: translateY(24px) scale(0.92);
    }
    to {
        opacity: 1;
        transform: translateY(0px) scale(1);
    }
}

.chat-bubble-assistant {
    background: rgba(30, 41, 59, 0.92);
    border: 1px solid rgba(51, 65, 85, 0.7);
    border-radius: 16px 16px 16px 4px;
    color: #f1f5f9;
    padding: 10px 14px;
    font-size: 0.83rem;
    line-height: 1.45;
    margin-bottom: 10px;
    max-width: 90%;
    align-self: flex-start;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    border-radius: 16px 16px 4px 16px;
    color: #ffffff;
    padding: 10px 14px;
    font-size: 0.83rem;
    line-height: 1.45;
    margin-bottom: 10px;
    max-width: 85%;
    align-self: flex-end;
    margin-left: auto;
}
</style>
""", unsafe_allow_html=True)

# 1. Render Floating Popup Card (When Open)
if st.session_state.floating_chat_open:
    with st.container():
        st.markdown('<div class="floating-popup-marker"></div>', unsafe_allow_html=True)
        
        # Header banner matching reference GIF
        st.markdown("""
        <div style="background: linear-gradient(135deg, #a855f7 0%, #7c3aed 50%, #4f46e5 100%); padding: 12px 16px; display: flex; align-items: center; justify-content: space-between; border-top-left-radius: 20px; border-top-right-radius: 20px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="position: relative; width: 38px; height: 38px; border-radius: 50%; background: rgba(255, 255, 255, 0.2); display: flex; align-items: center; justify-content: center; border: 1.5px solid rgba(255, 255, 255, 0.5);">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="3" y="11" width="18" height="10" rx="2"></rect>
                        <circle cx="12" cy="5" r="2"></circle>
                        <path d="M12 7v4"></path>
                        <line x1="8" y1="16" x2="8" y2="16"></line>
                        <line x1="16" y1="16" x2="16" y2="16"></line>
                    </svg>
                    <div style="position: absolute; bottom: 0; right: 0; width: 10px; height: 10px; background: #22c55e; border-radius: 50%; border: 2px solid #7c3aed; box-shadow: 0 0 6px #22c55e;"></div>
                </div>
                <div>
                    <div style="color: white; font-weight: 700; font-size: 0.95rem; line-height: 1.2;">ResilientAI Copilot</div>
                    <div style="color: rgba(255, 255, 255, 0.85); font-size: 0.72rem; line-height: 1;">Strategy Advisor • Online</div>
                </div>
            </div>
            <div style="font-size: 0.8rem; color: rgba(255,255,255,0.7); font-weight: 600;">Groq LLM</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Scrollable conversation thread
        chat_html_pieces = [
            '<div style="height: 290px; overflow-y: auto; padding: 12px 14px; display: flex; flex-direction: column; background: #0b1120;">'
        ]
        for msg in st.session_state.agent_chat_history:
            bubble_class = "chat-bubble-assistant" if msg["role"] == "assistant" else "chat-bubble-user"
            # Format markdown linebreaks
            formatted_text = msg["content"].replace("\n", "<br>")
            chat_html_pieces.append(f'<div class="{bubble_class}">{formatted_text}</div>')
        chat_html_pieces.append('</div>')
        st.markdown("".join(chat_html_pieces), unsafe_allow_html=True)
        
        # Quick Chips in small container
        chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)
        quick_query = None
        with chip_col1:
            if st.button("Optimal Plan", key="chip_opt", use_container_width=True):
                quick_query = "Summarize the optimal multi-agent recovery plan and allocations."
        with chip_col2:
            if st.button("Air Transit", key="chip_air", use_container_width=True):
                quick_query = "Why did logistics prioritize air expediting over standard freight?"
        with chip_col3:
            if st.button("Vendor Split", key="chip_split", use_container_width=True):
                quick_query = "Why is volume split between backup vendors instead of single-sourcing?"
        with chip_col4:
            if st.button("Clear", key="chip_clear", use_container_width=True):
                st.session_state.agent_chat_history = [
                    {
                        "role": "assistant",
                        "content": "Conversation reset. How can I assist with your supply chain decisions?"
                    }
                ]
                st.rerun()
                
        # Footer input form matching reference GIF ("Type a message...")
        with st.form("floating_chat_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns([4, 1])
            with f_col1:
                user_msg = st.text_input(
                    "Message",
                    placeholder="Type a message...",
                    label_visibility="collapsed"
                )
            with f_col2:
                send_pressed = st.form_submit_button("Send", use_container_width=True)
                
        active_query = quick_query or (user_msg if send_pressed and user_msg else None)
        if active_query:
            st.session_state.agent_chat_history.append({"role": "user", "content": active_query})
            from core.llm_service import query_chat_copilot
            session_ctx = {
                "active_scenario": st.session_state.active_scenario,
                "recovery_plan": st.session_state.recovery_plan,
                "suppliers_df": st.session_state.suppliers_df,
                "inventory_df": st.session_state.inventory_df,
                "demand_df": st.session_state.demand_df,
                "benchmark_results": st.session_state.benchmark_results,
                "workflow_execution": st.session_state.workflow_execution,
                "active_preset_name": st.session_state.get("active_preset_name", "Active Supply Chain Network")
            }
            ai_resp = query_chat_copilot(
                user_query=active_query,
                chat_history=st.session_state.agent_chat_history[:-1],
                session_state_dict=session_ctx
            )
            st.session_state.agent_chat_history.append({"role": "assistant", "content": ai_resp})
            st.rerun()

# 2. Render Floating Circular Levitating Action Button (FAB) at Bottom-Left
with st.container():
    fab_status_class = "opened" if st.session_state.floating_chat_open else "closed"
    st.markdown(f'<div class="floating-fab-marker {fab_status_class}"></div>', unsafe_allow_html=True)
    if st.button(" ", key="floating_fab_btn_toggle", help="ResilientAI Copilot Chat"):
        st.session_state.floating_chat_open = not st.session_state.floating_chat_open
        st.rerun()


