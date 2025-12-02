import pandas as pd
from pathlib import Path

from src.data.world_bank_loader import load_inflows, load_outflows


def extract_country_series(df: pd.DataFrame, country_name: str) -> pd.Series:
    """
    Return a series {year: value} for the specified country.
    """
    row = df[df["Country Name"] == country_name]
    if row.empty:
        raise ValueError(f"Country '{country_name}' not found in dataset.")

    # Only keep year columns (1960–2024)
    year_cols = [c for c in row.columns if c.isdigit()]

    series = row[year_cols].iloc[0].astype(float)
    series.index = series.index.astype(int)

    return series


def load_us_kenya_annual_2009_2024():
    """
    Extract annual series for:
    - Kenya inflows (BX…)
    - US outflows (BM…)

    Returns:
        dict with:
        - kenya_inflows
        - us_outflows
        - years
    """
    inflows = load_inflows()
    outflows = load_outflows()

    kenya_inf = extract_country_series(inflows, "Kenya")
    us_out = extract_country_series(outflows, "United States")

    # Restrict to 2009–2024
    years = list(range(2009, 2025))
    kenya_inf = kenya_inf.loc[years]
    us_out = us_out.loc[years]

    return {
        "years": years,
        "kenya_inflows": kenya_inf,
        "us_outflows": us_out,
    }
