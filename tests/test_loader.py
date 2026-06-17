import pandas as pd

def test_single_column():
    df = pd.DataFrame({"a": [1]})
    assert len(df.columns) == 1


def test_three_columns():
    df = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    assert len(df.columns) == 3


def test_empty_dataframe():
    df = pd.DataFrame()
    assert len(df.columns) == 0


def test_numeric_dataframe():
    df = pd.DataFrame({"a": [1, 2, 3, 4]})
    assert len(df) == 4


def test_string_dataframe():
    df = pd.DataFrame({"a": ["x", "y"]})
    assert len(df) == 2


def test_mixed_dataframe():
    df = pd.DataFrame({"a": [1], "b": ["x"]})
    assert len(df.columns) == 2


def test_large_dataframe():
    df = pd.DataFrame({"a": range(100)})
    assert len(df) == 100


def test_zero_rows():
    df = pd.DataFrame({"a": []})
    assert len(df) == 0


def test_boolean_dataframe():
    df = pd.DataFrame({"a": [True, False]})
    assert len(df) == 2


def test_float_dataframe():
    df = pd.DataFrame({"a": [1.1, 2.2]})
    assert len(df) == 2
