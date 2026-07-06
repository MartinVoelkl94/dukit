
import pandas as pd
import numpy as np
import typing
import re

from ..util import (
    log,
    build_log_context,
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
        self.op = Operation()

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


    def str_debug(self) -> str:
        txt_tokens = [token.name for token in self.tokens]
        txt_ops = [op.operator for op in self.ops]
        txt = (
            'Query object [q] with attributes:\n\n\n'
            f'>>> q.df\n{self.df}\n\n\n'
            f'>>> q.mask_cols\n{self.mask_cols}\n\n\n'
            f'>>> q.mask_rows\n{self.mask_rows}\n\n\n'
            f'>>> q.mask_vals\n{self.mask_vals}\n\n\n'
            f'>>> q.masks_saved\n{self.masks_saved}\n\n\n'
            f'>>> q.style_cols\n{self.style_cols}\n\n\n'
            f'>>> q.style_rows\n{self.style_rows}\n\n\n'
            f'>>> q.style_vals\n{self.style_vals}\n\n\n'
            f'>>> q.code\n{self.code!r}\n\n\n'
            f'>>> q.tokens\n{txt_tokens}\n\n\n'
            f'>>> q.ops\n{txt_ops}\n\n\n'
            f'>>> q.op\n{self.op.str_debug()}\n\n\n'
            )
        return txt



class Symbol(Box):

    #symbol attributes
    id = 0
    name = ''
    category = ''
    regex = ()

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {}
    op_scopes_allowed = {}
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def __init__(self, **kwargs):
        self.line = ''
        self.linenum = 0
        self.str_matched = ''
        self.literal = ''
        super().__init__(**kwargs)


    def __str__(self):

        spacer = '\n    '
        if len(self.regex) > 1:
            str_regex = spacer + spacer.join(self.regex)
        else:
            str_regex = str(self.regex)

        if len(self.op_flags) > 1:
            kvs = (
                f'{k}: {v}'
                for k, v in
                self.op_flags.items()
                )
            op_flags_str = spacer + spacer.join(kvs)
        else:
            op_flags_str = str(self.op_flags)

        txt = (
            f'Token {self.id}:\n'
            f'  name: {self.name}\n'
            f'  category: {self.category}\n'
            f'  regex: {str_regex}\n'
            f'  linenum: {self.linenum}\n'
            f'  str_matched: {self.str_matched}\n'
            f'  literal: {self.literal}\n'
            f'  op_flags: {op_flags_str}\n'
            )
        return txt


    def str_debug(self) -> str:
        return self.__str__()

    def build(self, str_matched: str) -> 'Symbol':
        token = self.copy()
        token.str_matched = str_matched
        return token

    def parse(
            self,
            q: Query,
            ) -> Query:
        return q


    def getter(
            self,
            op: 'Operation',
            series: pd.Series,
            mask: pd.Series[bool],
            arg: typing.Any,
            q: Query,
            ) -> pd.Series:
        raise NotImplementedError()


    def setter(
            self,
            op: 'Operation',
            series: pd.Series,
            mask: pd.Series[bool],
            args: list[typing.Any],
            q: Query,
            ) -> pd.Series:
        raise NotImplementedError()


    def shaper(
            self,
            op: 'Operation',
            q: Query,
            ) -> Query:
        raise NotImplementedError()


    def styler(
            self,
            op: 'Operation',
            q: Query,
            ) -> str:
        raise NotImplementedError()


    def viewer(
            self,
            op: 'Operation',
            q: Query,
            ) -> Query:
        raise NotImplementedError()



class Operation(Box):


    def __init__(self):

        #main attributes
        self.id = 'current'
        self.category = ''
        self.connector: str = ''
        self.scope: str = ''
        self.operator: str = ''
        self.flags: dict[str, str] = {}
        self.args: list[str] = []

        #for validation
        self.connectors_allowed: dict[str, str] = {}
        self.scopes_allowed: dict[str, str] = {}
        self.flags_allowed: dict[str, str] = {}
        self.args_allowed: dict[str, str] = {}
        self.args_min: int = 0
        self.args_max: int = 0
        self.list_started = False
        self.list_stopped = False


    def __str__(self):

        spacer = '\n    '
        if len(self.args) > 1:
            str_args = spacer + spacer.join(self.args)
        else:
            str_args = str(self.args)

        if len(self.flags) > 1:
            kvs = (
                f'{k}: {v}'
                for k, v in
                self.flags.items()
                )
            str_flags = spacer + spacer.join(kvs)
        else:
            str_flags = str(self.flags)

        # if len(self.flags_allowed) > 1:
        #     kvs = (
        #         f'{k}: {v}'
        #         for k, v in
        #         self.flags_allowed.items()
        #         )
        #     str_flags_allowed = spacer + spacer.join(kvs)
        # else:
        #     str_flags_allowed = str(self.flags_allowed)

        txt = (
            f'Operation {self.id}:\n'
            f'  connector: {self.connector}\n'
            f'  scope: {self.scope}\n'
            f'  operator: {self.operator}\n'
            f'  args: {str_args}\n'
            f'  flags: {str_flags}\n'
            # f'\targs_min: {self.args_min}\n'
            # f'\targs_max: {self.args_max}\n'
            # f'\tconnectors_allowed: {self.connectors_allowed}\n'
            # f'\tscopes_allowed: {self.scopes_allowed}\n'
            # f'\tflags_allowed: {str_flags_allowed}\n'
            )
        return txt


    def str_debug(self) -> str:
        return self.__str__()


    def getter(
            self,
            op: 'Operation',
            series: pd.Series,
            mask: pd.Series[bool],
            arg: typing.Any,
            q: Query,
            ) -> pd.Series:
        raise NotImplementedError()


    def setter(
            self,
            op: 'Operation',
            series: pd.Series,
            mask: pd.Series[bool],
            args: list[typing.Any],
            q: Query,
            ) -> pd.Series:
        raise NotImplementedError()


    def shaper(
            self,
            op: 'Operation',
            q: Query,
            ) -> Query:
        raise NotImplementedError()


    def styler(
            self,
            op: 'Operation',
            q: Query,
            ) -> str:
        raise NotImplementedError()


    def viewer(
            self,
            op: 'Operation',
            q: Query,
            ) -> Query:
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
        q = _run_op(op, q, verbosity)

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



def _run_op(
        op: Operation,
        q: Query,
        verbosity: int | None = None,
        ) -> Query:

    if verbosity is None:
        verbosity = q.verbosity

    if op.category == 'getter':
        if op.scope == 'cols':
            q = _get_cols(op, q)
        elif op.scope == 'rows':
            q = _get_rows(op, q)
        elif op.scope == 'vals':
            q = _get_vals(op, q)

    elif op.category == 'setter':
        if op.scope == 'cols':
            q = _set_cols(op, q)
        elif op.scope == 'rows':
            q = _set_rows(op, q)
        elif op.scope == 'vals':
            q = _set_vals(op, q)

    elif op.category == 'shaper':
        q = op.shaper(op, q)

    elif op.category == 'styler':
        q = _add_styles(op, q)

    elif op.category == 'viewer':
        q = op.viewer(op, q)

    else:
        msg = 'ERROR: op has no valid operator.'
        context = build_log_context(
            '_run_op',
            op=op.str_debug(),
            )
        log(msg, context, verbosity)

    _validate_dtypes(q, op, verbosity)

    return q


def _validate_dtypes(
        q: Query,
        op: Operation,
        verbosity: int,
        ) -> None:

    dtypes_current = set(q.df.dtypes.astype(str).unique())
    if not dtypes_current.issubset(DTYPES_ALLOWED):
        msg = 'WARNING: op resulted in invalid dtypes.'
        context = build_log_context(
            '_run_op',
            op=op.str_debug(),
            dtypes_current=dtypes_current,
            dtypes_allowed=DTYPES_ALLOWED,
            )
        log(msg, context, verbosity)

    return None



def _get_cols(
        op: Operation,
        q: Query,
        ) -> Query:

    context = build_log_context(
        '_get_cols',
        selected_cols=int(q.mask_cols.sum()),
        selected_rows=int(q.mask_rows.sum()),
        selected_vals=int(q.mask_vals.sum().sum()),
        op=op.str_debug(),
        )


    if 'index' in op.flags:
        _temp = {col: i for i, col in enumerate(q.df.columns)}
        data = pd.Series(_temp)
    else:
        data = pd.Series(
            q.df.columns,
            index=q.df.columns,
            )


    mask_cols_new = _apply_getter(
        data=data,
        mask_current=q.mask_cols,
        op=op,
        q=q,
        )

    if op.connector == 'new':
        q.mask_cols = mask_cols_new
    elif op.connector == 'and':
        q.mask_cols &= mask_cols_new
    elif op.connector == 'or':
        q.mask_cols |= mask_cols_new

    if op.operator != 'GetTrimmedSelection':
        q.mask_vals.loc[:, :] = False
        q.mask_vals.loc[q.mask_rows, q.mask_cols] = True


    if bool(mask_cols_new.any()) is False:  #.any() returns np.True_ or np.False_
        msg = 'WARNING: no cols fulfill the condition in current op.'
        log(msg, context, q.verbosity)

    no_overlap = (
        bool(q.mask_cols.any()) is False
        and op.connector == 'and'
        )
    if no_overlap:
        msg = (
            'WARNING: no cols fulfill the condition in '
            'current op and the previous condition(s).'
            )
        log(msg, context, q.verbosity)
    return q



def _get_rows(
        op: Operation,
        q: Query,
        ) -> Query:

    context = build_log_context(
        '_get_rows',
        selected_cols=int(q.mask_cols.sum()),
        selected_rows=int(q.mask_rows.sum()),
        selected_vals=int(q.mask_vals.sum().sum()),
        op=op.str_debug(),
        )

    if bool(q.mask_cols.any()) is False:
        msg = (
            'ERROR: row selection cannot be applied'
            ' when the current col selection is empty.'
            )
        log(msg, context, q.verbosity)
        return q


    mask_vals_new = pd.DataFrame(
        np.zeros(q.df.shape, dtype=bool),
        columns=q.df.columns,
        index=q.df.index
        )

    for icol, col in enumerate(q.df.columns[q.mask_cols]):

        if 'index' in op.flags:
            data = q.df.index.to_series()
        else:
            data = q.df[col]

        mask_current = q.mask_vals[col]
        mask_new = _apply_getter(
            data=data,
            mask_current=mask_current,
            op=op,
            q=q,
            )
        mask_vals_new[col] = mask_new

        if icol == 0:
            mask_rows = mask_new
        elif 'allcols' in op.flags:
            mask_rows = mask_rows & mask_new
        else:
            mask_rows = mask_rows | mask_new

    if op.connector == 'new':
        q.mask_rows = mask_rows
        q.mask_vals = mask_vals_new
    elif op.connector == 'and':
        q.mask_rows &= mask_rows
        q.mask_vals &= mask_vals_new
    elif op.connector == 'or':
        q.mask_rows |= mask_rows
        q.mask_vals |= mask_vals_new


    return q



def _get_vals(
        op: Operation,
        q: Query,
        ) -> Query:

    context = build_log_context(
        '_get_vals',
        selected_cols=int(q.mask_cols.sum()),
        selected_rows=int(q.mask_rows.sum()),
        selected_vals=int(q.mask_vals.sum().sum()),
        op=op.str_debug(),
        )

    if bool(q.mask_cols.any()) is False:
        msg = (
            'ERROR: val selection cannot be applied'
            ' when the current col selection is empty.'
            )
        log(msg, context, q.verbosity)
        return q

    if bool(q.mask_rows.any()) is False:
        msg = (
            'ERROR: val selection cannot be applied'
            ' when the current row selection is empty.'
            )
        log(msg, context, q.verbosity)
        return q


    mask_vals_new = pd.DataFrame(
        np.zeros(q.df.shape, dtype=bool),
        columns=q.df.columns,
        index=q.df.index
        )

    for col in q.df.columns[q.mask_cols]:

        data = q.df.loc[q.mask_rows, col]
        mask_current = q.mask_vals.loc[q.mask_rows, col]
        mask_new = _apply_getter(
            data=data,
            mask_current=mask_current,
            op=op,
            q=q,
            )

        mask_vals_new.loc[q.mask_rows, col] = mask_new

    if op.connector == 'new':
        q.mask_vals = mask_vals_new
    elif op.connector == 'and':
        q.mask_vals &= mask_vals_new
    elif op.connector == 'or':
        q.mask_vals |= mask_vals_new


    return q



def _apply_getter(
        data: pd.Series,
        mask_current: pd.Series,
        op: Operation,
        q: Query,
        ) -> pd.Series:

    mask_current = mask_current.copy()

    valid_edgecase = (
        len(op.args) == 0
        and op.args_max == 0
        )
    if valid_edgecase:
        msg = 'Trace: normalizing zero-arg getter to a single empty arg.'
        context = build_log_context(
            '_apply_getter',
            op=op.str_debug(),
            )
        log(msg, context, q.verbosity)
        op.args = ['']

    for i, arg in enumerate(op.args):

        mask_temp = op.getter(
            op,
            data,
            mask_current,
            arg,
            q,
            ).fillna(False)

        if len(mask_temp) != len(mask_current):
            msg = 'ERROR: getter returned invalid mask.'
            context = build_log_context(
                '_apply_getter',
                mask_length=len(mask_temp),
                expected_length=len(mask_current),
                mask=mask_temp,
                op=op.str_debug(),
                )
            log(msg, context, q.verbosity)
            continue

        if 'negate' in op.flags:
            mask_temp = ~mask_temp

        if i == 0:
            mask_current = mask_temp
        elif 'any' in op.flags:
            mask_current = mask_current | mask_temp
        elif 'all' in op.flags:
            mask_current = mask_current & mask_temp
        else:
            mask_current = mask_current & mask_temp

    return mask_current



def _set_cols(
        op: Operation,
        q: Query,
        ) -> Query:

    context = build_log_context(
        '_set_cols',
        selected_cols=int(q.mask_cols.sum()),
        selected_rows=int(q.mask_rows.sum()),
        selected_vals=int(q.mask_vals.sum().sum()),
        op=op.str_debug(),
        )

    if bool(q.mask_cols.any()) is False:
        msg = (
            'ERROR: cannot set cols when the'
            ' current col selection is empty.'
            )
        log(msg, context, q.verbosity)
        return q

    cols_all = q.df.columns.to_series().copy()
    cols_new = op.setter(
        op,
        cols_all,
        q.mask_cols,
        op.args,
        q,
        ).convert_dtypes()

    q.df.columns = cols_new
    q.mask_cols.index = cols_new
    q.mask_vals.columns = cols_new

    if q.style_cols is not None:
        q.style_cols.index = cols_new
    if q.style_vals is not None:
        q.style_vals.columns = cols_new

    return q



def _set_rows(
        op: Operation,
        q: Query,
        ) -> Query:

    context = build_log_context(
        '_set_rows',
        selected_cols=int(q.mask_cols.sum()),
        selected_rows=int(q.mask_rows.sum()),
        selected_vals=int(q.mask_vals.sum().sum()),
        op=op.str_debug(),
        )

    if bool(q.mask_rows.any()) is False:
        msg = (
            'ERROR: cannot set rows when the'
            ' current row selection is empty.'
            )
        log(msg, context, q.verbosity)
        return q

    rows_all = q.df.index.to_series().copy()
    rows_new = op.setter(
        op,
        rows_all,
        q.mask_rows,
        op.args,
        q,
        ).convert_dtypes()
    q.df.index = rows_new
    q.mask_rows.index = rows_new
    q.mask_vals.index = rows_new

    if q.style_rows is not None:
        q.style_rows.index = rows_new
    if q.style_vals is not None:
        q.style_vals.index = rows_new

    return q



def _set_vals(
        op: Operation,
        q: Query,
        ) -> Query:

    context = build_log_context(
        '_set_vals',
        selected_cols=int(q.mask_cols.sum()),
        selected_rows=int(q.mask_rows.sum()),
        selected_vals=int(q.mask_vals.sum().sum()),
        op=op.str_debug(),
    )

    if bool(q.mask_cols.any()) is False:
        msg = (
            'ERROR: cannot set vals when the'
            ' current col selection is empty.'
            )
        log(msg, context, q.verbosity)
        return q

    if bool(q.mask_rows.any()) is False:
        msg = (
            'ERROR: cannot set vals when the'
            ' current row selection is empty.'
            )
        log(msg, context, q.verbosity)
        return q

    if bool(q.mask_vals.any().any()) is False:
        msg = (
            'ERROR: cannot set vals when the'
            ' current val selection is empty.'
            )
        log(msg, context, q.verbosity)
        return q


    for col in q.df.columns[q.mask_cols]:
        mask_vals_col = q.mask_vals[col]
        mask_vals_col_rows = mask_vals_col & q.mask_rows

        if bool(mask_vals_col_rows.any()) is False:
            #this is expected and therefore should not throw an error
            msg = (
                'TRACE: cannot set vals when'
                f' the current val selection'
                f' for col "{col}" is empty.'
                )
            log(msg, context, q.verbosity)
            continue

        vals_col = q.df[col].copy()
        row_vals_new = op.setter(
            op,
            vals_col,
            mask_vals_col_rows,
            op.args,
            q,
            ).convert_dtypes()
        q.df[col] = row_vals_new

    return q



def _add_styles(
        op: Operation,
        q: Query,
        ) -> Query:

    if q.style_cols is None:
        q.style_cols = pd.Series(
            '',
            index=q.df.columns,
            )
    if q.style_rows is None:
        q.style_rows = pd.Series(
            '',
            index=q.df.index,
            )
    if q.style_vals is None:
        q.style_vals = pd.DataFrame(
            '',
            index=q.df.index,
            columns=q.df.columns,
            )

    style_str = op.styler(op, q)

    if op.scope == 'cols':
        q.style_cols[q.mask_cols] += style_str

    elif op.scope == 'rows':
        q.style_rows[q.mask_rows] += style_str

    elif op.scope == 'vals':
        mask_combined = q.mask_vals.copy()
        mask_combined.loc[~q.mask_rows, :] = False
        mask_combined.loc[:, ~q.mask_cols] = False
        rows_all = q.style_vals.index
        cols_all = q.style_vals.columns
        style_new = pd.DataFrame(
            '',
            index=rows_all,
            columns=cols_all,
            )
        style_new = style_new.mask(
            mask_combined,
            style_str,
            )
        q.style_vals += style_new

    return q



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
