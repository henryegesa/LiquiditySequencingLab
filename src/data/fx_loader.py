# src/data/fx_loader.py

import pandas as pd
from pathlib import Path

FX_FILE = Path("data/fx/usd_kes_annual.csv")

def load_usd_kes():
    """
    Load annual USD/KES FX.
    CSV must contain:
        year, usd_kes
    """
    df = pd.read_csv(FX_FILE)
    df = df.sort_values("year").reset_index(drop=True)
    return df
