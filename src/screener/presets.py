import pandas as pd

from src.screener.engine import ScreenerEngine


class PresetScreeners:

    def __init__(self):

        self.engine = ScreenerEngine()

        self.df = self.engine.load_data()

    # ----------------------------------------
    # Quality Compounder
    # ----------------------------------------

    def quality_compounder(self):

        return self.df[
            (self.df["return_on_equity_pct"] > 15)
            & (
                (self.df["debt_to_equity"] < 1)
                | (
                    self.df["broad_sector"]
                    == "Financials"
                )
            )
            & (self.df["free_cash_flow_cr"] > 0)
            & (self.df["revenue_cagr_5yr"] > 10)
        ]

    # ----------------------------------------
    # Value Pick
    # ----------------------------------------

    def value_pick(self):

        return self.df[
            (self.df["pe_ratio"] < 20)
            & (self.df["pb_ratio"] < 3)
            & (
                (self.df["debt_to_equity"] < 2)
                | (
                    self.df["broad_sector"]
                    == "Financials"
                )
            )
            & (
                self.df["dividend_yield_pct"]
                > 1
            )
        ]

    # ----------------------------------------
    # Growth Accelerator
    # ----------------------------------------

    def growth_accelerator(self):

        return self.df[
            (self.df["pat_cagr_5yr"] > 20)
            & (
                self.df["revenue_cagr_5yr"]
                > 15
            )
            & (
                (self.df["debt_to_equity"] < 2)
                | (
                    self.df["broad_sector"]
                    == "Financials"
                )
            )
        ]

    # ----------------------------------------
    # Dividend Champion
    # ----------------------------------------

    def dividend_champion(self):

        return self.df[
            (
                self.df["dividend_yield_pct"]
                > 2
            )
            & (
                self.df[
                    "dividend_payout_ratio_pct"
                ]
                < 80
            )
            & (
                self.df["free_cash_flow_cr"]
                > 0
            )
        ]

    # ----------------------------------------
    # Debt Free Blue Chip
    # ----------------------------------------

    def debt_free_bluechip(self):

        return self.df[
            (self.df["debt_to_equity"] == 0)
            & (
                self.df["return_on_equity_pct"]
                > 12
            )
            & (
                self.df["sales"] > 5000
            )
        ]

    # ----------------------------------------
    # Turnaround Watch
    # ----------------------------------------

    def turnaround_watch(self):

        df = self.df.copy()

        df = df.sort_values(
            [
                "company_id",
                "year",
            ]
        )

        df["prev_de"] = (
            df.groupby("company_id")[
                "debt_to_equity"
            ]
            .shift(1)
        )

        return df[
            (
                df["revenue_cagr_3yr"]
                > 10
            )
            & (
                df["free_cash_flow_cr"]
                > 0
            )
            & (
                df["debt_to_equity"]
                < df["prev_de"]
            )
        ]


def main():

    presets = PresetScreeners()

    screens = {
        "Quality Compounder":
            presets.quality_compounder(),

        "Value Pick":
            presets.value_pick(),

        "Growth Accelerator":
            presets.growth_accelerator(),

        "Dividend Champion":
            presets.dividend_champion(),

        "Debt Free Blue Chip":
            presets.debt_free_bluechip(),

        "Turnaround Watch":
            presets.turnaround_watch(),
    }

    print()

    print("=" * 60)

    print("PRESET SCREENER RESULTS")

    print("=" * 60)

    for name, df in screens.items():

        print(
            f"{name:<28}"
            f"{len(df):>6} companies"
        )


if __name__ == "__main__":
    main()

