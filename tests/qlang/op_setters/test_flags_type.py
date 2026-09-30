
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

    #type flags
    (
        r'age  =20000101 +str',
        ['age'],
        df.index,
        [['20000101'] * len(df)],
        ['string'],
        None,
    ),
    (
        r'age  =20000101 +int',
        ['age'],
        df.index,
        [[20000101] * len(df)],
        ['Int64'],
        None,
    ),
    (
        r'age  =20000101 +float',
        ['age'],
        df.index,
        [[20000101.0] * len(df)],
        ['Float64'],
        None,
    ),
    (
        r'age  =20000101 +num',
        ['age'],
        df.index,
        [[20000101] * len(df)],
        ['Int64'],
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
