
import pytest
import pandas as pd

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
        r'%.eval("x.lower()")',
        [
            'id',
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
            'dose'
        ],
        None,
        None,
        ['object'],
        None,
    ),

    ])
def test_cols(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()
    expected.columns = pd.Series(cols).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r'name  %%.eval("str(1)")',
        ['name'],
        [
            '1',
            '1',
            '1',
            '1',
            '1',
            '1',
            '1',
            '1',
            '1',
            '1',
            '1',
        ],
        None,
        ['object'],
        None,
    ),
    (
        r"""
        name  %%.eval("str(x)")
        %
        %%
        """,
        df.columns,
        [
            '0',
            '1',
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
        ],
        None,
        ['object'],
        None,
    ),

    ])
def test_rows(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = get_df()[cols]
    expected.index = pd.Series(rows).astype(dtypes[0])
    assert_frame_equal(result, expected)
    if message:
        check_message(message)



@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    (
        r"""
        name  .eval("x.lower()")
        """,
        ['name'],
        df.index,
        [[
            'john doe',
            'jane smith',
            'alice johnson',
            'bob brown',
            'eva white',
            'frank miller',
            'grace taylor',
            'harry clark',
            'ivy green',
            'jack williams',
            'john doe',
        ]],
        ['object'],
        None
    ),
    (
        r"""
        name  %%%.eval("x.lower()")
        """,
        ['name'],
        df.index,
        [[
            'john doe',
            'jane smith',
            'alice johnson',
            'bob brown',
            'eva white',
            'frank miller',
            'grace taylor',
            'harry clark',
            'ivy green',
            'jack williams',
            'john doe',
        ]],
        ['object'],
        None
    ),
    (
        r"""
        name
            %%!:eval("x == x.lower()")
                .eval("x.lower()")
        """,
        ['name'],
        [0, 1, 2, 3, 5, 6, 7, 8, 9, 10],
        [[
            'john doe',
            'jane smith',
            'alice johnson',
            'bob brown',
            'frank miller',
            'grace taylor',
            'harry clark',
            'ivy green',
            'jack williams',
            'john doe',
        ]],
        ['object'],
        None
    ),
    (
        r"""
        name
            %%!:eval("x == x.lower()")
                .eval("x.lower()")
        %%
        """,
        ['name'],
        df.index,
        [[
            'john doe',
            'jane smith',
            'alice johnson',
            'bob brown',
            'eva white',
            'frank miller',
            'grace taylor',
            'harry clark',
            'ivy green',
            'jack williams',
            'john doe',
        ]],
        ['object'],
        None
    ),
    (
        r"""
        id
            %%10001
            .eval("str(10001)")
        """,
        ['ID'],
        [0],
        [['10001']],
        ['object'],
        None
    ),
    (
        r"""
        id
            %%10001
            .eval("str(10001)")
            .tostr()
        """,
        ['ID'],
        [0],
        [['10001']],
        ['object'],
        None
    ),
    (
        r"""
        id  /age
            %%:isnum()
            %%%:all()
                .eval("str(0)")
        """,
        ['ID', 'age'],
        df.index,
        [[
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            ],
            [
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
        ]],
        ['object', 'object'],
        None
    ),
    (
        r"""
        id  /age
            %%:isnum()
                .eval("str(0)")
        """,
        ['ID', 'age'],
        df.index,
        [[
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            '0',
            ],
            [
            '0',
            '0',
            '0',
            pd.NaT,
            '0',
            'forty-five',
            'nan',
            'unk',
            '0',
            'unknown',
            '0',
        ]],
        ['object', 'object'],
        None
    ),
    (
        r"""
        id  /age
            %%:isnum()
                .eval("0")
        """,
        ['ID', 'age'],
        df.index,
        [[
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            ],
            [
            0,
            0,
            0,
            pd.NaT,
            0,
            'forty-five',
            'nan',
            'unk',
            0,
            'unknown',
            0,
        ]],
        ['object', 'object'],
        None
    ),
    (
        r"""
        id  /age
            %%:isnum(+allcols)
                .eval("0")
        """,
        ['ID', 'age'],
        [0, 1, 2, 4, 8, 10],
        [[
            0,
            0,
            0,
            0,
            0,
            0,
            ],
            [
            0,
            0,
            0,
            0,
            0,
            0,
        ]],
        ['object', 'object'],
        None
    ),
    (
        r"""
        id  /age
            %%:isnum(+allcols)
                .eval("0")
        %%
        """,
        ['ID', 'age'],
        df.index,
        [[
            0,
            0,
            0,
            20001,
            0,
            20003,
            30001,
            30002,
            0,
            30004,
            0,
            ],
            [
            0,
            0,
            0,
            pd.NaT,
            0,
            'forty-five',
            'nan',
            'unk',
            0,
            'unknown',
            0,
        ]],
        ['object', 'object'],
        None
    ),
    (
        r"""
        id  .eval('df["name"]')
        """,
        ['ID'],
        df.index,
        [[
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john Doe',
        ]],
        ['object'],
        None
    ),
    (
        r"""
        id  .eval('df["name"]')  %%
        """,
        ['ID'],
        df.index,
        [[
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john Doe',
        ]],
        ['object'],
        None
    ),
    (
        r"""
        id  /age  .eval('df["name"]')
        """,
        ['ID', 'age'],
        df.index,
        [[
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john Doe',
            ],
            [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john Doe',
        ]],
        ['object', 'object'],
        None
    ),
    (
        r"""
        .eval('df["name"]')
        """,
        df.columns,
        df.index,
        [df['name'] for col in df.columns],
        [
            'object',
            'string',
            'object',
            'object',
            'string',
            'object',
            'object',
            'object',
            'object',
            'string',
            'object',
            'string',
        ],
        None
    ),
    (
        r"""
        id  /age
            :isnum
            .eval('df["name"]')
        """,
        ['ID', 'age'],
        df.index,
        [[
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john Doe',
            ],
            [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            pd.NaT,
            'eva white',
            'forty-five',
            'nan',
            'unk',
            'IVY GREEN',
            'unknown',
            'john Doe',
        ]],
        ['object', 'object'],
        None
    ),
    (
        r"""
        id  /age
            :isnum +allcols
            .eval('df["name"]')
        """,
        ['ID', 'age'],
        [0, 1, 2, 4, 8, 10],
        [[
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'eva white',
            'IVY GREEN',
            'john Doe',
            ],
            [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'eva white',
            'IVY GREEN',
            'john Doe',
        ]],
        ['object', 'object'],
        None
    ),
    (
        r"""
        id  /age
            :isnum +allcols
            .eval('df["name"]')
        %%
        """,
        ['ID', 'age'],
        df.index,
        [[
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            20001,
            'eva white',
            20003,
            30001,
            30002,
            'IVY GREEN',
            30004,
            'john Doe',
            ],
            [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            pd.NaT,
            'eva white',
            'forty-five',
            'nan',
            'unk',
            'IVY GREEN',
            'unknown',
            'john Doe',
        ]],
        ['object', 'object'],
        None
    ),

    ])
def test_vals(code, cols, rows, vals, dtypes, message):

    result = df.dk.qr(code).result
    expected = pd.DataFrame(index=rows)
    for col, val, dtype in zip(cols, vals, dtypes):
        expected[col] = pd.Series(val, index=rows).astype(dtype)
    expected.columns = expected.columns.to_series().convert_dtypes()
    expected.index = expected.index.to_series().convert_dtypes()

    assert_frame_equal(result, expected)
    if message:
        check_message(message)