
import pandas as pd

from pandas.testing import (
    assert_frame_equal,
    assert_series_equal,
    )
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



def test_align_cols():
    code = r"""
    %.align(left)
    """
    result = df.dk.qr(code).style_cols
    expected = pd.Series(
        '',
        index=df.columns,
        )
    expected[:] = 'text-align: left;'
    assert_series_equal(result, expected)  # type: ignore



def test_align_rows():
    code = r"""
    %%.align(right)
    """
    result = df.dk.qr(code).style_rows
    expected = pd.Series(
        '',
        index=df.index,
        )
    expected[:] = 'text-align: right;'
    assert_series_equal(result, expected)  # type: ignore



def test_align_vals1():
    code = r"""
    %%%.align(center)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'text-align: center;'
    assert_frame_equal(result, expected)  # type: ignore



def test_align_vals2():
    code = r"""
    .align(start)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'text-align: start;'
    assert_frame_equal(result, expected)  # type: ignore



def test_align_vals3():
    code = r"""
    age  <0  .align(end)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[[0], 'age'] = 'text-align: end;'
    assert_frame_equal(result, expected)  # type: ignore



def test_align_vals4():
    code = r"""
    age  <0  .align(justify)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[[0], 'age'] = 'text-align: justify;'
    assert_frame_equal(result, expected)  # type: ignore
