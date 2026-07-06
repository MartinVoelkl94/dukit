
import pandas as pd
import numpy as np
import typing
import re

from IPython.display import display
from IPython.core.getipython import get_ipython


from .engine import (
    Query,
    Symbol,
    Operation,
    )
from ..util import (
    log,
    build_log_context,
    ensure_unique_string,
    )
from ..typing import (
    TYPES_STR,
    TYPES_INT,
    TYPES_FLOAT,
    TYPES_NUM,
    TYPES_BOOL,
    TYPES_DATE,
    _type,
    _convert,
    _repr,
    _typeinfo,
    _typeinfostrict,
    _int,
    _float,
    _num,
    _bool,
    _date,
    _datetime,
    _na,
    _nk,
    _yn,
    )





#when parsing code, symbols are checked
#in the order they are defined here, e.g.:
#'==' must be before '='




class QueryStart(Symbol):
    """
    pseudo-symbol that marks
    the start of a query.
    """
    name = 'QueryStart'
    category = 'pseudo'
    regex = ()




class QueryStop(Symbol):
    """
    pseudo-symbol that marks
    the end of a query.
    """
    name = 'QueryStop'
    category = 'pseudo'
    regex = ()

    def parse(self, q: Query) -> Query:
        return _preparse_for_scope(q)




class Newline(Symbol):
    """
    dispatches current op
    and starts a new one.
    """
    name = 'Newline'
    category = 'syntax'
    regex = (r'\n',)

    def parse(self, q: Query) -> Query:
        return _preparse_for_scope(q)




class ScopeValsNew(Symbol):
    """
    either:
    - set vals
    - get vals, replacing the previous val selection

    Examples
    --------
    >>> qs(df, r'%%%:isint')
    >>> qs(df, r'height /weight  %%%:isint')  #integer vals in height and weight cols
    """
    name = 'ScopeValsNew'
    category = 'scope'
    regex = (r'%%%',)

    def parse(self, q: Query) -> Query:
        q = _preparse_for_scope(q)
        q.op.connector = 'new'
        q.op.scope = 'vals'
        return q




class ScopeValsAnd(Symbol):
    """
    get val selection fulfilling this
    AND the previous condition(s).

    Examples
    --------
    >>> qs(df, r'%%%:isint  &&&>0')  #integer vals above 0
    """
    name = 'ScopeValsAnd'
    category = 'scope'
    regex = (r'&&&',)

    def parse(self, q: Query) -> Query:
        q = _preparse_for_scope(q)
        q.op.connector = 'and'
        q.op.scope = 'vals'
        return q




class ScopeValsOr(Symbol):
    """
    get val selection fulfilling this
    OR the previous condition(s).

    Examples
    --------
    >>> qs(df, r'%%%:isint  ///:isna')  #integer or na vals
    """
    name = 'ScopeValsOr'
    category = 'scope'
    regex = (r'\/\/\/',)

    def parse(self, q: Query) -> Query:
        q = _preparse_for_scope(q)
        q.op.connector = 'or'
        q.op.scope = 'vals'
        return q




class ScopeRowsNew(Symbol):
    """
    either:
    - set rows
    - get rows, replacing the previous row selection

    Examples
    --------
    >>> qs(df, r'age  %%>30')
    """
    name = 'ScopeRowsNew'
    category = 'scope'
    regex = (r'%%',)

    def parse(self, q: Query) -> Query:
        q = _preparse_for_scope(q)
        q.op.connector = 'new'
        q.op.scope = 'rows'
        return q




class ScopeRowsAnd(Symbol):
    """
    get row selection fulfilling this
    AND the previous condition(s).

    Examples
    --------
    >>> qs(df, r'age  %%>30  &&<50')  #rows where age >30 and <50
    """
    name = 'ScopeRowsAnd'
    category = 'scope'
    regex = (r'&&',)

    def parse(self, q: Query) -> Query:
        q = _preparse_for_scope(q)
        q.op.connector = 'and'
        q.op.scope = 'rows'
        return q




class ScopeRowsOr(Symbol):
    """
    get row selection fulfilling this
    OR the previous condition(s).

    Examples
    --------
    >>> qs(df, r'name  %%?a  //?b')  #rows where name contains "a" OR "b"
    """
    name = 'ScopeRowsOr'
    category = 'scope'
    regex = (r'\/\/',)

    def parse(self, q: Query) -> Query:
        q = _preparse_for_scope(q)
        q.op.connector = 'or'
        q.op.scope = 'rows'
        return q




class ScopeColsNew(Symbol):
    """
    either:
    - set cols
    - get cols, replacing the previous col selection

    Examples
    --------
    >>> qs(df, r'%==age')
    """
    name = 'ScopeColsNew'
    category = 'scope'
    regex = (r'%',)

    def parse(self, q: Query) -> Query:
        q = _preparse_for_scope(q)
        q.op.connector = 'new'
        q.op.scope = 'cols'
        return q




class ScopeColsAnd(Symbol):
    """
    get col selection fulfilling this
    AND the previous condition(s).

    Examples
    --------
    >>> qs(df, r'%?a  &?e')  #cols containing "a" AND "e"
    """
    name = 'ScopeColsAnd'
    category = 'scope'
    regex = (r'&',)

    def parse(self, q: Query) -> Query:
        q = _preparse_for_scope(q)
        q.op.connector = 'and'
        q.op.scope = 'cols'
        return q




class ScopeColsOr(Symbol):
    """
    get col selection fulfilling this
    OR the previous condition(s).

    Examples
    --------
    >>> qs(df, r'%?a  /?e')  #cols containing "a" OR "e"
    """
    name = 'ScopeColsOr'
    category = 'scope'
    regex = (r'\/',)

    def parse(self, q: Query) -> Query:
        q = _preparse_for_scope(q)
        q.op.connector = 'or'
        q.op.scope = 'cols'
        return q



def _preparse_for_scope(q: Query) -> Query:

    if q.op.scope and not q.op.operator:
        msg = 'Trace: inferring GetAll operator for scope-only op.'
        context = build_log_context(
            '_preparse_for_scope',
            op=q.op.str_debug(),
            )
        log(msg, context, q.verbosity)
        q = GetAll().parse(q)
        q = _process_op(q)

    else:
        q = _process_op(q)

    return q



def _process_op(q: Query) -> Query:

    if q.op == Operation():
        return q

    context = build_log_context(
        '_process_op',
        op=q.op.str_debug(),
        )
    valid = True

    validation_functions = [
        _validate_op_essentials,
        _validate_op_flags_allowed,
        _validate_op_flags_type,
        _validate_op_flags,
        _validate_op_args_allowed,
        _validate_op_args,
        ]
    for func in validation_functions:
        valid = func(q, valid, context)

    if valid:
        msg = 'Trace: saving valid op.'
        log(msg, context, q.verbosity)
        q.op.id = str(len(q.ops))
        q.ops.append(q.op)
        q.op = Operation()
    else:
        msg = 'Trace: discarding invalid op.'
        log(msg, context, q.verbosity)
        q.op = Operation()

    return q



def _validate_op_essentials(
        q: Query,
        valid: bool,
        context: str,
        ) -> bool:

    if not q.op.connector:
        msg = 'ERROR: op is missing a connector.'
        log(msg, context, q.verbosity)
        valid = False

    if not q.op.scope:
        msg = 'ERROR: op is missing a scope.'
        log(msg, context, q.verbosity)
        valid = False

    if not q.op.operator:
        msg = 'ERROR: op is missing an operator.'
        log(msg, context, q.verbosity)
        valid = False

    if q.op.connector not in q.op.connectors_allowed:
        msg = 'ERROR: op has an invalid connector.'
        log(msg, context, q.verbosity)
        valid = False

    if q.op.scope not in q.op.scopes_allowed:
        msg = 'ERROR: op has an invalid scope.'
        log(msg, context, q.verbosity)
        valid = False

    return valid



def _validate_op_flags_allowed(
        q: Query,
        valid: bool,
        context: str,
        ) -> bool:

    for flag in q.op.flags.keys():
        if flag not in q.op.flags_allowed:
            msg = f'ERROR: flag "{flag}" is not valid for op.'
            context = build_log_context(
                '_process_op',
                op=q.op.str_debug(),
                allowed_flags=q.op.flags_allowed,
                )
            log(msg, context, q.verbosity)
            valid = False

    return valid



def _validate_op_flags_type(
        q: Query,
        valid: bool,
        context: str,
        ) -> bool:

    _flags_type = {
        'int',
        'float',
        'num',
        'str',
        'bool',
        'date',
        'datetime',
        }
    flags_type_found = _flags_type.intersection(q.op.flags)
    if len(flags_type_found) > 1:
        msg = 'ERROR: multiple type flags are not allowed in the same op.'
        log(msg, context, q.verbosity)
        valid = False

    return valid



def _validate_op_flags(
        q: Query,
        valid: bool,
        context: str,
        ) -> bool:

    if 'index' in q.op.flags and q.op.scope not in ('rows', 'cols'):
        msg = (
            'ERROR: flag "index" is only valid for'
            r' scopes "%", "&", "/", "%%", "&&", "//".'
            )
        log(msg, context, q.verbosity)
        valid = False

    if 'allcols' in q.op.flags:
        if q.op.category != 'getter':
            msg = 'ERROR: "allcols" flag is only valid for getter ops.'
            log(msg, context, q.verbosity)
            valid = False
        if q.op.scope != 'rows':
            msg = r'ERROR: "allcols" flag is only valid for scopes "%%", "&&", "//".'
            log(msg, context, q.verbosity)
            valid = False

    if 'colref' in q.op.flags:
        if q.op.category == 'setter' and q.op.scope != 'vals':
            msg = r'ERROR: "colref" flag is only valid for setter ops with scope "%%%".'
            log(msg, context, q.verbosity)
            valid = False
        if q.op.category == 'getter' and q.op.scope == 'cols':
            msg = (
                'ERROR: "colref" flag is only valid for getter ops'
                r' with scopes "%%", "&&", "//", "%%%", "&&&", "///".'
                )
            log(msg, context, q.verbosity)
            valid = False

    return valid



def _validate_op_args_allowed(
        q: Query,
        valid: bool,
        context: str,
        ) -> bool:

    if q.op.args_allowed:
        for arg in q.op.args:
            if arg not in q.op.args_allowed:
                msg = f'ERROR: arg "{arg}" is not valid for op.'
                context = build_log_context(
                    '_process_op',
                    op=q.op.str_debug(),
                    allowed_args=q.op.args_allowed,
                    )
                log(msg, context, q.verbosity)
                valid = False

    return valid



def _validate_op_args(
        q: Query,
        valid: bool,
        context: str,
        ) -> bool:

    if len(q.op.args) < q.op.args_min:
        msg = 'ERROR: op has too few args.'
        log(msg, context, q.verbosity)
        valid = False

    if len(q.op.args) > q.op.args_max:
        msg = 'ERROR: op has too many args.'
        log(msg, context, q.verbosity)
        valid = False

    return valid




def _get_equals(
        op: Operation,
        series: pd.Series,
        arg: str,
        q: Query,
        ) -> pd.Series:

    if 'regex' in op.flags:
        series = series.astype('string')
        mask = series.str.fullmatch(arg)

    elif 'colref' in op.flags:
        series_other = _process_colref(
            series,
            arg,
            op,
            q,
            )
        series, series_other = _process_types_series(
            series,
            series_other,
            op,
            q,
            )
        mask = series == series_other

    else:
        series, arg = _process_types(
            series,
            arg,
            op,
            q,
            )
        mask = series == arg

    mask = mask.fillna(False)
    return mask




class GetEquals(Symbol):
    """
    get cols/rows/vals if
    they are equal to an arg.

    Examples
    --------
    >>> qs(df, r'age  ==30')
    """

    #symbol attributes
    name = 'GetEquals'
    category = 'getter'
    regex = (r'==',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'regex': 'parse arg as regex',
        'colref': 'parse arg as col reference',

        'index': 'condition is applied to index instead of vals',
        'any': 'condition must apply to any args',
        'all': 'condition must apply to all args',
        'allcols': 'get rows where condition applies in all selected cols',

        'strict': 'strict type comparison/conversion',
        'str': 'string type comparison',
        'int': 'integer type comparison',
        'float': 'float type comparison',
        'num': 'numeric type comparison',
        'bool': 'boolean type comparison',
        'date': 'date type comparison',
        'datetime': 'datetime type comparison',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1_000_000


    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q


    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        mask = _get_equals(
            op,
            series,
            arg,
            q,
            )
        return mask




class GetNotEquals(Symbol):
    """
    get cols/rows/vals if they
    are not equal to an arg.

    Examples
    --------
    >>> qs(df, r'age  !=30')
    """

    #symbol attributes
    name = 'GetNotEquals'
    category = 'getter'
    regex = (r'!=',)

    #used to build the current op
    op_flags = GetEquals.op_flags

    #used to validate the current op
    op_connectors_allowed = GetEquals.op_connectors_allowed
    op_scopes_allowed = GetEquals.op_scopes_allowed
    op_flags_allowed = GetEquals.op_flags_allowed
    op_args_allowed = GetEquals.op_args_allowed
    op_args_min = GetEquals.op_args_min
    op_args_max = GetEquals.op_args_max

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        mask = _get_equals(
            op,
            series,
            arg,
            q,
            )
        return ~mask




class GetContains(Symbol):
    """
    get cols/rows/vals if
    they contain an arg.

    Examples
    --------
    >>> qs(df, r'name  ?john')
    """

    #symbol attributes
    name = 'GetContains'
    category = 'getter'
    regex = (r'\?',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'regex': 'parse arg as regex',

        'index': 'condition is applied to index instead of vals',
        'any': 'condition must apply to any args',
        'all': 'condition must apply to all args',
        'allcols': 'get rows where condition applies in all selected cols',

        'strict': 'strict type comparison/conversion',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1_000_000


    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q


    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:

        series = series.astype('string')

        if 'regex' in op.flags:
            mask = series.str.contains(arg, regex=True)

        elif 'strict' in op.flags:
            mask = series.str.contains(arg, regex=False)

        else:
            series = series.str.lower()
            arg = arg.lower()
            mask = series.str.contains(arg, regex=False)

        return mask




class GetGreaterEqual(Symbol):
    """
    get cols/rows/vals if
    they are greater than
    or equal to an arg.

    Examples
    --------
    >>> qs(df, r'age  >=30')
    """

    #symbol attributes
    name = 'GetGreaterEqual'
    category = 'getter'
    regex = (r'>=',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'colref': 'parse arg as col reference',

        'index': 'condition is applied to index instead of vals',
        'any': 'condition must apply to any args',
        'all': 'condition must apply to all args',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1_000_000


    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q


    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:

        if 'colref' in op.flags:
            series_other = _process_colref(
                series,
                arg,
                op,
                q,
                )
            series, series_other = _process_types_series(
                series,
                series_other,
                op,
                q,
                )
            mask = series >= series_other

        else:
            series, arg = _process_types(
                series,
                arg,
                op,
                q,
                )
            mask = series >= arg

        return mask




class GetSmallerEqual(Symbol):
    """
    get cols/rows/vals if
    they are smaller than
    or equal to an arg.

    Examples
    --------
    >>> qs(df, r'age  <=30')
    """

    #symbol attributes
    name = 'GetSmallerEqual'
    category = 'getter'
    regex = (r'<=',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'colref': 'parse arg as col reference',

        'index': 'condition is applied to index instead of vals',
        'any': 'condition must apply to any args',
        'all': 'condition must apply to all args',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1_000_000


    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q


    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:

        if 'colref' in op.flags:
            series_other = _process_colref(
                series,
                arg,
                op,
                q,
                )
            series, series_other = _process_types_series(
                series,
                series_other,
                op,
                q,
                )
            mask = series <= series_other

        else:
            series, arg = _process_types(
                series,
                arg,
                op,
                q,
                )
            mask = series <= arg

        return mask




class GetGreater(Symbol):
    """
    get cols/rows/vals if
    they are greater than an arg.

    Examples
    --------
    >>> qs(df, r'age  >30')
    """

    #symbol attributes
    name = 'GetGreater'
    category = 'getter'
    regex = (r'>',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'colref': 'parse arg as col reference',

        'index': 'condition is applied to index instead of vals',
        'any': 'condition must apply to any args',
        'all': 'condition must apply to all args',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1_000_000


    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q


    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:

        if 'colref' in op.flags:
            series_other = _process_colref(
                series,
                arg,
                op,
                q,
                )
            series, series_other = _process_types_series(
                series,
                series_other,
                op,
                q,
                )
            mask = series > series_other

        else:
            series, arg = _process_types(
                series,
                arg,
                op,
                q,
                )
            mask = series > arg

        return mask




class GetSmaller(Symbol):
    """
    get cols/rows/vals if
    they are smaller than an arg.

    Examples
    --------
    >>> qs(df, r'age  <30')
    """

    #symbol attributes
    name = 'GetSmaller'
    category = 'getter'
    regex = (r'<',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'colref': 'parse arg as col reference',

        'index': 'condition is applied to index instead of vals',
        'any': 'condition must apply to any args',
        'all': 'condition must apply to all args',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1_000_000


    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q


    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:

        if 'colref' in op.flags:
            series_other = _process_colref(
                series,
                arg,
                op,
                q,
                )
            series, series_other = _process_types_series(
                series,
                series_other,
                op,
                q,
                )
            mask = series < series_other

        else:
            series, arg = _process_types(
                series,
                arg,
                op,
                q,
                )
            mask = series < arg

        return mask




class GetEval(Symbol):
    """
    get all cols/rows/vals where a custom
    python expression evaluates to True.

    "x" can be used in the expression
    to refer to the current item.

    Examples
    --------
    >>> qs(df, r'%:eval("len(x) > 3")')  #cols with names longer than 3 characters
    """

    #symbol attributes
    name = 'GetEval'
    category = 'getter'
    regex = (
        r':apply',
        r':eval',
        r':map',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:

        expression = arg

        def custom_func(x):
            namespace = {
                'x': x,
                'df': q.df,
                'pd': pd,
                'np': np,
                're': re,
                }
            return eval(expression, namespace)

        mask = series.apply(lambda x: custom_func(x)).astype(bool)

        return mask




class GetSavedSelection(Symbol):
    """
    load a previously saved selection
    for the current scope.

    Examples
    --------
    >>> qs(df, r'name  .save(1)   %age   %:load(1)')
    """

    #symbol attributes
    name = 'GetSavedSelection'
    category = 'getter'
    regex = (
        r':load',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:

        if arg not in q.masks_saved:
            msg = f'ERROR: No saved selection named "{arg}" found.'
            context = build_log_context(
                'GetSavedSelection.getter',
                missing_selection=arg,
                )
            log(msg, context, q.verbosity)

        elif op.scope == 'cols':
            mask = q.masks_saved[arg]['cols']

        elif op.scope == 'rows':
            mask = q.masks_saved[arg]['rows']

        elif op.scope == 'vals':
            col = series.name
            mask = q.masks_saved[arg]['vals'].loc[series.index, col]

        return mask




class GetTrimmedSelection(Symbol):
    """
    trim the current row or col selection to
    entries which contain currently selected vals.

    Examples
    --------
    >>> qs(df, r'%%%>0   &&&<100   %:trim')
    >>> qs(df, r'%%%>0   &&&<100   %%:trim')
    """

    #symbol attributes
    name = 'GetTrimmedSelection'
    category = 'getter'
    regex = (
        r':trim',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        if op.scope == 'cols':
            mask = q.mask_vals.any()
        elif op.scope == 'rows':
            mask = (
                q
                .mask_vals
                .loc[:, q.mask_cols]
                .any(axis=1)
                )
        return mask




class GetInvertedSelection(Symbol):
    """
    get the inverse of the current
    selection for the current scope.

    Examples
    --------
    >>> qs(df, r':isna  :invert')
    """

    #symbol attributes
    name = 'GetInvertedSelection'
    category = 'getter'
    regex = (
        r':inverted',
        r':invert',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        return ~mask




class GetIsStr(Symbol):
    """
    get cols/rows/vals
    which are strings.

    Examples
    --------
    >>> qs(df, r'age  :isstr')
    """

    #symbol attributes
    name = 'GetIsStr'
    category = 'getter'
    regex = (r':isstr',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        mask = series.apply(lambda x: isinstance(x, TYPES_STR))
        return mask




class GetIsInt(Symbol):
    """
    get cols/rows/vals
    which are integers.

    Examples
    --------
    >>> qs(df, r'age  :isint')
    """

    #symbol attributes
    name = 'GetIsInt'
    category = 'getter'
    regex = (r':isint',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'strict': 'strict type comparison',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        if 'strict' in op.flags:
            mask = series.apply(lambda x: isinstance(x, TYPES_INT))
        else:
            unrounded = pd.to_numeric(series, errors='coerce')
            rounded = unrounded.round(0)
            mask = rounded == unrounded
        return mask




class GetIsFloat(Symbol):
    """
    get cols/rows/vals
    which are floats.

    Examples
    --------
    >>> qs(df, r'age  :isfloat')
    """

    #symbol attributes
    name = 'GetIsFloat'
    category = 'getter'
    regex = (r':isfloat',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'strict': 'strict type comparison',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        if 'strict' in op.flags:
            mask = series.apply(lambda x: isinstance(x, TYPES_FLOAT))
        else:
            mask = series.apply(lambda x: _float(x, errors='X')) != 'X'
        return mask




class GetIsNum(Symbol):
    """
    get cols/rows/vals
    which are numeric.

    Examples
    --------
    >>> qs(df, r'age  :isnum')
    """

    #symbol attributes
    name = 'GetIsNum'
    category = 'getter'
    regex = (r':isnum',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'strict': 'strict type comparison',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        if 'strict' in op.flags:
            mask = series.apply(lambda x: isinstance(x, TYPES_NUM))
        else:
            mask = series.apply(lambda x: _num(x, errors='X')) != 'X'
        return mask




class GetIsBool(Symbol):
    """
    get cols/rows/vals
    which are boolean.

    Examples
    --------
    >>> qs(df, r'age  :isbool')
    """

    #symbol attributes
    name = 'GetIsBool'
    category = 'getter'
    regex = (r':isbool',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'strict': 'strict type comparison',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        if 'strict' in op.flags:
            mask = series.apply(lambda x: isinstance(x, TYPES_BOOL))
        else:
            mask = series.apply(lambda x: _bool(x, errors='X')) != 'X'
        return mask




class GetIsDatetime(Symbol):
    """
    get cols/rows/vals
    which are datetimes.

    Examples
    --------
    >>> qs(df, r'age  :isdatetime')
    """

    #symbol attributes
    name = 'GetIsDatetime'
    category = 'getter'
    regex = (r':isdatetime',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'strict': 'strict type comparison',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        if 'strict' in op.flags:
            mask = series.apply(lambda x: isinstance(x, TYPES_DATE))
        else:
            mask = series.apply(lambda x: _datetime(x, errors='X')) != 'X'
        return mask




class GetIsDate(Symbol):
    """
    get cols/rows/vals
    which are dates.

    Examples
    --------
    >>> qs(df, r'age  :isdate')
    """

    #symbol attributes
    name = 'GetIsDate'
    category = 'getter'
    regex = (r':isdate',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'strict': 'strict type comparison',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        if 'strict' in op.flags:
            mask = series.apply(lambda x: isinstance(x, TYPES_DATE))
        else:
            mask = series.apply(lambda x: _date(x, errors='X')) != 'X'
        return mask




class GetIsNA(Symbol):
    """
    get cols/rows/vals
    which are NA values.

    Examples
    --------
    >>> qs(df, r'age  :isna')
    """

    #symbol attributes
    name = 'GetIsNA'
    category = 'getter'
    regex = (r':isna',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'strict': 'strict type comparison',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        if 'strict' in op.flags:
            mask = series.isna()
        else:
            mask = series.apply(lambda x: _na(x, errors='X')) != 'X'
        return mask




class GetIsNK(Symbol):
    """
    get cols/rows/vals
    which are NK values.

    Examples
    --------
    >>> qs(df, r'age  :isnk')
    """

    #symbol attributes
    name = 'GetIsNK'
    category = 'getter'
    regex = (r':isnk',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        mask = series.apply(lambda x: _nk(x, errors='X')) != 'X'
        return mask




class GetIsYN(Symbol):
    """
    get cols/rows/vals
    which are yes/no values.

    Examples
    --------
    >>> qs(df, r'age  :isyn')
    """

    #symbol attributes
    name = 'GetIsYN'
    category = 'getter'
    regex = (r':isyn',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        mask = series.apply(lambda x: _yn(x, errors='X')) != 'X'
        return mask




class GetIsUnique(Symbol):
    """
    get cols/rows/vals
    which occur exactly once.

    Examples
    --------
    >>> qs(df, r'age  :isunique')
    """

    #symbol attributes
    name = 'GetIsUnique'
    category = 'getter'
    regex = (r':isunique',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        mask = series.duplicated(keep=False) == False  # noqa: E712
        return mask




class GetIsFirst(Symbol):
    """
    get cols/rows/vals which are the
    first occurrence of a repeated val.
    includes unique vals.

    Examples
    --------
    >>> qs(df, r'age  :isfirst')
    """

    #symbol attributes
    name = 'GetIsFirst'
    category = 'getter'
    regex = (r':isfirst',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        mask = series.duplicated(keep='first') == False  # noqa: E712
        return mask




class GetIsLast(Symbol):
    """
    get cols/rows/vals which are the
    last occurrence of a repeated val.
    includes unique vals.

    Examples
    --------
    >>> qs(df, r'age  :islast')
    """

    #symbol attributes
    name = 'GetIsLast'
    category = 'getter'
    regex = (r':islast',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        'index': 'condition is applied to index instead of vals',
        'allcols': 'get rows where condition applies in all selected cols',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        mask = series.duplicated(keep='last') == False  # noqa: E712
        return mask




class GetAll(Symbol):
    """
    get all cols/rows/vals
    in the current scope.

    Examples
    --------
    >>> qs(df, r'%:all')
    >>> qs(df, r'%')  #defaults to GetAll operator
    """

    #symbol attributes
    name = 'GetAll'
    category = 'getter'
    regex = (r':all',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        'and': 'combine getter selection with current selection using logical AND',
        'or': 'combine getter selection with current selection using logical OR',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'negate': 'negate the condition',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q = _parse_getter(self, q)
        return q

    def getter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series[bool],
            arg: str,
            q: Query,
            ) -> pd.Series:
        mask = pd.Series(
            [True for item in series],
            index=series.index,
            )
        return mask



def _preparse_for_getter(q: Query) -> Query:

    if q.op.scope and not q.op.operator:
        pass

    else:
        q = _process_op(q)
        msg = 'Trace: inferring rows scope for getter.'
        context = build_log_context('_preparse_for_getter')
        log(msg, context, q.verbosity)
        q.op.connector = 'new'
        q.op.scope = 'rows'

    return q


def _parse_getter(
        token: Symbol,
        q: Query,
        ) -> Query:

    #transfer main attributes
    q.op.category = token.category
    q.op.operator = token.name
    q.op.getter = token.getter
    q.op.flags.update(token.op_flags)

    #transfer validation attributes
    q.op.args_min = token.op_args_min
    q.op.args_max = token.op_args_max
    q.op.connectors_allowed.update(token.op_connectors_allowed)
    q.op.scopes_allowed.update(token.op_scopes_allowed)
    q.op.args_allowed.update(token.op_args_allowed)
    q.op.flags_allowed.update(token.op_flags_allowed)
    q.op.flags_allowed.update(token.op_flags)

    return q



def _process_colref(
        series: pd.Series,
        arg: str,
        op: Operation,
        q: Query,
        ) -> pd.Series:

    if arg in q.df.columns:
        series_other = q.df[arg]
    else:
        msg = f'ERROR: col "{arg}" not found for colref comparison.'
        context = build_log_context(
            '_process_colref',
            missing_column=arg,
            available_columns=list(q.df.columns),
            )
        log(msg, context, q.verbosity)
        series_other = pd.Series(
            pd.NA,
            index=series.index,
            )

    return series_other



def _process_types(
        series: pd.Series,
        arg: str,
        op: Operation,
        q: Query,
        ) -> tuple[pd.Series, typing.Any]:

    if 'strict' in op.flags:
        series_new, arg_new = _process_types_strict(
            series,
            arg,
            op,
            q,
            )
        return series_new, arg_new

    elif 'str' in op.flags:
        series_new = series.astype('string').str.lower()
        arg_new = arg.lower()

    elif 'int' in op.flags:
        series_new = series.apply(_int).astype('Int64')
        arg_new = _int(arg)

    elif 'float' in op.flags:
        series_new = series.apply(_float).astype('Float64')
        arg_new = _float(arg)

    elif 'num' in op.flags:
        series_new = series.apply(_num).convert_dtypes()
        arg_new = _num(arg)

    elif 'bool' in op.flags:
        series_new = series.apply(_bool).astype('boolean')
        arg_new = _bool(arg)

    elif 'date' in op.flags:
        series_new = series.apply(_date).astype('datetime64[us]').dt.date
        arg_new = _date(arg)

    elif 'datetime' in op.flags:
        series_new = series.apply(_datetime).astype('datetime64[us]')
        arg_new = _datetime(arg)

    elif op.category == 'getter':
        series_new, arg_new = _infer_types_for_getter(
            series,
            arg,
            op,
            q,
            )

    else:
        series_new = series.astype('object')
        arg_new = _convert(arg)

    return series_new, arg_new



def _process_types_strict(
        series: pd.Series,
        arg: str,
        op: Operation,
        q: Query,
        ) -> tuple[pd.Series, typing.Any]:

    if 'str' in op.flags:
        series_new = series.astype('string')
        arg_new = arg

    elif 'int' in op.flags:
        series_new = series.astype('Int64')
        arg_new = _int(arg, errors='raise')

    elif 'float' in op.flags:
        series_new = series.astype('Float64')
        arg_new = _float(arg, errors='raise')

    elif 'num' in op.flags:
        series_new = pd.to_numeric(series, errors='raise').convert_dtypes()
        arg_new = _num(arg, errors='raise')

    elif 'bool' in op.flags:
        series_new = series.astype('boolean')
        arg_new = _bool(arg, errors='raise')

    elif 'date' in op.flags:
        series_new = series.astype('datetime64[us]').dt.date
        arg_new = _date(arg, errors='raise')

    elif 'datetime' in op.flags:
        series_new = series.astype('datetime64[us]')
        arg_new = _datetime(arg, errors='raise')

    else:
        series_new = series
        arg_new = _convert(arg, errors='raise')

    return series_new, arg_new



def _infer_types_for_getter(
        series: pd.Series,
        arg: str,
        op: Operation,
        q: Query,
        ) -> tuple[pd.Series, typing.Any]:

    type_name = _type(arg)

    if type_name == 'str':
        series_new = series.astype('string').str.lower()
        arg_new = arg.lower()

    elif type_name == 'int':
        #while the arg should be converted to int as specified,
        #float makes more sense for the series for most comparisons.
        #eg. 70.2 should be greater than 70, instead of
        #converting 70.2 to 70 and saying they are equal.
        series_new = series.apply(_float)
        arg_new = _int(arg)

    elif type_name == 'float':
        series_new = series.apply(_float).astype('Float64')
        arg_new = _float(arg)

    elif type_name == 'num':
        series_new = series.apply(_num).convert_dtypes()
        arg_new = _num(arg)

    elif type_name == 'bool':
        series_new = series.apply(_bool).astype('boolean')
        arg_new = _bool(arg)

    elif type_name == 'date':
        series_new = series.apply(_date).astype('datetime64[us]').dt.date
        arg_new = _date(arg)

    elif type_name == 'datetime':
        series_new = series.apply(_datetime).astype('datetime64[us]')
        arg_new = _datetime(arg)

    else:
        msg = f'WARNING: unable to infer type for arg "{arg}".'
        context = build_log_context('_infer_types_for_getter')
        log(msg, context, q.verbosity)
        series_new = series
        arg_new = arg

    return series_new, arg_new



def _process_types_series(
        series: pd.Series,
        series_other: pd.Series,
        op: Operation,
        q: Query,
        ) -> tuple[pd.Series, pd.Series]:

    if 'strict' in op.flags:
        series_new, series_other_new = _process_types_series_strict(
            series,
            series_other,
            op,
            q,
            )
        return series_new, series_other_new

    elif 'str' in op.flags:
        series_new = series.astype('string').str.lower()
        series_other_new = series_other.astype('string').str.lower()

    elif 'int' in op.flags:
        series_new = series.apply(_int).astype('Int64')
        series_other_new = series_other.apply(_int).astype('Int64')

    elif 'float' in op.flags:
        series_new = series.apply(_float).astype('Float64')
        series_other_new = series_other.apply(_float).astype('Float64')

    elif 'num' in op.flags:
        series_new = series.apply(_num).convert_dtypes()
        series_other_new = series_other.apply(_num).convert_dtypes()

    elif 'bool' in op.flags:
        series_new = series.apply(_bool).astype('boolean')
        series_other_new = series_other.apply(_bool).astype('boolean')

    elif 'date' in op.flags:
        series_new = series.apply(_date).astype('datetime64[us]').dt.date
        series_other_new = series_other.apply(_date).astype('datetime64[us]').dt.date

    elif 'datetime' in op.flags:
        series_new = series.apply(_datetime).astype('datetime64[us]')
        series_other_new = series_other.apply(_datetime).astype('datetime64[us]')

    elif series.dtype != series_other.dtype:
        series_new = series.astype('object')
        series_other_new = series_other.astype('object')

    else:
        series_new = series
        series_other_new = series_other

    return series_new, series_other_new



def _process_types_series_strict(
        series: pd.Series,
        series_other: pd.Series,
        op: Operation,
        q: Query,
        ) -> tuple[pd.Series, pd.Series]:

    if 'str' in op.flags:
        series_new = series.astype('string')
        series_other_new = series_other.astype('string')

    elif 'int' in op.flags:
        series_new = series.astype('Int64')
        series_other_new = series_other.astype('Int64')

    elif 'float' in op.flags:
        series_new = series.astype('Float64')
        series_other_new = series_other.astype('Float64')

    elif 'num' in op.flags:
        series_new = pd.to_numeric(series, errors='raise').convert_dtypes()
        series_other_new = pd.to_numeric(series_other, errors='raise').convert_dtypes()

    elif 'bool' in op.flags:
        series_new = series.astype('boolean')
        series_other_new = series_other.astype('boolean')

    elif 'date' in op.flags:
        series_new = series.astype('datetime64[us]').dt.date
        series_other_new = series_other.astype('datetime64[us]').dt.date

    elif 'datetime' in op.flags:
        series_new = series.astype('datetime64[us]')
        series_other_new = series_other.astype('datetime64[us]')

    elif series.dtype != series_other.dtype:
        series_new = series
        series_other_new = series_other.astype(series.dtype)

    else:
        series_new = series
        series_other_new = series_other

    return series_new, series_other_new




class SetVals(Symbol):
    """
    set selected cols/rows/vals to an
    arg using automatic type conversion.

    Examples
    --------
    >>> qs(df, r'name  =="john doe"  ="JOHN DOE"')
    """

    #symbol attributes
    name = 'SetVals'
    category = 'setter'
    regex = (r'=',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'colref': 'use a col reference for setting/getting vals',
        'strict': 'force strict type conversion',
        'str': 'convert to string type',
        'int': 'convert to integer type',
        'float': 'convert to float type',
        'num': 'convert to numeric type',
        'bool': 'convert to boolean type',
        'date': 'convert to date type',
        'datetime': 'convert to datetime type',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:

        arg = args[0]

        if 'colref' in op.flags:
            series_other = _process_colref(
                series,
                arg,
                op,
                q,
                )
            series, arg = _process_types_series(
                series,
                series_other,
                op,
                q,
                )

        else:
            series, arg = _process_types(
                series,
                arg,
                op,
                q,
                )

        series[mask] = arg

        return series




class SetSum(Symbol):
    """
    add an arg or a col to the
    currently selected cols using
    automatic type conversion.

    Examples
    --------
    >>> qs(df, r'age  +=10')
    """

    #symbol attributes
    name = 'SetSum'
    category = 'setter'
    regex = (r'\+=',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'colref': 'use a col reference for setting/getting vals',
        'str': 'string type comparison',
        'int': 'integer type comparison',
        'float': 'float type comparison',
        'num': 'numeric type comparison',
        'bool': 'boolean type comparison',
        'date': 'date type comparison',
        'datetime': 'datetime type comparison',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:

        arg = args[0]

        if 'colref' in op.flags:
            series_other = _process_colref(
                series,
                arg,
                op,
                q,
                )
            series, arg = _process_types_series(
                series,
                series_other,
                op,
                q,
                )

        else:
            series, arg = _process_types(
                series,
                arg,
                op,
                q,
                )

        series[mask] += arg

        return series




class SetDifference(Symbol):
    """
    subtract an arg or a col from the
    currently selected cols using
    automatic type conversion.

    Examples
    --------
    >>> qs(df, r'age  -=10')
    """

    #symbol attributes
    name = 'SetDifference'
    category = 'setter'
    regex = (r'-=',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'colref': 'use a col reference for setting/getting vals',
        'str': 'string type comparison',
        'int': 'integer type comparison',
        'float': 'float type comparison',
        'num': 'numeric type comparison',
        'bool': 'boolean type comparison',
        'date': 'date type comparison',
        'datetime': 'datetime type comparison',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:

        arg = args[0]

        if 'colref' in op.flags:
            series_other = _process_colref(
                series,
                arg,
                op,
                q,
                )
            series, arg = _process_types_series(
                series,
                series_other,
                op,
                q,
                )

        else:
            series, arg = _process_types(
                series,
                arg,
                op,
                q,
                )

        series[mask] -= arg

        return series




class SetEval(Symbol):
    """
    set selected cols/rows/vals to the result
    of evaluating a custom python expression.

    "x" can be used in the expression
    to refer to the current item.

    Examples
    --------
    >>> qs(df, r'%name  .eval( "str(x).upper()" )')
    """

    #symbol attributes
    name = 'SetEval'
    category = 'setter'
    regex = (r'\.eval',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q


    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:

        expression = args[0]

        #needs to be evaluated for each val
        if 'x' in expression:
            def custom_func(x):
                namespace = {
                    'x': x,
                    'df': q.df,
                    'pd': pd,
                    'np': np,
                    're': re,
                    }
                return eval(expression, namespace)
            series_new = series.map(lambda x: custom_func(x))

        #only needs to be evaluated once
        else:
            namespace = {
                'df': q.df,
                'pd': pd,
                'np': np,
                're': re,
                }
            eval_result = eval(expression, namespace)

            switch_whole = (
                isinstance(eval_result, pd.Series)
                and eval_result.index.equals(series.index)
                )
            if switch_whole:
                series_new = eval_result
            else:
                series_new = pd.Series(eval_result, index=series.index)

        series, series_new = _process_types_series(
            series,
            series_new,
            op,
            q,
            )

        if mask.all():
            series = series_new
        else:
            series[mask] = series_new

        return series




class SetTypeInfo(Symbol):
    """
    show type info for selected cols/rows/vals.

    Examples
    --------
    >>> qs(df, r'name  .typeinfo')
    """

    #symbol attributes
    name = 'SetTypeInfo'
    category = 'setter'
    regex = (
        r'\.typeinfo',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'strict': 'show strict types instead of inferred types',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        if 'strict' in op.flags:
            series_new = series[mask].apply(_typeinfostrict)
        else:
            series_new = series[mask].apply(_typeinfo)
        series = series.astype('string')
        series[mask] = series_new
        return series




class SetRawRepresentation(Symbol):
    """
    show raw representations of the
    data in selected cols/rows/vals.

    eg:
    - 1983-06-30 -> datetime.date(1983, 6, 30)

    Examples
    --------
    >>> qs(df, r'name  .repr')
    """

    #symbol attributes
    name = 'SetRawRepresentation'
    category = 'setter'
    regex = (
        r'\.repr',
        r'\.raw',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        series_new = series[mask].apply(_repr)
        series = series.astype('string')
        series[mask] = series_new
        return series




class SetToObj(Symbol):
    """
    set selected cols/rows/vals to type object

    Examples
    --------
    >>> qs(df, r'name  .toobj')
    """

    #symbol attributes
    name = 'SetToObj'
    category = 'setter'
    regex = (
        r'\.toobject',
        r'\.toobj',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        series = series.astype('object')
        return series




class SetToStr(Symbol):
    """
    set selected cols/rows/vals to type str

    Examples
    --------
    >>> qs(df, r'name  .tostr')
    """

    #symbol attributes
    name = 'SetToStr'
    category = 'setter'
    regex = (
        r'\.tostring',
        r'\.tostr',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        if mask.all():
            series = series.astype('string')
        else:
            series_new = series[mask].astype('string')
            series[mask] = series_new
        return series




class SetToInt(Symbol):
    """
    set selected cols/rows/vals to type int

    Examples
    --------
    >>> qs(df, r'name  .toint')
    """

    #symbol attributes
    name = 'SetToInt'
    category = 'setter'
    regex = (
        r'\.tointeger',
        r'\.toint',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'strict': 'use stricter pandas ".astype(Int64)" for conversion',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:

        if 'strict' in op.flags:
            series_new = series[mask].astype('Int64')
        else:
            series_new = series[mask].apply(_int).astype('Int64')

        if mask.all():
            series = series_new
        else:
            series[mask] = series_new

        return series




class SetToFloat(Symbol):
    """
    set selected cols/rows/vals to type float

    Examples
    --------
    >>> qs(df, r'name  .tofloat')
    """

    #symbol attributes
    name = 'SetToFloat'
    category = 'setter'
    regex = (r'\.tofloat',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'strict': 'use stricter pandas ".astype(Float64)" for conversion',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:

        if 'strict' in op.flags:
            series_new = series[mask].astype('Float64')
        else:
            series_new = series[mask].apply(_float).astype('Float64')

        if mask.all():
            series = series_new
        else:
            series[mask] = series_new

        return series




class SetToNum(Symbol):
    """
    set selected cols/rows/vals to numeric type

    Examples
    --------
    >>> qs(df, r'name  .tonum')
    """

    #symbol attributes
    name = 'SetToNum'
    category = 'setter'
    regex = (
        r'\.tonumeric',
        r'\.tonum',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'strict': 'use stricter pandas ".to_numeric" for conversion',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:

        if 'strict' in op.flags:
            series_new = pd.to_numeric(series[mask]).convert_dtypes()
        else:
            series_new = series[mask].apply(_num).convert_dtypes()

        if mask.all():
            series = series_new
        else:
            series[mask] = series_new

        return series




class SetToBool(Symbol):
    """
    set selected cols/rows/vals to type boolean

    Examples
    --------
    >>> qs(df, r'name  .tobool')
    """

    #symbol attributes
    name = 'SetToBool'
    category = 'setter'
    regex = (
        r'\.toboolean',
        r'\.tobool',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {
        'strict': 'use stricter pandas ".astype(\'boolean?\')" for conversion',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:

        if 'strict' in op.flags:
            series_new = series[mask].astype('boolean')
        else:
            series_new = series[mask].apply(_bool).astype('boolean')

        if mask.all():
            series = series_new
        else:
            series = series.astype('object')
            series[mask] = series_new

        return series



#must be before SetToDate due to parsing order
class SetToDatetime(Symbol):
    """
    set selected cols/rows/vals to datetime type

    Examples
    --------
    >>> qs(df, r'name  .todatetime')
    """

    #symbol attributes
    name = 'SetToDatetime'
    category = 'setter'
    regex = (r'\.todatetime',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        series_new = series[mask].apply(_datetime).astype('datetime64[us]')
        if mask.all():
            series = series_new
        else:
            series[mask] = series_new
        return series




class SetToDate(Symbol):
    """
    set selected cols/rows/vals to date type

    Examples
    --------
    >>> qs(df, r'name  .todate')
    """

    #symbol attributes
    name = 'SetToDate'
    category = 'setter'
    regex = (r'\.todate',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        series_new = (
            series[mask]
            .apply(_date)
            .astype('datetime64[us]')
            .dt
            .date
            )
        if mask.all():
            series = series_new
        else:
            series[mask] = series_new
        return series




class SetToNA(Symbol):
    """
    set potential NA vals in
    selected cols/rows/vals
    to standardized NA vals

    Examples
    --------
    >>> qs(df, r'name  .tona')
    """

    #symbol attributes
    name = 'SetToNA'
    category = 'setter'
    regex = (r'\.tona',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        series_new = (
            series[mask]
            .apply(_na)
            .convert_dtypes()
            )
        if mask.all():
            series = series_new
        else:
            series[mask] = series_new
        return series




class SetToNK(Symbol):
    """
    set potential NK vals in
    selected cols/rows/vals
    to standardized NK vals

    Examples
    --------
    >>> qs(df, r'name  .tonk')
    """

    #symbol attributes
    name = 'SetToNK'
    category = 'setter'
    regex = (r'\.tonk',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        series_new = series[mask].apply(_nk).convert_dtypes()
        if mask.all():
            series = series_new
        else:
            series[mask] = series_new
        return series




class SetToYN(Symbol):
    """
    set potential yes/no vals in
    selected cols/rows/vals
    to standardized yes/no vals

    Examples
    --------
    >>> qs(df, r'name  .toyn')
    """

    #symbol attributes
    name = 'SetToYN'
    category = 'setter'
    regex = (r'\.toyn',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        series_new = series[mask].apply(_yn).convert_dtypes()
        if mask.all():
            series = series_new
        else:
            series[mask] = series_new
        return series




class SetUpper(Symbol):
    """
    set selected cols/rows/vals
    to uppercase.

    Examples
    --------
    >>> qs(df, r'name  .upper')
    """

    #symbol attributes
    name = 'SetUpper'
    category = 'setter'
    regex = (r'\.upper',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_args_min = 0
    op_args_max = 0
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        series_new = series[mask].astype('string').str.upper()
        if mask.all():
            series = series_new
        else:
            series[mask] = series_new
        return series




class SetLower(Symbol):
    """
    set selected cols/rows/vals
    to lowercase.

    Examples
    --------
    >>> qs(df, r'name  .lower')
    """

    #symbol attributes
    name = 'SetLower'
    category = 'setter'
    regex = (r'\.lower',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_setter(self, q)
        return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:
        series_new = series[mask].astype('string').str.lower()
        if mask.all():
            series = series_new
        else:
            series[mask] = series_new
        return series



def _preparse_for_setter(q: Query) -> Query:

    if q.op.scope and not q.op.operator:
        pass

    else:
        q = _process_op(q)
        msg = 'Trace: inferring vals scope for setter or styler.'
        context = build_log_context('_preparse_for_setter')
        log(msg, context, q.verbosity)
        q.op.connector = 'new'
        q.op.scope = 'vals'

    return q


def _parse_setter(
        token: Symbol,
        q: Query,
        ) -> Query:

    #transfer main attributes
    q.op.category = token.category
    q.op.operator = token.name
    q.op.setter = token.setter
    q.op.flags.update(token.op_flags)

    #transfer validation attributes
    q.op.args_min = token.op_args_min
    q.op.args_max = token.op_args_max
    q.op.connectors_allowed.update(token.op_connectors_allowed)
    q.op.scopes_allowed.update(token.op_scopes_allowed)
    q.op.args_allowed.update(token.op_args_allowed)
    q.op.flags_allowed.update(token.op_flags_allowed)
    q.op.flags_allowed.update(token.op_flags)

    return q

    def setter(
            self,
            op: Operation,
            series: pd.Series,
            mask: pd.Series,
            args: list,
            q: Query,
            ) -> pd.Series:

        arg = args[0]

        if 'colref' in op.flags:
            series_other = _process_colref(
                series,
                arg,
                op,
                q,
                )
            series, arg = _process_types_series(
                series,
                series_other,
                op,
                q,
                )

        else:
            series, arg = _process_types(
                series,
                arg,
                op,
                q,
                )

        series[mask] -= arg

        return series



class StyleFont(Symbol):
    """
    change the font style of
    selected cols/rows/vals

    Examples
    --------
    >>> qs(df, r'%.font(bold)')
    """

    #symbol attributes
    name = 'StyleFont'
    category = 'styler'
    regex = (
        r'\.font\-weight',
        r'\.font\-style',
        r'\.fontweight',
        r'\.fontstyle',
        r'\.weight',
        r'\.style',
        r'\.font',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {
        #used by css property "font-weight"
        'bold': 'bold font weight',
        'bolder': 'bolder font weight',
        'lighter': 'lighter font weight',

        #used by css property "font-style"
        'italic': 'italic font style',
        'oblique': 'oblique font style',

        #used by both css properties "font-weight" and "font-style"
        'normal': 'normal font weight and style',
        }
    op_args_min = 1
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_styler(self, q)
        return q


    def styler(self, op: Operation, q: Query) -> str:

        arg = op.args[0].lower()
        args_font_weight = (
            'bold',
            'bolder',
            'lighter',
            )
        args_font_style = (
            'italic',
            'oblique',
            )

        if arg in args_font_weight:
            return f'font-weight: {arg};'
        elif arg in args_font_style:
            return f'font-style: {arg};'
        else:
            return 'font-weight: normal; font-style: normal;'



class StyleColor(Symbol):
    """
    change the text color of
    selected cols/rows/vals

    Examples
    --------
    >>> qs(df, r'name  .color(red)')
    """

    #symbol attributes
    name = 'StyleColor'
    category = 'styler'
    regex = (
        r'\.colour',
        r'\.color',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_styler(self, q)
        return q

    def styler(self, op: Operation, q: Query) -> str:
        color = op.args[0]
        return f'color: {color};'




class StyleBackgroundColor(Symbol):
    """
    change the background color of
    selected cols/rows/vals

    Examples
    --------
    >>> qs(df, r'name  .bg(red)')
    """

    #symbol attributes
    name = 'StyleBackgroundColor'
    category = 'styler'
    regex = (
        r'\.background_colour',
        r'\.background_color',
        r'\.backgroundcolour',
        r'\.backgroundcolor',
        r'\.background',
        r'\.bg',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_styler(self, q)
        return q

    def styler(self, op: Operation, q: Query) -> str:
        color = op.args[0]
        return f'background-color: {color};'




class StyleAlignement(Symbol):
    """
    change the alignment of
    selected cols/rows/vals

    Examples
    --------
    >>> qs(df, r'name  .align(center)')
    """

    #symbol attributes
    name = 'StyleAlignement'
    category = 'styler'
    regex = (
        r'\.alignment',
        r'\.align',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {
        'left': 'align to the left',
        'right': 'align to the right',
        'center': 'align to the center',
        'start': 'align to the start',
        'end': 'align to the end',
        'justify': 'justify the text',
        }
    op_args_min = 1
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_styler(self, q)
        return q

    def styler(self, op: Operation, q: Query) -> str:
        alignement = op.args[0].lower()
        return f'text-align: {alignement};'




class StyleTextWrap(Symbol):
    """
    change the text wrapping style of
    selected cols/rows/vals

    Examples
    --------
    >>> qs(df, r'name  .wrap(nowrap)')
    """

    #symbol attributes
    name = 'StyleTextWrap'
    category = 'styler'
    regex = (
        r'\.whitespace',
        r'\.text\-wrap',
        r'\.textwrap',
        r'\.wrap',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'get or set cols/headers',
        'rows': 'get or set rows/index',
        'vals': 'get or set vals within current row and col selection',
        }
    op_flags_allowed = {}
    op_args_allowed = {
        #used by css property "text-wrap"
        'wrap': 'wrap text when it exceeds cell width',
        'nowrap': 'do not wrap text, let it overflow',
        'balance': 'wrap text and balance line lengths',
        'pretty': 'wrap text and try to break at word boundaries',
        'stable': 'wrap text without breaking words if possible',

        #used by css property "white-space"
        'normal': 'use normal whitespace handling (default)',
        'pre': 'preserve whitespace and line breaks',
        'pre-wrap': 'preserve whitespace and wrap as needed',
        'pre-line': 'collapse whitespace but preserve line breaks',

        #custom
        'hard': 'wrap at each whitespace character',
        }
    op_args_min = 1
    op_args_max = 1


    def parse(self, q: Query) -> Query:
        q = _preparse_for_setter(q)
        q = _parse_styler(self, q)
        return q


    def styler(self, op: Operation, q: Query) -> str:

        arg = op.args[0].lower()
        args_textwrap = (
            'wrap',
            'nowrap',
            'balance',
            'pretty',
            'stable',
            )
        args_whitespace = (
            'normal',
            'pre',
            'pre-wrap',
            'pre-line',
            )

        if arg in args_textwrap:
            return f'text-wrap: {arg};'
        elif arg in args_whitespace:
            return f'white-space: {arg};'
        elif arg == 'hard':
            return 'word-spacing: 999999999px;'
        else:
            msg = f'ERROR: invalid text-wrap arg "{arg!r}".'
            context = build_log_context(
                'StyleTextWrap.styler',
                arg=arg,
                allowed_args=args_textwrap + args_whitespace,
                op=op.str_debug(),
                )
            log(msg, context, q.verbosity)
            return ''



def _parse_styler(
        token: Symbol,
        q: Query,
        ) -> Query:

    #transfer main attributes
    q.op.category = token.category
    q.op.operator = token.name
    q.op.styler = token.styler
    q.op.flags.update(token.op_flags)

    #transfer validation attributes
    q.op.args_min = token.op_args_min
    q.op.args_max = token.op_args_max
    q.op.connectors_allowed.update(token.op_connectors_allowed)
    q.op.scopes_allowed.update(token.op_scopes_allowed)
    q.op.args_allowed.update(token.op_args_allowed)
    q.op.flags_allowed.update(token.op_flags_allowed)
    q.op.flags_allowed.update(token.op_flags)

    return q




class ShapeCopyCol(Symbol):
    """
    copy values in currently
    selected col(s) to new col(s)

    Examples
    --------
    >>> qs(df, r'.copy')
    >>> qs(df, r'.copy(new_col_name)')
    """

    #symbol attributes
    name = 'ShapeCopyCol'
    category = 'shaper'
    regex = (
        r'\.copy',
        r'\.cp',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_shaper(self, q)
        return q


    def shaper(self, op: Operation, q: Query) -> Query:

        for colname in q.df.columns[q.mask_cols]:

            loc = len(q.df.columns)
            val = q.df.loc[:, colname]

            if op.args:
                colname_new = op.args[0]
                warning = True
            else:
                colname_new = colname
                warning = False

            colname_new = _ensure_unique_col(
                colname_new,
                q.df.columns,
                strategy='increment',
                warning=warning,
                verbosity=q.verbosity,
                )

            q = _insert_col(
                loc,
                colname_new,
                val,
                q,
                )

        return q




class ShapeNewCol(Symbol):
    """
    append a new col, optionally
    initialized with a typed val.

    Examples
    --------
    >>> qs(df, r'.new a')
    >>> qs(df, r'.new(a, 1, +float)')
    """

    #symbol attributes
    name = 'ShapeNewCol'
    category = 'shaper'
    regex = (
        r'\.insert',
        r'\.newcol',
        r'\.new',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {
        'str': 'creates string col',
        'int': 'creates integer col',
        'float': 'creates float col',
        'num': 'creates numeric col',
        'bool': 'creates boolean col',
        'date': 'creates date col',
        'datetime': 'creates datetime col',
        }
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 2

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_shaper(self, q)
        return q


    def shaper(self, op: Operation, q: Query) -> Query:

        loc = len(q.df.columns)
        colname_new = _ensure_unique_col(
            op.args[0],
            q.df.columns,
            strategy='increment',
            warning=True,
            verbosity=q.verbosity,
            )

        if len(op.args) > 1:
            val = op.args[1]
            if 'str' in op.flags:
                val = str(val)
            elif 'int' in op.flags:
                val = _int(val)
            elif 'float' in op.flags:
                val = _float(val)
            elif 'num' in op.flags:
                val = _num(val)
            elif 'bool' in op.flags:
                val = _bool(val)
            elif 'date' in op.flags:
                val = _date(val)
            elif 'datetime' in op.flags:
                val = _datetime(val)
            else:
                val = _convert(val)
        else:
            val = pd.NA

        q = _insert_col(
            loc,
            colname_new,
            val,
            q,
            )

        return q




class ShapeTagMetadata(Symbol):
    """
    add a tag about the the currently
    selected rows into the metadata col.

    assumes the metadata col is named "_meta"
    and creates it if it doesn't exist.

    Examples
    --------
    >>> qs(df, r'age  <0  .tag("invalid age")')
    """

    #symbol attributes
    name = 'ShapeTagMetadata'
    category = 'shaper'
    regex = (
        r'\.metadata',
        r'\.meta',
        r'\.tag',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 2

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_shaper(self, q)
        return q

    def shaper(self, op: Operation, q: Query) -> Query:

        if len(op.args) == 2:
            col_meta = str(op.args[1])
        else:
            col_meta = '_meta'

        if col_meta not in q.df.columns:
            q = _insert_col_meta(col_meta, q)
        elif q.df[col_meta].dtype != 'string':
            q.df[col_meta] = q.df[col_meta].astype('string')

        tag = str(op.args[0])
        q.df.loc[q.mask_rows, col_meta] += tag

        return q




class ShapeSaveSelection(Symbol):
    """
    save the current selection state
    (cols, rows, vals) under a name.

    Examples
    --------
    >>> qs(df, r'name  .save(1)')
    """

    #symbol attributes
    name = 'ShapeSaveSelection'
    category = 'shaper'
    regex = (r'\.save',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_shaper(self, q)
        return q


    def shaper(self, op: Operation, q: Query) -> Query:

        masks = {}
        masks['cols'] = q.mask_cols.copy()
        masks['rows'] = q.mask_rows.copy()
        masks['vals'] = q.mask_vals.copy()
        name = op.args[0]

        if name in q.masks_saved:
            msg = f'WARNING: overwriting previously saved selection "{name}".'
            context = build_log_context(
                'ShapeSaveSelection.shaper',
                name=name,
                )
            log(msg, context, q.verbosity)

        q.masks_saved[name] = masks

        return q




class ShapeSortSelection(Symbol):
    """
    sort cols/rows/vals.

    Examples
    --------
    >>> qs(df, r'name  .sort')  #ascending
    >>> qs(df, r'name  !.sort')  #inverse order -> descending
    """

    #symbol attributes
    name = 'ShapeSortSelection'
    category = 'shaper'
    regex = (r'\.sort',)

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'cols': 'sort cols/headers',
        'rows': 'sort rows/index',
        'vals': 'sort vals within current row and col selection',
        'global': 'synonymous with "vals" scope',
        }
    op_flags_allowed = {
        'negate': 'invert the sorting order (descending instead of ascending)',
        }
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 0

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_shaper(self, q)
        return q

    def shaper(self, op: Operation, q: Query) -> Query:

        if 'negate' in op.flags:
            ascending = False
        else:
            ascending = True

        if op.scope == 'cols':
            q = _sort_cols(ascending, q)
        elif op.scope == 'rows':
            q = _sort_rows(ascending, q)
        elif op.scope in ('vals', 'global'):
            q = _sort_vals(ascending, q)

        return q



def _sort_cols(ascending: bool, q: Query) -> Query:

    mask_cols = q.mask_cols
    cols = q.df.columns

    cols_selected = cols[mask_cols]
    cols_selected_sorted = cols_selected.sort_values(ascending=ascending)

    cols_series = cols.to_series()
    cols_series[mask_cols] = cols_selected_sorted

    index_new = pd.Index(cols_series)

    #apply sorting to dataframe
    q.df = q.df[index_new]

    #update masks
    q.mask_cols = q.mask_cols[index_new]
    q.mask_vals = q.mask_vals[index_new]

    #update saved masks
    for mask in q.masks_saved.values():
        mask['cols'] = mask['cols'][index_new]
        mask['vals'] = mask['vals'][index_new]

    #update styles
    if q.style_cols is not None:
        q.style_cols = q.style_cols[index_new]
    if q.style_vals is not None:
        q.style_vals = q.style_vals[index_new]

    return q



def _sort_rows(ascending: bool, q: Query) -> Query:

    mask_rows = q.mask_rows
    rows = q.df.index

    rows_selected = rows[mask_rows]
    rows_selected_sorted = rows_selected.sort_values(ascending=ascending)

    rows_series = rows.to_series()
    rows_series[mask_rows] = rows_selected_sorted

    index_new = pd.Index(rows_series)

    #apply sorting to dataframe
    q.df = q.df.loc[index_new]

    #update masks
    q.mask_rows = q.mask_rows[index_new]
    q.mask_vals = q.mask_vals.loc[index_new]

    #update saved masks
    for mask in q.masks_saved.values():
        mask['rows'] = mask['rows'][index_new]
        mask['vals'] = mask['vals'].loc[index_new]

    #update styles
    if q.style_rows is not None:
        q.style_rows = q.style_rows[index_new]
    if q.style_vals is not None:
        q.style_vals = q.style_vals.loc[index_new]

    return q



def _sort_vals(ascending: bool, q: Query) -> Query:

    q.df = q.df.sort_values(
        by=q.df.columns[q.mask_cols].tolist(),
        ascending=ascending,
        )
    index_new = q.df.index

    #update masks
    q.mask_rows = q.mask_rows[index_new]
    q.mask_vals = q.mask_vals.loc[index_new]

    #update saved masks
    for mask in q.masks_saved.values():
        mask['rows'] = mask['rows'][index_new]
        mask['vals'] = mask['vals'].loc[index_new]

    #update styles
    if q.style_rows is not None:
        q.style_rows = q.style_rows[index_new]
    if q.style_vals is not None:
        q.style_vals = q.style_vals.loc[index_new]

    return q



def _ensure_unique_col(
        colname: str,
        cols: pd.Index,
        strategy: str = 'increment',
        warning: bool = True,
        verbosity: int = 3,
        ) -> str:

    if warning:
        level = 'WARNING'
    else:
        level = 'Trace'

    if colname in cols:
        msg = (
            f'{level}: colname "{colname}" already exists,'
            ' applying increment strategy to ensure uniqueness.'
            )
        context = build_log_context('_ensure_unique_col')
        log(msg, context, verbosity)
        colname = ensure_unique_string(
            colname,
            cols,
            strategy,
            )

    return colname



def _insert_col(
        loc: int,
        colname: str,
        val,
        q: Query,
        ) -> Query:

    q.df.insert(loc, colname, val)  #pyright: ignore
    q.df[colname] = q.df[colname].convert_dtypes()

    #update selection masks
    q.mask_cols[:] = False
    new_mask_cols = pd.Series([True], index=[colname])
    q.mask_cols = pd.concat([q.mask_cols, new_mask_cols])
    q.mask_vals.insert(loc, colname, True)

    #update saved masks
    for mask in q.masks_saved.values():
        new_mask_cols = pd.Series([False], index=[colname])
        mask['cols'] = pd.concat([mask['cols'], new_mask_cols])
        mask['vals'].insert(loc, colname, True)

    #update style metadata
    if q.style_cols is not None:
        new_col_style = pd.Series([''], index=[colname])
        q.style_cols = pd.concat([q.style_cols, new_col_style])
    if q.style_vals is not None:
        q.style_vals.insert(loc, colname, '')

    return q



def _insert_col_meta(
        col_meta: str,
        q: Query,
        ) -> Query:

    loc = len(q.df.columns)
    vals = pd.Series('', index=q.df.index, dtype='string')
    q.df[col_meta] = vals

    #update selection masks
    new_mask_cols = pd.Series([False], index=[col_meta])
    q.mask_cols = pd.concat([q.mask_cols, new_mask_cols])
    q.mask_vals.insert(loc, col_meta, True)

    #update saved masks
    for mask in q.masks_saved.values():
        new_mask_cols = pd.Series([False], index=[col_meta])
        mask['cols'] = pd.concat([mask['cols'], new_mask_cols])
        mask['vals'].insert(loc, col_meta, True)

    #update style metadata
    if q.style_cols is not None:
        new_col_style = pd.Series([''], index=[col_meta])
        q.style_cols = pd.concat([q.style_cols, new_col_style])
    if q.style_vals is not None:
        q.style_vals.insert(loc, col_meta, '')

    return q



def _preparse_for_shaper(q: Query) -> Query:

    if q.op.scope and not q.op.operator:
        pass

    else:
        q = _process_op(q)
        q.op.connector = 'new'
        q.op.scope = 'global'

    return q


def _parse_shaper(
        token: Symbol,
        q: Query,
        ) -> Query:

    #transfer main attributes
    q.op.category = token.category
    q.op.operator = token.name
    q.op.shaper = token.shaper
    q.op.flags.update(token.op_flags)

    #transfer validation attributes
    q.op.args_min = token.op_args_min
    q.op.args_max = token.op_args_max
    q.op.connectors_allowed.update(token.op_connectors_allowed)
    q.op.scopes_allowed.update(token.op_scopes_allowed)
    q.op.args_allowed.update(token.op_args_allowed)
    q.op.flags_allowed.update(token.op_flags_allowed)
    q.op.flags_allowed.update(token.op_flags)

    return q




class View(Symbol):
    """
    view the currently
    selected cols/rows/vals.

    use when debugging long queries.
    can also print an optional arg.

    Examples
    --------
    >>> qs(df, r'%%%:isna  .view(step1)  %name  ?john  .view')
    """

    #symbol attributes
    name = 'View'
    category = 'viewer'
    regex = (
        r'\.display',
        r'\.print',
        r'\.show',
        r'\.view',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 1


    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_viewer(self, q)
        return q


    def viewer(self, op: Operation, q: Query) -> Query:

        df_masked = (
            q.df
            [q.mask_vals]
            .loc[q.mask_rows, q.mask_cols]
            )

        if len(op.args) == 1:
            print(op.args[0])
        if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
            display(df_masked)
        else:
            print(df_masked)

        return q




class ViewQuery(Symbol):
    """
    view the query object itself.

    use when debugging long queries.
    can also print an optional arg.

    Examples
    --------
    >>> qs(df, r'%%%:isna  .q(step1)  %name  ?john  .q')
    """

    #symbol attributes
    name = 'ViewQuery'
    category = 'viewer'
    regex = (
        r'\.view_query',
        r'\.query',
        r'\.q',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_viewer(self, q)
        return q


    def viewer(self, op: Operation, q: Query) -> Query:

        if len(op.args) == 1:
            print(op.args[0])
        print(q.str_debug())

        return q




class ViewMasks(Symbol):
    """
    view the current selection masks.

    use when debugging long queries.
    can also print an optional arg.

    Examples
    --------
    >>> qs(df, r'%%%:isna  .masks(step1)  %name  ?john  .masks')
    """

    #symbol attributes
    name = 'ViewMasks'
    category = 'viewer'
    regex = (
        r'\.view_masks',
        r'\.masks',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_viewer(self, q)
        return q


    def viewer(self, op: Operation, q: Query) -> Query:

        if len(op.args) == 1:
            print(op.args[0])
        print(f'mask_cols:\n{q.mask_cols}\n')
        print(f'mask_rows:\n{q.mask_rows}\n')
        print(f'mask_vals:\n{q.mask_vals}\n')

        return q




class ViewMaskCols(Symbol):
    """
    view the current col selection masks.

    use when debugging long queries.
    can also print an optional arg.

    Examples
    --------
    >>> qs(df, r'%%%:isna  .cols(step1)  %name  ?john  .cols')
    """

    #symbol attributes
    name = 'ViewMaskCols'
    category = 'viewer'
    regex = (
        r'\.view_mask_cols',
        r'\.mask_cols',
        r'\.cols',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_viewer(self, q)
        return q


    def viewer(self, op: Operation, q: Query) -> Query:

        if len(op.args) == 1:
            print(op.args[0])
        print(f'mask_cols:\n{q.mask_cols}\n')

        return q




class ViewMaskRows(Symbol):
    """
    view the current row selection masks.

    use when debugging long queries.
    can also print an optional arg.

    Examples
    --------
    >>> qs(df, r'%%%:isna  .rows(step1)  %name  ?john  .rows')
    """

    #symbol attributes
    name = 'ViewMaskRows'
    category = 'viewer'
    regex = (
        r'\.view_mask_rows',
        r'\.mask_rows',
        r'\.rows',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_viewer(self, q)
        return q


    def viewer(self, op: Operation, q: Query) -> Query:

        if len(op.args) == 1:
            print(op.args[0])
        print(f'mask_rows:\n{q.mask_rows}\n')

        return q




class ViewMaskVals(Symbol):
    """
    print the current val selection masks.

    use when debugging long queries.
    can also print an optional arg.

    Examples
    --------
    >>> qs(df, r'%%%:isna  .vals(step1)  %name  ?john  .vals')
    """

    #symbol attributes
    name = 'ViewMaskVals'
    category = 'viewer'
    regex = (
        r'\.view_mask_vals',
        r'\.mask_vals',
        r'\.vals',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 0
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_viewer(self, q)
        return q


    def viewer(self, op: Operation, q: Query) -> Query:

        if len(op.args) == 1:
            print(op.args[0])
        print(f'mask_vals:\n{q.mask_vals}\n')

        return q




class ViewSetNArep(Symbol):
    """
    specify how NA values are displayed

    Examples
    --------
    >>> qs(df, r'name  .na_rep("N/A")')
    """

    #symbol attributes
    name = 'ViewSetNArep'
    category = 'viewer'
    regex = (
        r'\.na_rep',
        r'\.narep',
        )

    #used to build the current op
    op_flags = {}

    #used to validate the current op
    op_connectors_allowed = {
        'new': 'start a new op',
        }
    op_scopes_allowed = {
        'global': 'make global modifications',
        }
    op_flags_allowed = {}
    op_args_allowed = {}
    op_args_min = 1
    op_args_max = 1

    def parse(self, q: Query) -> Query:
        q = _preparse_for_shaper(q)
        q = _parse_viewer(self, q)
        return q


    def viewer(self, op: Operation, q: Query) -> Query:
        arg = op.args[0]
        pd.set_option('styler.format.na_rep', arg)

        #na_rep is only relevant if a styler
        #object is returned by the query,
        #which only happens if a style is created
        if q.style_vals is None:
            q.style_vals = pd.DataFrame(
                '',
                index=q.df.index,
                columns=q.df.columns,
                )

        return q



def _parse_viewer(
        token: Symbol,
        q: Query,
        ) -> Query:

    #transfer main attributes
    q.op.category = token.category
    q.op.operator = token.name
    q.op.viewer = token.viewer
    q.op.flags.update(token.op_flags)

    #transfer validation attributes
    q.op.args_min = token.op_args_min
    q.op.args_max = token.op_args_max
    q.op.connectors_allowed.update(token.op_connectors_allowed)
    q.op.scopes_allowed.update(token.op_scopes_allowed)
    q.op.args_allowed.update(token.op_args_allowed)
    q.op.flags_allowed.update(token.op_flags_allowed)
    q.op.flags_allowed.update(token.op_flags)

    return q




class ViewParserHelp(Symbol):
    """
    view debug information
    about currently available
    symbols during parsing

    Examples
    --------
    >>> qs(df, r'..help')
    """
    name = 'ViewParserHelp'
    category = 'viewer'
    regex = (r'\.\.help',)

    def parse(self, q: Query) -> Query:

        cols_show = [
            'name',
            'lexeme',
            'description',
            'example',
            ]

        if not q.op.scope:
            _print_or_display(
                'available scopes:',
                as_df('scopes')[cols_show],
                )

        if not q.op.operator:
            getters = _get_valid_operators(
                q.op,
                'getter',
                cols_show
                )
            _print_or_display(
                'get/select/filter cols/rows/vals:',
                getters[cols_show],
                )

            setters = _get_valid_operators(
                q.op,
                'setter',
                cols_show
                )
            _print_or_display(
                'set/change/modify cols/rows/vals:',
                setters[cols_show],
                )

            shapers = _get_valid_operators(
                q.op,
                'shaper',
                cols_show
                )
            _print_or_display(
                'change shape of data and metadata:',
                shapers[cols_show],
                )

            stylers = _get_valid_operators(
                q.op,
                'styler',
                cols_show
                )
            _print_or_display(
                'change style of cols/rows/vals:',
                stylers[cols_show],
                )

            viewers = _get_valid_operators(
                q.op,
                'viewer',
                cols_show
                )
            _print_or_display(
                'view debug information:',
                viewers[cols_show],
                )


        if not q.op.args and q.op.args_min > 0:
            print(f'Operator "{q.op.operator}" requires at least {q.op.args_min} args.')

        if q.op.args_allowed:
            df = pd.DataFrame(
                q.op.args_allowed.items(),
                columns=['arg', 'description'],
                )
            _print_or_display(
                'available args:',
                df,
                )

        if q.op.flags_allowed:
            df = pd.DataFrame(
                q.op.flags_allowed.items(),
                columns=['flag', 'description'],
                )
            _print_or_display(
                'available flags:',
                df,
                )

        return q




class ViewParserQuery(Symbol):
    """
    view debug information
    about the Query object
    during parsing

    Examples
    --------
    >>> qs(df, r'age  ..q')
    """
    name = 'ViewParserQuery'
    category = 'viewer'
    regex = (
        r'\.\.view_query',
        r'\.\.query',
        r'\.\.q',
        )

    def parse(self, q: Query) -> Query:
        print(q.str_debug())
        return q




class ViewParserOps(Symbol):
    """
    view debug information
    about current ops
    during parsing

    Examples
    --------
    >>> qs(df, r'age  ..ops')
    """
    name = 'ViewParserOps'
    category = 'viewer'
    regex = (r'\.\.ops',)

    def parse(self, q: Query) -> Query:
        strs_debug = [
            op.str_debug()
            for op
            in q.ops
            ]
        txt = 'Current ops:\n\n' + '\n\n'.join(strs_debug)
        print(txt)
        return q



class ViewParserOp(Symbol):
    """
    view debug information
    about current op
    during parsing

    Examples
    --------
    >>> qs(df, r'age  ..op')
    """
    name = 'ViewParserOp'
    category = 'viewer'
    regex = (r'\.\.op',)

    def parse(self, q: Query) -> Query:
        print(q.op.str_debug())
        return q




class ViewParserTokens(Symbol):
    """
    view debug information
    about current tokens
    during parsing

    Examples
    --------
    >>> qs(df, r'age  ..tokens')
    """
    name = 'ViewParserTokens'
    category = 'viewer'
    regex = (r'\.\.tokens',)

    def parse(self, q: Query) -> Query:
        strs_debug = [
            token.str_debug()
            for token
            in q.tokens
            ]
        txt = 'Current tokens:\n\n' + '\n\n'.join(strs_debug)
        print(txt)
        return q




class ViewParserToken(Symbol):
    """
    view debug information
    about the previous token
    during parsing
    (current token would be
    this parser token itself)

    Examples
    --------
    >>> qs(df, r'age  ..token')

    """
    name = 'ViewParserToken'
    category = 'viewer'
    regex = (r'\.\.token',)

    def parse(self, q: Query) -> Query:
        token = q.tokens[self.id - 1]
        print(token.str_debug())
        return q



def _get_valid_operators(
        op: Operation,
        category: str,
        cols_show: list[str],
        ) -> pd.DataFrame:

    operators = as_df(category)
    mask_rows = pd.Series(
        [True for _ in operators.index],
        index=operators.index,
        )
    if op.scope:
        mask_rows &= operators['op_scopes_allowed'].str.contains(op.scope)
    if op.connector:
        mask_rows &= operators['op_connectors_allowed'].str.contains(op.connector)
    operators = operators.loc[mask_rows, cols_show]

    return operators



def _print_or_display(
        txt: str,
        df: pd.DataFrame,
        ) -> None:
    if df.empty:
        return
    if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
        df_styled = (
            df
            .style
            .set_table_styles([_styles_table])  #pyright: ignore
            .set_properties(**_styles_cells)  #pyright: ignore
            )
        print(txt)
        display(df_styled)
    else:
        print(txt)
        print(df.to_string())


_styles_table = {
    'selector': 'th:not(.index_name)',
    'props': 'text-align: center;',
    }

_styles_cells = {
    'text-align': 'left',
    'white-space': 'pre-wrap',
    }




class Literal(Symbol):
    """
    literal token used for unquoted
    words, numbers and quoted strings.

    Examples
    --------
    >>> qs(df, r'% == age')
    >>> qs(df, r'% == "date of birth"')
    >>> qs(df, r'age  %%>30')
    >>> qs(df, r'age  %%>-30')
    >>> qs(df, r'age  %%>30.0')
    """
    name = 'Literal'
    category = 'syntax'
    regex = (
        r'\d\d[\.\-_]\d\d[\.\-_]\d\d\d\d',  #date
        r'\d\d\d\d[\.\-_]\d\d[\.\-_]\d\d',  #date
        r'-?\d+\.\d+',  #float
        r'-?\d+',  #int
        r'[a-zA-Z0-9_\-]+',  #unquoted string (e.g. col name or op arg)
        r'"[^"]*"',  #quoted string
        r"'[^']*'",  #quoted string
        )


    def build(self, str_matched: str) -> 'Symbol':
        token = self.copy()
        token.str_matched = str_matched
        if str_matched.startswith('"'):
            token.literal = str_matched.strip('"')
        elif str_matched.startswith("'"):
            token.literal = str_matched.strip("'")
        else:
            token.literal = str_matched
        return token


    def parse(self, q: Query) -> Query:
        q = _preparse_for_literal(self, q)
        q.op.args.append(self.literal)
        return q



def _preparse_for_literal(token: Symbol, q: Query) -> Query:

    if q.op.scope and q.op.operator:
        pass

    elif q.op.scope and not q.op.operator:
        q = GetEquals().parse(q)
        _check_if_operator_named(token.literal, q)

    else:
        q = _process_op(q)
        msg = 'Trace: inferring cols scope for literal token.'
        context = build_log_context('_preparse_for_literal')
        log(msg, context, q.verbosity)
        q.op.connector = 'new'
        q.op.scope = 'cols'
        q = GetEquals().parse(q)
        _check_if_operator_named(token.literal, q)

    return q



def _check_if_operator_named(literal: str, q: Query) -> None:

    if q.op.scope == 'cols' and literal not in q.df.columns:
        if literal in getters_named_regexes:
            prefix = ':'
        elif literal in setters_named_regexes:
            prefix = r'\.'
        else:
            return
        msg = (
            f'INFO: "{literal}" is not a col name, did you'
            f' mean to use the operator "{prefix}{literal}"?'
            )
        context = build_log_context(
            '_check_if_operator_named',
            literal=literal,
            op=q.op.str_debug(),
            )
        log(msg, context, q.verbosity)




class ListStart(Symbol):
    """
    starts a list of
    args and/or flags
    for an op

    Examples
    --------
    >>> qs(df, r'%==(name, age, +strict)')
    >>> qs(df, r'.newcol(year, 2001, +int)')
    """
    name = 'ListStart'
    category = 'syntax'
    regex = (r'\(',)


    def parse(self, q: Query) -> Query:

        #keep cases exhaustive (at the cost of repetition)!

        if q.op == Operation():
            q.op.connector = 'new'
            q.op.scope = 'cols'
            q = GetEquals().parse(q)
            q.op.list_started = True
            return q

        elif not q.op.scope and not q.op.operator:
            q.op.connector = 'new'
            q.op.scope = 'cols'
            q = GetEquals().parse(q)
            q.op.list_started = True
            return q

        elif not q.op.operator:
            q = GetEquals().parse(q)
            q.op.list_started = True
            return q

        elif len(q.op.args) > 0:
            msg = (
                f'ERROR: list start "{self.str_matched}" cannot be used'
                ' when args have already been added to the current op.'
                )
            context = build_log_context(
                'ListStart.parse',
                line=self.line,
                linenum=self.linenum,
                op=q.op.str_debug(),
                )
            log(msg, context, q.verbosity)
            return q

        #wip: should flags be allowed outside the list?

        elif q.op.list_stopped:
            msg = (
                f'ERROR: list start "{self.str_matched}"'
                ' cannot be used after a list stop token.'
                )
            context = build_log_context(
                'ListStart.parse',
                line=self.line,
                linenum=self.linenum,
                op=q.op.str_debug(),
                )
            log(msg, context, q.verbosity)
            return q

        else:
            q.op.list_started = True

        return q




class ListStop(Symbol):
    """
    stops a list of
    args and/or flags
    for an op

    Examples
    --------
    >>> qs(df, r'%==(name, age, +strict)')
    >>> qs(df, r'.newcol(year, 2001, +int)')
    """
    name = 'ListStop'
    category = 'syntax'
    regex = (r'\)',)

    def parse(self, q: Query) -> Query:

        if not q.op.list_started:
            msg = (
                f'ERROR: list stop "{self.str_matched}"'
                ' can only be used after a list start token.'
                )
            context = build_log_context(
                'ListStop.parse',
                line=self.line,
                linenum=self.linenum,
                op=q.op.str_debug(),
                )
            log(msg, context, q.verbosity)
            return q

        if q.op.list_stopped:
            msg = (
                f'ERROR: list stop "{self.str_matched}"'
                ' cannot be used if a list has not been'
                ' started or has already been stopped.'
                )
            context = build_log_context(
                'ListStop.parse',
                line=self.line,
                linenum=self.linenum,
                op=q.op.str_debug(),
                )
            log(msg, context, q.verbosity)
            return q

        else:
            q.op.list_stopped = True
            return q




class Separator(Symbol):
    """
    terminates tokens but is
    otherwise ignored while parsing.

    is interchangable with whitespace.

    use to visually separate args/flags
    to an op in a more explicit
    way than just whitespace.

    Examples
    --------
    #names containing "a" and "b"
    >>> qs(df, r'name  % ? a b')
    >>> qs(df, r'name  % ? a, b')
    >>> qs(df, r'name  % ? (a b)')
    >>> qs(df, r'name  % ? (a, b)')
    """
    name = 'Separator'
    category = 'syntax'
    regex = (r',',)




class Whitespace(Symbol):
    """
    terminates tokens but is
    otherwise ignored while parsing.

    spaces and tabs are interchangeable.

    use to separate
    args/flags to an op.

    Examples
    --------
    #names containing "a" and "b"
    >>> qs(df, r'name  % ? a b')
    """
    name = 'Whitespace'
    category = 'syntax'
    regex = (r'[ \t]+',)




class Comment(Symbol):
    """
    matches inline comments starting
    with "#". comment tokens are ignored.
    """
    name = 'Comment'
    category = 'syntax'
    regex = (r'#.*',)




class FlagNegate(Symbol):
    """
    negates the current
    negateable condition.

    Examples
    --------
    >>> qs(df, r'id   %%!>20000')
    """
    name = 'FlagNegate'
    category = 'syntax'
    regex = (r'!',)
    op_flags = {
        'negate': 'negate the condition',
        }

    def parse(self, q: Query) -> Query:
        q = _preparse_for_getter(q)
        q.op.flags.update(self.op_flags)
        return q




class FlagColref(Symbol):
    """
    interpret args as col references
    instead of literal values.

    Examples
    --------
    >>> qs(df, r'age  <@height')
    """
    name = 'FlagColref'
    category = 'syntax'
    regex = (r'@',)
    op_flags = {
        'colref': 'use a col reference for setting/getting vals',
        }

    def parse(self, q: Query) -> Query:

        if not q.op.operator:
            msg = 'ERROR: flag "colref" cannot be used without an operator.'
            context = build_log_context('FlagColref.parse')
            log(msg, context, q.verbosity)
            return q

        else:
            q.op.flags.update(self.op_flags)
            return q




class Flag(Symbol):
    """
    flag token used to modify
    operator behaviour

    Examples
    --------
    >>> qs(df, r'age  %%>30 +strict')
    """
    name = 'Flag'
    category = 'syntax'
    regex = (r'\+\w+',)

    def build(self, str_matched: str) -> 'Symbol':
        token = self.copy()
        token.str_matched = str_matched
        token.literal = str_matched.lstrip('+')
        return token

    def parse(self, q: Query) -> Query:
        if self.literal in q.op.flags_allowed:
            #adds the flags description found in flags allowed
            q.op.flags[self.literal] = q.op.flags_allowed[self.literal]
        else:
            q.op.flags[self.literal] = ''
        return q




all = []
syntax = []
scopes = []
operators = []
getters = []
setters = []
shapers = []
stylers = []
viewers = []
for _obj in list(locals().values()):
    if isinstance(_obj, type) and issubclass(_obj, Symbol):
        if _obj is not Symbol:
            all.append(_obj())
            if _obj.category == 'syntax':
                syntax.append(_obj())
            elif _obj.category == 'scope':
                scopes.append(_obj())
            elif _obj.category == 'getter':
                operators.append(_obj())
                getters.append(_obj())
            elif _obj.category == 'setter':
                operators.append(_obj())
                setters.append(_obj())
            elif _obj.category == 'shaper':
                operators.append(_obj())
                shapers.append(_obj())
            elif _obj.category == 'styler':
                operators.append(_obj())
                stylers.append(_obj())
            elif _obj.category == 'viewer':
                operators.append(_obj())
                viewers.append(_obj())



getters_named_regexes = []
setters_named_regexes = []
for operator in operators:
    for regex in operator.regex:
        if regex.startswith(r':'):
            getters_named_regexes.append(regex[1:])
        elif regex.startswith(r'\.'):
            setters_named_regexes.append(regex[2:])




def as_df(category='all') -> pd.DataFrame:
    singular = (
        'scope',
        'operator',
        'getter',
        'setter',
        'shaper',
        'styler',
        'viewer',
        )
    if category in singular:
        category += 's'

    if category == 'all':
        symbols = all
    elif category == 'syntax':
        symbols = syntax
    elif category == 'scopes':
        symbols = scopes
    elif category == 'operators':
        symbols = operators
    elif category == 'getters':
        symbols = getters
    elif category == 'setters':
        symbols = setters
    elif category == 'shapers':
        symbols = shapers
    elif category == 'stylers':
        symbols = stylers
    elif category == 'viewers':
        symbols = viewers
    else:
        raise ValueError(f"Unknown category: {category}")

    names = [s.name for s in symbols]
    lexemes = [_get_lexemes(s) for s in symbols]
    docs = [s.__doc__ for s in symbols]
    descriptions = [_get_description(d) for d in docs]
    examples = [_get_example(d) for d in docs]
    categories = [s.category for s in symbols]
    op_flags = ['\n'.join(s.op_flags) for s in symbols]
    op_flags_allowed = ['\n'.join(s.op_flags_allowed) for s in symbols]
    op_scopes_allowed = ['\n'.join(s.op_scopes_allowed) for s in symbols]
    op_connectors_allowed = ['\n'.join(s.op_connectors_allowed) for s in symbols]
    data = {
        'name': names,
        'lexeme': lexemes,
        'description': descriptions,
        'example': examples,
        'category': categories,
        'op_flags': op_flags,
        'op_flags_allowed': op_flags_allowed,
        'op_scopes_allowed': op_scopes_allowed,
        'op_connectors_allowed': op_connectors_allowed,
        }
    df = pd.DataFrame(data)
    return df


def as_df_styled(category='all') -> pd.io.formats.style.Styler:
    df = as_df(category)
    df_styled = (
        df
        .style
        .set_table_styles([_styles_table])  #pyright: ignore
        .set_properties(**_styles_cells)  #pyright: ignore
        )
    return df_styled


def _get_lexemes(symbol: Symbol) -> str:
    string = '\n'.join(symbol.regex).replace('\\', '')
    return string


def _get_description(string: str) -> str:
    string = (
        string
        .split('Examples')[0]
        .strip('\n')
        .rstrip()
        )
    return string


def _get_example(string: str) -> str:
    parts = string.split('--------')
    if len(parts) < 2:
        examples = ''
    else:
        examples = parts[1].replace('>>> ', '').strip()
    return examples
