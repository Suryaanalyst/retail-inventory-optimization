
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_DIR = PROJECT_ROOT / "outputs"


def main():
    print("=" * 50)
    print("RETAIL BUSINESS KPI ANALYSIS")
    print("=" * 50)

    sales_file = DATA_DIR / "online_retail_cleaned.csv"
    returns_file = DATA_DIR / "online_retail_returns.csv"
    cancellations_file = (
        DATA_DIR / "online_retail_cancellations.csv"
    )

    sales = pd.read_csv(
        sales_file,
        dtype={"InvoiceNo": "string"},
        parse_dates=["InvoiceDate"],
    )

    returns = pd.read_csv(returns_file)
    cancellations = pd.read_csv(cancellations_file)

    total_sales = sales["SalesValue"].sum()
    total_units = sales["Quantity"].sum()
    total_orders = sales["InvoiceNo"].nunique()

    average_order_value = (
        total_sales / total_orders if total_orders else 0
    )

    monthly_sales = (
        sales.assign(
            Month=sales["InvoiceDate"].dt.to_period("M")
        )
        .groupby("Month")["SalesValue"]
        .sum()
        .sort_index()
    )

    monthly_growth = monthly_sales.pct_change() * 100

    kpis = pd.DataFrame([
        {"KPI": "Total Sales", "Value": total_sales},
        {"KPI": "Total Units Sold", "Value": total_units},
        {"KPI": "Unique Invoices", "Value": total_orders},
        {
            "KPI": "Average Order Value",
            "Value": average_order_value,
        },
        {
            "KPI": "Negative-Quantity Return Records",
            "Value": len(returns),
        },
        {
            "KPI": "Cancellation Invoice Records",
            "Value": len(cancellations),
        },
    ])

    monthly = monthly_sales.rename("TotalSales").to_frame()
    monthly["MonthlyGrowthPct"] = monthly_growth
    monthly.index = monthly.index.astype(str)
    monthly.index.name = "Month"
    monthly = monthly.reset_index()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    kpis.to_csv(OUTPUT_DIR / "business_kpis.csv", index=False)
    monthly.to_csv(OUTPUT_DIR / "monthly_kpis.csv", index=False)

    print("\nBUSINESS KPIs")
    print(kpis.to_string(index=False))

    print("\nMONTHLY SALES AND GROWTH")
    print(monthly.to_string(index=False))

    print("\nSaved:")
    print("outputs/business_kpis.csv")
    print("outputs/monthly_kpis.csv")

    print("\nKPI analysis completed!")


if __name__ == "__main__":
    main()
