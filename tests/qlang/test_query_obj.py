
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



def test_repr():
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



def test_result_is_df():
    result = df.dk.qs('==name')
    assert isinstance(result, pd.DataFrame)


def test_result_is_styler():
    result = df.dk.qs('.color(red)')
    assert isinstance(result, pd.io.formats.style.Styler)



def test_str():
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



def test_verbosity_default():
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



def test_wrappers_return_query():
    query = get_query_obj('name')
    assert query.scan() is query
    assert query.parse() is query
    assert query.run() is query
