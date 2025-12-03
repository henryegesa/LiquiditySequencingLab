# src/foe/forecasting/model_logtrend.py

from typing import List, Optional, Tuple

import numpy as np
import pandas as pd

from .model_base import ForecastModel


class LogTrendModel(ForecastModel):
    """
    Log-linear trend model:

        log(y) = a + b * year
        y = exp(a + b * year)

    Simple, fast baseline for remittance forecasting.
    """

    def __init__(self) -> None:
        self._a: Optional[float] = None
        self._b: Optional[float] = None

    def _fit_log_trend(
        self,
        df: pd.DataFrame,
        year_col: str = "year",
        value_col: str = "remittance_usd",
    ) -> Tuple[float, float]:
        y = df[value_col].astype(float).values
        if (y <= 0).any():
            raise ValueError("All values must be positive to use log trend.")

        x = df[year_col].astype(float).values
        log_y = np.log(y)

        b, a = np.polyfit(x, log_y, 1)  # slope, intercept
        return float(a), float(b)

    def _predict_log_trend(self, years: List[int]) -> np.ndarray:
        if self._a is None or self._b is None:
            raise RuntimeError("LogTrendModel must be fit() before predict().")

        x = np.array(years, dtype=float)
        log_y_hat = self._a + self._b * x
        return np.exp(log_y_hat)

    def fit(self, df: pd.DataFrame) -> None:
        """
        Fit the model on a DataFrame with columns:
          - year
          - remittance_usd
        """
        a, b = self._fit_log_trend(df, year_col="year", value_col="remittance_usd")
        self._a, self._b = a, b

    def predict(self, years: List[int]) -> pd.DataFrame:
        """
        Predict for the given list of years.

        Returns:
            DataFrame with:
              - year
              - remittance_hat_usd
        """
        y_hat = self._predict_log_trend(years)
        return pd.DataFrame(
            {
                "year": years,
                "remittance_hat_usd": y_hat,
            }
        )
