
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

EXPECTED = {
    "Total Sales": 10642110.80,
    "Total Units Sold": 5572420,
    "Unique Invoices": 19962,
    "Average Order Value": 533.1719,
}


def main():
    print("=" * 50)
    print("PHASE 9 - KPI VALIDATION")
    print("=" * 50)

    df = pd.read_csv(
        DATA_FILE,
        dtype={"InvoiceNo": "string"},
        parse_dates=["InvoiceDate"],
    )

    actual = {
        "Total Sales": df["SalesValue"].sum(),
        "Total Units Sold": df["Quantity"].sum(),
        "Unique Invoices": df["InvoiceNo"].nunique(),
    }

    actual["Average Order Value"] = (
        actual["Total Sales"] / actual["Unique Invoices"]
    )

    results = []

    for kpi, expected_value in EXPECTED.items():
        actual_value = actual[kpi]

        passed = abs(actual_value - expected_value) < 0.02

        results.append({
            "KPI": kpi,
            "Expected": expected_value,
            "Actual": actual_value,
            "Status": "PASS" if passed else "CHECK",
        })

    # Check whether monthly sales reconcile to total sales.
    monthly_sales = (
        df.groupby(df["InvoiceDate"].dt.to_period("M"))[
            "SalesValue"
        ].sum()
    )

    monthly_total = monthly_sales.sum()
    monthly_passed = abs(
        monthly_total - actual["Total Sales"]
    ) < 0.02

    results.append({
        "KPI": "Monthly Sales Reconciliation",
        "Expected": actual["Total Sales"],
        "Actual": monthly_total,
        "Status": "PASS" if monthly_passed else "CHECK",
    })

    report = pd.DataFrame(results)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    report.to_csv(
        OUTPUT_DIR / "kpi_validation_report.csv",
        index=False,
    )

    print("\nVALIDATION RESULTS")
    print(report.to_string(index=False))

    if (report["Status"] == "PASS").all():
        print("\nAll KPI validation checks passed!")
    else:
        print("\nSome checks need investigation.")

    print("\nSaved: outputs/kpi_validation_report.csv")


if __name__ == "__main__":
    main()

