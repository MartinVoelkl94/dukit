
import pandas as pd
import dukit as dk

from pandas.testing import assert_frame_equal
from dukit._test_utils import (
    _setup_csv,
    _setup_xlsx,
    _get_expected_new,
    _get_expected_newplus,
    _get_expected_old,
    _get_expected_mix,
    )
from dukit import get_df_old, get_df_new



def test_mix_row_x():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected.loc[expected['uid'] == 'x', 'c'] = 1
    expected.loc[expected['uid'] == 'x', 'd'] = pd.NA
    expected = expected.loc[[3, 0, 1, 2]]
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        retain_rows='x',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mix_row_x_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected.loc[expected['uid'] == 'x', 'c'] = 1
    expected.loc[expected['uid'] == 'x', 'd'] = pd.NA
    expected = expected.loc[[3, 0, 1, 2]]
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_rows='x',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mix_row_x_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected.loc[expected['uid'] == 'x', 'c'] = 1
    expected.loc[expected['uid'] == 'x', 'd'] = pd.NA
    expected = expected.loc[[3, 0, 1, 2]]
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_rows='x',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mix_row_y():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'c'] = 2
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mix_row_y_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'c'] = 2
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mix_row_y_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'c'] = 2
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mix_rows():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'x', 'c'] = 1
    expected.loc[expected['uid'] == 'y', 'c'] = 2
    expected.loc[expected['uid'] == 'x', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected = expected.loc[[3, 0, 1, 2]]
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old,
        df_new,
        mode='mix',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mix_rows_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'x', 'c'] = 1
    expected.loc[expected['uid'] == 'y', 'c'] = 2
    expected.loc[expected['uid'] == 'x', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected = expected.loc[[3, 0, 1, 2]]
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_mix_rows_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_mix()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'x', 'a'] = 1
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'x', 'b'] = 1
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'x', 'c'] = 1
    expected.loc[expected['uid'] == 'y', 'c'] = 2
    expected.loc[expected['uid'] == 'x', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected = expected.loc[[3, 0, 1, 2]]
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='mix',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_new_row_x():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_new()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'a': 1,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        retain_rows=['x'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_new_row_x_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'a': 1,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_rows=['x'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_new_row_x_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'a': 1,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_rows=['x'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_new_row_y():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'a'] = 2

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_new_row_y_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'a'] = 2

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_new_row_y_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'a'] = 2

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_new_rows():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_new()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'a': 1,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'a'] = 2

    result = dk.diff(
        df_old,
        df_new,
        mode='new',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_new_rows_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'a': 1,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'a'] = 2

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_new_rows_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_new()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'a': 1,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'a'] = 2

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_newplus_row_x():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_newplus()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'b *old': pd.NA,
        'a': 1,
        'a *old': pd.NA,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()
    expected['b *old'] = expected['b *old'].astype('Int64')

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        retain_rows=['x'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_newplus_row_x_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'b *old': pd.NA,
        'a': 1,
        'a *old': pd.NA,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()
    expected['b *old'] = expected['b *old'].astype('Int64')

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_rows=['x'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_newplus_row_x_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'b *old': pd.NA,
        'a': 1,
        'a *old': pd.NA,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()
    expected['b *old'] = expected['b *old'].astype('Int64')

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_rows=['x'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_newplus_row_y():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_newplus()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'b *old'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'y', 'a *old'] = pd.NA

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_newplus_row_y_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'b *old'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'y', 'a *old'] = pd.NA

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_newplus_row_y_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'b *old'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'y', 'a *old'] = pd.NA

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_newplus_rows():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_newplus()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'b *old': pd.NA,
        'a': 1,
        'a *old': pd.NA,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()
    expected['b *old'] = expected['b *old'].astype('Int64')
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'b *old'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'y', 'a *old'] = pd.NA

    result = dk.diff(
        df_old,
        df_new,
        mode='new+',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_newplus_rows_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'b *old': pd.NA,
        'a': 1,
        'a *old': pd.NA,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()
    expected['b *old'] = expected['b *old'].astype('Int64')
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'b *old'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'y', 'a *old'] = pd.NA

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_newplus_rows_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_newplus()
    row_new = {
        'diff': '',
        'uid': 'x',
        'd': pd.NA,
        'b': 1,
        'b *old': pd.NA,
        'a': 1,
        'a *old': pd.NA,
        }
    expected = pd.concat([
        pd.DataFrame([row_new]),
        expected,
        ],
        ignore_index=True,
        ).convert_dtypes()
    expected['b *old'] = expected['b *old'].astype('Int64')
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'd'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'b'] = 2
    expected.loc[expected['uid'] == 'y', 'b *old'] = pd.NA
    expected.loc[expected['uid'] == 'y', 'a'] = 2
    expected.loc[expected['uid'] == 'y', 'a *old'] = pd.NA

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='new+',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_old_row_x():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        retain_rows='x',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_old_row_x_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_rows='x',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_old_row_x_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_rows='x',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_old_row_y():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected = expected.loc[[1, 0, 2]]
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_old_row_y_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected = expected.loc[[1, 0, 2]]
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_old_row_y_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'y', 'diff'] = ''
    expected = expected.loc[[1, 0, 2]]
    expected.reset_index(drop=True, inplace=True)

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_rows='y',
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_old_rows():

    df_old = get_df_old()
    df_new = get_df_new()

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'diff'] = ''

    result = dk.diff(
        df_old,
        df_new,
        mode='old',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_old_rows_csv(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_csv(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)



def test_old_rows_xlsx(tmpdir):

    df_old = get_df_old()
    df_new = get_df_new()
    df_old_file, df_new_file = _setup_xlsx(df_old, df_new, tmpdir)

    expected = _get_expected_old()
    expected.loc[expected['uid'] == 'x', 'diff'] = ''
    expected.loc[expected['uid'] == 'y', 'diff'] = ''

    result = dk.diff(
        df_old_file,
        df_new_file,
        mode='old',
        retain_rows=['x', 'y'],
        verbosity=0,
        ).show().data  #type:ignore

    assert_frame_equal(result, expected)
