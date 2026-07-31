
import pandas as pd
from .engine import Query
from .symbols import all as symbols_all
from . import (
    engine,
    symbols,
    )

def q(
        df: pd.DataFrame,
        code: str = '',
        verbosity: int = 3,
        ) -> Query:
    query = Query(
        df,
        code,
        symbols_all,
        symbols.QueryStart(),
        symbols.QueryStop(),
        verbosity,
        )
    return query


def qr(
        df: pd.DataFrame,
        code: str = '',
        verbosity: int = 3,
        ) -> Query:
    query_object = (
        q(df, code, verbosity)
        .scan(verbosity)
        .parse(verbosity)
        .run(verbosity)
        )
    return query_object


def qs(
        df: pd.DataFrame,
        code: str = '',
        verbosity: int = 3,
        ) -> pd.DataFrame | pd.io.formats.style.Styler:
    result = (
        q(df, code, verbosity)
        .scan(verbosity)
        .parse(verbosity)
        .run(verbosity)
        .show()
        )
    return result


__all__ = (
    'engine',
    'symbols',
    'q',
    'qr',
    'qs',
    )
