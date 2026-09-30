
import pytest
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    )


df = get_df()
tstamp = pd.Timestamp('2024-01-01')
df_types = pd.DataFrame({
    'a': ['a'],
    0: [0],
    0.1: [0.1],
    pd.Timestamp('2024-01-01'): [tstamp],
    True: [True],
    'unknown': ['unknown'],
    None: [None],
    'b': ['a'],
    }).convert_dtypes()
df_types.rename(columns={'b': 'a'}, inplace=True)
df_types.columns = df_types.columns.to_series().convert_dtypes()
df_types.index = df_types.index.to_series().convert_dtypes()


def check_message(expected_strings):

    if isinstance(expected_strings, str):
        expected_strings = (expected_strings,)

    logs = log().data  #type: ignore (using no args, log() always returns a styler)
    logs['text_full'] = logs['level'] + ': ' + logs['text']
    text_full = '\n'.join(logs['text_full'].to_list())

    for string in expected_strings:
        error = f'did not find string "{string}" in logs:\n{text_full}'
        assert string in text_full, error



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [
    (
        r'%:isstr',
        ['a', 'unknown'],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isint',
        [0, True],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isfloat',
        [0, 0.1, True],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isfloat +strict',
        [0.1],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isnum',
        [0, 0.1, tstamp, True, None],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isbool',
        [0, True],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isdatetime',
        [tstamp],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isdate',
        [tstamp],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isna',
        [None],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isnk',
        ['unknown'],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isyn',
        [0, True],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isunique',
        [0, 0.1, tstamp, True, 'unknown', None],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%!:isunique',
        ['a'],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:isfirst',
        ['a', 0, 0.1, tstamp, True, 'unknown', None],
        df_types.index,
        None,
        None,
        None,
    ),
    (
        r'%:islast',
        [0, 0.1, tstamp, True, 'unknown', None, 'a'],
        df_types.index,
        None,
        None,
        None,
    ),
    ])
def test_cols(code, cols, rows, vals, dtypes, message):

    result = df_types.dk.qr(code).result
    if code == '%:isstr':
        result = result[['a', 'unknown']]  #qlang reorders, while pd does not

    if code == '%:isfirst':
        expected = df_types.iloc[:, :7]  #type: ignore
        expected = expected.loc[rows, cols]
    elif code == '%:islast':
        expected = df_types.iloc[:, 1:]  #type: ignore
        expected = expected.loc[rows, cols]
    else:
        expected = df_types.loc[rows, cols]

    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)

    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r'name  %%:isstr()',
        ['name'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'name  %%!:isstr()',
        ['name'],
        [],
        None,
        None,
        None,
    ),
    (
        r'name  %%:isnum()',
        ['name'],
        [],
        None,
        None,
        None,
    ),
    (
        r'name  %%!:isnum()',
        ['name'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'name  %%:isna()',
        ['name'],
        [],
        None,
        None,
        None,
    ),
    (
        r'name  %%:!isna()',
        ['name'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'age   %%:isint()',
        ['age'],
        [0, 1, 4, 10],
        None,
        None,
        None,
    ),
    (
        r'age   %%:isint(+strict)',
        ['age'],
        [0, 10],
        None,
        None,
        None,
    ),
    (
        r'age   %%:isfloat()',
        ['age'],
        [0, 1, 2, 4, 6, 10],
        None,
        None,
        None,
    ),
    (
        r'age   %%:isfloat(+strict)',
        ['age'],
        [2],
        None,
        None,
        None,
    ),
    (
        r'age   %%:isna()',
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),

    (
        r'weight  %%:isint()',
        ['weight'],
        [1, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%:isint(+strict)',
        ['weight'],
        [10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%:isfloat()',
        ['weight'],
        [0, 1, 7, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%:isfloat(+strict)',
        ['weight'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'weight  %%:isnum()',
        ['weight'],
        [0, 1, 4, 6, 7, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%:isnum(+strict)',
        ['weight'],
        [0, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%:isnum()  &&!:isna()',
        ['weight'],
        [0, 1, 7, 9, 10],
        None,
        None,
        None,
    ),

    (
        r'height       %%:isbool()',
        ['height'],
        [6],
        None,
        None,
        None,
    ),
    (
        r'"bp diastole"  %%:isbool()',
        ['bp diastole'],
        [9],
        None,
        None,
        None,
    ),
    (
        r'diabetes     %%:isbool()',
        ['diabetes'],
        [0, 1, 3, 4, 5, 6, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'diabetes     %%:isbool(+strict)',
        ['diabetes'],
        [0, 10],
        None,
        None,
        None,
    ),

    (
        r'"date of birth"  %%:isdate()',
        ['date of birth'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%:isdate()  +strict',
        ['date of birth'],
        [0, 1, 5, 6],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%:isdatetime()',
        ['date of birth'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%:isdatetime()  +strict',
        ['date of birth'],
        [0, 1, 5, 6],
        None,
        None,
        None,
    ),

    (
        r'diabetes  %%:isyn()',
        ['diabetes'],
        [0, 1, 3, 4, 5, 6, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'diabetes  %%:isna()  //:isyn()',
        ['diabetes'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'cholesterol  %%:isna()',
        ['cholesterol'],
        [2, 4, 7, 9],
        None,
        None,
        None,
    ),
    (
        r'age  %%:isna()',
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),
    (
        r'age  %%:isna(+strict)',
        ['age'],
        [2, 3],
        None,
        None,
        None,
    ),

    (
        r'age  %%:isnk()',
        ['age'],
        [7, 9],
        None,
        None,
        None,
    ),

    ])
def test_rows(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r'name  %%%:isstr()  %%:trim',
        ['name'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'name  %%%!:isstr()  %%:trim',
        ['name'],
        [],
        None,
        None,
        None,
    ),
    (
        r'name  %%%:isnum()  %%:trim',
        ['name'],
        [],
        None,
        None,
        None,
    ),
    (
        r'name  %%%!:isnum()  %%:trim',
        ['name'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'name  %%%:isna()  %%:trim',
        ['name'],
        [],
        None,
        None,
        None,
    ),
    (
        r'name  %%%:!isna()  %%:trim',
        ['name'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'age   %%%:isint()  %%:trim',
        ['age'],
        [0, 1, 4, 10],
        None,
        None,
        None,
    ),
    (
        r'age   %%%:isint(+strict)  %%:trim',
        ['age'],
        [0, 10],
        None,
        None,
        None,
    ),
    (
        r'age   %%%:isfloat()  %%:trim',
        ['age'],
        [0, 1, 2, 4, 6, 10],
        None,
        None,
        None,
    ),
    (
        r'age   %%%:isfloat(+strict)  %%:trim',
        ['age'],
        [2],
        None,
        None,
        None,
    ),
    (
        r'age   %%%:isna()  %%:trim',
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),

    (
        r'weight  %%%:isint()  %%:trim',
        ['weight'],
        [1, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%%:isint(+strict)  %%:trim',
        ['weight'],
        [10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%%:isfloat()  %%:trim',
        ['weight'],
        [0, 1, 7, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%%:isfloat(+strict)  %%:trim',
        ['weight'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'weight  %%%:isnum()  %%:trim',
        ['weight'],
        [0, 1, 4, 6, 7, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%%:isnum(+strict)  %%:trim',
        ['weight'],
        [0, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%%:isnum()  &&!:isna()  %%:trim',
        ['weight'],
        [0, 1, 7, 9, 10],
        None,
        None,
        None,
    ),

    (
        r'height       %%%:isbool()  %%:trim',
        ['height'],
        [6],
        None,
        None,
        None,
    ),
    (
        r'"bp diastole"  %%%:isbool()  %%:trim',
        ['bp diastole'],
        [9],
        None,
        None,
        None,
    ),
    (
        r'diabetes     %%%:isbool()  %%:trim',
        ['diabetes'],
        [0, 1, 3, 4, 5, 6, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'diabetes     %%%:isbool(+strict)  %%:trim',
        ['diabetes'],
        [0, 10],
        None,
        None,
        None,
    ),

    (
        r'"date of birth"  %%%:isdate()  %%:trim',
        ['date of birth'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%:isdate()  +strict  %%:trim',
        ['date of birth'],
        [0, 1, 5, 6],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%:isdatetime()  %%:trim',
        ['date of birth'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%:isdatetime()  +strict  %%:trim',
        ['date of birth'],
        [0, 1, 5, 6],
        None,
        None,
        None,
    ),

    (
        r'diabetes  %%%:isyn()  %%:trim',
        ['diabetes'],
        [0, 1, 3, 4, 5, 6, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'diabetes  %%%:isna()  //:isyn()  %%:trim',
        ['diabetes'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'cholesterol  %%%:isna()  %%:trim',
        ['cholesterol'],
        [2, 4, 7, 9],
        None,
        None,
        None,
    ),
    (
        r'age  %%%:isna()  %%:trim',
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),
    (
        r'age  %%%:isna(+strict)  %%:trim',
        ['age'],
        [2, 3],
        None,
        None,
        None,
    ),

    (
        r'age  %%%:isnk()  %%:trim',
        ['age'],
        [7, 9],
        None,
        None,
        None,
    ),

    ])
def test_vals(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)