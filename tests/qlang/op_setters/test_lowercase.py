
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




def test_cols1():
    code = r"""
    ID %.lower()
    """
    result = df.dk.qr(code).result
    vals = df['ID']
    expected = pd.DataFrame({'id': vals}, dtype='Int64')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    expected.columns = expected.columns.astype('string')
    assert_frame_equal(result, expected)



def test_rows1():
    code = r"""
    name  %%.lower()
    """
    result = df.dk.qr(code).result
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



def test_vals1():
    code = r"""
    name  ?doe .lower()
    %%
    """
    result = df.dk.qr(code).result
    expected = df[['name']].copy()
    expected.loc[[0, 10], 'name'] = expected['name'].astype('string').str.lower()
    assert_frame_equal(result, expected)



def test_vals2():
    code = r"""
    name  %%?doe .lower()
    %%
    """
    result = df.dk.qr(code).result
    expected = df[['name']].copy()
    expected.loc[[0, 10], 'name'] = expected['name'].astype('string').str.lower()
    assert_frame_equal(result, expected)



def test_vals3():
    code = r"""
    name  %%?doe .lower()  %%
    """
    result = df.dk.qr(code).result
    expected = df[['name']].copy()
    expected.loc[[0, 10], 'name'] = expected['name'].astype('string').str.lower()
    assert_frame_equal(result, expected)



def test_vals4():
    code = r"""
    name  %%%.lower()
    """
    result = df.dk.qr(code).result
    vals = df['name'].astype('string').str.lower()
    expected = pd.DataFrame({'name': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)



def test_vals5():
    code = r"""
    name  .lower()
    """
    result = df.dk.qr(code).result
    vals = df['name'].astype('string').str.lower()
    expected = pd.DataFrame({'name': vals}, dtype='string')
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()
    assert_frame_equal(result, expected)
