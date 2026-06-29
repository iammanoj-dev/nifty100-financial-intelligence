from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    return_on_assets,
    debt_to_equity,
    high_leverage_flag,
    interest_coverage_ratio,
    interest_coverage_label,
    interest_coverage_warning,
    net_debt,
    asset_turnover,
)

def test_net_profit_margin_normal():
    assert net_profit_margin(
        200,
        1000,
    ) == 20.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(
        100,
        0,
    ) is None


def test_operating_profit_margin_normal():
    assert operating_profit_margin(
        250,
        1000,
    ) == 25.0


def test_operating_profit_margin_crosscheck():
    result = operating_profit_margin(
        250,
        1000,
        expected_opm=25,
    )

    assert result == 25.0


def test_return_on_equity_normal():
    assert return_on_equity(
        100,
        200,
        300,
    ) == 20.0


def test_return_on_equity_negative():
    assert return_on_equity(
        100,
        -200,
        100,
    ) is None


def test_return_on_capital_employed():
    assert return_on_capital_employed(
        200,
        400,
        300,
        300,
    ) == 20.0


def test_return_on_assets():
    assert return_on_assets(
        100,
        500,
    ) == 20.0

def test_debt_to_equity():
    assert debt_to_equity(
        200,
        100,
        100,
    ) == 1.0


def test_debt_to_equity_debt_free():
    assert debt_to_equity(
        0,
        100,
        100,
    ) == 0


def test_high_leverage_flag():
    assert high_leverage_flag(
        6.5,
        "Industrials",
    ) is True


def test_high_leverage_financial():
    assert high_leverage_flag(
        8.0,
        "Financials",
    ) is False

def test_interest_coverage_ratio():
    assert interest_coverage_ratio(
        200,
        50,
        50,
    ) == 5.0


def test_interest_coverage_zero_interest():
    assert interest_coverage_ratio(
        200,
        50,
        0,
    ) is None


def test_interest_coverage_label():
    assert interest_coverage_label(
        0,
    ) == "Debt Free"


def test_interest_coverage_warning():
    assert interest_coverage_warning(
        1.2,
    ) is True

def test_net_debt():
    assert net_debt(
        500,
        200,
    ) == 300


def test_asset_turnover():
    assert asset_turnover(
        1000,
        500,
    ) == 2.0


def test_asset_turnover_zero_assets():
    assert asset_turnover(
        1000,
        0,
    ) is None


def test_interest_coverage_warning_safe():
    assert interest_coverage_warning(
        3.0,
    ) is False
