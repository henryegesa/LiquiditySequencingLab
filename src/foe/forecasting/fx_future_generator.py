# src/foe/forecasting/fx_future_generator.py

import pandas as pd
import numpy as np

def generate_fx_future_linear(df_fx: pd.DataFrame, future_years):
    """
    Very simple FX extrapolation:
        - linear regression on (year -> usd_kes)
        - predict future years
    Inputs:
        df_fx = DataFrame(year, usd_kes) for history
        future_years = list[int]
    Output:
        DataFrame(year, usd_kes)
    """

    hist = df_fx.copy()

    # Fit linear regression: usd_kes = a + b * year
    X = hist["year"].astype(float).values
    y = hist["usd_kes"].astype(float).values

    coef = np.polyfit(X, y, deg=1)  # [b, a]
    b, a = coef[0], coef[1]

    preds = []
    for yr in future_years:
        fx = a + b * yr
        preds.append({"year": yr, "usd_kes": fx})

    return pd.DataFrame(preds)
