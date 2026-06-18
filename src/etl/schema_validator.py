import pandas as pd


class SchemaValidator:

    def __init__(self):
        self.failures = []

    def add_failure(
        self,
        rule_id,
        severity,
        table_name,
        column_name,
        message,
        row_count,
    ):
        self.failures.append(
            {
                "rule_id": rule_id,
                "severity": severity,
                "table_name": table_name,
                "column_name": column_name,
                "message": message,
                "row_count": row_count,
            }
        )

    def get_failures(self):
        return pd.DataFrame(self.failures)

    # DQ-01
    def validate_null_pk(self, df, table_name, pk_column="id"):
        failures = df[df[pk_column].isnull()]
        if len(failures):
            self.add_failure(
                "DQ-01",
                "CRITICAL",
                table_name,
                pk_column,
                "Null Primary Key",
                len(failures),
            )

    # DQ-02
    def validate_duplicate_pk(self, df, table_name, pk_column="id"):
        failures = df[df.duplicated(pk_column)]
        if len(failures):
            self.add_failure(
                "DQ-02",
                "CRITICAL",
                table_name,
                pk_column,
                "Duplicate Primary Key",
                len(failures),
            )

    # DQ-03
    def validate_null_company_id(self, df, table_name):
        failures = df[df["company_id"].isnull()]
        if len(failures):
            self.add_failure(
                "DQ-03",
                "CRITICAL",
                table_name,
                "company_id",
                "Null Company ID",
                len(failures),
            )

    # DQ-04
    def validate_foreign_key(
        self,
        df,
        table_name,
        valid_company_ids,
    ):
        failures = df[
            ~df["company_id"].isin(valid_company_ids)
        ]

        if len(failures):
            self.add_failure(
                "DQ-04",
                "CRITICAL",
                table_name,
                "company_id",
                "Invalid Foreign Key",
                len(failures),
            )

    # DQ-05
    def validate_null_year(self, df, table_name):
        failures = df[df["year"].isnull()]
        if len(failures):
            self.add_failure(
                "DQ-05",
                "CRITICAL",
                table_name,
                "year",
                "Null Year",
                len(failures),
            )

    # DQ-06
    def validate_duplicate_company_year(
        self,
        df,
        table_name,
    ):
        failures = df[
            df.duplicated(
                ["company_id", "year"],
                keep=False,
            )
        ]

        if len(failures):
            self.add_failure(
                "DQ-06",
                "CRITICAL",
                table_name,
                "company_id,year",
                "Duplicate Company-Year",
                len(failures),
            )

    # DQ-07
    def validate_negative_assets(self, df):
        failures = df[df["total_assets"] < 0]

        if len(failures):
            self.add_failure(
                "DQ-07",
                "CRITICAL",
                "balancesheet",
                "total_assets",
                "Negative Total Assets",
                len(failures),
            )

    # DQ-08
    def validate_negative_liabilities(self, df):
        failures = df[df["total_liabilities"] < 0]

        if len(failures):
            self.add_failure(
                "DQ-08",
                "CRITICAL",
                "balancesheet",
                "total_liabilities",
                "Negative Total Liabilities",
                len(failures),
            )

    # DQ-09
    def validate_negative_sales(self, df):
        failures = df[df["sales"] < 0]

        if len(failures):
            self.add_failure(
                "DQ-09",
                "WARNING",
                "profitandloss",
                "sales",
                "Negative Sales",
                len(failures),
            )

    # DQ-10
    def validate_negative_profit(self, df):
        failures = df[df["net_profit"] < 0]

        if len(failures):
            self.add_failure(
                "DQ-10",
                "WARNING",
                "profitandloss",
                "net_profit",
                "Negative Net Profit",
                len(failures),
            )

    # DQ-11
    def validate_opm_high(self, df):
        failures = df[df["opm_percentage"] > 100]

        if len(failures):
            self.add_failure(
                "DQ-11",
                "WARNING",
                "profitandloss",
                "opm_percentage",
                "OPM Greater Than 100",
                len(failures),
            )

    # DQ-12
    def validate_opm_low(self, df):
        failures = df[df["opm_percentage"] < -100]

        if len(failures):
            self.add_failure(
                "DQ-12",
                "WARNING",
                "profitandloss",
                "opm_percentage",
                "OPM Less Than -100",
                len(failures),
            )

    # DQ-13
    def validate_roce_high(self, df):
        failures = df[df["roce_percentage"] > 100]

        if len(failures):
            self.add_failure(
                "DQ-13",
                "WARNING",
                "companies",
                "roce_percentage",
                "ROCE Greater Than 100",
                len(failures),
            )

    # DQ-14
    def validate_roe_high(self, df):
        failures = df[df["roe_percentage"] > 100]

        if len(failures):
            self.add_failure(
                "DQ-14",
                "WARNING",
                "companies",
                "roe_percentage",
                "ROE Greater Than 100",
                len(failures),
            )

    # DQ-15
    def validate_missing_cashflow(self, df):
        failures = df[df["net_cash_flow"].isnull()]

        if len(failures):
            self.add_failure(
                "DQ-15",
                "WARNING",
                "cashflow",
                "net_cash_flow",
                "Missing Cash Flow",
                len(failures),
            )

    # DQ-16
    def validate_extreme_cashflow(
        self,
        df,
        threshold=100000,
    ):
        failures = df[
            abs(df["net_cash_flow"]) > threshold
        ]

        if len(failures):
            self.add_failure(
                "DQ-16",
                "WARNING",
                "cashflow",
                "net_cash_flow",
                "Extreme Cash Flow",
                len(failures),
            )
