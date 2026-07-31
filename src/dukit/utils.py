
import pandas as pd
import string as str_module
import datetime
import random

from collections.abc import Iterable
from IPython.display import display
from IPython.core.getipython import get_ipython
from .typing import str_

GREEN = '#6dae51'
RED = '#f73434'

GREY_LIGHT = '#d3d3d3'
BLUE_LIGHT = '#87ceeb'
GREEN_LIGHT = '#c0e7b0'
ORANGE_LIGHT = '#f7d67c'
RED_LIGHT = '#f7746a'


logs = []
_levels = {
    'TRACE': 5,
    'DEBUG': 4,
    'INFO': 3,
    'WARNING': 2,
    'ERROR': 1,
    }
_colors = {
    'TRACE': GREY_LIGHT,
    'DEBUG': BLUE_LIGHT,
    'INFO': GREEN_LIGHT,
    'WARNING': ORANGE_LIGHT,
    'ERROR': RED_LIGHT,
    }
_formats = {
    'TRACE': f'background-color: {_colors["TRACE"]}',
    'DEBUG': f'background-color: {_colors["DEBUG"]}',
    'INFO': f'background-color: {_colors["INFO"]}',
    'WARNING': f'background-color: {_colors["WARNING"]}',
    'ERROR': f'background-color: {_colors["ERROR"]}',
    }


def _build_log_context(
        function: str,
        verbosity=3,
        **kwargs,
        ) -> str:
    lines = [f'function: {function}\n']

    for key, value in kwargs.items():

        if isinstance(value, pd.DataFrame):
            pass
        elif isinstance(value, pd.Series):
            pass

        if isinstance(value, (tuple, list, dict)):
            value_str = str_(value)
        elif verbosity <= 3:
            value_str = repr(value)
        else:
            value_str = str(value)

        lines.append(f'{key}: {value_str}')

    return '\n'.join(lines)


def log(
        text: str = None,
        context: str = '',
        verbosity: int = None,
        clear: bool = False,
        ) -> pd.io.formats.style.Styler | None:
    """
    A very basic "logger" meant to be used in place
    of print() statements in jupyter notebooks.
    For more extensive logging purposes use a logging module.


    examples:

    from dukit import log

    log('trace: this is a trace entry which will be highlighted grey')
    log('debug: this is a debug entry which will be highlighted blue')
    log('info: this is a info entry which will be highlighted green')
    log('warning: this is a warning entry which will be highlighted orange')
    log('error: this is a error entry which will be highlighted red')

    log(clear=True)  #clear all log entries
    log()  #return dataframe of log entries
    dukit.utils.logs  #location of list containing log entries

    """
    if verbosity == 0:
        return None

    time = datetime.datetime.now()

    if clear:
        logs.clear()
        if verbosity in (None, 3, 4, 5):
            print('cleared all logs in dukit.util.logs.')
        return None

    if text is None:
        if len(logs) == 0:
            return pd.DataFrame().style
        df = pd.DataFrame(logs)
        col_format = df['level'].replace(_formats)
        df_style = pd.DataFrame(
            {col: col_format for col in df.columns},
            index=df.index,
            )
        df_styled = (
            df
            .style
            .apply(lambda x: df_style, axis=None)
            .set_properties(None, **{'text-align': 'left'})
            )
        return df_styled

    color = GREEN_LIGHT
    level = 'INFO'
    level_int = 3
    text_temp = text.upper()

    #detect logging level
    for level_temp in _levels.keys():
        if text_temp.startswith(level_temp):
            level = level_temp
            level_int = _levels[level]
            color = _colors[level]
            text = text[len(level_temp):].strip()
            if text and text[0] in [':', '-', ' ']:
                text = text[1:].strip()
            break

    if verbosity is None:
        verbosity = level_int

    if len(logs) == 0:
        total_ms = 0.0
        delta_ms = 0.0
    else:
        total_ms = datetime.datetime.now() - logs[0]['time']
        delta_ms = datetime.datetime.now() - logs[-1]['time']
        total_ms = total_ms.total_seconds() * 1000
        delta_ms = delta_ms.total_seconds() * 1000
    message = {
        'level': level,
        'text': text,
        'context': context,
        'time': time,
        'total_ms': total_ms,
        'delta_ms': delta_ms,
        }

    if level_int <= verbosity:
        logs.append(message)

        #for jupyter
        if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':  #pragma: no cover

            #make html friendly
            message['text'] = (
                message['text']
                .replace('<br>', '\n')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('\n', '<br>')
                .replace('\t', '&emsp;')
                )
            message['context'] = (
                message['context']
                .replace('<br>', '\n')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('\n', '<br>')
                .replace('\t', '&emsp;')
                )
            message_df = pd.DataFrame(message, index=[len(logs)])

            kwargs_format = {
                'whitespace': 'normal',
                'text-align': 'left',
                }
            display(
                message_df
                .style
                .hide(axis=1)
                .apply(lambda x: [f'background-color: {color}' for i in x], axis=1)
                .set_properties(None, **kwargs_format)
                )

        #everywhere else
        else:
            context_formatted = context.replace('\n', '\n    ')
            text_formatted = text.replace('\n', '\n    ')
            string = (
                f'{level} log message:\n'
                f'  time: {time}\n'
                f'  time since first log: {total_ms:.2f} ms\n'
                f'  time since last log: {delta_ms:.2f} ms\n'
                f'  context:{context_formatted}\n'
                f'  text:\n    """{text_formatted}"""\n'
                )
            print(string)



def ensure_unique_string(
        string: str,
        taken: Iterable[str],
        strategy: str = 'increment',
        ) -> str:
    """
    Ensure that a string is unique within a set of taken strings.

    Parameters
    ----------
    string : The original string to be made unique.
    taken : An iterable of strings that are already taken.
    strategy : The strategy to use for making the string unique. Default is 'increment'.
        * "increment": use incrementing numbers appended to the string.
        * "random": use random characters appended to the string.
        * "timestamp": use a timestamp appended to the string.
        * "datestamp": append the current date to the string.
            If date is already taken, incrementing numbers are appended.
        * "prefix=STR": prepend a custom prefix STR to the string.
            Will keep prepending until the string is unique.
        * "suffix=STR": append a custom suffix STR to the string.
            Will keep appending until the string is unique.

    """

    base_string = string

    if strategy == 'increment':
        counter = 1
        while string in taken:
            string = f"{base_string}{counter}"
            counter += 1
    elif strategy == 'random':
        while string in taken:
            chars = str_module.ascii_letters + str_module.digits
            rand_str = ''.join(random.choices(chars, k=6))
            string = f"{base_string}_{rand_str}"
    elif strategy == 'timestamp':
        while string in taken:
            timestamp = datetime.datetime.now().strftime('%Y_%m_%d_%Hh%Mm%Ss')
            string = f"{base_string}_{timestamp}"
    elif strategy == 'datestamp':
        datestamp = datetime.datetime.now().strftime('%Y_%m_%d')
        string_temp = f"{base_string}_{datestamp}"
        counter = 1
        while string_temp in taken:
            string_temp = f"{base_string}_{datestamp}_v{counter}"
            counter += 1
        string = string_temp
    elif strategy.startswith('prefix='):
        prefix = strategy.split('=')[1]
        while string in taken:
            string = f"{prefix}{string}"
    elif strategy.startswith('suffix='):
        suffix = strategy.split('=')[1]
        while string in taken:
            string = f"{string}{suffix}"
    else:
        raise ValueError(f'Unknown strategy: {strategy}')

    return string



def now(fmt='%Y_%m_%d'):
    """
    alias for datetime.datetime.now().strftime(format_str)

    common format_str options:
    '%Y_%m_%d_%Hh%Mm%Ss': standard
    %Y_%b_%d:  3 letter month
    """
    return datetime.datetime.now().strftime(fmt)
