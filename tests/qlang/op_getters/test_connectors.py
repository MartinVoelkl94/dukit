
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
def test_cols(code, cols, rows, vals, dtypes, message):
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
def test_rows(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore  #type: ignore
    if message:
        check_message(message)