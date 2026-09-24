
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



def test_font_cols():
    code = r"""
    %.font(bold)
    """
    result = df.dk.qr(code).style_cols
    expected = pd.Series(
        '',
        index=df.columns,
        )
    expected[:] = 'font-weight: bold;'
    assert_series_equal(result, expected)  # type: ignore



def test_font_rows():
    code = r"""
    %%.font(italic)
    """
    result = df.dk.qr(code).style_rows
    expected = pd.Series(
        '',
        index=df.index,
        )
    expected[:] = 'font-style: italic;'
    assert_series_equal(result, expected)  # type: ignore



def test_font_vals1():
    code = r"""
    %%%.font(normal)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'font-weight: normal; font-style: normal;'
    assert_frame_equal(result, expected)  # type: ignore



def test_font_vals2():
    code = r"""
    .font(bolder)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'font-weight: bolder;'
    assert_frame_equal(result, expected)  # type: ignore



def test_font_vals3():
    code = r"""
    age  <0  .font(lighter)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[[0], 'age'] = 'font-weight: lighter;'
    assert_frame_equal(result, expected)  # type: ignore



def test_font_vals4():
    code = r"""
    age  <0  .font(oblique)
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[[0], 'age'] = 'font-style: oblique;'
    assert_frame_equal(result, expected)  # type: ignore
