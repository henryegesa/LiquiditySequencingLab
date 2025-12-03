# src/foe/forecasting/model_base.py

from abc import ABC, abstractmethod
from typing import List
import pandas as pd


class ForecastModel(ABC):
    """
    Base interface for all corridor forecast models.

    Expect input df with columns:
      - year (int)
      - remittance_usd (float)
    """

    @abstractmethod
    def fit(self, df: pd.DataFrame) -> None:
        """Fit model on historical annual data."""
        ...

    @abstractmethod
    def predict(self, years: List[int]) -> pd.DataFrame:
        """
        Predict remittance for given years.

        Returns DataFrame with:
          - year
          - remittance_hat_usd
        """
        ...
