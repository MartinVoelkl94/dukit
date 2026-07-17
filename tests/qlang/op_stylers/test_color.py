
import pandas as pd

from pandas.testing import (
    assert_frame_equal,
    assert_series_equal,
    )
from dukit import (
    get_df,
    log,
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



def test_background_color_cols():
    code = r"""
    %.bg(orange)
    """
    result = df.dk.qr(code).style_cols
    expected = pd.Series(
        '',
        index=df.columns,
        )
    expected[:] = 'background-color: orange;'
    assert_series_equal(result, expected)  # type: ignore



def test_background_color_rows():
    code = r"""
    %%.bg(orange)
    """
    result = df.dk.qr(code).style_rows
    expected = pd.Series(
        '',
        index=df.index,
        )
    expected[:] = 'background-color: orange;'
    assert_series_equal(result, expected)  # type: ignore



def test_background_color_vals1():
    code = r"""
    %%%.bg(orange)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'background-color: orange;'
    assert_frame_equal(result, expected)  # type: ignore



def test_background_color_vals2():
    code = r"""
    .bg(orange)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'background-color: orange;'
    assert_frame_equal(result, expected)  # type: ignore



def test_background_color_vals3():
    code = r"""
    age  <0  .bg(orange)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[[0], 'age'] = 'background-color: orange;'
    assert_frame_equal(result, expected)  # type: ignore




def test_color_cols():
    code = r"""
    %.color(orange)
    """
    result = df.dk.qr(code).style_cols
    expected = pd.Series(
        '',
        index=df.columns,
        )
    expected[:] = 'color: orange;'
    assert_series_equal(result, expected)  # type: ignore



def test_color_rows():
    code = r"""
    %%.color(orange)
    """
    result = df.dk.qr(code).style_rows
    expected = pd.Series(
        '',
        index=df.index,
        )
    expected[:] = 'color: orange;'
    assert_series_equal(result, expected)  # type: ignore



def test_color_vals1():
    code = r"""
    %%%.color(orange)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'color: orange;'
    assert_frame_equal(result, expected)  # type: ignore



def test_color_vals2():
    code = r"""
    .color(orange)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'color: orange;'
    assert_frame_equal(result, expected)  # type: ignore



def test_color_vals3():
    code = r"""
    age  <0  .color(orange)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[[0], 'age'] = 'color: orange;'
    assert_frame_equal(result, expected)  # type: ignore
