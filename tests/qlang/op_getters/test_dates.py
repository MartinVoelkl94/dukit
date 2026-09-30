
import pytest

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
        r'"date of birth"  %%1995.01.02',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%==1995.01.02',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%==1995_01_02',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="1995-01-02"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="1995/01/02"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="1995 01 02"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="1995-Jan-02"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="02-01-1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="02-Jan-1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="Jan-02-1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="02-01.1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="02 Jan-1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="Jan/02_1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"   .todatetime()   %%==1995-01-02',
        ['date of birth'],
        [0],
        None,
        ['datetime64[us]'],
        None,
    ),
    (
        r'"date of birth"   .todatetime   %%<1950.01.01',
        ['date of birth'],
        [10],
        None,
        ['datetime64[us]'],
        None,
    ),
    (
        r'"date of birth"   %%%.todatetime()   %%>"1990/01/01"   &&<"2000-01-01"',
        ['date of birth'],
        [0, 1],
        None,
        ['datetime64[us]'],
        None,
    ),

    ])
def test_rows(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r'"date of birth"  %%%1995.01.02  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%==1995.01.02  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%==1995_01_02  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="1995-01-02"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="1995/01/02"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="1995 01 02"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="1995-Jan-02"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="02-01-1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="02-Jan-1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="Jan-02-1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="02-01.1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="02 Jan-1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="Jan/02_1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"   .todatetime()   %%%==1995-01-02  %%:trim',
        ['date of birth'],
        [0],
        None,
        ['datetime64[us]'],
        None,
    ),
    (
        r'"date of birth"   .todatetime   %%%<1950.01.01  %%:trim',
        ['date of birth'],
        [10],
        None,
        ['datetime64[us]'],
        None,
    ),
    (
        r'"date of birth"   .todatetime   %%%>"1990/01/01"   &&&<"2000-01-01"  %%:trim',
        ['date of birth'],
        [0, 1],
        None,
        ['datetime64[us]'],
        None,
    ),

    ])
def test_vals(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if vals:
        for col, val in zip(cols, vals):
            expected[col] = val
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)
