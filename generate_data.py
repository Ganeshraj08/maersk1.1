"""
Maritime Market Data Generator
================================
Generates two CSV files used for ML training and agent inference:
  - data/maritime_market_data.csv   : port-level market snapshot per month
  - data/route_training_data.csv    : historical route performance for optimization model

Run:  python generate_data.py
"""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import pandas as pd
from datetime import date, timedelta
from itertools import product
from config import (
    PORTS, CARGO_VESSEL_MAP, VESSEL_CARGO_MAP, BASE_MARKET_PRICES,
    VESSEL_FUEL_CONSUMPTION, VESSEL_SPEED_KNOTS, VESSEL_CAPACITY_TONS,
    FUEL_PRICE_PER_TON_USD, DATA_DIR, ALL_CARGO_TYPES, ALL_VESSEL_TYPES,
)

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)


# ── Haversine (kilometers) ────────────────────────────────────────────────
def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlam = np.radians(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlam / 2) ** 2
    return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


# ── Seasonal multipliers (Q1-Q4 for each cargo category) ─────────────────────
SEASONAL_DEMAND = {
    "Tanker":         [0.90, 0.85, 1.00, 1.10],   # higher winter energy
    "LNG_Carrier":    [1.20, 0.80, 0.85, 1.15],   # winter heating peaks
    "Bulk_Carrier":   [1.05, 1.10, 0.95, 0.90],   # harvest cycles
    "Container_Ship": [0.95, 1.00, 1.10, 1.15],   # pre-holiday restocking
    "Reefer":         [0.85, 1.15, 1.10, 0.90],   # summer perishables
}

REGION_DEMAND_BASE = {
    "Asia":        70,
    "Europe":      65,
    "Americas":    60,
    "Middle East": 55,
    "Africa":      45,
    "Oceania":     40,
}


def generate_market_data(months_back: int = 24) -> pd.DataFrame:
    """Generate monthly port × cargo demand records."""
    records = []
    today = date.today()
    start = date(today.year - (months_back // 12 + 1), 1, 1)

    port_ids = list(PORTS.keys())

    for port_id, cargo in product(port_ids, ALL_CARGO_TYPES):
        port = PORTS[port_id]
        vessel = CARGO_VESSEL_MAP[cargo]
        base_demand = REGION_DEMAND_BASE[port["region"]]
        seasonal_mults = SEASONAL_DEMAND[vessel]
        base_price = BASE_MARKET_PRICES[cargo]

        # Port-cargo affinity (some ports naturally trade certain commodities more)
        affinity_noise = rng.normal(0, 8)

        cur = start
        while cur <= today:
            month_idx = cur.month - 1
            quarter = cur.month // 3
            season_mult = seasonal_mults[quarter % 4]

            # Demand score with trend + noise
            trend = (cur.year - start.year) * 12 + (cur.month - start.month)
            drift = 0.15 * trend  # slow upward trend
            noise = rng.normal(0, 5)
            congestion = rng.uniform(0.5, 1.5)

            demand_score = float(np.clip(
                base_demand + affinity_noise + drift + noise + season_mult * 10,
                0, 100
            ))

            # Market price index (1.0 = base)
            price_shock = rng.uniform(0.85, 1.20)
            market_price_index = round(price_shock, 4)

            # Available return cargo (a compatible cargo available at this port)
            compatible_cargos = VESSEL_CARGO_MAP[vessel]
            available_return = rng.choice(compatible_cargos)

            # Return cargo demand
            return_cargo_demand = float(np.clip(rng.normal(50, 15), 5, 100))

            # Port-level metrics
            turnaround = rng.integers(18, 72)  # hours
            fuel_index = round(rng.uniform(0.90, 1.15), 4)
            historical_volume = int(rng.integers(10_000, 500_000))  # tons

            records.append({
                "Port_ID":              port_id,
                "Port_Name":            port["name"],
                "Country":              port["country"],
                "Region":               port["region"],
                "Latitude":             port["lat"],
                "Longitude":            port["lon"],
                "Cargo_Type":           cargo,
                "Vessel_Requirement":   vessel,
                "Year":                 cur.year,
                "Month":                cur.month,
                "Quarter":              (cur.month - 1) // 3 + 1,
                "Port_Demand_Score":    round(demand_score, 2),
                "Market_Price_Index":   market_price_index,
                "Available_Return_Cargo": available_return,
                "Return_Cargo_Demand":  round(return_cargo_demand, 2),
                "Port_Turnaround_Hours": int(turnaround),
                "Congestion_Index":     round(congestion, 4),
                "Fuel_Cost_Index":      fuel_index,
                "Historical_Volume_Tons": historical_volume,
            })

            # Advance month
            if cur.month == 12:
                cur = date(cur.year + 1, 1, 1)
            else:
                cur = date(cur.year, cur.month + 1, 1)

    df = pd.DataFrame(records)
    print(f"[generate_data] Market data: {len(df):,} rows")
    return df


def generate_route_data(n_routes: int = 8_000) -> pd.DataFrame:
    """
    Simulate historical route performance for training the optimization model.
    Each row = one voyage with calculated economics.
    """
    port_ids = list(PORTS.keys())
    records = []

    for _ in range(n_routes):
        # Random source / destination (must differ)
        src_id, dst_id = rng.choice(port_ids, size=2, replace=False)
        src, dst = PORTS[src_id], PORTS[dst_id]

        vessel = rng.choice(ALL_VESSEL_TYPES)
        cargo = rng.choice(VESSEL_CARGO_MAP[vessel])
        base_price = BASE_MARKET_PRICES[cargo]
        capacity = VESSEL_CAPACITY_TONS[vessel]

        distance_km = haversine_km(src["lat"], src["lon"], dst["lat"], dst["lon"])
        speed_kmh = VESSEL_SPEED_KNOTS[vessel] * 1.852 * rng.uniform(0.85, 1.00)  # weather factor
        transit_days = distance_km / (speed_kmh * 24)

        fuel_consumption = VESSEL_FUEL_CONSUMPTION[vessel]
        fuel_price = FUEL_PRICE_PER_TON_USD * rng.uniform(0.90, 1.15)
        fuel_cost = transit_days * fuel_consumption * fuel_price

        port_dues = (src["port_dues"] + dst["port_dues"]) * rng.uniform(0.9, 1.1)
        turnaround_hours = rng.integers(18, 72)

        # Revenue depends on fill rate and market
        fill_rate = rng.uniform(0.75, 1.00)
        market_mult = rng.uniform(0.90, 1.25)
        revenue = capacity * fill_rate * base_price * market_mult * 0.001  # scale to USD

        total_cost = fuel_cost + port_dues + transit_days * 15_000  # daily OPEX
        profit = revenue - total_cost
        profit_margin = profit / max(revenue, 1)

        # Demand score at destination (proxy for route attractiveness)
        dest_demand = rng.uniform(30, 90)

        # Optimization score: normalised profit considering distance risk
        opt_score = float(np.clip(
            (profit / 1_000_000) * (dest_demand / 100) / (1 + distance_km / 18_520),
            -1, 10
        ))

        records.append({
            "Source_Port_ID":       src_id,
            "Dest_Port_ID":         dst_id,
            "Vessel_Type":          vessel,
            "Cargo_Type":           cargo,
            "Distance_KM":          round(distance_km, 1),
            "Transit_Days":         round(transit_days, 2),
            "Fuel_Cost_USD":        round(fuel_cost, 0),
            "Port_Dues_USD":        round(port_dues, 0),
            "Revenue_USD":          round(revenue, 0),
            "Profit_USD":           round(profit, 0),
            "Profit_Margin":        round(profit_margin, 4),
            "Fill_Rate":            round(fill_rate, 4),
            "Market_Price_Mult":    round(market_mult, 4),
            "Turnaround_Hours":     int(turnaround_hours),
            "Dest_Demand_Score":    round(dest_demand, 2),
            "Optimization_Score":   round(opt_score, 4),
        })

    df = pd.DataFrame(records)
    print(f"[generate_data] Route training data: {len(df):,} rows")
    return df


if __name__ == "__main__":
    market_df = generate_market_data(months_back=24)
    market_path = os.path.join(DATA_DIR, "maritime_market_data.csv")
    market_df.to_csv(market_path, index=False)
    print(f"Saved -> {market_path}")

    route_df = generate_route_data(n_routes=8_000)
    route_path = os.path.join(DATA_DIR, "route_training_data.csv")
    route_df.to_csv(route_path, index=False)
    print(f"Saved -> {route_path}")

    print("\nSample — market data:")
    print(market_df.head(3).to_string())
    print("\nSample — route data:")
    print(route_df.head(3).to_string())
    print("\nDone.")
