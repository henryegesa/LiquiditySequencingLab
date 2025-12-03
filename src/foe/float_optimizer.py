# src/foe/float_optimizer.py

import pandas as pd


def compute_float_series(
    daily_df: pd.DataFrame,
    settlement_delay_days: int = 2
) -> pd.DataFrame:
    """
    Compute required float given daily flows and settlement delay.
    Positive flow = inbound; settlement occurs after N days.
    """
    df = daily_df.copy().reset_index(drop=True)

    # Cumulative inbound volume
    df["cumulative_flow"] = df["flow_usd"].cumsum()

    # Settlement happens after 'settlement_delay_days'
    df["settled"] = df["cumulative_flow"].shift(settlement_delay_days).fillna(0)

    # Float required = inbound not yet settled
    df["float_required"] = df["cumulative_flow"] - df["settled"]

    # Peak float over time
    df["peak_float"] = df["float_required"].cummax()

    return df


def summarize_float_metrics(df: pd.DataFrame) -> dict:
    """
    Summarize key float metrics over the period.
    """
    return {
        "peak_float_usd": float(df["peak_float"].max()),
        "final_float_usd": float(df["float_required"].iloc[-1]),
        "total_flow_usd": float(df["flow_usd"].sum()),
        "days": int(len(df)),
    }
