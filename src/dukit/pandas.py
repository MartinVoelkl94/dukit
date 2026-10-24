
import re
import copy
import datetime
import numpy as np
import pandas as pd

from .utils import (
    log,
    ensure_unique_string,
    GREEN_LIGHT,
    )
from .typing import (
    date_,
    list_,
    )


def get_df() -> pd.DataFrame:
    """
    return the package's sample df.

    Returns
    -------
    pandas.DataFrame
        small, intentionally messy medical-style
        dataset used in examples and tests.
    """
    data = {
        'ID': [
            10001,
            10002,
            10003,
            20001,
            20002,
            20003,
            30001,
            30002,
            30003,
            30004,
            30005,
            ],
        'name': [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            'eva white',
            'Frank miller',
            'Grace TAYLOR',
            'Harry Clark',
            'IVY GREEN',
            'JAck Williams',
            'john Doe',
            ],
        'date of birth': [
            pd.to_datetime('1995-01-02'),
            datetime.datetime(1990, 9, 14),
            '1985.08.23',
            '19800406',
            '05-11-2007',
            pd.to_datetime('06-30-1983').date(),
            datetime.datetime(1975, 5, 28).date(),
            '1960Mar08',
            '1955-Jan-09',
            '1950 Sep 10',
            '1945 October 11',
            ],
        'age': [
            -25,
            '30',
            np.nan,
            pd.NaT,
            '40.0',
            'forty-five',
            'nan',
            'unk',
            '',
            'unknown',
            35,
            ],
        'gender': [
            'M',
            'F',
            'Female',
            'Male',
            'Other',
            'm',
            'ff',
            'NaN',
            None,
            'Mal',
            'female',
            ],
        'height': [
            170,
            '175.5cm',
            None,
            '280',
            'NULL',
            '185',
            '1',
            '6ft 1in',
            -10,
            '',
            200,
            ],
        'weight': [
            70.2,
            '68',
            '72.5lb',
            'na',
            '',
            '75kg',
            None,
            '80.3',
            '130lbs',
            '1e2',
            -65,
            ],
        'bp systole': [
            ' 20 ',
            130,
            '<NA>',
            -np.inf,
            '135mmhg',
            '125.5',
            'NAN',
            '122,3',
            '',
            130,
            '45',
            ],
        'bp diastole': [
            80,
            '85',
            'N/A',
            '90mmHg',
            np.nan,
            '75',
            'NaN',
            pd.NA,
            '95',
            '0',
            'None ',
            ],
        'cholesterol': [
            'Normal',
            'Highe',
            'NaN',
            'GOOD',
            'n.a.',
            'High',
            'Normal',
            'n/a',
            'high',
            '',
            'Normal',
            ],
        'diabetes': [
            False,
            'true',
            'N/A',
            0,
            '1',
            'Yes',
            'NO',
            None,
            'NaN',
            'n',
            True,
            ],
        'dose': [
            '10kg',
            'NaN',
            '15 mg once a day',
            '20mg',
            '20 Mg',
            '25g',
            'NaN',
            None,
            '30 MG',
            ' 35 ',
            '40ml',
            ],
        }
    df = pd.DataFrame(data).convert_dtypes()
    df.columns = df.columns.to_series().convert_dtypes()
    df.index = df.index.to_series().convert_dtypes()
    return df



def get_df_patients() -> pd.DataFrame:
    patients = pd.DataFrame({
        'id': [
            10001,
            10002,
            20001,
            30001,
            ],
        'name': [
            'John Doe',
            'Jane Smith',
            'Alice Johnson',
            'Bob Brown',
            ],
        'age': [
            25,
            30,
            35,
            40,
            ],
        })
    return patients



def get_df_medications() -> pd.DataFrame:
    medications = pd.DataFrame({
        'id': [
            10002,
            20001,
            20001,
            30001,
            30001,
            30001,
            ],
        'medication': [
            'Aspirin',
            'Ibuprofen',
            'Paracetamol',
            'Amoxicillin',
            'Ciprofloxacin',
            'Metformin',
            ],
        'dose': [
            100,
            200,
            pd.NA,
            250,
            500,
            1000,
            ],
        'unit': [
            'mg',
            'mg',
            '',
            'mg',
            'ml',
            'mg',
            ]
        })
    return medications


def get_df_old() -> pd.DataFrame:

    old = pd.DataFrame(
        columns=['a', 'b', 'c'],
        index=['x', 'y', 'z', ],
        )

    old.insert(0, 'uid', old.index)

    old.loc['x', 'a'] = 1
    old.loc['x', 'b'] = 1
    old.loc['x', 'c'] = 1

    old.loc['y', 'a'] = 2
    old.loc['y', 'b'] = 2
    old.loc['y', 'c'] = 2

    old.loc['z', 'a'] = 3
    old.loc['z', 'b'] = None
    old.loc['z', 'c'] = 3

    return old


def get_df_new() -> pd.DataFrame:

    new = pd.DataFrame(
        columns=['d', 'b', 'a'],
        index=['y', 'x2', 'z', ],
        )

    new.insert(0, 'uid', new.index)

    new.loc['y', 'd'] = 2
    new.loc['y', 'b'] = 2
    new.loc['y', 'a'] = 0

    new.loc['x2', 'd'] = 1
    new.loc['x2', 'b'] = 1
    new.loc['x2', 'a'] = 1

    new.loc['z', 'd'] = 3
    new.loc['z', 'b'] = 3
    new.loc['z', 'a'] = pd.NA

    return new



def date_delta(
        df: pd.DataFrame,
        reference_date: str | datetime.date | pd.Timestamp = None,
        reference_col: str = None,
        linebreak: str = '\n',
        verbosity: int = 3,
        ):
    """
    calculates the number of days
    between a reference date or col
    and all other date cols in the df.

    Returns
    -------
    pandas.DataFrame
        copy of ``df`` with normalized dates and day-difference cols.
    """

    if reference_date is None and reference_col is None:
        msg = 'ERROR: no reference date or column provided'
        log(msg, 'dk.date_delta', verbosity)
        return df

    if reference_date is not None and reference_col is not None:
        msg = 'ERROR: both reference date and column provided'
        log(msg, 'dk.date_delta', verbosity)
        return df


    df = df.copy()
    df_dates = (
        df
        .copy()
        .map(date_)
        .convert_dtypes()
        )
    cols_dates = []
    cols_all = list(df.columns)

    for col in df_dates.columns:
        if df_dates[col].isna().all():
            df_dates.drop(columns=col, inplace=True)
        else:
            cols_dates.append(col)
            df.drop(columns=col, inplace=True)

    df = pd.concat([df, df_dates], axis=1)[cols_all]


    if 'reference_date' in df.columns:
        msg = 'WARNING: column "reference_date" already exists, overwriting'
        log(msg, 'dk.date_delta', verbosity)
    if reference_date is not None:
        df['reference_date'] = date_(reference_date)
        reference_col = str(reference_date)
    else:
        df['reference_date'] = df[reference_col].apply(date_)

    cols_reorder = [col for col in df.columns]
    df = df[cols_reorder]

    for col in df.columns:
        if col not in cols_dates:
            continue
        if col in ['reference_date', reference_col]:
            continue

        name = f'days from{linebreak}{reference_col}{linebreak}to{linebreak}{col}'
        if name in df.columns:
            log(f'WARNING: column "{name}" already exists, overwriting',
                'dk.date_delta', verbosity)

        #difference only works with pd.NA,
        #but x.days only works with pd.NaT.
        #_fix_nas converts accordingly
        col_formatted = df[col].apply(date_).apply(_fix_nas)
        col_diff = col_formatted - df['reference_date']
        df[name] = (
            col_diff
            .fillna(pd.NaT)  #type:ignore (pylance doesnt know date_ enables this)
            .apply(lambda x: x.days)
            )

    return df


def _fix_nas(x):
    return pd.NA if x is pd.NaT else x




def date_table(
        df: pd.DataFrame,
        reference_col: str = None,
        uid: str = None,
        upper: int = None,
        lower: int = None,
        start_at_day1: bool = True,
        schedule: dict[int, str] = None,
        filler: str = '.',
        linebreak: str = '\n',
        verbosity: int = 3,
        ) -> pd.DataFrame | pd.io.formats.style.Styler:
    """
    arranges all dates into a table,
    with positions relative to a
    reference date or col.
    """

    if reference_col is None:
        msg = 'ERROR: no reference column provided'
        log(msg, 'dk.date_delta', verbosity)
        return pd.DataFrame()

    df = df.copy()
    if uid:
        df.index = df[uid]
    df = df.map(date_).convert_dtypes()

    for col in df.columns:
        if df[col].isna().all():
            if col == reference_col:
                msg = f'WARNING: no dates found in reference col "{reference_col}"'
                log(msg, 'dk.date_delta', verbosity)
            else:
                df.drop(columns=col, inplace=True)

    reference = df[reference_col].apply(date_).apply(_fix_nas)

    blanks = {col: pd.NaT for col in df.columns}
    deltas = pd.DataFrame(
        blanks,
        index=df.index,
        )

    for col in df.columns:
        #difference only works with pd.NA,
        #but x.days only works with pd.NaT.
        #_fix_nas converts accordingly
        col_formatted = df[col].apply(date_).apply(_fix_nas)
        col_diff = col_formatted - reference
        deltas[col] = (
            col_diff
            .fillna(pd.NaT)  #type:ignore (pylance doesnt know date_ enables this)
            .apply(lambda x: x.days)
            )

    deltas = deltas.T

    if upper is None:
        upper = int(deltas.fillna(0).max().max()) + 1
    if lower is None:
        lower = int(deltas.fillna(0).min().min())

    days = list(range(lower, upper + 1))
    if start_at_day1:
        days.remove(0)
    else:
        days.pop(-1)
    days_df = pd.DataFrame({'days': days})

    df_timeline = days_df.copy()
    if schedule is not None:
        df_schedule = pd.DataFrame({
            'days': list(schedule.keys()),
            'planned': list(schedule.values()),
            })
        df_timeline = df_timeline.merge(
            df_schedule,
            on='days',
            how='left',
            ).fillna('')

    for col in deltas.columns:
        events = pd.DataFrame({
            'days': deltas[col].astype('Int64'),
            col: deltas.index,
            })

        if start_at_day1:
            events = _shift_day0(events)

        merged = days_df.copy().merge(events, on='days', how='left').fillna(filler)
        collapsed = collapse(
            merged,
            on='days',
            template_item='{item}' + linebreak,
            )
        df_timeline = df_timeline.merge(
            collapsed,
            on='days',
            how='left',
            )

    cols_records = [
        col for col
        in df_timeline.columns
        if col not in ('meta', 'days', 'planned')
        ]
    df_timeline.insert(
        loc=0,
        column='meta',
        value=''
        )
    has_event = df_timeline[cols_records] != filler
    records_per_row = has_event.sum(axis='columns')
    rows_with_records = records_per_row > 0
    summary = 'records: ' + records_per_row.astype(str)
    df_timeline.loc[rows_with_records, 'meta'] = summary
    df_timeline['meta'] = df_timeline['meta'].fillna('')

    if schedule is not None:
        df_timeline = _highlight_schedule(df_timeline, schedule)

    return df_timeline


def _shift_day0(df: pd.DataFrame) -> pd.DataFrame:
    if 'days' not in df.columns:
        return df
    if 0 not in df['days'].values:
        return df
    mask_positive = df['days'] >= 0
    df.loc[mask_positive, 'days'] += 1
    return df


def _highlight_schedule(
        df: pd.DataFrame,
        schedule: dict,
        ) -> pd.io.formats.style.Styler:

    days_highlight = list(schedule.keys())

    df_style = pd.DataFrame(
        'text-align: left;',
        columns=df.columns,
        index=df.index
        )

    mask_highlight = df['days'].isin(days_highlight)
    df_style.loc[mask_highlight, :] += f'background-color: {GREEN_LIGHT};'

    df_styled = df.style.apply(
        lambda x: df_style,
        axis=None,
        )

    return df_styled




def deduplicate(
        obj,
        name='object',
        rename_all=True,
        start_at_1=True,
        verbosity=3,
        ):
    """
    make values unique by appending consecutive numeric suffixes.

    Parameters
    ----------
    obj : object
        object convertible to a pandas Series.
    name : str, default 'object'
        name used in diagnostic messages.
    rename_all : bool, default True
        whether to rename all values, not just duplicates.
    start_at_1 : bool, default True
        whether to start numbering at 0 or 1.
    verbosity : int, default 3
        logging verbosity level.

    Returns
    -------
    object
        deduplicated object, converted back to its original type when
        possible. Values are converted to strings during processing.
    """

    obj = copy.deepcopy(obj)
    class_orig = obj.__class__
    obj = _to_series(obj)

    #Values can only be deduplicated if index is unique
    if not obj.index.is_unique:
        msg = (
            f'info: duplicates found in index of {name}.'
            ' deduplicating by appending consecutive numbers.'
            )
        log(msg, 'dk.pandas.deduplicate', verbosity)
        obj.index = _deduplicate(
            _to_series(obj.index),
            rename_all,
            start_at_1,
            )

    if rename_all:
        obj = _deduplicate(
            obj,
            rename_all,
            start_at_1,
            )
        rounds = 1
    else:
        rounds = 0

    while not obj.is_unique:
        if rounds == 0:
            msg = (
                f'debug: duplicates found in {name}.'
                ' deduplicating by appending consecutive numbers.'
                )
        else:
            msg = (
                f'debug: duplicates still found in {name} after'
                f' {rounds} deduplication rounds.'
                ' deduplicating again by appending consecutive numbers.'
                )
        log(msg, 'dk.pandas.deduplicate', verbosity)
        obj = _deduplicate(
            obj,
            rename_all,
            start_at_1,
            )
        rounds += 1

    if not isinstance(obj, class_orig):
        try:
            obj = class_orig(obj)
        except Exception as e:
            msg = (
                'Error: could not convert deduplicated object'
                f' back to original type {class_orig}: {e}'
                )
            log(msg, 'dk.pandas.deduplicate', verbosity)

    return obj


def _to_series(obj, verbosity=3):
    try:
        obj = pd.Series(obj, dtype=str)
    except Exception as e:
        msg = (
            'Error: could not convert input of type'
            f' {type(obj)} to Series: {e}'
            )
        log(msg, 'dk.pandas._to_series', verbosity)
    return obj


def _deduplicate(series, rename_all=True, start_at_1=True):
    cumulative_count = series.groupby(series).cumcount()
    if rename_all:
        if start_at_1:
            cumulative_count += 1
        series = (
            series.astype(str)
            + '_'
            + cumulative_count.astype(str)
            )
    else:
        duplicates_mask = series.index[cumulative_count > 0]
        duplicates = series[duplicates_mask]
        duplicates_new = (
            duplicates.astype(str)
            + '_'
            + cumulative_count[duplicates_mask].astype(str)
            )
        series[duplicates_mask] = duplicates_new
    return series



def collapse(
        df: pd.DataFrame,
        on: str,
        template_col='{colname}',
        template_item='#{counter}: {item}\n',
        ):
    """
    collapse repeated row values into numbered multiline cols.

    Returns
    -------
    pandas.DataFrame
        df with one row per value in ``on``.
    """
    df = df.groupby(on).agg(list)
    df = df.map(lambda x: _to_lines(x, template_item))
    df.columns = [template_col.format(colname=col) for col in df.columns]
    df.insert(0, on, df.index)
    df.reset_index(drop=True, inplace=True)
    return df


def _to_lines(
        x,
        template_item='#{counter}: {item}\n',
        ):
    if not isinstance(x, list):
        return x
    if len(x) == 1:
        return x[0]
    else:
        x_str = ''
        for i, item in enumerate(x):
            x_str += template_item.format(counter=i + 1, item=item)
    return x_str



def embed(
        df: pd.DataFrame,
        on: str,
        colname='',
        template='{colname} #{counter}',
        line_start='',
        separator=':',
        spacer='\u00A0',  #non-breaking space
        line_stop='\n',
        ):
    """
    combine repeated row values into formatted multiline cols.

    Returns
    -------
    pandas.DataFrame
        flattened df with one row per value in ``on``.
    """

    combined_cols_str = pd.DataFrame({
        on: df[on],
        colname: ''
        })

    len_max_cols = (
        df
        .columns
        .to_series()
        .astype('string')
        .str
        .len()
        .max()
        )
    for col in df.columns:
        if col == on:
            continue
        len_spacer = (
            len_max_cols
            - len(str(col))
            + 1
            )
        combined_cols_str[colname] += (
            line_start
            + str(col)
            + separator
            + spacer * len_spacer
            + df[col].apply(str)
            + line_stop
            )

    df_new = flatten(
        combined_cols_str,
        on=on,
        template=template,
        )

    return df_new



def flatten(
        df: pd.DataFrame,
        on: str,
        template='{colname} #{counter}',
        ):
    """
    arrange values from repeated rows into numbered cols.
    in contrast to :func:`stagger`, repeated 3 repeated
    values from cols a, b, c are arranged into new cols:
    a1, a2, a3, b1, b2, b3, c1, c2, c3.

    Parameters
    ----------
    df : pandas.DataFrame
        df containing repeated rows.
    on : str
        col used to group rows.
    template : str, default '{colname} #{counter}'
        format string for generated col names.

    Returns
    -------
    pandas.DataFrame
        df with one row per group and numbered value cols.
    """

    #aggregate repeating rows into lists
    df = df.groupby(on).agg(list)

    #create new cols from lists
    cols_new = []
    for col in df.columns:
        n_max = df[col].apply(lambda x: len(x)).max()
        cols_flat = [
            template.format(counter=i + 1, colname=col)
            for i
            in range(n_max)
            ]
        split = pd.DataFrame(df[col].to_list(), columns=cols_flat)
        split.index = df.index
        df = df.merge(
            split,
            left_index=True,
            right_index=True,
            how='left',
            )
        cols_new += cols_flat

    df = df[cols_new]
    df.insert(0, on, df.index)
    df.reset_index(drop=True, inplace=True)

    return df



def stagger(
        df: pd.DataFrame,
        on: str,
        template='#{counter} {colname}',
        separator_col='#{counter}'
        ):
    """
    arrange values from repeated rows into numbered cols.
    in contrast to :func:`flatten`, repeated 3 repeated
    values from cols a, b, c are arranged into new cols:
    #1, a1, b1, c1, #2, a2, b2, c2, #3, a3, b3, c3

    Parameters
    ----------
    df : pandas.DataFrame
        df containing repeated rows.
    on : str
        col used to group rows.
    template : str, default '#{counter} {colname}'
        format string for generated col names.
    separator_col : str or None, default '#{counter}'
        format string for separator cols. use ``None`` to omit them.

    Returns
    -------
    pandas.DataFrame
        df with one row per group and repeated values in cols.
    """

    duplicates_max = df[on].value_counts().max()
    df = df.groupby(on).agg(list)
    cols = df.columns.tolist()
    df_new = pd.DataFrame(
        df.index,
        index=df.index,
        )

    for i in range(duplicates_max):
        if separator_col:
            separator_vals = pd.Series(
                '',
                index=df.index,
                name=separator_col.format(counter=i + 1),
                )
            df_new = pd.concat([df_new, separator_vals], axis=1)
        for col in cols:
            if col == on:
                continue
            col_new = df[col].apply(lambda x: _get_from_list(x, i))
            col_new.name = template.format(counter=i + 1, colname=col)
            df_new = pd.concat([df_new, col_new], axis=1)

    df_new.reset_index(drop=True, inplace=True)

    return df_new


def _get_from_list(x, i):
    if len(x) > i:
        return x[i]
    else:
        return None



def transpose(
        df: pd.DataFrame,
        header='uid',
        ) -> pd.DataFrame:
    """
    transpose a df while preserving a designated header col.

    Parameters
    ----------
    df : pandas.DataFrame
        df to transpose.
    header : str, default 'uid'
        col used as the new header identifier.

    Returns
    -------
    pandas.DataFrame
        transposed df.
    """

    cols_old = df.columns
    cols_new = df[header].values

    df = df.T
    df.columns = cols_new
    df.insert(0, header, cols_old)
    df.drop(header, axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df



def split_col(
        df: pd.DataFrame,
        col: str = 'uid',
        sep: str = '::\n',
        new1: str = None,
        new2: str = 'label',
        ):

    if col not in df.columns:
        log(f'ERROR: no col named "{col}" found')
        return df
    elif df.columns.tolist().count(col) > 1:
        log(f'ERROR: multiple cols named "{col}" found')
        return df

    df = df.copy()
    pos = df.columns.get_loc(col)
    splits = df[col].str.partition(sep)

    df.drop(columns=[col], inplace=True)
    if new1 is None:
        new1 = col
    elif new1 in df.columns:
        log(f'WARNING: Col {new1} already exists, choosing new name.')
        new1 = ensure_unique_string(new1, df.columns.tolist())
    if new2 in df.columns:
        log(f'WARNING: Col {new2} already exists, choosing new name.')
        new2 = ensure_unique_string(new2, df.columns.tolist() + [new1])

    df.insert(pos, new1, splits[0])  #type: ignore
    df.insert(pos + 1, new2, splits[2])  #type: ignore

    return df



def stack(
        df: pd.DataFrame,
        uid: str,
        col_pattern: str = r'(?P<col>.+)_(?P<subid>.+)',
        uid_template: str = '{uid}_{subid}',
        cols_keep: list[str] | None = None,
        dropna: bool = True,
        sort: bool = True,
        verbosity: int = 3,
        ) -> pd.DataFrame:

    df = df.copy()
    df[uid] = df[uid].astype('string')
    _stack_check_uid_unique1(df, uid, verbosity)

    uid_old = ensure_unique_string(uid, df.columns)
    df.set_index(uid, inplace=True)
    df.index.name = uid_old
    cols_keep = list_(cols_keep)
    cols_stack = [col for col in df.columns if col not in cols_keep]

    non_na_vals = int(
        df[cols_stack]
        .notna()
        .sum()
        .sum()
        )

    subdfs = {}
    not_matched = []
    for col_old in cols_stack:
        match = re.match(col_pattern, col_old)
        if match:
            subid_val = match.group('subid')
            col_new = match.group('col')
            if subid_val not in subdfs:
                subdfs[subid_val] = pd.DataFrame()
            subdfs[subid_val][col_new] = df[col_old]
        else:
            not_matched.append(col_old)
    _stack_check_successfull_match(not_matched, verbosity)

    for subid_val in subdfs.keys():
        subdf = subdfs[subid_val]
        if dropna:
            subdf.dropna(
                inplace=True,
                how='all',
                )
        uid_vals = [
            uid_template.format(uid=uid_old, subid=subid_val)
            for uid_old in subdf.index
            ]
        subdf.insert(0, uid, uid_vals)

    df_new = pd.concat(list(subdfs.values()), axis='index')
    df_new = pd.merge(
        df[cols_keep].reset_index(),
        df_new.reset_index(),
        on=uid_old,
        how='right',
        )
    df_new.drop(columns=[uid_old], inplace=True)

    _stack_check_missed_values(df_new, uid, cols_keep, non_na_vals, verbosity)

    if sort:
        df_new.sort_values(by=uid, inplace=True)
    df_new.reset_index(drop=True, inplace=True)
 
    _stack_check_uid_unique2(uid, verbosity, df_new)

    return df_new


def _stack_check_uid_unique1(df, uid, verbosity):
    if not df[uid].is_unique:
        non_unique = df[uid][df[uid].duplicated()].unique()
        msg = (
            f'WARNING: Source uid col "{uid}" '
            f'contains non-unique values: {non_unique}'
            )
        log(msg, 'dk.pandas.stack', verbosity)


def _stack_check_successfull_match(not_matched, verbosity):
    if len(not_matched) > 0:
        msg = (
            'WARNING: Some cols did not '
            f'match col_pattern: {not_matched}'
            )
        log(msg, 'dk.pandas.stack', verbosity)


def _stack_check_missed_values(df_new, uid, cols_keep, non_na_vals1, verbosity):
    cols_stacked = [
            col for col
            in df_new.columns
            if col not in cols_keep + [uid]
            ]
    non_na_vals2 = int(
            df_new[cols_stacked]
            .notna()
            .sum()
            .sum()
            )
    if non_na_vals1 != non_na_vals2:
        msg = (
                f'WARNING: Non-NA value mismatch: '
                f'before={non_na_vals1}, after={non_na_vals2}'
                )
        log(msg, 'dk.pandas.stack', verbosity)


def _stack_check_uid_unique2(uid, verbosity, df_new):
    if not df_new[uid].is_unique:
        non_unique = df_new[uid][df_new[uid].duplicated()].unique()
        msg = (
            f'WARNING: Result uid col "{uid}" '
            f'contains non-unique values: {non_unique}'
            )
        log(msg, 'dk.pandas.stack', verbosity)



def unstack(
        df: pd.DataFrame,
        uid: str,
        uid_pattern: str = r'(?P<uid>.+)_(?P<subid>.+)',
        col_template: str = '{col}_{subid}',
        cols_keep: list[str] | None = None,
        stagger: bool = True,
        verbosity: int = 3,
        ) -> pd.DataFrame:

    df = df.copy()
    df[uid] = df[uid].astype('string')
    _unstack_check_uid_unique(df, uid, verbosity)

    ids = df[uid].str.extract(uid_pattern)
    expected_cols = ['uid', 'subid']
    _unstack_check_successfull_extraction(df, uid, ids, expected_cols, verbosity)


    ids.set_index('uid', inplace=True)
    df[uid] = ids.index
    df.set_index(uid, inplace=True)
    subid_col = ids['subid']
    subid_vals = subid_col.unique()
    cols_keep = list_(cols_keep)
    cols_unstack = [col for col in df.columns if col not in cols_keep]

    non_na_vals = int(
        df[cols_unstack]
        .notna()
        .sum()
        .sum()
        )

    cols_unstacked = []
    if stagger:
        for subid_val in subid_vals:
            mask = subid_col == subid_val
            for col_old in cols_unstack:
                col_unstacked = df.loc[mask, col_old]
                col_unstacked.name = col_template.format(col=col_old, subid=subid_val)
                cols_unstacked.append(col_unstacked)
    else:
        for col_old in cols_unstack:
            for subid_val in subid_vals:
                mask = subid_col == subid_val
                col_unstacked = df.loc[mask, col_old]
                col_unstacked.name = col_template.format(col=col_old, subid=subid_val)
                cols_unstacked.append(col_unstacked)


    df_new = df.loc[~df.index.duplicated(keep='first'), cols_keep]
    for col_unstacked in cols_unstacked:
        df_new = pd.merge(
            df_new,
            col_unstacked,
            left_index=True,
            right_index=True,
            how='left'
            )

    _unstack_check_missed_values(uid, cols_keep, verbosity, non_na_vals, df_new)

    df_new.reset_index(inplace=True)

    return df_new


def _unstack_check_uid_unique(df, uid, verbosity):
    if not df[uid].is_unique:
        non_unique = (
            df[uid]
            [df[uid].duplicated()]
            .unique()
            .tolist()
            )
        msg = (
            f'INFO: deduplicating non-unique values '
            f'in source uid col "{uid}": {non_unique}'
            )
        log(msg, 'dk.pandas.unstack', verbosity)
        df[uid] = deduplicate(df[uid])


def _unstack_check_successfull_extraction(df, uid, ids, expected_cols, verbosity):
    if list(ids.columns) != expected_cols:
        msg = (
            'WARNING: uid pattern must contain exactly 2 named '
            'match groups, one called uid and one called subid. '
            'use the subid group in col_template.'
            )
        log(msg, 'dk.pandas.unstack', verbosity)
    else:
        uid_isna = ids.iloc[:, 0].isna()
        uids_unmatched = df.loc[uid_isna, uid].tolist()
        if uid_isna.any():
            msg = (
                'WARNING: Some uids did not match '
                f'uid_pattern: {uids_unmatched}'
                )
            log(msg, 'dk.pandas.unstack', verbosity)


def _unstack_check_missed_values(uid, cols_keep, verbosity, non_na_vals1, df_new):
    cols_stacked = [
        col for col
        in df_new.columns
        if col not in cols_keep + [uid]
        ]
    non_na_vals2 = int(
        df_new[cols_stacked]
        .notna()
        .sum()
        .sum()
        )
    if non_na_vals1 != non_na_vals2:
        msg = (
            'WARNING: Non-NA value mismatch: '
            f'before={non_na_vals1}, after={non_na_vals2}'
            )
        log(msg, 'dk.pandas.unstack', verbosity)
