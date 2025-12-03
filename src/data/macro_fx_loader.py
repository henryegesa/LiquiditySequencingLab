import pandas as pd
from pathlib import Path

def load_usd_kes_fx_annual() -> pd.DataFrame:
    """
    Loads annual average USD/KES FX rates.
    Expected CSV structure:
        year, usd_kes
    """
    path = Path("data/external/fx_usd_kes_annual.csv")
    if not path.exists():
        raise FileNotFoundError(f"Missing FX file: {path}")

    df = pd.read_csv(path)
    if "year" not in df.columns or "usd_kes" not in df.columns:
        raise ValueError("FX CSV must contain 'year' and 'usd_kes' columns.")

    return df.sort_values("year").reset_index(drop=True)
