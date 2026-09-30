
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
        r'ID  %.lower()  %',
        [
            'id',
            'name',
            'date of birth',
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
        r'name  %%.lower()  %',
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

    ])
def test_rows(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()[cols]
    expected.index = pd.Series(rows).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r'name  ?doe .lower()  %%',
        ['name'],
        df.index,
        [[
            'john doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john doe',
        ]],
        ['string'],
        None
    ),
    (
        r'name  %%?doe .lower()  %%',
        ['name'],
        df.index,
        [[
            'john doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john doe',
        ]],
        ['string'],
        None
    ),
    (
        r'name  %%%.lower()',
        ['name'],
        df.index,
        [[
            'john doe',
            'jane smith',
            'alice johnson',
            'bob brown',
            'eva white',
            'frank miller',
            'grace taylor',
            'harry clark',
            'ivy green',
            'jack williams',
            'john doe',
        ]],
        ['string'],
        None
    ),
    (
        r'name  .lower()',
        ['name'],
        df.index,
        [[
            'john doe',
            'jane smith',
            'alice johnson',
            'bob brown',
            'eva white',
            'frank miller',
            'grace taylor',
            'harry clark',
            'ivy green',
            'jack williams',
            'john doe',
        ]],
        ['string'],
        None
    ),

    ])
def test_vals(code, cols, rows, vals, dtypes, message):

    result = df.dk.qr(code).result
    expected = pd.DataFrame(index=rows)
    for col, val, dtype in zip(cols, vals, dtypes):
        expected[col] = pd.Series(val, index=rows).astype(dtype)
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()

    assert_frame_equal(result, expected)
    if message:
        check_message(message)
