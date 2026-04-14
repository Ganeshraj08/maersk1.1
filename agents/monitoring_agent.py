"""
Monitoring Agent
=================
Continuously scans the port network for:
  1. Empty vessel requirements (vessels repositioning without cargo — costly).
  2. Port congestion spikes that may disrupt future voyages.
  3. Supply–demand imbalances (cargo stranded at low-demand ports).
  4. Cargo-type shortages at major hubs (e.g., Singapore needs LNG).

This agent runs passively and produces a list of alert dicts.
"""

import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
from datetime import date
from config import (
    PORTS, VESSEL_CARGO_MAP, CARGO_VESSEL_MAP,
    BASE_MARKET_PRICES, DATA_DIR,
)


ALERT_LEVELS = ("CRITICAL", "WARNING", "INFO")

# Major hub ports that are monitored with extra sensitivity
HUB_PORTS = {"SGP", "RTM", "SHA", "JEA", "HOU", "NYK", "HAM", "TYO"}

# Threshold for what counts as a 'low demand' signal
LOW_DEMAND_THRESHOLD = 45
HIGH_CONGESTION_THRESHOLD = 1.20
EMPTY_LEG_PENALTY_USD_PER_KM = 81   # daily cost to reposition empty per KM


class MonitoringAgent:
    """
    Passive monitoring agent — scans port data and generates prioritised alerts.
    """

    def __init__(self):
        self._market_df = None
        market_path = os.path.join(DATA_DIR, "maritime_market_data.csv")
        if os.path.exists(market_path):
            self._market_df = pd.read_csv(market_path)
            print("[MonitoringAgent] Market data loaded.")
        else:
            print("[MonitoringAgent] No market data — generating synthetic alerts.")

    # ── Public API ─────────────────────────────────────────────────────────────
    def run(
        self,
        active_vessel_type: str = None,
        approved_route: dict = None,
    ) -> list[dict]:
        """
        Generate all active monitoring alerts.
        Optionally focuses on alerts relevant to the approved route context.
        """
        alerts = []
        alerts.extend(self._check_empty_leg_risk(active_vessel_type))
        alerts.extend(self._check_hub_shortages(active_vessel_type))
        alerts.extend(self._check_congestion())
        alerts.extend(self._check_stranded_cargo())
        if approved_route:
            alerts.extend(self._check_route_risks(approved_route))

        # Sort: CRITICAL first, then WARNING, then INFO
        order = {level: i for i, level in enumerate(ALERT_LEVELS)}
        alerts.sort(key=lambda a: order.get(a["level"], 99))
        return alerts

    # ── Check: Empty Leg Risk ──────────────────────────────────────────────────
    def _check_empty_leg_risk(self, vessel_type: str) -> list[dict]:
        alerts = []
        compatible_cargos = VESSEL_CARGO_MAP.get(vessel_type, []) if vessel_type else []
        if vessel_type and not compatible_cargos:
            print(f"[MonitoringAgent] WARNING: vessel_type '{vessel_type}' not in VESSEL_CARGO_MAP — skipping empty-leg check.")
            return []

        # Identify ports where the given vessel type has no return cargo demand
        for pid, port in PORTS.items():
            compatible = compatible_cargos
            if not compatible:
                continue

            demand = self._avg_demand(pid, compatible)
            if demand < LOW_DEMAND_THRESHOLD:
                alerts.append({
                    "level":       "WARNING",
                    "port_id":     pid,
                    "port_name":   port["name"],
                    "alert_type":  "EMPTY_LEG_RISK",
                    "message":     (
                        f"Low {vessel_type} return cargo demand at {port['name']} "
                        f"({port['country']}) — avg demand {demand:.0f}/100. "
                        f"Empty repositioning cost est. "
                        f"${self._empty_leg_cost(pid):,.0f}."
                    ),
                    "metric":      round(demand, 1),
                    "icon":        "⚠️",
                })

        return alerts[:3]  # top 3 worst empty-leg risks

    # ── Check: Hub Cargo Shortages ─────────────────────────────────────────────
    def _check_hub_shortages(self, vessel_type: str) -> list[dict]:
        alerts = []
        today = date.today()
        shortage_cargos = []

        for pid in HUB_PORTS:
            port = PORTS[pid]
            compatible = VESSEL_CARGO_MAP.get(vessel_type, []) if vessel_type else list(CARGO_VESSEL_MAP.keys())

            for cargo in compatible:
                demand = self._latest_demand(pid, cargo)
                if demand is not None and demand > 75:
                    shortage_cargos.append((pid, cargo, demand))

        shortage_cargos.sort(key=lambda x: -x[2])
        for pid, cargo, demand in shortage_cargos[:4]:
            port = PORTS[pid]
            price_mult = np.random.uniform(1.05, 1.25)
            alerts.append({
                "level":       "INFO" if demand < 85 else "WARNING",
                "port_id":     pid,
                "port_name":   port["name"],
                "alert_type":  "HUB_SHORTAGE",
                "message":     (
                    f"High {cargo} demand at hub {port['name']} ({demand:.0f}/100). "
                    f"Price premium: +{(price_mult - 1) * 100:.0f}%. "
                    f"Opportunity for opportunistic diversion."
                ),
                "metric":      round(demand, 1),
                "icon":        "📈",
            })

        return alerts

    # ── Check: Port Congestion ─────────────────────────────────────────────────
    def _check_congestion(self) -> list[dict]:
        alerts = []
        if self._market_df is None:
            return alerts

        latest = (
            self._market_df
            .sort_values(["Year", "Month"])
            .groupby("Port_ID")
            .last()
            .reset_index()
        )

        congested = latest[latest["Congestion_Index"] > HIGH_CONGESTION_THRESHOLD]
        for _, row in congested.iterrows():
            pid = row["Port_ID"]
            port = PORTS.get(pid, {})
            ci = row["Congestion_Index"]
            delay_hrs = int((ci - 1.0) * 48)
            alerts.append({
                "level":       "CRITICAL" if ci > 1.50 else ("WARNING" if ci > 1.35 else "INFO"),
                "port_id":     pid,
                "port_name":   port.get("name", pid),
                "alert_type":  "PORT_CONGESTION",
                "message":     (
                    f"Congestion index {ci:.2f}x at {port.get('name', pid)}. "
                    f"Expected additional delay: ~{delay_hrs}h. "
                    f"Consider alternative discharge port."
                ),
                "metric":      round(ci, 3),
                "icon":        "🚢",
            })

        return alerts[:3]

    # ── Check: Stranded Cargo ──────────────────────────────────────────────────
    def _check_stranded_cargo(self) -> list[dict]:
        alerts = []
        if self._market_df is None:
            return self._synthetic_stranded_alerts()

        latest = (
            self._market_df
            .sort_values(["Year", "Month"])
            .groupby(["Port_ID", "Cargo_Type"])
            .last()
            .reset_index()
        )

        stranded = latest[
            (latest["Port_Demand_Score"] < 35) &
            (latest["Historical_Volume_Tons"] > 100_000)
        ]

        for _, row in stranded.head(3).iterrows():
            pid = row["Port_ID"]
            port = PORTS.get(pid, {})
            alerts.append({
                "level":       "CRITICAL" if row["Port_Demand_Score"] < 20 else "WARNING",
                "port_id":     pid,
                "port_name":   port.get("name", pid),
                "alert_type":  "STRANDED_CARGO",
                "message":     (
                    f"Stranded cargo risk: {row['Cargo_Type']} at {port.get('name', pid)} "
                    f"with demand score {row['Port_Demand_Score']:.0f}/100 "
                    f"but {row['Historical_Volume_Tons']:,} t historical volume. "
                    f"Market mismatch — rerouting advised."
                ),
                "metric":      round(row["Port_Demand_Score"], 1),
                "icon":        "🔴",
            })

        return alerts

    # ── Check: Route-Specific Risks ────────────────────────────────────────────
    def _check_route_risks(self, route: dict) -> list[dict]:
        alerts = []
        alt_port = route.get("alt_port_name", "")
        profit = route.get("profit_usd", 0)
        co2 = route.get("co2_tons", 0)

        if profit < 0:
            alerts.append({
                "level":       "CRITICAL",
                "port_id":     route.get("alt_port_id", ""),
                "port_name":   alt_port,
                "alert_type":  "UNPROFITABLE_ROUTE",
                "message":     (
                    f"Approved route to {alt_port} is projected UNPROFITABLE "
                    f"(${profit:,.0f}). Review cargo rates or seek spot charter."
                ),
                "metric":      profit,
                "icon":        "🔴",
            })

        if co2 > 5000:
            alerts.append({
                "level":       "INFO",
                "port_id":     route.get("alt_port_id", ""),
                "port_name":   alt_port,
                "alert_type":  "HIGH_EMISSIONS",
                "message":     (
                    f"Alternative route via {alt_port} emits {co2:,.0f} t CO2. "
                    f"Consider slow steaming to reduce by ~15%."
                ),
                "metric":      co2,
                "icon":        "🌿",
            })

        return alerts

    # ── Helpers ────────────────────────────────────────────────────────────────
    def _avg_demand(self, port_id, cargo_list):
        if self._market_df is None:
            return np.random.uniform(30, 70)
        sub = self._market_df[
            (self._market_df["Port_ID"] == port_id) &
            (self._market_df["Cargo_Type"].isin(cargo_list))
        ]
        if len(sub):
            return float(sub["Port_Demand_Score"].mean())
        return float(np.random.uniform(30, 70))

    def _latest_demand(self, port_id, cargo_type):
        if self._market_df is None:
            return None
        sub = self._market_df[
            (self._market_df["Port_ID"] == port_id) &
            (self._market_df["Cargo_Type"] == cargo_type)
        ]
        if len(sub):
            return float(sub.sort_values(["Year", "Month"])["Port_Demand_Score"].iloc[-1])
        return None

    def _empty_leg_cost(self, port_id):
        port = PORTS.get(port_id, {})
        # Distance to nearest hub as proxy
        nearest_hub_dist = min(
            [self._dist(port.get("lat", 0), port.get("lon", 0),
                        PORTS[h]["lat"], PORTS[h]["lon"]) for h in HUB_PORTS],
            default=5000
        )
        return nearest_hub_dist * EMPTY_LEG_PENALTY_USD_PER_KM

    def _dist(self, lat1, lon1, lat2, lon2):
        R = 6371.0
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        dphi = np.radians(lat2 - lat1)
        dlam = np.radians(lon2 - lon1)
        a = np.sin(dphi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlam / 2) ** 2
        return R * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    def _synthetic_stranded_alerts(self):
        return [{
            "level":       "INFO",
            "port_id":     "LAG",
            "port_name":   "Lagos",
            "alert_type":  "STRANDED_CARGO",
            "message":     "Low Crude Oil demand at Lagos — possible stranded cargo risk.",
            "metric":      32.0,
            "icon":        "🔴",
        }]
