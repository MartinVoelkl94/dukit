
import pytest
import pandas as pd

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



def test_basic():
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



def test_build_creates_new_token():
    symbol = symbols.Literal()
    token = symbol.build('name')
    assert token is not symbol



@pytest.mark.parametrize(
    'code',
    [
        '"2001-01-01"',
        '"01-01-2001"',
        "'date of birth'",
        '"date of birth"',
    ],
    )
def test_literal_variants(code):
    query = df.dk.q(code).scan().parse()

    assert isinstance(query.tokens[1], symbols.Literal)
    assert query.tokens[1].literal == code.strip('"\'')



def test_op_repr():
    op = df.dk.q('==name').scan().parse().ops[0]
    op_str = repr(op)
    assert "----Operation 0----\n" in op_str
    assert "connector: 'new'\n" in op_str
    assert "scope: 'rows'\n" in op_str
    assert "operator: 'GetEquals'\n" in op_str
    assert "flags: {}\n" in op_str
    assert "args: ['name']\n" in op_str



def test_op_str():
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



def test_token_repr():
    token = df.dk.q('(').scan().tokens[1]
    assert "<'ListStart' '('>" == repr(token)


def test_token_str():
    token = df.dk.q('(').scan().tokens[1]
    token_str = str(token)
    assert "----Token 1----\n" in token_str
    assert "name: 'ListStart'\n" in token_str
    assert "category: 'syntax'\n" in token_str
    assert "regex: ('\\\\(',)\n" in token_str
    assert 'linenum: 1' in token_str
    assert "str_matched: '('\n" in token_str
    assert "literal: ''\n" in token_str
