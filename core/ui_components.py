"""
ResilientAI - Enterprise UI Components and Plotly Visualizers
Industrial SaaS design tokens and restrained, high-density operations visualizers.
Symmetric, responsive, and color-matched to the Control Tower reference design.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List

def apply_custom_css():
    """Injects professional enterprise-grade SaaS styling with full laptop & mobile responsiveness."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #050505 !important;
        color: #E2E8F0 !important;
    }
    
    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Streamlit Header Styling - Transparent & Sleek */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2.25rem !important;
        z-index: 50 !important;
    }
    [data-testid="stAppDeployButton"], .stDeployButton {
        display: none !important;
    }

    /* Container padding - Symmetrical & Clean */
    .block-container,
    [data-testid="stMainBlockContainer"],
    .stMainBlockContainer {
        padding-top: 2.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        max-width: 100% !important;
    }

    /* Narrow Left Navigation Rail (Sidebar) Styling matching C3 AI Reference */
    [data-testid="stSidebar"] {
        background-color: #07090E !important;
        border-right: 1px solid #161D2A !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        padding-top: 0.5rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] li a {
        background: transparent !important;
        border-radius: 6px !important;
        color: #94A3B8 !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease !important;
        margin-bottom: 3px !important;
        padding: 8px 12px !important;
        border-left: 3px solid transparent !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] li a:hover {
        background: rgba(168, 85, 247, 0.08) !important;
        color: #F8FAFC !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarNavItems"] li a[aria-current="page"] {
        background: rgba(168, 85, 247, 0.15) !important;
        color: #FFFFFF !important;
        border-left: 3px solid #A855F7 !important;
        font-weight: 700 !important;
        box-shadow: 0 0 14px rgba(168, 85, 247, 0.22) !important;
    }

    /* Responsive Column Handling */
    @media (max-width: 1024px) {
        [data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
            margin-bottom: 1.25rem !important;
        }
    }

    /* Control Tower Top Navigation Header (Matching Reference Image) */
    .ct-top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #0B0E15;
        border: 1px solid #1A2333;
        border-radius: 8px;
        padding: 6px 14px;
        margin-bottom: 12px;
        flex-wrap: wrap;
        gap: 10px;
    }
    .ct-header-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .ct-header-logo {
        background: #A855F7;
        color: #FFFFFF;
        font-weight: 800;
        font-size: 0.72rem;
        padding: 3px 7px;
        border-radius: 4px;
        letter-spacing: 0.04em;
    }
    .ct-header-title {
        font-size: 1.12rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.01em;
    }
    .ct-header-center {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    .ct-header-tab {
        display: flex;
        flex-direction: column;
        cursor: pointer;
        padding: 2px 8px;
        border-radius: 4px;
        transition: background 0.15s ease;
    }
    .ct-header-tab:hover {
        background: rgba(255, 255, 255, 0.04);
    }
    .ct-tab-name {
        font-size: 0.76rem;
        font-weight: 700;
        color: #F1F5F9;
    }
    .ct-tab-sub {
        font-size: 0.65rem;
        color: #64748B;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .ct-header-right {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .ct-util-icon {
        font-size: 13px;
        cursor: pointer;
        color: #94A3B8;
        transition: color 0.15s ease;
    }
    .ct-util-icon:hover {
        color: #F8FAFC;
    }
    .ct-bell-badge {
        position: relative;
        cursor: pointer;
    }
    .ct-badge-dot {
        position: absolute;
        top: -4px;
        right: -6px;
        background: #EF4444;
        color: #FFFFFF;
        font-size: 8px;
        font-weight: 800;
        border-radius: 50%;
        padding: 0 3px;
        line-height: 12px;
    }
    .ct-user-avatar {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: linear-gradient(135deg, #A855F7 0%, #3B82F6 100%);
        color: #07090E;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: 800;
    }

    /* Quick Action 4-Halo Clusters (Matching Reference Image) */
    .qa-halo-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 12px;
        gap: 6px;
    }
    .qa-halo-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        flex: 1;
        cursor: pointer;
        transition: transform 0.15s ease;
    }
    .qa-halo-item:hover {
        transform: translateY(-2px);
    }
    .qa-halo-circle {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 13px;
        font-weight: 700;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.4);
    }
    .qa-halo-circle.red {
        background: rgba(239, 68, 68, 0.16);
        border: 1.5px solid #EF4444;
        color: #EF4444;
        box-shadow: 0 0 12px rgba(239, 68, 68, 0.25);
    }
    .qa-halo-circle.blue {
        background: rgba(59, 130, 246, 0.16);
        border: 1.5px solid #3B82F6;
        color: #3B82F6;
        box-shadow: 0 0 12px rgba(59, 130, 246, 0.25);
    }
    .qa-halo-circle.green {
        background: rgba(16, 185, 129, 0.16);
        border: 1.5px solid #10B981;
        color: #10B981;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.25);
    }
    .qa-halo-circle.purple {
        background: rgba(168, 85, 247, 0.16);
        border: 1.5px solid #A855F7;
        color: #A855F7;
        box-shadow: 0 0 12px rgba(168, 85, 247, 0.25);
    }
    .qa-halo-label {
        font-size: 0.64rem;
        color: #94A3B8;
        font-weight: 600;
        text-align: center;
    }

    /* Reference Card: "Summary | List of Missions" Toggle Pill */
    .ct-toggle-bar {
        display: flex;
        background: #0A0D14;
        border: 1px solid #1A2333;
        border-radius: 6px;
        padding: 2px;
        margin-bottom: 10px;
    }
    .ct-toggle-opt {
        flex: 1;
        text-align: center;
        padding: 5px 8px;
        font-size: 0.68rem;
        font-weight: 600;
        border-radius: 4px;
        cursor: pointer;
        color: #94A3B8;
        transition: all 0.15s ease;
    }
    .ct-toggle-opt.active {
        background: #18202E;
        color: #F8FAFC;
        box-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }

    /* Mission Feed Card with Donut Ring */
    .ct-mission-card {
        background: #10141D;
        border: 1px solid #1A2333;
        border-radius: 8px;
        padding: 9px 12px;
        margin-bottom: 8px;
        transition: border-color 0.15s ease, background 0.15s ease;
    }
    .ct-mission-card:hover {
        border-color: #2D3B52;
        background: #131824;
    }
    .ct-mission-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .ct-mission-id {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.74rem;
        font-weight: 700;
        color: #F8FAFC;
    }
    .ct-mission-route {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.70rem;
        color: #94A3B8;
        margin-bottom: 8px;
    }
    .ct-mission-bottom {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .ct-progress-text {
        font-size: 0.66rem;
        color: #94A3B8;
    }

    /* Status Chips */
    .ops-status-chip {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 9px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 600;
        white-space: nowrap;
    }
    .chip-green {
        background: rgba(16, 185, 129, 0.12);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .chip-amber {
        background: rgba(245, 158, 11, 0.12);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .chip-red {
        background: rgba(239, 68, 68, 0.12);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    .chip-cyan {
        background: rgba(6, 182, 212, 0.12);
        color: #06B6D4;
        border: 1px solid rgba(6, 182, 212, 0.3);
    }
    .chip-purple {
        background: rgba(168, 85, 247, 0.12);
        color: #A855F7;
        border: 1px solid rgba(168, 85, 247, 0.3);
    }

    /* Enterprise Panel Card */
    .ops-panel {
        background: #0E121A;
        border: 1px solid #1C2433;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 12px;
    }
    .ops-panel-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        padding-bottom: 6px;
        border-bottom: 1px solid #18202D;
    }
    .ops-panel-title {
        font-size: 0.8rem;
        font-weight: 700;
        color: #F1F5F9;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .ops-panel-badge {
        font-size: 0.7rem;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Symmetrical Full-Width KPI Row (No awkward cutoffs) */
    .ops-kpi-row {
        background: #10141D;
        border: 1px solid #1A2333;
        border-radius: 6px;
        padding: 8px 12px;
        margin-bottom: 7px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: border-color 0.15s ease;
    }
    .ops-kpi-row:hover {
        border-color: #2D3B52;
    }
    .ops-kpi-left {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .ops-kpi-label {
        font-size: 0.68rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .ops-kpi-sub {
        font-size: 0.70rem;
        color: #64748B;
        font-weight: 500;
    }
    .ops-kpi-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 2px;
    }
    .ops-kpi-val {
        font-size: 1.15rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.1;
    }

    /* Symmetrical Key-Value Metadata Grid */
    .ops-kv-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px 10px;
        background: #10141D;
        border: 1px solid #1A2333;
        border-radius: 6px;
        padding: 10px 12px;
        margin-bottom: 12px;
    }
    .ops-kv-cell {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    .ops-kv-label {
        font-size: 0.64rem;
        color: #64748B;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .ops-kv-val {
        font-size: 0.78rem;
        font-weight: 600;
        color: #F8FAFC;
        word-break: break-word;
    }

    /* Donut Legend List */
    .donut-legend-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px 8px;
        margin-top: 6px;
        font-size: 0.70rem;
        color: #94A3B8;
    }
    .donut-legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Enterprise Button Styling */
    div[data-testid="stButton"] > button {
        background-color: #10141D !important;
        color: #E2E8F0 !important;
        border: 1px solid #1E2738 !important;
        border-radius: 6px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.74rem !important;
        font-weight: 600 !important;
        padding: 6px 12px !important;
        transition: all 0.15s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        border-color: #A855F7 !important;
        color: #FFFFFF !important;
        background-color: #171E2D !important;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%) !important;
        border: 1px solid #C084FC !important;
        color: #FFFFFF !important;
        box-shadow: 0 2px 12px rgba(168, 85, 247, 0.3) !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #6D28D9 0%, #9333EA 100%) !important;
        box-shadow: 0 4px 16px rgba(168, 85, 247, 0.45) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtext: str, status: str = "green", comparison: str = ""):
    """Backward-compatible metric card renderer using enterprise styling."""
    color_class = {
        "green": "chip-green",
        "red": "chip-red",
        "amber": "chip-amber",
        "blue": "chip-cyan"
    }.get(status, "chip-green")
    
    st.markdown(f"""
    <div class="ops-kpi-row">
        <div class="ops-kpi-left">
            <span class="ops-kpi-label">{title}</span>
            <span class="ops-kpi-sub">{subtext}</span>
        </div>
        <div class="ops-kpi-right">
            <span class="ops-kpi-val">{value}</span>
            <span class="ops-status-chip {color_class}" style="font-size:0.65rem;">{comparison or status.upper()}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def build_three_echelon_network_fig(disrupted_supplier: str = "SUP-A", plan=None, suppliers_df=None, inventory_df=None, demand_df=None):
    """
    Symmetrical, high-contrast Network Map matching the enterprise Control Tower architecture.
    Dynamically positions active suppliers, manufacturing assembly, and downstream distribution centers.
    """
    allocs_by_sup = {}
    air_by_sup = {}
    if plan and hasattr(plan, "allocations"):
        for a in plan.allocations:
            allocs_by_sup[a.supplier_id] = allocs_by_sup.get(a.supplier_id, 0) + a.allocated_units
            if "EXPEDITED" in a.shipping_mode:
                air_by_sup[a.supplier_id] = air_by_sup.get(a.supplier_id, 0) + a.allocated_units

    # Dynamic runway calculation
    runway_val = 2.08
    if inventory_df is not None and demand_df is not None:
        try:
            curr = float(inventory_df.iloc[0]["current_stock"])
            daily = float(demand_df["demand_units"].sum()) / max(1, demand_df["day"].nunique())
            runway_val = round(curr / max(1.0, daily), 2)
        except Exception:
            runway_val = 2.08

    fig = go.Figure()

    # Subtle Tactical Grid Coordinate Lines
    for gy in [0.22, 0.50, 0.78]:
        fig.add_trace(go.Scatter(
            x=[-0.05, 1.05], y=[gy, gy], mode="lines",
            line=dict(color="#161D29", width=1, dash="dot"),
            hoverinfo="none", showlegend=False
        ))
    for gx in [0.12, 0.50, 0.88]:
        fig.add_trace(go.Scatter(
            x=[gx, gx], y=[0.05, 0.95], mode="lines",
            line=dict(color="#161D29", width=1, dash="dot"),
            hoverinfo="none", showlegend=False
        ))

    # Extract suppliers list from suppliers_df
    sup_list = []
    if suppliers_df is not None and not suppliers_df.empty:
        t1 = suppliers_df[suppliers_df["tier"] == 1]
        sup_list = t1.to_dict(orient="records") if not t1.empty else suppliers_df.to_dict(orient="records")
    else:
        sup_list = [
            {"supplier_id": "SUP-A", "name": "Apex Microelectronics (Primary)", "daily_capacity": 500},
            {"supplier_id": "SUP-B", "name": "Beacon Tech Solutions (Backup 1)", "daily_capacity": 350},
            {"supplier_id": "SUP-C", "name": "Crestline Components (Backup 2)", "daily_capacity": 300}
        ]

    # Assign vertical positions to suppliers
    n_sup = len(sup_list)
    y_coords = np.linspace(0.76, 0.24, n_sup) if n_sup > 1 else [0.50]
    
    nodes = []
    for idx, s in enumerate(sup_list):
        sid = s["supplier_id"]
        sname = s.get("name", sid).split("(")[0].strip()
        y_pos = y_coords[idx]
        is_disrupted = (sid == disrupted_supplier)
        alloc_qty = allocs_by_sup.get(sid, 0)
        
        if is_disrupted:
            # Disrupted Supplier Route to Plant (Red dashed line)
            fig.add_trace(go.Scatter(
                x=[0.14, 0.50], y=[y_pos, 0.50],
                mode="lines",
                line=dict(color="#EF4444", width=2.4, dash="dash"),
                hoverinfo="text",
                hovertext=f"<b>PRIMARY VENDOR: {sname.upper()} ({sid}) -> PLANT ALPHA</b><br>Status: DISRUPTED OUTAGE<br>Flow: 0 Units/Day",
                showlegend=False
            ))
            nodes.append({
                "id": sid,
                "label": f"{sname} ({sid})<br><span style='color:#EF4444;'>SHUTDOWN [0 u]</span>",
                "x": 0.14, "y": y_pos, "sym": "circle-x",
                "color": "#1C141E", "border": "#EF4444", "size": 22,
                "desc": f"Disrupted Supplier: {sname} (Offline)"
            })
        else:
            # Active Backup Route to Plant
            has_air = air_by_sup.get(sid, 0) > 0
            route_color = "#A855F7" if has_air else "#06B6D4"
            route_width = 3.6 if alloc_qty > 0 else 1.8
            dash_style = "solid" if alloc_qty > 0 else "dot"
            mode_desc = "Air Expedite + Ground" if has_air else "Standard Freight"
            
            fig.add_trace(go.Scatter(
                x=[0.14, 0.50], y=[y_pos, 0.50],
                mode="lines",
                line=dict(color=route_color, width=route_width, dash=dash_style),
                hoverinfo="text",
                hovertext=f"<b>BACKUP ROUTE: {sname.upper()} ({sid}) -> PLANT ALPHA</b><br>Mode: {mode_desc}<br>Allocated: {alloc_qty:,} Units",
                showlegend=False
            ))
            alloc_tag = f"<span style='color:{route_color};'>ALLOC [{alloc_qty:,} u]</span>" if alloc_qty > 0 else "<span style='color:#64748B;'>STANDBY</span>"
            nodes.append({
                "id": sid,
                "label": f"{sname} ({sid})<br>{alloc_tag}",
                "x": 0.14, "y": y_pos, "sym": "circle",
                "color": "#1A1426" if has_air else "#121F29",
                "border": route_color, "size": 22,
                "desc": f"Alternative Supplier: {sname} ({s.get('daily_capacity', 300)} u/d capacity)"
            })

    # Outbound Fulfillment: Plant Alpha -> DC East (Tier 1 Priority 100%)
    fig.add_trace(go.Scatter(
        x=[0.50, 0.86], y=[0.50, 0.72],
        mode="lines",
        line=dict(color="#10B981", width=2.8),
        hoverinfo="text",
        hovertext="<b>OUTBOUND: PLANT ALPHA -> DC EAST</b><br>Tier-1 Healthcare & Defense: 100% Guaranteed SLA<br>Zero Backorders",
        showlegend=False
    ))

    # Outbound Fulfillment: Plant Alpha -> DC West (Commercial Tier 2 & 3)
    fill_rate_display = f"{plan.fulfillment_rate:.1f}%" if plan else "94.2%"
    fig.add_trace(go.Scatter(
        x=[0.50, 0.86], y=[0.50, 0.28],
        mode="lines",
        line=dict(color="#64748B", width=2.2),
        hoverinfo="text",
        hovertext=f"<b>OUTBOUND: PLANT ALPHA -> DC WEST</b><br>Tier-2 & Tier-3 Fulfillment: {fill_rate_display} Service Level",
        showlegend=False
    ))

    # Plant Alpha and Distribution Hub Nodes
    nodes.extend([
        {
            "id": "PLANT-A",
            "label": f"Assembly Plant Alpha<br><span style='color:#F59E0B;'>RUNWAY: {runway_val} DAYS</span>",
            "x": 0.50, "y": 0.50, "sym": "square",
            "color": "#201A15", "border": "#F59E0B", "size": 26,
            "desc": "Central Manufacturing Facility"
        },
        {
            "id": "DC-EAST",
            "label": "DC East (Regional Hub)<br><span style='color:#10B981;'>TIER-1 SLA: 100%</span>",
            "x": 0.86, "y": 0.72, "sym": "diamond",
            "color": "#13211D", "border": "#10B981", "size": 22,
            "desc": "Healthcare & Critical Infrastructure Fulfillment"
        },
        {
            "id": "DC-WEST",
            "label": f"DC West (Regional Hub)<br><span style='color:#94A3B8;'>SERVICE: {fill_rate_display}</span>",
            "x": 0.86, "y": 0.28, "sym": "diamond",
            "color": "#151B26", "border": "#64748B", "size": 22,
            "desc": "Enterprise Telecom & Commercial Fulfillment"
        }
    ])

    ndf = pd.DataFrame(nodes)
    fig.add_trace(go.Scatter(
        x=ndf["x"], y=ndf["y"],
        mode="markers+text",
        marker=dict(
            symbol=ndf["sym"],
            size=ndf["size"],
            color=ndf["color"],
            line=dict(color=ndf["border"], width=2.5)
        ),
        text=ndf["label"],
        textposition="top center",
        textfont=dict(color="#F1F5F9", size=9.5, family="Inter"),
        hoverinfo="text",
        hovertext=[f"<b>{n['id']}</b><br>{n['desc']}" for n in nodes],
        showlegend=False
    ))

    # Echelon Column Labels
    fig.add_annotation(x=0.14, y=0.98, text="<b>ECHELON 1: SUPPLIERS</b>", showarrow=False, font=dict(color="#64748B", size=9.5, family="Inter"))
    fig.add_annotation(x=0.50, y=0.98, text="<b>ECHELON 2: MANUFACTURING</b>", showarrow=False, font=dict(color="#64748B", size=9.5, family="Inter"))
    fig.add_annotation(x=0.86, y=0.98, text="<b>ECHELON 3: DISTRIBUTION</b>", showarrow=False, font=dict(color="#64748B", size=9.5, family="Inter"))

    # Symmetrical Legend Bar
    fig.add_annotation(
        x=0.5, y=-0.04,
        text="● <span style='color:#EF4444;'>Disrupted Lane (0 Flow)</span> &nbsp;&nbsp;|&nbsp;&nbsp; ● <span style='color:#A855F7;'>Air Expedited Route</span> &nbsp;&nbsp;|&nbsp;&nbsp; ● <span style='color:#06B6D4;'>Dual-Source Standard</span> &nbsp;&nbsp;|&nbsp;&nbsp; ■ <span style='color:#F59E0B;'>Assembly Facility</span> &nbsp;&nbsp;|&nbsp;&nbsp; ◆ <span style='color:#10B981;'>DC Hub</span>",
        showarrow=False,
        font=dict(color="#94A3B8", size=9.5, family="Inter"),
        xref="paper", yref="paper"
    )

    fig.update_layout(
        height=350,
        autosize=True,
        margin=dict(l=15, r=15, t=25, b=25),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.02, 1.02]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.08, 1.04]),
        plot_bgcolor="#080A0F",
        paper_bgcolor="#080A0F"
    )
    return fig

def build_enterprise_timeline_fig(plan=None, scenario=None, inventory_df=None, demand_df=None):
    """
    Symmetrical Gantt Chart dynamically rendering outage windows, buffer exhaustion point,
    and actual supplier replenishment arrivals.
    """
    disruption_days = scenario.duration_days if scenario else 7
    disrupted_id = scenario.disrupted_supplier_id if scenario else "SUP-A"
    
    runout_val = 2.08
    if inventory_df is not None and demand_df is not None:
        try:
            curr = float(inventory_df.iloc[0]["current_stock"])
            daily = float(demand_df["demand_units"].sum()) / max(1, demand_df["day"].nunique())
            runout_val = round(curr / max(1.0, daily), 2)
        except Exception:
            runout_val = 2.08

    lanes = [
        {"Lane": f"Primary ({disrupted_id}) Outage", "Start": 1, "Duration": disruption_days, "Color": "#EF4444", "Label": f"{disruption_days} Days (Outage)"}
    ]

    color_palette = ["#A855F7", "#06B6D4", "#10B981", "#3B82F6", "#F59E0B"]
    if plan and hasattr(plan, "allocations") and plan.allocations:
        for idx, a in enumerate(plan.allocations):
            mode_tag = "Air" if "EXPEDITED" in a.shipping_mode else "Std"
            c = "#A855F7" if "EXPEDITED" in a.shipping_mode else color_palette[(idx + 1) % len(color_palette)]
            start_day = 1 if "EXPEDITED" in a.shipping_mode else 1
            lanes.append({
                "Lane": f"{a.supplier_name.split()[0]} ({a.supplier_id}) {mode_tag}",
                "Start": start_day,
                "Duration": a.lead_time_days,
                "Color": c,
                "Label": f"{a.lead_time_days}d ({a.allocated_units:,}u -> Lands Day {a.arrival_day})"
            })
    else:
        lanes.extend([
            {"Lane": "Beacon (SUP-B) Air", "Start": 1, "Duration": 2, "Color": "#A855F7", "Label": "2 Days (700u Air -> Day 3)"},
            {"Lane": "Crestline (SUP-C) Air", "Start": 1, "Duration": 2, "Color": "#06B6D4", "Label": "2 Days (600u Air -> Day 3)"},
            {"Lane": "Crestline (SUP-C) Std", "Start": 1, "Duration": 4, "Color": "#10B981", "Label": "4 Days (900u Std -> Day 5)"},
            {"Lane": "Beacon (SUP-B) Std", "Start": 1, "Duration": 5, "Color": "#3B82F6", "Label": "5 Days (1,050u Std -> Day 6)"}
        ])

    fig = go.Figure()

    for item in lanes:
        fig.add_trace(go.Bar(
            y=[item["Lane"]],
            x=[item["Duration"]],
            base=[item["Start"]],
            orientation="h",
            marker=dict(
                color=item["Color"],
                line=dict(color="#0D1017", width=1.5),
                opacity=0.92
            ),
            text=item["Label"],
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="#F8FAFC", size=9, family="Inter"),
            hoverinfo="text",
            hovertext=f"<b>{item['Lane']}</b><br>Transit Window: Day {item['Start']} to Day {item['Start'] + item['Duration']}<br>Duration: {item['Duration']} Days",
            showlegend=False
        ))

    # Buffer exhaustion vertical line
    fig.add_vline(
        x=runout_val, line_dash="dash", line_color="#EF4444", line_width=1.8,
        annotation_text=f"Buffer Exhaustion (Day {runout_val})",
        annotation_position="top right",
        annotation_font=dict(color="#EF4444", size=8.5, family="JetBrains Mono")
    )

    fig.update_layout(
        height=190,
        autosize=True,
        margin=dict(l=10, r=15, t=10, b=25),
        xaxis=dict(
            title="Planning Horizon (Days 1 to 14)",
            title_font=dict(color="#64748B", size=9),
            tickmode="linear", tick0=1, dtick=1,
            range=[0.5, 14.5],
            showgrid=True, gridcolor="#18202D",
            tickfont=dict(color="#64748B", size=8.5)
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color="#CBD5E1", size=9, family="Inter"),
            showgrid=False
        ),
        plot_bgcolor="#080A0F",
        paper_bgcolor="#080A0F",
        barmode="overlay"
    )
    return fig

def build_enterprise_cost_donut_fig(fill_rate=95.7, total_cost=266361, plan=None):
    """
    Symmetrical Category Donut Chart dynamically displaying landed cost breakdown.
    """
    if plan and hasattr(plan, "total_material_cost"):
        labels = ["Material PO Spend", "Expedited Freight", "Buffer Holding", "Backorder Penalties"]
        values = [
            max(0, plan.total_material_cost),
            max(0, plan.total_freight_cost),
            max(0, plan.total_holding_cost),
            max(0, plan.total_backorder_penalty)
        ]
        total_cost = plan.total_landed_cost
    else:
        labels = ["Material PO Spend", "Expedited Freight", "Buffer Holding", "Backorder Penalties"]
        values = [187700, 43650, 3250, 31761]

    colors = ["#A855F7", "#06B6D4", "#10B981", "#EF4444"]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.72,
        marker=dict(colors=colors, line=dict(color="#0D1017", width=2.5)),
        textinfo="none",
        hoverinfo="label+value+percent",
        direction="clockwise",
        sort=False
    )])

    # Center stat annotation
    fig.add_annotation(
        text=f"<b style='font-size:18px; color:#F8FAFC;'>${total_cost/1000:.1f}K</b><br><span style='font-size:8.5px; color:#94A3B8; text-transform:uppercase;'>Landed Cost</span>",
        x=0.5, y=0.5,
        font=dict(family="Inter"),
        showarrow=False
    )

    fig.update_layout(
        height=175,
        autosize=True,
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False,
        plot_bgcolor="#0E121A",
        paper_bgcolor="#0E121A"
    )
    return fig

def build_sparkline_risk_fig(inventory_df=None, demand_df=None, plan=None):
    """Area sparkline dynamically showing risk intensity across planning horizon."""
    x = list(range(1, 15))
    if plan and hasattr(plan, "stockout_duration_days"):
        stk = plan.stockout_duration_days
        y = [max(0, stk - i) if i < 4 else 0 for i in range(14)]
    else:
        y = [1, 1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        line=dict(color="#10B981", width=2),
        fill="tozeroy",
        fillcolor="rgba(16, 185, 129, 0.15)",
        hoverinfo="none",
        showlegend=False
    ))
    fig.update_layout(
        height=45,
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def build_delivery_prediction_bar_fig(demand_df=None, plan=None):
    """Slender vertical dual-bar chart showing dynamic requested vs fulfilled demand."""
    days = [f"D{i}" for i in range(1, 15)]
    if demand_df is not None and not demand_df.empty:
        daily_req = demand_df.groupby("day")["demand_units"].sum().to_dict()
        requested = [daily_req.get(d, 430) for d in range(1, 15)]
    else:
        requested = [430, 425, 440, 435, 450, 420, 430, 445, 430, 420, 435, 440, 425, 430]
        
    predicted = list(requested)
    # Reflect transitional stockout dip if any
    if plan and hasattr(plan, "stockout_duration_days") and plan.stockout_duration_days > 0:
        predicted[2] = max(50, int(predicted[2] * 0.45))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=days, y=requested,
        name="Requested",
        marker_color="rgba(100, 116, 139, 0.4)",
        width=0.28
    ))
    fig.add_trace(go.Bar(
        x=days, y=predicted,
        name="Delivered",
        marker_color="#A855F7",
        width=0.28
    ))
    
    fig.update_layout(
        height=140,
        autosize=True,
        margin=dict(l=5, r=5, t=5, b=10),
        barmode="overlay",
        xaxis=dict(showgrid=False, tickfont=dict(color="#64748B", size=8), showticklabels=True),
        yaxis=dict(showgrid=True, gridcolor="#18202D", showticklabels=False),
        showlegend=False,
        plot_bgcolor="#0E121A",
        paper_bgcolor="#0E121A"
    )
    return fig
