# src/foe/scenarios/fx_sensitivity.py

from __future__ import annotations
import pandas as pd
from copy import deepcopy
import src.foe.corridor_flow as corridor_flow


def run_fx_sensitivity_grid(
    annual_df: pd.DataFrame,
    base_cfg,
    train_end_year: int,
    validation_year: int,
    forecast_years,
):
    """
    B11:
    - Run FX scenarios
    - Forecast corridor flows
    - Run FOE per scenario
    - Return combined DataFrame with FOE metadata
    """

    scenarios = {
        "base_none": {"scenario": "none", "pct": 0.0},
        "fx_minus_10pct": {"scenario": "shock_fixed", "pct": -0.10},
        "fx_plus_10pct": {"scenario": "shock_fixed", "pct": +0.10},
    }

    outputs = []

    for scenario_name, params in scenarios.items():

        cfg = deepcopy(base_cfg)

        # Run full pipeline including FOE
        result = corridor_flow.run_corridor_foe_pipeline(
            annual_df=annual_df,
            cfg=cfg,
            train_end_year=train_end_year,
            validation_year=validation_year,
            forecast_years=forecast_years,
        )

        path = result["full_annual"].copy()
        path["scenario_name"] = scenario_name

        # FOE object saved as string for now
        path["foe_output"] = str(result["foe"])

        outputs.append(path)

    return pd.concat(outputs, ignore_index=True)
