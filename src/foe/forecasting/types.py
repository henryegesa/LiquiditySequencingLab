# src/foe/forecasting/types.py
from __future__ import annotations

from typing import Protocol, List
import pandas as pd


class ForecastModel(Protocol):
    def fit(self, df: pd.DataFrame) -> "ForecastModel":
        """
        df must contain at least:
          - 'year'
          - 'remittance_usd'
        FX-aware models may require extra columns (e.g. 'fx_rate').
        """
        ...

    def predict(self, years: List[int]) -> pd.DataFrame:
        """
        Returns a DataFrame with at least:
          - 'year'
          - 'remittance_hat_usd'
        """
        ...
