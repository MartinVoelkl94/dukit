
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



@pytest.mark.parametrize('code, expected_cols_vals, message', [
    (
        r'.new(a, b)',
        {'a': 'b'},
        None
    ),
    (
        r'.new(a, 1)',
        {'a': 1},
        None
    ),
    (
        r'.new(a, 1.0)',
        {'a': 1.0},
        None
    ),
    (
        r'.new(a, 1.0, +int)',
        {'a': 1},
        None
    ),
    (
        r'.new(a, 1.0, +float)',
        {'a': 1.0},
        None
    ),
    (
        r'.new(a, 1.0, +num)',
        {'a': 1.0},
        None
    ),
    (
        r'.new(a, 1.0, +str)',
        {'a': '1.0'},
        None
    ),
    (
        r'.new(a, 1.0, +bool)',
        {'a': True},
        None
    ),
    (
        r'.new(a, 1.0, +date)',
        {'a': pd.NaT},
        None
    ),
    (
        r'.new(a, 1.0, +datetime)',
        {'a': pd.NaT},
        None
    ),
    (
        r'.new(a, 2000.01.02, +date)',
        {'a': pd.to_datetime('2000-01-02').date()},
        None
    ),
    (
        r'.new(a, 2000.01.02, +datetime)',
        {'a': pd.to_datetime('2000-01-02')},
        None
    ),
    (
        r'.new(a, 1)   .new(b, 2)',
        {'b': 2},
        None
    ),
    (
        r'.new(a, 1)   .new(b, 2) /a',
        {'a': 1, 'b': 2},
        None
    ),

    ])
def test_basic(code, expected_cols_vals, message):

    result = df.dk.qr(code).result
    expected = get_df()
    for col, value in expected_cols_vals.items():
        expected[col] = value
    cols_expected = list(expected_cols_vals.keys())
    expected = expected.convert_dtypes().loc[:, cols_expected]
    assert_frame_equal(result, expected)

    if message:
        check_message(message)




def test_complex1():
    code = 'name   .new(a, 1)'
    result = df.dk.qr(code).result
    expected = get_df()
    expected['a'] = 1
    expected = expected.convert_dtypes().loc[:, ['a']]
    assert_frame_equal(result, expected)



def test_complex2():
    code = 'name   .new(a, 1)   /age'
    result = df.dk.qr(code).result
    expected = get_df()
    expected['a'] = 1
    expected = expected.convert_dtypes().loc[:, ['age', 'a']]
    assert_frame_equal(result, expected)



def test_complex3():
    code = r'.new(a, 1)  %%==(0, +index)'
    result = df.dk.qr(code).result
    expected = get_df()
    expected['a'] = 1
    expected = expected.convert_dtypes().loc[[0], ['a']]
    assert_frame_equal(result, expected)



def test_complex4():
    code = r"""
    name
        %%?john
    .new(a, 1)
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['a'] = 1
    expected = expected.convert_dtypes().loc[[0, 2, 10], ['a']]
    assert_frame_equal(result, expected)



def test_complex5():
    code = r"""
    name
        %%?john

    .new(a, 1)

    name
        &&?doe

    /a
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['a'] = 1
    expected = expected.convert_dtypes().loc[[0, 10], ['name', 'a']]
    assert_frame_equal(result, expected)



def test_complex6():
    code = r"""
    name
        %%?john
    .save 1

    .new(a, 1)

    %
    %%

    name
        %%?doe
        //:load 1
    a
    """
    result = df.dk.qr(code).result
    expected = get_df()
    expected['a'] = 1
    expected = expected.convert_dtypes().loc[[0, 2, 10], ['a']]
    assert_frame_equal(result, expected)



def test_update_styles_cols():
    code = r"""
    age  %.color(orange)
    %
    .new(a)
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
    .new(a)
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
    .new(a)
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
