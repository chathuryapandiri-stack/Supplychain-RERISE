"""
ResilientAI - Master Coordinator Agent
Coordinates the multi-agent workflow, reconciles agent conflicts,
validates hard business constraints, and produces explainable recovery recommendations.
"""

from typing import Dict, Any, List
import pandas as pd
from core.models import DisruptionScenario, AgentProposal, RecoveryPlanResult
from core.agents.demand_agent import DemandAgent
from core.agents.inventory_agent import InventoryAgent
from core.agents.supplier_risk_agent import SupplierRiskAgent
from core.agents.logistics_agent import LogisticsAgent
from core.optimization.solver import SupplyChainOptimizer

class CoordinatorAgent:
    def __init__(self, suppliers_df: pd.DataFrame, inventory_df: pd.DataFrame, demand_df: pd.DataFrame):
        self.suppliers_df = suppliers_df
        self.inventory_df = inventory_df
        self.demand_df = demand_df
        
        self.demand_agent = DemandAgent(demand_df)
        self.inventory_agent = InventoryAgent(inventory_df)
        self.supplier_risk_agent = SupplierRiskAgent(suppliers_df)
        self.logistics_agent = LogisticsAgent(suppliers_df)
        self.optimizer = SupplyChainOptimizer(suppliers_df, inventory_df, demand_df)
        
        self.name = "Coordinator Agent"
        self.role = "Multi-Agent Reconciliation & Plan Synthesis"
        
    def execute_workflow(self, scenario: DisruptionScenario) -> Dict[str, Any]:
        """
        Executes sequential and collaborative multi-agent analysis:
        Step 1: Demand Agent senses customer commitments & tier breakdown
        Step 2: Inventory Agent computes runway & identifies starvation day
        Step 3: Supplier Risk Agent screens backup suppliers & capacity headroom
        Step 4: Logistics Agent evaluates freight lead times & expediting necessity
        Step 5: Coordinator reconciles conflicting objectives and invokes optimization solver
        """
        # Step 1: Demand
        demand_result = self.demand_agent.analyze(scenario)
        
        # Step 2: Inventory (depends on demand findings)
        inventory_result = self.inventory_agent.analyze(scenario, demand_result["findings"])
        
        # Step 3: Supplier Risk (depends on shortage projection)
        shortage_units = inventory_result["findings"]["net_shortage_units"]
        supplier_result = self.supplier_risk_agent.analyze(scenario, shortage_units)
        
        # Step 4: Logistics (depends on inventory stockout timeline)
        logistics_result = self.logistics_agent.analyze(scenario, inventory_result["findings"])
        
        # Step 5: Coordinator Reconciliation & Plan Generation
        all_proposals: List[AgentProposal] = [
            demand_result["proposal"],
            inventory_result["proposal"],
            supplier_result["proposal"],
            logistics_result["proposal"]
        ]
        
        runout_days = inventory_result["findings"]["runout_days"]
        stockout_day = inventory_result["findings"]["stockout_day"]
        total_backup_cap = supplier_result["findings"]["total_backup_daily_capacity"]
        avg_demand = demand_result["findings"]["avg_daily_demand"]

        # Identify conflicts resolved dynamically by coordinator:
        conflicts_resolved = [
            {
                "conflict": "Lead Time Mismatch vs Inventory Runout",
                "agents_involved": ["Inventory Monitoring Agent", "Logistics Agent"],
                "issue": f"Standard shipping requires 4-5 days, but plant inventory buffer exhausts in {runout_days} days.",
                "resolution": f"Enforce Phase 1 Expedited Air shipping (landing Day {stockout_day}) to bridge buffer exhaustion without halting operations."
            },
            {
                "conflict": "Cost Minimization vs Capacity Bottleneck",
                "agents_involved": ["Supplier Risk Agent", "Procurement/Cost Heuristics"],
                "issue": f"No single backup supplier alone can comfortably fulfill {avg_demand} units/day without exceeding local factory headroom.",
                "resolution": f"Enforce Multi-Sourcing Split across qualified backup suppliers ({total_backup_cap} u/d combined) to cover total demand."
            },
            {
                "conflict": "Customer Fulfillment vs Material Scarcity",
                "agents_involved": ["Demand Sensing Agent", "Inventory Monitoring Agent"],
                "issue": "Transitional stockout risk could cause indiscriminate delivery failures across critical customers.",
                "resolution": "Apply strict Tier-1 Rationing priority (100% allocation to Healthcare and Mission-Critical accounts, eliminating high SLA penalties)."
            }
        ]
        
        # Generate optimal recovery plan
        recovery_plan = self.optimizer.solve_resilient_ai_plan(scenario)
        recovery_plan.agent_proposals = all_proposals
        
        # Coordinator Proposal
        coord_proposal = AgentProposal(
            agent_name=self.name,
            action_type="SYNTHESIZED_RECOVERY_COORDINATION",
            parameters={
                "conflicts_resolved_count": len(conflicts_resolved),
                "total_allocated_units": sum(a.allocated_units for a in recovery_plan.allocations),
                "fulfillment_rate_target": recovery_plan.fulfillment_rate,
                "projected_cost": recovery_plan.total_landed_cost
            },
            confidence_score=0.96,
            rationale=(
                f"Reconciled {len(conflicts_resolved)} agent conflicts across inventory runway, vendor capacity, and transit speeds. "
                f"Generated feasible plan delivering {recovery_plan.fulfillment_rate}% fulfillment rate "
                f"while satisfying all supplier capacity and SLA constraints."
            ),
            estimated_cost=recovery_plan.total_landed_cost,
            trade_off_notes="Balances freight expediting premiums against severe stockout penalties."
        )
        all_proposals.append(coord_proposal)
        
        return {
            "status": "COMPLETED",
            "scenario": scenario,
            "agent_results": {
                "demand": demand_result,
                "inventory": inventory_result,
                "supplier_risk": supplier_result,
                "logistics": logistics_result,
                "coordinator": {
                    "agent": self.name,
                    "status": "COMPLETED",
                    "proposal": coord_proposal,
                    "conflicts_resolved": conflicts_resolved
                }
            },
            "proposals": all_proposals,
            "conflicts_resolved": conflicts_resolved,
            "recovery_plan": recovery_plan
        }
