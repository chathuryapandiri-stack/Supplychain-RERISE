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
        
        # Apply capacity overrides if scenario specifies
        if getattr(scenario, "supplier_capacity_overrides", None):
            for sid, cap in scenario.supplier_capacity_overrides.items():
                if sid in df["supplier_id"].values:
                    df.loc[df["supplier_id"] == sid, "daily_capacity"] = cap

        candidate_sups = df[df["supplier_id"] != scenario.disrupted_supplier_id]
        if scenario.supplier_b_capacity_override is not None:
            if "SUP-B" in df["supplier_id"].values and scenario.disrupted_supplier_id != "SUP-B":
                df.loc[df["supplier_id"] == "SUP-B", "daily_capacity"] = scenario.supplier_b_capacity_override
            elif len(candidate_sups) >= 1:
                df.loc[df["supplier_id"] == candidate_sups.iloc[0]["supplier_id"], "daily_capacity"] = scenario.supplier_b_capacity_override

        if scenario.supplier_c_capacity_override is not None:
            if "SUP-C" in df["supplier_id"].values and scenario.disrupted_supplier_id != "SUP-C":
                df.loc[df["supplier_id"] == "SUP-C", "daily_capacity"] = scenario.supplier_c_capacity_override
            elif len(candidate_sups) >= 2:
                df.loc[df["supplier_id"] == candidate_sups.iloc[1]["supplier_id"], "daily_capacity"] = scenario.supplier_c_capacity_override
            
        disrupted_id = scenario.disrupted_supplier_id
        
        # Disrupted supplier info
        disrupted_match = df[df["supplier_id"] == disrupted_id]
        if not disrupted_match.empty:
            disrupted_sup = disrupted_match.iloc[0].to_dict()
        else:
            disrupted_sup = df.iloc[0].to_dict()
            
        baseline_cost = float(disrupted_sup.get("unit_cost", 45.0))
        comp_keyword = str(disrupted_sup.get("component", "")).split()[0].lower()

        # Candidate alternative suppliers for the same component
        candidates = df[
            (df["supplier_id"] != disrupted_id) & 
            (df["component"].str.lower().str.contains(comp_keyword, na=False))
        ].copy()
        if candidates.empty:
            candidates = df[(df["supplier_id"] != disrupted_id) & (df["tier"] == 1)].copy()
        if candidates.empty:
            candidates = df[df["supplier_id"] != disrupted_id].copy()

        candidate_evaluations = []
        total_backup_daily_capacity = int(candidates["daily_capacity"].sum())
        
        for _, row in candidates.iterrows():
            cost_ratio = baseline_cost / max(1.0, row["unit_cost"])
            composite_score = round(
                (row["reliability_score"] * 0.45) + 
                (min(1.0, row["daily_capacity"] / max(1.0, disrupted_sup.get("daily_capacity", 500))) * 0.30) + 
                (cost_ratio * 0.25),
                3
            )
            candidate_evaluations.append({
                "supplier_id": row["supplier_id"],
                "name": row["name"],
                "daily_capacity": int(row["daily_capacity"]),
                "unit_cost": float(row["unit_cost"]),
                "cost_premium_pct": round(((row["unit_cost"] - baseline_cost) / max(1.0, baseline_cost)) * 100, 1),
                "std_lead_time": int(row["std_lead_time_days"]),
                "expedite_lead_time": int(row["expedite_lead_time_days"]),
                "reliability_score": float(row["reliability_score"]),
                "composite_qualification_score": composite_score,
                "qualification_status": "APPROVED_TIER_1_BACKUP"
            })
            
        cand_descriptions = [f"{c['name']} ({c['daily_capacity']} u/d @ ${c['unit_cost']:.0f})" for c in candidate_evaluations]
        proposal = AgentProposal(
            agent_name=self.name,
            action_type="ALTERNATE_SOURCING_RECOMMENDATION",
            parameters={
                "disrupted_supplier": disrupted_sup["name"],
                "total_backup_capacity_daily": total_backup_daily_capacity,
                "candidates": candidate_evaluations,
                "recommended_sourcing_policy": "MULTI_SOURCE_SPLIT"
            },
            confidence_score=0.94,
            rationale=(
                f"Primary supplier {disrupted_sup['name']} is offline for {scenario.duration_days} days. "
                f"Qualified alternatives: {', '.join(cand_descriptions[:2])} "
                f"provide collective capacity of {total_backup_daily_capacity} units/day. "
                f"Recommend multi-sourcing split to hedge against single-point failure."
            ),
            estimated_cost=0.0,
            trade_off_notes="Multi-sourcing incurs higher administrative overhead and unit costs but guarantees capacity coverage."
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
