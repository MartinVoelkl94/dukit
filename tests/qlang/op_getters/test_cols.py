
import pytest

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    qr,
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
def test_cols(code, expected_cols: list[str], message):
    result = qr(df, code).result
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
def test_cols_connect(code, expected_cols: list[str], message):
    result = qr(df, code).result
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
def test_cols_flags(code, expected_cols: list[str], message):
    result = qr(df, code).result
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
def test_cols_index(code, expected, message):
    result = qr(df, code).result
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
def test_cols_lists(code, expected_cols: list[str], message):
    result = qr(df, code).result
    expected = get_df().loc[:, expected_cols]
    assert_frame_equal(result, expected)
    if message:
        check_message(message)
