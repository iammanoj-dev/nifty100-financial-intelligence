import sqlite3
import pandas as pd
import re

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)

from src.analytics.cashflow import (
    free_cash_flow,
    capex_intensity,
)

from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)

DATABASE = "database/nifty100.db"
def normalize_year(value):
    """
    Convert different financial year formats
    into a common 4-digit year.

    Examples

    Mar 2022 -> 2022
    Dec 2012 -> 2012
    Mar-22 -> 2022
    FY24 -> 2024
    """

    if pd.isna(value):
        return None

    value = str(value).strip()

    match = re.search(r"(20\d{2})", value)

    if match:
        return match.group(1)

    match = re.search(r"(\d{2})$", value)

    if match:

        yy = int(match.group(1))

        if yy <= 30:
            return str(2000 + yy)

        return str(1900 + yy)

    return value

def load_tables(conn):
    """
    Load all required tables from SQLite,
    normalize year format,
    remove duplicate company-year records,
    and return clean DataFrames.
    """

    # -----------------------------
    # Read tables
    # -----------------------------

    profit = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn,
    )

    balance = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn,
    )

    cashflow = pd.read_sql(
        "SELECT * FROM cashflow",
        conn,
    )

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn,
    )

    # -----------------------------
    # Normalize year formats
    # -----------------------------

    profit["year"] = profit["year"].apply(normalize_year)

    balance["year"] = balance["year"].apply(normalize_year)

    cashflow["year"] = cashflow["year"].apply(normalize_year)

    # -----------------------------
    # Remove duplicate company-year rows
    # -----------------------------

    profit = (
        profit
        .sort_values("id")
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first",
        )
        .reset_index(drop=True)
    )

    balance = (
        balance
        .sort_values("id")
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first",
        )
        .reset_index(drop=True)
    )

    cashflow = (
        cashflow
        .sort_values("id")
        .drop_duplicates(
            subset=["company_id", "year"],
            keep="first",
        )
        .reset_index(drop=True)
    )

    # -----------------------------
    # Debug information
    # -----------------------------

    print("\n==============================")
    print("Cleaned Source Tables")
    print("==============================")

    print(f"Profit rows    : {len(profit)}")
    print(f"Balance rows   : {len(balance)}")
    print(f"Cashflow rows  : {len(cashflow)}")
    print(f"Companies rows : {len(companies)}")

    print("\nProfit")
    print(profit[["company_id", "year"]].head())

    print("\nBalance")
    print(balance[["company_id", "year"]].head())

    print("\nCashflow")
    print(cashflow[["company_id", "year"]].head())

    return (
        profit,
        balance,
        cashflow,
        companies,
    )

def merge_tables(
    profit,
    balance,
    cashflow,
    companies,
):
    """
    Merge all yearly financial datasets.
    """

    df = profit.merge(
        balance,
        on=["company_id", "year"],
        how="left",
        suffixes=("", "_balance"),
    )

    df = df.merge(
        cashflow,
        on=["company_id", "year"],
        how="left",
        suffixes=("", "_cashflow"),
    )

    df = df.merge(
        companies,
        left_on="company_id",
        right_on="id",
        how="left",
    )

    return df


def calculate_kpis(df):
    """
    Compute KPI columns.
    """

    df["net_profit_margin_pct"] = df.apply(
        lambda x: net_profit_margin(
            x["net_profit"],
            x["sales"],
        ),
        axis=1,
    )

    df["operating_profit_margin_pct"] = df.apply(
        lambda x: operating_profit_margin(
            x["operating_profit"],
            x["sales"],
            x["opm_percentage"],
        ),
        axis=1,
    )

    df["return_on_equity_pct"] = df.apply(
        lambda x: return_on_equity(
            x["net_profit"],
            x["equity_capital"],
            x["reserves"],
        ),
        axis=1,
    )

    df["debt_to_equity"] = df.apply(
        lambda x: debt_to_equity(
            x["borrowings"],
            x["equity_capital"],
            x["reserves"],
        ),
        axis=1,
    )

    df["interest_coverage"] = df.apply(
        lambda x: interest_coverage_ratio(
            x["operating_profit"],
            x["other_income"],
            x["interest"],
        ),
        axis=1,
    )

    df["asset_turnover"] = df.apply(
        lambda x: asset_turnover(
            x["sales"],
            x["total_assets"],
        ),
        axis=1,
    )

    df["free_cash_flow_cr"] = df.apply(
        lambda x: free_cash_flow(
            x["operating_activity"],
            x["investing_activity"],
        ),
        axis=1,
    )

    df["capex_cr"] = df.apply(
        lambda x: capex_intensity(
            x["investing_activity"],
            x["sales"],
        )[0],
        axis=1,
    )

    df["earnings_per_share"] = df["eps"]

    df["book_value_per_share"] = df["book_value"]

    df["dividend_payout_ratio_pct"] = df["dividend_payout"]

    df["total_debt_cr"] = df["borrowings"]

    df["cash_from_operations_cr"] = (
        df["operating_activity"]
    )

    return df


def calculate_growth(df):
    """
    Compute CAGR metrics.
    """

    df = df.sort_values(
        [
            "company_id",
            "year",
        ]
    )

    revenue5 = []
    revenue_flag = []

    pat5 = []
    pat_flag = []

    eps5 = []
    eps_flag = []

    for _, group in df.groupby("company_id"):

        group = group.reset_index(drop=True)

        for i in range(len(group)):

            if i >= 5:

                rev, rf = revenue_cagr(
                    group.loc[i - 5, "sales"],
                    group.loc[i, "sales"],
                    5,
                )

                pat, pf = pat_cagr(
                    group.loc[i - 5, "net_profit"],
                    group.loc[i, "net_profit"],
                    5,
                )

                eps, ef = eps_cagr(
                    group.loc[i - 5, "eps"],
                    group.loc[i, "eps"],
                    5,
                )

            else:

                rev, rf = (None, "INSUFFICIENT")
                pat, pf = (None, "INSUFFICIENT")
                eps, ef = (None, "INSUFFICIENT")

            revenue5.append(rev)
            revenue_flag.append(rf)

            pat5.append(pat)
            pat_flag.append(pf)

            eps5.append(eps)
            eps_flag.append(ef)

    df["revenue_cagr_5yr"] = revenue5
    df["pat_cagr_5yr"] = pat5
    df["eps_cagr_5yr"] = eps5

    df["revenue_cagr_flag"] = revenue_flag
    df["pat_cagr_flag"] = pat_flag
    df["eps_cagr_flag"] = eps_flag

    return df

def composite_quality_score(row):
    """
    Simple composite quality score.

    Equal weighting:
    ROE
    Net Profit Margin
    Operating Profit Margin
    Interest Coverage
    Asset Turnover
    """

    score = 0
    count = 0

    metrics = [
        row["return_on_equity_pct"],
        row["net_profit_margin_pct"],
        row["operating_profit_margin_pct"],
        row["interest_coverage"],
        row["asset_turnover"],
    ]

    for value in metrics:

        if pd.notna(value):

            score += value
            count += 1

    if count == 0:
        return None

    return score / count


def prepare_dataframe(df):
    """
    Final dataframe before inserting into SQLite.
    """

    df["composite_quality_score"] = df.apply(
        composite_quality_score,
        axis=1,
    )

    insert_columns = [

        "company_id",
        "year",

        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",

        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",

        "free_cash_flow_cr",
        "capex_cr",

        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",

        "total_debt_cr",
        "cash_from_operations_cr",

        "revenue_cagr_3yr",
        "revenue_cagr_5yr",
        "revenue_cagr_10yr",

        "pat_cagr_3yr",
        "pat_cagr_5yr",
        "pat_cagr_10yr",

        "eps_cagr_3yr",
        "eps_cagr_5yr",
        "eps_cagr_10yr",

        "revenue_cagr_flag",
        "pat_cagr_flag",
        "eps_cagr_flag",

        "composite_quality_score",
    ]

    for column in insert_columns:

        if column not in df.columns:
            df[column] = None

    return df[insert_columns]


def write_to_sqlite(
    df,
    conn,
):
    """
    Write KPIs into financial_ratios table.
    """

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM financial_ratios"
    )

    records = df.to_records(index=False)

    for record in records:

        cursor.execute(
            """
            INSERT INTO financial_ratios(

                company_id,
                year,

                net_profit_margin_pct,
                operating_profit_margin_pct,
                return_on_equity_pct,

                debt_to_equity,
                interest_coverage,
                asset_turnover,

                free_cash_flow_cr,
                capex_cr,

                earnings_per_share,
                book_value_per_share,
                dividend_payout_ratio_pct,

                total_debt_cr,
                cash_from_operations_cr,

                revenue_cagr_3yr,
                revenue_cagr_5yr,
                revenue_cagr_10yr,

                pat_cagr_3yr,
                pat_cagr_5yr,
                pat_cagr_10yr,

                eps_cagr_3yr,
                eps_cagr_5yr,
                eps_cagr_10yr,

                revenue_cagr_flag,
                pat_cagr_flag,
                eps_cagr_flag,

                composite_quality_score

            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            tuple(record),
        )

    conn.commit()

    print(
        f"Inserted {len(df)} rows into financial_ratios"
    )

def main():
    """
    Execute the complete Day 12 KPI population pipeline.
    """

    conn = sqlite3.connect(DATABASE)

    print("=" * 60)
    print("Loading source tables...")
    print("=" * 60)

    (
        profit,
        balance,
        cashflow,
        companies,
    ) = load_tables(conn)

    print("Merging datasets...")

    df = merge_tables(
        profit,
        balance,
        cashflow,
        companies,
    )

    print(f"Records after merge: {len(df)}")

    print("Calculating KPIs...")

    df = calculate_kpis(df)

    print("Calculating CAGR metrics...")

    df = calculate_growth(df)

    print("Preparing final dataset...")

    final_df = prepare_dataframe(df)

    print("Writing to SQLite...")

    write_to_sqlite(
        final_df,
        conn,
    )

    print("=" * 60)
    print("Day 12 completed successfully.")
    print(f"financial_ratios rows inserted : {len(final_df)}")
    print("=" * 60)

    conn.close()


if __name__ == "__main__":
    main()
