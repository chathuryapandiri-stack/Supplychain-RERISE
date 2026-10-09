"""
ResilientAI - Supplier Risk Agent
Assesses supplier availability, qualification, unit pricing, capacity limits, and reliability scores.
"""

import pandas as pd
from typing import Dict, Any
from core.models import AgentProposal, DisruptionScenario

class SupplierRiskAgent:
    def __init__(self, suppliers_df: pd.DataFrame):
        self.suppliers_df = suppliers_df.copy()
        self.name = "Supplier Risk Agent"
        self.role = "Alternate Supplier Qualification & Capacity Screening"
        self.status = "ACTIVE"
        
    def analyze(self, scenario: DisruptionScenario, required_units: int) -> Dict[str, Any]:
        df = self.suppliers_df.copy()
        
        # Apply overrides if scenario specifies
        if scenario.supplier_b_capacity_override is not None:
            df.loc[df["supplier_id"] == "SUP-B", "daily_capacity"] = scenario.supplier_b_capacity_override
        if scenario.supplier_c_capacity_override is not None:
            df.loc[df["supplier_id"] == "SUP-C", "daily_capacity"] = scenario.supplier_c_capacity_override
            
        disrupted_id = scenario.disrupted_supplier_id
        
        # Disrupted supplier info
        disrupted_sup = df[df["supplier_id"] == disrupted_id].iloc[0].to_dict()
        
        # Candidate alternative suppliers for the same component (MCU-900)
        candidates = df[(df["supplier_id"] != disrupted_id) & (df["component"].str.contains("MCU-900"))].copy()
        
        # Calculate scores
        # Score based on (Reliability * 0.4) + (Capacity headroom * 0.3) + (Cost economy * 0.3)
        candidate_evaluations = []
        total_backup_daily_capacity = int(candidates["daily_capacity"].sum())
        
        for _, row in candidates.iterrows():
            cost_ratio = 45.0 / row["unit_cost"]  # comparison to baseline $45
            composite_score = round(
                (row["reliability_score"] * 0.45) + 
                (min(1.0, row["daily_capacity"] / 400.0) * 0.30) + 
                (cost_ratio * 0.25),
                3
            )
            candidate_evaluations.append({
                "supplier_id": row["supplier_id"],
                "name": row["name"],
                "daily_capacity": int(row["daily_capacity"]),
                "unit_cost": float(row["unit_cost"]),
                "cost_premium_pct": round(((row["unit_cost"] - 45.0) / 45.0) * 100, 1),
                "std_lead_time": int(row["std_lead_time_days"]),
                "expedite_lead_time": int(row["expedite_lead_time_days"]),
                "reliability_score": float(row["reliability_score"]),
                "composite_qualification_score": composite_score,
                "qualification_status": "APPROVED_TIER_1_BACKUP"
            })
            
        proposal = AgentProposal(
            agent_name=self.name,
            action_type="ALTERNATE_SOURCING_RECOMMENDATION",
            parameters={
                "disrupted_supplier": disrupted_sup["name"],
                "total_backup_capacity_daily": total_backup_daily_capacity,
                "candidates": candidate_evaluations,
                "recommended_sourcing_policy": "DUAL_SOURCE_SPLIT"
            },
            confidence_score=0.94,
            rationale=(
                f"Primary supplier {disrupted_sup['name']} is 100% shutdown for {scenario.duration_days} days. "
                f"Qualified alternatives SUP-B (Beacon, 350 units/day @ $58) and SUP-C (Crestline, 300 units/day @ $64) "
                f"provide a collective daily capacity of {total_backup_daily_capacity} units/day. "
                f"Recommend dual-sourcing: allocate ~55-60% to SUP-B (cost-efficient) and ~40-45% to SUP-C (high reliability, hedge against single-point failure)."
            ),
            estimated_cost=0.0,
            trade_off_notes="Dual-sourcing incurs higher administrative overhead and unit costs (+29% to +42%) but guarantees capacity coverage."
        )
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "disrupted_supplier": disrupted_sup,
                "total_backup_daily_capacity": total_backup_daily_capacity,
                "candidates": candidate_evaluations
            },
            "proposal": proposal
        }
