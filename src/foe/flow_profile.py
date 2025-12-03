# src/foe/flow_profile.py

import pandas as pd
import calendar


def monthly_to_daily_flow(monthly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert monthly remittance flow into daily flow.
    Assumes `monthly_df` has columns:
        - year
        - month
        - flow_usd

    v1: split evenly across all days in the month.
    """
    rows = []

    for _, row in monthly_df.iterrows():
        year = int(row["year"])
        month = int(row["month"])
        flow = float(row["flow_usd"])

        days_in_month = calendar.monthrange(year, month)[1]
        daily_amount = flow / days_in_month

        for day in range(1, days_in_month + 1):
            rows.append(
                {
                    "year": year,
                    "month": month,
                    "day": day,
                    "flow_usd": daily_amount,
                }
            )

    return pd.DataFrame(rows)
