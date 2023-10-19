import pytest
import pandas as pd
import datatest as dt


pytestmark = pytest.mark.filterwarnings('ignore:subset and superset warning')


def is_not_null(x):
    return x is not None


@pytest.fixture(scope='module')
@dt.working_directory(__file__)
def df():
    return pd.read_csv('step_4.csv')
    # return pd.read_parquet('step_4.parquet.gzip')


@pytest.mark.mandatory
def test_columns(df):
    dt.validate(
        df.columns,
        {"geographical_feature", "age", "counts"},
    )


@pytest.mark.mandatory
def test_count(df):
    dt.validate(
        len(df), 15,)


def test_geographical_feature(df):
    dt.validate.subset(df["geographical_feature"], {"water", "relief", "flat"})


def test_age(df):
    dt.validate(df["age"], is_not_null)
    dt.validate(df["age"], int)


def test_counts(df):
    dt.validate(df["counts"], is_not_null)
    dt.validate(df["counts"], int)
