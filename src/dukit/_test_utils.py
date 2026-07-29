
import pandas as pd


def _setup_csv(df_old, df_new, tmpdir):

    path_df_old = f'{tmpdir}/df_old.csv'
    df_old.to_csv(path_df_old, index=False)

    path_df_new = f'{tmpdir}/df_new.csv'
    df_new.to_csv(path_df_new, index=False)

    return path_df_old, path_df_new


def _setup_xlsx(df_old, df_new, tmpdir):

    path_df_old = f'{tmpdir}/df_old.xlsx'
    df_old.to_excel(path_df_old, index=False)

    path_df_new = f'{tmpdir}/df_new.xlsx'
    df_new.to_excel(path_df_new, index=False)

    return path_df_old, path_df_new



def _get_dfs():

    df_old = pd.DataFrame(
        columns=['a', 'b', 'c'],
        index=['x', 'y', 'z', ],
        )

    df_old.insert(0, 'uid', df_old.index)

    df_old.loc['x', 'a'] = 1
    df_old.loc['x', 'b'] = 1
    df_old.loc['x', 'c'] = 1

    df_old.loc['y', 'a'] = 2
    df_old.loc['y', 'b'] = 2
    df_old.loc['y', 'c'] = 2

    df_old.loc['z', 'a'] = 3
    df_old.loc['z', 'b'] = None
    df_old.loc['z', 'c'] = 3


    df_new = pd.DataFrame(
        columns=['d', 'b', 'a'],
        index=['y', 'x2', 'z', ],
        )

    df_new.insert(0, 'uid', df_new.index)

    df_new.loc['y', 'd'] = 2
    df_new.loc['y', 'b'] = 2
    df_new.loc['y', 'a'] = 0

    df_new.loc['x2', 'd'] = 1
    df_new.loc['x2', 'b'] = 1
    df_new.loc['x2', 'a'] = 1

    df_new.loc['z', 'd'] = 3
    df_new.loc['z', 'b'] = 3
    df_new.loc['z', 'a'] = pd.NA

    return df_old, df_new



def _get_expected_new():

    uid = pd.Series(
        ['y', 'x2', 'z'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['diff', 'uid', 'd', 'b', 'a'],
        index=uid,
        dtype='string',
        )

    expected['uid'] = expected.index

    expected.loc['y', 'diff'] = 'vals changed: 1'
    expected.loc['y', 'd'] = '2'
    expected.loc['y', 'b'] = '2'
    expected.loc['y', 'a'] = '0'

    expected.loc['x2', 'diff'] = 'row added'
    expected.loc['x2', 'd'] = '1'
    expected.loc['x2', 'b'] = '1'
    expected.loc['x2', 'a'] = '1'

    expected.loc['z', 'diff'] = 'vals added: 1<br>vals removed: 1'
    expected.loc['z', 'd'] = '3'
    expected.loc['z', 'b'] = '3'
    expected.loc['z', 'a'] = pd.NA

    return expected


def _get_expected_newplus():

    uid = pd.Series(
        ['y', 'x2', 'z'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['diff', 'uid', 'd', 'b', 'b *old', 'a', 'a *old'],
        index=uid,
        dtype='string',
        )

    expected['uid'] = expected.index

    expected.loc['y', 'diff'] = 'vals changed: 1'
    expected.loc['y', 'd'] = '2'
    expected.loc['y', 'b'] = '2'
    expected.loc['y', 'b *old'] = ''
    expected.loc['y', 'a'] = '0'
    expected.loc['y', 'a *old'] = '2'

    expected.loc['x2', 'diff'] = 'row added'
    expected.loc['x2', 'd'] = '1'
    expected.loc['x2', 'b'] = '1'
    expected.loc['x2', 'b *old'] = ''
    expected.loc['x2', 'a'] = '1'
    expected.loc['x2', 'a *old'] = ''

    expected.loc['z', 'diff'] = 'vals added: 1<br>vals removed: 1'
    expected.loc['z', 'd'] = '3'
    expected.loc['z', 'b'] = '3'
    expected.loc['z', 'b *old'] = pd.NA
    expected.loc['z', 'a'] = pd.NA
    expected.loc['z', 'a *old'] = '3'

    return expected


def _get_expected_old():

    uid = pd.Series(
        ['x', 'y', 'z'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['diff', 'uid', 'a', 'b', 'c'],
        index=uid,
        dtype='string',
        )

    expected['uid'] = expected.index

    expected.loc['x', 'diff'] = 'row removed'
    expected.loc['x', 'a'] = '1'
    expected.loc['x', 'b'] = '1'
    expected.loc['x', 'c'] = '1'

    expected.loc['y', 'diff'] = 'vals changed: 1'
    expected.loc['y', 'a'] = '2'
    expected.loc['y', 'b'] = '2'
    expected.loc['y', 'c'] = '2'

    expected.loc['z', 'diff'] = 'vals added: 1<br>vals removed: 1'
    expected.loc['z', 'a'] = '3'
    expected.loc['z', 'b'] = pd.NA
    expected.loc['z', 'c'] = '3'

    return expected


def _get_expected_mix():

    uid = pd.Series(
        ['y', 'x2', 'z', 'x'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['diff', 'uid', 'd', 'b', 'a', 'c'],
        index=uid,
        dtype='string',
        )

    expected['uid'] = expected.index

    expected.loc['y', 'diff'] = 'vals changed: 1'
    expected.loc['y', 'd'] = '2'
    expected.loc['y', 'b'] = '2'
    expected.loc['y', 'a'] = '0'
    expected.loc['y', 'c'] = '2'

    expected.loc['x2', 'diff'] = 'row added'
    expected.loc['x2', 'd'] = '1'
    expected.loc['x2', 'b'] = '1'
    expected.loc['x2', 'a'] = '1'
    expected.loc['x2', 'c'] = pd.NA

    expected.loc['z', 'diff'] = 'vals added: 1<br>vals removed: 1'
    expected.loc['z', 'd'] = '3'
    expected.loc['z', 'b'] = '3'
    expected.loc['z', 'a'] = pd.NA
    expected.loc['z', 'c'] = '3'

    expected.loc['x', 'diff'] = 'row removed'
    expected.loc['x', 'd'] = pd.NA
    expected.loc['x', 'b'] = '1'
    expected.loc['x', 'a'] = '1'
    expected.loc['x', 'c'] = '1'

    return expected
