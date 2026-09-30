
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
        r"""
        %.typeinfo +strict
        """,
        [
            "'ID' [str]",
            "'name' [str]",
            "'date of birth' [str]",
            "'age' [str]",
            "'gender' [str]",
            "'height' [str]",
            "'weight' [str]",
            "'bp systole' [str]",
            "'bp diastole' [str]",
            "'cholesterol' [str]",
            "'diabetes' [str]",
            "'dose' [str]",
        ],
        None,
        None,
        ['string'],
        None,
    ),

    ])
def test_cols(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()
    expected.columns = pd.Series(cols).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r"""
        %%.typeinfo +strict
        """,
        df.columns,
        [
            '0 [int]',
            '1 [int]',
            '2 [int]',
            '3 [int]',
            '4 [int]',
            '5 [int]',
            '6 [int]',
            '7 [int]',
            '8 [int]',
            '9 [int]',
            '10 [int]',
        ],
        None,
        ['string'],
        None,
    ),

    ])
def test_rows(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()
    expected.index = pd.Series(rows).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r"""
        age  .typeinfo +strict
        """,
        ['age'],
        df.index,
        [[
            "-25 [int]",
            "'30' [str]",
            "nan [float]",
            "NaT [NaTType]",
            "'40.0' [str]",
            "'forty-five' [str]",
            "'nan' [str]",
            "'unk' [str]",
            "'' [str]",
            "'unknown' [str]",
            "35 [int]",
        ]],
        ['string'],
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
