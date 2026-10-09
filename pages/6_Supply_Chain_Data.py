"""
ResilientAI - Page 6: Supply Chain Data (Inspecting Underlying Information)
Transparent data browser, search/filtering, CSV export/import, and dataset configuration.
"""

import streamlit as st
import pandas as pd
from core.state import init_session_state, run_multi_agent_workflow
from core.data_loader import get_default_suppliers_df, get_default_inventory_df, get_default_demand_df
from core.ui_components import apply_custom_css

st.set_page_config(page_title="Supply Chain Data | ResilientAI", page_icon="🗄️", layout="wide")
apply_custom_css()
init_session_state()

st.markdown('<div class="hero-badge">PAGE 6 • DATA REPOSITORY</div>', unsafe_allow_html=True)
st.title("Supply Chain Master Data & Schema")
st.caption("Inspect, filter, export, and edit the underlying 3-echelon network datasets powering the multi-agent system.")

tab_sup, tab_inv, tab_dem, tab_bom = st.tabs([
    "🏭 Suppliers Master Data",
    "📦 Plant Inventory Buffers",
    "📈 Customer Demand & Orders",
    "⚙️ Bill of Materials (BOM)"
])

# 1. Suppliers Tab
with tab_sup:
    st.markdown("#### 🏭 Tier-1 & Tier-2 Suppliers Dataset")
    st.caption("Contains physical capacities, lead times, freight rates, unit costs, and reliability ratings.")
    
    col_s_f1, col_s_f2 = st.columns([2, 1])
    with col_s_f1:
        search_sup = st.text_input("🔍 Search Suppliers by Name or Component", "")
    with col_s_f2:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_sup = st.session_state.suppliers_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Suppliers CSV", data=csv_sup, file_name="suppliers_master.csv", mime="text/csv")
        
    df_s = st.session_state.suppliers_df.copy()
    if search_sup:
        df_s = df_s[df_s["name"].str.contains(search_sup, case=False) | df_s["component"].str.contains(search_sup, case=False)]
        
    st.dataframe(df_s, use_container_width=True, hide_index=True)

# 2. Inventory Tab
with tab_inv:
    st.markdown("#### 📦 Facility Inventory & Storage Buffers")
    st.caption("On-hand stock levels, safety thresholds, consumption burn rates, and unit holding costs.")
    
    csv_inv = st.session_state.inventory_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Export Inventory CSV", data=csv_inv, file_name="inventory_buffers.csv", mime="text/csv")
    st.dataframe(st.session_state.inventory_df, use_container_width=True, hide_index=True)

# 3. Demand Tab
with tab_dem:
    st.markdown("#### 📈 Customer Orders & SLA Schedule (14-Day Horizon)")
    st.caption("Daily order volume by customer tier and unfulfilled backorder penalties.")
    
    c_df1, c_df2 = st.columns([1, 1])
    with c_df1:
        tier_filter = st.multiselect("Filter by Customer Tier", options=[1, 2, 3], default=[1, 2, 3])
    with c_df2:
        st.markdown("<br>", unsafe_allow_html=True)
        csv_dem = st.session_state.demand_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export Demand CSV", data=csv_dem, file_name="demand_schedule.csv", mime="text/csv")
        
    df_d = st.session_state.demand_df[st.session_state.demand_df["tier"].isin(tier_filter)]
    st.dataframe(df_d, use_container_width=True, hide_index=True)

# 4. BOM Tab
with tab_bom:
    st.markdown("#### ⚙️ Bill of Materials (BOM) & Network Architecture")
    st.caption("Structural dependencies for finished goods assembly at Plant Alpha.")
    
    bom_data = [
        {"Finished Product": "Industrial IoT Gateway G-500", "Component ID": "MCU-900", "Component Name": "Control Chipset MCU-900", "Qty Required": 1, "Primary Supplier": "Apex (SUP-A)", "Criticality": "CRITICAL (Single Point)"},
        {"Finished Product": "Industrial IoT Gateway G-500", "Component ID": "CH-10", "Component Name": "Enclosure Chassis CH-10", "Qty Required": 1, "Primary Supplier": "Delta (SUP-D)", "Criticality": "STANDARD"}
    ]
    st.dataframe(pd.DataFrame(bom_data), use_container_width=True, hide_index=True)

st.markdown("---")
# Reset dataset button
if st.button("🔄 Reset All Data to Standard Benchmark"):
    st.session_state.suppliers_df = get_default_suppliers_df()
    st.session_state.inventory_df = get_default_inventory_df()
    st.session_state.demand_df = get_default_demand_df()
    run_multi_agent_workflow()
    st.success("All datasets reset to standard benchmark default.")
    st.rerun()
