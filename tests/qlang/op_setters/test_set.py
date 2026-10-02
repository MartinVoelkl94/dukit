
import pytest
import numpy as np
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
        name  %=full_name  %
        """,
        [
            'ID',
            'full_name',
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
        r"""
        name  /age  %=renamed  %
        """,
        [
            'ID',
            'renamed',
            'date of birth',
            'renamed',
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
        name %=full_name
        'date of birth' %=dob
        %
        """,
        [
            'ID',
            'full_name',
            'dob',
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
def test_rows(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()
    expected.index = pd.Series(rows).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r'age =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['object'],
        None,
    ),
    (
        r"""
        age
            %%>30
                %%%:isnum()
                    =X
                %%%
        %%
        """,
        ['age'],
        df.index,
        [[
            -25,
            '30',
            np.nan,
            pd.NaT,
            'X',
            'forty-five',
            'nan',
            'unk',
            '',
            'unknown',
            'X',
        ]],
        ['object'],
        None,
    ),
    (
        r"""
        age
            %%%:isint()
                %%%=X
            %%%
        %%
        """,
        ['age'],
        df.index,
        [[
            'X',
            'X',
            np.nan,
            pd.NaT,
            'X',
            'forty-five',
            'nan',
            'unk',
            '',
            'unknown',
            'X',
        ]],
        ['object'],
        None,
    ),
    (
        r"""
        name /age
            %%!?(Grace, alice, +strict, +allcols, +all)
                %%%?o
                &&&?e
                    =X
                %%%
        %%
        """,
        ['name', 'age'],
        df.index,
        [[
            'X',
            'Jane Smith',
            'X',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'X',
            ],
            [
            -25,
            '30',
            np.nan,
            pd.NaT,
            '40.0',
            'X',
            'nan',
            'unk',
            '',
            'unknown',
            35,
        ]],
        ['string', 'object'],
        None,
    ),
    (
        r"""
        name
            %%=="john doe"
                =deleted
        %%
        """,
        ['name', 'age'],
        df.index,
        [[
            'deleted',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'deleted',
        ]],
        ['string', 'object'],
        None,
    ),
    (
        r"""
        name
            %%=="john doe"
                =deleted
        /age
            %%%=deleted
        %%
        """,
        ['name', 'age'],
        df.index,
        [[
            'deleted',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'deleted',
            ],
            [
            'deleted',
            '30',
            np.nan,
            pd.NaT,
            '40.0',
            'forty-five',
            'nan',
            'unk',
            '',
            'unknown',
            'deleted',
        ]],
        ['string', 'object'],
        None,
    ),
    (
        r"""
        name
            %%=="john doe"
        /age
            //30
            %%%:all
            =deleted
        %%
        """,
        ['name', 'age'],
        df.index,
        [[
            'deleted',
            'deleted',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'deleted',
            ],
            [
            'deleted',
            'deleted',
            np.nan,
            pd.NaT,
            '40.0',
            'forty-five',
            'nan',
            'unk',
            '',
            'unknown',
            'deleted',
        ]],
        ['string', 'object'],
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



def test_vals1():
    code = r"""
    %%%:isna  = none
    %%%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    cols = [
        'age',
        'gender',
        'height',
        'weight',
        'bp systole',
        'bp diastole',
        'cholesterol',
        'diabetes',
        'dose',
        ]
    expected[cols] = expected[cols]
    expected['gender'] = expected['gender'].astype('object')
    expected['cholesterol'] = expected['cholesterol'].astype('object')
    expected['dose'] = expected['dose'].astype('object')
    expected.loc[[2, 3, 6, 8], 'age'] = None
    expected.loc[[7, 8], 'gender'] = None
    expected.loc[[2, 4, 9], 'height'] = None
    expected.loc[[3, 4, 6], 'weight'] = None
    expected.loc[[2, 6, 8], 'bp systole'] = None
    expected.loc[[2, 4, 6, 7, 10], 'bp diastole'] = None
    expected.loc[[2, 4, 7, 9], 'cholesterol'] = None
    expected.loc[[2, 7, 8], 'diabetes'] = None
    expected.loc[[1, 6, 7], 'dose'] = None
    assert_frame_equal(result, expected)
