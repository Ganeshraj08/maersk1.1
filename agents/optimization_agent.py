"""
TCS ATLAS — Optimization Agent
Uses XGBoost to score route feasibility/cost efficiency.
Supports weight profiles for Re-Rank: Balanced / Cost / Carbon / SLA.
"""
import numpy as np
import pandas as pd
from config import XGB_FEATURES, ROUTE_OPTIONS_BASE, WEIGHT_PROFILES


def _generate_training_data(n: int = 1200, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "distance_km":         rng.uniform(100,  8_000, n),
        "transit_days":        rng.uniform(0.5,     20, n),
        "vessel_capacity_teu": rng.choice([5_000, 8_000, 12_000, 15_000, 18_000, 20_000, 24_000], n),
        "available_empty_teu": rng.uniform(100,  5_000, n),
        "demand_teu":          rng.uniform(100,  1_500, n),
        "fuel_cost_per_nm":    rng.uniform(150,    450, n),
        "port_handling_fee_k": rng.uniform( 20,    150, n),
        "weather_score":       rng.beta(8, 2, n),
        "congestion_index":    rng.beta(2, 5, n),
        "depot_util_pct":      rng.uniform(0.30, 0.95, n),
    })
    df["cost_efficiency"] = (
        50
        - 0.003 * df["distance_km"]
        - 2.5   * df["transit_days"]
        + 0.001 * df["vessel_capacity_teu"]
        - 0.008 * df["fuel_cost_per_nm"]
        - 0.05  * df["port_handling_fee_k"]
        + 15    * df["weather_score"]
        - 20    * df["congestion_index"]
        + rng.normal(0, 5, n)
    ).clip(0, 100)
    return df


class OptimizationAgent:
    """
    Agent C — Route Optimization using XGBoost.
    Weight profiles change Re-Rank emphasis:
      Balanced | Cost Optimized | Carbon Neutral | SLA Priority
    """

    def __init__(self):
        self.model      = None
        self.r2_score   = None
        self.feat_imp   = {}
        self._trained   = False

    def train(self) -> "OptimizationAgent":
        try:
            import xgboost as xgb
            from sklearn.model_selection import train_test_split

            df = _generate_training_data()
            X  = df[XGB_FEATURES]
            y  = df["cost_efficiency"]
            X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

            self.model = xgb.XGBRegressor(
                n_estimators=200, max_depth=5, learning_rate=0.1,
                subsample=0.8, colsample_bytree=0.8,
                random_state=42, verbosity=0,
            )
            self.model.fit(X_tr, y_tr)
            self.r2_score = round(float(self.model.score(X_te, y_te)), 4)
            imp = self.model.feature_importances_
            self.feat_imp = {f: round(float(v), 4) for f, v in zip(XGB_FEATURES, imp)}
            self._trained = True
        except Exception:
            self._trained = False
        return self

    def _xgb_score(self, route: dict) -> float:
        """Raw XGBoost cost-efficiency score (0–100)."""
        if not self._trained or self.model is None:
            return route.get("xgb_score", 80.0)
        row = pd.DataFrame([{
            "distance_km":         route.get("distance_km", 1200),
            "transit_days":        route.get("transit_days", 2.0),
            "vessel_capacity_teu": 18_000,
            "available_empty_teu": route.get("teu", 847),
            "demand_teu":          847,
            "fuel_cost_per_nm":    route.get("cost_per_teu", 300) * 0.6,
            "port_handling_fee_k": 75,
            "weather_score":       0.85,
            "congestion_index":    0.12,
            "depot_util_pct":      0.65,
        }])
        raw = float(self.model.predict(row)[0])
        return round(float(np.clip(70 + (raw / 100) * 28, 70, 98)), 1)

    def _composite_score(self, route: dict, weights: dict) -> float:
        """
        Weighted composite score combining:
          cost    : normalised cost-efficiency (lower cost_per_teu → higher)
          carbon  : normalised CO₂ savings (lower co2_tons → higher)
          sla     : SLA probability (higher → higher)
        All sub-scores are 0–100.
        """
        # Normalise cost: $200 = 100 pts, $450 = 0 pts
        cost_score = max(0, min(100, (450 - route.get("cost_per_teu", 350)) / 2.5))

        # Normalise carbon: 50 t = 100 pts, 250 t = 0 pts
        carbon_score = max(0, min(100, (250 - route.get("co2_tons", 150)) / 2.0))

        # SLA directly as 0–100
        sla_score = route.get("sla_pct", 85.0)

        return round(
            weights["cost"]   * cost_score
            + weights["carbon"] * carbon_score
            + weights["sla"]    * sla_score,
            1,
        )

    def run(self, routes: list | None = None,
            weight_profile: str = "Balanced (Cost + Carbon + SLA)") -> dict:
        """
        Parameters
        ----------
        routes         : list of route dicts (defaults to ROUTE_OPTIONS_BASE)
        weight_profile : key in config.WEIGHT_PROFILES

        Returns
        -------
        dict { ranked_routes, model_r2, feat_imp, stream_lines, weight_profile }
        """
        if routes is None:
            routes = ROUTE_OPTIONS_BASE

        weights = WEIGHT_PROFILES.get(weight_profile, WEIGHT_PROFILES["Balanced (Cost + Carbon + SLA)"])

        scored = []
        for r in routes:
            rc = dict(r)
            rc["xgb_score"]       = self._xgb_score(rc)
            rc["composite_score"] = self._composite_score(rc, weights)
            # Final rank score = blend XGBoost + composite
            rc["_final"] = 0.5 * rc["xgb_score"] + 0.5 * rc["composite_score"]
            scored.append(rc)

        scored.sort(key=lambda x: x["_final"], reverse=True)
        for i, r in enumerate(scored):
            r["rank"] = i + 1

        model_info = f"XGBoost R²={self.r2_score}" if self._trained else "Rule-based fallback"

        stream_lines = [
            "[TCS ATLAS OPTIMIZER] Loading XGBoost cost-efficiency model...",
            f"Model              : {model_info}",
            f"Training samples   : 1,200 synthetic repositioning records",
            f"Weight profile     : {weight_profile}",
            f"  Cost weight      : {weights['cost']:.0%}",
            f"  Carbon weight    : {weights['carbon']:.0%}",
            f"  SLA weight       : {weights['sla']:.0%}",
            "",
            "[SCORING] Evaluating candidate routes...",
        ]
        for r in scored:
            stream_lines.append(
                f"  Route via {r['from_port']:28s}  XGB:{r['xgb_score']:5.1f} "
                f"Composite:{r['composite_score']:5.1f}  Final:{r['_final']:5.1f}"
            )

        top = scored[0]
        savings_per_teu = 412 - top["cost_per_teu"]

        stream_lines += [
            "",
            "OPTIMISATION COMPLETE",
            f"  TOP RECOMMENDATION : {top['from_port']}",
            f"  Cost / TEU         : ${top['cost_per_teu']} (vs $412 manual baseline)",
            f"  Savings / TEU      : ${savings_per_teu}",
            f"  Carbon             : {top['co2_tons']}t CO₂",
            f"  SLA Probability    : {top['sla_pct']}%",
            f"  Final Agent Score  : {top['_final']:.1f}",
            "",
            "Status: READY FOR HUMAN APPROVAL >>",
        ]

        return {
            "ranked_routes":  scored,
            "model_r2":       self.r2_score,
            "feat_imp":       self.feat_imp,
            "stream_lines":   stream_lines,
            "weight_profile": weight_profile,
        }
