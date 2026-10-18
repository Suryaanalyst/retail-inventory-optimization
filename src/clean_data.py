
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

SALES_FILE = OUTPUT_DIR / "online_retail_cleaned.csv"
RETURNS_FILE = OUTPUT_DIR / "online_retail_returns.csv"
CANCELLATIONS_FILE = OUTPUT_DIR / "online_retail_cancellations.csv"


def main():
    print("Starting data cleaning...")

    df = pd.read_excel(INPUT_FILE)
    print("Original rows:", len(df))

    # Remove exact duplicate records.
    df = df.drop_duplicates().copy()

    # Remove rows without a product description.
    df = df.dropna(subset=["Description"]).copy()

    # Convert columns to correct data types.
    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )
    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce"
    )
    df["UnitPrice"] = pd.to_numeric(
        df["UnitPrice"], errors="coerce"
    )

    # Remove rows with invalid essential values.
    df = df.dropna(
        subset=["InvoiceDate", "Quantity", "UnitPrice"]
    ).copy()

    # Identify cancellation invoices.
    is_cancellation = df["InvoiceNo"].astype(str).str.startswith("C")

    # Identify negative-quantity records separately.
    is_return = df["Quantity"] < 0

    cancellations = df[is_cancellation].copy()
    returns = df[is_return & ~is_cancellation].copy()

    # Keep only positive-quantity, positive-price sales
    # in the main sales dataset.
    sales = df[
        (~is_cancellation)
        & (df["Quantity"] > 0)
        & (df["UnitPrice"] > 0)
    ].copy()

    # Calculate gross sales value for eligible sales records.
    sales["SalesValue"] = sales["Quantity"] * sales["UnitPrice"]

    # Save separate outputs without changing the original Excel file.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sales.to_csv(SALES_FILE, index=False)
    returns.to_csv(RETURNS_FILE, index=False)
    cancellations.to_csv(CANCELLATIONS_FILE, index=False)

    print("\nCleaning summary")
    print("-" * 35)
    print("Unique rows after duplicate removal:", len(df))
    print("Sales records:", len(sales))
    print("Negative-quantity return records:", len(returns))
    print("Cancellation invoice records:", len(cancellations))
    print("Sales value column added.")

    print("\nFiles saved:")
    print(SALES_FILE)
    print(RETURNS_FILE)
    print(CANCELLATIONS_FILE)

    print("\nPhase 3 cleaning completed!")


if __name__ == "__main__":
    main()
