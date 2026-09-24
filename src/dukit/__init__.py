
from importlib.metadata import version
__version__ = version('dukit')

from . import qlang
from .qlang import (
    q,
    qr,
    qs,
    )
from .interfaces import (
    DukitAccessor
    )
from .diffing import (
    diff,
    rediff,
    )
from .utils import (
    log,
    ensure_unique_string,
    )
from .excel import (
    format,
    save,
    )
from .pandas import (
    collapse,
    date_delta,
    date_table,
    deduplicate,
    embed,
    flatten,
    get_df,
    get_dfs,
    stagger,
    transpose,
    )
from .os import (
    cd,
    cp,
    fetch,
    isdir,
    isfile,
    ispath,
    mv,
    mkdir,
    pwd,
    )
from .typing import (
    Box,
    str_ as str,
    int_ as int,
    float_ as float,
    num_ as num,
    bool_ as bool,
    date_ as date,
    datetime_ as datetime,
    na_ as na,
    nk_ as nk,
    yn_ as yn,
    type_ as type,
    dtype_ as dtype,
    convert_ as convert,
    typeinfo_ as typeinfo,
    typeinfostrict_ as typeinfostrict,
    list_ as list,
    )


__all__ = (
    '__version__',

    'qlang',
    'q',
    'qr',
    'qs',
    'DukitAccessor',

    'diff',
    'rediff',

    'log',
    'ensure_unique_string',

    'format',
    'save',

    'collapse',
    'date_delta',
    'date_table',
    'deduplicate',
    'embed',
    'flatten',
    'get_df',
    'get_dfs',
    'stagger',
    'transpose',

    'cd',
    'cp',
    'fetch',
    'isdir',
    'isfile',
    'ispath',
    'mv',
    'mkdir',
    'pwd',

    'Box',
    'str',
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
    'dtype',
    'convert',
    'typeinfo',
    'typeinfostrict',
    'list',
    )
