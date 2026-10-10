"""
ResilientAI - Mock Data and Scenario Generator
Parametric, reproducible generation of supply chain networks, suppliers, inventory buffers,
demand schedules, and BOM relationships across multiple industry verticals.
"""

import os
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional

INDUSTRY_PRESETS = {
    "industrial_iot": {
        "name": "Industrial IoT Electronics",
        "finished_product": "Industrial IoT Gateway G-500",
        "critical_component": "MCU-900 Control Chipset",
        "critical_item_id": "MCU-900",
        "secondary_component": "Enclosure Chassis CH-10",
        "secondary_item_id": "CH-10",
        "daily_burn_default": 430,
        "holding_cost_default": 0.85,
        "stockout_penalty_default": 110.0,
        "suppliers": [
            {
                "supplier_id": "SUP-A",
                "name": "Apex Microelectronics (Primary)",
                "tier": 1,
                "component": "MCU-900 Control Chipset",
                "status": "DISRUPTED (Outage)",
                "daily_capacity": 500,
                "unit_cost": 45.0,
                "std_lead_time_days": 3,
                "expedite_lead_time_days": 2,
                "std_freight_cost": 4.5,
                "expedite_freight_cost": 14.0,
                "reliability_score": 0.98,
                "risk_index": 0.89,
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
        ],
        "customers": [
            {"customer_id": "CUST-T1", "name": "MediCare Systems (Tier 1 Priority)", "tier": 1, "share": 0.35, "penalty": 180.0},
            {"customer_id": "CUST-T2", "name": "Apex Telecom (Tier 2 Enterprise)", "tier": 2, "share": 0.40, "penalty": 105.0},
            {"customer_id": "CUST-T3", "name": "Global Retail Corp (Tier 3 Standard)", "tier": 3, "share": 0.25, "penalty": 55.0}
        ]
    },
    "automotive_ev": {
        "name": "Automotive EV Powertrain",
        "finished_product": "EV Motor Inverter Module INV-400",
        "critical_component": "SiC MOSFET Power Module",
        "critical_item_id": "SIC-800",
        "secondary_component": "Liquid Cooling Plate CP-20",
        "secondary_item_id": "CP-20",
        "daily_burn_default": 650,
        "holding_cost_default": 1.40,
        "stockout_penalty_default": 180.0,
        "suppliers": [
            {
                "supplier_id": "SUP-A",
                "name": "HyperSemi Silicon (Primary)",
                "tier": 1,
                "component": "SiC MOSFET Power Module",
                "status": "DISRUPTED (Outage)",
                "daily_capacity": 750,
                "unit_cost": 72.0,
                "std_lead_time_days": 4,
                "expedite_lead_time_days": 2,
                "std_freight_cost": 6.5,
                "expedite_freight_cost": 18.0,
                "reliability_score": 0.97,
                "risk_index": 0.92,
                "is_critical": True
            },
            {
                "supplier_id": "SUP-B",
                "name": "Vanguard Micro Electronics (Backup 1)",
                "tier": 1,
                "component": "SiC MOSFET Power Module",
                "status": "OPERATIONAL",
                "daily_capacity": 520,
                "unit_cost": 92.0,
                "std_lead_time_days": 5,
                "expedite_lead_time_days": 2,
                "std_freight_cost": 8.0,
                "expedite_freight_cost": 21.0,
                "reliability_score": 0.94,
                "risk_index": 0.16,
                "is_critical": False
            },
            {
                "supplier_id": "SUP-C",
                "name": "Silicon Fab Pacific (Backup 2)",
                "tier": 1,
                "component": "SiC MOSFET Power Module",
                "status": "OPERATIONAL",
                "daily_capacity": 450,
                "unit_cost": 98.0,
                "std_lead_time_days": 4,
                "expedite_lead_time_days": 2,
                "std_freight_cost": 7.5,
                "expedite_freight_cost": 19.5,
                "reliability_score": 0.95,
                "risk_index": 0.14,
                "is_critical": False
            },
            {
                "supplier_id": "SUP-D",
                "name": "Nordic Thermal Dynamics (Cooling)",
                "tier": 2,
                "component": "Liquid Cooling Plate CP-20",
                "status": "OPERATIONAL",
                "daily_capacity": 900,
                "unit_cost": 34.0,
                "std_lead_time_days": 3,
                "expedite_lead_time_days": 1,
                "std_freight_cost": 4.5,
                "expedite_freight_cost": 11.0,
                "reliability_score": 0.98,
                "risk_index": 0.06,
                "is_critical": False
            }
        ],
        "customers": [
            {"customer_id": "CUST-T1", "name": "Global EV Motors (Tier 1 Priority)", "tier": 1, "share": 0.45, "penalty": 240.0},
            {"customer_id": "CUST-T2", "name": "Fleet Commercial Vans (Tier 2 Enterprise)", "tier": 2, "share": 0.35, "penalty": 130.0},
            {"customer_id": "CUST-T3", "name": "Aftermarket Parts Distribution (Tier 3)", "tier": 3, "share": 0.20, "penalty": 60.0}
        ]
    },
    "aerospace_defense": {
        "name": "Aerospace & Defense Avionics",
        "finished_product": "Avionics Guidance Computer AGC-9",
        "critical_component": "Rad-Hard FPGA Processing Unit",
        "critical_item_id": "FPGA-90",
        "secondary_component": "Precision Titanium Housing TH-4",
        "secondary_item_id": "TH-4",
        "daily_burn_default": 180,
        "holding_cost_default": 3.80,
        "stockout_penalty_default": 450.0,
        "suppliers": [
            {
                "supplier_id": "SUP-A",
                "name": "Orbital Microchips (Primary)",
                "tier": 1,
                "component": "Rad-Hard FPGA Processing Unit",
                "status": "DISRUPTED (Outage)",
                "daily_capacity": 220,
                "unit_cost": 175.0,
                "std_lead_time_days": 5,
                "expedite_lead_time_days": 2,
                "std_freight_cost": 12.0,
                "expedite_freight_cost": 32.0,
                "reliability_score": 0.99,
                "risk_index": 0.94,
                "is_critical": True
            },
            {
                "supplier_id": "SUP-B",
                "name": "AeroDynamics Silicon (Backup 1)",
                "tier": 1,
                "component": "Rad-Hard FPGA Processing Unit",
                "status": "OPERATIONAL",
                "daily_capacity": 160,
                "unit_cost": 235.0,
                "std_lead_time_days": 6,
                "expedite_lead_time_days": 3,
                "std_freight_cost": 15.0,
                "expedite_freight_cost": 38.0,
                "reliability_score": 0.95,
                "risk_index": 0.20,
                "is_critical": False
            },
            {
                "supplier_id": "SUP-C",
                "name": "Apex Space Components (Backup 2)",
                "tier": 1,
                "component": "Rad-Hard FPGA Processing Unit",
                "status": "OPERATIONAL",
                "daily_capacity": 140,
                "unit_cost": 255.0,
                "std_lead_time_days": 4,
                "expedite_lead_time_days": 2,
                "std_freight_cost": 14.0,
                "expedite_freight_cost": 35.0,
                "reliability_score": 0.96,
                "risk_index": 0.15,
                "is_critical": False
            },
            {
                "supplier_id": "SUP-D",
                "name": "Titan Precision Aero Alloys",
                "tier": 2,
                "component": "Precision Titanium Housing TH-4",
                "status": "OPERATIONAL",
                "daily_capacity": 300,
                "unit_cost": 85.0,
                "std_lead_time_days": 3,
                "expedite_lead_time_days": 1,
                "std_freight_cost": 8.0,
                "expedite_freight_cost": 18.0,
                "reliability_score": 0.99,
                "risk_index": 0.04,
                "is_critical": False
            }
        ],
        "customers": [
            {"customer_id": "CUST-T1", "name": "Defense Prime Contractors (Tier 1 Priority)", "tier": 1, "share": 0.60, "penalty": 520.0},
            {"customer_id": "CUST-T2", "name": "National Space Agency (Tier 1 Mission Critical)", "tier": 1, "share": 0.25, "penalty": 480.0},
            {"customer_id": "CUST-T3", "name": "Commercial Regional Aviation (Tier 2)", "tier": 2, "share": 0.15, "penalty": 180.0}
        ]
    },
    "medical_devices": {
        "name": "Medical Life Support Equipment",
        "finished_product": "ICU Ventilator Controller VENT-X",
        "critical_component": "Precision Pressure Micro-Sensor",
        "critical_item_id": "PS-500",
        "secondary_component": "Medical Grade Valving Unit MV-12",
        "secondary_item_id": "MV-12",
        "daily_burn_default": 380,
        "holding_cost_default": 1.15,
        "stockout_penalty_default": 280.0,
        "suppliers": [
            {
                "supplier_id": "SUP-A",
                "name": "BioSense Microelectronics (Primary)",
                "tier": 1,
                "component": "Precision Pressure Micro-Sensor",
                "status": "DISRUPTED (Outage)",
                "daily_capacity": 420,
                "unit_cost": 52.0,
                "std_lead_time_days": 3,
                "expedite_lead_time_days": 1,
                "std_freight_cost": 5.0,
                "expedite_freight_cost": 16.0,
                "reliability_score": 0.99,
                "risk_index": 0.91,
                "is_critical": True
            },
            {
                "supplier_id": "SUP-B",
                "name": "MedTech Silicon Hub (Backup 1)",
                "tier": 1,
                "component": "Precision Pressure Micro-Sensor",
                "status": "OPERATIONAL",
                "daily_capacity": 310,
                "unit_cost": 69.0,
                "std_lead_time_days": 4,
                "expedite_lead_time_days": 2,
                "std_freight_cost": 6.8,
                "expedite_freight_cost": 18.5,
                "reliability_score": 0.96,
                "risk_index": 0.15,
                "is_critical": False
            },
            {
                "supplier_id": "SUP-C",
                "name": "Precision BioComponents (Backup 2)",
                "tier": 1,
                "component": "Precision Pressure Micro-Sensor",
                "status": "OPERATIONAL",
                "daily_capacity": 270,
                "unit_cost": 75.0,
                "std_lead_time_days": 4,
                "expedite_lead_time_days": 2,
                "std_freight_cost": 6.2,
                "expedite_freight_cost": 17.0,
                "reliability_score": 0.97,
                "risk_index": 0.11,
                "is_critical": False
            },
            {
                "supplier_id": "SUP-D",
                "name": "Swiss Medical Precision Valving",
                "tier": 2,
                "component": "Medical Grade Valving Unit MV-12",
                "status": "OPERATIONAL",
                "daily_capacity": 500,
                "unit_cost": 36.0,
                "std_lead_time_days": 3,
                "expedite_lead_time_days": 1,
                "std_freight_cost": 4.0,
                "expedite_freight_cost": 10.0,
                "reliability_score": 0.99,
                "risk_index": 0.05,
                "is_critical": False
            }
        ],
        "customers": [
            {"customer_id": "CUST-T1", "name": "Acute Care Hospital Networks (Tier 1 Priority)", "tier": 1, "share": 0.55, "penalty": 360.0},
            {"customer_id": "CUST-T2", "name": "Emergency Preparedness Reserves (Tier 1 Priority)", "tier": 1, "share": 0.30, "penalty": 310.0},
            {"customer_id": "CUST-T3", "name": "Regional Private Clinics (Tier 2)", "tier": 2, "share": 0.15, "penalty": 110.0}
        ]
    }
}


class MockDataGenerator:
    """
    Parametric Mock Data Generator for Supply Chain Simulation.
    Creates dynamic datasets according to user parameters, disruption scenarios,
    and industry configurations.
    """

    def __init__(self, preset_key: str = "industrial_iot", seed: Optional[int] = 42):
        self.preset_key = preset_key if preset_key in INDUSTRY_PRESETS else "industrial_iot"
        self.preset = INDUSTRY_PRESETS[self.preset_key]
        self.seed = seed
        if self.seed is not None:
            np.random.seed(self.seed)

    def generate_suppliers_df(
        self,
        disrupted_supplier_id: str = "SUP-A",
        duration_days: int = 7,
        capacity_drop_pct: float = 100.0,
        supplier_b_capacity_override: Optional[int] = None,
        supplier_c_capacity_override: Optional[int] = None,
        cost_multiplier: float = 1.0
    ) -> pd.DataFrame:
        """Generates suppliers dataframe reflecting active scenario parameters."""
        raw_list = [dict(s) for s in self.preset["suppliers"]]
        
        for sup in raw_list:
            sup["supplier_name"] = sup["name"]
            sup["critical_component"] = sup["component"]
            # Scale costs
            sup["unit_cost"] = round(sup["unit_cost"] * cost_multiplier, 2)
            sup["std_freight_cost"] = round(sup["std_freight_cost"] * cost_multiplier, 2)
            sup["expedite_freight_cost"] = round(sup["expedite_freight_cost"] * cost_multiplier, 2)
            
            # Apply disruption
            if sup["supplier_id"] == disrupted_supplier_id:
                if capacity_drop_pct >= 99.0:
                    sup["status"] = f"DISRUPTED ({duration_days}-Day Shutdown)"
                    sup["risk_index"] = 0.95
                else:
                    sup["status"] = f"RESTRICTED (-{int(capacity_drop_pct)}% Capacity)"
                    sup["risk_index"] = round(0.5 + (capacity_drop_pct / 200.0), 2)
                sup["is_critical"] = True
            else:
                sup["status"] = "OPERATIONAL"
                if sup["supplier_id"] == "SUP-B" and supplier_b_capacity_override is not None:
                    sup["daily_capacity"] = supplier_b_capacity_override
                elif sup["supplier_id"] == "SUP-C" and supplier_c_capacity_override is not None:
                    sup["daily_capacity"] = supplier_c_capacity_override

        return pd.DataFrame(raw_list)

    def generate_inventory_df(
        self,
        daily_burn_rate: Optional[float] = None,
        initial_stock_days: float = 2.08,
        safety_stock_days: float = 1.05,
        holding_cost_override: Optional[float] = None,
        penalty_override: Optional[float] = None
    ) -> pd.DataFrame:
        """Generates inventory buffers dynamically mapped to burn rates and runway targets."""
        burn = daily_burn_rate if daily_burn_rate is not None else float(self.preset["daily_burn_default"])
        crit_item_id = self.preset["critical_item_id"]
        crit_item_name = self.preset["critical_component"]
        sec_item_id = self.preset["secondary_item_id"]
        sec_item_name = self.preset["secondary_component"]
        
        current_stock = int(round(burn * initial_stock_days))
        safety_stock = int(round(burn * safety_stock_days))
        runout_days = round(current_stock / burn, 2)
        
        h_cost = holding_cost_override or self.preset["holding_cost_default"]
        p_cost = penalty_override or self.preset["stockout_penalty_default"]

        data = [
            {
                "item_id": crit_item_id,
                "item_name": crit_item_name,
                "location": "Plant Alpha (Central)",
                "current_stock": current_stock,
                "safety_stock": safety_stock,
                "daily_burn_rate": int(burn),
                "runout_days": runout_days,
                "holding_cost_per_day": round(h_cost, 2),
                "stockout_penalty_per_unit": round(p_cost, 2),
                "unit": "Units"
            },
            {
                "item_id": sec_item_id,
                "item_name": sec_item_name,
                "location": "Plant Alpha (Central)",
                "current_stock": int(burn * 5.5),
                "safety_stock": int(burn * 1.8),
                "daily_burn_rate": int(burn),
                "runout_days": 5.5,
                "holding_cost_per_day": round(h_cost * 0.4, 2),
                "stockout_penalty_per_unit": round(p_cost * 0.4, 2),
                "unit": "Units"
            },
            {
                "item_id": "FG-MOD",
                "item_name": f"Finished {self.preset['finished_product']}",
                "location": "DC East / DC West",
                "current_stock": int(burn * 0.8),
                "safety_stock": int(burn * 1.2),
                "daily_burn_rate": int(burn * 0.95),
                "runout_days": 0.8,
                "holding_cost_per_day": round(h_cost * 1.7, 2),
                "stockout_penalty_per_unit": round(p_cost * 1.3, 2),
                "unit": "Units"
            }
        ]
        return pd.DataFrame(data)

    def generate_demand_df(
        self,
        horizon_days: int = 14,
        daily_mean_demand: Optional[float] = None,
        volatility_pct: float = 0.06,
        demand_shock_pct: float = 0.0
    ) -> pd.DataFrame:
        """Generates dynamic customer demand across planning horizon."""
        if self.seed is not None:
            np.random.seed(self.seed)
            
        base_mean = daily_mean_demand or float(self.preset["daily_burn_default"])
        # Apply demand shock
        mean_demand = base_mean * (1.0 + demand_shock_pct / 100.0)
        std_dev = mean_demand * volatility_pct
        
        customers = self.preset["customers"]
        records = []
        
        for day in range(1, horizon_days + 1):
            daily_total = max(10, int(round(np.random.normal(mean_demand, std_dev))))
            for cust in customers:
                qty = max(1, int(round(daily_total * cust["share"])))
                records.append({
                    "day": day,
                    "customer_id": cust["customer_id"],
                    "customer_name": cust["name"],
                    "tier": cust["tier"],
                    "customer_tier": cust["tier"],
                    "demand_units": qty,
                    "sla_penalty_per_unit": cust["penalty"]
                })
                
        return pd.DataFrame(records)

    def generate_bom_df(self) -> pd.DataFrame:
        """Generates structural Bill of Materials for assembly operations."""
        bom = [
            {
                "Finished Product": self.preset["finished_product"],
                "Component ID": self.preset["critical_item_id"],
                "Component Name": self.preset["critical_component"],
                "Qty Required": 1,
                "Primary Supplier": f"{self.preset['suppliers'][0]['name']} ({self.preset['suppliers'][0]['supplier_id']})",
                "Criticality": "CRITICAL (Bottleneck Component)"
            },
            {
                "Finished Product": self.preset["finished_product"],
                "Component ID": self.preset["secondary_item_id"],
                "Component Name": self.preset["secondary_component"],
                "Qty Required": 1,
                "Primary Supplier": f"{self.preset['suppliers'][3]['name']} ({self.preset['suppliers'][3]['supplier_id']})",
                "Criticality": "STANDARD (Redundant Available)"
            }
        ]
        return pd.DataFrame(bom)

    def generate_network_nodes(self, suppliers_df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """Generates network graph node definitions."""
        s_df = suppliers_df if suppliers_df is not None else self.generate_suppliers_df()
        
        sup_nodes = []
        for _, row in s_df.iterrows():
            if row["tier"] == 1:
                is_disrupted = "DISRUPTED" in str(row["status"]).upper()
                sup_nodes.append({
                    "id": row["supplier_id"],
                    "label": row["name"],
                    "type": "supplier",
                    "echelon": 1,
                    "status": "down" if is_disrupted else "active"
                })
                
        return {
            "suppliers": sup_nodes,
            "plants": [
                {"id": "PLANT-ALPHA", "label": "Assembly Plant Alpha", "type": "plant", "echelon": 2, "status": "active", "capacity": int(self.preset["daily_burn_default"] * 1.05)}
            ],
            "dcs": [
                {"id": "DC-EAST", "label": "Regional Hub East", "type": "dc", "echelon": 3, "status": "active"},
                {"id": "DC-WEST", "label": "Regional Hub West", "type": "dc", "echelon": 3, "status": "active"}
            ]
        }


def generate_scenario_dataset(
    preset_key: str = "industrial_iot",
    preset: Optional[str] = None,
    disrupted_supplier_id: str = "SUP-A",
    duration_days: int = 7,
    capacity_drop_pct: float = 100.0,
    demand_shock_pct: float = 0.0,
    daily_burn_rate: Optional[float] = None,
    initial_stock_days: float = 2.08,
    safety_stock_days: float = 1.05,
    inventory_buffer_days: Optional[float] = None,
    disruption_severity: str = "critical",
    demand_volatility: str = "stable",
    num_suppliers: int = 4,
    supplier_b_capacity_override: Optional[int] = None,
    supplier_c_capacity_override: Optional[int] = None,
    seed: Optional[int] = 42
) -> Dict[str, Any]:
    """
    Convenience orchestrator generating a complete coherent bundle of
    suppliers, inventory, demand, BOM, and network metadata.
    """
    actual_preset = preset or preset_key
    gen = MockDataGenerator(preset_key=actual_preset, seed=seed)
    
    # Handle disruption severity mapping
    severity_map = {
        "low": 40.0,
        "medium": 70.0,
        "high": 90.0,
        "critical": 100.0
    }
    actual_drop = severity_map.get(disruption_severity.lower(), capacity_drop_pct)

    # Handle buffer days
    actual_init_days = inventory_buffer_days if inventory_buffer_days is not None else initial_stock_days

    # Handle volatility mapping
    vol_map = {
        "stable": 0.05,
        "moderate": 0.12,
        "high": 0.25
    }
    actual_vol = vol_map.get(demand_volatility.lower(), 0.06)

    sup_df = gen.generate_suppliers_df(
        disrupted_supplier_id=disrupted_supplier_id,
        duration_days=duration_days,
        capacity_drop_pct=actual_drop,
        supplier_b_capacity_override=supplier_b_capacity_override,
        supplier_c_capacity_override=supplier_c_capacity_override
    )
    
    inv_df = gen.generate_inventory_df(
        daily_burn_rate=daily_burn_rate,
        initial_stock_days=actual_init_days,
        safety_stock_days=safety_stock_days
    )
    
    dem_df = gen.generate_demand_df(
        horizon_days=14,
        daily_mean_demand=daily_burn_rate,
        demand_shock_pct=demand_shock_pct,
        volatility_pct=actual_vol
    )
    
    bom_df = gen.generate_bom_df()
    network_nodes = gen.generate_network_nodes(sup_df)
    
    return {
        "suppliers_df": sup_df,
        "inventory_df": inv_df,
        "demand_df": dem_df,
        "bom_df": bom_df,
        "network_nodes": network_nodes,
        "preset_name": gen.preset["name"],
        "critical_item_id": gen.preset["critical_item_id"],
        "critical_component": gen.preset["critical_component"],
        "disrupted_supplier_id": disrupted_supplier_id
    }
