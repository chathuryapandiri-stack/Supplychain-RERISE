"""
ResilientAI - Core Data Models and Synthetic Dataset Generator
Reproducible Three-Echelon Supply Chain Network Dataset
"""

import os
import pandas as pd
from typing import Dict, Any, Optional
from core.mock_data_generator import MockDataGenerator, generate_scenario_dataset, INDUSTRY_PRESETS

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def get_default_suppliers_df() -> pd.DataFrame:
    gen = MockDataGenerator("industrial_iot", seed=42)
    return gen.generate_suppliers_df(
        disrupted_supplier_id="SUP-A",
        duration_days=7,
        capacity_drop_pct=100.0
    )

def get_default_inventory_df() -> pd.DataFrame:
    gen = MockDataGenerator("industrial_iot", seed=42)
    return gen.generate_inventory_df(
        daily_burn_rate=430.0,
        initial_stock_days=2.08,
        safety_stock_days=1.05
    )

def get_default_demand_df() -> pd.DataFrame:
    gen = MockDataGenerator("industrial_iot", seed=42)
    return gen.generate_demand_df(
        horizon_days=14,
        daily_mean_demand=430.0,
        volatility_pct=0.06
    )

def get_default_bom_df() -> pd.DataFrame:
    gen = MockDataGenerator("industrial_iot", seed=42)
    return gen.generate_bom_df()

def get_default_network_nodes() -> Dict[str, Any]:
    gen = MockDataGenerator("industrial_iot", seed=42)
    return gen.generate_network_nodes()

def initialize_data_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    sup_path = os.path.join(DATA_DIR, "suppliers.csv")
    inv_path = os.path.join(DATA_DIR, "inventory.csv")
    dem_path = os.path.join(DATA_DIR, "demand.csv")
    
    if not os.path.exists(sup_path):
        get_default_suppliers_df().to_csv(sup_path, index=False)
    if not os.path.exists(inv_path):
        get_default_inventory_df().to_csv(inv_path, index=False)
    if not os.path.exists(dem_path):
        get_default_demand_df().to_csv(dem_path, index=False)

if __name__ == "__main__":
    initialize_data_files()
    print("Default datasets generated successfully.")
