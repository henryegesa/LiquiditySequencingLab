# src/foe/engine.py

import pandas as pd

from src.foe.flow_profile import monthly_to_daily_flow
from src.foe.float_optimizer import compute_float_series, summarize_float_metrics


def run_foe(corridor_id: str, flows_df: pd.DataFrame):
    """
    FOE v1:
    - Input: monthly flows_df with columns [year, month, flow_usd]
    - Expand to daily flows
    - Compute float requirement with a settlement delay
    - Return detailed series + summary metrics
    """

    # Step 1: monthly -> daily expansion
    daily_df = monthly_to_daily_flow(flows_df)

    # Step 2: compute float series with 2-day settlement delay (v1 default)
    float_df = compute_float_series(daily_df, settlement_delay_days=2)

    # Step 3: summarise metrics
    metrics = summarize_float_metrics(float_df)

    return {
        "corridor_id": corridor_id,
        "daily_df": daily_df,
        "float_df": float_df,
        "metrics": metrics,
    }
