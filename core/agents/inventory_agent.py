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
        # Focus on the disrupted component: MCU-900
        mcu_row = self.inventory_df[self.inventory_df["item_id"] == "MCU-900"].iloc[0]
        
        current_stock = int(mcu_row["current_stock"])
        safety_stock = int(mcu_row["safety_stock"])
        avg_daily_burn = float(demand_findings.get("avg_daily_demand", 430.0))
        
        runout_days = round(current_stock / avg_daily_burn, 2)
        stockout_day = int(current_stock // avg_daily_burn) + 1
        
        # Shortage during disruption window if 0 incoming supply
        disruption_demand = demand_findings.get("disruption_window_units", 3010)
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
                "current_stock": current_stock,
                "safety_stock_target": safety_stock,
                "days_to_stockout": runout_days,
                "projected_stockout_day": stockout_day,
                "net_shortage_units": net_shortage_window,
                "holding_cost_daily": float(mcu_row["holding_cost_per_day"]),
                "buffer_health": buffer_health
            },
            confidence_score=0.98,
            rationale=(
                f"Plant Alpha holds {current_stock} units of MCU-900 against a daily consumption of {avg_daily_burn} units. "
                f"Current inventory will be EXHAUSTED in {runout_days} days (Day {stockout_day}). "
                f"Assembly lines will halt on Day 3 without inbound shipments. "
                f"Net deficit during 7-day disruption is {net_shortage_window:,} units."
            ),
            estimated_cost=current_stock * float(mcu_row["holding_cost_per_day"]) * 7,
            trade_off_notes="Replenishing immediately avoids line stoppage and idle labor ($15,000/day) at the expense of expedited freight costs."
        )
        
        return {
            "agent": self.name,
            "status": "COMPLETED",
            "findings": {
                "component": "MCU-900 Control Chipset",
                "current_stock": current_stock,
                "safety_stock": safety_stock,
                "runout_days": runout_days,
                "stockout_day": stockout_day,
                "net_shortage_units": net_shortage_window,
                "buffer_health": buffer_health
            },
            "proposal": proposal
        }
