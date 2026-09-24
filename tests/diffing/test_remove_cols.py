
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



def test_cols_by_suffix_mix():

    df_old, df_new = _get_dfs()
    df_old['metadata *old'] = 'old'
    df_new['metadata *old'] = 'new'
    expected = _get_expected_mix()

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        remove_cols_by_suffix=' *old',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_cols_by_suffix_new():

    df_old, df_new = _get_dfs()
    df_old['metadata *old'] = 'old'
    df_new['metadata *old'] = 'new'
    expected = _get_expected_new()

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        remove_cols_by_suffix=' *old',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_cols_by_suffix_newplus():

    df_old, df_new = _get_dfs()
    df_old['metadata *old'] = 'old'
    df_new['metadata *old'] = 'new'
    expected = _get_expected_newplus()

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        remove_cols_by_suffix=' *old',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_cols_by_suffix_old():

    df_old, df_new = _get_dfs()
    df_old['metadata *old'] = 'old'
    df_new['metadata *old'] = 'new'
    expected = _get_expected_old()

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        remove_cols_by_suffix=' *old',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mix_col_a():

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



def test_mix_col_a_csv(tmpdir):

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



def test_mix_col_a_xlsx(tmpdir):

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



def test_mix_col_b():

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



def test_mix_col_b_csv(tmpdir):

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



def test_mix_col_b_xlsx(tmpdir):

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



def test_mix_cols():

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



def test_mix_cols_csv(tmpdir):

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



def test_mix_cols_xlsx(tmpdir):

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



def test_new_col_a():

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



def test_new_col_a_csv(tmpdir):

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



def test_new_col_a_xlsx(tmpdir):

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



def test_new_col_b():

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



def test_new_col_b_csv(tmpdir):

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



def test_new_col_b_xlsx(tmpdir):

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



def test_new_cols():

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



def test_new_cols_csv(tmpdir):

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



def test_new_cols_xlsx(tmpdir):

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



def test_newplus_col_a():

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



def test_newplus_col_a_csv(tmpdir):

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



def test_newplus_col_a_xlsx(tmpdir):

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



def test_newplus_col_b():

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



def test_newplus_col_b_csv(tmpdir):

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



def test_newplus_col_b_xlsx(tmpdir):

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



def test_newplus_cols():

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



def test_newplus_cols_csv(tmpdir):

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



def test_newplus_cols_xlsx(tmpdir):

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



def test_old_col_a():

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



def test_old_col_a_csv(tmpdir):

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



def test_old_col_a_xlsx(tmpdir):

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



def test_old_col_b():

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



def test_old_col_b_csv(tmpdir):

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



def test_old_col_b_xlsx(tmpdir):

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



def test_old_cols():

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



def test_old_cols_csv(tmpdir):

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



def test_old_cols_xlsx(tmpdir):

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
