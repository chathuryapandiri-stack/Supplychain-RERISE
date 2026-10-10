"""
ResilientAI - Data Models and Schema Definitions
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DisruptionScenario:
    disrupted_supplier_id: str = "SUP-A"
    duration_days: int = 7
    capacity_drop_pct: float = 100.0  # 100% shutdown
    demand_shock_pct: float = 0.0     # +/- % shift in customer demand
    supplier_b_capacity_override: Optional[int] = None
    supplier_c_capacity_override: Optional[int] = None
    supplier_capacity_overrides: Dict[str, int] = field(default_factory=dict)
    expedite_available: bool = True

@dataclass
class AgentProposal:
    agent_name: str
    action_type: str  # e.g., "SENSE_DEMAND", "EXPEDITE_PO", "SPLIT_ALLOCATION", "TIER_RATIONING"
    parameters: Dict[str, Any]
    confidence_score: float
    rationale: str
    estimated_cost: float
    trade_off_notes: str

@dataclass
class SupplierAllocation:
    supplier_id: str
    supplier_name: str
    allocated_units: int
    shipping_mode: str  # "EXPEDITED_AIR" or "STANDARD_FREIGHT"
    lead_time_days: int
    arrival_day: int
    unit_cost: float
    freight_cost_per_unit: float
    total_cost: float

@dataclass
class ConstraintCheckResult:
    constraint_name: str
    status: str  # "PASSED", "WARNING", "VIOLATED"
    message: str
    metric_value: Any
    threshold: Any

@dataclass
class RecoveryPlanResult:
    scenario: DisruptionScenario
    allocations: List[SupplierAllocation]
    total_material_cost: float
    total_freight_cost: float
    total_holding_cost: float
    total_backorder_penalty: float
    total_landed_cost: float
    fulfillment_rate: float
    unmet_demand_units: int
    recovery_time_days: int
    stockout_duration_days: int
    constraints_status: List[ConstraintCheckResult]
    is_feasible: bool
    confidence_score: float
    executive_summary: str
    trade_off_analysis: Dict[str, Any]
    agent_proposals: List[AgentProposal] = field(default_factory=list)

@dataclass
class AuditRecord:
    timestamp: str
    action: str  # "PLAN_APPROVED", "PLAN_REJECTED", "WHAT_IF_TESTED", "OVERRIDE"
    planner_id: str
    scenario_summary: str
    plan_cost: float
    fill_rate: float
    notes: str
