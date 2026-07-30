
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



def test_remove_col_a_new():

    df_old, df_new = _get_dfs()

    expected = _get_expected_new()
    expected.drop(columns=['a'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_new_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.drop(columns=['a'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_new_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.drop(columns=['a'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_new():

    df_old, df_new = _get_dfs()

    expected = _get_expected_new()
    expected.drop(columns=['b'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_new_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.drop(columns=['b'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_new_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.drop(columns=['b'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_new():

    df_old, df_new = _get_dfs()

    expected = _get_expected_new()
    expected.drop(columns=['a', 'b'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_new_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.drop(columns=['a', 'b'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_new_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.drop(columns=['a', 'b'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_newplus():

    df_old, df_new = _get_dfs()

    expected = _get_expected_newplus()
    expected.drop(columns=['a', 'a *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_newplus_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['a', 'a *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_newplus_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['a', 'a *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_newplus():

    df_old, df_new = _get_dfs()

    expected = _get_expected_newplus()
    expected.drop(columns=['b', 'b *old'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_newplus_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['b', 'b *old'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_newplus_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['b', 'b *old'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_newplus():

    df_old, df_new = _get_dfs()

    expected = _get_expected_newplus()
    expected.drop(columns=['a', 'a *old', 'b', 'b *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_newplus_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['a', 'a *old', 'b', 'b *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_newplus_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.drop(columns=['a', 'a *old', 'b', 'b *old'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_old():

    df_old, df_new = _get_dfs()

    expected = _get_expected_old()
    expected.drop(columns=['a'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_old_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.drop(columns=['a'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_old_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.drop(columns=['a'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_old():

    df_old, df_new = _get_dfs()

    expected = _get_expected_old()
    expected.drop(columns=['b'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_old_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.drop(columns=['b'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_old_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.drop(columns=['b'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_old():

    df_old, df_new = _get_dfs()

    expected = _get_expected_old()
    expected.drop(columns=['a', 'b'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_old_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.drop(columns=['a', 'b'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_old_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.drop(columns=['a', 'b'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_mix():

    df_old, df_new = _get_dfs()

    expected = _get_expected_mix()
    expected.drop(columns=['a'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_mix_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.drop(columns=['a'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_a_mix_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.drop(columns=['a'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals added: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        remove_cols='a',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_mix():

    df_old, df_new = _get_dfs()

    expected = _get_expected_mix()
    expected.drop(columns=['b'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_mix_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.drop(columns=['b'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_col_b_mix_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.drop(columns=['b'], inplace=True)
    expected.loc[expected['uid'] == 'z', 'diff'] = 'vals removed: 1'

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        remove_cols='b',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_mix():

    df_old, df_new = _get_dfs()

    expected = _get_expected_mix()
    expected.drop(columns=['a', 'b'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_mix_csv(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.drop(columns=['a', 'b'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_remove_cols_mix_xlsx(tmpdir):

    df_old, df_new = _get_dfs()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.drop(columns=['a', 'b'], inplace=True)
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'z', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        remove_cols=['a', 'b'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)
