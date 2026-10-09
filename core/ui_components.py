"""
ResilientAI - UI Components and Visual Styling Tokens
Modern, premium aesthetic styling tokens and reusable Plotly supply chain visualizers.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, Any, List

def apply_custom_css():
    """Injects high-end enterprise styling for supply chain control room."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Top Header Accent */
    .hero-badge {
        display: inline-block;
        padding: 4px 12px;
        background: linear-gradient(135deg, rgba(56, 189, 248, 0.15), rgba(99, 102, 241, 0.15));
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 9999px;
        color: #38bdf8;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    
    /* Metric Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(51, 65, 85, 0.8);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.5);
    }
    
    .metric-title {
        font-size: 0.82rem;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    
    .metric-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.2;
    }
    
    .metric-sub {
        font-size: 0.8rem;
        margin-top: 0.35rem;
        font-weight: 500;
    }
    
    .sub-green { color: #34d399; }
    .sub-red { color: #f87171; }
    .sub-amber { color: #fbbf24; }
    .sub-blue { color: #60a5fa; }
    
    /* Alert Banner */
    .disruption-banner {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(185, 28, 28, 0.25));
        border: 1px solid rgba(239, 68, 68, 0.4);
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .disruption-title {
        color: #fca5a5;
        font-weight: 700;
        font-size: 1.05rem;
    }
    
    .disruption-desc {
        color: #e2e8f0;
        font-size: 0.88rem;
        margin-top: 2px;
    }
    
    /* Agent Node Pills */
    .agent-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 14px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .agent-pill.active {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    /* Constraint Badges */
    .badge-passed {
        background: rgba(16, 185, 129, 0.2);
        color: #34d399;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .badge-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #fbbf24;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .badge-violated {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid rgba(239, 68, 68, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

def render_metric_card(title: str, value: str, subtext: str, status: str = "green"):
    color_class = {
        "green": "sub-green",
        "red": "sub-red",
        "amber": "sub-amber",
        "blue": "sub-blue"
    }.get(status, "sub-green")
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub {color_class}">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

def build_three_echelon_network_fig(disrupted_supplier: str = "SUP-A"):
    """Creates an interactive 3-Echelon Network graph using Plotly."""
    # Nodes in 3 Echelons
    # Echelon 1: Suppliers (x=0)
    # Echelon 2: Manufacturing Plant Alpha (x=1)
    # Echelon 3: Distribution Centers (x=2)
    nodes = [
        # Suppliers
        {"id": "SUP-A", "label": "Apex Microelectronics\n[Tier 1 Primary]", "x": 0.1, "y": 0.8, "type": "supplier", "status": "down"},
        {"id": "SUP-B", "label": "Beacon Tech\n[Tier 1 Backup]", "x": 0.1, "y": 0.5, "type": "supplier", "status": "active"},
        {"id": "SUP-C", "label": "Crestline Components\n[Tier 1 Backup]", "x": 0.1, "y": 0.2, "type": "supplier", "status": "active"},
        
        # Plant
        {"id": "PLANT-A", "label": "Central Plant Alpha\n[Assembly Hub]", "x": 0.55, "y": 0.5, "type": "plant", "status": "active"},
        
        # DCs / Customers
        {"id": "DC-EAST", "label": "DC East\n[Healthcare/Defense T1]", "x": 0.95, "y": 0.7, "type": "dc", "status": "active"},
        {"id": "DC-WEST", "label": "DC West\n[Telecom & Retail T2/T3]", "x": 0.95, "y": 0.3, "type": "dc", "status": "active"},
    ]
    
    node_df = pd.DataFrame(nodes)
    
    fig = go.Figure()
    
    # Edges from Suppliers to Plant
    edge_traces = [
        {"from": "SUP-A", "to": "PLANT-A", "color": "rgba(239, 68, 68, 0.6)", "dash": "dot", "width": 2, "text": "DISRUPTED (0 flow)"},
        {"from": "SUP-B", "to": "PLANT-A", "color": "rgba(56, 189, 248, 0.9)", "dash": "solid", "width": 4, "text": "Active Re-routed Flow"},
        {"from": "SUP-C", "to": "PLANT-A", "color": "rgba(16, 185, 129, 0.9)", "dash": "solid", "width": 3, "text": "Active Re-routed Flow"},
        {"from": "PLANT-A", "to": "DC-EAST", "color": "rgba(148, 163, 184, 0.8)", "dash": "solid", "width": 3, "text": "Priority 1 Fulfillment"},
        {"from": "PLANT-A", "to": "DC-WEST", "color": "rgba(148, 163, 184, 0.8)", "dash": "solid", "width": 3, "text": "Tier 2/3 Fulfillment"}
    ]
    
    id_map = {n["id"]: n for n in nodes}
    
    for edge in edge_traces:
        src = id_map[edge["from"]]
        dst = id_map[edge["to"]]
        fig.add_trace(go.Scatter(
            x=[src["x"], dst["x"]],
            y=[src["y"], dst["y"]],
            mode="lines",
            line=dict(color=edge["color"], width=edge["width"], dash=edge["dash"]),
            hoverinfo="text",
            text=f"{edge['from']} ➔ {edge['to']}: {edge['text']}",
            showlegend=False
        ))
        
    # Draw Nodes
    colors = []
    symbols = []
    sizes = []
    for _, n in node_df.iterrows():
        if n["status"] == "down":
            colors.append("#ef4444")
            symbols.append("x-thin-open")
            sizes.append(26)
        elif n["type"] == "plant":
            colors.append("#f59e0b")
            symbols.append("square")
            sizes.append(30)
        elif n["type"] == "dc":
            colors.append("#10b981")
            symbols.append("diamond")
            sizes.append(24)
        else:
            colors.append("#38bdf8")
            symbols.append("circle")
            sizes.append(24)
            
    fig.add_trace(go.Scatter(
        x=node_df["x"],
        y=node_df["y"],
        mode="markers+text",
        marker=dict(size=sizes, color=colors, line=dict(color="#ffffff", width=2)),
        text=node_df["label"],
        textposition="top center",
        textfont=dict(color="#f8fafc", size=11, family="Plus Jakarta Sans"),
        hoverinfo="text",
        showlegend=False
    ))
    
    # Echelon Column Labels
    fig.add_annotation(x=0.1, y=0.98, text="<b>ECHELON 1: SUPPLIERS</b>", showarrow=False, font=dict(color="#94a3b8", size=12))
    fig.add_annotation(x=0.55, y=0.98, text="<b>ECHELON 2: MANUFACTURING</b>", showarrow=False, font=dict(color="#94a3b8", size=12))
    fig.add_annotation(x=0.95, y=0.98, text="<b>ECHELON 3: DISTRIBUTION HUBS</b>", showarrow=False, font=dict(color="#94a3b8", size=12))
    
    fig.update_layout(
        height=380,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05, 1.1]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.05, 1.05]),
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )
    return fig
