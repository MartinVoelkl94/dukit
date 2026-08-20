
import pandas as pd
import numpy as np
import datetime
import copy
from .utils import log
from .typing import date_

def get_df() -> pd.DataFrame:
    """
    Returns a small sample dataframe containing very messy fake medical data.
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



def get_dfs():
    df1 = pd.DataFrame({
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
    df2 = pd.DataFrame({
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
    return df1, df2




def deduplicate(obj, name='object', verbosity=3):
    """
    Deduplicate entries in object which can be converted
    to pandas Series by appending consecutive numbers.
    Note that the entries are converted to strings in the process.
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
        obj.index = _deduplicate(_to_series(obj.index))

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
        obj = _deduplicate(obj)
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


def _deduplicate(series):
    cumulative_count = series.groupby(series).cumcount()
    duplicates_mask = series.index[cumulative_count > 0]
    duplicates = series[duplicates_mask]
    duplicates_new = (
        duplicates.astype(str)
        + '_'
        + cumulative_count[duplicates_mask].astype(str)
        )
    series[duplicates_mask] = duplicates_new
    return series




def flatten(
        df: pd.DataFrame,
        on: str,
        template='{colname} #{counter}',
        ):

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



def collapse(
        df: pd.DataFrame,
        on: str,
        template='{colname}',
        line_start='#',
        line_stop='\n',
        ):
    df = df.groupby(on).agg(list)
    df = df.map(lambda x: _to_lines(x, line_start, line_stop))
    df.columns = [template.format(colname=col) for col in df.columns]
    df.insert(0, on, df.index)
    df.reset_index(drop=True, inplace=True)
    return df


def _to_lines(
        x,
        line_start='#',
        line_stop='\n',
        ):
    if not isinstance(x, list):
        return x
    if len(x) == 1:
        return x[0]
    else:
        x_str = ''
        for i, item in enumerate(x):
            x_str += f'{line_start}{i + 1}: {item}{line_stop}'
    return x_str



def transpose(
        df: pd.DataFrame,
        header='uid',
        ) -> pd.DataFrame:

    cols_old = df.columns
    cols_new = df[header].values

    df = df.T
    df.columns = cols_new
    df.insert(0, header, cols_old)
    df.drop(header, axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df



def date_delta(
        df: pd.DataFrame,
        reference_date: str | datetime.date | pd.Timestamp = None,
        reference_col: str = None,
        linebreak: str = '<br>',
        verbosity: int = 3,
        ):
    """
    Calculates the number of days
    between a reference date or col
    and all other date cols in the df.
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

    cols_reorder = ['reference_date']
    cols_reorder += [
        col
        for col
        in df.columns
        if col != 'reference_date'
        ]
    df = df[cols_reorder]

    for col in df.columns:
        if col not in cols_dates:
            continue
        if col == 'reference_date':
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
