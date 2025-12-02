from src.data.corridor_builder import load_us_kenya_annual_2009_2024


def main() -> None:
    data = load_us_kenya_annual_2009_2024()
    print("Years:", data["years"])
    print("\nKenya inflows (USD):")
    print(data["kenya_inflows"])
    print("\nUS outflows (USD):")
    print(data["us_outflows"])


if __name__ == "__main__":
    main()
