import pytest
import pandas as pd
import datatest as dt


pytestmark = pytest.mark.filterwarnings('ignore:subset and superset warning')


def is_not_null(x):
    return x is not None


@pytest.fixture(scope='module')
@dt.working_directory(__file__)
def df():
    return pd.read_csv('step_2.csv')
    # return pd.read_parquet('step_2.parquet.gzip')


@pytest.mark.mandatory
def test_columns(df):
    dt.validate(
        df.columns,
        {"age", "address", "job", "marital", "education", "default", "balance", "housing", "loan", "contact",
         "duration", "campaign", "pdays", "previous", "poutcome", "outcome", "first_name", "second_name",
         "date", "geographical_feature"},
    )


@pytest.mark.mandatory
def test_count(df):
    dt.validate(
        len(df), 816,)


def test_geographical_feature(df):
    dt.validate.subset(df["geographical_feature"], {"unknown", "water", "relief", "flat"})


def test_pdays(df):
    dt.validate.interval(df["pdays"], min=0)


def test_first_name(df):
    dt.validate(df["first_name"], is_not_null)


def test_second_name(df):
    dt.validate(df["second_name"], is_not_null)


def test_age(df):
    dt.validate.interval(df["age"], min=0, max=10)


def test_date(df):
    dt.validate.regex(df["date"], r'^\d\d/\d\d$')


def test_default(df):
    dt.validate.subset(df["default"], {True, False})


def test_housing(df):
    dt.validate.subset(df["housing"], {True, False})


def test_loan(df):
    dt.validate.subset(df["loan"], {True, False})


def test_outcome(df):
    dt.validate.subset(df["outcome"], {True, False})
