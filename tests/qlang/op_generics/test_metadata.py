
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



def test_append():
    df1 = df.copy()
    df1['_meta'] = 'a'

    code = r"""
    .tag('b')
    %
    """
    result = df1.dk.qr(code).result
    expected = get_df()
    expected['_meta'] = 'ab'
    expected['_meta'] = expected['_meta'].astype('string')
    assert_frame_equal(result, expected)



def test_basic1():
    code = r"""
    .tag('')
    %
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['_meta'] = ''
    expected['_meta'] = expected['_meta'].astype('string')
    assert_frame_equal(result, expected)



def test_basic2():
    code = r"""
    .tag('', _meta1)
    %
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['_meta1'] = ''
    expected['_meta1'] = expected['_meta1'].astype('string')
    assert_frame_equal(result, expected)



def test_basic3():
    code = r"""
    .tag(a, _meta1)
    %
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['_meta1'] = 'a'
    expected['_meta1'] = expected['_meta1'].astype('string')
    assert_frame_equal(result, expected)



def test_basic4():
    code = r"""
    age  <0  .tag('INVALID')
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    vals = [
        'INVALID',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ]
    expected['_meta'] = pd.Series(vals, dtype='string')
    assert_frame_equal(result, expected)



def test_basic5():
    code = r"""
    age  <0  //!:isnum  .tag('INVALID')
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    vals = [
        'INVALID',
        '',
        '',
        'INVALID',
        '',
        'INVALID',
        'INVALID',
        'INVALID',
        '',
        'INVALID',
        '',
        ]
    expected['_meta'] = pd.Series(vals, dtype='string')
    assert_frame_equal(result, expected)



def test_basic6():
    code = r"""
    age  <0  //!:isnum  .tag('INVALID age;  ')
    height <0  //!:isnum  //>220  .tag('INVALID height;  ')
    %
    %%
    """
    result = df.dk.qr(code).result
    expected = get_df()
    vals = [
        'INVALID age;  ',
        'INVALID height;  ',
        '',
        'INVALID age;  INVALID height;  ',
        'INVALID height;  ',
        'INVALID age;  ',
        'INVALID age;  ',
        'INVALID age;  INVALID height;  ',
        'INVALID height;  ',
        'INVALID age;  ',
        '',
        ]
    expected['_meta'] = pd.Series(vals, dtype='string')
    assert_frame_equal(result, expected)



def test_complex():
    code = r"""
    name
        %%?john
    .save 1

    .tag(a)

    %
    %%

    name
        %%?doe
        //:load 1
    _meta
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['_meta'] = 'a'
    expected = expected.convert_dtypes().loc[[0, 2, 10], ['_meta']]
    assert_frame_equal(result, expected)



def test_coerce_type():
    df1 = df.copy()
    df1['_meta'] = 1

    code = r"""
    .tag('b')
    %
    """
    result = df1.dk.qr(code).result
    expected = get_df()
    expected['_meta'] = '1b'
    expected['_meta'] = expected['_meta'].astype('string')
    assert_frame_equal(result, expected)



def test_update_styles_cols():
    code = r"""
    age  %.color(orange)
    %
    .tag(a)
    %
    """
    result = df.dk.qr(code).style_cols.to_list()
    expected = [
        '',
        '',
        '',
        'color: orange;',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ]
    assert result == expected



def test_update_styles_rows():
    code = r"""
    %%§1  %%.color(orange)
    %%
    .tag(a)
    %
    """
    result = df.dk.qr(code).style_rows.to_list()
    expected = [
        '',
        'color: orange;',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ]
    assert result == expected



def test_update_styles_vals():
    code = r"""
    name  =='Bob Brown' .color(orange)
    %%
    .tag(a)
    %
    """
    result = df.dk.qr(code).style_vals['name'].to_list()
    expected = [
        '',
        '',
        '',
        'color: orange;',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        ]
    assert result == expected
