# src/foe/forecasting/__init__.py

from .model_base import ForecastModel
from .model_logtrend import LogTrendModel
from .model_fx_linear import FXLinearModel


def get_forecast_model(name: str = "logtrend") -> ForecastModel:
    """
    Simple factory for forecast models.

    name:
      - "logtrend"  -> LogTrendModel (default)
      - "fx_linear" -> FXLinearModel (uses year + usd_kes)
    """
    name = name.lower()

    if name == "logtrend":
        return LogTrendModel()
    if name == "fx_linear":
        return FXLinearModel()

    raise ValueError(f"Unknown forecast model: {name}")
