from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any

import numpy as np
import pandas as pd

from src.foe.corridor_foe_runner import foe_corridor_runner
from src.foe.forecasting import get_forecast_model    # factory for models


# ---------- Types & Config ----------

@dataclass
class CorridorFlowConfig:
    corridor_id: str = "US-KEN"
    source: str = "world_bank"
    value_col: str = "remittance_usd"  # annual aggregate amount
    year_col: str = "year"

    # B4: FX-adjusted forecasting
    forecast_model: str = "fx_linear"  # use FX-aware model via factory
    fx_col: str = "fx_rate"            # expected FX column name (e.g. USD→local)


FOECallback = Callable[[pd.DataFrame, CorridorFlowConfig], Any]


# ---------- Core helpers ----------

def _check_monotonic_years(df: pd.DataFrame, year_col: str) -> pd.DataFrame:
    df_sorted = df.sort_values(year_col).reset_index(drop=True)
    if df_sorted[year_col].duplicated().any():
        raise ValueError("Duplicate years found in annual corridor series.")
    return df_sorted


# ---------- Public API ----------

def prepare_annual_corridor_series(
    raw_df: pd.DataFrame,
    cfg: Optional[CorridorFlowConfig] = None,
) -> pd.DataFrame:
    """
    Normalize raw annual corridor flows → [corridor_id, year, remittance_usd, (optional fx_col)]
    """
    cfg = cfg or CorridorFlowConfig()

    if cfg.year_col not in raw_df.columns:
        raise KeyError(f"Missing year column '{cfg.year_col}' in input.")
    if cfg.value_col not in raw_df.columns:
        raise KeyError(f"Missing value column '{cfg.value_col}' in input.")

    df = raw_df.copy()
    df = _check_monotonic_years(df, cfg.year_col)

    df["corridor_id"] = cfg.corridor_id

    cols = ["corridor_id", cfg.year_col, cfg.value_col]
    # If FX is already present on the raw DF, carry it through
    if cfg.fx_col in df.columns:
        cols.append(cfg.fx_col)

    df = df[cols].rename(
        columns={
            cfg.year_col: "year",
            cfg.value_col: "remittance_usd",
            # fx_col name is kept as-is (cfg.fx_col)
        }
    )

    return df


def train_validate_forecast_corridor(
    annual_df: pd.DataFrame,
    cfg: Optional[CorridorFlowConfig] = None,
    train_end_year: int = 2023,
    validation_year: int = 2024,
    forecast_years: Optional[List[int]] = None,
    fx_df: Optional[pd.DataFrame] = None,
) -> Dict[str, pd.DataFrame]:
    """
    B4: FX-adjusted forecasting.

    - If cfg.forecast_model == "fx_linear", we expect an FX column `cfg.fx_col`
      either already on `annual_df` or supplied via `fx_df` (with columns: ["year", cfg.fx_col]).
    - The FOE-facing outputs (train/validation/forecast) remain in USD and keep
      the same schema as in the log-trend baseline.
    """
    cfg = cfg or CorridorFlowConfig()
    forecast_years = forecast_years or [2025]

    # Normalize year/value names if needed
    if cfg.year_col in annual_df.columns or cfg.value_col in annual_df.columns:
        df = annual_df.rename(
            columns={
                cfg.year_col: "year",
                cfg.value_col: "remittance_usd",
            }
        ).copy()
    else:
        df = annual_df.copy()

    df = _check_monotonic_years(df, "year")

    # Attach FX if provided separately
    if fx_df is not None:
        # Expect fx_df with "year" and cfg.fx_col
        missing = { "year", cfg.fx_col } - set(fx_df.columns)
        if missing:
            raise KeyError(
                f"fx_df is missing required columns: {missing}. "
                f"Expected at least ['year', '{cfg.fx_col}']."
            )
        df = df.merge(
            fx_df[["year", cfg.fx_col]],
            on="year",
            how="left",
            validate="one_to_one",
        )

    # If using FX-aware model, enforce presence of FX column
    if cfg.forecast_model == "fx_linear" and cfg.fx_col not in df.columns:
        raise ValueError(
            f"FX-adjusted model '{cfg.forecast_model}' requires FX column "
            f"'{cfg.fx_col}' on the annual series (or via fx_df)."
        )

    # Split train & validation
    train_mask = df["year"] <= train_end_year
    val_mask = df["year"] == validation_year

    train_df = df.loc[train_mask].copy()
    if train_df.empty:
        raise ValueError("Training set is empty. Check train_end_year.")

    # ---- MODEL: now using factory, default 'fx_linear' ----
    model = get_forecast_model(cfg.forecast_model)

    # Choose fit features based on model type
    if cfg.forecast_model == "fx_linear":
        fit_cols = ["year", "remittance_usd", cfg.fx_col]
        missing = set(fit_cols) - set(train_df.columns)
        if missing:
            raise KeyError(
                f"Training data missing required columns for fx_linear model: {missing}"
            )
        model.fit(train_df[fit_cols])
    else:
        # Fallback for other models (e.g. logtrend)
        model.fit(train_df[["year", "remittance_usd"]])

    # Training fitted values
    train_pred = model.predict(train_df["year"].tolist())
    train_df = train_df.merge(train_pred, on="year", how="left")

    # Validation
    validation_df = df.loc[val_mask].copy()
    if not validation_df.empty:
        val_pred_df = model.predict([validation_year])
        y_hat_val = float(val_pred_df["remittance_hat_usd"].iloc[0])
        validation_df["remittance_hat_usd"] = y_hat_val
        validation_df["error_abs_usd"] = (
            validation_df["remittance_usd"] - y_hat_val
        ).abs()
        validation_df["error_pct"] = (
            validation_df["error_abs_usd"] / validation_df["remittance_usd"]
        )
    else:
        # synthetic validation-only row
        val_pred_df = model.predict([validation_year])
        validation_df = pd.DataFrame({
            "year": [validation_year],
            "remittance_usd": [np.nan],
            "remittance_hat_usd": val_pred_df["remittance_hat_usd"].values,
        })

    # Forecast (exclude validation year from future list)
    future_years = [y for y in forecast_years if y != validation_year]
    if future_years:
        future_pred_df = model.predict(future_years)
        future_df = future_pred_df.copy()
        future_df["corridor_id"] = cfg.corridor_id
    else:
        future_df = pd.DataFrame(columns=["corridor_id", "year", "remittance_hat_usd"])

    # Tag corridor id
    train_df["corridor_id"] = cfg.corridor_id
    validation_df["corridor_id"] = cfg.corridor_id

    # Column order for FOE compatibility (drop FX columns here)
    train_df = train_df[
        ["corridor_id", "year", "remittance_usd", "remittance_hat_usd"]
    ]

    validation_cols = [
        c for c in [
            "corridor_id",
            "year",
            "remittance_usd",
            "remittance_hat_usd",
            "error_abs_usd",
            "error_pct",
        ] if c in validation_df.columns
    ]
    validation_df = validation_df[validation_cols]

    future_df = future_df[
        ["corridor_id", "year", "remittance_hat_usd"]
    ]

    return {
        "train": train_df,
        "validation": validation_df,
        "forecast": future_df,
    }


def run_corridor_foe_pipeline(
    annual_df: pd.DataFrame,
    cfg: Optional[CorridorFlowConfig] = None,
    foe_callback: Optional[FOECallback] = None,
    train_end_year: int = 2023,
    validation_year: int = 2024,
    forecast_years: Optional[List[int]] = None,
    fx_df: Optional[pd.DataFrame] = None,
) -> Dict[str, Any]:
    """
    B4 pipeline:

    - Normalize raw annual corridor series.
    - Run FX-adjusted forecasting via the factory model (default: 'fx_linear').
    - Maintain FOE pipeline and FOE-facing schema exactly as before.
    """
    cfg = cfg or CorridorFlowConfig()
    forecast_years = forecast_years or [2025]

    # Normalize (this may already carry fx_col if present)
    base_df = prepare_annual_corridor_series(annual_df, cfg)

    # Forecast segments
    segments = train_validate_forecast_corridor(
        base_df,
        cfg=CorridorFlowConfig(
            corridor_id=cfg.corridor_id,
            source=cfg.source,
            value_col="remittance_usd",
            year_col="year",
            forecast_model=cfg.forecast_model,
            fx_col=cfg.fx_col,
        ),
        train_end_year=train_end_year,
        validation_year=validation_year,
        forecast_years=forecast_years,
        fx_df=fx_df,
    )

    # Full annual series (historical + pred) for FOE
    full_annual = pd.concat(
        [segments["train"], segments["validation"], segments["forecast"]],
        ignore_index=True,
        sort=False,
    ).sort_values("year")

    # FOE pipeline unchanged
    foe_callback = foe_callback or default_foe_callback
    foe_result = foe_callback(full_annual, cfg) if foe_callback else None

    return {
        "cfg": cfg,
        "segments": segments,
        "full_annual": full_annual,
        "foe": foe_result,
    }


def default_foe_callback(annual_path: pd.DataFrame, cfg: CorridorFlowConfig):
    return foe_corridor_runner(annual_path, cfg)
