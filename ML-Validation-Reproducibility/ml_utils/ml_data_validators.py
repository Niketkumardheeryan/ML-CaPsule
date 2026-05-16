import pandas as pd

def check_missing_values(df):
    return df.isnull().sum()

def check_duplicates(df):
    return df.duplicated().sum()

def validate_schema(df):
    return df.dtypes