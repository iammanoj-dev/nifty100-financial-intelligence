from src.analytics.cashflow import (
    free_cash_flow,
    cfo_quality_score,
    capex_intensity,
    fcf_conversion_rate,
    capital_allocation_pattern,
)


def test_free_cash_flow_positive():
    assert free_cash_flow(
        500,
        -200,
    ) == 300


def test_free_cash_flow_negative():
    assert free_cash_flow(
        100,
        -250,
    ) == -150


def test_cfo_quality_high():

    score, label = cfo_quality_score(
        120,
        100,
    )

    assert score == 1.2
    assert label == "High Quality"


def test_cfo_quality_moderate():

    score, label = cfo_quality_score(
        75,
        100,
    )

    assert score == 0.75
    assert label == "Moderate"


def test_cfo_quality_accrual():

    score, label = cfo_quality_score(
        30,
        100,
    )

    assert score == 0.3
    assert label == "Accrual Risk"


def test_cfo_quality_pat_zero():

    score, label = cfo_quality_score(
        100,
        0,
    )

    assert score is None
    assert label is None


def test_capex_intensity():

    value, label = capex_intensity(
        -50,
        1000,
    )

    assert value == 5.0
    assert label == "Moderate"


def test_fcf_conversion():

    assert fcf_conversion_rate(
        300,
        600,
    ) == 50.0


def test_capital_allocation_pattern():

    _, _, _, label = capital_allocation_pattern(
        500,
        -200,
        -100,
        1.2,
    )

    assert label == "Shareholder Returns"


def test_capital_allocation_distress():

    _, _, _, label = capital_allocation_pattern(
        -100,
        50,
        40,
    )

    assert label == "Distress Signal"
