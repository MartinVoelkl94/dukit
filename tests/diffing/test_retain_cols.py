
import pandas as pd
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



def test_retain_col_a_new():

    df_old, df_new = _get_dfs()

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected = expected[['uid', 'diff', 'a', 'd', 'b']]

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_new_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected = expected[['uid', 'diff', 'a', 'd', 'b']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_new_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected = expected[['uid', 'diff', 'a', 'd', 'b']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_new():

    df_old, df_new = _get_dfs()

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'b', 'd', 'a']]

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_new_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'b', 'd', 'a']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_new_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'b', 'd', 'a']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_new():

    df_old, df_new = _get_dfs()

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'a', 'b', 'd']]

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_new_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'a', 'b', 'd']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_new_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'a', 'b', 'd']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_newplus():

    df_old, df_new = _get_dfs()

    expected = _get_expected_newplus()
    expected.drop(columns=['a *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected = expected[['uid', 'diff', 'a', 'd', 'b', 'b *old']]

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_newplus_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['a *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected = expected[['uid', 'diff', 'a', 'd', 'b', 'b *old']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_newplus_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['a *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected = expected[['uid', 'diff', 'a', 'd', 'b', 'b *old']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_newplus():

    df_old, df_new = _get_dfs()

    expected = _get_expected_newplus()
    expected.drop(columns=['b *old'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'b', 'd', 'a', 'a *old']]

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_newplus_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['b *old'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'b', 'd', 'a', 'a *old']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_newplus_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['b *old'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'b', 'd', 'a', 'a *old']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_newplus():

    df_old, df_new = _get_dfs()

    expected = _get_expected_newplus()
    expected.drop(columns=['a *old', 'b *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'a', 'b', 'd']]

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_newplus_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['a *old', 'b *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'a', 'b', 'd']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_newplus_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['a *old', 'b *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected = expected[['uid', 'diff', 'a', 'b', 'd']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_old():

    df_old, df_new = _get_dfs()

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_old_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_old_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_old():

    df_old, df_new = _get_dfs()

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected = expected[['uid', 'diff', 'b', 'a', 'c']]

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_old_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected = expected[['uid', 'diff', 'b', 'a', 'c']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_old_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected = expected[['uid', 'diff', 'b', 'a', 'c']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_old():

    df_old, df_new = _get_dfs()

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_old_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_old_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_mix():

    df_old, df_new = _get_dfs()

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected = expected[['uid', 'diff', 'a', 'd', 'b', 'c']]

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_mix_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected = expected[['uid', 'diff', 'a', 'd', 'b', 'c']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_a_mix_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected = expected[['uid', 'diff', 'a', 'd', 'b', 'c']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_mix():

    df_old, df_new = _get_dfs()

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected = expected[['uid', 'diff', 'b', 'd', 'a', 'c']]

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_mix_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected = expected[['uid', 'diff', 'b', 'd', 'a', 'c']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_col_b_mix_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected = expected[['uid', 'diff', 'b', 'd', 'a', 'c']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_mix():

    df_old, df_new = _get_dfs()

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected = expected[['uid', 'diff', 'a', 'b', 'd', 'c']]

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_mix_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected = expected[['uid', 'diff', 'a', 'b', 'd', 'c']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_retain_cols_mix_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''
    expected.loc[expected['uid'] == 'x2', 'a'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'z', 'a'] = 3
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected.loc[expected['uid'] == 'x2', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'z', 'b'] = pd.NA
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected = expected[['uid', 'diff', 'a', 'b', 'd', 'c']]

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)
