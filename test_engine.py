import sys
from core.data_loader import get_default_suppliers_df, get_default_inventory_df, get_default_demand_df
from core.mock_data_generator import generate_scenario_dataset, INDUSTRY_PRESETS
from core.models import DisruptionScenario
from core.agents.coordinator_agent import CoordinatorAgent
from core.optimization.solver import SupplyChainOptimizer

def main():
    print("Initializing standard test datasets...")
    sup = get_default_suppliers_df()
    inv = get_default_inventory_df()
    dem = get_default_demand_df()
    
    print(f"Loaded {len(sup)} suppliers, {len(inv)} inventory items, {len(dem)} demand entries.")
    
    scenario = DisruptionScenario(
        disrupted_supplier_id="SUP-A",
        duration_days=7,
        capacity_drop_pct=100.0
    )
    
    print("Testing Multi-Agent Workflow on Default Baseline...")
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
    
    print("\nTesting Parametric Mock Data Generator across all industry presets...")
    for preset_key in INDUSTRY_PRESETS.keys():
        print(f"  --> Testing preset: {preset_key}...")
        bundle = generate_scenario_dataset(
            preset=preset_key,
            num_suppliers=4,
            disruption_severity="critical",
            demand_volatility="moderate",
            inventory_buffer_days=3.0,
            seed=101
        )
        assert len(bundle["suppliers_df"]) >= 3, "Suppliers generation failed"
        assert len(bundle["inventory_df"]) >= 1, "Inventory generation failed"
        assert len(bundle["demand_df"]) >= 10, "Demand generation failed"
        
        test_scen = DisruptionScenario(
            disrupted_supplier_id=bundle["disrupted_supplier_id"],
            duration_days=7
        )
        test_coord = CoordinatorAgent(bundle["suppliers_df"], bundle["inventory_df"], bundle["demand_df"])
        test_res = test_coord.execute_workflow(test_scen)
        test_plan = test_res["recovery_plan"]
        assert test_plan.fulfillment_rate > 0, f"Fulfillment rate 0 for preset {preset_key}"
        print(f"      [OK] Fill rate: {test_plan.fulfillment_rate}%, Landed cost: ${test_plan.total_landed_cost:,.2f}, Feasible: {test_plan.is_feasible}")
        
    print("\nALL VERIFICATIONS AND PRESETS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()

