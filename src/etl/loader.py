from pathlib import Path
import pandas as pd


def load_excel(path, header=1):
    """
    Load Excel dataset.
    """

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"{path} not found")

    return pd.read_excel(path, header=header)


def get_row_count(df):
    return len(df)


def get_column_count(df):
    return len(df.columns)
