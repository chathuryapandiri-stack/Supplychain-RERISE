"""
ResilientAI - Inventory Monitoring Agent
Monitors stock levels, safety stock buffers, runout calculations, and line starvation risk.
"""

import pandas as pd
from typing import Dict, Any
from core.models import AgentProposal, DisruptionScenario

class InventoryAgent:
    def __init__(self, inventory_df: pd.DataFrame):
        self.inventory_df = inventory_df.copy()
        self.name = "Inventory Monitoring Agent"
        self.role = "Buffer Analysis & Stockout Runway Prediction"
        self.status = "ACTIVE"
        
    def analyze(self, scenario: DisruptionScenario, demand_findings: Dict[str, Any]) -> Dict[str, Any]:
        # Dynamically select critical component from inventory buffers
        crit_row = self.inventory_df.iloc[0]
        for _, row in self.inventory_df.iterrows():
            if "control" in str(row["item_name"]).lower() or "chip" in str(row["item_name"]).lower() or "sensor" in str(row["item_name"]).lower() or "fpga" in str(row["item_name"]).lower() or "sic" in str(row["item_name"]).lower() or "mcu" in str(row["item_id"]).lower():
                crit_row = row
                break
                
        item_id = str(crit_row["item_id"])
        item_name = str(crit_row["item_name"])
        current_stock = int(crit_row["current_stock"])
        safety_stock = int(crit_row["safety_stock"])
        avg_daily_burn = float(demand_findings.get("avg_daily_demand", 430.0))
        
        runout_days = round(current_stock / max(1.0, avg_daily_burn), 2)
        stockout_day = int(current_stock // max(1.0, avg_daily_burn)) + 1
        
        # Shortage during disruption window if 0 incoming supply
        disruption_demand = demand_findings.get("disruption_window_units", int(avg_daily_burn * scenario.duration_days))
        net_shortage_window = max(0, disruption_demand - current_stock)
        
        # Buffer health categorization
        if runout_days < 3.0:
            buffer_health = "CRITICAL_DEFICIT"
        elif runout_days < 7.0:
            buffer_health = "MODERATE_RISK"
        else:
            buffer_health = "ADEQUATE"
            
        proposal = AgentProposal(
            agent_name=self.name,
            action_type="EMERGENCY_REPLENISHMENT_FLAG",
            parameters={
                "item_id": item_id,
                "item_name": item_name,
                "current_stock": current_stock,
                "safety_stock_target": safety_stock,
                "days_to_stockout": runout_days,
                "projected_stockout_day": stockout_day,
                "net_shortage_units": net_shortage_window,
                "holding_cost_daily": float(crit_row["holding_cost_per_day"]),
                "buffer_health": buffer_health
            },
            confidence_score=0.98,
            rationale=(
                f"Plant Alpha holds {current_stock} units of {item_name} against a daily consumption of {avg_daily_burn} units. "
                f"Current inventory will be exhausted in {runout_days} days (Day {stockout_day}). "
                f"Assembly lines will halt on Day {stockout_day} without inbound shipments. "
                f"Net deficit during {scenario.duration_days}-day disruption is {net_shortage_window:,} units."
            ),
            estimated_cost=current_stock * float(crit_row["holding_cost_per_day"]) * scenario.duration_days,
            trade_off_notes="Replenishing immediately avoids line stoppage and idle labor ($15,000/day) at the expense of expedited freight costs."
        )
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "component": item_name,
                "item_id": item_id,
                "current_stock": current_stock,
                "safety_stock": safety_stock,
                "runout_days": runout_days,
                "stockout_day": stockout_day,
                "net_shortage_units": net_shortage_window,
                "buffer_health": buffer_health
            },
            "proposal": proposal
        }
