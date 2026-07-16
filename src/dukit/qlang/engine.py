
import pandas as pd
import numpy as np
import typing
import re

from ..util import (
    log,
    build_log_context,
    dict_to_str,
    list_to_str,
    )
from ..typing import (
    Box,
    DTYPES_ALLOWED,
    )


class Query(Box):

    def __init__(
            self,
            df: pd.DataFrame,
            code: str,
            symbols_allowed: list['Symbol'],
            symbol_start: 'Symbol',
            symbol_stop: 'Symbol',
            verbosity: int = 3,
            ):

        super().__init__()
        df = df.copy().convert_dtypes()
        df.columns = df.columns.to_series().convert_dtypes()
        df.index = df.index.to_series().convert_dtypes()
        cols = df.columns
        rows = df.index
        symbol_start.id = 0

        #main attributes
        self.df = df
        self.code = code
        self.verbosity = verbosity

        #used for parsing
        self.symbols_allowed = symbols_allowed
        self.symbol_start = symbol_start
        self.symbol_stop = symbol_stop
        self.match_str = ''
        self.tokens = []
        self.ops = []
        self.op = Symbol()

        #masks for current selection state
        self.mask_cols = pd.Series([True for col in cols])
        self.mask_rows = pd.Series([True for idx in rows])
        self.mask_cols.index = cols
        self.mask_rows.index = rows
        self.mask_vals = pd.DataFrame(
            np.ones(self.df.shape, dtype=bool),
            columns=cols,
            index=rows,
            )
        self.masks_saved = {}

        #optional style information
        self.style_cols: None | pd.Series[str] = None
        self.style_rows: None | pd.Series[str] = None
        self.style_vals: None | pd.DataFrame = None

        #styled/unstyled results
        self.result = pd.DataFrame()
        self.styled = self.result.style


    def __str__(self) -> str:
        txt_tokens = [token.name for token in self.tokens]
        txt_ops = [op.operator for op in self.ops]
        txt = (
            '----------------Query object [q]----------------\n'
            'attributes:\n\n\n'
            f'>>> q.code\n{self.code!r}\n\n\n'
            f'>>> q.tokens\n{txt_tokens}\n\n\n'
            f'>>> q.ops\n{txt_ops}\n\n\n'
            f'>>> q.op\n{self.op}\n\n\n'
            f'>>> q.mask_cols\n{self.mask_cols}\n\n\n'
            f'>>> q.mask_rows\n{self.mask_rows}\n\n\n'
            f'>>> q.mask_vals\n{self.mask_vals}\n\n\n'
            f'>>> q.masks_saved\n{self.masks_saved}\n\n\n'
            f'>>> q.style_cols\n{self.style_cols}\n\n\n'
            f'>>> q.style_rows\n{self.style_rows}\n\n\n'
            f'>>> q.style_vals\n{self.style_vals}\n\n\n'
            f'>>> q.df\n{self.df}\n\n\n'
            '----------------Query object end----------------\n'
            )
        return txt


    def __repr__(self) -> str:
        txt = (
            '--------Query object [q]--------\n'
            'attributes:\n'
            '>>> q.code\n'
            '>>> q.tokens\n'
            '>>> q.ops\n'
            '>>> q.op\n'
            '>>> q.mask_cols\n'
            '>>> q.mask_rows\n'
            '>>> q.mask_vals\n'
            '>>> q.masks_saved\n'
            '>>> q.style_cols\n'
            '>>> q.style_rows\n'
            '>>> q.style_vals\n'
            '>>> q.df\n'
            '>>> q.result  #run query first\n'
            '>>> q.styled  #run query first\n'
            '--------Query object end--------\n'
            )
        return txt


    def scan(
            self,
            verbosity: int | None = None,
            ) -> 'Query':
        return scan(self, verbosity)


    def parse(
            self,
            verbosity: int | None = None,
            ) -> 'Query':
        return parse(self, verbosity)


    def run(
            self,
            verbosity: int | None = None,
            ) -> 'Query':
        return run(self, verbosity)


    def show(self) -> pd.DataFrame | pd.io.formats.style.Styler:
        any_style = (
            self.style_cols is not None
            or self.style_rows is not None
            or self.style_vals is not None
            )
        if any_style:
            return self.styled
        else:
            return self.result



class Symbol(Box):

    #symbol attributes
    id = 0
    name = ''
    category = ''
    regex = ()

    #op validation attributes
    connectors_allowed: dict[str, str] = {}
    scopes_allowed: dict[str, str] = {}
    flags_allowed: dict[str, str] = {}
    args_allowed: dict[str, str] = {}
    args_min = 0
    args_max = 0


    def __init__(self, **kwargs):

        #needed by all symbols
        self.line = ''
        self.linenum = 0
        self.str_matched = ''
        self.literal = ''

        #only needed by op symbols
        self.id = -1
        self.connector: str = ''
        self.scope: str = ''
        self.operator: str = ''
        self.flags: dict[str, str] = {}
        self.args: list[str] = []
        self.list_started = False
        self.list_stopped = False

        super().__init__(**kwargs)


    def __str__(self):
        if self.operator:
            txt = (
                f'--------Operation {self.id}--------\n'
                f'connector: {self.connector!r}\n'
                f'scope: {self.scope!r}\n'
                f'operator: {self.operator!r}\n'
                f'flags: {dict_to_str(self.flags)}\n'
                f'args: {list_to_str(self.args)}\n'
                f'connectors_allowed: {dict_to_str(self.connectors_allowed)}\n'
                f'scopes_allowed: {dict_to_str(self.scopes_allowed)}\n'
                f'flags_allowed: {dict_to_str(self.flags_allowed)}\n'
                f'args_allowed: {dict_to_str(self.args_allowed)}\n'
                f'args_min: {self.args_min}\n'
                f'args_max: {self.args_max}\n'
                )
        else:
            txt = (
                f'----Token {self.id}----\n'
                f'name: {self.name!r}\n'
                f'category: {self.category!r}\n'
                f'regex: {self.regex!r}\n'
                f'linenum: {self.linenum}\n'
                f'str_matched: {self.str_matched!r}\n'
                f'literal: {self.literal!r}\n'
                )
        return txt


    def __repr__(self):
        txt = f'<{self.name!r} {self.str_matched!r}>'
        return txt


    def build(self, str_matched: str) -> 'Symbol':
        token = self.new()
        token.str_matched = str_matched
        return token


    def parse(self, q: Query) -> Query:
        return q


    def run(self, q: Query) -> Query:
        """carries behaviour unique to each op symbol"""
        raise NotImplementedError()


    def getter(
            self,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: typing.Any,
            q: Query,
            ) -> pd.Series[bool]:
        """only used by some op symbols"""
        raise NotImplementedError()


    def setter(
            self,
            series: pd.Series,
            mask: pd.Series[bool],
            args: list[typing.Any],
            q: Query,
            ) -> pd.Series:
        """only used by some op symbols"""
        raise NotImplementedError()


    def styler(self) -> str:
        """only used by some op symbols"""
        raise NotImplementedError()



def scan(
        q: Query,
        verbosity: int | None = None,
        ) -> Query:

    code = q.code
    line = ''
    linenum = 1
    if verbosity is None:
        verbosity = q.verbosity

    q.tokens.append(q.symbol_start)

    while len(code) > 0:
        for symbol in q.symbols_allowed:
            token = _match_symbol(symbol, code)
            if token is not None:
                if token.name == 'Newline':
                    line = ''
                    linenum += 1
                else:
                    line += token.str_matched
                token.id = len(q.tokens)
                token.line = line
                token.linenum = linenum
                q.tokens.append(token)
                code = code[len(token.str_matched):]
                break
        else:
            char = code[0]
            line += char
            msg = f'ERROR: Unrecognized character "{char}"'
            context = build_log_context(
                'scan',
                line=f'"{line}"',
                linenum=linenum,
                )
            log(msg, context, verbosity)
            code = code[1:]

    q.symbol_stop.id = len(q.tokens)
    q.tokens.append(q.symbol_stop)

    msg = f'Debug: scanned code into {len(q.tokens)} tokens.'
    context = build_log_context(
        'scan',
        code=q.code,
        lines=linenum,
        tokens=[token.name for token in q.tokens],
        )
    log(msg, context, verbosity)
    return q


def _match_symbol(
        symbol,
        code: str,
        ) -> 'None | Symbol':
    for regex in symbol.regex:
        matched = re.match(regex, code)
        if matched:
            return symbol.build(matched.group())
    return None



def parse(
        q: Query,
        verbosity: int | None = None,
        ) -> Query:

    if verbosity is None:
        verbosity = q.verbosity

    for token in q.tokens:
        q = token.parse(q)

    msg = f'Debug: parsed tokens into {len(q.ops)} ops.'
    context = build_log_context(
        'parse',
        ops=[op.operator for op in q.ops],
        )
    log(msg, context, verbosity)
    return q



def run(
        q: Query,
        verbosity: int | None = None,
        ) -> Query:

    if verbosity is None:
        verbosity = q.verbosity

    for op in q.ops:
        q = op.run(q)
        _validate_dtypes(op, q, verbosity)

    q.result = q.df.loc[q.mask_rows, q.mask_cols]
    q.styled = _apply_styles(
        q.result,
        q,
        verbosity,
        )

    msg = f'Debug: ran {len(q.ops)} ops.'
    context = build_log_context('run')
    log(msg, context, verbosity)
    return q


def _validate_dtypes(
        op: Symbol,
        q: Query,
        verbosity: int,
        ) -> None:

    dtypes_current = set(q.df.dtypes.astype(str).unique())
    if not dtypes_current.issubset(DTYPES_ALLOWED):
        msg = 'WARNING: op resulted in invalid dtypes.'
        context = build_log_context(
            '_run_op',
            op=op,
            dtypes_current=dtypes_current,
            dtypes_allowed=DTYPES_ALLOWED,
            )
        log(msg, context, verbosity)

    return None



def _apply_styles(
        result: pd.DataFrame,
        q: 'Query',
        verbosity: int = 3,
        ) -> pd.io.formats.style.Styler:

    styled = result.style

    if q.style_cols is not None:
        style_cols = q.style_cols[q.mask_cols].to_list()
        styled = styled.apply_index(
            lambda x: style_cols,
            axis=1,
            )

    if q.style_rows is not None:
        style_rows = q.style_rows[q.mask_rows].to_list()
        styled = styled.apply_index(
            lambda x: style_rows,
            axis=0,
            )

    if q.style_vals is not None:
        style_vals = (
            q.style_vals
            [q.mask_vals]
            .loc[q.mask_rows, q.mask_cols]
            )
        styled = styled.apply(
            lambda x: style_vals,
            axis=None,
            )

    return styled
