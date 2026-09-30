
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
        %.replace(i, I)
        """,
        [
            'ID',
            'name',
            'date of bIrth',
            'age',
            'gender',
            'heIght',
            'weIght',
            'bp systole',
            'bp dIastole',
            'cholesterol',
            'dIabetes',
            'dose'
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
        %%.replace(0, x)
        """,
        df.columns,
        [
            'x',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '1x',
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

    #replace
    (
        r'name  .replace(John, JOHN)',
        ['name'],
        df.index,
        [[
            'JOHN Doe',
            'Jane Smith',
            'Alice JOHNson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john Doe',
        ]],
        ['string'],
        None,
    ),
    (
        r'name  ?doe  .replace(John, JOHN)  %%',
        ['name'],
        df.index,
        [[
            'JOHN Doe',
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
