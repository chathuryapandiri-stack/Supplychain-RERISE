"""
ResilientAI - Session State and Context Management
Ensures all 6 application pages share unified scenario data, simulation runs, and audit trail.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List
from core.data_loader import (
    get_default_suppliers_df, get_default_inventory_df, get_default_demand_df,
    initialize_data_files
)
from core.models import DisruptionScenario, RecoveryPlanResult, AuditRecord
from core.agents.coordinator_agent import CoordinatorAgent
from core.optimization.solver import SupplyChainOptimizer

def init_session_state():
    """Initializes global session state across all pages."""
    initialize_data_files()
    
    if "suppliers_df" not in st.session_state:
        st.session_state.suppliers_df = get_default_suppliers_df()
        
    if "inventory_df" not in st.session_state:
        st.session_state.inventory_df = get_default_inventory_df()
        
    if "demand_df" not in st.session_state:
        st.session_state.demand_df = get_default_demand_df()
        
    if "active_scenario" not in st.session_state:
        st.session_state.active_scenario = DisruptionScenario(
            disrupted_supplier_id="SUP-A",
            duration_days=7,
            capacity_drop_pct=100.0,
            demand_shock_pct=0.0
        )
        
    if "audit_history" not in st.session_state:
        st.session_state.audit_history = [
            AuditRecord(
                timestamp=datetime.now().strftime("%Y-%m-%d 08:30:00"),
                action="SYSTEM_INIT",
                planner_id="SYSTEM",
                scenario_summary="Initial 7-day Supplier A disruption scenario loaded.",
                plan_cost=0.0,
                fill_rate=100.0,
                notes="Network baseline initialized."
            )
        ]
        
    if "plan_approval_status" not in st.session_state:
        st.session_state.plan_approval_status = "PENDING_REVIEW"  # "APPROVED", "REJECTED", "PENDING_REVIEW"
        
    if "workflow_execution" not in st.session_state or st.session_state.get("force_recompute", False):
        run_multi_agent_workflow()
        st.session_state.force_recompute = False

def run_multi_agent_workflow():
    """Runs the full multi-agent collaborative workflow and updates session state."""
    coordinator = CoordinatorAgent(
        st.session_state.suppliers_df,
        st.session_state.inventory_df,
        st.session_state.demand_df
    )
    result = coordinator.execute_workflow(st.session_state.active_scenario)
    st.session_state.workflow_execution = result
    st.session_state.recovery_plan = result["recovery_plan"]
    
    # Also run benchmark
    optimizer = SupplyChainOptimizer(
        st.session_state.suppliers_df,
        st.session_state.inventory_df,
        st.session_state.demand_df
    )
    st.session_state.benchmark_results = optimizer.run_benchmark_comparison(st.session_state.active_scenario)

def record_audit(action: str, planner_id: str, notes: str):
    """Records an action in the immutable audit log."""
    plan: RecoveryPlanResult = st.session_state.recovery_plan
    record = AuditRecord(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        action=action,
        planner_id=planner_id,
        scenario_summary=f"Supplier {st.session_state.active_scenario.disrupted_supplier_id} ({st.session_state.active_scenario.duration_days}d shutdown)",
        plan_cost=plan.total_landed_cost,
        fill_rate=plan.fulfillment_rate,
        notes=notes
    )
    st.session_state.audit_history.insert(0, record)
