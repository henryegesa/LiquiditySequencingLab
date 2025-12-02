from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class CorridorFloatInput:
    """
    Inputs for float sizing for a single corridor over a given risk horizon.
    All amounts are in base currency (e.g. USD).
    """

    corridor_id: str
    currency: str
    expected_outflow: float        # mean net outflow over the risk horizon
    outflow_volatility: float      # std dev of net outflow over the horizon
    service_level: float           # e.g. 0.95 for 95% probability of no stock-out
    cost_of_float_per_year: float  # cost of capital, e.g. 0.08 for 8% per year
    horizon_days: float = 1.0      # risk horizon in days (e.g. settlement lag)


@dataclass
class CorridorFloatResult:
    """
    Result of float sizing for one corridor.
    """

    corridor_id: str
    required_float: float
    annual_float_cost: float
    z_value: float


class FloatOptimizationEngine:
    """
    Corridor-level Float Optimization Engine (FOE) v1.

    Responsibilities:
    - Given mean and volatility of net outflows over a horizon,
      compute required float to hit a target service level.
    - Estimate annual cost of holding that float.
    """

    def __init__(self) -> None:
        # Simple mapping from service level to z-score.
        # Later we can replace this with a proper inverse normal CDF.
        self._z_map: Dict[float, float] = {
            0.90: 1.28,
            0.95: 1.64,
            0.99: 2.33,
        }

    def _z_for_service_level(self, service_level: float) -> float:
        # Default to 95% if not in the map.
        return self._z_map.get(service_level, 1.64)

    def size_float(self, inp: CorridorFloatInput) -> CorridorFloatResult:
        """
        Compute required float and its annual holding cost for a corridor.
        Formula:
            required_float = mean_outflow + z * volatility
        """

        z = self._z_for_service_level(inp.service_level)
        mean = max(inp.expected_outflow, 0.0)
        sigma = max(inp.outflow_volatility, 0.0)

        required = mean + z * sigma
        required = max(required, 0.0)

        annual_cost = required * inp.cost_of_float_per_year

        return CorridorFloatResult(
            corridor_id=inp.corridor_id,
            required_float=required,
            annual_float_cost=annual_cost,
            z_value=z,
        )
