
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
        r'id  == @ID',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'id  == @id',
        ['ID'],
        [],
        None,
        None,
        None,
    ),
    (
        r'age   == @"bp systole"',
        ['age'],
        [8],
        None,
        None,
        None,
    ),
    (
        r"""
        age  /height  .tonum
        age  < height +colref
        """,
        ['age'],
        [0, 10],
        None,
        ['Int64'],
        None,
    ),
    (
        r"""
        age  /height  .tonum
        age  < @height
        """,
        ['age'],
        [0, 10],
        None,
        ['Int64'],
        None,
    ),
    (
        r"""
        age  /height  .tonum
        height  > @age
        """,
        ['height'],
        [0, 10],
        None,
        ['Int64'],
        None,
    ),
    (
        r"""
        age  /height  .tonum
        age  <= @height
        """,
        ['age'],
        [0, 10],
        None,
        ['Int64'],
        None,
    ),
    (
        r"""
        age  /height  .tonum
        height  >= @age
        """,
        ['height'],
        [0, 10],
        None,
        ['Int64'],
        None,
    ),

    ])
def test_colref(code, cols, rows, vals, dtypes, message):
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
        r'id  /name   ?j',
        ['ID', 'name'],
        [0, 1, 2, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'id  /name   ?o',
        ['ID', 'name'],
        [0, 2, 3, 6, 10],
        None,
        None,
        None,
    ),
    (
        r'id  /name   ?jo',
        ['ID', 'name'],
        [0, 2, 10],
        None,
        None,
        None,
    ),
    (
        r'id  /name   ?(j, o)',
        ['ID', 'name'],
        [0, 2, 10],
        None,
        None,
        None,
    ),
    (
        r'id  /name   ?(j, o, +all)',
        ['ID', 'name'],
        [0, 2, 10],
        None,
        None,
        None,
    ),
    (
        r'id  /name   ?j  &&?o',
        ['ID', 'name'],
        [0, 2, 10],
        None,
        None,
        None,
    ),
    (
        r'id  /name   ?(j, o, +any)',
        ['ID', 'name'],
        [0, 1, 2, 3, 6, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'id  /name   ?j  //?o',
        ['ID', 'name'],
        [0, 1, 2, 3, 6, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'id  /name   ?j  &&?n',
        ['ID', 'name'],
        [0, 1, 2, 10],
        None,
        None,
        None,
    ),
    (
        r'height  /weight   :isnum',
        ['height', 'weight'],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'height  /weight   :isnum +strict',
        ['height', 'weight'],
        [0, 8, 10],
        None,
        None,
        None,
    ),
    (
        r'height  /weight   :isnum(+strict)',
        ['height', 'weight'],
        [0, 8, 10],
        None,
        None,
        None,
    ),
    (
        r'height  /weight   :isnum(+allcols)',
        ['height', 'weight'],
        [0, 6, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'height  /weight   :isnum(+allcols +strict)',
        ['height', 'weight'],
        [0, 10],
        None,
        None,
        None,
    ),
    (
        r'height  /weight   :isnum(+allcols, +strict)',
        ['height', 'weight'],
        [0, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        age
            %%>30
        age
            //<18
        """,
        ['age'],
        [0, 4, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        age
            %%>30
            //<18
        """,
        ['age'],
        [0, 4, 10],
        None,
        None,
        None,
    ),

    ])
def test_connect(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r'"date of birth"  %%1995.01.02',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%==1995.01.02',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%==1995_01_02',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="1995-01-02"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="1995/01/02"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="1995 01 02"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="1995-Jan-02"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="02-01-1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="02-Jan-1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="Jan-02-1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="02-01.1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="02 Jan-1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"  %%=="Jan/02_1995"',
        ['date of birth'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'"date of birth"   .todatetime()   %%==1995-01-02',
        ['date of birth'],
        [0],
        None,
        ['datetime64[us]'],
        None,
    ),
    (
        r'"date of birth"   .todatetime   %%<1950.01.01',
        ['date of birth'],
        [10],
        None,
        ['datetime64[us]'],
        None,
    ),
    (
        r'"date of birth"   %%%.todatetime()   %%>"1990/01/01"   &&<"2000-01-01"',
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
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #by evaluating python expressions
    (
        r'age  :eval("isinstance(x, int)")',
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

    (
        r'%% == (3 +index)',
        df.columns,
        [3],
        None,
        None,
        None,
    ),
    (
        r'%% > (5 +index)',
        df.columns,
        [6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'%% < (5 +index)',
        df.columns,
        [0, 1, 2, 3, 4],
        None,
        None,
        None,
    ),
    (
        r'%% >= (5 +index)',
        df.columns,
        [5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'%% <= (5 +index)',
        df.columns,
        [0, 1, 2, 3, 4, 5],
        None,
        None,
        None,
    ),
    (
        r'%% != (5 +index)',
        df.columns,
        [0, 1, 2, 3, 4, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'%% == (5 +index)',
        df.columns,
        [5],
        None,
        None,
        None,
    ),
    (
        r'%% > (5 +index)  && < (8 +index)',
        df.columns,
        [6, 7],
        None,
        None,
        None,
    ),
    (
        r'%% > (5 +index)  && < (8 +index)  && != (6 +index)',
        df.columns,
        [7],
        None,
        None,
        None,
    ),
    (
        r'%% > (5 +index)  && < (8 +index)  && != (6 +index)  && != (7 +index)',
        df.columns,
        [],
        None,
        None,
        None,
    ),
    (
        r'%% > (5 +index)  && < (8 +index)  && != (6, 7 +index +all)',
        df.columns,
        [],
        None,
        None,
        None,
    ),
    (
        r'%% ? (1 +index)',
        df.columns,
        [1, 10],
        None,
        None,
        None,
    ),

    ])
def test_index(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #by evaluating python expressions
    (
        r'age  :eval("isinstance(x, int)")',
        ['age'],
        [0, 10],
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
        r'age  ==30',
        ['age'],
        [1],
        None,
        None,
        None,
    ),
    (
        r'age  %%30',
        ['age'],
        [1],
        None,
        None,
        None,
    ),
    (
        r'age  %%==30',
        ['age'],
        [1],
        None,
        None,
        None,
    ),
    (
        r'age  %%==30.0',
        ['age'],
        [1],
        None,
        None,
        None,
    ),
    (
        r'age  %%==(30.0 +strict)',
        ['age'],
        [],
        None,
        None,
        None,
    ),
    (
        r'age  %%>30',
        ['age'],
        [4, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%>=30',
        ['age'],
        [1, 4, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%<30',
        ['age'],
        [0],
        None,
        None,
        None,
    ),
    (
        r'age  %%<=30',
        ['age'],
        [0, 1],
        None,
        None,
        None,
    ),
    (
        r'age  %%!=30',
        ['age'],
        [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%!=30.0',
        ['age'],
        [0, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%!=(30 +strict)',
        ['age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'age  %%!=(30.0, +strict)',
        ['age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'age  %% !=30.0 +strict',
        ['age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'age  %%!>30',
        ['age'],
        [0, 1, 2, 3, 5, 6, 7, 8, 9],
        None,
        None,
        None,
    ),
    (
        r'age  %%!>=30',
        ['age'],
        [0, 2, 3, 5, 6, 7, 8, 9],
        None,
        None,
        None,
    ),
    (
        r'age  %%!<30',
        ['age'],
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'age  %%!<=30',
        ['age'],
        [2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'weight  %%>70',
        ['weight'],
        [0, 7, 9],
        None,
        None,
        None,
    ),
    (
        r'weight  %%70',
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
        r'ID  ==("1...." +regex)',
        ['ID'],
        [0, 1, 2],
        None,
        None,
        None,
    ),
    (
        r'ID  %%("1...." +regex)',
        ['ID'],
        [0, 1, 2],
        None,
        None,
        None,
    ),
    (
        r'ID  %%==("1...." +regex)',
        ['ID'],
        [0, 1, 2],
        None,
        None,
        None,
    ),
    (
        r'ID  %% == ("1...." +regex)',
        ['ID'],
        [0, 1, 2],
        None,
        None,
        None,
    ),
    (
        r'ID  %%!=("3...." +regex)',
        ['ID'],
        [0, 1, 2, 3, 4, 5],
        None,
        None,
        None,
    ),
    (
        r'ID  %%!=("3...." +regex)',
        ['ID'],
        [0, 1, 2, 3, 4, 5],
        None,
        None,
        None,
    ),
    (
        #two words with first letter capitalized and separated by a space
        r'name  %%==("\b[A-Z][a-z]*\s[A-Z][a-z]*\b" +regex)',
        ['name'],
        [0, 1, 2, 3, 7],
        None,
        None,
        None,
    ),
    (
        #all lowercase
        r'name  %%==("^[^A-Z]*$" +regex)',
        ['name'],
        [4],
        None,
        None,
        None,
    ),
    (
        #containing letters and numbers
        r'dose  %%==("^(?=.*[a-zA-Z])(?=.*[0-9]).*$" +regex)',
        ['dose'],
        [0, 2, 3, 4, 5, 8, 10],
        None,
        None,
        None,
    ),


    #regex search
    (
        r'"bp systole"  %%?(m +regex)',
        ['bp systole'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'"bp systole"  %%?("\D" +regex)',
        ['bp systole'],
        [0, 2, 3, 4, 5, 6, 7],
        None,
        None,
        None,
    ),
    (
        r'"bp systole"  %%?("\d" +regex)',
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
        r'age  ==40',
        ['age'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'age  ==40  +int',
        ['age'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'age  ==40  +float',
        ['age'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'age  ==40  +num',
        ['age'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'age  ==40.0  +num',
        ['age'],
        [4],
        None,
        None,
        None,
    ),
    (
        r'age  ==40  +str',
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
        diabetes  :isunique
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
        diabetes  :isfirst()
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
        diabetes  %%:islast()
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
