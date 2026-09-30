
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

    #regex flag + type based selection
    (
        r"""
        ID  ==("1...." +regex)
        diabetes  &&:isyn
        """,
        ['diabetes'],
        [0, 1],
        None,
        None,
        None,
    ),
    (
        r"""
        ID
            %%==("1...." +regex)
        diabetes
            &&:isyn
        """,
        ['diabetes'],
        [0, 1],
        None,
        None,
        None,
    ),
    (
        r"""
        ID
            %%==("1...." +regex)
        diabetes
            &&:isyn()
        ID
        /diabetes
        """,
        ['ID', 'diabetes'],
        [0, 1],
        None,
        None,
        None,
    ),
    (
        r"""
        diabetes
            %%:isyn()
        ID
            &&==("1...." +regex)
        /diabetes
        """,
        ['ID', 'diabetes'],
        [0, 1],
        None,
        None,
        None,
    ),
    (
        r"""
        diabetes
            %%:isyn()
        /ID
            &&==("1...." +regex)
        """,
        ['ID', 'diabetes'],
        [0, 1],
        None,
        None,
        None,
    ),

    ])
def test_any(code, cols, rows, vals, dtypes, message):
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
def test_vals(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)