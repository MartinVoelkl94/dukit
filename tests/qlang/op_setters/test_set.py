
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
def test_rows(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()
    expected.index = pd.Series(rows).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #set values
    (
        r'age =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['object'],
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
    %%%:isna  = ""
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



def test_vals2():
    code = r"""
    %age
        %%>30
            %%%:isnum()
                =X
            %%%
    """
    result = df.dk.qr(code).result
    expected = (
        get_df()
        .loc[[4, 10], ['age']]
        .astype(object)
        )
    expected.loc[:, 'age'] = 'X'
    expected['age'] = expected['age'].astype('object')
    assert_frame_equal(result, expected)



def test_vals3():
    code = r"""
    %age
        %%%:isint()
            %%%=X
        %%%
    """
    result = df.dk.qr(code).result
    expected = get_df()[['age']]
    expected.loc[[0, 1, 4, 10], 'age'] = 'X'
    expected['age'] = expected['age'].astype('object')
    assert_frame_equal(result, expected)



def test_vals4():
    code = r"""
    %name /age
        %%!?(Grace, alice, +strict, +allcols, +all)
            %%%?o
            &&&?e
                =X
            %%%
    """
    result = df.dk.qr(code).result
    rows = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]
    expected = get_df().loc[rows, ['name', 'age']]
    expected.loc[[0, 2, 10], 'name'] = 'X'
    expected.loc[5, 'age'] = 'X'
    expected = expected.convert_dtypes()
    assert_frame_equal(result, expected)



def test_vals5():
    code = r"""
    %name /age
        %%!?(Grace, alice, +strict +allcols +all)
            %%%?o
            &&&?e
                =X
            %%%
    """
    result = df.dk.qr(code).result
    rows = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10]
    expected = get_df().loc[rows, ['name', 'age']]
    expected.loc[[0, 2, 10], 'name'] = 'X'
    expected.loc[5, 'age'] = 'X'
    expected = expected.convert_dtypes()
    assert_frame_equal(result, expected)



def test_vals6():
    code = r"""
    name
        %%=="john doe"
            =deleted
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected.loc[[0, 10], 'name'] = 'deleted'
    assert_frame_equal(result, expected)



def test_vals7():
    code = r"""
    name
        %%=="john doe"
    /age
        %%%=deleted
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected.loc[[0, 10], ['name', 'age']] = 'deleted'
    assert_frame_equal(result, expected)



def test_vals8():
    code = r"""
    name
        %%=="john doe"
        %
        =deleted
    /age
        //30
        %
        =deleted
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['ID'] = expected['ID'].astype('object')
    expected.loc[[0, 1, 10], :] = 'deleted'
    assert_frame_equal(result, expected)



def test_vals9():
    code = r"""
    name
        %%=="john doe"
    /age
        //30
        %%%:all
        =deleted
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected.loc[[0, 1, 10], ['name', 'age']] = 'deleted'
    assert_frame_equal(result, expected)
