
import pandas as pd

from pandas.testing import (
    assert_frame_equal,
    assert_series_equal,
    )
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




def test_wrap1():
    code = r"""
    %.wrap(wrap)
    """
    result = qr(df, code).style_cols
    expected = pd.Series(
        '',
        index=df.columns,
        )
    expected[:] = 'text-wrap: wrap;'
    assert_series_equal(result, expected)  # type: ignore



def test_wrap2():
    code = r"""
    %%.wrap(wrap)
    """
    result = qr(df, code).style_rows
    expected = pd.Series(
        '',
        index=df.index,
        )
    expected[:] = 'text-wrap: wrap;'
    assert_series_equal(result, expected)  # type: ignore



def test_wrap3():
    code = r"""
    %%%.wrap(wrap)
    """
    result = qr(df, code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'text-wrap: wrap;'
    assert_frame_equal(result, expected)  # type: ignore



def test_wrap4():
    code = r"""
    .wrap(wrap)
    """
    result = qr(df, code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'text-wrap: wrap;'
    assert_frame_equal(result, expected)  # type: ignore



def test_wrap5():
    code = r"""
    age  <0  .wrap(wrap)
    """
    result = qr(df, code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[[0], 'age'] = 'text-wrap: wrap;'
    assert_frame_equal(result, expected)  # type: ignore




def test_hard1():
    code = r"""
    %.wrap(hard)
    """
    result = qr(df, code).style_cols
    expected = pd.Series(
        '',
        index=df.columns,
        )
    expected[:] = 'word-spacing: 999999999px;'
    assert_series_equal(result, expected)  # type: ignore



def test_hard2():
    code = r"""
    %%.wrap(hard)
    """
    result = qr(df, code).style_rows
    expected = pd.Series(
        '',
        index=df.index,
        )
    expected[:] = 'word-spacing: 999999999px;'
    assert_series_equal(result, expected)  # type: ignore



def test_hard3():
    code = r"""
    %%%.wrap(hard)
    """
    result = qr(df, code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'word-spacing: 999999999px;'
    assert_frame_equal(result, expected)  # type: ignore



def test_hard4():
    code = r"""
    .wrap(hard)
    """
    result = qr(df, code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'word-spacing: 999999999px;'
    assert_frame_equal(result, expected)  # type: ignore



def test_hard5():
    code = r"""
    age  <0  .wrap(hard)
    """
    result = qr(df, code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[[0], 'age'] = 'word-spacing: 999999999px;'
    assert_frame_equal(result, expected)  # type: ignore




def test_pre1():
    code = r"""
    %.wrap(pre)
    """
    result = qr(df, code).style_cols
    expected = pd.Series(
        '',
        index=df.columns,
        )
    expected[:] = 'white-space: pre;'
    assert_series_equal(result, expected)  # type: ignore



def test_pre2():
    code = r"""
    %%.wrap(pre)
    """
    result = qr(df, code).style_rows
    expected = pd.Series(
        '',
        index=df.index,
        )
    expected[:] = 'white-space: pre;'
    assert_series_equal(result, expected)  # type: ignore



def test_pre3():
    code = r"""
    %%%.wrap(pre)
    """
    result = qr(df, code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'white-space: pre;'
    assert_frame_equal(result, expected)  # type: ignore



def test_pre4():
    code = r"""
    .wrap(pre)
    """
    result = qr(df, code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'white-space: pre;'
    assert_frame_equal(result, expected)  # type: ignore



def test_pre5():
    code = r"""
    age  <0  .wrap(pre)
    """
    result = qr(df, code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[[0], 'age'] = 'white-space: pre;'
    assert_frame_equal(result, expected)  # type: ignore
