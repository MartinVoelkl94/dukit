
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

    #regex flag + type based selection
    (
        r"""
        ID  ==("1...." +regex)
        diabetes  &&:isyn
        """,
        df.loc[[0, 1], ['diabetes']],
        None
    ),
    (
        r"""
        ID
            %%==("1...." +regex)
        diabetes
            &&:isyn
        """,
        df.loc[[0, 1], ['diabetes']],
        None
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
        df.loc[[0, 1], ['ID', 'diabetes']],
        None
    ),
    (
        r"""
        diabetes
            %%:isyn()
        ID
            &&==("1...." +regex)
        /diabetes
        """,
        df.loc[[0, 1], ['ID', 'diabetes']],
        None
    ),
    (
        r"""
        diabetes
            %%:isyn()
        /ID
            &&==("1...." +regex)
        """,
        df.loc[[0, 1], ['ID', 'diabetes']],
        None
    ),


    #saving and loading selections
    (
        r"""
        name  .save(1)
        age
        %:load(1)
        """,
        df.loc[:, ['name']],
        None
    ),
    (
        r"""
        name  .save(1)
        age
        /:load(1)
        """,
        df.loc[:, ['name', 'age']],
        None
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
        df.loc[[0, 3, 5], ['ID', 'gender']],
        None
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
        df.loc[[0, 3, 5], ['gender']],
        None
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
        df.loc[[0, 1, 2, 3, 4, 5], ['gender']],
        None
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
        df.loc[[0, 1, 2, 3, 4, 5, 10], ['ID']],
        None
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
        df.loc[[10], ['age']],
        None
    ),
    (
        r"""
        age   %%>30   .save(a)
        age   %%<18   //:load(a)
        """,
        df.loc[[0, 4, 10], ['age']],
        None
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
        df.loc[[0, 1], ['diabetes']],
        None
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
        df.loc[[3, 4, 5, 6, 9, 10], ['diabetes']],
        None
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%
        age  %%%:load(1)
        """,
        df.loc[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['age']],
        None
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%
        age  %%%:load(1)  %%:trim
        """,
        df.loc[[2, 3, 6, 8], ['age']],
        None
    ),
    (
        r"""
        %%%:isna  .save(1)
        %
        %%%
        age  %%%:load(1)  %%:trim
        """,
        df.loc[[2, 3, 6, 8], ['age']],
        None
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %%%
        age  %%%:load(1)  %%:trim
        """,
        df.loc[[2, 3, 6, 8], ['age']],
        None
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%:isnum
        age  %%%:load(1)  %%:trim
        """,
        df.loc[[2, 3, 6, 8], ['age']],
        None
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
        df.loc[[2, 3, 6, 8], ['age']],
        None
    ),
    (
        r"""
        age  %%%:isna  .save(1)
        %
        %%%
        age  %%%:load(1)  %%:trim
        """,
        df.loc[[2, 3, 6, 8], ['age']],
        None
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
        df.loc[[0, 1, 2, 3, 4, 6, 8, 10], ['age']],
        None
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
        df.loc[[6, 8], ['age']],
        None
    ),

    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_complex_queries(code, expected, message):
    result = qr(df, code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)




params = [

    (
        r"""
        name /age
            %%%?john
        %:trim
        """,
        df.loc[:, ['name']],
        None,
    ),
    (
        r"""
        %name /age
            %%%?john
        %%:trim
        """,
        df.loc[[0, 2, 10], ['name', 'age']],
        None,
    ),
    (
        r"""
        name /age
            %%%?john
        %:trim()
        """,
        df.loc[:, ['name']],
        None,
    ),
    (
        r"""
        %name /age
            %%%?john
        %%:trim()
        """,
        df.loc[[0, 2, 10], ['name', 'age']],
        None,
    ),
    (
        r"""
        %name /age
            %%%?john
        :trim
        """,
        df.loc[[0, 2, 10], ['name', 'age']],
        None,
    ),
    (
        r'%%%:isna  %:trim',
        df.loc[:, [
            'age',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
            ]],
        None,
    ),
    (
        r'%%%:isna  %%:trim',
        df.loc[[1, 2, 3, 4, 6, 7, 8, 9, 10], :],
        None,
    ),
    (
        r'%%%:isna  %:trim  %%:trim',
        df.loc[[1, 2, 3, 4, 6, 7, 8, 9, 10], [
            'age',
            'gender',
            'height',
            'weight',
            'bp systole',
            'bp diastole',
            'cholesterol',
            'diabetes',
            'dose',
            ]],
        None,
    ),
    (
        r'%%%:isna  %!:trim  %%%',
        df.loc[:, ['ID', 'name', 'date of birth']],
        None,
    ),
    ]
@pytest.mark.parametrize('code, expected, message', params)
def test_trim(code, expected, message):
    result = qr(df, code).result
    assert_frame_equal(result, expected)
    if message:
        check_message(message)
