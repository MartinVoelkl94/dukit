
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

    #set
    (
        r'%%§0  %%=1  %%',
        df.columns,
        [
            1,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
        ],
        None,
        ['Int64'],
        None,
    ),

    ])
def test_set(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()
    expected.index = pd.Series(rows).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #type conversion
    (
        r'%%.toobj',
        df.columns,
        [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
        ],
        None,
        ['object'],
        None,
    ),
    (
        r'%%.tostr',
        df.columns,
        [
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
        ],
        None,
        ['string'],
        None,
    ),
    (
        r'%%.toint',
        df.columns,
        [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
        ],
        None,
        ['Int64'],
        None,
    ),
    (
        r'%%.tofloat',
        df.columns,
        [
            0,
            1.0,
            2.0,
            3.0,
            4.0,
            5.0,
            6.0,
            7.0,
            8.0,
            9.0,
            10.0,
        ],
        None,
        ['Float64'],
        None,
    ),
    (
        r'%%.tonum',
        df.columns,
        [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
        ],
        None,
        ['Int64'],
        None,
    ),
    (
        r'%%.tobool',
        df.columns,
        [
            False,
            True,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
        ],
        None,
        ['boolean'],
        None,
    ),
    (
        r'%%.todate',
        df.columns,
        [pd.NaT for ind in df.index],
        None,
        ['datetime64[s]'],
        None,
    ),
    (
        r'%%.todatetime',
        df.columns,
        [pd.NaT for ind in df.index],
        None,
        ['datetime64[us]'],
        None,
    ),

    ])
def test_type_conversion(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()
    expected.index = pd.Series(rows).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)
