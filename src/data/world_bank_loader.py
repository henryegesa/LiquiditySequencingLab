import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/world_bank")


def load_inflows() -> pd.DataFrame:
    """
    Load World Bank remittances received (BX...) for all countries.
    """
    file = DATA_DIR / "API_BX.TRF.PWKR.CD.DT_DS2_en_csv_v2_128516.csv"
    df = pd.read_csv(file, skiprows=4)
    return df


def load_outflows() -> pd.DataFrame:
    """
    Load World Bank remittances paid (BM...) for all countries.
    """
    file = DATA_DIR / "API_BM.TRF.PWKR.CD.DT_DS2_en_csv_v2_5897.csv"
    df = pd.read_csv(file, skiprows=4)
    return df
