import pandas as pd

from schema_validator import SchemaValidator
from validation_report import save_validation_report


def main():

    validator = SchemaValidator()

    companies = pd.read_excel(
        "data/raw/companies.xlsx",
        header=1,
    )

    profit_loss = pd.read_excel(
        "data/raw/profitandloss.xlsx",
        header=1,
    )

    balance_sheet = pd.read_excel(
        "data/raw/balancesheet.xlsx",
        header=1,
    )

    cash_flow = pd.read_excel(
        "data/raw/cashflow.xlsx",
        header=1,
    )

    validator.validate_null_pk(
        companies,
        "companies",
    )

    validator.validate_duplicate_pk(
        companies,
        "companies",
    )

    validator.validate_null_company_id(
        profit_loss,
        "profitandloss",
    )

    validator.validate_null_year(
        profit_loss,
        "profitandloss",
    )

    validator.validate_duplicate_company_year(
        profit_loss,
        "profitandloss",
    )

    validator.validate_negative_sales(
        profit_loss,
    )

    validator.validate_negative_profit(
        profit_loss,
    )

    validator.validate_opm_high(
        profit_loss,
    )

    validator.validate_opm_low(
        profit_loss,
    )

    validator.validate_negative_assets(
        balance_sheet,
    )

    validator.validate_negative_liabilities(
        balance_sheet,
    )

    validator.validate_missing_cashflow(
        cash_flow,
    )

    failures = validator.get_failures()

    save_validation_report(
        failures,
    )

    print(
        f"Validation completed. "
        f"Failures found: {len(failures)}"
    )


if __name__ == "__main__":
    main()
