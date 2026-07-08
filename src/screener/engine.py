import sqlite3
import yaml
import pandas as pd

DATABASE = "database/nifty100.db"
CONFIG = "screener_config.yaml"


class ScreenerEngine:

    def __init__(self):

        self.conn = sqlite3.connect(DATABASE)

        with open(
            CONFIG,
            "r",
            encoding="utf-8",
        ) as f:

            self.config = yaml.safe_load(f)

    def load_data(self):
        """
        Load all required tables from SQLite.
        """

        ratios = pd.read_sql(
            "SELECT * FROM financial_ratios",
            self.conn,
        )

        sectors = pd.read_sql(
            """
            SELECT
                company_id,
                broad_sector
            FROM sectors
            """,
            self.conn,
        )

        market = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                market_cap_crore,
                pe_ratio,
                pb_ratio,
                dividend_yield_pct
            FROM market_cap
            """,
            self.conn,
        )

        profit = pd.read_sql(
            """
            SELECT
                company_id,
                year,
                sales,
                net_profit
            FROM profitandloss
            """,
            self.conn,
        )

        # --------------------------
        # Normalize year format
        # --------------------------

        ratios["year"] = ratios["year"].astype(str)

        market["year"] = market["year"].astype(str)

        profit["year"] = (
            profit["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
        )

        profit["year"] = profit["year"].astype(str)

        # --------------------------
        # Merge tables
        # --------------------------

        df = (
            ratios
            .merge(
                sectors,
                on="company_id",
                how="left",
            )
            .merge(
                market,
                on=[
                    "company_id",
                    "year",
                ],
                how="left",
            )
            .merge(
                profit,
                on=[
                    "company_id",
                    "year",
                ],
                how="left",
            )
        )

        print(f"Loaded {len(df)} records")

        return df

    def apply_filters(
        self,
        df,
    ):
        """
        Apply screener filters from YAML.
        """

        filters = self.config["filters"]

        # ---------------- ROE ----------------

        if filters["roe_min"] is not None:
            df = df[
                df["return_on_equity_pct"]
                >= filters["roe_min"]
            ]

        # ---------------- D/E ----------------

        if filters["debt_to_equity_max"] is not None:

            financials = (
                df["broad_sector"]
                == "Financials"
            )

            others = (
                df["debt_to_equity"]
                <= filters["debt_to_equity_max"]
            )

            df = df[
                financials | others
            ]

        # ---------------- Free Cash Flow ----------------

        if filters["free_cash_flow_min"] is not None:

            df = df[
                df["free_cash_flow_cr"]
                >= filters["free_cash_flow_min"]
            ]

        # ---------------- Revenue CAGR ----------------

        if filters["revenue_cagr_5yr_min"] is not None:

            df = df[
                df["revenue_cagr_5yr"]
                >= filters["revenue_cagr_5yr_min"]
            ]

        # ---------------- PAT CAGR ----------------

        if filters["pat_cagr_5yr_min"] is not None:

            df = df[
                df["pat_cagr_5yr"]
                >= filters["pat_cagr_5yr_min"]
            ]

        # ---------------- OPM ----------------

        if filters["operating_profit_margin_min"] is not None:

            df = df[
                df["operating_profit_margin_pct"]
                >= filters["operating_profit_margin_min"]
            ]

        # ---------------- PE ----------------

        if filters["pe_max"] is not None:

            df = df[
                df["pe_ratio"]
                <= filters["pe_max"]
            ]

        # ---------------- PB ----------------

        if filters["pb_max"] is not None:

            df = df[
                df["pb_ratio"]
                <= filters["pb_max"]
            ]

        # ---------------- Dividend Yield ----------------

        if filters["dividend_yield_min"] is not None:

            df = df[
                df["dividend_yield_pct"]
                >= filters["dividend_yield_min"]
            ]

        # ---------------- Interest Coverage ----------------

        if filters["interest_coverage_min"] is not None:

            df["interest_coverage"] = (
                df["interest_coverage"]
                .fillna(float("inf"))
            )

            df = df[
                df["interest_coverage"]
                >= filters["interest_coverage_min"]
            ]

        # ---------------- Market Cap ----------------

        if filters["market_cap_min"] is not None:

            df = df[
                df["market_cap_crore"]
                >= filters["market_cap_min"]
            ]

        # ---------------- Net Profit ----------------

        if filters["net_profit_min"] is not None:

            df = df[
                df["net_profit"]
                >= filters["net_profit_min"]
            ]

        # ---------------- EPS CAGR ----------------

        if filters["eps_cagr_5yr_min"] is not None:

            df = df[
                df["eps_cagr_5yr"]
                >= filters["eps_cagr_5yr_min"]
            ]

        # ---------------- Asset Turnover ----------------

        if filters["asset_turnover_min"] is not None:

            df = df[
                df["asset_turnover"]
                >= filters["asset_turnover_min"]
            ]

        # ---------------- Sales ----------------

        if filters["sales_min"] is not None:

            df = df[
                df["sales"]
                >= filters["sales_min"]
            ]

        # ---------------- Composite Score ----------------

        if "composite_quality_score" not in df.columns:

            score_columns = [
                "return_on_equity_pct",
                "operating_profit_margin_pct",
                "revenue_cagr_5yr",
                "pat_cagr_5yr",
                "asset_turnover",
            ]

            available = [
                c for c in score_columns
                if c in df.columns
            ]

            df["composite_quality_score"] = (
                df[available]
                .fillna(0)
                .mean(axis=1)
            )

        df = df.sort_values(
            by="composite_quality_score",
            ascending=False,
        )

        return df


def main():

    engine = ScreenerEngine()

    df = engine.load_data()

    print(
        f"Loaded {len(df)} rows"
    )

    result = engine.apply_filters(df)

    print(
        f"Returned {len(result)} rows"
    )

    print()

    print(
        result[
            [
                "company_id",
                "year",
                "return_on_equity_pct",
                "debt_to_equity",
                "composite_quality_score",
            ]
        ].head(20)
    )


if __name__ == "__main__":
    main()
