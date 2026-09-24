
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




def test_basic():
    code = r"""
    age  =1
    """
    result = df.dk.qr(code).result
    vals = [1] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_flag_str():
    code = r"""
    age  =20000101 +str
    """
    result = df.dk.qr(code).result
    vals = ['20000101'] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_flag_int():
    code = r"""
    age  =20000101 +int
    """
    result = df.dk.qr(code).result
    vals = [20000101] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_flag_float():
    code = r"""
    age  =20000101 +float
    """
    result = df.dk.qr(code).result
    vals = [20000101.0] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='Float64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_flag_num():
    code = r"""
    age  =20000101 +num
    """
    result = df.dk.qr(code).result
    vals = [20000101] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_tostr():
    code = r"""
    age  .tostr  =1
    """
    result = df.dk.qr(code).result
    vals = [1] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_toint():
    code = r"""
    age  .toint  =1
    """
    result = df.dk.qr(code).result
    vals = [1] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_tofloat():
    code = r"""
    age  .tofloat  =1
    """
    result = df.dk.qr(code).result
    vals = [1] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='Float64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_tonum():
    code = r"""
    age  .tonum  =1
    """
    result = df.dk.qr(code).result
    vals = [1] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_tobool():
    code = r"""
    age  .tobool  =1
    """
    result = df.dk.qr(code).result
    vals = [1] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_todate():
    code = r"""
    age  .todate  =1
    """
    result = df.dk.qr(code).result
    vals = [1] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_todatetime():
    code = r"""
    age  .todatetime  =1
    """
    result = df.dk.qr(code).result
    vals = [1] * len(df)
    expected = pd.DataFrame({'age': vals}, dtype='object')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




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
