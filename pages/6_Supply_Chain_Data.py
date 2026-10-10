"""
ResilientAI - Page 6: Supply Chain Data (Inspecting Underlying Information)
Transparent data browser, search/filtering, CSV export/import, and dynamic dataset generator.
"""

import streamlit as st
import pandas as pd
import random
from core.state import init_session_state, run_multi_agent_workflow, apply_mock_dataset
from core.data_loader import (
    get_default_suppliers_df, get_default_inventory_df, get_default_demand_df,
    get_default_bom_df
)
from core.mock_data_generator import (
    generate_scenario_dataset, INDUSTRY_PRESETS, MockDataGenerator
)
from core.models import DisruptionScenario
from core.ui_components import apply_custom_css

st.set_page_config(page_title="Supply Chain Data | ResilientAI", layout="wide")
apply_custom_css()
init_session_state()

st.markdown('<div class="hero-badge">PAGE 6 • DATA REPOSITORY & GENERATOR</div>', unsafe_allow_html=True)
st.title("Supply Chain Master Data & Scenario Generator")
st.caption("Inspect underlying datasets, export schemas, or generate custom synthetic supply chain topologies across industry presets.")

# Interactive Scenario & Mock Data Generator
with st.container(border=True):
    st.markdown("#### Synthetic Network & Mock Data Generator")
    st.caption("Generate realistic parametric datasets to evaluate how the multi-agent system adapts to distinct industry operating conditions.")

    preset_options = {
        "industrial_iot": "Industrial IoT Gateways (Standard)",
        "automotive_ev": "Automotive & EV Battery Powertrain",
        "aerospace_defense": "Aerospace & Defense Avionics",
        "medical_devices": "Life-Critical Medical Diagnostics"
    }

    g_col1, g_col2, g_col3 = st.columns([1, 1, 1])

    with g_col1:
        selected_preset = st.selectbox(
            "Industry Ecosystem Preset",
            options=list(preset_options.keys()),
            format_func=lambda k: preset_options[k],
            index=0
        )
        disruption_sev = st.select_slider(
            "Disruption Severity",
            options=["low", "medium", "high", "critical"],
            value="critical"
        )

    with g_col2:
        outage_duration = st.slider(
            "Supplier Outage Duration (Days)",
            min_value=3,
            max_value=14,
            value=7,
            step=1
        )
        volatility_choice = st.select_slider(
            "Demand Volatility",
            options=["stable", "moderate", "high"],
            value="stable"
        )

    with g_col3:
        buffer_days = st.slider(
            "Initial Inventory Buffer (Days)",
            min_value=1.0,
            max_value=8.0,
            value=2.1,
            step=0.1
        )
        randomize_seed = st.checkbox("Randomize Seed (Stochastic Generation)", value=False)
        seed_val = random.randint(1, 99999) if randomize_seed else 42

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate & Apply Custom Dataset", type="primary", use_container_width=True):
        new_dataset = generate_scenario_dataset(
            preset=selected_preset,
            num_suppliers=4,
            disruption_severity=disruption_sev,
            demand_volatility=volatility_choice,
            inventory_buffer_days=buffer_days,
            seed=seed_val
        )
        new_scenario = DisruptionScenario(
            disrupted_supplier_id=new_dataset["disrupted_supplier_id"],
            duration_days=outage_duration,
            capacity_drop_pct=100.0,
            demand_shock_pct=0.0
        )
        apply_mock_dataset(
            dataset_bundle=new_dataset,
            scenario=new_scenario,
            notes=f"Generated {preset_options[selected_preset]} dataset (Severity: {disruption_sev}, Buffer: {buffer_days}d, Outage: {outage_duration}d)"
        )
        st.toast(f"Successfully loaded {preset_options[selected_preset]} dataset across all modules!")
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Dataset Master Tabs
tab_sup, tab_inv, tab_dem, tab_bom = st.tabs([
    "Suppliers Master Data",
    "Plant Inventory Buffers",
    "Customer Demand & Orders",
    "Bill of Materials (BOM)"
])

# 1. Suppliers Tab
with tab_sup:
    st.markdown("#### Tier-1 & Tier-2 Suppliers Dataset")
    st.caption("Contains physical capacities, lead times, freight rates, unit costs, and reliability ratings.")
    
    col_s_f1, col_s_f2 = st.columns([2, 1])
    with col_s_f1:
        search_sup = st.text_input("Search Suppliers by Name or Component", "")
    with col_s_f2:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_sup = st.session_state.suppliers_df.to_csv(index=False).encode('utf-8')
        st.download_button("Export Suppliers CSV", data=csv_sup, file_name="suppliers_master.csv", mime="text/csv")
        
    df_s = st.session_state.suppliers_df.copy()
    if search_sup:
        name_col = "supplier_name" if "supplier_name" in df_s.columns else "name"
        comp_col = "critical_component" if "critical_component" in df_s.columns else "component"
        mask = (df_s[name_col].astype(str).str.contains(search_sup, case=False)) | (df_s[comp_col].astype(str).str.contains(search_sup, case=False))
        df_s = df_s[mask]
        
    st.dataframe(df_s, use_container_width=True, hide_index=True)

# 2. Inventory Tab
with tab_inv:
    st.markdown("#### Facility Inventory & Storage Buffers")
    st.caption("On-hand stock levels, safety thresholds, consumption burn rates, and unit holding costs.")
    
    csv_inv = st.session_state.inventory_df.to_csv(index=False).encode('utf-8')
    st.download_button("Export Inventory CSV", data=csv_inv, file_name="inventory_buffers.csv", mime="text/csv")
    st.dataframe(st.session_state.inventory_df, use_container_width=True, hide_index=True)

# 3. Demand Tab
with tab_dem:
    st.markdown("#### Customer Orders & SLA Schedule (14-Day Horizon)")
    st.caption("Daily order volume by customer tier and unfulfilled backorder penalties.")
    
    c_df1, c_df2 = st.columns([1, 1])
    with c_df1:
        available_tiers = sorted(st.session_state.demand_df["customer_tier"].unique().tolist()) if "customer_tier" in st.session_state.demand_df.columns else [1, 2, 3]
        tier_filter = st.multiselect("Filter by Customer Tier", options=available_tiers, default=available_tiers)
    with c_df2:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_dem = st.session_state.demand_df.to_csv(index=False).encode('utf-8')
        st.download_button("Export Demand CSV", data=csv_dem, file_name="demand_schedule.csv", mime="text/csv")
        
    tier_col = "customer_tier" if "customer_tier" in st.session_state.demand_df.columns else "tier"
    df_d = st.session_state.demand_df[st.session_state.demand_df[tier_col].isin(tier_filter)]
    st.dataframe(df_d, use_container_width=True, hide_index=True)

# 4. BOM Tab
with tab_bom:
    st.markdown("#### Bill of Materials (BOM) & Network Architecture")
    st.caption("Structural dependencies for finished goods assembly at Plant Alpha.")
    
    bom_df = st.session_state.get("bom_df", get_default_bom_df())
    st.dataframe(bom_df, use_container_width=True, hide_index=True)

st.markdown("---")
# Reset dataset button
if st.button("Reset All Data to Standard Benchmark"):
    st.session_state.suppliers_df = get_default_suppliers_df()
    st.session_state.inventory_df = get_default_inventory_df()
    st.session_state.demand_df = get_default_demand_df()
    st.session_state.bom_df = get_default_bom_df()
    st.session_state.active_scenario = DisruptionScenario(
        disrupted_supplier_id="SUP-A",
        duration_days=7,
        capacity_drop_pct=100.0,
        demand_shock_pct=0.0
    )
    run_multi_agent_workflow()
    st.success("All datasets reset to standard benchmark default.")
    st.rerun()

