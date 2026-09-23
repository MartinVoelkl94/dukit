
import pandas as pd
import pytest
import typing

from dukit.qlang import (
    engine,
    symbols,
    )
from dukit import (
    get_df,
    log,
    )


params = []
df = get_df()


def get_query_obj():
    query_obj = engine.Query(
        df,
        '',
        symbols.all,
        symbols.QueryStart(),
        symbols.QueryStop(),
        2,
        )
    return query_obj


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

    #engine internals

    (
        r"""
        ~
        """,
        'ERROR: Unrecognized character "~"',
    ),
    (
        r"""
        name  &age
        """,
        (
            'WARNING: no cols fulfill the condition in '
            'current op and the previous condition(s).'
        ),
    ),
    (
        r"""
        na_col
        """,
        'WARNING: no cols fulfill the condition in current op.',
    ),
    (
        r"""
        na_col  >0
        """,
        (
            'ERROR: row selection cannot be applied'
            ' when the current col selection is empty.'
        ),
    ),
    (
        r"""
        na_col  %%%>0
        """,
        (
            'ERROR: val selection cannot be applied'
            ' when the current col selection is empty.'
        ),
    ),
    (
        r"""
        %%!:all  %%%>0
        """,
        (
            'ERROR: val selection cannot be applied'
            ' when the current row selection is empty.'
        ),
    ),
    (
        r"""
        na_col  %=x
        """,
        (
            'ERROR: cannot set cols when the'
            ' current col selection is empty.'
        ),
    ),
    (
        r"""
        %%!:all  %%=x
        """,
        (
            'ERROR: cannot set rows when the'
            ' current row selection is empty.'
        ),
    ),
    (
        r"""
        na_col  %%%=x
        """,
        (
            'ERROR: cannot set vals when the'
            ' current col selection is empty.'
        ),
    ),
    (
        r"""
        na_col  =x
        """,
        (
            'ERROR: cannot set vals when the'
            ' current col selection is empty.'
        ),
    ),
    (
        r"""
        %%!:all  =x
        """,
        (
            'ERROR: cannot set vals when the'
            ' current row selection is empty.'
        ),
    ),
    (
        r"""
        %%%!:all  =x
        """,
        (
            'ERROR: cannot set vals when the'
            ' current val selection is empty.'
        ),
    ),


    #symbols internals
    (
        r"""
        .lower +strict
        """,
        'ERROR: flag "strict" is not valid for op.',
    ),
    (
        r"""
        ==1 +int +float
        """,
        'ERROR: multiple type flags are not allowed in the same op.',
    ),
    (
        r"""
        %%%>0 +index
        """,
        (
            'ERROR: flag "index" is only valid for'
            r' scopes "%", "&", "/", "%%", "&&", "//".'
        ),
    ),
    (
        r"""
        =x +allcols
        """,
        'ERROR: "allcols" flag is only valid for getter ops.',
    ),
    (
        r"""
        %=x +allcols
        """,
        r'ERROR: "allcols" flag is only valid for scopes "%%", "&&", "//".',
    ),
    (
        r"""
        %%%=x +allcols
        """,
        r'ERROR: "allcols" flag is only valid for scopes "%%", "&&", "//".',
    ),
    (
        r"""
        %%=a +colref
        """,
        r'ERROR: "colref" flag is only valid for setter ops with scope "%%%".',
    ),
    (
        r"""
        %?a +colref
        """,
        (
            'ERROR: "colref" flag is only valid for getter ops'
            r' with scopes "%%", "&&", "//", "%%%", "&&&", "///".'
        ),
    ),
    (
        r"""
        %:all  +strict
        """,
        'ERROR: flag "strict" is not valid for op.',
    ),
    (
        r"""
        =
        """,
        'ERROR: op has too few args.',
    ),
    (
        r"""
        = a b
        """,
        'ERROR: op has too many args.',
    ),
    (
        r"""
        .save 1
        :load 2
        """,
        'ERROR: No saved selection named "2" found.',
    ),
    (
        r"""
        .save 1
        .save 1
        """,
        'WARNING: overwriting previously saved selection "1".',
    ),
    (
        r"""
        age  <@na_col
        """,
        'ERROR: col "na_col" not found for colref comparison.',
    ),
    (
        r"""
        .new(age)
        """,
        (
            'WARNING: colname "age" already exists,'
            ' applying increment strategy to ensure uniqueness.'
        ),
    ),
    (
        r"""
        = a (b, c)
        """,
        (
            'ERROR: list start "(" cannot be used'
            ' when args have already been added to the current op.'
        ),
    ),
    (
        r"""
        = ()(
        """,
        'ERROR: list start "(" cannot be used after a list stop token.',
    ),
    (
        r"""
        = a)
        """,
        'ERROR: list stop ")" can only be used after a list start token.',
    ),
    (
        r"""
        = (a))
        """,
        (
            'ERROR: list stop ")" cannot be used if a list has'
            ' not been started or has already been stopped.'
        ),
    ),
    (
        r"""
        @
        """,
        'ERROR: flag "colref" cannot be used without an operator.',
    ),
    ]
@pytest.mark.parametrize('code, message', params)
def test_log_messages(code, message):
    log(clear=True)
    df.dk.qs(code)
    check_message(message)




def test_invalid_operator():
    log(clear=True)
    query = df.dk.q()
    query.op = engine.Symbol()
    query.op.connector = 'new'
    symbols._process_op(query)
    messages = 'ERROR: op is missing an operator.'
    check_message(messages)


def test_invalid_getter_mask():

    log(clear=True)
    series = pd.Series([1, 2, 3])
    mask = pd.Series([True, False, True])

    def getter_invalid(
            series: pd.Series,
            mask: pd.Series[bool],
            arg: typing.Any,
            q: engine.Query,
            ) -> pd.Series:
        mask = pd.Series([True, False])
        return mask
    op = engine.Symbol()
    op.getter = getter_invalid
    query = df.dk.q()

    symbols._apply_getter(
        series,
        mask,
        op,
        query,
        )
    message = 'ERROR: getter returned invalid mask.'
    check_message(message)



def test_invalid_op():
    log(clear=True)

    query = df.dk.q()
    query.op = engine.Symbol()
    symbols._validate_op_essentials(query, True)
    messages = [
        'ERROR: op is missing a connector.',
        'ERROR: op is missing a scope.',
        'ERROR: op is missing an operator.',
        'ERROR: op has an invalid connector.',
        'ERROR: op has an invalid scope.',
        ]
    check_message(messages)


def test_invalid_arg_type():
    log(clear=True)

    series = pd.Series([1, 2, 3])
    arg = None
    op = engine.Symbol()
    query = df.dk.q()

    symbols._infer_types_getter(
        series,
        arg,  # type: ignore
        op,
        query,
        )
    message = 'WARNING: unable to infer type for arg "None".'
    check_message(message)
