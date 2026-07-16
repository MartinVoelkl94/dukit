
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    qr,
    )



params = []
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




def test_lower1():
    code = r"""
    ID %.lower()
    """
    result = qr(df, code).result
    vals = df['ID']
    expected = pd.DataFrame({'id': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_lower2():
    code = r"""
    name  %%.lower()
    """
    result = qr(df, code).result
    expected = df[['name']]
    expected.index = (
        df
        .index
        .astype(str)
        .str
        .lower()
        .astype('string')
        )
    assert_frame_equal(result, expected)



def test_lower3():
    code = r"""
    name  ?doe .lower()
    %%
    """
    result = qr(df, code).result
    expected = df[['name']].copy()
    expected.loc[[0, 10], 'name'] = expected['name'].astype('string').str.lower()
    assert_frame_equal(result, expected)



def test_lower4():
    code = r"""
    name  %%?doe .lower()
    %%
    """
    result = qr(df, code).result
    expected = df[['name']].copy()
    expected.loc[[0, 10], 'name'] = expected['name'].astype('string').str.lower()
    assert_frame_equal(result, expected)



def test_lower5():
    code = r"""
    name  %%?doe .lower()  %%
    """
    result = qr(df, code).result
    expected = df[['name']].copy()
    expected.loc[[0, 10], 'name'] = expected['name'].astype('string').str.lower()
    assert_frame_equal(result, expected)



def test_lower6():
    code = r"""
    name  %%%.lower()
    """
    result = qr(df, code).result
    vals = df['name'].astype('string').str.lower()
    expected = pd.DataFrame({'name': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_lower7():
    code = r"""
    name  .lower()
    """
    result = qr(df, code).result
    vals = df['name'].astype('string').str.lower()
    expected = pd.DataFrame({'name': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)




def test_upper1():
    code = r"""
    name %.upper()
    """
    result = qr(df, code).result
    vals = df['name']
    expected = pd.DataFrame({'NAME': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_upper2():
    code = r"""
    name  %%.upper()
    """
    result = qr(df, code).result
    expected = df[['name']]
    expected.index = (
        df
        .index
        .astype('string')
        .str
        .upper()
        )
    assert_frame_equal(result, expected)



def test_upper3():
    code = r"""
    name  ?doe .upper()
    %%
    """
    result = qr(df, code).result
    expected = df[['name']].copy()
    expected.loc[[0, 10], 'name'] = expected['name'].str.upper()
    assert_frame_equal(result, expected)



def test_upper4():
    code = r"""
    name  %%?doe .upper()
    %%
    """
    result = qr(df, code).result
    expected = df[['name']].copy()
    expected.loc[[0, 10], 'name'] = expected['name'].str.upper()
    assert_frame_equal(result, expected)



def test_upper5():
    code = r"""
    name  %%?doe .upper()  %%
    """
    result = qr(df, code).result
    expected = df[['name']].copy()
    expected.loc[[0, 10], 'name'] = expected['name'].str.upper()
    assert_frame_equal(result, expected)



def test_upper6():
    code = r"""
    name  %%%.upper()
    """
    result = qr(df, code).result
    vals = df['name'].str.upper()
    expected = pd.DataFrame({'name': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_upper7():
    code = r"""
    name  .upper()
    """
    result = qr(df, code).result
    vals = df['name'].str.upper()
    expected = pd.DataFrame({'name': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)
