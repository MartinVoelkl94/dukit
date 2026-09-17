
import pytest
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    )



params = []
df = get_df()

tstamp = pd.Timestamp('2024-01-01')
def get_df_types():
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
    return df_types

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

    #equals getter
    ('', df.columns, None),
    ('ID', ['ID'], None),
    (' ID', ['ID'], None),
    ('ID ', ['ID'], None),
    (' ID ', ['ID'], None),

    ('%', df.columns, None),
    ('%ID', ['ID'], None),
    ('% ID', ['ID'], None),
    ('%ID ', ['ID'], None),
    ('% ID ', ['ID'], None),

    ('%==ID', ['ID'], None),
    ('% ==ID', ['ID'], None),
    ('%== ID', ['ID'], None),
    ('%== ID ', ['ID'], None),
    ('% == ID ', ['ID'], None),

    ("""ID""", ['ID'], None),
    ("""%ID""", ['ID'], None),
    (""" ID """, ['ID'], None),
    ("""%==ID""", ['ID'], None),
    ("""% == ID""", ['ID'], None),

    ('"date of birth"', ['date of birth'], None),
    ('%"date of birth"', ['date of birth'], None),
    ('"date of birth"    /age', ['date of birth', 'age'], None),
    ('"date of birth"    / ==age', ['date of birth', 'age'], None),
    ('%"date of birth"    / ==age', ['date of birth', 'age'], None),

    (
        """ID
        """,
        ['ID'],
        None
    ),

    (
        """
        ID""",
        ['ID'],
        None
    ),

    (
        """
        ID
        """,
        ['ID'],
        None
    ),

    (
        r"""ID""",
        ['ID'],
        None
    ),

    (
        r"""ID
        """,
        ['ID'],
        None
    ),

    (
        r"""
        ID""",
        ['ID'],
        None
    ),

    (
        r"""
        ID
        """,
        ['ID'],
        None
    ),


    #contains getter
    ('%?bp', ['bp systole', 'bp diastole'], None),
    (
        '%?I',
        [
            'ID',
            'date of birth',
            'height',
            'weight',
            'bp diastole',
            'diabetes',
        ],
        None
    ),
    ('%!?I', ['name', 'age', 'gender', 'bp systole', 'cholesterol', 'dose'], None),
    ('%?I, +strict', ['ID'], None),
    ('%?I +strict)', ['ID'], None),
    ('%?(I +strict)', ['ID'], None),
    ('%?(I, +strict)', ['ID'], None),


    ('%:eval("len(x)==2")', ['ID'], None),
    ('%:eval("x")', df.columns.tolist(), None),
    ('%:eval("True")', df.columns.tolist(), None),
    ("""%:eval(" 'ag' in x ")""", ['age'], None),


    #invert
    (
        'id  %:invert',
        [
            'name',
            'date of birth',
            'age',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
        ],
        None,
    ),
    (
        'name  /gender  %:invert',
        [
            'ID',
            'date of birth',
            'age',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
        ],
        None,
    ),

    ]
@pytest.mark.parametrize('code, expected_cols, message', params)
def test_basic(code, expected_cols: list[str], message):
    result = df.dk.qr(code).result
    expected = get_df().loc[:, expected_cols]
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    ('%?bp   /diabetes', ['bp systole', 'bp diastole', 'diabetes'], None),
    (
        '%?bp   /diabetes   /cholesterol',
        [
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
        ],
        None
    ),
    (
        '%?bp /cholesterol/diabetes',
        [
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
        ],
        None
    ),
    (
        'cholesterol/diabetes/?bp',
        [
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
        ],
        None
    ),
    ('%?bp   & ?systole', ['bp systole'], None),
    ('%?bp   & !?systole', ['bp diastole'], None),
    ('%?bp   & !?systole   & ?diastole', ['bp diastole'], None),
    ('%?bp   & !?systole   / ?ID', ['ID', 'bp diastole'], None),

    ]
@pytest.mark.parametrize('code, expected_cols, message', params)
def test_connect(code, expected_cols: list[str], message):
    result = df.dk.qr(code).result
    expected = get_df().loc[:, expected_cols]
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    #negate
    (
        '%!="date of birth"',
        [
            'ID',
            'name',
            'age',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
        ],
        None
    ),


    #strict
    ('%==(ID, +strict)', ['ID'], None),
    ('% ==(ID, +strict)', ['ID'], None),
    ('%== (ID, +strict)', ['ID'], None),
    ('% == (ID, +strict)', ['ID'], None),
    ('%==(id, +strict)', [], 'WARNING: no cols fulfill the condition'),

    ('%==ID +strict', ['ID'], None),
    ('% ==ID +strict', ['ID'], None),
    ('%== ID +strict', ['ID'], None),
    ('% == ID +strict', ['ID'], None),
    ('%==id +strict', [], 'WARNING: no cols fulfill the condition'),


    #regex
    ('ID +regex', ['ID'], None),
    ('%=="." +regex', [], r'WARNING: no cols fulfill the condition'),
    ('%==".." +regex', ['ID'], None),

    ('%? ID +regex', ['ID'], None),
    (
        '%? "e." +regex',
        [
            'date of birth',
            'gender',
            'height',
            'weight',
            'cholesterol',
            'diabetes'
        ],
        None
    ),
    (
        '%? "e.o" +regex',
        [
            'date of birth',
            'cholesterol',
        ],
        None
    ),

    ('%(ID, +regex)', ['ID'], None),
    ('%==(".", +regex)', [], r'WARNING: no cols fulfill the condition'),
    ('%==("..", +regex)', ['ID'], None),

    ('%? (ID, +regex)', ['ID'], None),
    (
        '%? ("e.", +regex)',
        [
            'date of birth',
            'gender',
            'height',
            'weight',
            'cholesterol',
            'diabetes'
        ],
        None
    ),
    (
        '%? ("e.o", +regex)',
        [
            'date of birth',
            'cholesterol',
        ],
        None
    ),

    ]
@pytest.mark.parametrize('code, expected_cols, message', params)
def test_flags(code, expected_cols: list[str], message):
    result = df.dk.qr(code).result
    expected = get_df().loc[:, expected_cols]
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    (
        r'% == (3 +index)',
        df.iloc[:, [3]],
        None,
    ),
    (
        r'% > (5 +index)',
        df.iloc[:, 6:],

        None,
    ),
    (
        r'% < (5 +index)',
        df.iloc[:, :5],
        None,
    ),
    (
        r'% >= (5 +index)',
        df.iloc[:, 5:],
        None,
    ),
    (
        r'% <= (5 +index)',
        df.iloc[:, :6],
        None,
    ),
    (
        r'% != (5 +index)',
        df.iloc[:, [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11]],
        None,
    ),
    (
        r'% == (5 +index)',
        df.iloc[:, [5]],
        None,
    ),
    (
        r'% > (5 +index)  & < (8 +index)',
        df.iloc[:, 6:8],
        None,
    ),
    (
        r'% > (5 +index)  & < (8 +index)  & != (6 +index)',
        df.iloc[:, [7]],
        None,
    ),
    (
        r'% > (5 +index)  & < (8 +index)  & != (6 +index)  & != (7 +index)',
        df.iloc[:, []],
        None,
    ),
    (
        r'% > (5 +index)  & < (8 +index)  & != (6, 7 +index +all)',
        df.iloc[:, []],
        None,
    ),
    (
        r'% ? (1 +index)',
        df.iloc[:, [1, 10, 11]],
        None,
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_header(code, expected, message):
    result = df.dk.qr(code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    ('%(ID)', ['ID'], None),
    ('%==(ID)', ['ID'], None),

    ('%(ID, age, +any)', ['ID', 'age'], None),
    ('%==(ID, age, +any)', ['ID', 'age'], None),

    ('%(ID age, +any)', ['ID', 'age'], None),
    ('%==(ID age, +any)', ['ID', 'age'], None),

    ]
@pytest.mark.parametrize('code, expected_cols, message', params)
def test_lists(code, expected_cols: list[str], message):
    result = df.dk.qr(code).result
    expected = get_df().loc[:, expected_cols]
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



params = [
    ('%:isstr', ['a', 'unknown'], None),
    ('%:isint', [0, True], None),
    ('%:isfloat', [0, 0.1, True], None),
    ('%:isfloat +strict', [0.1], None),
    ('%:isnum', [0, 0.1, tstamp, True, None], None),
    ('%:isbool', [0, True], None),
    ('%:isdatetime', [tstamp], None),
    ('%:isdate', [tstamp], None),
    ('%:isna', [None], None),
    ('%:isnk', ['unknown'], None),
    ('%:isyn', [0, True], None),
    ('%:isunique', [0, 0.1, tstamp, True, 'unknown', None], None),
    ('%!:isunique', ['a'], None),
    ('%:isfirst', ['a', 0, 0.1, tstamp, True, 'unknown', None], None),
    ('%:islast', [0, 0.1, tstamp, True, 'unknown', None, 'a'], None),
    ]
@pytest.mark.parametrize('code, expected_cols, message', params)
def test_types(code, expected_cols: list[str], message):

    df_types = get_df_types()
    result = df_types.dk.qr(code).result

    if code == '%:isstr':
        result = result[['a', 'unknown']]  #qlang reorders, while pd does not
    elif code == '%:isfirst':
        df_types = df_types.iloc[:, :7]
    elif code == '%:islast':
        df_types = df_types.iloc[:, 1:]

    expected = df_types.loc[:, expected_cols]
    assert_frame_equal(result, expected)
    if message:
        check_message(message)
