
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
        name  /age  %-=e  %
        """,
        [
            'ID',
            'nam',
            'date of birth',
            'ag',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose'
        ],
        None,
        None,
        ['string'],
        None,
    ),
    (
        r"""
        %-=e  %
        """,
        [
            'ID',
            'nam',
            'date of birth',
            'ag',
            'gender',
            'height',
            'weight',
            'bp systol',
            'bp diastol',
            'cholesterol',
            'diabetes',
            'dos'
        ],
        None,
        None,
        ['string'],
        None,
    ),
    (
        r"""
        name %-=e
        'date of birth' %-=" of birth"
        %
        """,
        [
            'ID',
            'nam',
            'date',
            'age',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose'
        ],
        None,
        None,
        ['string'],
        None,
    ),
    (
        r'name  %!-=1  %',
        df.columns,
        None,
        None,
        ['object'],
        'ERROR: cannot negate substraction of a non-string value',
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
        r'%%-=1',
        df.columns,
        [
            -1,
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
        ],
        None,
        ['Int64'],
        None,
    ),

    ])
def test_rows(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()[cols]
    expected.index = pd.Series(rows).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



@pytest.mark.parametrize('code, col, vals, dtype, message', [

    (
        r'age  .toint  -=1',
        'age',
        [
            -26,
            29,
            pd.NA,
            pd.NA,
            39,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            34,
        ],
        'Int64',
        None
    ),
    (
        r'age  -=1  +int',
        'age',
        [
            -26,
            29,
            pd.NA,
            pd.NA,
            39,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            34,
        ],
        'Int64',
        None
    ),

    (
        r'name  -=Doe',
        'name',
        [
            'John ',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john ',
        ],
        'string',
        None
    ),

    (
        r'name  -=" Doe"',
        'name',
        [
            'John',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john',
        ],
        'string',
        None
    ),

    (
        r'name  !-=John',
        'name',
        [
            ' Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john Doe',
        ],
        'string',
        None
    ),

    (
        r'name  !-=john',
        'name',
        [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            ' Doe',
        ],
        'string',
        None
    ),

    (
        r'name  !-="john "',
        'name',
        [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'Doe',
        ],
        'string',
        None
    ),

    (
        r'height  -=@weight +int',
        'height',
        [
            100,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            265,
        ],
        'Int64',
        None
    ),

    ])
def test_vals(code, col, vals, dtype, message):
    result = df.dk.qr(code).result
    expected = pd.DataFrame({col: vals}, dtype=dtype)
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)
    if message:
        check_message(message)
