"""
ResilientAI - Page 4: What-If Simulator (Testing Alternative Scenarios)
Stress-test supply chain scenarios with dynamic parameters and side-by-side impact comparison.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from core.state import init_session_state, record_audit, run_multi_agent_workflow
from core.models import DisruptionScenario
from core.optimization.solver import SupplyChainOptimizer
from core.ui_components import apply_custom_css, render_metric_card

st.set_page_config(page_title="What-If Simulator | ResilientAI", layout="wide")
apply_custom_css()
init_session_state()

st.markdown('<div class="hero-badge">PAGE 4 • WHAT-IF SIMULATOR</div>', unsafe_allow_html=True)
st.title("What-If Scenario Stress Testing")
st.caption("Simulate varying disruption durations, demand surges, backup vendor constraints, and compare outcomes side-by-side with real-time MILP optimization.")

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

# Safe supplier name helper
def get_supplier_display_name(row_or_series) -> str:
    if isinstance(row_or_series, pd.Series) or isinstance(row_or_series, dict):
        return str(row_or_series.get("supplier_name") or row_or_series.get("name") or row_or_series.get("supplier_id", "Supplier"))
    return "Supplier"

disrupted_match = suppliers_df[suppliers_df['supplier_id'] == disrupted_id]
disrupted_name = get_supplier_display_name(disrupted_match.iloc[0]) if not disrupted_match.empty else disrupted_id
backup_suppliers = suppliers_df[suppliers_df['supplier_id'] != disrupted_id]

# Standard 7-Day Baseline Plan
baseline_scenario = DisruptionScenario(disrupted_supplier_id=disrupted_id, duration_days=7, demand_shock_pct=0.0)
baseline_plan = optimizer.solve_resilient_ai_plan(baseline_scenario)

# Simulation Parameters Panel
with st.container(border=True):
    st.markdown("#### Simulation Parameters & Network Stress Levers")
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("**Disruption Duration & Demand**")
        sim_duration = st.slider(
            f"Outage Duration for {disrupted_name} (Days)",
            min_value=3,
            max_value=14,
            value=int(active_scen.duration_days) if 3 <= active_scen.duration_days <= 14 else 7,
            step=1,
            key="slider_sim_duration"
        )
        sim_demand_shock = st.slider(
            "Customer Demand Shock (%)",
            min_value=-30,
            max_value=50,
            value=int(active_scen.demand_shock_pct) if -30 <= active_scen.demand_shock_pct <= 50 else 0,
            step=5,
            key="slider_sim_demand_shock"
        )
        
    with col_p2:
        st.markdown("**Secondary Supplier Daily Capacities**")
        cap_overrides = {}
        if len(backup_suppliers) >= 1:
            b_sup = backup_suppliers.iloc[0]
            b_name = get_supplier_display_name(b_sup)
            b_id = b_sup["supplier_id"]
            b_default_cap = int(b_sup.get("daily_capacity", 350))
            sim_cap_b = st.slider(
                f"{b_name} Capacity (u/day)",
                min_value=max(50, int(b_default_cap * 0.4)),
                max_value=max(200, int(b_default_cap * 1.8)),
                value=b_default_cap,
                step=25,
                key="slider_sim_cap_b"
            )
            cap_overrides[b_id] = sim_cap_b
        else:
            sim_cap_b = 350

        if len(backup_suppliers) >= 2:
            c_sup = backup_suppliers.iloc[1]
            c_name = get_supplier_display_name(c_sup)
            c_id = c_sup["supplier_id"]
            c_default_cap = int(c_sup.get("daily_capacity", 300))
            sim_cap_c = st.slider(
                f"{c_name} Capacity (u/day)",
                min_value=max(50, int(c_default_cap * 0.4)),
                max_value=max(200, int(c_default_cap * 1.8)),
                value=c_default_cap,
                step=25,
                key="slider_sim_cap_c"
            )
            cap_overrides[c_id] = sim_cap_c
        else:
            sim_cap_c = 300
        
    with col_p3:
        st.markdown("**Logistics Modes & Simulation Run**")
        sim_expedite = st.toggle("Enable Air Freight Expediting", value=True, key="toggle_sim_expedite")
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        run_sim = st.button("Simulate Revised Scenario", use_container_width=True, type="primary", key="btn_run_sim")
        if run_sim:
            st.toast("Simulation executed: parameters evaluated against optimization engine.", icon="check_circle")

# Execute revised simulation with dynamic overrides
revised_scenario = DisruptionScenario(
    disrupted_supplier_id=disrupted_id,
    duration_days=sim_duration,
    demand_shock_pct=float(sim_demand_shock),
    supplier_b_capacity_override=sim_cap_b,
    supplier_c_capacity_override=sim_cap_c,
    supplier_capacity_overrides=cap_overrides,
    expedite_available=sim_expedite
)
revised_plan = optimizer.solve_resilient_ai_plan(revised_scenario)

# Active status indicator
is_diverged = (
    sim_duration != baseline_scenario.duration_days or
    sim_demand_shock != baseline_scenario.demand_shock_pct or
    not sim_expedite or
    (len(backup_suppliers) >= 1 and sim_cap_b != int(backup_suppliers.iloc[0].get("daily_capacity", 350))) or
    (len(backup_suppliers) >= 2 and sim_cap_c != int(backup_suppliers.iloc[1].get("daily_capacity", 300)))
)

status_badge_color = "#D29922" if is_diverged else "#238636"
status_text = f"Stress Testing Active: {sim_duration}d Outage, {sim_demand_shock:+}% Demand, Expediting {'ON' if sim_expedite else 'OFF'}" if is_diverged else "Baseline Parameters Active: Nominal 7-day disruption"

st.markdown(f"""
<div style="background:#161B22; border:1px solid #30363D; border-left:3px solid {status_badge_color}; border-radius:6px; padding:8px 14px; margin-bottom:16px; display:flex; justify-content:space-between; align-items:center;">
    <span style="font-size:0.80rem; font-weight:600; color:#E6EDF3;">{status_text}</span>
    <span style="font-size:0.72rem; color:#8B949E; font-family:'JetBrains Mono', monospace;">Target: {disrupted_name}</span>
</div>
""", unsafe_allow_html=True)

st.markdown("### Side-by-Side Scenario Comparison")

# Side-by-side delta cards
c_base, c_rev = st.columns(2)

with c_base:
    with st.container(border=True):
        st.markdown("#### Baseline Scenario (Standard 7-Day Outage)")
        st.caption(f"Standard 7-day shutdown of {disrupted_name}, nominal demand, standard backup allocation.")
        
        b1, b2 = st.columns(2)
        with b1:
            render_metric_card("Fulfillment Rate", f"{baseline_plan.fulfillment_rate}%", "Tier 1: 100% Protected", "green")
            render_metric_card("Stockout Days", f"{baseline_plan.stockout_duration_days} Days", "Runway gap bridged", "blue")
        with b2:
            render_metric_card("Total Landed Cost", f"${baseline_plan.total_landed_cost:,.0f}", "Baseline Spend", "blue")
            render_metric_card("Unmet Demand", f"{baseline_plan.unmet_demand_units} Units", "Minimal backlog", "green")

with c_rev:
    with st.container(border=True):
        st.markdown(f"#### What-If Revised Scenario ({sim_duration}d Outage, {sim_demand_shock:+}% Demand)")
        st.caption(f"Backup 1 ({sim_cap_b}/d), Backup 2 ({sim_cap_c}/d), Expedite: {'On' if sim_expedite else 'Off'}.")
        
        # Calculate deltas
        cost_delta = revised_plan.total_landed_cost - baseline_plan.total_landed_cost
        cost_sign = "+" if cost_delta >= 0 else "-"
        fill_delta = round(revised_plan.fulfillment_rate - baseline_plan.fulfillment_rate, 1)
        fill_sign = "+" if fill_delta >= 0 else ""
        unmet_delta = revised_plan.unmet_demand_units - baseline_plan.unmet_demand_units
        stockout_delta = revised_plan.stockout_duration_days - baseline_plan.stockout_duration_days
        
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
                f"{'Zero starvation' if revised_plan.stockout_duration_days == 0 else f'+{stockout_delta} Days Starvation' if stockout_delta > 0 else 'Stockout eliminated'}", 
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
                f"Delta: {unmet_delta:+d} units", 
                "green" if revised_plan.unmet_demand_units == 0 else "red"
            )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Comparative Charts & Rationale
col_ch1, col_ch2 = st.columns([1.1, 0.9])

with col_ch1:
    with st.container(border=True):
        st.markdown("#### Dual-Metric Operational Comparison")
        st.caption("Fulfillment rate and landed cost compared across baseline vs revised stress-test.")
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=["Fulfillment Rate (%)", "Total Landed Cost ($)"],
            horizontal_spacing=0.18
        )
        
        # Subplot 1: Fulfillment Rate
        fig.add_trace(
            go.Bar(
                name="Baseline",
                x=["Baseline", "Revised"],
                y=[baseline_plan.fulfillment_rate, revised_plan.fulfillment_rate],
                text=[f"{baseline_plan.fulfillment_rate}%", f"{revised_plan.fulfillment_rate}%"],
                textposition="auto",
                marker_color=["#388BFD", "#238636" if revised_plan.fulfillment_rate >= baseline_plan.fulfillment_rate else "#DA3633"],
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Subplot 2: Total Landed Cost
        fig.add_trace(
            go.Bar(
                name="Cost",
                x=["Baseline", "Revised"],
                y=[baseline_plan.total_landed_cost, revised_plan.total_landed_cost],
                text=[f"${baseline_plan.total_landed_cost:,.0f}", f"${revised_plan.total_landed_cost:,.0f}"],
                textposition="auto",
                marker_color=["#388BFD", "#D29922" if revised_plan.total_landed_cost > baseline_plan.total_landed_cost else "#238636"],
                showlegend=False
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            height=280,
            margin=dict(l=20, r=20, t=30, b=20),
            plot_bgcolor="#0D1117",
            paper_bgcolor="#161B22",
            font=dict(color="#E6EDF3", size=11, family="Inter, sans-serif"),
        )
        fig.update_xaxes(showgrid=False, linecolor="#30363D")
        fig.update_yaxes(gridcolor="#21262D", linecolor="#30363D")
        
        st.plotly_chart(fig, use_container_width=True)

with col_ch2:
    with st.container(border=True):
        st.markdown("#### Dynamic Agent Rationale Explanation")
        st.caption("Root-cause synthesis from the Multi-Agent Coordinator explaining metric deltas:")
        
        avg_demand = int(demand_df['demand_units'].mean()) if 'demand_units' in demand_df.columns else (int(demand_df['daily_demand'].mean()) if 'daily_demand' in demand_df.columns else 400)
        explanation = []
        
        if sim_duration > 7:
            explanation.append(f"• **Extended Outage ({sim_duration} days)**: Primary recovery is deferred to Day {sim_duration + 1}. Requires sustained backup supplier replenishment to prevent assembly line starvation.")
        elif sim_duration < 7:
            explanation.append(f"• **Shortened Outage ({sim_duration} days)**: Early recovery on Day {sim_duration + 1} reduces required reliance on secondary vendors, lowering freight expedite premiums.")
            
        if sim_demand_shock > 0:
            burn = int(avg_demand * (1 + sim_demand_shock / 100))
            explanation.append(f"• **Demand Surge (+{sim_demand_shock}%)**: Daily consumption spikes to ~{burn:,} units/day, exhausting safety buffer faster and risking Tier 2/3 customer backorders.")
        elif sim_demand_shock < 0:
            explanation.append(f"• **Demand Contraction ({sim_demand_shock}%)**: Lower customer consumption extends existing warehouse runway, lessening required replenishment urgency.")
            
        if len(backup_suppliers) >= 1 and sim_cap_b < backup_suppliers.iloc[0].get('daily_capacity', 350):
            b_n = get_supplier_display_name(backup_suppliers.iloc[0])
            explanation.append(f"• **{b_n} Capacity Cap ({sim_cap_b} u/d)**: Restricts primary backup dispatch volume, shifting order allocation to secondary vendors or risking backlogs.")
            
        if not sim_expedite:
            explanation.append("• **Air Expediting Disabled**: Restricts network to standard transit (4-5 days lead time). Stockout gap cannot be closed before warehouse buffer runs out, causing production halts.")
            
        if not explanation:
            explanation.append("• Parameters match nominal baseline conditions. Dual-sourcing split across qualified backup vendors achieves optimal SLA balance.")
            
        for exp in explanation:
            st.markdown(f"<div style='font-size:0.78rem; line-height:1.45; color:#C9D1D9; margin-bottom:6px;'>{exp}</div>", unsafe_allow_html=True)
            
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        
        if st.button("Apply What-If Parameters as Active Scenario", type="primary", use_container_width=True, key="btn_apply_what_if"):
            st.session_state.active_scenario = revised_scenario
            st.session_state.recovery_plan = revised_plan
            
            # Synchronize the full multi-agent workflow across all pages
            run_multi_agent_workflow()
            
            record_audit(
                action="WHAT_IF_TESTED",
                planner_id="Operations Planner",
                notes=f"Applied What-If: {sim_duration}d outage for {disrupted_id}, {sim_demand_shock:+}% demand, Expedite={'ON' if sim_expedite else 'OFF'}."
            )
            st.toast("Active scenario updated across Command Center, Agent Workspace, and Planner.", icon="check_circle")
            st.success("Successfully updated active scenario across all application pages.")
            st.rerun()
