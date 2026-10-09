"""
ResilientAI - Core Data Models and Synthetic Dataset Generator
Reproducible Three-Echelon Supply Chain Network Dataset
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def get_default_suppliers_df():
    data = [
        {
            "supplier_id": "SUP-A",
            "name": "Apex Microelectronics (Primary)",
            "tier": 1,
            "component": "MCU-900 Control Chipset",
            "status": "DISRUPTED (7-Day Shutdown)",
            "daily_capacity": 500,
            "unit_cost": 45.0,
            "std_lead_time_days": 3,
            "expedite_lead_time_days": 2,
            "std_freight_cost": 4.5,
            "expedite_freight_cost": 14.0,
            "reliability_score": 0.98,
            "risk_index": 0.89,  # High risk due to shutdown
            "is_critical": True
        },
        {
            "supplier_id": "SUP-B",
            "name": "Beacon Tech Solutions (Backup 1)",
            "tier": 1,
            "component": "MCU-900 Control Chipset",
            "status": "OPERATIONAL",
            "daily_capacity": 350,
            "unit_cost": 58.0,
            "std_lead_time_days": 5,
            "expedite_lead_time_days": 2,
            "std_freight_cost": 6.0,
            "expedite_freight_cost": 16.5,
            "reliability_score": 0.92,
            "risk_index": 0.18,
            "is_critical": False
        },
        {
            "supplier_id": "SUP-C",
            "name": "Crestline Components (Backup 2)",
            "tier": 1,
            "component": "MCU-900 Control Chipset",
            "status": "OPERATIONAL",
            "daily_capacity": 300,
            "unit_cost": 64.0,
            "std_lead_time_days": 4,
            "expedite_lead_time_days": 2,
            "std_freight_cost": 5.5,
            "expedite_freight_cost": 15.0,
            "reliability_score": 0.96,
            "risk_index": 0.12,
            "is_critical": False
        },
        {
            "supplier_id": "SUP-D",
            "name": "Delta Raw Forge (Chassis)",
            "tier": 2,
            "component": "Enclosure Chassis CH-10",
            "status": "OPERATIONAL",
            "daily_capacity": 600,
            "unit_cost": 22.0,
            "std_lead_time_days": 2,
            "expedite_lead_time_days": 1,
            "std_freight_cost": 3.0,
            "expedite_freight_cost": 8.0,
            "reliability_score": 0.99,
            "risk_index": 0.05,
            "is_critical": False
        }
    ]
    return pd.DataFrame(data)

def get_default_inventory_df():
    data = [
        {
            "item_id": "MCU-900",
            "item_name": "MCU-900 Control Chipset",
            "location": "Plant Alpha (Central)",
            "current_stock": 900,
            "safety_stock": 450,
            "daily_burn_rate": 450,
            "runout_days": 2.0,
            "holding_cost_per_day": 0.85,
            "stockout_penalty_per_unit": 110.0,
            "unit": "Units"
        },
        {
            "item_id": "CH-10",
            "item_name": "Enclosure Chassis CH-10",
            "location": "Plant Alpha (Central)",
            "current_stock": 2500,
            "safety_stock": 800,
            "daily_burn_rate": 450,
            "runout_days": 5.5,
            "holding_cost_per_day": 0.35,
            "stockout_penalty_per_unit": 45.0,
            "unit": "Units"
        },
        {
            "item_id": "FG-500",
            "item_name": "Finished IoT Gateway G-500",
            "location": "DC East / DC West",
            "current_stock": 350,
            "safety_stock": 500,
            "daily_burn_rate": 420,
            "runout_days": 0.8,
            "holding_cost_per_day": 1.50,
            "stockout_penalty_per_unit": 140.0,
            "unit": "Units"
        }
    ]
    return pd.DataFrame(data)

def get_default_demand_df():
    days = 14
    records = []
    np.random.seed(42)
    
    customers = [
        {"customer_id": "CUST-T1", "name": "MediCare Systems (Tier 1 Priority)", "tier": 1, "share": 0.35, "penalty": 180.0},
        {"customer_id": "CUST-T2", "name": "Apex Telecom (Tier 2 Enterprise)", "tier": 2, "share": 0.40, "penalty": 105.0},
        {"customer_id": "CUST-T3", "name": "Global Retail Corp (Tier 3 Standard)", "tier": 3, "share": 0.25, "penalty": 55.0}
    ]
    
    for day in range(1, days + 1):
        total_daily_demand = 430 + int(np.random.normal(0, 25))
        for cust in customers:
            qty = int(round(total_daily_demand * cust["share"]))
            records.append({
                "day": day,
                "customer_id": cust["customer_id"],
                "customer_name": cust["name"],
                "tier": cust["tier"],
                "demand_units": qty,
                "sla_penalty_per_unit": cust["penalty"]
            })
    return pd.DataFrame(records)

def get_default_network_nodes():
    return {
        "suppliers": [
            {"id": "SUP-A", "label": "Apex (Primary)", "type": "supplier", "echelon": 1, "status": "down"},
            {"id": "SUP-B", "label": "Beacon (Backup 1)", "type": "supplier", "echelon": 1, "status": "active"},
            {"id": "SUP-C", "label": "Crestline (Backup 2)", "type": "supplier", "echelon": 1, "status": "active"}
        ],
        "plants": [
            {"id": "PLANT-ALPHA", "label": "Assembly Plant Alpha", "type": "plant", "echelon": 2, "status": "active", "capacity": 450}
        ],
        "dcs": [
            {"id": "DC-EAST", "label": "Fulfillment Hub East", "type": "dc", "echelon": 3, "status": "active"},
            {"id": "DC-WEST", "label": "Fulfillment Hub West", "type": "dc", "echelon": 3, "status": "active"}
        ]
    }

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
