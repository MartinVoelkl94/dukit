
import pandas as pd

from .pandas import get_df
from .utils import (
    GREEN,
    RED,
    GREEN_LIGHT,
    ORANGE_LIGHT,
    RED_LIGHT,
    )


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



def _get_diff_new():

    uid = pd.Series(
        ['y', 'x2', 'z'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['diff', 'uid', 'd', 'b', 'a'],
        index=uid,
        )

    expected['uid'] = expected.index

    expected.loc['y', 'diff'] = 'vals changed: 1'
    expected.loc['x2', 'diff'] = 'row added'
    expected.loc['z', 'diff'] = 'vals added: 1<br>vals removed: 1'

    expected.loc['y', 'd'] = 2
    expected.loc['x2', 'd'] = 1
    expected.loc['z', 'd'] = 3

    expected.loc['y', 'b'] = 2
    expected.loc['x2', 'b'] = 1
    expected.loc['z', 'b'] = 3

    expected.loc['y', 'a'] = 0
    expected.loc['x2', 'a'] = 1
    expected.loc['z', 'a'] = pd.NA

    expected = expected.reset_index(drop=True)

    return expected.convert_dtypes()


def _get_diff_newplus():

    uid = pd.Series(
        ['y', 'x2', 'z'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['diff', 'uid', 'd', 'b', 'b *old', 'a', 'a *old'],
        index=uid,
        )

    expected['uid'] = expected.index

    expected.loc['y', 'diff'] = 'vals changed: 1'
    expected.loc['x2', 'diff'] = 'row added'
    expected.loc['z', 'diff'] = 'vals added: 1<br>vals removed: 1'

    expected.loc['y', 'd'] = 2
    expected.loc['x2', 'd'] = 1
    expected.loc['z', 'd'] = 3

    expected.loc['y', 'b'] = 2
    expected.loc['x2', 'b'] = 1
    expected.loc['z', 'b'] = 3

    expected.loc['y', 'b *old'] = pd.NA
    expected.loc['x2', 'b *old'] = pd.NA
    expected.loc['z', 'b *old'] = pd.NA

    expected.loc['y', 'a'] = 0
    expected.loc['x2', 'a'] = 1
    expected.loc['z', 'a'] = pd.NA

    expected.loc['y', 'a *old'] = 2
    expected.loc['x2', 'a *old'] = pd.NA
    expected.loc['z', 'a *old'] = 3

    expected['b *old'] = expected['b *old'].astype('Int64')
    expected = expected.reset_index(drop=True)

    return expected.convert_dtypes()


def _get_diff_old():

    uid = pd.Series(
        ['x', 'y', 'z'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['diff', 'uid', 'a', 'b', 'c'],
        index=uid,
        )

    expected['uid'] = expected.index

    expected.loc['x', 'diff'] = 'row removed'
    expected.loc['y', 'diff'] = 'vals changed: 1'
    expected.loc['z', 'diff'] = 'vals added: 1<br>vals removed: 1'

    expected.loc['x', 'a'] = 1
    expected.loc['y', 'a'] = 2
    expected.loc['z', 'a'] = 3

    expected.loc['x', 'b'] = 1
    expected.loc['y', 'b'] = 2
    expected.loc['z', 'b'] = pd.NA

    expected.loc['x', 'c'] = 1
    expected.loc['y', 'c'] = 2
    expected.loc['z', 'c'] = 3

    expected = expected.reset_index(drop=True)

    return expected.convert_dtypes()


def _get_diff_mix():

    uid = pd.Series(
        ['y', 'x2', 'z', 'x'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['diff', 'uid', 'd', 'b', 'a', 'c'],
        index=uid,
        )

    expected['uid'] = expected.index

    expected.loc['y', 'diff'] = 'vals changed: 1'
    expected.loc['x2', 'diff'] = 'row added'
    expected.loc['z', 'diff'] = 'vals added: 1<br>vals removed: 1'
    expected.loc['x', 'diff'] = 'row removed'

    expected.loc['y', 'd'] = 2
    expected.loc['x2', 'd'] = 1
    expected.loc['z', 'd'] = 3
    expected.loc['x', 'd'] = pd.NA

    expected.loc['y', 'b'] = 2
    expected.loc['x2', 'b'] = 1
    expected.loc['z', 'b'] = 3
    expected.loc['x', 'b'] = 1


    expected.loc['y', 'a'] = 0
    expected.loc['x2', 'a'] = 1
    expected.loc['z', 'a'] = pd.NA
    expected.loc['x', 'a'] = 1

    expected.loc['y', 'c'] = 2
    expected.loc['x2', 'c'] = pd.NA
    expected.loc['z', 'c'] = 3
    expected.loc['x', 'c'] = 1

    expected = expected.reset_index(drop=True)

    return expected.convert_dtypes()




def _get_diff_style_new():

    uid = pd.Series(
        ['y', 'x2', 'z'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['d', 'b', 'a'],
        index=uid,
        )

    expected.loc['y', 'd'] = f'background-color: {GREEN};'
    expected.loc['x2', 'd'] = f'background-color: {GREEN};background-color: {GREEN};'
    expected.loc['z', 'd'] = f'background-color: {GREEN};'

    expected.loc['y', 'b'] = ''
    expected.loc['x2', 'b'] = f'background-color: {GREEN};'
    expected.loc['z', 'b'] = f'background-color: {GREEN_LIGHT};'

    expected.loc['y', 'a'] = f'background-color: {ORANGE_LIGHT};'
    expected.loc['x2', 'a'] = f'background-color: {GREEN};'
    expected.loc['z', 'a'] = f'background-color: {RED_LIGHT};'

    expected = expected.reset_index(drop=True)

    return expected.convert_dtypes()



def _get_diff_style_newplus():

    uid = pd.Series(
        ['y', 'x2', 'z'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['d', 'b', 'b *old', 'a', 'a *old'],
        index=uid,
        )

    expected.loc['y', 'd'] = f'background-color: {GREEN};'
    expected.loc['x2', 'd'] = f'background-color: {GREEN};background-color: {GREEN};'
    expected.loc['z', 'd'] = f'background-color: {GREEN};'

    expected.loc['y', 'b'] = ''
    expected.loc['x2', 'b'] = f'background-color: {GREEN};'
    expected.loc['z', 'b'] = f'background-color: {GREEN_LIGHT};'

    expected.loc['y', 'b *old'] = 'font-style: italic;'
    expected.loc['x2', 'b *old'] = f'font-style: italic;background-color: {GREEN};'
    expected.loc['z', 'b *old'] = 'font-style: italic;'

    expected.loc['y', 'a'] = f'background-color: {ORANGE_LIGHT};'
    expected.loc['x2', 'a'] = f'background-color: {GREEN};'
    expected.loc['z', 'a'] = f'background-color: {RED_LIGHT};'

    expected.loc['y', 'a *old'] = 'font-style: italic;'
    expected.loc['x2', 'a *old'] = f'font-style: italic;background-color: {GREEN};'
    expected.loc['z', 'a *old'] = 'font-style: italic;'

    expected = expected.reset_index(drop=True)

    return expected.convert_dtypes()



def _get_diff_style_old():

    uid = pd.Series(
        ['x', 'y', 'z'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['a', 'b', 'c'],
        index=uid,
        )

    expected.loc['x', 'a'] = f'background-color: {RED};'
    expected.loc['y', 'a'] = f'background-color: {ORANGE_LIGHT};'
    expected.loc['z', 'a'] = f'background-color: {RED_LIGHT};'

    expected.loc['x', 'b'] = f'background-color: {RED};'
    expected.loc['y', 'b'] = ''
    expected.loc['z', 'b'] = f'background-color: {GREEN_LIGHT};'

    expected.loc['x', 'c'] = f'background-color: {RED};background-color: {RED};'
    expected.loc['y', 'c'] = f'background-color: {RED};'
    expected.loc['z', 'c'] = f'background-color: {RED};'

    expected = expected.reset_index(drop=True)

    return expected.convert_dtypes()



def _get_diff_style_mix():

    uid = pd.Series(
        ['y', 'x2', 'z', 'x'],
        dtype='string',
        name='uid',
        )
    expected = pd.DataFrame(
        columns=['d', 'b', 'a', 'c'],
        index=uid,
        )

    expected.loc['x', 'd'] = f'background-color: {GREEN};background-color: {RED};'
    expected.loc['y', 'd'] = f'background-color: {GREEN};'
    expected.loc['x2', 'd'] = f'background-color: {GREEN};background-color: {GREEN};'
    expected.loc['z', 'd'] = f'background-color: {GREEN};'

    expected.loc['x', 'b'] = f'background-color: {RED};'
    expected.loc['y', 'b'] = ''
    expected.loc['x2', 'b'] = f'background-color: {GREEN};'
    expected.loc['z', 'b'] = f'background-color: {GREEN_LIGHT};'

    expected.loc['x', 'a'] = f'background-color: {RED};'
    expected.loc['y', 'a'] = f'background-color: {ORANGE_LIGHT};'
    expected.loc['x2', 'a'] = f'background-color: {GREEN};'
    expected.loc['z', 'a'] = f'background-color: {RED_LIGHT};'

    expected.loc['x', 'c'] = f'background-color: {RED};background-color: {RED};'
    expected.loc['y', 'c'] = f'background-color: {RED};'
    expected.loc['x2', 'c'] = f'background-color: {GREEN};background-color: {RED};'
    expected.loc['z', 'c'] = f'background-color: {RED};'


    expected = expected.reset_index(drop=True)

    return expected.convert_dtypes()



def _get_ungrouped_basic():

    expected = get_df()
    col_new1 = pd.Series([
        'John',
        'Jane',
        'Alice',
        'Bob',
        'eva',
        'Frank',
        'Grace',
        'Harry',
        'IVY',
        'JAck',
        'john',
        ],
        dtype='string',
        )
    col_new2 = pd.Series([
        'Doe',
        'Smith',
        'Johnson',
        'Brown',
        'white',
        'miller',
        'TAYLOR',
        'Clark',
        'GREEN',
        'Williams',
        'Doe',
        ],
        dtype='string',
        )
    expected = expected.drop(columns=['name'])
    expected.insert(loc=1, column='first name', value=col_new1)
    expected.insert(loc=2, column='last name', value=col_new2)

    return expected



def _get_ungrouped_default():

    expected = get_df()
    col_new1 = pd.Series([
        'John',
        'Jane',
        'Alice',
        'Bob',
        'eva',
        'Frank',
        'Grace',
        'Harry',
        'IVY',
        'JAck',
        'john',
        ],
        dtype='string',
        )
    col_new2 = pd.Series([
        'Doe',
        'Smith',
        'Johnson',
        'Brown',
        'white',
        'miller',
        'TAYLOR',
        'Clark',
        'GREEN',
        'Williams',
        'Doe',
        ],
        dtype='string',
        )
    expected = expected.drop(columns=['name'])
    expected.insert(loc=1, column='name_1', value=col_new1)
    expected.insert(loc=2, column='name_2', value=col_new2)

    return expected



def _get_ungrouped_overwrite():

    expected = get_df()
    col_new1 = pd.Series([
        'John',
        'Jane',
        'Alice',
        'Bob',
        'eva',
        'Frank',
        'Grace',
        'Harry',
        'IVY',
        'JAck',
        'john',
        ],
        dtype='string',
        )
    col_new2 = pd.Series([
        'Doe',
        'Smith',
        'Johnson',
        'Brown',
        'white',
        'miller',
        'TAYLOR',
        'Clark',
        'GREEN',
        'Williams',
        'Doe',
        ],
        dtype='string',
        )
    expected = expected.drop(columns=['name'])
    expected.insert(loc=1, column='name', value=col_new1)
    expected.insert(loc=2, column='last name', value=col_new2)

    return expected



def _get_ungrouped_no_match():

    expected = get_df()
    col_new1 = pd.Series(
        [pd.NA for col in expected.columns],
        dtype='string',
        )
    col_new2 = pd.Series(
        [pd.NA for col in expected.columns],
        dtype='string',
        )
    expected['name'] = col_new1
    expected.insert(loc=2, column='last name', value=col_new2)

    return expected
