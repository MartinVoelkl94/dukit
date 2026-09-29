
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



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r"""
        name  %=full_name  %
        """,
        [
            'ID',
            'full_name',
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
        ],
        None,
        None,
        ['string'],
        None,
    ),
    (
        r"""
        name  /age  %=renamed  %
        """,
        [
            'ID',
            'renamed',
            'date of birth',
            'renamed',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
        ],
        None,
        None,
        ['string'],
        None,
    ),
    (
        r"""
        name %=full_name
        'date of birth' %=dob
        %
        """,
        [
            'ID',
            'full_name',
            'dob',
            'age',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
        ],
        None,
        None,
        ['string'],
        None,
    ),

    ])
def test_set(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()
    expected.columns = pd.Series(cols).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #subtract
    (
        r'name  %!-=1  %',
        df.columns,
        None,
        None,
        ['object'],
        'ERROR: cannot negate substraction of a non-string value',
    ),

    ])
def test_subtract(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()
    expected.columns = pd.Series(cols).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)
