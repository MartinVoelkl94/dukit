
import pytest
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    )


df = get_df()

def check_message(expected_strings):

    if isinstance(expected_strings, str):
        expected_strings = (expected_strings,)

    logs = log().data  #type: ignore (using no args, log() always returns a styler)
    logs['text_full'] = logs['level'] + ': ' + logs['text']
    text_full = '\n'.join(logs['text_full'].to_list())

    for string in expected_strings:
        error = f'did not find string "{string}" in logs:\n{text_full}'
        assert string in text_full, error



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r'name  = age +colref',
        ['name'],
        df.index,
        [df['age']],
        ['object'],
        None,
    ),
    (
        r'name  = @age',
        ['name'],
        df.index,
        [df['age']],
        ['object'],
        None,
    ),
    (
        r'name  = @age +str',
        ['name'],
        df.index,
        [df['age']],
        ['string'],
        None,
    ),
    (
        r'name  = @age +int',
        ['name'],
        df.index,
        [[
            -25,
            30,
            pd.NA,
            pd.NA,
            40,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            35,
        ]],
        ['Int64'],
        None,
    ),
    (
        r'name  = @weight +int',
        ['name'],
        df.index,
        [[
            70,
            68,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            80,
            pd.NA,
            100,
            -65,
        ]],
        ['Int64'],
        None,
    ),
    (
        r'name  = @age +float',
        ['name'],
        df.index,
        [[
            -25.0,
            30.0,
            pd.NA,
            pd.NA,
            40.0,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            35.0,
        ]],
        ['Float64'],
        None,
    ),
    (
        r'name  = @weight +float',
        ['name'],
        df.index,
        [[
            70.2,
            68.0,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            80.3,
            pd.NA,
            100.0,
            -65.0,
        ]],
        ['Float64'],
        None,
    ),
    (
        r'name  = @age +num',
        ['name'],
        df.index,
        [[
            -25,
            30,
            pd.NA,
            pd.NA,
            40,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            35,
        ]],
        ['Int64'],
        None,
    ),
    (
        r'name  = @weight +num',
        ['name'],
        df.index,
        [[
            70.2,
            68.0,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            80.3,
            pd.NA,
            100.0,
            -65.0,
        ]],
        ['Float64'],
        None,
    ),
    (
        r'name  = @diabetes +bool',
        ['name'],
        df.index,
        [[
            False,
            True,
            pd.NA,
            False,
            True,
            True,
            False,
            pd.NA,
            pd.NA,
            False,
            True,
        ]],
        ['boolean'],
        None,
    ),
    (
        r'name  = @"date of birth" +date',
        ['name'],
        df.index,
        [[
            pd.to_datetime('1995-01-02').date(),
            pd.to_datetime('1990-09-14').date(),
            pd.to_datetime('1985-08-23').date(),
            pd.to_datetime('1980-04-06').date(),
            pd.to_datetime('2007-11-05').date(),
            pd.to_datetime('1983-06-30').date(),
            pd.to_datetime('1975-05-28').date(),
            pd.to_datetime('1960-03-08').date(),
            pd.to_datetime('1955-01-09').date(),
            pd.to_datetime('1950-09-10').date(),
            pd.to_datetime('1945-10-11').date(),
        ]],
        ['datetime64[s]'],
        None,
    ),
    (
        r'name  = @"date of birth" +datetime',
        ['name'],
        df.index,
        [[
            pd.to_datetime('1995-01-02'),
            pd.to_datetime('1990-09-14'),
            pd.to_datetime('1985-08-23'),
            pd.to_datetime('1980-04-06'),
            pd.to_datetime('2007-11-05'),
            pd.to_datetime('1983-06-30'),
            pd.to_datetime('1975-05-28'),
            pd.to_datetime('1960-03-08'),
            pd.to_datetime('1955-01-09'),
            pd.to_datetime('1950-09-10'),
            pd.to_datetime('1945-10-11'),
        ]],
        ['datetime64[us]'],
        None,
    ),


    ])
def test_vals(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result

    expected = pd.DataFrame(index=rows)
    for col, val, dtype in zip(cols, vals, dtypes):
        expected[col] = val
        if dtype:
            expected[col] = expected[col].astype(dtype)
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()

    assert_frame_equal(result, expected)
    if message:
        check_message(message)



def test_vals1():
    code = r"""
    a = @b +colref +date +strict
    """
    df_test = pd.DataFrame({
        'a': ['2020-01-01', '2020-01-02'],
        'b': ['2021-02-01', '2021-02-02'],
        })
    result = df_test.dk.qr(code).result
    vals = [
        pd.to_datetime('2021-02-01').date(),
        pd.to_datetime('2021-02-02').date(),
        ]
    expected = pd.DataFrame({'a': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_vals2():
    code = r"""
    a = @b +colref +datetime +strict
    """
    df_test = pd.DataFrame({
        'a': ['2020-01-01 00:00:00', '2020-01-02 03:04:05'],
        'b': ['2021-02-01 01:02:03', '2021-02-02 04:05:06'],
        })
    result = df_test.dk.qr(code).result
    vals = [
        pd.to_datetime('2021-02-01 01:02:03'),
        pd.to_datetime('2021-02-02 04:05:06'),
        ]
    expected = pd.DataFrame({'a': vals}, dtype='datetime64[us]')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)
