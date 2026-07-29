
import dukit as dk
from pandas.testing import assert_frame_equal
from dukit._test_utils import (
    _setup_csv,
    _setup_xlsx,
    _get_dfs,
    _get_expected_new,
    _get_expected_newplus,
    _get_expected_old,
    _get_expected_mix,
    )



def test_mode_new():

    df_old, df_new = _get_dfs()
    expected = _get_expected_new()

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_new_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)
    expected = _get_expected_new()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_new_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)
    expected = _get_expected_new()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_newplus():

    df_old, df_new = _get_dfs()
    expected = _get_expected_newplus()

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_newplus_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)
    expected = _get_expected_newplus()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_newplus_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)
    expected = _get_expected_newplus()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_old():

    df_old, df_new = _get_dfs()
    expected = _get_expected_old()

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_old_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)
    expected = _get_expected_old()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_old_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)
    expected = _get_expected_old()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_mix():

    df_old, df_new = _get_dfs()
    expected = _get_expected_mix()

    #in memory dfs
    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_mix_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)
    expected = _get_expected_mix()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mode_mix_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)
    expected = _get_expected_mix()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)
