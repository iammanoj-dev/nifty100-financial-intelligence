import pandas as pd


def check_null_pk(df, pk_column):
    return df[df[pk_column].isnull()]


def check_duplicate_pk(df, pk_column):
    return df[df.duplicated(pk_column, keep=False)]


def check_null_fk(df, fk_column):
    return df[df[fk_column].isnull()]


def check_invalid_fk(df, fk_column, valid_values):
    return df[~df[fk_column].isin(valid_values)]


def check_duplicate_company_year(df):
    return df[df.duplicated(["company_id", "year"], keep=False)]


def check_negative_values(df, column):
    return df[df[column] < 0]


def check_opm_high(df):
    return df[df["opm_percentage"] > 100]


def check_opm_low(df):
    return df[df["opm_percentage"] < -100]
