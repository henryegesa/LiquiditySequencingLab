# src/foe/corridor_adapter.py

import pandas as pd

def corridor_to_foe_input(annual_path: pd.DataFrame) -> pd.DataFrame:
    """
    Expand annual corridor flows into a synthetic monthly profile
    for FOE v1. Assumes annual_path has columns:
        - year
        - remittance_hat_usd OR remittance_usd
    """
    rows = []
    for _, row in annual_path.iterrows():
        year = int(row["year"])
        amount = float(
            row["remittance_usd"]
            if not pd.isna(row.get("remittance_usd"))
            else row["remittance_hat_usd"]
        )
        monthly = amount / 12.0

        for m in range(1, 13):
            rows.append({
                "year": year,
                "month": m,
                "flow_usd": monthly,
            })

    return pd.DataFrame(rows)
