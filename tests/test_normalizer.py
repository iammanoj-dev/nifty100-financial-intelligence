from src.etl.normalizer import (
    normalize_ticker,
    normalize_year,
)

def test_ticker_mixed_case():
    assert normalize_ticker("TcS") == "TCS"


def test_ticker_empty():
    assert normalize_ticker("") == ""


def test_ticker_single_char():
    assert normalize_ticker("a") == "A"


def test_ticker_numeric():
    assert normalize_ticker(123) == "123"


def test_ticker_special_char():
    assert normalize_ticker("tcs.ns") == "TCS.NS"


def test_ticker_long_value():
    assert normalize_ticker("relianceindustries") == "RELIANCEINDUSTRIES"


def test_year_jan20():
    assert normalize_year("Jan-20") == "2020-01"


def test_year_feb21():
    assert normalize_year("Feb-21") == "2021-02"


def test_year_apr23():
    assert normalize_year("Apr-23") == "2023-04"


def test_year_may24():
    assert normalize_year("May-24") == "2024-05"


def test_year_jun25():
    assert normalize_year("Jun-25") == "2025-06"


def test_year_jul26():
    assert normalize_year("Jul-26") == "2026-07"


def test_year_aug27():
    assert normalize_year("Aug-27") == "2027-08"


def test_year_sep28():
    assert normalize_year("Sep-28") == "2028-09"


def test_year_oct29():
    assert normalize_year("Oct-29") == "2029-10"


def test_year_nov30():
    assert normalize_year("Nov-30") == "2030-11"


def test_year_dec31():
    assert normalize_year("Dec-31") == "2031-12"


def test_year_none():
    assert normalize_year(None) is None


def test_year_invalid():
    assert normalize_year("invalid") == "invalid"


def test_year_empty():
    assert normalize_year("") == ""
