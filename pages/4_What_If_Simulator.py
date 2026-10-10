"""
ResilientAI - Page 4: What-If Simulator (Testing Alternative Scenarios)
Stress-test supply chain scenarios with dynamic parameters and side-by-side impact comparison.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from copy import deepcopy
from core.state import init_session_state, record_audit
from core.models import DisruptionScenario
from core.optimization.solver import SupplyChainOptimizer
from core.ui_components import apply_custom_css, render_metric_card

st.set_page_config(page_title="What-If Simulator | ResilientAI", layout="wide")
apply_custom_css()
init_session_state()

st.markdown('<div class="hero-badge">PAGE 4 • WHAT-IF SIMULATOR</div>', unsafe_allow_html=True)
st.title("What-If Scenario Stress Testing")
st.caption("Simulate varying disruption durations, demand surges, backup vendor constraints, and compare outcomes side-by-side.")

suppliers_df = st.session_state.suppliers_df
inventory_df = st.session_state.inventory_df
demand_df = st.session_state.demand_df

optimizer = SupplyChainOptimizer(
    suppliers_df,
    inventory_df,
    demand_df
)

active_scen = st.session_state.active_scenario
disrupted_id = active_scen.disrupted_supplier_id if active_scen.disrupted_supplier_id in suppliers_df['supplier_id'].values else suppliers_df['supplier_id'].iloc[0]
backup_suppliers = suppliers_df[suppliers_df['supplier_id'] != disrupted_id]

# Baseline Plan
baseline_scenario = DisruptionScenario(disrupted_supplier_id=disrupted_id, duration_days=7, demand_shock_pct=0.0)
baseline_plan = optimizer.solve_resilient_ai_plan(baseline_scenario)

# Simulation Parameters Panel
with st.container(border=True):
    st.markdown("#### Simulation Parameters & Network Stress Levers")
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        sim_duration = st.slider(f"Outage Duration for {disrupted_id} (Days)", min_value=3, max_value=14, value=7, step=1)
        sim_demand_shock = st.slider("Customer Demand Shock (%)", min_value=-30, max_value=50, value=0, step=5)
        
    with col_p2:
        if len(backup_suppliers) >= 1:
            b_sup = backup_suppliers.iloc[0]
            b_default_cap = int(b_sup.get("daily_capacity", 350))
            sim_cap_b = st.slider(f"{b_sup['supplier_name']} Capacity", min_value=max(50, int(b_default_cap * 0.4)), max_value=max(200, int(b_default_cap * 1.8)), value=b_default_cap, step=25)
        else:
            sim_cap_b = 350

        if len(backup_suppliers) >= 2:
            c_sup = backup_suppliers.iloc[1]
            c_default_cap = int(c_sup.get("daily_capacity", 300))
            sim_cap_c = st.slider(f"{c_sup['supplier_name']} Capacity", min_value=max(50, int(c_default_cap * 0.4)), max_value=max(200, int(c_default_cap * 1.8)), value=c_default_cap, step=25)
        else:
            sim_cap_c = 300
        
    with col_p3:
        sim_expedite = st.toggle("Enable Air Freight Expediting", value=True)
        st.markdown("<br>", unsafe_allow_html=True)
        run_sim = st.button("Simulate Revised Scenario", use_container_width=True, type="primary")

# Execute revised simulation
revised_scenario = DisruptionScenario(
    disrupted_supplier_id=disrupted_id,
    duration_days=sim_duration,
    demand_shock_pct=float(sim_demand_shock),
    supplier_b_capacity_override=sim_cap_b,
    supplier_c_capacity_override=sim_cap_c,
    expedite_available=sim_expedite
)
revised_plan = optimizer.solve_resilient_ai_plan(revised_scenario)

st.markdown("---")
st.markdown("### Side-by-Side Scenario Comparison")

# Side-by-side delta cards
c_base, c_rev = st.columns(2)

with c_base:
    with st.container(border=True):
        st.markdown("#### Baseline Scenario (Standard 7-Day Outage)")
        st.caption(f"Standard 7-day shutdown of {disrupted_id}, nominal demand, standard backup allocation.")
        
        b1, b2 = st.columns(2)
        with b1:
            render_metric_card("Fulfillment Rate", f"{baseline_plan.fulfillment_rate}%", "Tier 1: 100%", "green")
            render_metric_card("Stockout Days", f"{baseline_plan.stockout_duration_days} Days", "Bridge achieved", "blue")
        with b2:
            render_metric_card("Total Landed Cost", f"${baseline_plan.total_landed_cost:,.0f}", "Baseline Spend", "blue")
            render_metric_card("Unmet Demand", f"{baseline_plan.unmet_demand_units} Units", "Minimal backlog", "green")

with c_rev:
    with st.container(border=True):
        st.markdown(f"#### What-If Revised Scenario ({sim_duration}d Outage, {sim_demand_shock:+}% Demand)")
        st.caption(f"Capacities: Backup 1 ({sim_cap_b}/d), Backup 2 ({sim_cap_c}/d), Expedite: {'On' if sim_expedite else 'Off'}.")
        
        # Calculate deltas
        cost_delta = revised_plan.total_landed_cost - baseline_plan.total_landed_cost
        cost_sign = "+" if cost_delta >= 0 else "-"
        fill_delta = round(revised_plan.fulfillment_rate - baseline_plan.fulfillment_rate, 1)
        fill_sign = "+" if fill_delta >= 0 else ""
        
        r1, r2 = st.columns(2)
        with r1:
            render_metric_card(
                "Fulfillment Rate", 
                f"{revised_plan.fulfillment_rate}%", 
                f"Delta: {fill_sign}{fill_delta}%", 
                "green" if fill_delta >= 0 else "red"
            )
            render_metric_card(
                "Stockout Days", 
                f"{revised_plan.stockout_duration_days} Days", 
                f"{'Zero starvation' if revised_plan.stockout_duration_days==0 else 'Assembly line halted'}", 
                "green" if revised_plan.stockout_duration_days == 0 else "red"
            )
        with r2:
            render_metric_card(
                "Total Landed Cost", 
                f"${revised_plan.total_landed_cost:,.0f}", 
                f"Delta: {cost_sign}${abs(cost_delta):,.0f}", 
                "amber" if cost_delta > 0 else "blue"
            )
            render_metric_card(
                "Unmet Demand", 
                f"{revised_plan.unmet_demand_units} Units", 
                f"Delta: {revised_plan.unmet_demand_units - baseline_plan.unmet_demand_units:+d} units", 
                "green" if revised_plan.unmet_demand_units == 0 else "red"
            )

st.markdown("<br>", unsafe_allow_html=True)

# Comparative Charts
col_ch1, col_ch2 = st.columns([1, 1])

with col_ch1:
    with st.container(border=True):
        st.markdown("#### Fulfillment Rate & Cost Comparison")
        fig_comp = go.Figure(data=[
            go.Bar(name="Baseline (7-Day)", x=["Fulfillment Rate (%)", "Cost ($ / 10k)"], y=[baseline_plan.fulfillment_rate, baseline_plan.total_landed_cost / 10000], marker_color="#38bdf8"),
            go.Bar(name="What-If Revised", x=["Fulfillment Rate (%)", "Cost ($ / 10k)"], y=[revised_plan.fulfillment_rate, revised_plan.total_landed_cost / 10000], marker_color="#f59e0b")
        ])
        fig_comp.update_layout(barmode="group", height=280, margin=dict(l=10, r=10, t=20, b=10), plot_bgcolor="rgba(15, 23, 42, 0.4)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_comp, use_container_width=True)

with col_ch2:
    with st.container(border=True):
        st.markdown("#### Dynamic Agent Rationale Explanation")
        st.caption("Why did the system adjust allocations under the new scenario?")
        
        avg_demand = int(demand_df['daily_demand'].mean()) if 'daily_demand' in demand_df.columns else 400
        explanation = []
        if sim_duration > 7:
            explanation.append(f"• **Extended Outage ({sim_duration} days)**: Requires sustained backup sourcing past Day 7. Standard freight batches were scaled to avoid inventory starvation.")
        if sim_demand_shock > 0:
            burn = int(avg_demand * (1 + sim_demand_shock / 100))
            explanation.append(f"• **Demand Surge (+{sim_demand_shock}%)**: Increased daily burn to ~{burn:,} units/day, exhausting safety stock faster.")
        if len(backup_suppliers) >= 1 and sim_cap_b < backup_suppliers.iloc[0].get('daily_capacity', 350):
            explanation.append(f"• **{backup_suppliers.iloc[0]['supplier_name']} Capacity Constraint ({sim_cap_b}/day)**: Triggered higher allocation to alternate vendor to prevent capacity overflow.")
        if not sim_expedite:
            explanation.append("• **Expediting Disabled**: Forced standard transit, increasing risk of stockout before initial shipments arrive.")
            
        if not explanation:
            explanation.append("• Parameters are at baseline nominal levels. Dual-sourcing split is optimal.")
            
        for exp in explanation:
            st.markdown(exp)
            
        if st.button("Apply What-If Parameters as Active Scenario"):
            st.session_state.active_scenario = revised_scenario
            st.session_state.recovery_plan = revised_plan
            record_audit("WHAT_IF_TESTED", "Operations Planner", f"Applied What-If: {sim_duration}d outage, {sim_demand_shock}% demand")
            st.success("Updated active scenario across all application pages!")
            st.rerun()
