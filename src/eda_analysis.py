
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "online_retail_cleaned.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs"


def main():
    print("=" * 50)
    print("RETAIL SALES - EXPLORATORY DATA ANALYSIS")
    print("=" * 50)

    df = pd.read_csv(DATA_FILE, parse_dates=["InvoiceDate"])

    # Overall sales metrics
    total_sales = df["SalesValue"].sum()
    total_units = df["Quantity"].sum()
    total_orders = df["InvoiceNo"].nunique()
    total_products = df["StockCode"].nunique()
    total_countries = df["Country"].nunique()

    print("\n1. BUSINESS SUMMARY")
    print("-" * 30)
    print(f"Total sales value: {total_sales:,.2f}")
    print(f"Total units sold: {total_units:,}")
    print(f"Unique invoices: {total_orders:,}")
    print(f"Unique products: {total_products:,}")
    print(f"Countries: {total_countries:,}")

    # Top 10 products by sales value
    top_products = (
        df.groupby("Description", as_index=False)
        .agg(
            TotalSales=("SalesValue", "sum"),
            UnitsSold=("Quantity", "sum"),
        )
        .sort_values("TotalSales", ascending=False)
        .head(10)
    )

    print("\n2. TOP 10 PRODUCTS BY SALES VALUE")
    print(top_products.to_string(index=False))

    # Monthly sales trend
    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    monthly_sales = (
        df.groupby("Month", as_index=False)
        .agg(TotalSales=("SalesValue", "sum"))
        .sort_values("Month")
    )

    print("\n3. MONTHLY SALES")
    print(monthly_sales.to_string(index=False))

    # Top 10 countries by sales value
    country_sales = (
        df.groupby("Country", as_index=False)
        .agg(TotalSales=("SalesValue", "sum"))
        .sort_values("TotalSales", ascending=False)
        .head(10)
    )

    print("\n4. TOP 10 COUNTRIES BY SALES")
    print(country_sales.to_string(index=False))

    # Save analysis outputs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    top_products.to_csv(
        OUTPUT_DIR / "top_products.csv", index=False
    )
    monthly_sales.to_csv(
        OUTPUT_DIR / "monthly_sales.csv", index=False
    )
    country_sales.to_csv(
        OUTPUT_DIR / "country_sales.csv", index=False
    )

    print("\n5. OUTPUT FILES CREATED")
    print("outputs/top_products.csv")
    print("outputs/monthly_sales.csv")
    print("outputs/country_sales.csv")

    print("\nEDA completed successfully!")


if __name__ == "__main__":
    main()
