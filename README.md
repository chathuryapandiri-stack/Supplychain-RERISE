# ResilientAI: Agentic AI-Based Supply Chain Decision-Support System

**ResilientAI** is an autonomous, agentic decision-support platform designed to help manufacturing enterprises respond to acute supply chain disruptions. 

Engineered specifically for a **three-echelon network** facing a critical disruption (**a 7-day complete shutdown of primary supplier Apex Microelectronics**), ResilientAI replaces siloed, manual spreadsheets and brittle ERP reorder heuristics with a coordinated multi-agent workflow paired with mathematical optimization and human-in-the-loop governance.

---

## 🏛️ System Architecture

ResilientAI coordinates **five specialized autonomous agents** sharing an underlying schema and state:

```
                               [ Disruption Signal: Supplier A 7-Day Outage ]
                                                     │
                 ┌───────────────────┬───────────────┴───────────────┬───────────────────┐
                 ▼                   ▼                               ▼                   ▼
         ┌───────────────┐   ┌───────────────┐               ┌───────────────┐   ┌───────────────┐
         │ Demand Agent  │   │Inventory Agent│               │ Supplier Risk │   │Logistics Agent│
         │ (Priority     │   │(Runway & Line │               │ (Qualification│   │(Air Expedite  │
         │  Tiers 1/2/3) │   │ Starvation)   │               │  & Headroom)  │   │ vs Standard)  │
         └───────┬───────┘   └───────┬───────┘               └───────┬───────┘   └───────┬───────┘
                 │                   │                               │                   │
                 └───────────────────┼───────────────┬───────────────┘                   │
                                     ▼               ▼                                   ▼
                             [ Specialized Domain Proposals & JSON Action Schemas ]
                                                     │
                                                     ▼
                                      ┌──────────────────────────────┐
                                      │   Master Coordinator Agent   │
                                      │  - Conflict Resolution       │
                                      │  - Constraint Checking       │
                                      │  - MILP / Solver Synthesis   │
                                      └──────────────┬───────────────┘
                                                     │
                                                     ▼
                                      ┌──────────────────────────────┐
                                      │ Human-in-the-Loop Governance │
                                      │  - What-If Stress Testing    │
                                      │  - Planner Approval Gating   │
                                      │  - Immutable Audit History   │
                                      └──────────────────────────────┘
```

---

## 📑 The 6 Interconnected Control Room Pages

1. **📊 Command Center (Main Dashboard)**: Real-time situational awareness, key metrics (available runway, fulfillment %, unmet demand, landed cost), interactive Plotly 3-echelon network diagram (Suppliers ➔ Plant Alpha ➔ Customer DCs), and live disruption telemetry.
2. **🤖 Agent Workspace (Collaborative AI Analysis)**: Visual DAG pipeline showing sequential and collaborative agent interactions. Interactive telemetry inspector for all 5 specialized agents with inputs, outputs, JSON contracts, and resolved conflicts.
3. **🎯 Recovery Planner (Actionable Recovery Strategy)**: Actionable purchase and dispatch schedule across backup vendors (Beacon Tech & Crestline), air freight schedules, landed cost decomposition, hard constraint verification badges, and human planner approval/rejection gating.
4. **🧪 What-If Simulator (Testing Alternative Scenarios)**: Dynamic simulation testing varying outage durations (3-14 days), customer demand surges (-30% to +50%), supplier capacity constraints, and freight modes with side-by-side delta metrics.
5. **⚖️ Performance & Audit (Tri-Way Benchmarking & Governance)**: Quantitative benchmarking comparing **No-Action** vs. **Rule-Based ERP** vs. **ResilientAI** across 8 core metrics: Fill Rate, Backorders, Total Landed Cost, Recovery Time, and Stockout Duration. Includes an immutable decision history audit trail.
6. **🗄️ Supply Chain Data (Master Data Repository)**: Transparent data browser for Tier-1 suppliers, on-hand inventory buffers, 14-day customer demand orders, and Bill of Materials (BOM) with search, filtering, and CSV export.

---

## 📊 Tri-Way Benchmark Evaluation

Tested over the identical 7-day Supplier A outage on a 14-day planning horizon:

| Performance Metric | 1. No Action (Passive) | 2. Rule-Based ERP (s, S) | 3. ResilientAI (Multi-Agent) | ResilientAI Advantage |
| :--- | :---: | :---: | :---: | :---: |
| **Fulfillment Rate (%)** | 14.8% | 55.2% | **95.7%** | **+40.5% vs ERP** |
| **Unmet Backorders (Units)** | 5,173 units | 2,723 units | **264 units** | **-90.3% reduction** |
| **Total Landed Cost ($)** | $803,355 | $546,175 | **$266,361** | **$279.8k savings vs ERP** |
| **Stockout Duration** | 8 Days | 4 Days | **1 Day (Transitional)** | **-75% downtime** |
| **Recovery Time** | 15 Days | 12 Days | **9 Days** | **3-day faster stabilization** |
| **Constraint Violations** | 3 Violations | 1 Violation | **0 Violations** | **100% Feasible** |
| **Tier-1 Healthcare SLA** | Failed (18% fill) | Partial (62% fill) | **100.0% Guaranteed** | **Zero critical penalty** |

---

## 🚀 Running the Application Locally

### Prerequisites
- Python 3.10+ (Tested on Python 3.13)
- Required packages: `streamlit`, `plotly`, `pandas`, `numpy`, `pulp`, `pydantic`

### Launch Command
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.
