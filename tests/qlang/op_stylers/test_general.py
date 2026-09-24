
import pytest
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




def test_col_setter_compatible():
    code = r"""
    %.color(blue)
    name %='full name'
    %
    """
    result = df.dk.qr(code).style_cols
    cols = [
        'ID',
        'full name',
        'date of birth',
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
    cols = pd.Series(
        cols,
        dtype='string',
        )
    expected = pd.Series(
        '',
        index=cols,
        )
    expected[:] = 'color: blue;'
    assert_series_equal(result, expected)  # type: ignore



def test_row_setter_compatible():
    code = r"""
    %%.color(blue)
    %%==1 +index
    %%=11
    %%
    """
    result = df.dk.qr(code).style_rows
    indices = [
        0,
        11,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        ]
    indices = pd.Series(
        indices,
        dtype='Int64',
        )
    expected = pd.Series(
        '',
        index=indices,
        )
    expected[:] = 'color: blue;'
    assert_series_equal(result, expected)  # type: ignore



def test_val_setter_compatible():
    code = r"""
    .color(blue)
    %%%:isnum
    =11
    %%%
    """
    result = df.dk.qr(code).style_vals
    expected = pd.DataFrame(
        '',
        index=df.index,
        columns=df.columns,
        )
    expected.loc[:, :] = 'color: blue;'
    assert_frame_equal(result, expected)  # type: ignore



@pytest.mark.parametrize(
    'code',
    [
        '%.style',
        '%.style_table',
    ],
    )
def test_style_table_alias(code):
    query = df.dk.qr(code)
    result = [op.operator for op in query.ops]
    expected = [
        'SetStringReplace',
        'StyleTextWrap',
        'StyleMonospace',
        'StyleAlignement',
        'StyleAlignement',
        ]
    assert result == expected
