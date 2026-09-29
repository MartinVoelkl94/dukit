
import pytest
import pandas as pd

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    )



tstamp = pd.Timestamp('2024-01-01')
cols1 = [
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
    ]
cols2 = [
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
    ]
cols3 = [
    'ID',
    'name',
    'gender',
    'height',
    'weight',
    'bp systole',
    'bp diastole',
    'cholesterol',
    'diabetes',
    'dose',
    ]

df = get_df()

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
        r'%?bp   /diabetes',
        [
            'bp systole',
            'bp diastole',
            'diabetes',
        ],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?bp   /diabetes   /cholesterol',
        [
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
        ],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?bp /cholesterol/diabetes',
        [
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
        ],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'cholesterol/diabetes/?bp',
        [
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
        ],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?bp   & ?systole',
        ['bp systole'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?bp   & !?systole',
        ['bp diastole'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?bp   & !?systole   & ?diastole',
        ['bp diastole'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?bp   & !?systole   / ?ID',
        ['ID', 'bp diastole'],
        df.index,
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
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #contains substring
    (
        r'%?bp',
        ['bp systole', 'bp diastole'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?I',
        [
            'ID',
            'date of birth',
            'height',
            'weight',
            'bp diastole',
            'diabetes',
        ],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!?I',
        [
            'name',
            'age',
            'gender',
            'bp systole',
            'cholesterol',
            'dose',
        ],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?I, +strict',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?I +strict)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?(I +strict)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%?(I, +strict)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%:eval("len(x)==2")',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%:eval("x")',
        df.columns,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%:eval("True")',
        df.columns,
        df.index,
        None,
        None,
        None,
    ),
    (
        """%:eval(" 'ag' in x ")""",
        ['age'],
        df.index,
        None,
        None,
        None,
    ),

    ])
def test_contains(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #equality
    (
        r'',
        df.columns,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'ID',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r' ID',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'ID ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r' ID ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%',
        df.columns,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%ID',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ID',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%ID ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ID ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%==ID',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ==ID',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%== ID',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%== ID ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% == ID ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        """ID""",
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        """%ID""",
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        """ ID """,
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        """%==ID""",
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        """% == ID""",
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'"date of birth"',
        ['date of birth'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%"date of birth"',
        ['date of birth'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'"date of birth"    /age',
        ['date of birth', 'age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'"date of birth"    / ==age',
        ['date of birth', 'age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%"date of birth"    / ==age',
        ['date of birth', 'age'],
        df.index,
        None,
        None,
        None,
    ),

    (
        """ID
        """,
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        """
        ID""",
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        """
        ID
        """,
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r"""ID""",
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r"""ID
        """,
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r"""
        ID""",
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r"""
        ID
        """,
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    ])
def test_equality(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #strict
    (
        r'%==(ID, +strict)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ==(ID, +strict)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%== (ID, +strict)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% == (ID, +strict)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%==(id, +strict)',
        [],
        df.index,
        None,
        None,
        'WARNING: no cols fulfill the condition',
    ),

    (
        r'%==ID +strict',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ==ID +strict',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%== ID +strict',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% == ID +strict',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%==id +strict',
        [],
        df.index,
        None,
        None,
        'WARNING: no cols fulfill the condition',
    ),


    #regex
    (
        r'ID +regex',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%=="." +regex',
        [],
        df.index,
        None,
        None,
        r'WARNING: no cols fulfill the condition',
    ),
    (
        r'%==".." +regex',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%? ID +regex',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%? "e." +regex',
        [
            'date of birth',
            'gender',
            'height',
            'weight',
            'cholesterol',
            'diabetes'
        ],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%? "e.o" +regex',
        [
            'date of birth',
            'cholesterol',
        ],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%(ID, +regex)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%==(".", +regex)',
        [],
        df.index,
        None,
        None,
        r'WARNING: no cols fulfill the condition',
    ),
    (
        r'%==("..", +regex)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%? (ID, +regex)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%? ("e.", +regex)',
        [
            'date of birth',
            'gender',
            'height',
            'weight',
            'cholesterol',
            'diabetes'
        ],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%? ("e.o", +regex)',
        [
            'date of birth',
            'cholesterol',
        ],
        df.index,
        None,
        None,
        None,
    ),

    ])
def test_flags(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #prefix
    (
        r'§0',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§ 0',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§0 ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r' § 0 ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'§ 0',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§  0',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§ 0 ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r' § 0 ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%§0',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ 0',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§0 ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ 0 ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%§==0',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ ==0',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§== 0',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ == 0 ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ == 0 ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§  == 0 ',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),



    #postfix
    (
        r'0+index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r' 0+index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'0 +index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r' 0 +index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%0+index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% 0+index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%0 +index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% 0 +index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%==0+index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ==0+index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%== 0+index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% == 0 +index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% == 0 +index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%  == 0 +index',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    ])
def test_flags_index(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #prefix
    (
        r'!ID',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'! ID',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'!ID ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r' !ID ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%!ID',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%! ID',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!ID ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% !ID ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%!==ID',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%! ==ID',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!== ID',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% !== ID ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%! == ID ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ! == ID ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (  #technically not a flag, but identical result
        r'%!=ID',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (  #technically not a flag, but identical result
        r'%!= ID',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (  #technically not a flag, but identical result
        r'% !=ID ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (  #technically not a flag, but identical result
        r'% != ID ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'!"date of birth"',
        cols2,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!"date of birth"',
        cols2,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'!"date of birth"    &!age',
        cols3,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'!"date of birth"    &!age',
        cols3,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!"date of birth"    &!=age',
        cols3,
        df.index,
        None,
        None,
        None,
    ),

    (
        """!ID
        """,
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        """
        !ID""",
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        """
        !ID
        """,
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r"""!ID""",
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r"""!ID
        """,
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r"""
        !ID""",
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r"""
        !ID
        """,
        cols1,
        df.index,
        None,
        None,
        None,
    ),



    #postfix
    (
        r'ID+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r' ID+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'ID +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r' ID +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%ID+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ID+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%ID +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ID +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%==ID+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ==ID+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%== ID+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% == ID +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% == ID +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%  == ID +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    ])
def test_flags_negate(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #prefix
    (
        r'§!0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§! 0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§!0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§ !0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'§ !0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§ ! 0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§ !0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r' § !0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%§!0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§! 0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§!0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ !0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%§!==0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§! ==0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§!== 0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ !== 0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§! == 0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ ! == 0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'!§0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'!§ 0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'!§0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'! §0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'! §0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'! § 0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'! §0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r' ! §0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'% §!0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% §! 0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% §!0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% § !0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'% §!==0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% §! ==0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% §!== 0',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% § !== 0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% §! == 0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% § ! == 0 ',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'§!2',
        cols2,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§!2',
        cols2,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§!2    &§!3',
        cols3,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§!2    &§!3',
        cols3,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§!2    &§!=3',
        cols3,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'!§2',
        cols2,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!§2',
        cols2,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'!§2    &!§3',
        cols3,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'!§2    &!§3',
        cols3,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!§2    &!§3',
        cols3,
        df.index,
        None,
        None,
        None,
    ),



    #postfix
    (
        r'0+index+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'0 +index+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'0+index +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'0 +index +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'0+negate+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'0 +negate+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'0+negate +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'0 +negate +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%0+index+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%0 +index+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%0+index +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%0 +index +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'% 0+negate+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% 0 +negate+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% 0+negate +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% 0 +negate +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),



    #mixed
    (
        r'§0+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§ 0+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§0 +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'§ 0 +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'!0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'! 0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'!0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'! 0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%§0+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ 0+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§0 +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ 0 +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'% !0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ! 0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% !0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ! 0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%§==0+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§== 0+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§==0 +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§== 0 +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%!==0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!== 0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!==0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%!== 0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%§ ==0+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ == 0+negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ ==0 +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%§ == 0 +negate',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%! ==0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%! == 0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%! ==0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%! == 0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    (  #technically not a flag, but identical result
        r'%!=0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (  #technically not a flag, but identical result
        r'%!= 0+index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (  #technically not a flag, but identical result
        r'%!=0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),
    (  #technically not a flag, but identical result
        r'%!= 0 +index',
        cols1,
        df.index,
        None,
        None,
        None,
    ),

    ])
def test_flags_negate_index(code, cols, rows, vals, dtypes, message):
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
        r'% == (3 +index)',
        [3],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% > (5 +index)',
        [6, 7, 8, 9, 10, 11],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% < (5 +index)',
        [0, 1, 2, 3, 4],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% >= (5 +index)',
        [5, 6, 7, 8, 9, 10, 11],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% <= (5 +index)',
        [0, 1, 2, 3, 4, 5],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% != (5 +index)',
        [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% == (5 +index)',
        [5],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% > (5 +index)  & < (8 +index)',
        [6, 7],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% > (5 +index)  & < (8 +index)  & != (6 +index)',
        [7],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% > (5 +index)  & < (8 +index)  & != (6 +index)  & != (7 +index)',
        [],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% > (5 +index)  & < (8 +index)  & != (6, 7 +index +all)',
        [],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'% ? (1 +index)',
        [1, 10, 11],
        df.index,
        None,
        None,
        None,
    ),

    ])
def test_header(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.iloc[:, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #invert selection
    (
        r'id  %:invert',
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
        df.index,
        None,
        None,
        None,
    ),
    (
        r'name  /gender  %:invert',
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
        df.index,
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
        r'%(ID)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%==(ID)',
        ['ID'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%(ID, age, +any)',
        ['ID', 'age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%==(ID, age, +any)',
        ['ID', 'age'],
        df.index,
        None,
        None,
        None,
    ),

    (
        r'%(ID age, +any)',
        ['ID', 'age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r'%==(ID age, +any)',
        ['ID', 'age'],
        df.index,
        None,
        None,
        None,
    ),

    ])
def test_lists(code, cols, rows, vals, dtypes, message):
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
def test_types(code, cols, rows, vals, dtypes, message):

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
