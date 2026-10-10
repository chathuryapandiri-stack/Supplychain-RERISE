"""
ResilientAI - Logistics Agent
Evaluates freight modes, transit lead times, expedited shipping feasibility, and landed transport costs.
"""

import pandas as pd
from typing import Dict, Any, List
from core.models import AgentProposal, DisruptionScenario

class LogisticsAgent:
    def __init__(self, suppliers_df: pd.DataFrame):
        self.suppliers_df = suppliers_df.copy()
        self.name = "Logistics Agent"
        self.role = "Freight Mode Optimization & Lead Time Feasibility"
        self.status = "ACTIVE"
        
    def analyze(self, scenario: DisruptionScenario, inventory_findings: Dict[str, Any]) -> Dict[str, Any]:
        days_to_stockout = float(inventory_findings.get("runout_days", 2.0))
        stockout_day = int(inventory_findings.get("stockout_day", 3))
        disrupted_id = scenario.disrupted_supplier_id
        
        # Candidates are operational suppliers excluding disrupted
        candidates = self.suppliers_df[
            (self.suppliers_df["supplier_id"] != disrupted_id) &
            (~self.suppliers_df["status"].str.contains("DISRUPTED|SHUTDOWN", case=False, na=False))
        ].copy()
        if candidates.empty:
            candidates = self.suppliers_df[self.suppliers_df["supplier_id"] != disrupted_id].copy()
        
        lane_evaluations = []
        requires_expedite = False
        
        for _, row in candidates.iterrows():
            std_lt = int(row["std_lead_time_days"])
            exp_lt = int(row["expedite_lead_time_days"])
            std_cost = float(row["std_freight_cost"])
            exp_cost = float(row["expedite_freight_cost"])
            
            # Check timing against stockout day
            std_feasible_before_stockout = (std_lt <= days_to_stockout)
            exp_feasible_before_stockout = (exp_lt <= days_to_stockout + 0.5)
            
            if not std_feasible_before_stockout:
                requires_expedite = True
                
            lane_evaluations.append({
                "supplier_id": row["supplier_id"],
                "name": row["name"],
                "std_lead_time_days": std_lt,
                "exp_lead_time_days": exp_lt,
                "std_arrival_day": 1 + std_lt,
                "exp_arrival_day": 1 + exp_lt,
                "std_freight_cost": std_cost,
                "exp_freight_cost": exp_cost,
                "freight_premium_per_unit": round(exp_cost - std_cost, 2),
                "std_causes_stockout": not std_feasible_before_stockout,
                "expedite_bridges_gap": exp_feasible_before_stockout
            })
            
        proposal = AgentProposal(
            agent_name=self.name,
            action_type="FREIGHT_MODE_RECOMMENDATION",
            parameters={
                "mandatory_initial_expedite": requires_expedite,
                "lanes": lane_evaluations,
                "recommended_mode": "HYBRID_FREIGHT_DISPATCH"
            },
            confidence_score=0.97,
            rationale=(
                f"Plant inventory depletes on Day {stockout_day}. Standard ground/ocean freight requires 4-5 days "
                f"which risks line starvation before standard replenishment arrives. "
                f"Emergency Air Expediting arrives on Day 3 morning, directly averting line starvation. "
                f"Recommend immediate Phase 1 Expedited dispatch, followed by Phase 2 Standard freight to control costs."
            ),
            estimated_cost=1300 * 15.5,
            trade_off_notes="Expedited air freight adds premium, but prevents $15,000/day idle plant penalties and customer backorders."
        )
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "requires_expedite": requires_expedite,
                "lanes": lane_evaluations,
                "recommended_policy": "HYBRID_TWO_PHASE_EXPEDITE"
            },
            "proposal": proposal
        }
