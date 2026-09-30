
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

    #colref
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
