
import dukit as dk
from pandas.testing import assert_frame_equal
from dukit._test_utils import (
    _get_dfs,
    _get_expected_new,
    )


def test_change_names():

    df_old, df_new = _get_dfs()

    result = dk.diff(
        df_old,
        df_new,
        rename_cols={'a': 'alpha', 'b': 'beta'},
        mode='new',
        verbosity=0,
        ).show().data  #type:ignore

    expected = _get_expected_new()
    expected.rename(columns={'a': 'alpha', 'b': 'beta'}, inplace=True)

    assert_frame_equal(result, expected)


def test_swap_names():

    df_old, df_new = _get_dfs()

    result = dk.diff(
        df_old,
        df_new,
        rename_cols={'a': 'b', 'b': 'a'},
        mode='new',
        verbosity=0,
        ).show().data  #type:ignore

    expected = _get_expected_new()
    expected.rename(columns={'a': 'b', 'b': 'a'}, inplace=True)

    assert_frame_equal(result, expected)
