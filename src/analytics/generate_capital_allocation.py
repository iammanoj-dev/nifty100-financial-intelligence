import sqlite3
import pandas as pd

from cashflow import (
    capital_allocation_pattern,
)

DATABASE = "database/nifty100.db"


def main():

    conn = sqlite3.connect(DATABASE)

    query = """
    SELECT
        company_id,
        year,
        operating_activity,
        investing_activity,
        financing_activity
    FROM cashflow
    """

    df = pd.read_sql(query, conn)

    rows = []

    for _, row in df.iterrows():

        cfo_sign, cfi_sign, cff_sign, label = (
            capital_allocation_pattern(
                row["operating_activity"],
                row["investing_activity"],
                row["financing_activity"],
            )
        )

        rows.append(
            {
                "company_id": row["company_id"],
                "year": row["year"],
                "cfo_sign": cfo_sign,
                "cfi_sign": cfi_sign,
                "cff_sign": cff_sign,
                "pattern_label": label,
            }
        )

    output = pd.DataFrame(rows)

    output.to_csv(
        "output/capital_allocation.csv",
        index=False,
    )

    conn.close()

    print(
        "Generated:",
        len(output),
        "rows"
    )


if __name__ == "__main__":
    main()
