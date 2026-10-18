
from pathlib import Path
import sqlite3

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "online_retail_cleaned.csv"
)

DB_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "retail_inventory.db"
)

OUTPUT_DIR = PROJECT_ROOT / "outputs"


def main():
    print("=" * 50)
    print("RETAIL INVENTORY - SQL ANALYTICS")
    print("=" * 50)

    # Check whether the cleaned dataset exists.
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {DATA_FILE}"
        )

    # Read the cleaned CSV.
    df = pd.read_csv(
        DATA_FILE,
        dtype={"InvoiceNo": "string"},
        parse_dates=["InvoiceDate"],
    )

    # Prepare folders and database.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load the dataset into SQLite.
    with sqlite3.connect(DB_FILE) as connection:
        df.to_sql(
            "retail_sales",
            connection,
            if_exists="replace",
            index=False,
        )

        print("\nDataset loaded into SQLite.")
        print("Table name: retail_sales")
        print("Rows loaded:", len(df))

        # Query 1: Top 10 products by sales value.
        top_products_query = """
            SELECT
                Description,
                SUM(SalesValue) AS TotalSales,
                SUM(Quantity) AS UnitsSold
            FROM retail_sales
            GROUP BY Description
            ORDER BY TotalSales DESC
            LIMIT 10;
        """

        top_products = pd.read_sql_query(
            top_products_query, connection
        )

        # Query 2: Monthly sales.
        monthly_sales_query = """
            SELECT
                strftime('%Y-%m', InvoiceDate) AS Month,
                ROUND(SUM(SalesValue), 2) AS TotalSales
            FROM retail_sales
            GROUP BY strftime('%Y-%m', InvoiceDate)
            ORDER BY Month;
        """

        monthly_sales = pd.read_sql_query(
            monthly_sales_query, connection
        )

        # Query 3: Top 10 countries by sales.
        country_sales_query = """
            SELECT
                Country,
                ROUND(SUM(SalesValue), 2) AS TotalSales
            FROM retail_sales
            GROUP BY Country
            ORDER BY TotalSales DESC
            LIMIT 10;
        """

        country_sales = pd.read_sql_query(
            country_sales_query, connection
        )

        # Query 4: Overall business summary.
        summary_query = """
            SELECT
                ROUND(SUM(SalesValue), 2) AS TotalSales,
                SUM(Quantity) AS TotalUnits,
                COUNT(DISTINCT InvoiceNo) AS UniqueInvoices,
                COUNT(DISTINCT StockCode) AS UniqueProducts
            FROM retail_sales;
        """

        summary = pd.read_sql_query(
            summary_query, connection
        )

    # Save SQL query results.
    top_products.to_csv(
        OUTPUT_DIR / "sql_top_products.csv", index=False
    )
    monthly_sales.to_csv(
        OUTPUT_DIR / "sql_monthly_sales.csv", index=False
    )
    country_sales.to_csv(
        OUTPUT_DIR / "sql_country_sales.csv", index=False
    )
    summary.to_csv(
        OUTPUT_DIR / "sql_business_summary.csv", index=False
    )

    print("\nBUSINESS SUMMARY")
    print(summary.to_string(index=False))

    print("\nTOP 10 PRODUCTS")
    print(top_products.to_string(index=False))

    print("\nMONTHLY SALES")
    print(monthly_sales.to_string(index=False))

    print("\nTOP 10 COUNTRIES")
    print(country_sales.to_string(index=False))

    print("\nDatabase saved to:")
    print(DB_FILE)

    print("\nSQL analysis completed successfully!")


if __name__ == "__main__":
    main()
