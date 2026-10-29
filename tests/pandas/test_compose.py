

import pytest
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import get_df, log
from dukit._test_utils import (
    _get_decomposed_basic,
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
    df = _get_decomposed_basic()
    result = df.dk.compose(
        col='name',
        cols=['first name', 'last name'],
        template='{0} {1}',
        )
    expected = get_df()
    assert_frame_equal(result, expected, check_dtype=False)


def test_overwrite():
    df = _get_decomposed_overwrite()
    result = df.dk.compose(
        col='name',
        cols=['name', 'last name'],
        template='{0} {1}',
        )
    expected = get_df()
    assert_frame_equal(result, expected, check_dtype=False)
    check_message('WARNING: col "name" already exists.')


def test_no_cols():
    df = _get_decomposed_basic()
    with pytest.raises(ValueError):
        result = df.dk.compose(
            col='name',
            cols=['non_existent_col', 'last name'],
            template='{0}_{1}',
            )


def test_col_not_unique():
    df = _get_decomposed_basic()
    df = pd.concat([df,df], axis='columns')
    with pytest.raises(ValueError):
        result = df.dk.compose(
            col='name',
            cols=['first name', 'last name'],
            template='{0} {1}',
            )


def test_too_many_groups():
    df = _get_decomposed_basic()
    with pytest.raises(IndexError):
        result = df.dk.compose(
            col='name',
            cols=['first name', 'last name'],
            template='{0} {1} {2}',
            )


def test_too_few_groups():
    df = _get_decomposed_basic()
    result = df.dk.compose(
        col='name',
        cols=['first name', 'last name', 'age'],
        template='{0} {1}',
        )
    expected = get_df()
    expected = expected.drop(columns=['age'])
    assert_frame_equal(result, expected, check_dtype=False)
