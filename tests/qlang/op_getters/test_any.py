
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
def test_regex_flag(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #saving and loading selections
    (
        r"""
        name  .save(1)
        age
        %:load(1)
        """,
        ['name'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r"""
        name  .save(1)
        age
        /:load(1)
        """,
        ['name', 'age'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r"""
        ID
            %%==('1....' +regex)
            //("2...." +regex)
        .save 1

        gender
            %%m
            //==male
            &&:load 1
        ID  /gender
        """,
        ['ID', 'gender'],
        [0, 3, 5],
        None,
        None,
        None,
    ),
    (
        r"""
        ID
            %%==('1....' +regex)
            //==('2....' +regex)
        .save(1)

        gender
            %%==m
            //male
            &&:load(1)
        """,
        ['gender'],
        [0, 3, 5],
        None,
        None,
        None,
    ),
    (
        r"""
        ID
            %%==('1....' +regex)
            //==('2....' +regex)
        .save(1)

        gender
            %%==m
            //==m
            //== male
            // :load(1)
        """,
        ['gender'],
        [0, 1, 2, 3, 4, 5],
        None,
        None,
        None,
    ),
    (
        r"""
        ID
            %%==('1....' +regex)
            //==('2....' +regex)
        .save(1)

        gender
            %%==f
            //f
            //==(female,)
            //:load(1)
        ID
        """,
        ['ID'],
        [0, 1, 2, 3, 4, 5, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        gender
            %%==f
            //==female
        .save 1

        age
            %%>30
            && :load 1
        """,
        ['age'],
        [10],
        None,
        None,
        None,
    ),
    (
        r"""
        age   %%>30   .save(a)
        age   %%<18   //:load(a)
        """,
        ['age'],
        [0, 4, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        weight
            %%<90
            &&>40
        .save('between 40 and 90')

        diabetes
            %%:isyn()
            &&:load('between 40 and 90')
        """,
        ['diabetes'],
        [0, 1],
        None,
        None,
        None,
    ),
    (
        r"""
        weight
            %%<90
            &&>40
        .save('between 40 and 90')

        diabetes
            %%:isyn()
            &&!:load('between 40 and 90')
        """,
        ['diabetes'],
        [3, 4, 5, 6, 9, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%
        age  %%%:load(1)
        """,
        ['age'],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%
        age  %%%:load(1)  %%:trim
        """,
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),
    (
        r"""
        %%%:isna  .save(1)
        %
        %%%
        age  %%%:load(1)  %%:trim
        """,
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %%%
        age  %%%:load(1)  %%:trim
        """,
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%:isnum
        age  %%%:load(1)  %%:trim
        """,
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %%>0
        %
        %%%
        %%
        age  %%%:load(1)  %%:trim
        """,
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%
        age  %%%:load(1)  %%:trim
        """,
        ['age'],
        [2, 3, 6, 8],
        None,
        None,
        None,
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%
        age
            %%%:isnum
            ///:load(1)  %%:trim
        """,
        ['age'],
        [0, 1, 2, 3, 4, 6, 8, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%
        age
            %%%:isstr
            &&&:load(1)  %%:trim
        """,
        ['age'],
        [6, 8],
        None,
        None,
        None,
    ),

    ])
def test_save_load(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)




@pytest.mark.parametrize('code, cols, rows, vals, dtypes, message', [

    #trim rows and cols based on val selection
    (
        r"""
        name /age
            %%%?john
        %:trim
        """,
        ['name'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r"""
        %name /age
            %%%?john
        %%:trim
        """,
        ['name', 'age'],
        [0, 2, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        name /age
            %%%?john
        %:trim()
        """,
        ['name'],
        df.index,
        None,
        None,
        None,
    ),
    (
        r"""
        %name /age
            %%%?john
        %%:trim()
        """,
        ['name', 'age'],
        [0, 2, 10],
        None,
        None,
        None,
    ),
    (
        r"""
        %name /age
            %%%?john
        :trim
        """,
        ['name', 'age'],
        [0, 2, 10],
        None,
        None,
        None,
    ),
    (
        r'%%%:isna  %:trim',
        [
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
        r'%%%:isna  %%:trim',
        df.columns,
        [1, 2, 3, 4, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'%%%:isna  %:trim  %%:trim',
        [
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
        [1, 2, 3, 4, 6, 7, 8, 9, 10],
        None,
        None,
        None,
    ),
    (
        r'%%%:isna  %!:trim  %%%',
        ['ID', 'name', 'date of birth'],
        df.index,
        None,
        None,
        None,
    ),

    ])
def test_trim(code, cols, rows, vals, dtypes, message):
    result = df.dk.qr(code).result
    expected = df.loc[rows, cols]
    if dtypes:
        for col, dtype in zip(cols, dtypes):
            expected[col] = expected[col].astype(dtype)
    assert_frame_equal(result, expected)  #type: ignore
    if message:
        check_message(message)
