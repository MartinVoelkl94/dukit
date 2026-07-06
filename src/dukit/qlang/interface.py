
import pandas as pd

from .engine import Query
from .symbols import (
    all as symbols_all,
    QueryStart,
    QueryStop,
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
        QueryStart(),
        QueryStop(),
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



@pd.api.extensions.register_dataframe_accessor('q')
class QueryAccessor():
    def __init__(
            self,
            df: pd.DataFrame,
            ):
        self.df = df
    def __call__(
            self,
            code: str = '',
            verbosity: int = 3,
            ):
        return q(self.df, code, verbosity)


@pd.api.extensions.register_dataframe_accessor('qr')
class QueryRunAccessor():
    def __init__(
            self,
            df: pd.DataFrame,
            ):
        self.df = df
    def __call__(
            self,
            code: str = '',
            verbosity: int = 3,
            ):
        return qr(self.df, code, verbosity)


@pd.api.extensions.register_dataframe_accessor('qs')
class QueryShowAccessor():
    def __init__(
            self,
            df: pd.DataFrame,
            ):
        self.df = df
    def __call__(
            self,
            code: str = '',
            verbosity: int = 3,
            ):
        return qs(self.df, code, verbosity)
