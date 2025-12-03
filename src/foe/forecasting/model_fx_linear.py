# src/foe/forecasting/model_fx_linear.py

from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd

from .model_base import ForecastModel


class FXLinearModel(ForecastModel):
    """
    Multivariate linear regression model for FX-adjusted remittance flow forecasting.

    Model form:
        remittance_usd = b0 + b1 * year + b2 * usd_kes

    This captures:
        - long-term secular trend (year)
        - FX pressure (usd_kes)
    """

    def __init__(self) -> None:
        # _coef_ = [b0, b1, b2]
        self._coef_: Optional[np.ndarray] = None

    # ---------------------------------------------------------
    # FIT
    # ---------------------------------------------------------
    def fit(self, df: pd.DataFrame) -> None:
        """
        Fit the FX-linear model on a DataFrame with columns:
          - year
          - remittance_usd
          - usd_kes

        Raises a ValueError if required columns are missing.
        """
        required_cols = {"year", "remittance_usd", "usd_kes"}
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"FXLinearModel.fit missing columns: {missing}")

        # dependent variable
        y = df["remittance_usd"].astype(float).values

        # independent variables: intercept, year, usd_kes
        X = np.column_stack(
            [
                np.ones(len(df)),                         # intercept term
                df["year"].astype(float).values,         # time trend
                df["usd_kes"].astype(float).values,      # FX rate driver
            ]
        )

        # OLS solution: minimize ||Xb - y||^2 using least squares
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        self._coef_ = coef  # np.ndarray of shape (3,)

    # ---------------------------------------------------------
    # INTERNAL PREDICTION CORE
    # ---------------------------------------------------------
    def _predict_internal(
        self,
        years: List[int],
        usd_kes: List[float]
    ) -> np.ndarray:
        """
        Internal numerical predictor. Computes:
            b0 + b1*year + b2*usd_kes

        Requires:
            len(years) == len(usd_kes)
        """
        if self._coef_ is None:
            raise RuntimeError("FXLinearModel must be fit() before predict().")

        if len(years) != len(usd_kes):
            raise ValueError("years and usd_kes must have same length.")

        years_arr = np.asarray(years, dtype=float)
        fx_arr = np.asarray(usd_kes, dtype=float)

        X = np.column_stack(
            [
                np.ones(len(years)),
                years_arr,
                fx_arr,
            ]
        )

        return X @ self._coef_

    # ---------------------------------------------------------
    # NORMAL predict() IS NOT USED — FORCE USE OF FEATURES
    # ---------------------------------------------------------
    def predict(self, years: List[int]) -> pd.DataFrame:
        """
        This model is FX-dependent; predict() without FX is unsafe.

        Use predict_with_features(years, usd_kes) instead.
        """
        raise NotImplementedError(
            "FXLinearModel requires FX values. "
            "Call predict_with_features(years, usd_kes) instead."
        )

    # ---------------------------------------------------------
    # PUBLIC METHOD: FULL FX-AWARE PREDICTION
    # ---------------------------------------------------------
    def predict_with_features(
        self,
        years: List[int],
        usd_kes: List[float],
    ) -> pd.DataFrame:
        """
        Predict using a fully specified feature vector for each year.

        Inputs:
            years:    [2025, 2026, ...]
            usd_kes:  corresponding FX values for those years

        Returns:
            DataFrame with columns:
                - year
                - remittance_hat_usd
        """
        y_hat = self._predict_internal(years, usd_kes)
        return pd.DataFrame(
            {
                "year": years,
                "remittance_hat_usd": y_hat,
            }
        )
