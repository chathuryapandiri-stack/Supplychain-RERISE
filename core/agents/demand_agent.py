"""
ResilientAI - Demand Sensing Agent
Analyzes customer demand, priority tiers, and required component volume.
"""

import pandas as pd
from typing import Dict, Any
from core.models import AgentProposal, DisruptionScenario

class DemandAgent:
    def __init__(self, demand_df: pd.DataFrame):
        self.demand_df = demand_df.copy()
        self.name = "Demand Sensing Agent"
        self.role = "Demand Sensing & Priority Classification"
        self.status = "ACTIVE"
        
    def analyze(self, scenario: DisruptionScenario) -> Dict[str, Any]:
        df = self.demand_df.copy()
        if scenario.demand_shock_pct != 0:
            df["demand_units"] = (df["demand_units"] * (1.0 + scenario.demand_shock_pct / 100.0)).round().astype(int)
            
        disruption_days = scenario.duration_days
        
        # Demand during disruption window (Days 1 to disruption_days)
        disruption_window_df = df[df["day"] <= disruption_days]
        total_disruption_demand = int(disruption_window_df["demand_units"].sum())
        
        # 14-Day Full Horizon Demand
        total_horizon_demand = int(df["demand_units"].sum())
        avg_daily_demand = round(total_horizon_demand / df["day"].nunique(), 1)
        
        # Tier breakdown
        tier_summary = df.groupby("tier")["demand_units"].sum().to_dict()
        tier_names = {1: "Tier 1 (Critical Healthcare/Defense)", 2: "Tier 2 (Enterprise Telecom)", 3: "Tier 3 (Commercial Retail)"}
        
        tier_breakdown_formatted = [
            {
                "tier": t,
                "label": tier_names.get(t, f"Tier {t}"),
                "units": int(tier_summary.get(t, 0)),
                "pct": round(tier_summary.get(t, 0) / total_horizon_demand * 100, 1)
            }
            for t in sorted(tier_summary.keys())
        ]
        
        proposal = AgentProposal(
            agent_name=self.name,
            action_type="DEMAND_SENSING_AND_PROTECTION",
            parameters={
                "avg_daily_burn": avg_daily_demand,
                "disruption_window_units": total_disruption_demand,
                "total_horizon_units": total_horizon_demand,
                "tier_breakdown": tier_breakdown_formatted,
                "recommended_tier_protection": "Strict Tier 1 Allocation Guarantee"
            },
            confidence_score=0.96,
            rationale=(
                f"During the {disruption_days}-day supplier outage, total manufacturing demand is "
                f"{total_disruption_demand:,} units (avg {avg_daily_demand} units/day). "
                f"Tier 1 critical demand represents {tier_summary.get(1, 0):,} units with severe penalty costs "
                f"($180/unit). Recommend absolute prioritization of Tier 1 order allocations."
            ),
            estimated_cost=0.0,
            trade_off_notes="Prioritizing Tier 1 avoids $180/unit penalties but may defer Tier 3 retail orders if supply is tight."
        )
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "avg_daily_demand": avg_daily_demand,
                "disruption_window_units": total_disruption_demand,
                "total_horizon_units": total_horizon_demand,
                "tier_summary": tier_breakdown_formatted
            },
            "proposal": proposal
        }
