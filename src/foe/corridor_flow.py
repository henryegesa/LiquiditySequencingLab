from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Any

import numpy as np
import pandas as pd

from src.foe.corridor_foe_runner import foe_corridor_runner
from src.foe.forecasting import get_forecast_model
from src.foe.forecasting.model_fx_linear import FXLinearModel


# ---------- Types & Config ----------

@dataclass
class CorridorFlowConfig:
    corridor_id: str = "US-KEN"
    source: str = "world_bank"
    value_col: str = "remittance_usd"  # annual aggregate amount
    year_col: str = "year"

    # B4: forecasting switch
    #   - "logtrend"   -> old baseline
    #   - "fx_linear"  -> FX-adjusted forecast using usd_kes
    forecast_model: str = "fx_linear"

    # FX column (must match what FXLinearModel expects)
    fx_col: str = "usd_kes"


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
    Normalize raw annual corridor flows → [corridor_id, year, remittance_usd, (optional usd_kes)].
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
    if cfg.fx_col in df.columns:
        cols.append(cfg.fx_col)

    df = df[cols].rename(
        columns={
            cfg.year_col: "year",
            cfg.value_col: "remittance_usd",
            # fx_col (usd_kes) name is preserved
        }
    )

    return df


def _fit_and_predict_logtrend(
    df: pd.DataFrame,
    train_end_year: int,
    validation_year: int,
    forecast_years: List[int],
    corridor_id: str,
) -> Dict[str, pd.DataFrame]:
    """
    Old baseline path: log-trend model without FX.
    """
    model = get_forecast_model("logtrend")
    model.fit(df[["year", "remittance_usd"]])

    # Training fitted values
    train_mask = df["year"] <= train_end_year
    val_mask = df["year"] == validation_year

    train_df = df.loc[train_mask].copy()
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
        val_pred_df = model.predict([validation_year])
        validation_df = pd.DataFrame(
            {
                "year": [validation_year],
                "remittance_usd": [np.nan],
                "remittance_hat_usd": val_pred_df["remittance_hat_usd"].values,
            }
        )

    # Forecast
    future_years = [y for y in forecast_years if y != validation_year]
    if future_years:
        future_pred_df = model.predict(future_years)
        future_df = future_pred_df.copy()
        future_df["corridor_id"] = corridor_id
    else:
        future_df = pd.DataFrame(columns=["corridor_id", "year", "remittance_hat_usd"])

    # Tag corridor id
    train_df["corridor_id"] = corridor_id
    validation_df["corridor_id"] = corridor_id

    # Column order
    train_df = train_df[
        ["corridor_id", "year", "remittance_usd", "remittance_hat_usd"]
    ]

    validation_cols = [
        c
        for c in [
            "corridor_id",
            "year",
            "remittance_usd",
            "remittance_hat_usd",
            "error_abs_usd",
            "error_pct",
        ]
        if c in validation_df.columns
    ]
    validation_df = validation_df[validation_cols]

    future_df = future_df[["corridor_id", "year", "remittance_hat_usd"]]

    return {
        "train": train_df,
        "validation": validation_df,
        "forecast": future_df,
    }


def _fit_and_predict_fx_linear(
    df: pd.DataFrame,
    cfg: CorridorFlowConfig,
    train_end_year: int,
    validation_year: int,
    forecast_years: List[int],
) -> Dict[str, pd.DataFrame]:
    """
    FX-adjusted path using FXLinearModel.

    Requirements:
      - df has columns: year, remittance_usd, usd_kes (or cfg.fx_col).
      - FX must exist for:
          - all training years
          - validation_year
          - all forecast_years (if you want forecasts)
    """
    if cfg.fx_col not in df.columns:
        raise ValueError(
            f"FX-adjusted model requires FX column '{cfg.fx_col}' on the annual series."
        )

    # Split
    df = df.copy()
    df = _check_monotonic_years(df, "year")

    train_mask = df["year"] <= train_end_year
    val_mask = df["year"] == validation_year

    train_df = df.loc[train_mask].copy()
    if train_df.empty:
        raise ValueError("Training set is empty. Check train_end_year.")

    # Model
    model = get_forecast_model("fx_linear")
    if not isinstance(model, FXLinearModel):
        raise TypeError("get_forecast_model('fx_linear') must return FXLinearModel.")

    # Fit
    model.fit(train_df[["year", "remittance_usd", cfg.fx_col]])

    # Train predictions (using actual FX)
    train_y_hat = model.predict_with_features(
        years=train_df["year"].tolist(),
        usd_kes=train_df[cfg.fx_col].tolist(),
    )
    train_df = train_df.merge(train_y_hat, on="year", how="left")

    # Validation
    validation_df = df.loc[val_mask].copy()
    if not validation_df.empty:
        if validation_df[cfg.fx_col].isna().any():
            raise ValueError(
                f"Missing FX value '{cfg.fx_col}' for validation year {validation_year}."
            )

        val_pred_df = model.predict_with_features(
            years=[validation_year],
            usd_kes=[float(validation_df[cfg.fx_col].iloc[0])],
        )
        y_hat_val = float(val_pred_df["remittance_hat_usd"].iloc[0])

        validation_df["remittance_hat_usd"] = y_hat_val
        validation_df["error_abs_usd"] = (
            validation_df["remittance_usd"] - y_hat_val
        ).abs()
        validation_df["error_pct"] = (
            validation_df["error_abs_usd"] / validation_df["remittance_usd"]
        )
    else:
        # synthetic validation row with FX but no actual remittance_usd
        val_pred_df = model.predict_with_features(
            years=[validation_year],
            usd_kes=[np.nan],
        )
        validation_df = pd.DataFrame(
            {
                "year": [validation_year],
                "remittance_usd": [np.nan],
                "remittance_hat_usd": val_pred_df["remittance_hat_usd"].values,
            }
        )

    # Forecast
    future_years = [y for y in forecast_years if y != validation_year]
    if future_years:
        future_df = df[df["year"].isin(future_years)].copy()
        if future_df.empty:
            raise ValueError(
                f"No FX/flow rows available for forecast years {future_years}. "
                f"Provide FX for these years."
            )
        if future_df[cfg.fx_col].isna().any():
            missing_years = future_df.loc[future_df[cfg.fx_col].isna(), "year"].tolist()
            raise ValueError(
                f"Missing FX '{cfg.fx_col}' for forecast years: {missing_years}"
            )

        future_pred_df = model.predict_with_features(
            years=future_df["year"].tolist(),
            usd_kes=future_df[cfg.fx_col].tolist(),
        )
        future_df = future_df.merge(future_pred_df, on="year", how="left")
        future_df["corridor_id"] = cfg.corridor_id
        future_df = future_df[["corridor_id", "year", "remittance_hat_usd"]]
    else:
        future_df = pd.DataFrame(columns=["corridor_id", "year", "remittance_hat_usd"])

    # Tag corridor id
    train_df["corridor_id"] = cfg.corridor_id
    validation_df["corridor_id"] = cfg.corridor_id

    # Column order (FOE-facing)
    train_df = train_df[
        ["corridor_id", "year", "remittance_usd", "remittance_hat_usd"]
    ]

    validation_cols = [
        c
        for c in [
            "corridor_id",
            "year",
            "remittance_usd",
            "remittance_hat_usd",
            "error_abs_usd",
            "error_pct",
        ]
        if c in validation_df.columns
    ]
    validation_df = validation_df[validation_cols]

    return {
        "train": train_df,
        "validation": validation_df,
        "forecast": future_df,
    }


def train_validate_forecast_corridor(
    annual_df: pd.DataFrame,
    cfg: Optional[CorridorFlowConfig] = None,
    train_end_year: int = 2023,
    validation_year: int = 2024,
    forecast_years: Optional[List[int]] = None,
) -> Dict[str, pd.DataFrame]:
    """
    Wrapper that selects between:
      - logtrend path (no FX)
      - fx_linear path (with usd_kes)
    """
    cfg = cfg or CorridorFlowConfig()
    forecast_years = forecast_years or [2025]

    # Normalize year/value names if caller used original cols
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

    if cfg.forecast_model == "fx_linear":
        return _fit_and_predict_fx_linear(
            df=df,
            cfg=cfg,
            train_end_year=train_end_year,
            validation_year=validation_year,
            forecast_years=forecast_years,
        )
    else:
        # fallback to logtrend baseline
        return _fit_and_predict_logtrend(
            df=df,
            train_end_year=train_end_year,
            validation_year=validation_year,
            forecast_years=forecast_years,
            corridor_id=cfg.corridor_id,
        )


def run_corridor_foe_pipeline(
    annual_df: pd.DataFrame,
    cfg: Optional[CorridorFlowConfig] = None,
    foe_callback: Optional[FOECallback] = None,
    train_end_year: int = 2023,
    validation_year: int = 2024,
    forecast_years: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """
    B4 pipeline:

    - Normalize raw annual corridor series.
    - Run chosen forecasting model.
    - Feed combined path into FOE.
    """
    cfg = cfg or CorridorFlowConfig()
    forecast_years = forecast_years or [2025]

    base_df = prepare_annual_corridor_series(annual_df, cfg)

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
    )

    full_annual = pd.concat(
        [segments["train"], segments["validation"], segments["forecast"]],
        ignore_index=True,
        sort=False,
    ).sort_values("year")

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
