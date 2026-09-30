
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
        r'name  %+=1 +str  %',
        [
            'ID',
            'name1',
            'date of birth',
            'age',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
        ],
        None,
        None,
        ['string'],
        None,
    ),
    (
        r'name  /age  %+=1 +str  %',
        [
            'ID',
            'name1',
            'date of birth',
            'age1',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
        ],
        None,
        None,
        ['string'],
        None,
    ),
    (
        r"""
        name %+=1 +str
        'date of birth' %+=1 +str
        %
        """,
        [
            'ID',
            'name1',
            'date of birth1',
            'age',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
        ],
        None,
        None,
        ['string'],
        None,
    ),
    (
        r'name  %!+=1  %',
        df.columns,
        None,
        None,
        ['object'],
        'ERROR: cannot negate addition of a non-string value',
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

    #set
    (
        r'%%+=1',
        df.columns,
        [
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
            11,
        ],
        None,
        ['Int64'],
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
        r'age  .toint  +=1',
        ['age'],
        df.index,
        [[
            -24,
            31,
            pd.NA,
            pd.NA,
            41,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            36,
        ]],
        ['Int64'],
        None
    ),
    (
        r'age  +=1  +int',
        ['age'],
        df.index,
        [[
            -24,
            31,
            pd.NA,
            pd.NA,
            41,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            36,
        ]],
        ['Int64'],
        None
    ),
    (
        r'age  +=1  +str',
        ['age'],
        df.index,
        [[
            '-251',
            '301',
            pd.NA,
            pd.NA,
            '40.01',
            'forty-five1',
            'nan1',
            'unk1',
            '1',
            'unknown1',
            '351',
        ]],
        ['string'],
        None
    ),
    (
        r'name  +=_',
        ['name'],
        df.index,
        [[
            'John Doe_',
            'Jane Smith_',
            'Alice Johnson_',
            'Bob Brown_',
            'eva white_',
            'Frank miller_',
            'Grace TAYLOR_',
            'Harry Clark_',
            'IVY GREEN_',
            'JAck Williams_',
            'john Doe_',
        ]],
        ['string'],
        None
    ),
    (
        r'name  !+=_',
        ['name'],
        df.index,
        [[
            '_John Doe',
            '_Jane Smith',
            '_Alice Johnson',
            '_Bob Brown',
            '_eva white',
            '_Frank miller',
            '_Grace TAYLOR',
            '_Harry Clark',
            '_IVY GREEN',
            '_JAck Williams',
            '_john Doe',
        ]],
        ['string'],
        None
    ),
    (
        r'height  +=@weight +int',
        ['height'],
        df.index,
        [[
            240,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            pd.NA,
            135,
        ]],
        ['Int64'],
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


