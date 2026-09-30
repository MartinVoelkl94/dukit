
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
        r'id  == @ID',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'id  == @id',
        ['ID'],
        [],
        None,
        None,
        None,
    ),
    (
        r'age   == @"bp systole"',
        ['age'],
        [8],
        None,
        None,
        None,
    ),
    (
        r"""
        age  /height  .tonum
        age  < height +colref
        """,
        ['age'],
        [0, 10],
        None,
        ['Int64'],
        None,
    ),
    (
        r"""
        age  /height  .tonum
        age  < @height
        """,
        ['age'],
        [0, 10],
        None,
        ['Int64'],
        None,
    ),
    (
        r"""
        age  /height  .tonum
        height  > @age
        """,
        ['height'],
        [0, 10],
        None,
        ['Int64'],
        None,
    ),
    (
        r"""
        age  /height  .tonum
        age  <= @height
        """,
        ['age'],
        [0, 10],
        None,
        ['Int64'],
        None,
    ),
    (
        r"""
        age  /height  .tonum
        height  >= @age
        """,
        ['height'],
        [0, 10],
        None,
        ['Int64'],
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
