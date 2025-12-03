import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from src.data.corridor_flow_v2 import (
    run_corridor_foe_pipeline,
    CorridorFlowConfig,
    default_foe_callback,
)
from src.data.corridor_builder import load_us_kenya_annual_2009_2024
from src.data.macro_fx_loader import load_usd_kes_fx_annual  # <-- NEW


def load_us_ken_corridor_annual() -> pd.DataFrame:
    """Build real annual US→Kenya corridor flow using WB inflow/outflow data + FX."""
    data = load_us_kenya_annual_2009_2024()

    years = data["years"]
    kenya_inf = data["kenya_inflows"]
    us_out = data["us_outflows"]

    corridor_vals = pd.Series(
        [min(kenya_inf[y], us_out[y]) for y in years],
        index=years,
    )

    base_df = pd.DataFrame({
        "year": years,
        "remittance_usd": corridor_vals.values,
    })

    # Join FX feature
    fx_df = load_usd_kes_fx_annual()
    df = base_df.merge(fx_df, on="year", how="left")

    return df


def ensure_plot_dir() -> Path:
    """Create reports/plots directory if missing."""
    plot_dir = Path("reports/plots")
    plot_dir.mkdir(parents=True, exist_ok=True)
    return plot_dir


def main():
    # 1) Build annual DF
    annual_df = load_us_ken_corridor_annual()

    cfg = CorridorFlowConfig(corridor_id="US-KEN")

    # 2) Run FOE pipeline
    result = run_corridor_foe_pipeline(
        annual_df=annual_df,
        cfg=cfg,
        foe_callback=default_foe_callback,
        train_end_year=2023,
        validation_year=2024,
        forecast_years=[2025],
    )

    segments = result["segments"]
    foe_result = result["foe"]["foe_result"]

    # 3) Yearly peak float table
    float_df = foe_result["float_df"]
    yearly_peaks = (
        float_df.groupby("year")["peak_float"]
        .max()
        .reset_index()
        .rename(columns={"peak_float": "peak_float_usd"})
    )

    print("\n=== YEARLY PEAK FLOAT (USD) ===")
    print(yearly_peaks)

    # Ensure directory
    plot_dir = ensure_plot_dir()

    # ---- FIGURE 1: Peak Float Over Time ----
    fig1 = plt.figure(figsize=(8, 4))
    plt.plot(yearly_peaks["year"], yearly_peaks["peak_float_usd"], marker="o")
    plt.xlabel("Year")
    plt.ylabel("Peak Float (USD)")
    plt.title("US→Kenya Corridor – Yearly Peak Float Requirement")
    plt.grid(True)
    plt.tight_layout()

    fig1_path = plot_dir / "peak_float_yearly.png"
    fig1.savefig(fig1_path, dpi=200)
    print(f"Saved: {fig1_path}")

    # ---- FIGURE 2: Actual vs Fitted vs Forecast ----
    train = segments["train"]
    validation = segments["validation"]
    forecast = segments["forecast"]

    train_part = train[["year", "remittance_usd", "remittance_hat_usd"]].copy()
    validation_part = validation[["year", "remittance_usd", "remittance_hat_usd"]].copy()

    forecast_part = forecast[["year", "remittance_hat_usd"]].copy()
    forecast_part["remittance_usd"] = pd.NA

    annual_model_df = (
        pd.concat([train_part, validation_part, forecast_part], ignore_index=True)
        .sort_values("year")
    )

    fig2 = plt.figure(figsize=(8, 4))
    plt.plot(
        annual_model_df["year"],
        annual_model_df["remittance_hat_usd"],
        label="Model (Fit + Forecast)",
    )

    actual_mask = annual_model_df["remittance_usd"].notna()
    plt.scatter(
        annual_model_df.loc[actual_mask, "year"],
        annual_model_df.loc[actual_mask, "remittance_usd"],
        label="Actual",
        zorder=3,
    )

    plt.xlabel("Year")
    plt.ylabel("Annual Corridor Flow (USD)")
    plt.title("US→Kenya Corridor – Actual vs Fitted vs Forecast")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    fig2_path = plot_dir / "corridor_actual_vs_model.png"
    fig2.savefig(fig2_path, dpi=200)
    print(f"Saved: {fig2_path}")

    # ---- FIGURE 3: Residual Diagnostics (Annual) ----
    combined = pd.concat(
        [
            train[["year", "remittance_usd", "remittance_hat_usd"]],
            validation[["year", "remittance_usd", "remittance_hat_usd"]],
        ],
        ignore_index=True,
    )
    combined["residual"] = combined["remittance_usd"] - combined["remittance_hat_usd"]

    fig3 = plt.figure(figsize=(8, 4))
    plt.axhline(0, linewidth=1)
    plt.scatter(combined["year"], combined["residual"])
    plt.plot(combined["year"], combined["residual"])
    plt.xlabel("Year")
    plt.ylabel("Residual (Actual - Model)")
    plt.title("US→Kenya Corridor – Annual Residual Diagnostics")
    plt.grid(True)
    plt.tight_layout()

    fig3_path = plot_dir / "corridor_residuals.png"
    fig3.savefig(fig3_path, dpi=200)
    print(f"Saved: {fig3_path}")

    # Show all figures
    plt.show()


if __name__ == "__main__":
    main()
