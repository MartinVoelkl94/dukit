
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
        %.typeinfo
        """,
        [
            "'ID' [str] 'ID'",
            "'name' [str] 'name'",
            "'date of birth' [str] 'date of birth'",
            "'age' [str] 'age'",
            "'gender' [str] 'gender'",
            "'height' [str] 'height'",
            "'weight' [str] 'weight'",
            "'bp systole' [str] 'bp systole'",
            "'bp diastole' [str] 'bp diastole'",
            "'cholesterol' [str] 'cholesterol'",
            "'diabetes' [str] 'diabetes'",
            "'dose' [str] 'dose'",
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
        %%.typeinfo
        """,
        df.columns,
        [
            '0 [int] 0',
            '1 [int] 1',
            '2 [int] 2',
            '3 [int] 3',
            '4 [int] 4',
            '5 [int] 5',
            '6 [int] 6',
            '7 [int] 7',
            '8 [int] 8',
            '9 [int] 9',
            '10 [int] 10',
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
        age  .typeinfo
        """,
        ['age'],
        df.index,
        [[
            "-25 [int] -25",
            "'30' [int] 30",
            "nan [float] nan",
            "NaT [na] None",
            "'40.0' [float] 40.0",
            "'forty-five' [str] 'forty-five'",
            "'nan' [str] 'nan'",
            "'unk' [str] 'unk'",
            "'' [str] ''",
            "'unknown' [str] 'unknown'",
            "35 [int] 35",
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
