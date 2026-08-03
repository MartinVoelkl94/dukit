
import pandas as pd
import numpy as np
import re
import typing
import datetime
from pandas import isna


TYPES_INT: tuple[type, ...] = (
    int,
    np.int64,
    np.int32,
    np.int16,
    np.int8,
    pd.Int64Dtype,
    pd.Int32Dtype,
    pd.Int16Dtype,
    pd.Int8Dtype,
    )
TYPES_FLOAT: tuple[type, ...] = (
    float,
    np.float64,
    np.float32,
    np.float16,
    pd.Float64Dtype,
    pd.Float32Dtype,
    )
TYPES_NUM: tuple[type, ...] = (
    int,
    float,
    np.int64,
    np.float64,
    np.int32,
    np.float32,
    np.int16,
    np.float16,
    np.int8,
    np.number,
    pd.Int64Dtype,
    pd.Float64Dtype,
    pd.Int32Dtype,
    pd.Float32Dtype,
    pd.Int16Dtype,
    pd.Int8Dtype,
    )
TYPES_STR: tuple[type, ...] = (
    str,
    pd.StringDtype,
    )
TYPES_BOOL: tuple[type, ...] = (
    bool,
    np.bool_,
    pd.BooleanDtype,
    )
TYPES_DATE: tuple[type, ...] = (
    datetime.date,
    pd.Timestamp,
    )

VALUES_NA = (
    '',
    'na',
    '<na>',
    'n/a',
    '<n/a>',
    'n.a',
    'n.a.',
    'na.',
    'n.a',
    'nan',
    'n.a.n',
    'n.a.n.',
    'not available',
    'not applicable',
    'not a number',
    'missing',
    'missing.',
    'null',
    'nil',
    'none',
    'void',
    'blank',
    'empty',
    )
VALUES_NK = (
    'unk',
    'unknown',
    'not known',
    'not known.',
    'nk',
    'n.k.',
    'n.k',
    'n/k',
    'not specified',
    'not specified.',
    )

DTYPES_ALLOWED = set([
    'string',
    'Int64',
    'Float64',
    'boolean',
    'datetime64[s]',
    'datetime64[us]',
    'object',
    ])



def str_(x, spacer='\n  ') -> str:
    if isinstance(x, str):
        return x
    elif isinstance(x, tuple):
        return _tuple_to_str(x, spacer)
    elif isinstance(x, (list, pd.Series, pd.Index)):
        return _list_to_str(x, spacer)
    elif isinstance(x, dict):
        return _dict_to_str(x, spacer)
    else:
        return str(x)



def _tuple_to_str(tpl: tuple, spacer='\n  ') -> str:
    if len(tpl) < 2:
        return str(tpl)
    str_tpl = (
        '('
        + spacer
        + spacer.join(f'{item!r}' for item in tpl)
        + '\n)'
        )
    return str_tpl



def _list_to_str(
        lst: list | pd.Series | pd.Index,
        spacer='\n  ',
        ) -> str:

    if isinstance(lst, pd.Series):
        lst = lst.to_list()
    elif isinstance(lst, pd.Index):
        lst = lst.to_list()

    if len(lst) < 2:
        return str(lst)
    str_lst = (
        '['
        + spacer
        + spacer.join(f'{item!r}' for item in lst)
        + '\n]'
        )

    return str_lst



def _dict_to_str(d: dict, spacer='\n  ') -> str:
    if len(d) < 2:
        return str(d)
    kvs = (
        f'{k!r}: {v!r}'
        for k, v in
        d.items()
        )
    str_d = (
        '{'
        + spacer
        + spacer.join(kvs)
        + '\n}'
        )
    return str_d



def int_(x, errors='coerce', na=np.nan) -> typing.Any:
    if x is True or x is False:
        return na
    elif isinstance(x, TYPES_INT):
        return x
    elif isinstance(x, str):
        x = x.replace(',', '.')
    try:
        return round(float(x))  #float first to handle strings like '1.0'
    except Exception as e:
        if errors == 'raise':
            raise ValueError(
                f'could not convert "{x}" to integer.\n'
                'Error handling:\n'
                'errors="raise": raises a ValueError\n'
                'errors="ignore": returns the original value\n'
                'errors="coerce": returns np.nan\n'
                'errors=<any other value>: returns <any other value>\n'
                f'original error:\n{e}'
                )
        elif errors == 'ignore':
            return x
        elif errors == 'coerce':
            return na
        else:
            return errors



def float_(x, errors='coerce', na=np.nan) -> typing.Any:
    if isinstance(x, TYPES_FLOAT):
        return x
    elif isinstance(x, str):
        x = x.replace(',', '.')
    try:
        return float(x)
    except Exception as e:
        if errors == 'raise':
            raise ValueError(
                f'could not convert "{x}" to float.\n'
                'Error handling:\n'
                'errors="raise": raises a ValueError\n'
                'errors="ignore": returns the original value\n'
                'errors="coerce": returns np.nan\n'
                'errors=<any other value>: returns <any other value>\n'
                f'original error:\n{e}'
                )
        elif errors == 'ignore':
            return x
        elif errors == 'coerce':
            return na
        else:
            return errors



def num_(x, errors='coerce', na=np.nan) -> typing.Any:
    if isinstance(x, TYPES_NUM):
        return x
    try:
        return pd.to_numeric(x)
    except Exception as e:
        if errors == 'raise':
            raise ValueError(
                f'could not convert "{x}" to numeric value.\n'
                'Error handling:\n'
                'errors="raise": raises a ValueError\n'
                'errors="ignore": returns the original value\n'
                'errors="coerce": returns np.nan\n'
                'errors=<any other value>: returns <any other value>\n'
                f'original error:\n{e}'
                )
        elif errors == 'ignore':
            return x
        elif errors == 'coerce':
            return na
        else:
            return errors



def bool_(x, errors='coerce', na=None) -> typing.Any:
    if isinstance(x, TYPES_BOOL):
        return x
    elif str(x).lower() in ['y', 'yes', 'true', '1', '1.0', 'positive', 'pos']:
        return True
    elif str(x).lower() in ['n', 'no', 'false', '0', '0.0', 'negative', 'neg']:
        return False
    else:
        if errors == 'raise':
            raise ValueError(
                f'could not convert "{x}" to numeric boolean.\n'
                'Error handling:\n'
                'errors="raise": raises a ValueError\n'
                'errors="ignore": returns the original value\n'
                'errors="coerce": returns np.nan\n'
                'errors=<any other value>: returns <any other value>\n'
                )
        elif errors == 'ignore':
            return x
        elif errors == 'coerce':
            return na
        else:
            return errors



_months_txt = (
    'Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|'
    'January|February|March|April|May|June|July|'
    'August|September|October|November|December'
    )
def date_(x, errors='coerce', na=pd.NaT) -> typing.Any:
    """
    recognizes and converts potential dates
    between 0001-01-01 and 2999-12-31 in various formats.
    """
    result = datetime_(x, errors=errors, na=na)
    if result is na:
        return na
    elif isinstance(result, datetime.datetime) or isinstance(result, pd.Timestamp):
        return result.date()

    #raise and coerce are handled in _datetime and should not be reached here
    elif errors == 'raise':  #pragma: no cover
        raise ValueError(
            f'could not convert "{x}" to datetime.\n'
            'Error handling:\n'
            'errors="raise": raises a ValueError\n'
            'errors="ignore": returns the original value\n'
            'errors="coerce": returns np.nan\n'
            'errors=<any other value>: returns <any other value>\n'
            )
    elif errors == 'ignore':
        return x
    elif errors == 'coerce':
        return na  #pragma: no cover
    else:
        return errors



def datetime_(x, errors='coerce', na=pd.NaT) -> typing.Any:
    if isinstance(x, datetime.datetime):
        return x
    elif isinstance(x, datetime.date):
        return pd.to_datetime(x)
    elif isinstance(x, str):
        x = x.replace('.', '-')
        x = x.replace('/', '-')
        x = x.replace('\\', '-')
        x = x.replace('_', '-')
    try:

        if len(str(x).strip()) < 8:
            raise ValueError(f'could not convert "{x}" to date: too short to be a date')

        elif re.fullmatch(r'[012]\d\d\d[-\d\s:]+.*', x):
            result = pd.to_datetime(x, dayfirst=False)

        elif re.match(
                f'(\\d\\d\\d\\d)\\D?({_months_txt})\\D?(\\d\\d)',
                x,
                flags=re.IGNORECASE,
                ):
            x = re.sub(
                f'(\\d\\d\\d\\d)\\D?({_months_txt})\\D?(\\d\\d)(.*)',
                r'\3-\2-\1\4',
                x,
                flags=re.IGNORECASE,
                )
            result = pd.to_datetime(x, dayfirst=True)

        elif re.match(
                f'(\\d\\d)\\D?({_months_txt})\\D?(\\d\\d\\d\\d)',
                x,
                flags=re.IGNORECASE,
                ):
            x = re.sub(
                f'(\\d\\d)\\D?({_months_txt})\\D?(\\d\\d\\d\\d)(.*)',
                r'\1-\2-\3\4',
                x,
                flags=re.IGNORECASE,
                )
            result = pd.to_datetime(x, dayfirst=True)

        elif re.match(
                f'({_months_txt})\\D?(\\d\\d)\\D?(\\d\\d\\d\\d)',
                x,
                flags=re.IGNORECASE,
                ):
            x = re.sub(
                f'({_months_txt})\\D?(\\d\\d)\\D?(\\d\\d\\d\\d)(.*)',
                r'\2-\1-\3\4',
                x,
                flags=re.IGNORECASE,
                )
            result = pd.to_datetime(x, dayfirst=True)

        else:
            result = pd.to_datetime(x, dayfirst=True)

        if result is pd.NaT:
            raise ValueError(f'could not convert "{x}" to date')
        else:
            return result
    except Exception as e:
        if errors == 'raise':
            raise ValueError(
                f'could not convert "{x}" to datetime.\n'
                'Error handling:\n'
                'errors="raise": raises a ValueError\n'
                'errors="ignore": returns the original value\n'
                'errors="coerce": returns np.nan\n'
                'errors=<any other value>: returns <any other value>\n'
                f'original error:\n{e}'
                )
        elif errors == 'ignore':
            return x
        elif errors == 'coerce':
            return na
        else:
            return errors



def na_(x, errors='ignore', na=None) -> typing.Any:

    if str(x).lower().strip() in VALUES_NA:
        return na
    elif isna(x):
        return na
    else:
        if errors == 'raise':
            raise ValueError(
                f'could not convert "{x}" to "{na}".\n'
                'Error handling:\n'
                'errors="raise": raises a ValueError\n'
                'errors="ignore": returns the original value\n'
                'errors="coerce": returns np.nan\n'
                'errors=<any other value>: returns <any other value>\n'
                )
        elif errors == 'ignore':
            return x
        elif errors == 'coerce':
            return None
        else:
            return errors



def nk_(x, errors='ignore', nk='unknown', na=None) -> typing.Any:
    if str(x).lower().strip() in VALUES_NK:
        return nk
    else:
        if errors == 'raise':
            raise ValueError(
                f'could not convert "{x}" to "{nk}".\n'
                'Error handling:\n'
                'errors="raise": raises a ValueError\n'
                'errors="ignore": returns the original value\n'
                'errors="coerce": returns np.nan\n'
                'errors=<any other value>: returns <any other value>\n'
                )
        elif errors == 'ignore':
            return x
        elif errors == 'coerce':
            return na
        else:
            return errors



def yn_(x, errors='coerce', yes='yes', no='no', na=None) -> typing.Any:
    if str(x).lower() in ['y', 'yes', 'true', '1', '1.0', 'positive', 'pos']:
        return yes
    elif str(x).lower() in ['n', 'no', 'false', '0', '0.0', 'negative', 'neg']:
        return no
    else:
        if errors == 'raise':
            raise ValueError(
                f'could not convert "{x}" to "{yes}" or "{no}".\n'
                'Error handling:\n'
                'errors="raise": raises a ValueError\n'
                'errors="ignore": returns the original value\n'
                'errors="coerce": returns np.nan\n'
                'errors=<any other value>: returns <any other value>\n'
                )
        elif errors == 'ignore':
            return x
        elif errors == 'coerce':
            return na
        else:
            return errors



def type_(x) -> str:
    """
    Returns what type something "should" be. e.g.: dk.type('1') == 'int'
    """

    if isinstance(x, bool):
        return 'bool'
    elif isinstance(x, TYPES_INT):
        return 'int'
    elif isinstance(x, TYPES_FLOAT):
        return 'float'
    elif datetime_(x) is not pd.NaT:
        x = str(x).strip()
        if re.fullmatch(r'\d*', x):
            return 'int'
        elif re.search(r'\d\d:\d\d', x):
            return 'datetime'
        else:
            return 'date'

    elif isinstance(x, str):
        x = x.strip()
        if re.fullmatch(r'(true|false)', x, re.IGNORECASE):
            return 'bool'
        elif re.fullmatch(r'-?\d+', x):
            return 'int'
        elif re.fullmatch(r'-?\d+[\.,]\d+', x):
            return 'float'
        elif str(x).lower() in VALUES_NA:
            return 'na'
        else:
            try:
                x = pd.to_numeric(x)
                return 'num'
            except Exception:
                return 'str'

    elif pd.isna(x):
        return 'na'

    else:
        return type(x).__name__


_conversion_mapping = {
    'int': int_,
    'float': float_,
    'num': num_,
    'bool': bool_,
    'date': date_,
    'datetime': datetime_,
    'na': na_,
    'nk': nk_,
    'yn': yn_,
    'NoneType': lambda x, errors, na: na,
    }
def convert_(value, errors='coerce', na=None) -> typing.Any:
    """
    Converts to the type something "should" be according to dk.type().
    e.g.: dk.convert('1') == 1
    """
    type_name = type_(value)
    if type_name == 'str':
        result = str(value)
    elif type_name in _conversion_mapping:
        result = _conversion_mapping[type_name](value, errors, na)
    else:
        result = value
    return result


def repr_(x) -> str:
    txt = f'{x!r}'
    return txt


def typeinfo_(x) -> str:
    type_inferred = type_(x)
    new = convert_(x)
    #"<{type_inferred}>" would get interpreted as a html tag by the pandas styler
    txt = f'{x!r} [{type_inferred}] {new!r}'
    return txt


def typeinfostrict_(x) -> str:
    type_strict = type(x).__name__
    #"<{type_inferred}>" would get interpreted as a html tag by the pandas styler
    txt = f'{x!r} [{type_strict}]'
    return txt



def list_(x) -> list:
    if x is None:
        return []
    elif isinstance(x, list):
        return x
    elif isinstance(x, str):
        return [x]
    elif hasattr(x, '__iter__'):
        return list(x)
    else:
        return [x]



class Box:
    """
    - stores key-value pairs as attributes
    - prevents collisions with class methods and reserved attributes
    - provides dict-like introspection via keys(), values(), items()
    - debug-friendly self referential representation
    """

    #essential methods

    def __init__(
            self,
            **kwargs,
            ):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


    def __setattr__(
            self,
            name: str,
            value: typing.Any,
            ):
        if name in dir(Box):
            msg = (
                f'{name!r}'
                ' is a reserved attribute/method name.'
                )
            raise AttributeError(msg)
        super().__setattr__(name, value)


    def __getitem__(
            self,
            key: str,
            ):
        return self.__dict__[key]


    #dict-like interface

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()


    #utility

    def __repr__(self):
        txt = (
            f'<{self.__class__.__name__};'
            f' {len(self.__dict__)} attributes>'
            )
        return txt

    def __str__(self):
        kwargs = [(k, v) for k, v in self.__dict__.items()]
        if len(kwargs) == 0:
            txt = f'{self.__class__.__name__}()'
        elif len(kwargs) == 1:
            content = f'{kwargs[0][0]}={kwargs[0][1]!r}'
            txt = f'{self.__class__.__name__}({content})'
        else:
            content = []
            for k, v in kwargs:
                if isinstance(v, Box):
                    v = str(v).replace('\n', '\n  ')
                    content.append(f'  {k} = {v},')
                elif isinstance(v, pd.DataFrame):
                    cols = len(v.columns)
                    rows = len(v.index)
                    v = f'<DataFrame; cols={cols}, rows={rows}>'
                    content.append(f'  {k} = {v},')
                else:
                    content.append(f'  {k} = {v!r},')
            content = '\n'.join(content)
            txt = f'{self.__class__.__name__}(\n{content}\n  )'
        return txt

    def print(self):
        print(str(self))

    def __eq__(self, value):
        if isinstance(value, self.__class__):
            return self.__dict__ == value.__dict__
        else:
            return False

    def clear(self):
        for key in list(self.__dict__.keys()):
            del self.__dict__[key]

    def copy(self):
        return self.__class__(**self.__dict__)

    def new(self, **kwargs):
        return self.__class__(**kwargs)
