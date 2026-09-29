
import pytest

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    )



df = get_df()

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
        r'"date of birth"  %%%1995.01.02  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%==1995.01.02  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%==1995_01_02  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="1995-01-02"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="1995/01/02"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="1995 01 02"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="1995-Jan-02"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="02-01-1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="02-Jan-1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="Jan-02-1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="02-01.1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="02 Jan-1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%%=="Jan/02_1995"  %%:trim',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"   .todatetime()   %%%==1995-01-02  %%:trim',
        ['date of birth'],
        [0],
        None,
        ['datetime64[us]'],
        None,
    ),
    (
        r'"date of birth"   .todatetime   %%%<1950.01.01  %%:trim',
        ['date of birth'],
        [10],
        None,
        ['datetime64[us]'],
        None,
    ),
    (
        r'"date of birth"   .todatetime   %%%>"1990/01/01"   &&&<"2000-01-01"  %%:trim',
        ['date of birth'],
        [0, 1],
        None,
        ['datetime64[us]'],
        None,
    ),

    ])
def test_dates(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if vals:
        for col, val in zip(cols, vals):
            expected[col] = val
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #by evaluating python expressions
    (
        r'age  %%%:eval("isinstance(x, int)")  %%:trim',
        ['age'],
        [0, 10],
        None,
        None,
        None,
    ),

    ])
def test_eval(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)


@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #invert
    (
        r"""
        name
            %%%?j
            %%%:invert
            %%:trim
        """,
        ['name'],
        [3, 4, 5, 6, 7, 8],
        None,
        None,
        None,
    ),

    ])
def test_invert(code, cols, rows, vals, dtypes, message):
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
        r'age  %%%==30  %%:trim',
        ['age'],
        [1],
        None,
        None,
        None,
    ),
    (
        r'age  %%%30  %%:trim',
        ['age'],
        [1],
        None,
        None,
        None,
    ),
    (
        r'age  %%%==30  %%:trim',
        ['age'],
        [1],
        None,
        None,
        None,
    ),
    (
        r'age  %%%==30.0  %%:trim',
        ['age'],
        [1],
        None,
        None,
        None,
    ),
    (
        r'age  %%%==(30.0 +strict)  %%:trim',
        ['age'],
        [],
        None,
        None,
        None,
    ),
    (
        r'age  %%%>30  %%:trim',
        ['age'],
        [4, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%%>=30  %%:trim',
        ['age'],
        [1, 4, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%%<30  %%:trim',
        ['age'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'age  %%%<=30  %%:trim',
        ['age'],
        [0, 1],
        None,
        None,
        None,
    ),
    (
        r'age  %%%!=30  %%:trim',
        ['age'],
        [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%%!=30.0  %%:trim',
        ['age'],
        [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%%!=(30 +strict)  %%:trim',
        ['age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'age  %%%!=(30.0, +strict)  %%:trim',
        ['age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'age  %%% !=30.0 +strict  %%:trim',
        ['age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'age  %%%!>30  %%:trim',
        ['age'],
        [0, 1, 2, 3, 5, 6, 7, 8, 9],
        None,
        None,
        None,
    ),
    (
        r'age  %%%!>=30  %%:trim',
        ['age'],
        [0, 2, 3, 5, 6, 7, 8, 9],
        None,
        None,
        None,
    ),
    (
        r'age  %%%!<30  %%:trim',
        ['age'],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%%!<=30  %%:trim',
        ['age'],
        [2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%%>70  %%:trim',
        ['weight'],
        [0, 7, 9],
        None,
        None,
        None,
    ),
    (
        r'weight  %%%70  %%:trim',
        ['weight'],
        [],
        None,
        None,
        None,
    ),

    ])
def test_numeric(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #regex equality
    (
        r'ID  %%%==("1...." +regex)  %%:trim',
        ['ID'],
        [0, 1, 2],
        None,
        None,
        None,
    ),
    (
        r'ID  %%%("1...." +regex)  %%:trim',
        ['ID'],
        [0, 1, 2],
        None,
        None,
        None,
    ),
    (
        r'ID  %%%==("1...." +regex)  %%:trim',
        ['ID'],
        [0, 1, 2],
        None,
        None,
        None,
    ),
    (
        r'ID  %%% == ("1...." +regex)  %%:trim',
        ['ID'],
        [0, 1, 2],
        None,
        None,
        None,
    ),
    (
        r'ID  %%%!=("3...." +regex)  %%:trim',
        ['ID'],
        [0, 1, 2, 3, 4, 5],
        None,
        None,
        None,
    ),
    (
        r'ID  %%%!=("3...." +regex)  %%:trim',
        ['ID'],
        [0, 1, 2, 3, 4, 5],
        None,
        None,
        None,
    ),
    (
        #two words with first letter capitalized and separated by a space
        r'name  %%%==("\b[A-Z][a-z]*\s[A-Z][a-z]*\b" +regex)  %%:trim',
        ['name'],
        [0, 1, 2, 3, 7],
        None,
        None,
        None,
    ),
    (
        #all lowercase
        r'name  %%%==("^[^A-Z]*$" +regex)  %%:trim',
        ['name'],
        [4],
        None,
        None,
        None,
    ),
    (
        #containing letters and numbers
        r'dose  %%%==("^(?=.*[a-zA-Z])(?=.*[0-9]).*$" +regex)  %%:trim',
        ['dose'],
        [0, 2, 3, 4, 5, 8, 10],
        None,
        None,
        None,
    ),


    #regex search
    (
        r'"bp systole"  %%%?(m +regex)  %%:trim',
        ['bp systole'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'"bp systole"  %%%?("\D" +regex)  %%:trim',
        ['bp systole'],
        [0, 2, 3, 4, 5, 6, 7],
        None,
        None,
        None,
    ),
    (
        r'"bp systole"  %%%?("\d" +regex)  %%:trim',
        ['bp systole'],
        [0, 1, 4, 5, 7, 9, 10],
        None,
        None,
        None,
    ),

    ])
def test_regex(code, cols, rows, vals, dtypes, message):
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
def test_typechecks(code, cols, rows, vals, dtypes, message):
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
        r'age  %%%==40  %%:trim',
        ['age'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'age  %%%==40  +int  %%:trim',
        ['age'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'age  %%%==40  +float  %%:trim',
        ['age'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'age  %%%==40  +num  %%:trim',
        ['age'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'age  %%%==40  +str  %%:trim',
        ['age'],
        [],
        None,
        None,
        None,
    ),

    ])
def test_typeflags(code, cols, rows, vals, dtypes, message):
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
        r"""
        diabetes  %%%:isunique  %%:trim
        %
        """,
        df.columns,
        [1, 2, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        diabetes  %%%:isfirst()  %%:trim
        %
        """,
        df.columns,
        [0, 1, 2, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        diabetes  %%%:islast()  %%:trim
        %
        """,
        df.columns,
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),

    ])
def test_uniqueness(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)
