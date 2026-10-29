

import pytest
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import get_df, log
from dukit._test_utils import (
    _get_decomposed_basic,
    _get_decomposed_default,
    _get_decomposed_overwrite,
    _get_decomposed_no_match,
    )



def check_message(expected_strings):

    if isinstance(expected_strings, str):
        expected_strings = (expected_strings,)

    logs = log().data  #type: ignore (using no args, log() always returns a styler)
    logs['text_full'] = logs['level'] + ': ' + logs['text']
    text_full = '\n'.join(logs['text_full'].to_list())

    for string in expected_strings:
        error = f'did not find string "{string}" in logs:\n{text_full}'
        assert string in text_full, error



def test_basic():
    df = get_df()
    result = df.dk.decompose(
        col='name',
        cols=['first name', 'last name'],
        pattern='(.+) (.+)',
        )
    expected = _get_decomposed_basic()
    assert_frame_equal(result, expected)


def test_default():
    df = get_df()
    result = df.dk.decompose(
        col='name',
        pattern='(.+) (.+)',
        )
    expected = _get_decomposed_default()
    assert_frame_equal(result, expected)


def test_overwrite():
    df = get_df()
    result = df.dk.decompose(
        col='name',
        cols=['name', 'last name'],
        pattern='(.+) (.+)',
        )
    expected = _get_decomposed_overwrite()
    assert_frame_equal(result, expected)
    check_message('WARNING: col "name" already exists.')


def test_no_col():
    df = get_df()
    with pytest.raises(ValueError):
        result = df.dk.decompose(
            col='non_existent_col',
            cols=['first name', 'last name'],
            pattern='(.+) (.+)',
            )


def test_col_not_unique():
    df = get_df()
    df = pd.concat([df,df], axis='columns')
    with pytest.raises(ValueError):
        result = df.dk.decompose(
            col='name',
            cols=['first name', 'last name'],
            pattern='(.+) (.+)',
            )


def test_too_many_groups():
    df = get_df()
    with pytest.raises(ValueError):
        result = df.dk.decompose(
            col='name',
            cols=['first name', 'last name'],
            pattern='(.+) (.+) (.+)',
            )


def test_too_few_groups():
    df = get_df()
    with pytest.raises(ValueError):
        result = df.dk.decompose(
            col='name',
            cols=['first name', 'last name'],
            pattern='(.+)',
            )


def test_no_match():
    df = get_df()
    result = df.dk.decompose(
        col='name',
        cols=['name', 'last name'],
        pattern='(.+)_(.+)',
        )
    expected = _get_decomposed_no_match()
    assert_frame_equal(result, expected)
    check_message('WARNING: No match found for group "0".')
    check_message('WARNING: No match found for group "1".')


def test_cols_already_exist():
    df = get_df()
    result = df.dk.decompose(
        col='name',
        cols=['ID', 'age'],
        pattern='(.+) (.+)',
        )
    check_message('WARNING: col "ID" already exists.')
    check_message('WARNING: col "age" already exists.')
