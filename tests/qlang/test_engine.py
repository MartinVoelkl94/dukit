
import pandas as pd
import pytest

from dukit import get_df
from dukit.qlang import (
    engine,
    symbols,
    )


df = get_df()

def get_query_obj(code=''):
    query = engine.Query(
        df,
        code,
        symbols.all,
        symbols.QueryStart(),
        symbols.QueryStop(),
        0,
        )
    return query



def test_result_is_df():
    result = df.dk.qs('==name')
    assert isinstance(result, pd.DataFrame)


def test_result_is_styler():
    result = df.dk.qs('.color(red)')
    assert isinstance(result, pd.io.formats.style.Styler)


def test_wrappers_return_query():
    query = get_query_obj('name')
    assert query.scan() is query
    assert query.parse() is query
    assert query.run() is query


def test_query_str():
    query = get_query_obj('name')
    query.scan()
    qstr = str(query)

    assert '----------------Query object [q]----------------\n' in qstr
    assert '>>> q.code' in qstr
    assert '>>> q.tokens' in qstr
    assert '>>> q.ops' in qstr
    assert '>>> q.mask_cols' in qstr
    assert '>>> q.mask_rows' in qstr
    assert '>>> q.mask_vals' in qstr
    assert '>>> q.masks_saved' in qstr
    assert '>>> q.style_cols' in qstr
    assert '>>> q.style_rows' in qstr
    assert '>>> q.style_vals' in qstr
    assert '>>> q.df' in qstr
    assert '----------------Query object end----------------\n' in qstr



def test_query_repr():
    query = get_query_obj('name')
    query.scan()
    qrepr = repr(query)

    assert '--------Query object [q]--------\n' in qrepr
    assert '>>> q.code' in qrepr
    assert '>>> q.tokens' in qrepr
    assert '>>> q.ops' in qrepr
    assert '>>> q.df' in qrepr
    assert '>>> q.scan()  #scan code into tokens\n' in qrepr
    assert '>>> q.parse()  #parse tokens into ops\n' in qrepr
    assert '>>> q.run()  #run ops on the df\n' in qrepr
    assert '>>> q.result\n' in qrepr
    assert '>>> q.styled\n' in qrepr
    assert '--------Query object end--------\n' in qrepr



def test_query_verbosity_default():
    query = engine.Query(
        df,
        '',
        symbols.all,
        symbols.QueryStart(),
        symbols.QueryStop(),
        )
    assert query.verbosity == 3
    assert query.scan(verbosity=None).verbosity == 3
    assert query.parse(verbosity=None).verbosity == 3
    assert query.run(verbosity=None).verbosity == 3



def test_symbol_basic():
    query = get_query_obj()

    class TestSymbol(engine.Symbol):
        name = 'TestSymbol'

    with pytest.raises(NotImplementedError):
        TestSymbol().run(query)

    with pytest.raises(NotImplementedError):
        TestSymbol().getter(
            pd.Series(),
            pd.Series(True, index=df.index),
            'arg',
            query,
            )

    with pytest.raises(NotImplementedError):
        TestSymbol().setter(
            pd.Series(),
            pd.Series(True, index=df.index),
            ['arg'],
            query,
            )

    with pytest.raises(NotImplementedError):
        TestSymbol().styler()



def test_symbol_token_repr():
    token = df.dk.q('(').scan().tokens[1]
    assert "<'ListStart' '('>" == repr(token)


def test_symbol_token_str():
    token = df.dk.q('(').scan().tokens[1]
    token_str = str(token)
    assert "----Token 1----\n" in token_str
    assert "name: 'ListStart'\n" in token_str
    assert "category: 'syntax'\n" in token_str
    assert "regex: ('\\\\(',)\n" in token_str
    assert 'linenum: 1' in token_str
    assert "str_matched: '('\n" in token_str
    assert "literal: ''\n" in token_str



def test_symbol_op_repr():
    op = df.dk.q('==name').scan().parse().ops[0]
    op_str = repr(op)
    assert "----Operation 0----\n" in op_str
    assert "connector: 'new'\n" in op_str
    assert "scope: 'rows'\n" in op_str
    assert "operator: 'GetEquals'\n" in op_str
    assert "flags: {}\n" in op_str
    assert "args: ['name']\n" in op_str


def test_symbol_op_str():
    op = df.dk.q('==name').scan().parse().ops[0]
    op_str = str(op)
    assert "--------Operation 0--------\n" in op_str
    assert "connector: 'new'\n" in op_str
    assert "scope: 'rows'\n" in op_str
    assert "operator: 'GetEquals'\n" in op_str
    assert "flags: {}\n" in op_str
    assert "args: ['name']\n" in op_str
    assert "connectors_allowed: " in op_str
    assert "scopes_allowed: " in op_str
    assert "flags_allowed: " in op_str
    assert "args_allowed: {}\n" in op_str
    assert "args_min: 1\n" in op_str
    assert "args_max: 1000000\n" in op_str


def test_symbol_build_creates_new_token():
    symbol = symbols.Literal()
    token = symbol.build('name')
    assert token is not symbol
