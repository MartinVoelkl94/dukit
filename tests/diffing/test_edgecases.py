
import pytest
import dukit as dk
from pandas.testing import assert_frame_equal
from dukit._test_utils import (
    _get_dfs,
    _get_expected_new,
    )



def test_index_as_uid():

    df_old, df_new = _get_dfs()
    expected = _get_expected_new()
    expected.rename(columns={'uid': '<index>'}, inplace=True)

    result = dk.diff(
        df_old.set_index('uid'),
        df_new.set_index('uid'),
        uid=False,
        mode='new',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected, check_dtype=False)



def test_invalid_mode():

    df_old, df_new = _get_dfs()

    with pytest.raises(ValueError, match='Unknown mode'):
        dk.diff(
            df_old,
            df_new,
            mode='invalid',
            verbosity=0,
            )



def test_invalid_uid():

    df_old, df_new = _get_dfs()

    with pytest.raises(ValueError, match='UID column'):
        dk.diff(
            df_old,
            df_new,
            uid='missing',
            verbosity=0,
            )



def test_diffs_accessors():

    df_old, df_new = _get_dfs()
    diffs = dk.diff(df_old, df_new, verbosity=0)

    assert diffs[0] is diffs['data']
    assert list(diffs) == [diffs['data']]
    assert diffs.info().shape == (2, 2)
    assert list(diffs.summary().columns) == [
        'data',
        'uid',
        'in both dfs',
        'cols shared',
        'cols added',
        'cols removed',
        'rows shared',
        'rows added',
        'rows removed',
        'vals added',
        'vals removed',
        'vals changed',
        ]
    assert 'Diff objects:' in str(diffs)
    assert repr(diffs) == str(diffs)
