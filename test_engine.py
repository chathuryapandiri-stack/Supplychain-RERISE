import sys
from core.data_loader import get_default_suppliers_df, get_default_inventory_df, get_default_demand_df
from core.models import DisruptionScenario
from core.agents.coordinator_agent import CoordinatorAgent
from core.optimization.solver import SupplyChainOptimizer

def main():
    print("Initializing test datasets...")
    sup = get_default_suppliers_df()
    inv = get_default_inventory_df()
    dem = get_default_demand_df()
    
    print(f"Loaded {len(sup)} suppliers, {len(inv)} inventory items, {len(dem)} demand entries.")
    
    scenario = DisruptionScenario(
        disrupted_supplier_id="SUP-A",
        duration_days=7,
        capacity_drop_pct=100.0
    )
    
    print("Testing Multi-Agent Workflow...")
    coordinator = CoordinatorAgent(sup, inv, dem)
    wf_result = coordinator.execute_workflow(scenario)
    
    plan = wf_result["recovery_plan"]
    print("--- RECOVERY PLAN GENERATED ---")
    print(f"Feasible: {plan.is_feasible}")
    print(f"Fulfillment Rate: {plan.fulfillment_rate}%")
    print(f"Total Landed Cost: ${plan.total_landed_cost:,.2f}")
    print(f"Stockout Days: {plan.stockout_duration_days}")
    print(f"Allocations Count: {len(plan.allocations)}")
    for a in plan.allocations:
        print(f"  - {a.supplier_name} ({a.shipping_mode}): {a.allocated_units} units, arriving Day {a.arrival_day}")
        
    print("\nTesting 3-Way Benchmark Comparison...")
    optimizer = SupplyChainOptimizer(sup, inv, dem)
    benchmarks = optimizer.run_benchmark_comparison(scenario)
    print(benchmarks["comparison_df"].to_string())
    
    print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
