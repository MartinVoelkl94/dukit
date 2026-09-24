
import pytest
import dukit as dk

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




@pytest.mark.parametrize('code, expected, message', [

    (
        r'"date of birth"  %%%1995.01.02  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%==1995.01.02  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%==1995_01_02  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="1995-01-02"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="1995/01/02"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="1995 01 02"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="1995-Jan-02"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="02-01-1995"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="02-Jan-1995"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="Jan-02-1995"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="02-01.1995"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="02 Jan-1995"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%%=="Jan/02_1995"  %%:trim',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"   .todatetime()   %%%==1995-01-02  %%:trim',
        df.loc[[0], ['date of birth']].map(dk.datetime),
        None,
    ),
    (
        r'"date of birth"   .todatetime   %%%<1950.01.01  %%:trim',
        df.loc[[10], ['date of birth']].map(dk.datetime),
        None,
    ),
    (
        r'"date of birth"   .todatetime   %%%>"1990/01/01"   &&&<"2000-01-01"  %%:trim',
        df.loc[[0, 1], ['date of birth']].map(dk.datetime),
        None,
    ),

    ])
def test_dates(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




@pytest.mark.parametrize('code, expected, message', [

    (
        r'age  %%%==30  %%:trim',
        df.loc[[1], ['age']],
        None
    ),
    (
        r'age  %%%30  %%:trim',
        df.loc[[1], ['age']],
        None
    ),
    (
        r'age  %%%==30  %%:trim',
        df.loc[[1], ['age']],
        None
    ),
    (
        r'age  %%%==30.0  %%:trim',
        df.loc[[1], ['age']],
        None
    ),
    (
        r'age  %%%==(30.0 +strict)  %%:trim',
        df.loc[[], ['age']],
        None
    ),
    (
        r'age  %%%>30  %%:trim',
        df.loc[[4, 10], ['age']],
        None
    ),
    (
        r'age  %%%>=30  %%:trim',
        df.loc[[1, 4, 10], ['age']],
        None
    ),
    (
        r'age  %%%<30  %%:trim',
        df.loc[[0], ['age']],
        None
    ),
    (
        r'age  %%%<=30  %%:trim',
        df.loc[[0, 1], ['age']],
        None
    ),
    (
        r'age  %%%!=30  %%:trim',
        df.loc[[0, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['age']],
        None
    ),
    (
        r'age  %%%!=30.0  %%:trim',
        df.loc[[0, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['age']],
        None
    ),
    (
        r'age  %%%!=(30 +strict)  %%:trim',
        df.loc[:, ['age']],
        None
    ),
    (
        r'age  %%%!=(30.0, +strict)  %%:trim',
        df.loc[:, ['age']],
        None
    ),
    (
        r'age  %%% !=30.0 +strict  %%:trim',
        df.loc[:, ['age']],
        None
    ),
    (
        r'age  %%%!>30  %%:trim',
        df.loc[[0, 1, 2, 3, 5, 6, 7, 8, 9], ['age']],
        None
    ),
    (
        r'age  %%%!>=30  %%:trim',
        df.loc[[0, 2, 3, 5, 6, 7, 8, 9], ['age']],
        None
    ),
    (
        r'age  %%%!<30  %%:trim',
        df.loc[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['age']],
        None
    ),
    (
        r'age  %%%!<=30  %%:trim',
        df.loc[[2, 3, 4, 5, 6, 7, 8, 9, 10], ['age']],
        None
    ),
    (
        r'weight  %%%>70  %%:trim',
        df.loc[[0, 7, 9], ['weight']],
        None
    ),
    (
        r'weight  %%%70  %%:trim',
        df.loc[[], ['weight']],
        None
    ),

    ])
def test_numeric(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




@pytest.mark.parametrize('code, expected, message', [

    #by evaluating python expressions
    (
        r'age  %%%:eval("isinstance(x, int)")  %%:trim',
        df.loc[[0, 10], ['age']],
        None
    ),


    #invert
    (
        r"""
        name
            %%%?j
            %%%:invert
            %%:trim
        """,
        df.loc[3:8, ['name']],
        None
    ),

    ])
def test_other(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




@pytest.mark.parametrize('code, expected, message', [

    #regex equality
    (
        r'ID  %%%==("1...." +regex)  %%:trim',
        df.loc[[0, 1, 2], ['ID']],
        None
    ),
    (
        r'ID  %%%("1...." +regex)  %%:trim',
        df.loc[[0, 1, 2], ['ID']],
        None
    ),
    (
        r'ID  %%%==("1...." +regex)  %%:trim',
        df.loc[[0, 1, 2], ['ID']],
        None
    ),
    (
        r'ID  %%% == ("1...." +regex)  %%:trim',
        df.loc[[0, 1, 2], ['ID']],
        None
    ),
    (
        r'ID  %%%!=("3...." +regex)  %%:trim',
        df.loc[[0, 1, 2, 3, 4, 5], ['ID']],
        None
    ),
    (
        r'ID  %%%!=("3...." +regex)  %%:trim',
        df.loc[[0, 1, 2, 3, 4, 5], ['ID']],
        None
    ),
    (
        #two words with first letter capitalized and separated by a space
        r'name  %%%==("\b[A-Z][a-z]*\s[A-Z][a-z]*\b" +regex)  %%:trim',
        df.loc[[0, 1, 2, 3, 7], ['name']],
        None
    ),
    (
        #all lowercase
        r'name  %%%==("^[^A-Z]*$" +regex)  %%:trim',
        df.loc[[4], ['name']],
        None
    ),
    (
        #containing letters and numbers
        r'dose  %%%==("^(?=.*[a-zA-Z])(?=.*[0-9]).*$" +regex)  %%:trim',
        df.loc[[0, 2, 3, 4, 5, 8, 10], ['dose']],
        None
    ),


    #regex search
    (
        r'"bp systole"  %%%?(m +regex)  %%:trim',
        df.loc[[4], ['bp systole']],
        None
    ),
    (
        r'"bp systole"  %%%?("\D" +regex)  %%:trim',
        df.loc[[0, 2, 3, 4, 5, 6, 7], ['bp systole']],
        None
    ),
    (
        r'"bp systole"  %%%?("\d" +regex)  %%:trim',
        df.loc[[0, 1, 4, 5, 7, 9, 10], ['bp systole']],
        None
    ),

    ])
def test_regex(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




@pytest.mark.parametrize('code, expected, message', [

    (
        r'name  %%%:isstr()  %%:trim',
        df.loc[:, ['name']],
        None
    ),
    (
        r'name  %%%!:isstr()  %%:trim',
        df.loc[[], ['name']],
        None
    ),
    (
        r'name  %%%:isnum()  %%:trim',
        df.loc[[], ['name']],
        None
    ),
    (
        r'name  %%%!:isnum()  %%:trim',
        df.loc[:, ['name']],
        None
    ),
    (
        r'name  %%%:isna()  %%:trim',
        df.loc[[], ['name']],
        None
    ),
    (
        r'name  %%%:!isna()  %%:trim',
        df.loc[:, ['name']],
        None
    ),

    (
        r'age   %%%:isint()  %%:trim',
        df.loc[[0, 1, 4, 10], ['age']],
        None
    ),
    (
        r'age   %%%:isint(+strict)  %%:trim',
        df.loc[[0, 10], ['age']],
        None
    ),
    (
        r'age   %%%:isfloat()  %%:trim',
        df.loc[[0, 1, 2, 4, 6, 10], ['age']],
        None
    ),
    (
        r'age   %%%:isfloat(+strict)  %%:trim',
        df.loc[[2], ['age']],
        None
    ),
    (
        r'age   %%%:isna()  %%:trim',
        df.loc[[2, 3, 6, 8], ['age']],
        None
    ),

    (
        r'weight  %%%:isint()  %%:trim',
        df.loc[[1, 9, 10], ['weight']],
        None
    ),
    (
        r'weight  %%%:isint(+strict)  %%:trim',
        df.loc[[10], ['weight']],
        None
    ),
    (
        r'weight  %%%:isfloat()  %%:trim',
        df.loc[[0, 1, 7, 9, 10], ['weight']],
        None
    ),
    (
        r'weight  %%%:isfloat(+strict)  %%:trim',
        df.loc[[0], ['weight']],
        None
    ),
    (
        r'weight  %%%:isnum()  %%:trim',
        df.loc[[0, 1, 4, 6, 7, 9, 10], ['weight']],
        None
    ),
    (
        r'weight  %%%:isnum(+strict)  %%:trim',
        df.loc[[0, 10], ['weight']],
        None
    ),
    (
        r'weight  %%%:isnum()  &&!:isna()  %%:trim',
        df.loc[[0, 1, 7, 9, 10], ['weight']],
        None
    ),

    (
        r'height       %%%:isbool()  %%:trim',
        df.loc[[6], ['height']],
        None
    ),
    (
        r'"bp diastole"  %%%:isbool()  %%:trim',
        df.loc[[9], ['bp diastole']],
        None
    ),
    (
        r'diabetes     %%%:isbool()  %%:trim',
        df.loc[[0, 1, 3, 4, 5, 6, 9, 10], ['diabetes']],
        None
    ),
    (
        r'diabetes     %%%:isbool(+strict)  %%:trim',
        df.loc[[0, 10], ['diabetes']],
        None
    ),

    (
        r'"date of birth"  %%%:isdate()  %%:trim',
        df.loc[:, ['date of birth']],
        None
    ),
    (
        r'"date of birth"  %%%:isdate()  +strict  %%:trim',
        df.loc[[0, 1, 5, 6], ['date of birth']],
        None
    ),
    (
        r'"date of birth"  %%%:isdatetime()  %%:trim',
        df.loc[:, ['date of birth']],
        None
    ),
    (
        r'"date of birth"  %%%:isdatetime()  +strict  %%:trim',
        df.loc[[0, 1, 5, 6], ['date of birth']],
        None
    ),

    (
        r'diabetes  %%%:isyn()  %%:trim',
        df.loc[[0, 1, 3, 4, 5, 6, 9, 10], ['diabetes']],
        None
    ),
    (
        r'diabetes  %%%:isna()  //:isyn()  %%:trim',
        df.loc[:, ['diabetes']],
        None
    ),

    (
        r'cholesterol  %%%:isna()  %%:trim',
        df.loc[[2, 4, 7, 9], ['cholesterol']],
        None
    ),
    (
        r'age  %%%:isna()  %%:trim',
        df.loc[[2, 3, 6, 8], ['age']],
        None
    ),
    (
        r'age  %%%:isna(+strict)  %%:trim',
        df.loc[[2, 3], ['age']],
        None
    ),

    (
        r'age  %%%:isnk()  %%:trim',
        df.loc[[7, 9], ['age']],
        None
    ),

    ])
def test_typechecks(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




@pytest.mark.parametrize('code, expected, message', [

    (
        r'age  %%%==40  %%:trim',
        df.loc[[4], ['age']],
        None
    ),
    (
        r'age  %%%==40  +int  %%:trim',
        df.loc[[4], ['age']],
        None
    ),
    (
        r'age  %%%==40  +float  %%:trim',
        df.loc[[4], ['age']],
        None
    ),
    (
        r'age  %%%==40  +num  %%:trim',
        df.loc[[4], ['age']],
        None
    ),
    (
        r'age  %%%==40  +str  %%:trim',
        df.loc[[], ['age']],
        None
    ),

    ])
def test_typeflags(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




@pytest.mark.parametrize('code, expected, message', [

    (
        r"""
        diabetes  %%%:isunique  %%:trim
        %
        """,
        df.loc[[1, 2, 4, 5, 6, 7, 8, 9, 10], :],
        None
    ),
    (
        r"""
        diabetes  %%%:isfirst()  %%:trim
        %
        """,
        df.loc[[0, 1, 2, 4, 5, 6, 7, 8, 9, 10], :],
        None
    ),
    (
        r"""
        diabetes  %%%:islast()  %%:trim
        %
        """,
        df.loc[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], :],
        None
    ),

    ])
def test_uniqueness(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)
