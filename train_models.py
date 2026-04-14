"""
ML Model Trainer
=================
Trains two XGBoost models:
  1. demand_model.pkl   — predicts Port_Demand_Score for any port × cargo × time
  2. optim_model.pkl    — scores triangle routes by predicted Optimization_Score

Run AFTER generate_data.py:
    python generate_data.py
    python train_models.py
"""

import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor
from config import DATA_DIR, MODEL_DIR


# ── Helper: encode categoricals ────────────────────────────────────────────────
def encode_df(df: pd.DataFrame, cat_cols: list, encoders: dict = None) -> tuple:
    df = df.copy()
    if encoders is None:
        encoders = {}
        for col in cat_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            encoders[col] = le
    else:
        for col in cat_cols:
            le = encoders[col]
            df[col] = df[col].astype(str).map(
                lambda x, le=le: le.transform([x])[0] if x in le.classes_ else 0
            )
    return df, encoders


# ── 1. Demand Model ────────────────────────────────────────────────────────────
def train_demand_model():
    market_path = os.path.join(DATA_DIR, "maritime_market_data.csv")
    if not os.path.exists(market_path):
        raise FileNotFoundError(f"Missing {market_path}. Run generate_data.py first.")

    df = pd.read_csv(market_path)
    print(f"[demand_model] Loaded {len(df):,} rows from {market_path}")

    cat_cols = ["Port_ID", "Region", "Cargo_Type", "Vessel_Requirement"]
    feature_cols = cat_cols + [
        "Year", "Month", "Quarter",
        "Market_Price_Index", "Congestion_Index",
        "Fuel_Cost_Index", "Historical_Volume_Tons",
    ]
    target_col = "Port_Demand_Score"

    df_enc, encoders = encode_df(df[feature_cols + [target_col]], cat_cols)

    X = df_enc[feature_cols].values
    y = df_enc[target_col].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )

    model = XGBRegressor(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        verbosity=0,
    )
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"[demand_model] MAE={mae:.2f}  R²={r2:.4f}")

    # Feature importances for transparency
    importances = dict(zip(feature_cols, model.feature_importances_))
    top_features = sorted(importances.items(), key=lambda x: -x[1])[:5]
    print(f"[demand_model] Top features: {top_features}")

    artifact = {
        "model":    model,
        "encoders": encoders,
        "features": feature_cols,
        "cat_cols": cat_cols,
        "mae":      mae,
        "r2":       r2,
    }
    out_path = os.path.join(MODEL_DIR, "demand_model.pkl")
    joblib.dump(artifact, out_path)
    print(f"[demand_model] Saved -> {out_path}")
    return artifact


# ── 2. Optimization Model ──────────────────────────────────────────────────────
def train_optim_model():
    route_path = os.path.join(DATA_DIR, "route_training_data.csv")
    if not os.path.exists(route_path):
        raise FileNotFoundError(f"Missing {route_path}. Run generate_data.py first.")

    df = pd.read_csv(route_path)
    print(f"[optim_model] Loaded {len(df):,} rows from {route_path}")

    cat_cols = ["Source_Port_ID", "Dest_Port_ID", "Vessel_Type", "Cargo_Type"]
    feature_cols = cat_cols + [
        "Distance_KM", "Transit_Days", "Fuel_Cost_USD", "Port_Dues_USD",
        "Revenue_USD", "Profit_USD", "Profit_Margin", "Fill_Rate",
        "Market_Price_Mult", "Turnaround_Hours", "Dest_Demand_Score",
    ]
    target_col = "Optimization_Score"

    df_enc, encoders = encode_df(df[feature_cols + [target_col]], cat_cols)

    X = df_enc[feature_cols].values
    y = df_enc[target_col].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )

    model = XGBRegressor(
        n_estimators=500,
        max_depth=7,
        learning_rate=0.04,
        subsample=0.85,
        colsample_bytree=0.75,
        random_state=42,
        n_jobs=-1,
        verbosity=0,
    )
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)
    print(f"[optim_model] MAE={mae:.4f}  R²={r2:.4f}")

    artifact = {
        "model":    model,
        "encoders": encoders,
        "features": feature_cols,
        "cat_cols": cat_cols,
        "mae":      mae,
        "r2":       r2,
    }
    out_path = os.path.join(MODEL_DIR, "optim_model.pkl")
    joblib.dump(artifact, out_path)
    print(f"[optim_model] Saved -> {out_path}")
    return artifact


if __name__ == "__main__":
    print("=" * 60)
    print("Training Demand Prediction Model…")
    print("=" * 60)
    train_demand_model()

    print()
    print("=" * 60)
    print("Training Route Optimization Model…")
    print("=" * 60)
    train_optim_model()

    print("\nAll models trained and saved to models/")
