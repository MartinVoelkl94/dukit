
import pytest
import dukit as dk

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    )



params = []
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




params = [
    (
        r'id  == @ID',
        df.loc[:, ['ID']],
        None
    ),
    (
        r'id  == @id',
        df.loc[[], ['ID']],
        None
    ),
    (
        r'age   == @"bp systole"',
        df.loc[[8], ['age']],
        None
    ),
    (
        r"""
        age  /height  .tonum
        age  < height +colref
        """,
        df.loc[[0, 10], ['age']].astype('Int64'),
        None
    ),
    (
        r"""
        age  /height  .tonum
        age  < @height
        """,
        df.loc[[0, 10], ['age']].astype('Int64'),
        None
    ),
    (
        r"""
        age  /height  .tonum
        height  > @age
        """,
        df.loc[[0, 10], ['height']].astype('Int64'),
        None
    ),
    (
        r"""
        age  /height  .tonum
        age  <= @height
        """,
        df.loc[[0, 10], ['age']].astype('Int64'),
        None
    ),
    (
        r"""
        age  /height  .tonum
        height  >= @age
        """,
        df.loc[[0, 10], ['height']].astype('Int64'),
        None
    ),
    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_colref(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [
    (
        r'id  /name   ?j',
        df.loc[[0, 1, 2, 9, 10], ['ID', 'name']],
        None
    ),
    (
        r'id  /name   ?o',
        df.loc[[0, 2, 3, 6, 10], ['ID', 'name']],
        None
    ),
    (
        r'id  /name   ?jo',
        df.loc[[0, 2, 10], ['ID', 'name']],
        None
    ),
    (
        r'id  /name   ?(j, o)',
        df.loc[[0, 2, 10], ['ID', 'name']],
        None
    ),
    (
        r'id  /name   ?(j, o, +all)',
        df.loc[[0, 2, 10], ['ID', 'name']],
        None
    ),
    (
        r'id  /name   ?j  &&?o',
        df.loc[[0, 2, 10], ['ID', 'name']],
        None
    ),
    (
        r'id  /name   ?(j, o, +any)',
        df.loc[[0, 1, 2, 3, 6, 9, 10], ['ID', 'name']],
        None
    ),
    (
        r'id  /name   ?j  //?o',
        df.loc[[0, 1, 2, 3, 6, 9, 10], ['ID', 'name']],
        None
    ),
    (
        r'id  /name   ?j  &&?n',
        df.loc[[0, 1, 2, 10], ['ID', 'name']],
        None
    ),
    (
        r'height  /weight   :isnum',
        df.loc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['height', 'weight']],
        None
    ),
    (
        r'height  /weight   :isnum +strict',
        df.loc[[0, 8, 10], ['height', 'weight']],
        None
    ),
    (
        r'height  /weight   :isnum(+strict)',
        df.loc[[0, 8, 10], ['height', 'weight']],
        None
    ),
    (
        r'height  /weight   :isnum(+allcols)',
        df.loc[[0, 6, 9, 10], ['height', 'weight']],
        None
    ),
    (
        r'height  /weight   :isnum(+allcols +strict)',
        df.loc[[0, 10], ['height', 'weight']],
        None
    ),
    (
        r'height  /weight   :isnum(+allcols, +strict)',
        df.loc[[0, 10], ['height', 'weight']],
        None
    ),
    (
        r"""
        age
            %%>30
        age
            //<18
        """,
        df.loc[[0, 4, 10], ['age']],
        None
    ),
    (
        r"""
        age
            %%>30
            //<18
        """,
        df.loc[[0, 4, 10], ['age']],
        None
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_connect(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    (
        r'"date of birth"  %%1995.01.02',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%==1995.01.02',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%==1995_01_02',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="1995-01-02"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="1995/01/02"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="1995 01 02"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="1995-Jan-02"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="02-01-1995"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="02-Jan-1995"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="Jan-02-1995"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="02-01.1995"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="02 Jan-1995"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"  %%=="Jan/02_1995"',
        df.loc[[0], ['date of birth']],
        None,
    ),
    (
        r'"date of birth"   .todatetime()   %%==1995-01-02',
        df.loc[[0], ['date of birth']].map(dk.datetime),
        None,
    ),
    (
        r'"date of birth"   .todatetime   %%<1950.01.01',
        df.loc[[10], ['date of birth']].map(dk.datetime),
        None,
    ),
    (
        r'"date of birth"   %%%.todatetime()   %%>"1990/01/01"   &&<"2000-01-01"',
        df.loc[[0, 1], ['date of birth']].map(dk.datetime),
        None,
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_dates(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    (
        r'%% == (3 +index)',
        df.iloc[[3], :],
        None,
    ),
    (
        r'%% > (5 +index)',
        df.iloc[6:, :],
        None,
    ),
    (
        r'%% < (5 +index)',
        df.iloc[:5, :],
        None,
    ),
    (
        r'%% >= (5 +index)',
        df.iloc[5:, :],
        None,
    ),
    (
        r'%% <= (5 +index)',
        df.iloc[:6, :],
        None,
    ),
    (
        r'%% != (5 +index)',
        df.iloc[[0, 1, 2, 3, 4, 6, 7, 8, 9, 10], :],
        None,
    ),
    (
        r'%% == (5 +index)',
        df.iloc[[5], :],
        None,
    ),
    (
        r'%% > (5 +index)  && < (8 +index)',
        df.iloc[6:8, :],
        None,
    ),
    (
        r'%% > (5 +index)  && < (8 +index)  && != (6 +index)',
        df.iloc[[7], :],
        None,
    ),
    (
        r'%% > (5 +index)  && < (8 +index)  && != (6 +index)  && != (7 +index)',
        df.iloc[[], :],
        None,
    ),
    (
        r'%% > (5 +index)  && < (8 +index)  && != (6, 7 +index +all)',
        df.iloc[[], :],
        None,
    ),
    (
        r'%% ? (1 +index)',
        df.iloc[[1, 10], :],
        None,
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_index(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)





params = [

    (
        r'age  ==30',
        df.loc[[1], ['age']],
        None
    ),
    (
        r'age  %%30',
        df.loc[[1], ['age']],
        None
    ),
    (
        r'age  %%==30',
        df.loc[[1], ['age']],
        None
    ),
    (
        r'age  %%==30.0',
        df.loc[[1], ['age']],
        None
    ),
    (
        r'age  %%==(30.0 +strict)',
        df.loc[[], ['age']],
        None
    ),
    (
        r'age  %%>30',
        df.loc[[4, 10], ['age']],
        None
    ),
    (
        r'age  %%>=30',
        df.loc[[1, 4, 10], ['age']],
        None
    ),
    (
        r'age  %%<30',
        df.loc[[0], ['age']],
        None
    ),
    (
        r'age  %%<=30',
        df.loc[[0, 1], ['age']],
        None
    ),
    (
        r'age  %%!=30',
        df.loc[[0, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['age']],
        None
    ),
    (
        r'age  %%!=30.0',
        df.loc[[0, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['age']],
        None
    ),
    (
        r'age  %%!=(30 +strict)',
        df.loc[:, ['age']],
        None
    ),
    (
        r'age  %%!=(30.0, +strict)',
        df.loc[:, ['age']],
        None
    ),
    (
        r'age  %% !=30.0 +strict',
        df.loc[:, ['age']],
        None
    ),
    (
        r'age  %%!>30',
        df.loc[[0, 1, 2, 3, 5, 6, 7, 8, 9], ['age']],
        None
    ),
    (
        r'age  %%!>=30',
        df.loc[[0, 2, 3, 5, 6, 7, 8, 9], ['age']],
        None
    ),
    (
        r'age  %%!<30',
        df.loc[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['age']],
        None
    ),
    (
        r'age  %%!<=30',
        df.loc[[2, 3, 4, 5, 6, 7, 8, 9, 10], ['age']],
        None
    ),
    (
        r'weight  %%>70',
        df.loc[[0, 7, 9], ['weight']],
        None
    ),
    (
        r'weight  %%70',
        df.loc[[], ['weight']],
        None
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_numeric(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    #by evaluating python expressions
    (
        r'age  :eval("isinstance(x, int)")',
        df.loc[[0, 10], ['age']],
        None
    ),


    #invert
    (
        r"""
        name
            ?j
            :invert
        """,
        df.loc[3:8, ['name']],
        None
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_other(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    #regex equality
    (
        r'ID  ==("1...." +regex)',
        df.loc[[0, 1, 2], ['ID']],
        None
    ),
    (
        r'ID  %%("1...." +regex)',
        df.loc[[0, 1, 2], ['ID']],
        None
    ),
    (
        r'ID  %%==("1...." +regex)',
        df.loc[[0, 1, 2], ['ID']],
        None
    ),
    (
        r'ID  %% == ("1...." +regex)',
        df.loc[[0, 1, 2], ['ID']],
        None
    ),
    (
        r'ID  %%!=("3...." +regex)',
        df.loc[[0, 1, 2, 3, 4, 5], ['ID']],
        None
    ),
    (
        r'ID  %%!=("3...." +regex)',
        df.loc[[0, 1, 2, 3, 4, 5], ['ID']],
        None
    ),
    (
        #two words with first letter capitalized and separated by a space
        r'name  %%==("\b[A-Z][a-z]*\s[A-Z][a-z]*\b" +regex)',
        df.loc[[0, 1, 2, 3, 7], ['name']],
        None
    ),
    (
        #all lowercase
        r'name  %%==("^[^A-Z]*$" +regex)',
        df.loc[[4], ['name']],
        None
    ),
    (
        #containing letters and numbers
        r'dose  %%==("^(?=.*[a-zA-Z])(?=.*[0-9]).*$" +regex)',
        df.loc[[0, 2, 3, 4, 5, 8, 10], ['dose']],
        None
    ),


    #regex search
    (
        r'"bp systole"  %%?(m +regex)',
        df.loc[[4], ['bp systole']],
        None
    ),
    (
        r'"bp systole"  %%?("\D" +regex)',
        df.loc[[0, 2, 3, 4, 5, 6, 7], ['bp systole']],
        None
    ),
    (
        r'"bp systole"  %%?("\d" +regex)',
        df.loc[[0, 1, 4, 5, 7, 9, 10], ['bp systole']],
        None
    ),
    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_regex(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    (
        r'name  %%:isstr()',
        df.loc[:, ['name']],
        None
    ),
    (
        r'name  %%!:isstr()',
        df.loc[[], ['name']],
        None
    ),
    (
        r'name  %%:isnum()',
        df.loc[[], ['name']],
        None
    ),
    (
        r'name  %%!:isnum()',
        df.loc[:, ['name']],
        None
    ),
    (
        r'name  %%:isna()',
        df.loc[[], ['name']],
        None
    ),
    (
        r'name  %%:!isna()',
        df.loc[:, ['name']],
        None
    ),

    (
        r'age   %%:isint()',
        df.loc[[0, 1, 4, 10], ['age']],
        None
    ),
    (
        r'age   %%:isint(+strict)',
        df.loc[[0, 10], ['age']],
        None
    ),
    (
        r'age   %%:isfloat()',
        df.loc[[0, 1, 2, 4, 6, 10], ['age']],
        None
    ),
    (
        r'age   %%:isfloat(+strict)',
        df.loc[[2], ['age']],
        None
    ),
    (
        r'age   %%:isna()',
        df.loc[[2, 3, 6, 8], ['age']],
        None
    ),

    (
        r'weight  %%:isint()',
        df.loc[[1, 9, 10], ['weight']],
        None
    ),
    (
        r'weight  %%:isint(+strict)',
        df.loc[[10], ['weight']],
        None
    ),
    (
        r'weight  %%:isfloat()',
        df.loc[[0, 1, 7, 9, 10], ['weight']],
        None
    ),
    (
        r'weight  %%:isfloat(+strict)',
        df.loc[[0], ['weight']],
        None
    ),
    (
        r'weight  %%:isnum()',
        df.loc[[0, 1, 4, 6, 7, 9, 10], ['weight']],
        None
    ),
    (
        r'weight  %%:isnum(+strict)',
        df.loc[[0, 10], ['weight']],
        None
    ),
    (
        r'weight  %%:isnum()  &&!:isna()',
        df.loc[[0, 1, 7, 9, 10], ['weight']],
        None
    ),

    (
        r'height       %%:isbool()',
        df.loc[[6], ['height']],
        None
    ),
    (
        r'"bp diastole"  %%:isbool()',
        df.loc[[9], ['bp diastole']],
        None
    ),
    (
        r'diabetes     %%:isbool()',
        df.loc[[0, 1, 3, 4, 5, 6, 9, 10], ['diabetes']],
        None
    ),
    (
        r'diabetes     %%:isbool(+strict)',
        df.loc[[0, 10], ['diabetes']],
        None
    ),

    (
        r'"date of birth"  %%:isdate()',
        df.loc[:, ['date of birth']],
        None
    ),
    (
        r'"date of birth"  %%:isdate()  +strict',
        df.loc[[0, 1, 5, 6], ['date of birth']],
        None
    ),
    (
        r'"date of birth"  %%:isdatetime()',
        df.loc[:, ['date of birth']],
        None
    ),
    (
        r'"date of birth"  %%:isdatetime()  +strict',
        df.loc[[0, 1, 5, 6], ['date of birth']],
        None
    ),

    (
        r'diabetes  %%:isyn()',
        df.loc[[0, 1, 3, 4, 5, 6, 9, 10], ['diabetes']],
        None
    ),
    (
        r'diabetes  %%:isna()  //:isyn()',
        df.loc[:, ['diabetes']],
        None
    ),

    (
        r'cholesterol  %%:isna()',
        df.loc[[2, 4, 7, 9], ['cholesterol']],
        None
    ),
    (
        r'age  %%:isna()',
        df.loc[[2, 3, 6, 8], ['age']],
        None
    ),
    (
        r'age  %%:isna(+strict)',
        df.loc[[2, 3], ['age']],
        None
    ),

    (
        r'age  %%:isnk()',
        df.loc[[7, 9], ['age']],
        None
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_typechecks(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    (
        r'age  ==40',
        df.loc[[4], ['age']],
        None
    ),
    (
        r'age  ==40  +int',
        df.loc[[4], ['age']],
        None
    ),
    (
        r'age  ==40  +float',
        df.loc[[4], ['age']],
        None
    ),
    (
        r'age  ==40  +num',
        df.loc[[4], ['age']],
        None
    ),
    (
        r'age  ==40  +str',
        df.loc[[], ['age']],
        None
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_typeflags(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    (
        r"""
        diabetes  :isunique
        %
        """,
        df.loc[[1, 2, 4, 5, 6, 7, 8, 9, 10], :],
        None
    ),
    (
        r"""
        diabetes  :isfirst()
        %
        """,
        df.loc[[0, 1, 2, 4, 5, 6, 7, 8, 9, 10], :],
        None
    ),
    (
        r"""
        diabetes  %%:islast()
        %
        """,
        df.loc[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], :],
        None
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_uniqueness(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)
