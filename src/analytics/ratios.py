import logging

logger = logging.getLogger(__name__)


def net_profit_margin(
    net_profit,
    sales,
):
    """
    Net Profit Margin (%)

    Formula:
    (Net Profit / Sales) * 100

    Returns None if sales is zero.
    """

    if sales == 0:
        return None

    return (net_profit / sales) * 100


def operating_profit_margin(
    operating_profit,
    sales,
    expected_opm=None,
):
    """
    Operating Profit Margin (%)

    Formula:
    (Operating Profit / Sales) * 100

    If expected_opm is provided, logs a warning if the
    difference is greater than 1%.
    """

    if sales == 0:
        return None

    calculated_opm = (operating_profit / sales) * 100

    if expected_opm is not None:

        difference = abs(
            calculated_opm - expected_opm
        )

        if difference > 1:

            logger.warning(
                "OPM mismatch "
                f"(Calculated={calculated_opm:.2f}, "
                f"Expected={expected_opm:.2f})"
            )

    return calculated_opm


def return_on_equity(
    net_profit,
    equity_capital,
    reserves,
):
    """
    Return on Equity (%)

    Formula:
    Net Profit / (Equity + Reserves) * 100

    Returns None if equity <= 0.
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings,
    broad_sector=None,
):
    """
    Return on Capital Employed (%)

    Formula:
    EBIT / (Equity + Reserves + Borrowings) * 100

    Financial companies use sector-relative benchmarking.
    """

    capital = (
        equity_capital
        + reserves
        + borrowings
    )

    if capital <= 0:
        return None

    roce = (ebit / capital) * 100

    if broad_sector == "Financials":

        logger.info(
            "Financial sector detected. "
            "Use sector-relative ROCE benchmark."
        )

    return roce


def return_on_assets(
    net_profit,
    total_assets,
):
    """
    Return on Assets (%)

    Formula:
    Net Profit / Total Assets * 100

    Returns None if total assets is zero.
    """

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100

def debt_to_equity(
    borrowings,
    equity_capital,
    reserves,
):
    """
    Debt-to-Equity Ratio

    Formula:
    Borrowings / (Equity Capital + Reserves)

    Returns:
        0 if borrowings = 0
        None if equity <= 0
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return borrowings / equity
 
def high_leverage_flag(
    debt_to_equity_ratio,
    broad_sector,
):
    """
    High leverage flag.

    True when:
    D/E > 5
    AND company is not in Financials sector.
    """

    if (
        debt_to_equity_ratio is not None
        and debt_to_equity_ratio > 5
        and broad_sector != "Financials"
    ):
        return True

    return False

def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest,
):
    """
    Interest Coverage Ratio

    Formula:
    (Operating Profit + Other Income) / Interest

    Returns:
        None if interest = 0
    """

    if interest == 0:
        return None

    return (
        operating_profit
        + other_income
    ) / interest


def interest_coverage_label(
    interest,
):
    """
    Returns display label for debt-free companies.
    """

    if interest == 0:
        return "Debt Free"

    return ""

def interest_coverage_warning(
    icr,
):
    """
    Flag companies unable to comfortably
    cover interest payments.

    Warning when ICR < 1.5
    """

    if icr is None:
        return False

    return icr < 1.5

def net_debt(
    borrowings,
    investments,
):
    """
    Net Debt

    Formula:
    Borrowings - Investments

    Investments are treated as
    liquid asset proxy.
    """

    return borrowings - investments
def asset_turnover(
    sales,
    total_assets,
):
    """
    Asset Turnover Ratio

    Formula:
    Sales / Total Assets

    Returns None if total_assets = 0.
    """

    if total_assets == 0:
        return None

    return sales / total_assets
