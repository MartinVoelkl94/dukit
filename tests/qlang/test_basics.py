
import pandas as pd
import pytest
import dukit.qlang as ql

from pandas.testing import assert_frame_equal
from dukit import (
    get_df,
    log,
    qr,
    qs,
    )



df = get_df()
params = []

def check_message(expected_strings):

    if isinstance(expected_strings, str):
        expected_strings = (expected_strings,)

    logs = log().data  #type: ignore (using no args, log() always returns a styler)
    logs['text_full'] = logs['level'] + ': ' + logs['text']
    text_full = '\n'.join(logs['text_full'].to_list())

    for string in expected_strings:
        error = f'did not find string "{string}" in logs:\n{text_full}'
        assert string in text_full, error


def test_bare_literal_selects_column():
    result = qr(df, 'age', verbosity=0).result
    expected = df.loc[:, ['age']]
    assert_frame_equal(result, expected)


def test_bare_scope_selects_all_columns():
    result = qr(df, '%', verbosity=0).result
    expected = df.copy()
    assert_frame_equal(result, expected)


def test_basic_parsing():
    query = qr(df, r'name  ?doe +strict  =FOUND', verbosity=0)

    assert len(query.ops) == 3

    op_cols = query.ops[0]
    assert op_cols.category == 'getter'
    assert op_cols.connector == 'new'
    assert op_cols.scope == 'cols'
    assert op_cols.operator == 'GetEquals'
    assert op_cols.args == ['name']

    op_rows = query.ops[1]
    assert op_rows.category == 'getter'
    assert op_rows.connector == 'new'
    assert op_rows.scope == 'rows'
    assert op_rows.operator == 'GetContains'
    assert op_rows.args == ['doe']
    assert 'strict' in op_rows.flags

    op_rows = query.ops[2]
    assert op_rows.category == 'setter'
    assert op_rows.connector == 'new'
    assert op_rows.scope == 'vals'
    assert op_rows.operator == 'SetVals'
    assert op_rows.args == ['FOUND']



def test_ignore_comment():
    code = '#id'
    result = qr(df, code).result
    expected = get_df()
    assert_frame_equal(result, expected)

    code = 'id #name'
    result = qr(df, code).result
    expected = get_df().loc[:, ['ID']]
    assert_frame_equal(result, expected)

    code = r"""
        id
        #name
        """
    result = qr(df, code).result
    expected = get_df().loc[:, ['ID']]
    assert_frame_equal(result, expected)


def test_ignore_op_with_invalid_flags():
    query = qr(df, r'name  ?doe +strict +doesnotexist', verbosity=0)
    assert len(query.ops) == 1


def test_ignore_op_using_invalid_args():
    query = qr(df, 'name  .align(diagonal)', verbosity=0)
    assert len(query.ops) == 1


def test_negate_inverts_getter_condition():
    result = qr(df, r'name  !?doe', verbosity=0).result
    expected = df.drop(index=[0, 10]).loc[:, ['name']]
    assert_frame_equal(result, expected)


def test_returns_dataframe():
    code = 'name'
    result = qr(df, code).result
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ['name']


def test_scope_order():
    symbol_names = [symbol.name for symbol in ql.symbols.all]
    assert symbol_names.index('ScopeValsNew') < symbol_names.index('ScopeRowsNew')
    assert symbol_names.index('ScopeRowsNew') < symbol_names.index('ScopeColsNew')
    assert symbol_names.index('ScopeValsOr') < symbol_names.index('ScopeRowsOr')
    assert symbol_names.index('ScopeRowsOr') < symbol_names.index('ScopeColsOr')



params = [

    #getter scopes
    (
        r'name',
        ['new'],
        ['cols'],
        None
    ),
    (
        r'name  %age',
        ['new', 'new'],
        ['cols', 'cols'],
        None
    ),
    (
        r'name  ?j',
        ['new', 'new'],
        ['cols', 'rows'],
        None
    ),
    (
        r'name  %%?j',
        ['new', 'new'],
        ['cols', 'rows'],
        None
    ),
    (
        r'name  %%%:isint',
        ['new', 'new'],
        ['cols', 'vals'],
        None
    ),
    (
        r'name  /age  %%?j  &&?a',
        ['new', 'or', 'new', 'and'],
        ['cols', 'cols', 'rows', 'rows'],
        None
    ),
    (
        r'name  /age  %%?j  ?a',
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'rows'],
        None
    ),
    (
        r'name  /age  %%?j  %%%?a',
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'vals'],
        None
    ),
    (
        r'name  /age  %%%?j  %%?a',
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'vals', 'rows'],
        None
    ),
    (
        r'name  /age  %%%?j  ?a',
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'vals', 'rows'],
        None
    ),
    (
        r'name  /age  ?j  ?a',
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'rows'],
        None
    ),
    (
        r'name  /age  ?j  %%?a',
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'rows'],
        None
    ),
    (
        r'name  /age  ?j  %%%?a',
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'vals'],
        None
    ),


    #setter scopes
    (
        r'name  =abc',
        ['new', 'new'],
        ['cols', 'vals'],
        None
    ),
    (
        r'name  %=abc',
        ['new', 'new'],
        ['cols', 'cols'],
        None
    ),
    (
        r'name  %%=abc',
        ['new', 'new'],
        ['cols', 'rows'],
        None
    ),
    (
        r'name  %%%=abc',
        ['new', 'new'],
        ['cols', 'vals'],
        None
    ),


    #global scopes
    (
        r'name  .save 1',
        ['new', 'new'],
        ['cols', 'global'],
        None
    ),
    (
        r'name  %%?j .save 1',
        ['new', 'new', 'new'],
        ['cols', 'rows', 'global'],
        None
    ),
    (
        r'name  %%%?j .save 1',
        ['new', 'new', 'new'],
        ['cols', 'vals', 'global'],
        None
    ),


    #multi line getter scopes
    (
        r"""
        name
        """,
        ['new'],
        ['cols'],
        None
    ),
    (
        r"""
        name
        %age
        """,
        ['new', 'new'],
        ['cols', 'cols'],
        None
    ),
    (
        r"""
        name
        age
        """,
        ['new', 'new'],
        ['cols', 'cols'],
        None
    ),
    (
        r"""
        name
        ?j
        """,
        ['new', 'new'],
        ['cols', 'rows'],
        None
    ),
    (
        r"""
        name
        %?j
        """,
        ['new', 'new'],
        ['cols', 'cols'],
        None
    ),
    (
        r"""
        name
        %%?j
        """,
        ['new', 'new'],
        ['cols', 'rows'],
        None
    ),
    (
        r"""
        %%?j
        name
        """,
        ['new', 'new'],
        ['rows', 'cols'],
        None
    ),
    (
        r"""
        name
        %%%:isint
        """,
        ['new', 'new'],
        ['cols', 'vals'],
        None
    ),
    (
        r"""
        %%%:isint()
        name
        """,
        ['new', 'new'],
        ['vals', 'cols'],
        None
    ),
    (
        r"""
        name
        /age
        %%?j
        &&?a
        """,
        ['new', 'or', 'new', 'and'],
        ['cols', 'cols', 'rows', 'rows'],
        None
    ),
    (
        r"""
        name
        /age
        %%?j
        ?a
        """,
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'rows'],
        None
    ),
    (
        r"""
        name
        /age
        %%?j
        %%%?a
        """,
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'vals'],
        None
    ),
    (
        r"""
        name
        /age
        %%%?j
        %%?a
        """,
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'vals', 'rows'],
        None
    ),
    (
        r"""
        name
        /age
        ?j
        ?a
        """,
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'rows'],
        None
    ),
    (
        r"""
        name
        /age
        ?j
        %%?a
        """,
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'rows'],
        None
    ),
    (
        r"""
        name
        /age
        ?j
        %%%?a
        """,
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'rows', 'vals'],
        None
    ),
    (
        r"""
        name
        /age
        %%%?j
        ?a
        """,
        ['new', 'or', 'new', 'new'],
        ['cols', 'cols', 'vals', 'rows'],
        None
    ),


    #setter scopes
    (
        r"""
        =abc
        """,
        ['new'],
        ['vals'],
        None
    ),
    (
        r"""
        name
        =abc
        """,
        ['new', 'new'],
        ['cols', 'vals'],
        None
    ),
    (
        r"""
        %name
        =abc
        """,
        ['new', 'new'],
        ['cols', 'vals'],
        None
    ),
    (
        r"""
        %%?j
        =abc
        """,
        ['new', 'new'],
        ['rows', 'vals'],
        None
    ),
    (
        r"""
        %%%?j
        =abc
        """,
        ['new', 'new'],
        ['vals', 'vals'],
        None
    ),
    (
        r"""
        name  =abc
        """,
        ['new', 'new'],
        ['cols', 'vals'],
        None
    ),
    (
        r"""
        name  %=abc
        """,
        ['new', 'new'],
        ['cols', 'cols'],
        None
    ),
    (
        r"""
        name  %%=abc
        """,
        ['new', 'new'],
        ['cols', 'rows'],
        None
    ),
    (
        r"""
        name  %%%=abc
        """,
        ['new', 'new'],
        ['cols', 'vals'],
        None
    ),
    (
        r"""
        %name  =abc
        """,
        ['new', 'new'],
        ['cols', 'vals'],
        None
    ),
    (
        r"""
        %%?j  =abc
        """,
        ['new', 'new'],
        ['rows', 'vals'],
        None
    ),
    (
        r"""
        %%?j  %=abc
        """,
        ['new', 'new'],
        ['rows', 'cols'],
        None
    ),
    (
        r"""
        %%?j  %%=abc
        """,
        ['new', 'new'],
        ['rows', 'rows'],
        None
    ),
    (
        r"""
        %%?j  %%%=abc
        """,
        ['new', 'new'],
        ['rows', 'vals'],
        None
    ),
    (
        r"""
        %%%?j  =abc
        """,
        ['new', 'new'],
        ['vals', 'vals'],
        None
    ),
    (
        r"""
        %%%?j  %=abc
        """,
        ['new', 'new'],
        ['vals', 'cols'],
        None
    ),
    (
        r"""
        %%%?j  %%=abc
        """,
        ['new', 'new'],
        ['vals', 'rows'],
        None
    ),
    (
        r"""
        %%%?j  %%%=abc
        """,
        ['new', 'new'],
        ['vals', 'vals'],
        None
    ),
    (
        r"""
        name  =abc  .color(red)
        """,
        ['new', 'new', 'new'],
        ['cols', 'vals', 'vals'],
        None
    ),
    (
        r"""
        name  .color(red)  =abc
        """,
        ['new', 'new', 'new'],
        ['cols', 'vals', 'vals'],
        None
    ),
    (
        r"""
        name  .color(red).color(green)=abc.color(blue)
        """,
        ['new', 'new', 'new', 'new', 'new'],
        ['cols', 'vals', 'vals', 'vals', 'vals'],
        None
    ),


    #multi line global scopes
    (
        r"""
        name
        .save(1)
        """,
        ['new', 'new'],
        ['cols', 'global'],
        None
    ),
    (
        r"""
        name
        %%?j
        .save(1)
        """,
        ['new', 'new', 'new'],
        ['cols', 'rows', 'global'],
        None
    ),
    (
        r"""
        name
        %%%?j
        .save(1)
        """,
        ['new', 'new', 'new'],
        ['cols', 'vals', 'global'],
        None
    ),
    ]
@pytest.mark.parametrize('code, connectors, scopes, message', params)
def test_scope_parsing(code, connectors, scopes, message):

    q = qr(df, code, verbosity=0)

    result = [op.connector for op in q.ops]
    expected = connectors
    for i in range(len(expected)):
        msg = f'Expected connectors "{expected}", but got "{result}" for code: {code}'
        assert result[i] == expected[i], msg

    result = [op.scope for op in q.ops]
    expected = scopes
    for i in range(len(expected)):
        msg = f'Expected scopes "{expected}", but got "{result}" for code: {code}'
        assert result[i] == expected[i], msg

    if message:
        check_message(message)


def test_scope_scan_precedence():
    symbol_names = {
        r'%%%': 'ScopeValsNew',
        r'%%': 'ScopeRowsNew',
        r'%': 'ScopeColsNew',
        r'///': 'ScopeValsOr',
        r'//': 'ScopeRowsOr',
        r'/': 'ScopeColsOr',
        }

    for code, token_name in symbol_names.items():
        query_obj = qr(df, code, verbosity=0)
        result = query_obj.tokens[1].name  #0 is always QueryStart
        expected = token_name
        assert result == expected, f'Expected {expected} but "{code}" yielded: {result}'


def test_setter_defaults_to_vals_scope():
    df1 = df.loc[:, ['name']].copy()
    result = qr(df1, '.upper()', verbosity=0).result
    expected = df.loc[:, ['name']].copy()
    expected['name'] = expected['name'].astype('string').str.upper()
    assert_frame_equal(result, expected)


def test_styler_op_returns_styler():
    styled = qs(df, 'name  .color(red)', verbosity=0)
    assert isinstance(styled, pd.io.formats.style.Styler)


def test_symbol_attributes():
    for symbol in ql.symbols.all:
        assert hasattr(symbol, 'id')
        assert hasattr(symbol, 'name')
        assert hasattr(symbol, 'category')
        assert hasattr(symbol, 'regex')
        assert hasattr(symbol, 'flags')
        assert hasattr(symbol, 'args')
        assert hasattr(symbol, 'connectors_allowed')
        assert hasattr(symbol, 'scopes_allowed')
        assert hasattr(symbol, 'flags_allowed')
        assert hasattr(symbol, 'args_allowed')
        assert hasattr(symbol, 'args_min')
        assert hasattr(symbol, 'args_max')


def test_symbol_order():
    """
    if a symbols regex lexeme matches the start of another
    lexeme, the longer lexeme must be parsed first.
    Otherwise, the shorter lexeme would always
    match and the longer lexeme would never be parsed.
    """

    symbols_checked = []
    for symbol in ql.symbols.all[::-1]:
        for symbol_checked in symbols_checked:
            for regex in symbol.regex:
                for regex_checked in symbol_checked.regex:
                    if regex_checked.startswith(regex):
                        print(regex, regex_checked)
        symbols_checked.append(symbol)


def test_unique_symbol_names():
    names = [symbol.name for symbol in ql.symbols.all]
    assert len(names) == len(set(names))


def test_unrecognized_character_logs_error_and_continues():
    log(clear=True, verbosity=2)

    result = qr(df, r'name  $  ?doe  ', verbosity=2).result
    expected = df.loc[[0, 10], ['name']]

    assert_frame_equal(result, expected)
    check_message('ERROR: Unrecognized character "$"')
