
import pandas as pd
import os
import shutil
import datetime
from .utils import log
from .typing import date_, datetime_



def pwd():
    """
    return the path to the current working directory.

    Returns
    -------
    str
        current working directory.
    """
    return os.getcwd()



def ls(path='', recursive=False) -> pd.DataFrame:
    """
    list files and directories in a path.

    Parameters
    ----------
    path : str, default ''
        directory to inspect. an empty path uses the current directory.
    recursive : bool, default False
        whether to include files in nested directories.

    Returns
    -------
    pandas.DataFrame
        file metadata including path, size, timestamps, permissions, and type.
    """

    if path == '':
        path = os.getcwd()

    if recursive is True:
        filepaths = []
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                filepaths.append(os.path.join(root, filename))
    else:
        filepaths = [os.path.join(path, filename) for filename in os.listdir(path)]

    files = pd.DataFrame()
    files['_path'] = filepaths
    files['name'] = files['_path'].apply(lambda x: os.path.basename(x))
    files['size'] = files['_path'].apply(
        lambda x: (
            os.path.getsize(x)
            if os.path.isfile(x)
            else None
            )
        )
    files['created'] = files['_path'].apply(
        lambda x: (
            datetime
            .datetime
            .fromtimestamp(os.path.getctime(x))
            .strftime('%Y-%m-%d %H:%M:%S')
            )
        )
    files['last modified'] = files['_path'].apply(
        lambda x: (
            datetime
            .datetime
            .fromtimestamp(os.path.getmtime(x))
            .strftime('%Y-%m-%d %H:%M:%S')
            )
        )
    files['last accessed'] = files['_path'].apply(
        lambda x: (
            datetime
            .datetime
            .fromtimestamp(os.path.getatime(x))
            .strftime('%Y-%m-%d %H:%M:%S')
            )
        )
    files['permissions'] = files['_path'].apply(
        lambda x: (
            oct(os.stat(x).st_mode)[-3:]
            if os.path.isfile(x)
            else None
            )
        )
    files['path'] = files['_path']
    files['folder'] = files['_path'].apply(lambda x: os.path.dirname(x))
    files['type'] = files['_path'].apply(
        lambda x: (
            'dir'
            if os.path.isdir(x)
            else os.path.splitext(x)[1]
            )
        )

    files.drop(columns='_path', inplace=True)

    return files



def lsr(path='') -> pd.DataFrame:
    """recursively list files and directories below ``path``."""
    return ls(path, recursive=True)



def cd(path=None, verbosity=3):
    """
    change the current working directory.

    Parameters
    ----------
    path : str, optional
        destination directory. ``None``, ``''``, and ``'.'`` mean the current
        directory; ``'..'`` means the parent directory.
    verbosity : int, default 3
        logging verbosity level.

    Returns
    -------
    None
    """

    if path is None:
        path = os.getcwd()
    elif path in ('', '.'):
        path = os.getcwd()
    elif path == '..':
        path = os.path.dirname(os.getcwd())

    dir_old = os.getcwd()
    if dir_old.endswith(path):
        log(f'INFO: already in "{path}"', f'dk.cd("{path}")', verbosity)
        return

    os.chdir(path)
    dir_new = os.getcwd()
    text = f'INFO: moved from<br>"{dir_old}"<br>to<br>"{dir_new}"'
    log(text, f'dk.cd("{path}")', verbosity)
    return



def cp(src, dest, verbosity=3):
    """
    copy a file or directory.

    Parameters
    ----------
    src, dest : str or os.PathLike
        source and destination paths.
    verbosity : int, default 3
        logging verbosity level.

    Returns
    -------
    None
    """

    if os.path.isdir(dest):
        dest = os.path.join(dest, os.path.basename(src))

    if os.path.exists(dest):
        text = f'WARNING: "{dest}" already exists and will be overwritten'
        log(text, 'dk.cp()', verbosity)

    if os.path.isdir(src):
        shutil.copytree(src, dest)
    else:
        shutil.copy(src, dest)

    log(f'INFO: copied<br>{src}<br>to<br>{dest}', 'dk.cp()', verbosity)
    return



def mv(src, dest, verbosity=3):
    """
    move a file or directory.

    Parameters
    ----------
    src, dest : str or os.PathLike
        source and destination paths.
    verbosity : int, default 3
        logging verbosity level.
    """

    if os.path.isdir(dest):
        dest = os.path.join(dest, os.path.basename(src))

    if os.path.exists(dest):
        text = f'WARNING: "{dest}" already exists and will be overwritten'
        log(text, 'dk.mv()', verbosity)

    shutil.move(src, dest)

    text = f'INFO: moved<br>"{src}"<br>to<br>"{dest}"'
    log(text, 'dk.mv()', verbosity)
    return



def mkdir(name, verbosity=3):
    """
    create a directory if it does not already exist.

    Parameters
    ----------
    name : str or os.PathLike
        directory path.
    verbosity : int, default 3
        logging verbosity level.
    """
    if os.path.isdir(name):
        text = f'INFO: directory "{name}" already exists'
        log(text, f'dk.mkdir("{name}")', verbosity)
    else:
        os.mkdir(name)
        text = f'INFO: created directory "{name}"'
        log(text, f'dk.mkdir("{name}")', verbosity)
    return



def isdir(name):
    """return whether ``name`` is an existing directory."""
    return os.path.isdir(name)



def isfile(name):
    """return whether ``name`` is an existing file."""
    return os.path.isfile(name)



def ispath(name):
    """return whether ``name`` exists as a file or directory."""
    return os.path.exists(name)



nums_str = [
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    ]
def fetch(path, before='now', verbosity=3):
    """
    return the most recent dated version of a file.

    Parameters
    ----------
    path : str or os.PathLike
        file path or filename prefix.
    before : str, default 'now'
        cutoff such as ``'today'``, ``'this week'``, ``'this month'``,
        ``'this year'``, or a date string.
    verbosity : int, default 3
        logging verbosity level.

    Returns
    -------
    str or None
        path to the newest matching file, if one exists.
    """

    if os.path.isfile(path):
        log(f'INFO: found file "{path}"', 'dk.fetch()', verbosity)
        return path

    today = datetime.date.today()


    if before == 'now':
        cutoff = today + datetime.timedelta(days=1)
    elif before == 'today':
        cutoff = today
    elif before == 'this day':
        cutoff = today
    elif before == 'this week':
        cutoff = today - datetime.timedelta(days=today.weekday())
    elif before == 'this month':
        cutoff = today - datetime.timedelta(days=today.day - 1)
    elif before == 'this year':
        cutoff = pd.to_datetime(f'{today.year}0101').date()
    else:
        cutoff = date_(before)


    name = os.path.basename(path)
    folder = os.path.dirname(path)
    extension = ''


    if folder == '':
        folder = os.getcwd()

    timestamps = pd.Series([])
    for file in os.listdir(folder):
        #check if file starts with name and is a file
        filepath = os.path.join(folder, file)
        if os.path.isfile(filepath) and file.startswith(name):
            try:
                timestamp_str_full = file.split(name)[-1]
                if timestamp_str_full[0] not in nums_str:
                    continue
                extension = '.' + timestamp_str_full.split('.')[-1]
                timestamp_str = timestamp_str_full.replace(f'{extension}', '')
                timestamp = datetime_(timestamp_str)
                if timestamp < datetime_(cutoff):
                    timestamps[timestamp] = (timestamp_str, extension)
            except Exception:
                pass
    if len(timestamps) == 0:
        text = (
            'ERROR: no timestamped files starting with'
            f' "{name}" found in "{folder}" before {cutoff}'
            )
        log(text, 'dk.fetch()', verbosity)
        raise FileNotFoundError(text)
    else:
        timestamps = timestamps.sort_index()
        latest = timestamps.iloc[len(timestamps) - 1][0]
        extension = timestamps.iloc[len(timestamps) - 1][1]
        path = os.path.join(folder, f'{name}{latest}{extension}')
        log(f'INFO: found file "{path}"', 'dk.fetch()', verbosity)
        return path
