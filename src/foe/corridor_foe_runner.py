# src/foe/corridor_foe_runner.py

from typing import Dict, Any
import pandas as pd

from .corridor_adapter import corridor_to_foe_input
from .engine import run_foe  # your existing FOE v1 entrypoint


def foe_corridor_runner(
    annual_path: pd.DataFrame,
    cfg: Any
) -> Dict[str, Any]:
    """
    Convert annual path → intra-year synthetic flows → FOE engine.
    Returns FOE metrics/results.
    """

    # Convert annual totals to monthly flow schedule
    monthly_flows = corridor_to_foe_input(annual_path)

    # Feed into FOE v1
    foe_result = run_foe(
        corridor_id=cfg.corridor_id,
        flows_df=monthly_flows
    )

    return {
        "monthly_flows": monthly_flows,
        "foe_result": foe_result
    }
