
import datetime
import numpy as np
import pandas as pd
import dukit as dk

from pandas.testing import assert_frame_equal
from dukit import date_delta, log


def check_message(expected_strings):

    if isinstance(expected_strings, str):
        expected_strings = (expected_strings,)

    logs = log().data  #type: ignore (using no args, log() always returns a styler)
    logs['text_full'] = logs['level'] + ': ' + logs['text']
    text_full = '\n'.join(logs['text_full'].to_list())

    for string in expected_strings:
        error = f'did not find string "{string}" in logs:\n{text_full}'
        assert string in text_full, error


def get_df():

    df = pd.DataFrame()
    df['date0'] = [
        '2023-01-01',
        '2023-09-07',
        '2024-12-03',
        ]
    df['date1'] = [
        '2024-01-01',
        '2024-02-01',
        None,
        ]
    df['date2'] = [
        '2024-01-05',
        '2024-02-10',
        '2024-03-15',
        ]
    df['date3'] = [
        'nan',
        'na',
        np.nan,
        ]
    df['date4'] = [
        pd.NaT,
        pd.NA,
        pd.Timestamp('2024-04-01'),
        ]
    df['date5'] = [
        datetime.datetime(2024, 5, 1),
        pd.Timestamp('2024-06-01'),
        datetime.datetime(2024, 7, 1),
        ]

    return df



def test_col():

    result = date_delta(
        get_df(),
        reference_col='date1',
        ).iloc[:, 6:].astype(object)

    expected = pd.DataFrame()
    expected['reference_date'] = [
        dk.date('2024-01-01'),
        dk.date('2024-02-01'),
        pd.NaT,
        ]
    expected['days from\ndate1\nto\ndate0'] = [
        -365,
        -147,
        np.nan,
        ]
    expected['days from\ndate1\nto\ndate2'] = [
        4,
        9,
        np.nan,
        ]
    expected['days from\ndate1\nto\ndate4'] = [
        np.nan,
        np.nan,
        np.nan,
        ]
    expected['days from\ndate1\nto\ndate5'] = [
        121,
        121,
        np.nan,
        ]
    expected = expected.astype(object)

    assert_frame_equal(result, expected)



def test_date():

    result = date_delta(
        get_df(),
        reference_date='2024-01-01',
        ).iloc[:, 6:].astype(object)

    expected = pd.DataFrame()
    expected['reference_date'] = [
        dk.date('2024-01-01'),
        dk.date('2024-01-01'),
        dk.date('2024-01-01'),
        ]
    expected['days from\n2024-01-01\nto\ndate0'] = [
        -365,
        -116,
        337,
        ]
    expected['days from\n2024-01-01\nto\ndate1'] = [
        0,
        31,
        np.nan,
        ]
    expected['days from\n2024-01-01\nto\ndate2'] = [
        4,
        40,
        74,
        ]
    expected['days from\n2024-01-01\nto\ndate4'] = [
        np.nan,
        np.nan,
        91,
        ]
    expected['days from\n2024-01-01\nto\ndate5'] = [
        121,
        152,
        182,
        ]
    expected = expected.astype(object)

    assert_frame_equal(result, expected)



def test_logging():
    log(clear=True)

    result = date_delta(
        get_df(),
        )
    expected = get_df()
    assert result.equals(expected), dk.diff(result, expected)
    check_message('ERROR: no reference date or column provided')

    result = date_delta(
        get_df(),
        reference_col='date1',
        reference_date='date1',
        )
    expected = get_df()
    assert result.equals(expected), dk.diff(result, expected)
    check_message('ERROR: both reference date and column provided')


    df = get_df()
    df['reference_date'] = [0, 0, 0]
    df['days from\ndate1\nto\ndate0'] = [0, 0, 0]

    result = date_delta(
        df.copy(),
        reference_col='date1',
        ).iloc[:, 6:].astype(object)

    expected = pd.DataFrame()
    expected['reference_date'] = [
        dk.date('2024-01-01'),
        dk.date('2024-02-01'),
        pd.NaT,
        ]
    expected['days from\ndate1\nto\ndate0'] = [
        -365,
        -147,
        np.nan,
        ]
    expected['days from\ndate1\nto\ndate2'] = [
        4,
        9,
        np.nan,
        ]
    expected['days from\ndate1\nto\ndate4'] = [
        np.nan,
        np.nan,
        np.nan,
        ]
    expected['days from\ndate1\nto\ndate5'] = [
        121,
        121,
        np.nan,
        ]
    expected = expected.astype(object)

    assert result.equals(expected), dk.diff(result, expected)
    check_message('WARNING: column "reference_date" already exists, overwriting')
    check_message(
        'WARNING: column "days from\ndate1\nto\ndate0" already exists, overwriting'
        )
