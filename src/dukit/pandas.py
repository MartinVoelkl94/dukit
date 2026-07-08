
import pandas as pd
import numpy as np
import datetime
from .util import log


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
            10001,
            10001,
            20001,
            20001,
            20001,
            30001,
            ],
        'name': [
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
def merge(
        left: pd.DataFrame,
        right: pd.DataFrame,
        on='uid',
        mode='flat',
        prefix='',
        line_start='',
        line_stop='\n',
        transpose=False,
        verbosity=3,
        ):
    r"""
    left join on 2 dfs with preprocessing
    to deal with non-unique keys in right df[on].
    """

    left = left.copy()
    right = right.copy()
    context = 'dk.merge'

    if on not in left.columns:
        msg = f'ERROR: "{on}" is not in left df'
        log(msg, context, verbosity)
        return left

    if on not in right.columns:
        msg = f'Error: "{on}" is not in right df'
        log(msg, context, verbosity)
        return left

    if not left[on].is_unique:
        msg = f'WARNING: "{on}" is not unique in left df'
        log(msg, context, verbosity)

    if right[on].is_unique:
        right.columns = [
            f'{prefix}{col}'
            if col != on
            else col
            for col in right.columns
            ]

    elif mode == 'flat':
        right = _flatten(
            right,
            on,
            prefix,
            )

    elif mode == 'staggered':
        right = _stagger(
            right,
            on,
            prefix,
            )

    elif mode == 'vertical':
        right = _embed(
            right,
            on,
            prefix,
            line_start=line_start,
            line_stop=line_stop,
            )

    elif mode == 'horizontal':
        right = right.groupby(on).agg(list)
        right = right.map(lambda x: _to_lines(x, line_start, line_stop))
        right.columns = [f'{prefix}{col}' for col in right.columns]

    else:
        msg = f'ERROR: unknown mode "{mode}"'
        log(msg, context, verbosity)
        return left


    result = pd.merge(
        left,
        right,
        how='left',
        on=on,
        )

    if transpose:
        result = result.T
        result.columns = result.iloc[0]
        result = result.iloc[1:]

    return result



def _flatten(
        df: pd.DataFrame,
        on: str,
        prefix='',
        ):

    #aggregate repeating rows into lists
    df = df.groupby(on).agg(list)

    #create new cols from lists
    cols_new = []
    for col in df.columns:
        n_max = df[col].apply(lambda x: len(x)).max()
        cols_flat = [f'{prefix}{col}_{i + 1}' for i in range(n_max)]
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

    return df



def _embed(
        df: pd.DataFrame,
        on: str,
        prefix='',
        line_start='',
        line_stop='\n',
        ):

    combined_cols_str = pd.DataFrame({
        on: df[on],
        prefix: ''
        })

    for col in df.columns:
        if col == on:
            continue
        combined_cols_str[prefix] += (
            line_start
            + str(col)
            + ': '
            + df[col].apply(str)
            + line_stop
            )

    df_new = _flatten(combined_cols_str, on)
    return df_new



def _to_lines(
        x,
        line_start='',
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



def _get_from_list(x, i):
    if len(x) > i:
        return x[i]
    else:
        return None



def _stagger(
        df: pd.DataFrame,
        on: str,
        prefix='',
        ):

    duplicates_max = df[on].value_counts().max()
    df = df.groupby(on).agg(list)
    cols = df.columns.tolist()
    df_new = pd.DataFrame(
        df.index,
        index=df.index,
        )

    for i in range(duplicates_max):
        for col in cols:
            if col == on:
                continue
            col_new = df[col].apply(lambda x: _get_from_list(x, i))
            col_new.name = f'{prefix}{col}_{i + 1}'
            df_new = pd.concat([df_new, col_new], axis=1)

    df_new.reset_index(drop=True, inplace=True)
    return df_new
