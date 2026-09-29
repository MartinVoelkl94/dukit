
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

    #colref
    (
        r'name  = age +colref',
        ['name'],
        df.index,
        [df['age']],
        ['object'],
        None,
    ),
    (
        r'name  = @age',
        ['name'],
        df.index,
        [df['age']],
        ['object'],
        None,
    ),

    ])
def test_colref(code, cols, rows, vals, dtypes, message):
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




def test_complex1():
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



def test_complex2():
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



def test_complex3():
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



def test_complex4():
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



def test_complex5():
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



def test_complex6():
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



def test_complex7():
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



def test_complex8():
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



def test_complex9():
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
def test_replace(code, cols, rows, vals, dtypes, message):
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
def test_set(code, cols, rows, vals, dtypes, message):
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




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #type conversion
    (
        r'age  .toobj  =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['object'],
        None,
    ),
    (
        r'age  .tostr  =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['object'],
        None,
    ),
    (
        r'age  .toint  =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['Int64'],
        None,
    ),
    (
        r'age  .tofloat  =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['Float64'],
        None,
    ),
    (
        r'age  .tonum  =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['Int64'],
        None,
    ),
    (
        r'age  .tobool  =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['object'],
        None,
    ),
    (
        r'age  .todate  =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['object'],
        None,
    ),
    (
        r'age  .todatetime  =1',
        ['age'],
        df.index,
        [[1] * len(df)],
        ['object'],
        None,
    ),

    ])
def test_type_conversion(code, cols, rows, vals, dtypes, message):
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




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #type flags
    (
        r'age  =20000101 +str',
        ['age'],
        df.index,
        [['20000101'] * len(df)],
        ['string'],
        None,
    ),
    (
        r'age  =20000101 +int',
        ['age'],
        df.index,
        [[20000101] * len(df)],
        ['Int64'],
        None,
    ),
    (
        r'age  =20000101 +float',
        ['age'],
        df.index,
        [[20000101.0] * len(df)],
        ['Float64'],
        None,
    ),
    (
        r'age  =20000101 +num',
        ['age'],
        df.index,
        [[20000101] * len(df)],
        ['Int64'],
        None,
    ),

    ])
def test_type_flags(code, cols, rows, vals, dtypes, message):
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

