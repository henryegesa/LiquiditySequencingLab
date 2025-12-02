import pandas as pd

from src.data.world_bank_loader import load_inflows, load_outflows


def extract_country_series(df: pd.DataFrame, country_name: str) -> pd.Series:
    """
    Return a series {year: value} for the specified country.
    """
    row = df[df["Country Name"] == country_name]
    if row.empty:
        raise ValueError(f"Country '{country_name}' not found in dataset.")

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
        - years
        - kenya_inflows
        - us_outflows
    """
    inflows = load_inflows()
    outflows = load_outflows()

    kenya_inf = extract_country_series(inflows, "Kenya")
    us_out = extract_country_series(outflows, "United States")

    years = list(range(2009, 2025))
    kenya_inf = kenya_inf.loc[years]
    us_out = us_out.loc[years]

    return {
        "years": years,
        "kenya_inflows": kenya_inf,
        "us_outflows": us_out,
    }


def build_us_kenya_corridor_series(
    corridor_share_of_us_outflows: float = 0.02,
) -> pd.DataFrame:
    """
    Build an approximate US -> Kenya corridor series using:
        corridor_flow(t) = min( KenyaInflows(t),
                                 USOutflows(t) * corridor_share )

    Args:
        corridor_share_of_us_outflows: assumed share of US outflows
                                       that go to Kenya (e.g. 0.02 = 2%).

    Returns:
        DataFrame with columns:
            year
            kenya_inflows
            us_outflows
            corridor_flow
    """
    data = load_us_kenya_annual_2009_2024()
    years = data["years"]
    kenya_inf = data["kenya_inflows"]
    us_out = data["us_outflows"]

    # Approximate bilateral corridor flow
    approx_from_us = us_out * corridor_share_of_us_outflows
    corridor_flow = pd.concat(
        [kenya_inf, approx_from_us], axis=1, keys=["kenya_inf", "from_us_share"]
    ).min(axis=1)

    df = pd.DataFrame(
        {
            "year": years,
            "kenya_inflows": kenya_inf.values,
            "us_outflows": us_out.values,
            "corridor_flow": corridor_flow.values,
        }
    )

    return df
