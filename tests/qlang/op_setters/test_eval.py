
import pandas as pd
import numpy as np

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




def test_eval1():
    code = r'%.eval("x.lower()")'
    result = qr(df, code).result
    expected = get_df()
    expected.columns = expected.columns.astype('string').str.lower()
    assert_frame_equal(result, expected)




def test_eval2():
    code = r'name  %%.eval("str(1)")'
    result = qr(df, code).result
    expected = get_df().loc[:, ['name']]
    index_new = pd.Index([str(1)] * len(expected), dtype='string')
    expected.index = index_new
    assert_frame_equal(result, expected)



def test_eval3():
    code = r"""
    name  %%.eval("str(x).lower()")
    %
    %%
    """
    result = qr(df, code).result
    expected = get_df()
    expected.index = expected.index.astype('string').str.lower()
    assert_frame_equal(result, expected)



def test_eval4():
    code = r"""
    name  %%%.eval("x.lower()")
    %
    %%
    """
    result = qr(df, code).result
    expected = get_df()
    expected['name'] = expected['name'].astype('string').str.lower()
    assert_frame_equal(result, expected)



def test_eval5():
    code = r"""
    name
        %%!:eval("x == x.lower()")
            .eval("x.lower()")
    %
    %%
    """
    result = qr(df, code).result
    expected = get_df()
    expected['name'] = expected['name'].astype('string').str.lower()
    assert_frame_equal(result, expected)



def test_eval6():
    code = r"""
    id
        %%10001
        .eval("str(10001)")
        .tostr
    """
    result = qr(df, code).result
    expected = get_df().loc[[0], ['ID']].astype('object')
    expected.loc[0, 'ID'] = np.nan
    expected.loc[0, 'ID'] = '10001'
    assert_frame_equal(result, expected)



def test_eval7():
    code = r"""
    id  /age
        %%:isnum()
        %%%:all
            .eval("str(0)")
    """
    result = qr(df, code).result
    expected = get_df().loc[:, ['ID', 'age']]
    expected['ID'] = str(0)
    expected['age'] = str(0)
    expected = expected.astype('string')
    assert_frame_equal(result, expected)



def test_eval8():
    code = r"""
    id  /age
        %%:isnum()
            .eval("str(0)")
    """
    result = qr(df, code).result
    expected = get_df().loc[:, ['ID', 'age']]
    expected['ID'] = str(0)
    expected.loc[[0, 1, 2, 4, 8, 10], 'age'] = str(0)
    expected['ID'] = expected['ID'].astype('string')
    assert_frame_equal(result, expected)



def test_eval9():
    code = r"""
    id  /age
        %%:isnum(+allcols)
            .eval("0")
    """
    result = qr(df, code).result
    rows = [0, 1, 2, 4, 8, 10]
    expected = get_df().loc[rows, ['ID', 'age']]
    expected['age'] = expected['age'].astype('object')
    expected.loc[rows, 'ID'] = 0
    expected.loc[rows, 'age'] = 0
    assert_frame_equal(result, expected)



def test_eval_col1():
    code = r"""
    id  .eval('df["name"]')
    %
    """
    result = qr(df, code).result
    expected = get_df()
    expected['ID'] = expected['name']
    assert_frame_equal(result, expected)


def test_eval_col2():
    code = r"""
    id  .eval('df["name"]')
    %
    %%
    """
    result = qr(df, code).result
    expected = get_df()
    expected['ID'] = expected['name']
    assert_frame_equal(result, expected)



def test_eval_col3():
    code = r"""
    id  /age  .eval('df["name"]')
    %
    """
    result = qr(df, code).result
    expected = get_df()
    expected['ID'] = expected['name']
    expected['age'] = expected['name']
    assert_frame_equal(result, expected)



def test_eval_col4():
    code = r"""
    .eval('df["name"]')
    """
    result = qr(df, code).result
    expected = get_df()
    for col in expected.columns:
        expected[col] = expected['name']
    assert_frame_equal(result, expected)



def test_eval_col5():
    code = r"""
    id  /age
        :isnum
        .eval('df["name"]')
    %
    """
    result = qr(df, code).result
    expected = get_df()
    expected['ID'] = expected['name']
    expected.loc[[0, 1, 2, 4, 8, 10], 'age'] = expected['name']
    assert_frame_equal(result, expected)



def test_eval_col6():
    code = r"""
    id  /age
        :isnum +allcols
        .eval('df["name"]')
    %
    """
    result = qr(df, code).result
    expected = get_df().loc[[0, 1, 2, 4, 8, 10], :]
    expected['ID'] = expected['name'].astype('object')
    expected['age'] = expected['name'].astype('object')
    assert_frame_equal(result, expected)



def test_eval_col7():
    code = r"""
    id  /age
        :isnum +allcols
        .eval('df["name"]')
    %
    %%
    """
    result = qr(df, code).result
    expected = get_df()
    rows = [0, 1, 2, 4, 8, 10]
    expected['ID'] = expected['ID'].astype('object')
    expected['age'] = expected['age'].astype('object')
    expected.loc[rows, 'ID'] = expected.loc[rows, 'name'].astype('object')
    expected.loc[rows, 'age'] = expected.loc[rows, 'name'].astype('object')
    assert_frame_equal(result, expected)
