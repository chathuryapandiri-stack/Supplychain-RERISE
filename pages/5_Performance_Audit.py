"""
ResilientAI - Page 5: Performance & Audit (Measuring and Explaining Results)
Tri-way benchmark comparison against baselines and immutable decision history audit trail.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from core.state import init_session_state
from core.ui_components import apply_custom_css, render_metric_card

st.set_page_config(page_title="Performance & Audit | ResilientAI", page_icon="⚖️", layout="wide")
apply_custom_css()
init_session_state()

st.markdown('<div class="hero-badge">PAGE 5 • PERFORMANCE & AUDIT</div>', unsafe_allow_html=True)
st.title("Performance Benchmarking & Decision Audit")
st.caption("Quantitative tri-way evaluation against traditional supply chain baselines and immutable governance audit log.")

benchmark = st.session_state.benchmark_results
comp_df = benchmark["comparison_df"]
plan = benchmark["resilient_plan"]

# Top Value Delivered Metrics
v1, v2, v3 = st.columns(3)
with v1:
    render_metric_card(
        "Cost Savings vs No-Action",
        f"${benchmark['cost_savings_vs_no_action']:,.0f}",
        "Averted catastrophic shutdown & SLA penalties",
        "green"
    )
with v2:
    render_metric_card(
        "Cost Savings vs Rule-Based ERP",
        f"${benchmark['cost_savings_vs_rule_based']:,.0f}",
        "Avoided 4-day stockout via air expediting",
        "green"
    )
with v3:
    render_metric_card(
        "Fulfillment Rate Uplift",
        f"+{benchmark['fill_rate_gain_pct']}%",
        f"Reached {plan.fulfillment_rate}% OTIF service level",
        "blue"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Tri-Way Strategy Benchmark Table
st.markdown("### 📊 Tri-Way Benchmark Evaluation Matrix")
st.caption("Evaluating No-Action, Rule-Based Reorder (s, S Heuristic), and ResilientAI over identical disruption conditions.")

# Format dataframe for display
display_df = comp_df.copy()
display_df["Total Landed Cost ($)"] = display_df["Total Landed Cost ($)"].apply(lambda x: f"${x:,.0f}")
display_df["Unmet Demand (Units)"] = display_df["Unmet Demand (Units)"].apply(lambda x: f"{x:,}")

st.dataframe(display_df, hide_index=True, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Comparative Visualizations
col_b1, col_b2 = st.columns([1, 1])

with col_b1:
    with st.container(border=True):
        st.markdown("#### 📈 Fulfillment Rate Across Strategies")
        fig_fill = px.bar(
            comp_df,
            x="Strategy",
            y="Fulfillment Rate (%)",
            color="Strategy",
            color_discrete_sequence=["#ef4444", "#f59e0b", "#10b981"],
            text="Fulfillment Rate (%)"
        )
        fig_fill.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_fill.update_layout(height=280, margin=dict(l=10, r=10, t=20, b=10), showlegend=False, plot_bgcolor="rgba(15, 23, 42, 0.4)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fill, use_container_width=True)

with col_b2:
    with st.container(border=True):
        st.markdown("#### 💵 Total Landed Cost & Penalties ($)")
        fig_cost = px.bar(
            comp_df,
            x="Strategy",
            y="Total Landed Cost ($)",
            color="Strategy",
            color_discrete_sequence=["#ef4444", "#f59e0b", "#38bdf8"],
            text="Total Landed Cost ($)"
        )
        fig_cost.update_traces(texttemplate='$%{y:,.0f}', textposition='outside')
        fig_cost.update_layout(height=280, margin=dict(l=10, r=10, t=20, b=10), showlegend=False, plot_bgcolor="rgba(15, 23, 42, 0.4)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_cost, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Governance & Decision History Audit Trail
st.markdown("### 📜 Governance & Human Decision History Audit Trail")
st.caption("Immutable log of scenario changes, model runs, planner approvals, and overrides.")

audit_records = st.session_state.audit_history
audit_data = [
    {
        "Timestamp": a.timestamp,
        "Action Taken": a.action,
        "Planner ID": a.planner_id,
        "Scenario Context": a.scenario_summary,
        "Projected Cost": f"${a.plan_cost:,.2f}" if a.plan_cost > 0 else "N/A",
        "Fill Rate": f"{a.fill_rate}%" if a.fill_rate > 0 else "N/A",
        "Planner Notes & Rationale": a.notes
    }
    for a in audit_records
]

st.dataframe(pd.DataFrame(audit_data), hide_index=True, use_container_width=True)
