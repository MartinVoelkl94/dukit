
import pandas as pd

from .diffing import (
    diff,
    rediff,
    )
from .qlang import (
    q,
    qr,
    qs,
    )
from .utils import (
    log,
    dict_to_str,
    list_to_str,
    )
from .pandas import (
    get_df,
    get_dfs,
    deduplicate,
    flatten,
    stagger,
    embed,
    collapse,
    transpose,
    )
from .excel import (
    format,
    save,
    )
from .typing import (
    Box,
    _int as int,
    _float as float,
    _num as num,
    _bool as bool,
    _date as date,
    _datetime as datetime,
    _na as na,
    _nk as nk,
    _yn as yn,
    _type as type,
    _convert as convert,
    _typeinfo as typeinfo,
    _typeinfostrict as typeinfostrict,
    )
from .os import (
    pwd,
    cd,
    cp,
    mv,
    mkdir,
    isdir,
    isfile,
    ispath,
    fetch,
    )

__all__ = (
    'diff',
    'rediff',
    'q',
    'qr',
    'qs',
    'log',
    'dict_to_str',
    'list_to_str',
    'get_df',
    'get_dfs',
    'deduplicate',
    'flatten',
    'stagger',
    'embed',
    'collapse',
    'transpose',
    'format',
    'save',
    'Box',
    'int',
    'float',
    'num',
    'bool',
    'date',
    'datetime',
    'na',
    'nk',
    'yn',
    'type',
    'convert',
    'typeinfo',
    'typeinfostrict',
    'pwd',
    'cd',
    'cp',
    'mv',
    'mkdir',
    'isdir',
    'isfile',
    'ispath',
    'fetch',
    )




@pd.api.extensions.register_dataframe_accessor('dk')
class DukitAccessor():

    def __init__(
            self,
            df: pd.DataFrame,
            ):
        self.df = df


    def q(
            self,
            code='',
            verbosity=3,
            ):
        return q(self.df, code, verbosity)


    def qs(
            self,
            code='',
            verbosity=3,
            ):
        return qs(self.df, code, verbosity)


    def qr(
            self,
            code='',
            verbosity=3,
            ):
        return qr(self.df, code, verbosity)


    def flatten(
            self,
            on: str,
            template='{colname}_#{counter}',
            ):
        df_new = flatten(
            self.df,
            on=on,
            template=template,
            )
        return df_new


    def stagger(
            self,
            on: str,
            template='#{counter}_{colname}',
            separator_col='#{counter}',
            ):
        df_new = stagger(
            self.df,
            on=on,
            template=template,
            separator_col=separator_col,
            )
        return df_new


    def embed(
            self,
            on: str,
            colname='',
            template='{colname}_#{counter}',
            line_start='',
            separator=':',
            spacer='\u00A0',  #non-breaking space
            line_stop='\n',
            ):
        df_new = embed(
            self.df,
            on=on,
            colname=colname,
            template=template,
            line_start=line_start,
            separator=separator,
            spacer=spacer,
            line_stop=line_stop,
            )
        return df_new


    def collapse(
            self,
            on: str,
            template='{colname}',
            line_start='#',
            line_stop='\n',
            ):
        df_new = collapse(
            self.df,
            on=on,
            template=template,
            line_start=line_start,
            line_stop=line_stop,
            )
        return df_new


    def transpose(
            self,
            header='uid',
            ) -> pd.DataFrame:
        df_new = transpose(
            self.df,
            header=header,
            )
        return df_new


    def save(
            self,
            path: str,
            sheet_name='df',
            index=False,
            format_excel=True,
            **kwargs,
            ):
        save(
            df=self.df,
            path=path,
            sheet_name=sheet_name,
            index=index,
            format_excel=format_excel,
            **kwargs,
            )
        return None


    def style(self):
        code = """
        .replace("\n", "<br>")
        .wrap(normal)
        .mono()
        .align(left)
        %.align(center)
        """
        df_styled = qs(self.df, code)
        return df_styled
