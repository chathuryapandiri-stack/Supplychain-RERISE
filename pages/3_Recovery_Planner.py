"""
ResilientAI - Page 3: Recovery Planner (Generating the Final Recovery Plan)
Actionable mitigation plan, multi-supplier allocations, cost breakdown, constraint validations, and HITL approval.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from core.state import init_session_state, record_audit
from core.ui_components import apply_custom_css, render_metric_card

st.set_page_config(page_title="Recovery Planner | ResilientAI", layout="wide")
apply_custom_css()
init_session_state()

st.markdown('<div class="hero-badge">PAGE 3 • RECOVERY PLANNER</div>', unsafe_allow_html=True)
st.title("Autonomous Recovery Plan & Execution")
st.caption("Actionable multi-sourcing allocations, freight schedules, constraint validation, and human planner approval.")

plan = st.session_state.recovery_plan
scenario = st.session_state.active_scenario

# Executive Summary
st.info(f"**Coordinator Strategy Synthesis**: {plan.executive_summary}")

# High-Level Metrics
m1, m2, m3, m4 = st.columns(4)
with m1:
    render_metric_card("Service Fulfillment", f"{plan.fulfillment_rate}%", "Tier 1: 100% Guaranteed", "green")
with m2:
    render_metric_card("Total Landed Cost", f"${plan.total_landed_cost:,.0f}", f"Purchasing: ${plan.total_material_cost:,.0f}", "blue")
with m3:
    render_metric_card("Unmet Backorders", f"{plan.unmet_demand_units} Units", "Deferred non-critical Tier 3", "green" if plan.unmet_demand_units < 100 else "amber")
with m4:
    render_metric_card("Recovery Horizon", f"{plan.recovery_time_days} Days", "Full stock stabilization", "blue")

st.markdown("<br>", unsafe_allow_html=True)

# Sourcing Allocation Table and Cost Breakdown
col_alloc, col_cost = st.columns([3, 2])

with col_alloc:
    with st.container(border=True):
        st.markdown("#### Recommended Purchase & Dispatch Schedule")
        st.caption("Volume allocations split between backup vendors to satisfy demand and avoid single-vendor bottlenecks.")
        
        alloc_table = []
        for a in plan.allocations:
            alloc_table.append({
                "Supplier": a.supplier_name,
                "Shipping Mode": "Air Expedited" if "EXPEDITED" in a.shipping_mode else "Standard Freight",
                "Allocated Units": f"{a.allocated_units:,}",
                "Lead Time": f"{a.lead_time_days} Days",
                "Arrival Day": f"Day {a.arrival_day}",
                "Unit Price": f"${a.unit_cost:.2f}",
                "Freight / Unit": f"${a.freight_cost_per_unit:.2f}",
                "Total PO Spend": f"${a.total_cost:,.2f}"
            })
        st.dataframe(pd.DataFrame(alloc_table), hide_index=True, use_container_width=True)

with col_cost:
    with st.container(border=True):
        st.markdown("#### Landed Cost Decomposition")
        cost_df = pd.DataFrame([
            {"Category": "Material Purchasing", "Amount": plan.total_material_cost},
            {"Category": "Freight & Expedite", "Amount": plan.total_freight_cost},
            {"Category": "Inventory Holding", "Amount": plan.total_holding_cost},
            {"Category": "Backorder SLA Penalties", "Amount": plan.total_backorder_penalty}
        ])
        fig_cost = px.pie(
            cost_df,
            values="Amount",
            names="Category",
            hole=0.45,
            color_discrete_sequence=["#38bdf8", "#f59e0b", "#64748b", "#f43f5e"]
        )
        fig_cost.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=260, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_cost, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Constraint Validation Section
st.markdown("### Hard Constraint & SLA Validation Engine")
st.caption("Verifies mathematical bounds, supplier physical capacity, lead-time feasibility, and budget ceilings.")

c_cols = st.columns(len(plan.constraints_status))
for idx, c in enumerate(plan.constraints_status):
    with c_cols[idx]:
        with st.container(border=True):
            badge_class = "badge-passed" if c.status == "PASSED" else ("badge-warning" if c.status == "WARNING" else "badge-violated")
            st.markdown(f'<span class="{badge_class}">{c.status}</span>', unsafe_allow_html=True)
            st.markdown(f"**{c.constraint_name}**")
            st.caption(c.message)
            st.markdown(f"<span style='font-size:0.8rem; color:#94a3b8;'>Value: <b>{c.metric_value}</b><br>Threshold: <b>{c.threshold}</b></span>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Human-in-the-Loop Planner Decision Form
st.markdown("### Human-in-the-Loop (HITL) Planner Approval Gating")
st.caption("ResilientAI requires explicit human authorization before executing supplier allocations into the enterprise ERP.")

with st.container(border=True):
    current_status = st.session_state.plan_approval_status
    status_color = "#10b981" if current_status == "APPROVED" else ("#ef4444" if current_status == "REJECTED" else "#f59e0b")
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div>
            <span style="font-weight: 700; color: #f8fafc; font-size: 1.1rem;">Current Status: </span>
            <span style="color: {status_color}; font-weight: 800; font-size: 1.1rem; border: 1px solid {status_color}; padding: 2px 10px; border-radius: 6px;">
                {current_status.replace('_', ' ')}
            </span>
        </div>
        <div style="font-size: 0.85rem; color: #94a3b8;">
            Audit-tracked action • Immutable log
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        planner_name = st.text_input("Planner Name / Badge ID", value="Lead Planner (Operations)")
    with col_p2:
        approval_notes = st.text_input("Decision Notes / Rationale", value="Approved dual-sourcing allocation with Phase 1 air expediting to prevent plant starvation.")
        
    btn_approve, btn_reject, _ = st.columns([1, 1, 2])
    with btn_approve:
        if st.button("Approve Recovery Plan", use_container_width=True, type="primary"):
            st.session_state.plan_approval_status = "APPROVED"
            record_audit("PLAN_APPROVED", planner_name, approval_notes)
            st.toast("Recovery plan approved and logged to audit trail!")
            st.rerun()
            
    with btn_reject:
        if st.button("Reject Plan (Request Revision)", use_container_width=True):
            st.session_state.plan_approval_status = "REJECTED"
            record_audit("PLAN_REJECTED", planner_name, approval_notes)
            st.toast("Plan rejected. Revision requested.")
            st.rerun()
