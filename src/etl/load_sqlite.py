import sqlite3
import pandas as pd

DATABASE_PATH = "database/nifty100.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def load_table(excel_file, table_name, header_row):

    conn = get_connection()

    df = pd.read_excel(
        excel_file,
        header=header_row,
    )

    print("\n" + "=" * 60)
    print(f"Loading {table_name}")
    print("=" * 60)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 3 Rows:")
    print(df.head(3))

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False,
    )

    row_count = len(df)

    conn.close()

    return row_count


def main():

    datasets = [
        ("data/raw/companies.xlsx", "companies", 1),
        ("data/raw/profitandloss.xlsx", "profitandloss", 1),
        ("data/raw/balancesheet.xlsx", "balancesheet", 1),
        ("data/raw/cashflow.xlsx", "cashflow", 1),
        ("data/raw/analysis.xlsx", "analysis", 1),
        ("data/raw/documents.xlsx", "documents", 1),
        ("data/raw/prosandcons.xlsx", "prosandcons", 1),
        ("data/raw/sectors.xlsx", "sectors", 0),
        ("data/raw/peer_groups.xlsx", "peer_groups", 0),
        ("data/raw/stock_prices.xlsx", "stock_prices", 0),
        ("data/raw/financial_ratios.xlsx", "financial_ratios", 0),
        ("data/raw/market_cap.xlsx", "market_cap", 0),
    ]

    for excel_file, table_name, header_row in datasets:

        try:

            rows = load_table(
                excel_file,
                table_name,
                header_row,
            )

            print(f"\nSUCCESS -> {table_name}: {rows} rows loaded")

        except Exception as e:

            print(f"\nFAILED -> {table_name}")
            print(f"ERROR: {e}")

            break


if __name__ == "__main__":
    main()
