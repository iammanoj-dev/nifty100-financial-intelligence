import sqlite3
from pathlib import Path
import pandas as pd

from src.analytics.ratios import (
    return_on_capital_employed,
)

DATABASE = "database/nifty100.db"
OUTPUT_FILE = "output/ratio_edge_cases.log"


def connect_database():
    """Connect to SQLite database."""
    return sqlite3.connect(DATABASE)


def load_data(conn):
    """Load required tables."""

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn,
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn,
    )

    profit = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn,
    )

    balance = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn,
    )

    financial_ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    return (
        companies,
        sectors,
        profit,
        balance,
        financial_ratios,
    )
def classify_issue(difference):
    """
    Classify ratio anomaly.
    """

    if difference > 20:
        return "DATA SOURCE ISSUE"

    if difference > 10:
        return "VERSION DIFFERENCE"

    return "FORMULA DISCREPANCY"


def validate_roce(
    companies,
    sectors,
    profit,
    balance,
):
    """
    Recompute ROCE and compare with source ROCE.
    """

    results = []

    merged = (
        profit.merge(
            balance,
            on=["company_id", "year"],
            how="inner",
            suffixes=("_p", "_b"),
        )
        .merge(
            companies[
                [
                    "id",
                    "roce_percentage",
                ]
            ],
            left_on="company_id",
            right_on="id",
            how="left",
        )
        .merge(
            sectors[
                [
                    "company_id",
                    "broad_sector",
                ]
            ],
            on="company_id",
            how="left",
        )
    )

    for _, row in merged.iterrows():

        computed = return_on_capital_employed(
            row["operating_profit"],
            row["equity_capital"],
            row["reserves"],
            row["borrowings"],
            row["broad_sector"],
        )

        source = row["roce_percentage"]

        if (
            computed is None
            or pd.isna(source)
        ):
            continue

        diff = abs(
            computed - source
        )

        if diff > 5:

            results.append(
                {
                    "company": row["company_id"],
                    "metric": "ROCE",
                    "computed": round(computed, 2),
                    "source": round(source, 2),
                    "difference": round(diff, 2),
                    "category": classify_issue(diff),
                }
            )

    return results


def validate_roe(
    companies,
    financial_ratios,
):
    """
    Compare stored ROE against source ROE.
    """

    results = []

    merged = financial_ratios.merge(
        companies[
            [
                "id",
                "roe_percentage",
            ]
        ],
        left_on="company_id",
        right_on="id",
        how="left",
    )

    for _, row in merged.iterrows():

        if (
            pd.isna(row["return_on_equity_pct"])
            or pd.isna(row["roe_percentage"])
        ):
            continue

        diff = abs(
            row["return_on_equity_pct"]
            - row["roe_percentage"]
        )

        if diff > 5:

            results.append(
                {
                    "company": row["company_id"],
                    "metric": "ROE",
                    "computed": round(
                        row["return_on_equity_pct"],
                        2,
                    ),
                    "source": round(
                        row["roe_percentage"],
                        2,
                    ),
                    "difference": round(diff, 2),
                    "category": classify_issue(diff),
                }
            )

    return results
def write_log(results):
    """
    Write edge case report.
    """

    Path("output").mkdir(
        exist_ok=True
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
    ) as f:

        f.write("=" * 60 + "\n")
        f.write("RATIO EDGE CASE REPORT\n")
        f.write("=" * 60 + "\n\n")

        if not results:

            f.write(
                "No anomalies detected.\n"
            )

            return

        for row in results:

            f.write(
                f"Company    : {row['company']}\n"
            )

            f.write(
                f"Metric     : {row['metric']}\n"
            )

            f.write(
                f"Calculated : {row['computed']}\n"
            )

            f.write(
                f"Source     : {row['source']}\n"
            )

            f.write(
                f"Difference : {row['difference']}\n"
            )

            f.write(
                f"Category   : {row['category']}\n"
            )

            f.write(
                "-" * 60 + "\n"
            )


def financial_sector_note(
    sectors,
):
    """
    Add Financials carve-out note.
    """

    notes = []

    financials = sectors[
        sectors["broad_sector"] == "Financials"
    ]

    for _, row in financials.iterrows():

        notes.append(
            {
                "company": row["company_id"],
                "metric": "LEVERAGE",
                "computed": "-",
                "source": "-",
                "difference": "-",
                "category": (
                    "High leverage check skipped "
                    "(Financial Institution)"
                ),
            }
        )

    return notes


def main():

    conn = connect_database()

    (
        companies,
        sectors,
        profit,
        balance,
        financial_ratios,
    ) = load_data(conn)

    roce_results = validate_roce(
        companies,
        sectors,
        profit,
        balance,
    )

    roe_results = validate_roe(
        companies,
        financial_ratios,
    )

    carveout = financial_sector_note(
        sectors,
    )

    results = (
        carveout
        + roce_results
        + roe_results
    )

    write_log(results)

    conn.close()

    print("=" * 60)
    print("Day 13 completed")
    print("=" * 60)
    print(f"Total edge cases : {len(results)}")
    print(f"Log written to   : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
