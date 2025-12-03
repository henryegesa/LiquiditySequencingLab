# src/foe/scenarios/fx_shocks.py

from __future__ import annotations
from typing import Dict, List, Optional
import numpy as np
import pandas as pd


def apply_fx_shock(
    df: pd.DataFrame,
    fx_col: str,
    scenario: str = "none",
    shock_pct: float = 0.0,
    shock_years: Optional[List[int]] = None,
    shock_path: Optional[Dict[int, float]] = None,
) -> pd.DataFrame:
    """
    Apply FX shock scenarios to an annual FX series.

    df must contain:
        - year
        - fx_col (e.g. usd_kes)

    Output:
        df with new column: f"{fx_col}_shocked"
    """

    df = df.copy()

    if "year" not in df.columns:
        raise KeyError("apply_fx_shock requires a 'year' column.")
    if fx_col not in df.columns:
        raise KeyError(f"FX column '{fx_col}' missing in df.")

    years = df["year"].astype(int).values
    fx = df[fx_col].astype(float).values

    # --------------------
    # Scenario handlers
    # --------------------
    if scenario == "none":
        shocked = fx

    elif scenario == "shock_fixed":
        shocked = fx * (1.0 + shock_pct)

    elif scenario == "shock_year":
        if shock_years is None:
            raise ValueError("shock_year requires 'shock_years'.")
        shocked = fx.copy()
        for yr in shock_years:
            mask = years == yr
            shocked[mask] = fx[mask] * (1.0 + shock_pct)

    elif scenario == "shock_path":
        if shock_path is None:
            raise ValueError("shock_path requires 'shock_path'.")
        shocked = fx.copy()
        for yr, pct in shock_path.items():
            mask = years == yr
            shocked[mask] = fx[mask] * (1.0 + pct)

    else:
        raise ValueError(f"Unknown FX shock scenario '{scenario}'.")

    df[f"{fx_col}_shocked"] = shocked
    return df
